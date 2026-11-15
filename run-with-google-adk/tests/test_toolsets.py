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

import pytest

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import build_mcp_toolsets


@contextmanager
def _loopback_mcp_server(tools: list[dict[str, Any]] | None = None, require_bearer: bool = False):
    """Starts an ephemeral 127.0.0.1 Streamable HTTP JSON-RPC MCP server."""
    captured_requests: list[dict[str, Any]] = []
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

            if require_bearer and not headers_lower.get("authorization", "").startswith("Bearer "):
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error":"missing bearer token"}')
                return

            method = payload.get("method")
            msg_id = payload.get("id")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "loopback-mcp", "version": "1.0.0"},
                    },
                }
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
async def test_remote_secops_loopback_authenticates_none_and_rotates_token_on_one_session():
    with _loopback_mcp_server(require_bearer=True) as (base_url, captured), patch.dict(os.environ, {}, clear=True):
        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.token = None

        tokens = iter(["initial-token-1", "rotated-token-2"])

        def _refresh_side_effect(_request):
            mock_creds.token = next(tokens)
            mock_creds.valid = True
            mock_creds.expired = False

        mock_creds.refresh.side_effect = _refresh_side_effect

        with patch("google.auth.default", return_value=(mock_creds, "detected-proj")) as mock_auth_default:
            settings = AgentSettings(
                _env_file=None,
                SECOPS_MCP_URL=f"{base_url}/mcp",
                CHRONICLE_PROJECT_ID="my-secops-proj",
            )
            toolsets = build_mcp_toolsets(settings)
            assert len(toolsets) == 1
            ts = toolsets[0]
            try:
                # 1. readonly_context=None (adk web / bare get_tools) must authenticate!
                tools_none = await ts.get_tools()
                assert [t.name for t in tools_none] == ["ping_tool"]
                assert mock_auth_default.call_count == 1
                assert mock_creds.refresh.call_count == 1

                # 2. Cached valid token is reused without extra refresh()
                tools_ctx = await ts.get_tools(readonly_context=MagicMock())
                assert [t.name for t in tools_ctx] == ["ping_tool"]
                assert mock_creds.refresh.call_count == 1

                # 3. After 60m expiry, both ctx and None calls send the rotated token on 1 pooled session!
                mock_creds.expired = True
                mock_creds.valid = False
                await ts.get_tools(readonly_context=MagicMock())
                await ts.get_tools()
                assert mock_creds.refresh.call_count == 2
                assert len(ts._mcp_session_manager._sessions) == 1
            finally:
                await ts.close()

    list_calls = [r for r in captured if r["method"] == "tools/list"]
    assert len(list_calls) == 4
    assert list_calls[0]["headers"]["authorization"] == "Bearer initial-token-1"
    assert list_calls[0]["headers"]["x-goog-user-project"] == "my-secops-proj"
    assert list_calls[1]["headers"]["authorization"] == "Bearer initial-token-1"
    assert list_calls[2]["headers"]["authorization"] == "Bearer rotated-token-2"
    assert list_calls[3]["headers"]["authorization"] == "Bearer rotated-token-2"


@pytest.mark.asyncio
async def test_remote_secops_sa_path_impersonation_and_cross_origin_guard():
    with _loopback_mcp_server(require_bearer=True) as (base_url, captured), patch.dict(os.environ, {}, clear=True):
        source_creds = MagicMock(valid=True, expired=False, token="source-access-token")
        impersonated_creds = MagicMock(valid=True, expired=False, token="impersonated-access-token")

        with patch("google.auth.load_credentials_from_file", return_value=(source_creds, "sa-proj")) as mock_load_sa, \
             patch("google.auth.impersonated_credentials.Credentials", return_value=impersonated_creds) as mock_imp:
            settings = AgentSettings(
                _env_file=None,
                SECOPS_MCP_URL=f"{base_url}/mcp",
                SECOPS_SA_PATH="/tmp/secops-sa.json",
                SECOPS_IMPERSONATE_SERVICE_ACCOUNT="target-sa@example.iam.gserviceaccount.com",
                GOOGLE_CLOUD_PROJECT="fallback-quota-proj",
            )
            ts = build_mcp_toolsets(settings)[0]
            try:
                tools = await ts.get_tools()
                assert [t.name for t in tools] == ["ping_tool"]
            finally:
                await ts.close()

            mock_load_sa.assert_called_once_with(
                "/tmp/secops-sa.json",
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            mock_imp.assert_called_once()
            assert captured[-1]["headers"]["authorization"] == "Bearer impersonated-access-token"
            assert captured[-1]["headers"]["x-goog-user-project"] == "fallback-quota-proj"


def test_remote_url_validation_rejects_cleartext_and_non_googleapis_secops(caplog):
    with patch.dict(os.environ, {}, clear=True):
        # 1. Cleartext http:// on non-loopback rejected
        s_http = AgentSettings(
            _env_file=None,
            GTI_MCP_URL="http://www.virustotal.com/api/v3/agentspace/mcp/",
            VT_APIKEY="vt-key",
        )
        with pytest.raises(ValueError, match="must use https://"):
            build_mcp_toolsets(s_http)

        # 2. Non-googleapis.com SECOPS_MCP_URL rejected before leaking GCP ADC tokens
        s_non_gcp = AgentSettings(
            _env_file=None,
            SECOPS_MCP_URL="https://evil.example.com/mcp?secret=do-not-log",
            CHRONICLE_PROJECT_ID="my-proj",
        )
        with pytest.raises(ValueError, match="googleapis.com") as exc_info:
            build_mcp_toolsets(s_non_gcp)
        assert "do-not-log" not in str(exc_info.value)

        # 3. Standard VT_APIKEY is skipped with warning when GTI_MCP_URL targets ai.virustotal.com
        caplog.set_level(logging.WARNING)
        s_vtai = AgentSettings(
            _env_file=None,
            GTI_MCP_URL="https://ai.virustotal.com/mcp?token=redact-me",
            VT_APIKEY="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        )
        ts_list = build_mcp_toolsets(s_vtai)
        assert len(ts_list) == 1
        assert ts_list[0]._connection_params.headers is None
        assert any("Skipping non-VTAI VT_APIKEY" in rec.message for rec in caplog.records)
        assert all("redact-me" not in rec.getMessage() for rec in caplog.records)


def test_remote_scc_and_soar_mcp_urls_register_streamable_http_toolsets():
    with patch.dict(os.environ, {}, clear=True):
        settings = AgentSettings(
            _env_file=None,
            LOAD_SCC_MCP="Y",
            SCC_MCP_URL="https://securitycenter.googleapis.com/mcp",
            GOOGLE_CLOUD_PROJECT="my-scc-proj",
            SECOPS_SOAR_MCP_URL="https://soar-gateway.example.com/mcp",
        )
        toolsets = build_mcp_toolsets(settings)
        assert len(toolsets) == 2
