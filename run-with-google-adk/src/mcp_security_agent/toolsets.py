# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Multi-transport MCP toolsets builder for Google ADK."""

import asyncio
import logging
import os
from pathlib import Path
import threading
from typing import Any, AsyncGenerator
import urllib.parse

import httpx
from mcp_security_agent.config import AgentSettings

logger = logging.getLogger(__name__)

_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
_VT_APIKEY_HOSTS = frozenset({"www.virustotal.com", "virustotal.com", "ai.virustotal.com"})


def _sanitize_url_for_log(raw_url: str) -> str:
    """Strips userinfo, query parameters, and fragments before logging a URL."""
    parsed = urllib.parse.urlparse(raw_url.strip())
    if not parsed.scheme or not parsed.hostname:
        return "<invalid-url>"
    host = f"[{parsed.hostname}]" if ":" in parsed.hostname else parsed.hostname
    port = f":{parsed.port}" if parsed.port else ""
    path = parsed.path or ""
    return f"{parsed.scheme}://{host}{port}{path}"


def _is_google_api_host(hostname: str) -> bool:
    return hostname == "googleapis.com" or hostname.endswith(".googleapis.com")


def _validate_remote_mcp_url(
    raw_url: str,
    setting_name: str,
    *,
    require_google_api_host: bool = False,
) -> tuple[str, urllib.parse.ParseResult, bool]:
    """Validates scheme and hostname boundaries on a configured remote MCP URL."""
    cleaned = raw_url.strip()
    parsed = urllib.parse.urlparse(cleaned)
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        raise ValueError(f"{setting_name} is missing a valid hostname: {_sanitize_url_for_log(cleaned)}")

    is_loopback = hostname in _LOOPBACK_HOSTS
    if parsed.scheme != "https" and not (parsed.scheme == "http" and is_loopback):
        raise ValueError(
            f"{setting_name} must use https:// (or http:// on loopback for local testing), "
            f"got: {_sanitize_url_for_log(cleaned)}"
        )

    if require_google_api_host and not is_loopback and not _is_google_api_host(hostname):
        raise ValueError(
            f"{setting_name} must target a *.googleapis.com endpoint (or loopback for local testing) "
            f"when attaching Google Cloud credentials, got: {_sanitize_url_for_log(cleaned)}"
        )

    return cleaned, parsed, is_loopback


class _GoogleCloudMcpAuth(httpx.Auth):
    """Refreshes Google Cloud OAuth bearer tokens off-loop and pins origin headers."""

    def __init__(
        self,
        *,
        target_origin: tuple[str, str, int | None],
        quota_project: str | None = None,
        sa_path: str | None = None,
        impersonate_sa: str | None = None,
        scopes: list[str] | None = None,
    ) -> None:
        self._target_origin = target_origin
        self._quota_project = quota_project
        self._sa_path = sa_path
        self._impersonate_sa = impersonate_sa
        self._scopes = scopes or ["https://www.googleapis.com/auth/cloud-platform"]
        self._creds: Any = None
        self._lock = threading.Lock()

    def _get_fresh_token_sync(self) -> str:
        import google.auth
        from google.auth.transport.requests import Request

        with self._lock:
            if self._creds is None:
                if self._sa_path:
                    self._creds, _ = google.auth.load_credentials_from_file(
                        self._sa_path,
                        scopes=self._scopes,
                    )
                else:
                    self._creds, _ = google.auth.default(scopes=self._scopes)

                if self._impersonate_sa:
                    from google.auth import impersonated_credentials

                    self._creds = impersonated_credentials.Credentials(
                        source_credentials=self._creds,
                        target_principal=self._impersonate_sa,
                        target_scopes=self._scopes,
                    )

            if not self._creds.valid or self._creds.expired or not self._creds.token:
                self._creds.refresh(Request())

            return str(self._creds.token)

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        req_origin = (
            request.url.scheme,
            (request.url.host or "").lower(),
            request.url.port,
        )
        if req_origin == self._target_origin:
            token = await asyncio.to_thread(self._get_fresh_token_sync)
            request.headers["Authorization"] = f"Bearer {token}"
            if self._quota_project:
                request.headers["x-goog-user-project"] = self._quota_project
        yield request


def _build_google_cloud_client_factory(
    google_auth: _GoogleCloudMcpAuth,
    create_client_fn: Any,
) -> Any:
    def _factory(
        headers: dict[str, str] | None = None,
        timeout: httpx.Timeout | None = None,
        auth: httpx.Auth | None = None,
    ) -> httpx.AsyncClient:
        return create_client_fn(
            headers=headers,
            timeout=timeout,
            auth=auth or google_auth,
        )

    return _factory


def build_mcp_toolsets(settings: AgentSettings) -> list[Any]:
    """Builds and returns all configured MCP toolsets using native ADK transports.

    Args:
        settings: Initialized AgentSettings instance.

    Returns:
        List of initialized MCP toolset objects for the ADK agent.
    """
    toolsets: list[Any] = []
    any_enabled = bool(
        settings.load_secops_mcp
        or settings.load_scc_mcp
        or settings.load_gti_mcp
        or settings.load_secops_soar_mcp
    )

    pkg_dir = Path(__file__).resolve().parents[2]
    repo_root = pkg_dir.parent
    server_dir = repo_root / "server"

    try:
        from google.adk.tools.mcp_tool.mcp_session_manager import create_mcp_http_client
        from google.adk.tools.mcp_tool.mcp_toolset import (
            McpToolset,
            StdioConnectionParams,
            StdioServerParameters,
            StreamableHTTPConnectionParams,
        )
    except ImportError as exc:
        if any_enabled:
            logger.error("Failed to import Google ADK MCP dependencies: %s", exc)
            raise
        logger.warning("google.adk.tools.mcp_tool not available; returning empty toolsets.")
        return toolsets

    def _build_stdio_env() -> dict[str, str]:
        """Constructs environment dictionary for Stdio subprocesses with credential and project isolation."""
        env = dict(os.environ)

        if settings.google_application_credentials:
            env["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
            if "CLOUDSDK_CONFIG" not in env:
                env["CLOUDSDK_CONFIG"] = str(Path(settings.google_application_credentials).parent)

        if settings.secops_sa_path:
            env["SECOPS_SA_PATH"] = settings.secops_sa_path
        if settings.secops_impersonate_service_account:
            env["SECOPS_IMPERSONATE_SERVICE_ACCOUNT"] = settings.secops_impersonate_service_account

        gcp_project = (
            settings.google_cloud_project
            or os.environ.get("GOOGLE_CLOUD_PROJECT")
            or os.environ.get("GCP_PROJECT_ID")
            or settings.chronicle_project_id
        )
        if gcp_project:
            env["GOOGLE_CLOUD_PROJECT"] = gcp_project

        chronicle_project = settings.chronicle_project_id or gcp_project
        if chronicle_project:
            env["CHRONICLE_PROJECT_ID"] = chronicle_project

        if settings.chronicle_customer_id:
            env["CHRONICLE_CUSTOMER_ID"] = settings.chronicle_customer_id
        if settings.chronicle_region:
            env["CHRONICLE_REGION"] = settings.chronicle_region

        if settings.vt_apikey:
            env["VT_APIKEY"] = settings.vt_apikey
        if settings.soar_url:
            env["SOAR_URL"] = settings.soar_url
        if settings.soar_app_key:
            env["SOAR_APP_KEY"] = settings.soar_app_key

        env.setdefault("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        env.setdefault("GOOGLE_API_USE_MTLS_ENDPOINT", "never")
        env.setdefault("CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE", "false")

        return env

    stdio_env = _build_stdio_env()

    def _get_stdio_cmd_args(server_path: Path, script_relpath: str) -> tuple[str, list[str], dict[str, str]]:
        import shutil
        import sys

        env = dict(stdio_env)
        if shutil.which("uv"):
            return "uv", ["--directory", str(server_path), "run", script_relpath], env

        logger.warning(
            "uv executable not found in PATH; falling back to sys.executable (%s) for %s",
            sys.executable,
            server_path.name,
        )
        existing_pp = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{server_path}{os.pathsep}{existing_pp}" if existing_pp else str(server_path)
        script_full = str(server_path / script_relpath)
        return sys.executable, [script_full], env

    sa_path = settings.secops_sa_path.strip() if settings.secops_sa_path else None
    impersonate_sa = (
        settings.secops_impersonate_service_account.strip()
        if settings.secops_impersonate_service_account
        else None
    )

    # 1. Google SecOps SIEM MCP
    if settings.load_secops_mcp:
        if settings.secops_mcp_url and settings.secops_mcp_url.strip():
            secops_url, parsed_secops, _ = _validate_remote_mcp_url(
                settings.secops_mcp_url,
                "SECOPS_MCP_URL",
                require_google_api_host=True,
            )
            logger.info(
                "Configuring SecOps SIEM MCP via Remote URL: %s",
                _sanitize_url_for_log(secops_url),
            )
            quota_project = (
                (settings.chronicle_project_id.strip() if settings.chronicle_project_id else "")
                or (settings.google_cloud_project.strip() if settings.google_cloud_project else "")
            ) or None
            secops_auth = _GoogleCloudMcpAuth(
                target_origin=(
                    parsed_secops.scheme,
                    (parsed_secops.hostname or "").lower(),
                    parsed_secops.port,
                ),
                quota_project=quota_project,
                sa_path=sa_path or None,
                impersonate_sa=impersonate_sa or None,
            )
            conn = StreamableHTTPConnectionParams(
                url=secops_url,
                timeout=max(settings.stdio_timeout_seconds, 60.0),
                sse_read_timeout=max(settings.stdio_timeout_seconds, 300.0),
                httpx_client_factory=_build_google_cloud_client_factory(
                    secops_auth,
                    create_mcp_http_client,
                ),
            )
            toolsets.append(McpToolset(connection_params=conn))
        else:
            secops_dir = server_dir / "secops"
            logger.info("Configuring SecOps SIEM MCP via Stdio subprocess at %s", secops_dir)
            cmd, args, env = _get_stdio_cmd_args(secops_dir, "secops_mcp/server.py")
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=cmd,
                    args=args,
                    env=env,
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    # 2. Security Command Center (SCC) MCP
    if settings.load_scc_mcp:
        if settings.scc_mcp_url and settings.scc_mcp_url.strip():
            scc_url, parsed_scc, _ = _validate_remote_mcp_url(
                settings.scc_mcp_url,
                "SCC_MCP_URL",
                require_google_api_host=True,
            )
            logger.info(
                "Configuring SCC MCP via Remote URL: %s",
                _sanitize_url_for_log(scc_url),
            )
            scc_project = (
                (settings.google_cloud_project.strip() if settings.google_cloud_project else "")
                or (settings.chronicle_project_id.strip() if settings.chronicle_project_id else "")
            ) or None
            scc_auth = _GoogleCloudMcpAuth(
                target_origin=(
                    parsed_scc.scheme,
                    (parsed_scc.hostname or "").lower(),
                    parsed_scc.port,
                ),
                quota_project=scc_project,
                sa_path=sa_path or None,
                impersonate_sa=impersonate_sa or None,
            )
            conn = StreamableHTTPConnectionParams(
                url=scc_url,
                timeout=max(settings.stdio_timeout_seconds, 60.0),
                sse_read_timeout=max(settings.stdio_timeout_seconds, 300.0),
                httpx_client_factory=_build_google_cloud_client_factory(
                    scc_auth,
                    create_mcp_http_client,
                ),
            )
            toolsets.append(McpToolset(connection_params=conn))
        else:
            scc_dir = server_dir / "scc"
            logger.info("Configuring SCC MCP via Stdio subprocess at %s", scc_dir)
            cmd, args, env = _get_stdio_cmd_args(scc_dir, "scc_mcp.py")
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=cmd,
                    args=args,
                    env=env,
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    # 3. Google Threat Intelligence (GTI) MCP
    if settings.load_gti_mcp:
        if settings.gti_mcp_url and settings.gti_mcp_url.strip():
            gti_url, parsed_gti, is_loopback = _validate_remote_mcp_url(
                settings.gti_mcp_url,
                "GTI_MCP_URL",
            )
            if gti_url.rstrip("/").endswith("/api/v3/agentspace/mcp") and not gti_url.endswith("/"):
                gti_url = f"{gti_url}/"
                parsed_gti = urllib.parse.urlparse(gti_url)

            logger.info(
                "Configuring GTI MCP via Remote URL: %s",
                _sanitize_url_for_log(gti_url),
            )
            gti_host = (parsed_gti.hostname or "").lower()
            gti_headers: dict[str, str] = {}
            vt_key = settings.vt_apikey.strip() if settings.vt_apikey else ""
            if vt_key:
                if gti_host == "ai.virustotal.com" and not vt_key.startswith("vtai_"):
                    logger.warning(
                        "Skipping non-VTAI VT_APIKEY header for ai.virustotal.com "
                        "(requires OAuth 2.1 or a vtai_... Agent Token)."
                    )
                elif gti_host in _VT_APIKEY_HOSTS or is_loopback:
                    gti_headers["x-apikey"] = vt_key
                else:
                    logger.warning(
                        "Not attaching VT_APIKEY to non-VirusTotal host %s.",
                        gti_host,
                    )

            if parsed_gti.path.endswith("/api/v3/agentspace/mcp/") and "x-apikey" not in gti_headers:
                logger.warning(
                    "GTI_MCP_URL targets /api/v3/agentspace/mcp/ without VT_APIKEY configured; "
                    "requests will fail with HTTP 401."
                )

            gti_timeout = max(settings.stdio_timeout_seconds, 300.0)
            conn = StreamableHTTPConnectionParams(
                url=gti_url,
                headers=gti_headers or None,
                timeout=gti_timeout,
                sse_read_timeout=gti_timeout,
            )
            toolsets.append(McpToolset(connection_params=conn))
        else:
            gti_dir = server_dir / "gti"
            logger.info("Configuring GTI MCP via Stdio subprocess at %s", gti_dir)
            cmd, args, env = _get_stdio_cmd_args(gti_dir, "gti_mcp/server.py")
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=cmd,
                    args=args,
                    env=env,
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    # 4. SecOps SOAR MCP
    if settings.load_secops_soar_mcp:
        if settings.secops_soar_mcp_url and settings.secops_soar_mcp_url.strip():
            soar_mcp_url, _, _ = _validate_remote_mcp_url(
                settings.secops_soar_mcp_url,
                "SECOPS_SOAR_MCP_URL",
            )
            logger.info(
                "Configuring SecOps SOAR MCP via Remote URL: %s",
                _sanitize_url_for_log(soar_mcp_url),
            )
            conn = StreamableHTTPConnectionParams(
                url=soar_mcp_url,
                timeout=max(settings.stdio_timeout_seconds, 60.0),
                sse_read_timeout=max(settings.stdio_timeout_seconds, 300.0),
            )
            toolsets.append(McpToolset(connection_params=conn))
        else:
            soar_dir = server_dir / "secops-soar"
            logger.info("Configuring SecOps SOAR MCP via Stdio subprocess at %s", soar_dir)
            cmd, args, env = _get_stdio_cmd_args(soar_dir, "secops_soar_mcp/server.py")
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=cmd,
                    args=args,
                    env=env,
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    return toolsets
