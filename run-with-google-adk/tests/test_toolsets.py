"""Unit and loopback behavioral tests for mcp_security_agent.toolsets."""

from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import os
import sys
import threading
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import (
    _GoogleCloudMcpAuth,
    _normalized_origin,
    build_mcp_toolsets,
)


@contextmanager
def _loopback_mcp_server(
    tools: list[dict[str, Any]] | None = None,
    require_bearer: bool = False,
    reject_tokens: set[str] | None = None,
):
    """Starts an ephemeral 127.0.0.1 Streamable HTTP JSON-RPC MCP server."""
    captured_requests: list[dict[str, Any]] = []
    rejected = set(reject_tokens or ())
    tool_defs = tools or [
        {
            "name": "ping_tool",
            "description": "Loopback test tool.",
            "inputSchema": {"type": "object", "properties": {}},
        }
    ]

    class _Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw) if raw else {}
            headers_lower = {k.lower(): v for k, v in self.headers.items()}
            captured_requests.append(
                {
                    "path": self.path,
                    "method": payload.get("method"),
                    "headers": headers_lower,
                }
            )

            auth_hdr = headers_lower.get("authorization", "")
            bearer = auth_hdr[7:] if auth_hdr.startswith("Bearer ") else ""
            if require_bearer and (not bearer or bearer in rejected):
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error":"missing or revoked bearer token"}')
                return

            method = payload.get("method")
            msg_id = payload.get("id")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2025",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "loopback-mcp", "version": "1.0.0"},
                    },
                }
                resp["jsonrpc"] = "2.0"
            elif method == "notifications/initialized":
                self.send_response(202)
                self.end_headers()
                return
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"tools": tool_defs},
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}

            encoded = json.dumps(resp).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_DELETE(self) -> None:  # noqa: N802
            self.send_response(204)
            self.end_headers()

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        yield f"http://{host}:{port}", captured_requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_build_toolsets_none_enabled():
    with patch.dict(os.environ, {}, clear=True):
        settings = AgentSettings(_env_file=None)
        toolsets = build_mcp_toolsets(settings)
        assert toolsets == []


def test_build_toolsets_stdio_secops_and_scc():
    with patch.dict(os.environ, {}, clear=True):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.McpToolset", side_effect=lambda connection_params: f"Toolset({connection_params})"), \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StdioConnectionParams") as mock_params:
            settings = AgentSettings(_env_file=None, LOAD_SECOPS_MCP="Y", LOAD_SCC_MCP="Y")
            toolsets = build_mcp_toolsets(settings)
            assert len(toolsets) == 2
            assert mock_params.call_count == 2


def test_build_toolsets_stdio_env_propagation():
    with patch.dict(os.environ, {}, clear=True):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.McpToolset", side_effect=lambda connection_params: f"Toolset({connection_params})"), \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StdioConnectionParams") as mock_params:
            settings = AgentSettings(
                _env_file=None,
                LOAD_SECOPS_MCP="Y",
                CHRONICLE_PROJECT_ID="chronicle-tenant-project",
                GOOGLE_CLOUD_PROJECT="gcp-scc-project",
                CHRONICLE_CUSTOMER_ID="cust-1234",
                CHRONICLE_REGION="europe",
                SECOPS_SA_PATH="/path/to/secops_sa.json",
                SECOPS_IMPERSONATE_SERVICE_ACCOUNT="sa@chronicle.iam.gserviceaccount.com",
                VT_APIKEY="vt-key-999",
                SOAR_URL="https://soar.domain.com",
                SOAR_APP_KEY="soar-app-key-888",
            )
            toolsets = build_mcp_toolsets(settings)
            assert len(toolsets) == 3
            assert mock_params.call_count == 3
            call_kwargs = mock_params.call_args.kwargs
            server_params = call_kwargs["server_params"]
            env = server_params.env
            assert env["CHRONICLE_PROJECT_ID"] == "chronicle-tenant-project"
            assert env["GOOGLE_CLOUD_PROJECT"] == "gcp-scc-project"
            assert env["CHRONICLE_CUSTOMER_ID"] == "cust-1234"
            assert env["CHRONICLE_REGION"] == "europe"
            assert env["SECOPS_SA_PATH"] == "/path/to/secops_sa.json"
            assert env["SECOPS_IMPERSONATE_SERVICE_ACCOUNT"] == "sa@chronicle.iam.gserviceaccount.com"
            assert env["VT_APIKEY"] == "vt-key-999"
            assert env["SOAR_URL"] == "https://soar.domain.com"
            assert env["SOAR_APP_KEY"] == "soar-app-key-888"
            assert env["GOOGLE_API_USE_CLIENT_CERTIFICATE"] == "false"
            assert env["GOOGLE_API_USE_MTLS_ENDPOINT"] == "never"


def test_build_toolsets_uv_fallback_to_sys_executable():
    with patch.dict(os.environ, {}, clear=True), patch("shutil.which", return_value=None):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.McpToolset", side_effect=lambda connection_params: f"Toolset({connection_params})"), \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StdioConnectionParams") as mock_params:
            settings = AgentSettings(_env_file=None, LOAD_SECOPS_MCP="Y")
            toolsets = build_mcp_toolsets(settings)
            assert len(toolsets) == 1
            call_kwargs = mock_params.call_args.kwargs
            server_params = call_kwargs["server_params"]
            assert server_params.command == sys.executable
            assert "secops_mcp/server.py" in server_params.args[0]
            assert "PYTHONPATH" in server_params.env


@pytest.mark.asyncio
async def test_remote_gti_loopback_normalizes_slash_sends_apikey_and_preserves_accept():
    with _loopback_mcp_server() as (base_url, captured), patch.dict(os.environ, {}, clear=True):
        settings = AgentSettings(
            _env_file=None,
            GTI_MCP_URL=f"{base_url}/api/v3/agentspace/mcp",
            VT_APIKEY="vt-loopback-key",
        )
        toolsets = build_mcp_toolsets(settings)
        assert len(toolsets) == 1
        ts = toolsets[0]
        try:
            tools = await ts.get_tools()
            assert [t.name for t in tools] == ["ping_tool"]
        finally:
            await ts.close()

    assert len(captured) >= 2
    for req in captured:
        assert req["path"] == "/api/v3/agentspace/mcp/"
        assert req["headers"]["x-apikey"] == "vt-loopback-key"
        accept = req["headers"].get("accept", "")
        assert "application/json" in accept
        assert "text/event-stream" in accept


@pytest.mark.asyncio
async def test_remote_gti_client_disables_cross_origin_redirect_header_leak():
    sink_received: list[dict[str, str]] = []

    class _SinkHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

        def do_POST(self) -> None:  # noqa: N802
            sink_received.append({k.lower(): v for k, v in self.headers.items()})
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()

    sink = ThreadingHTTPServer(("127.0.0.1", 0), _SinkHandler)
    threading.Thread(target=sink.serve_forever, daemon=True).start()

    class _RedirectHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

        def do_POST(self) -> None:  # noqa: N802
            self.send_response(307)
            self.send_header("Location", f"http://localhost:{sink.server_port}/mcp/")
            self.send_header("Content-Length", "0")
            self.end_headers()

    redir = ThreadingHTTPServer(("127.0.0.1", 0), _RedirectHandler)
    threading.Thread(target=redir.serve_forever, daemon=True).start()
    try:
        with patch.dict(os.environ, {}, clear=True):
            settings = AgentSettings(
                _env_file=None,
                GTI_MCP_URL=f"http://127.0.0.1:{redir.server_port}/custom-mcp",
                VT_APIKEY="secret-vt-key-no-redirect",
            )
            (ts,) = build_mcp_toolsets(settings)
            factory = ts._connection_params.httpx_client_factory
            assert factory is not None
            async with factory(headers={"x-apikey": "secret-vt-key-no-redirect"}) as client:
                assert client.follow_redirects is False
                resp = await client.post(f"http://127.0.0.1:{redir.server_port}/custom-mcp", json={})
                assert resp.status_code == 307
            await ts.close()
        assert sink_received == []
    finally:
        redir.shutdown()
        redir.server_close()
        sink.shutdown()
        sink.server_close()


@pytest.mark.asyncio
async def test_remote_secops_loopback_authenticates_none_and_rotates_token_on_one_session():
    with _loopback_mcp_server(
        require_bearer=True,
        reject_tokens={"revoked-token"},
    ) as (base_url, captured), patch.dict(os.environ, {}, clear=True):
        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.token = None
        mock_creds.quota_project_id = "adc-fallback-quota-proj"

        tokens = iter(["initial-token-1", "rotated-token-2", "forced-401-token-3"])

        def _refresh_side_effect(_request):
            mock_creds.token = next(tokens)
            mock_creds.valid = True
            mock_creds.expired = False

        mock_creds.refresh.side_effect = _refresh_side_effect

        with patch("google.auth.default", return_value=(mock_creds, "detected-proj")) as mock_auth_default:
            settings = AgentSettings(
                _env_file=None,
                SECOPS_MCP_URL=f"{base_url}/mcp",
            )
            toolsets = build_mcp_toolsets(settings)
            assert len(toolsets) == 1
            ts = toolsets[0]
            try:
                # 1. readonly_context=None (adk web / bare get_tools) authenticates + falls back to ADC quota_project_id
                tools_none = await ts.get_tools()
                assert [t.name for t in tools_none] == ["ping_tool"]
                assert mock_auth_default.call_count == 1
                assert mock_creds.refresh.call_count == 1

                # 2. Cached valid token is reused without extra refresh()
                tools_ctx = await ts.get_tools(readonly_context=MagicMock())
                assert [t.name for t in tools_ctx] == ["ping_tool"]
                assert mock_creds.refresh.call_count == 1

                # 3. After 60m expiry, both ctx and None calls send the rotated token on 1 pooled session
                mock_creds.expired = True
                mock_creds.valid = False
                await ts.get_tools(readonly_context=MagicMock())
                await ts.get_tools()
                assert mock_creds.refresh.call_count == 2
                assert len(ts._mcp_session_manager._sessions) == 1

                # 4. If cached token is revoked server-side (401 while valid=True), auth flow forces 1 refresh
                mock_creds.token = "revoked-token"
                mock_creds.valid = True
                mock_creds.expired = False
                await ts.get_tools()
                assert mock_creds.refresh.call_count == 3
            finally:
                await ts.close()

    list_calls = [r for r in captured if r["method"] == "tools/list"]
    assert list_calls[0]["headers"]["authorization"] == "Bearer initial-token-1"
    assert list_calls[0]["headers"]["x-goog-user-project"] == "adc-fallback-quota-proj"
    assert list_calls[1]["headers"]["authorization"] == "Bearer initial-token-1"
    assert list_calls[2]["headers"]["authorization"] == "Bearer rotated-token-2"
    assert list_calls[3]["headers"]["authorization"] == "Bearer rotated-token-2"
    assert list_calls[-1]["headers"]["authorization"] == "Bearer forced-401-token-3"


@pytest.mark.asyncio
async def test_google_cloud_mcp_auth_explicit_443_origin_pinning_and_atomic_impersonation():
    source_creds = MagicMock(valid=True, expired=False, token="source-access-token", quota_project_id=None)
    impersonated_creds = MagicMock(valid=True, expired=False, token="impersonated-access-token", quota_project_id=None)

    # 1. Explicit :443 normalizes identically to httpx.Request URL (port=None) AND blocks cross-origin leaks
    auth = _GoogleCloudMcpAuth(
        target_origin=_normalized_origin("https://chronicle.us.rep.googleapis.com:443/mcp"),
        quota_project="pinned-quota-proj",
        sa_path="/tmp/secops-sa.json",
        impersonate_sa="target-sa@example.iam.gserviceaccount.com",
    )

    with patch("google.auth.load_credentials_from_file", return_value=(source_creds, "sa-proj")), \
         patch("google.auth.impersonated_credentials.Credentials", return_value=impersonated_creds):
        same_origin_req = httpx.Request("POST", "https://chronicle.us.rep.googleapis.com/mcp")
        flow = auth.async_auth_flow(same_origin_req)
        authed_req = await flow.__anext__()
        await flow.aclose()
        assert authed_req.headers["Authorization"] == "Bearer impersonated-access-token"
        assert authed_req.headers["x-goog-user-project"] == "pinned-quota-proj"

        for cross_url in (
            "https://evil.example.com/mcp",
            "http://chronicle.us.rep.googleapis.com/mcp",
            "https://chronicle.us.rep.googleapis.com:8443/mcp",
        ):
            cross_req = httpx.Request("POST", cross_url)
            cross_flow = auth.async_auth_flow(cross_req)
            forwarded = await cross_flow.__anext__()
            await cross_flow.aclose()
            assert "Authorization" not in forwarded.headers
            assert "x-goog-user-project" not in forwarded.headers

    # 2. Failed impersonation initialization does not cache raw source_creds
    broken_auth = _GoogleCloudMcpAuth(
        target_origin=_normalized_origin("https://chronicle.us.rep.googleapis.com/mcp"),
        sa_path="/tmp/secops-sa.json",
        impersonate_sa="broken-sa@example.iam.gserviceaccount.com",
    )
    with patch("google.auth.load_credentials_from_file", return_value=(source_creds, "sa-proj")), \
         patch("google.auth.impersonated_credentials.Credentials", side_effect=RuntimeError("impersonation failed")):
        for _ in range(2):
            with pytest.raises(RuntimeError, match="impersonation failed"):
                flow_err = broken_auth.async_auth_flow(
                    httpx.Request("POST", "https://chronicle.us.rep.googleapis.com/mcp")
                )
                await flow_err.__anext__()
        assert broken_auth._creds is None


def test_remote_url_validation_and_vt_host_allowlist(caplog):
    with patch.dict(os.environ, {}, clear=True):
        # 1. Cleartext http:// on non-loopback rejected
        s_http = AgentSettings(
            _env_file=None,
            GTI_MCP_URL="http://www.virustotal.com/api/v3/agentspace/mcp/",
            VT_APIKEY="vt-key",
        )
        with pytest.raises(ValueError, match="must use https://"):
            build_mcp_toolsets(s_http)

        # 2. Embedded userinfo rejected without leaking password
        s_userinfo = AgentSettings(
            _env_file=None,
            GTI_MCP_URL="https://user:super-secret-pw@www.virustotal.com/api/v3/agentspace/mcp/",
            VT_APIKEY="vt-key",
        )
        with pytest.raises(ValueError, match="userinfo") as ui_exc:
            build_mcp_toolsets(s_userinfo)
        assert "super-secret-pw" not in str(ui_exc.value)

        # 3. Non-googleapis.com SECOPS_MCP_URL rejected before leaking GCP ADC tokens
        s_non_gcp = AgentSettings(
            _env_file=None,
            SECOPS_MCP_URL="https://evil.example.com/mcp?secret=do-not-log",
            CHRONICLE_PROJECT_ID="my-proj",
        )
        with pytest.raises(ValueError, match="googleapis.com") as exc_info:
            build_mcp_toolsets(s_non_gcp)
        assert "do-not-log" not in str(exc_info.value)

        # 4. Non-VirusTotal host and bare apex virustotal.com do NOT receive x-apikey
        caplog.set_level(logging.WARNING)
        for untrusted_url in (
            "https://evil.example.com/mcp",
            "https://virustotal.com/api/v3/agentspace/mcp/",
        ):
            s_untrusted = AgentSettings(
                _env_file=None,
                GTI_MCP_URL=untrusted_url,
                VT_APIKEY="vt-secret-key",
            )
            (ts_untrusted,) = build_mcp_toolsets(s_untrusted)
            assert ts_untrusted._connection_params.headers is None

        # 5. Standard VT_APIKEY is skipped with warning when GTI_MCP_URL targets ai.virustotal.com,
        # while a vtai_... Agent Token IS attached via x-apikey
        s_vtai_bad = AgentSettings(
            _env_file=None,
            GTI_MCP_URL="https://ai.virustotal.com/mcp?token=redact-me",
            VT_APIKEY="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        )
        (ts_vtai_bad,) = build_mcp_toolsets(s_vtai_bad)
        assert ts_vtai_bad._connection_params.headers is None
        assert any("Skipping non-VTAI VT_APIKEY" in rec.message for rec in caplog.records)
        assert all("redact-me" not in rec.getMessage() for rec in caplog.records)

        s_vtai_ok = AgentSettings(
            _env_file=None,
            GTI_MCP_URL="https://ai.virustotal.com/mcp",
            VT_APIKEY="vtai_test_token_12345",
        )
        (ts_vtai_ok,) = build_mcp_toolsets(s_vtai_ok)
        assert ts_vtai_ok._connection_params.headers == {"x-apikey": "vtai_test_token_12345"}


def test_remote_scc_auto_enables_and_soar_url_preserves_stdio(caplog):
    from google.adk.tools.mcp_tool.mcp_toolset import (
        StdioConnectionParams,
        StreamableHTTPConnectionParams,
    )

    caplog.set_level(logging.WARNING)
    with patch.dict(os.environ, {}, clear=True):
        settings = AgentSettings(
            _env_file=None,
            SCC_MCP_URL="https://securitycenter.googleapis.com/mcp/investigate",
            GOOGLE_CLOUD_PROJECT="my-scc-proj",
            SECOPS_SOAR_MCP_URL="https://soar-gateway.example.com/mcp?token=redact-soar",
            SOAR_URL="https://tenant.siemplify-soar.com",
            SOAR_APP_KEY="soar-app-key",
        )
        toolsets = build_mcp_toolsets(settings)
        assert len(toolsets) == 2
        scc_conn = toolsets[0]._connection_params
        soar_conn = toolsets[1]._connection_params
        assert isinstance(scc_conn, StreamableHTTPConnectionParams)
        assert scc_conn.url == "https://securitycenter.googleapis.com/mcp/investigate"
        assert scc_conn.httpx_client_factory is not None
        assert isinstance(soar_conn, StdioConnectionParams)
        assert any("SECOPS_SOAR_MCP_URL" in rec.getMessage() for rec in caplog.records)
        assert all("redact-soar" not in rec.getMessage() for rec in caplog.records)
