"""Unit tests for mcp_security_agent.toolsets."""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import build_mcp_toolsets


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


def test_build_toolsets_remote_gti_normalizes_trailing_slash_and_skips_stdio():
    with patch.dict(os.environ, {}, clear=True):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.McpToolset", side_effect=lambda **kwargs: kwargs) as mock_toolset, \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StreamableHTTPConnectionParams") as mock_http_params, \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StdioConnectionParams") as mock_stdio_params:
            settings = AgentSettings(
                _env_file=None,
                GTI_MCP_URL="https://www.virustotal.com/api/v3/agentspace/mcp",
                VT_APIKEY="vt-key",
            )
            toolsets = build_mcp_toolsets(settings)

            assert len(toolsets) == 1
            assert mock_stdio_params.call_count == 0
            assert mock_http_params.call_count == 1
            http_kwargs = mock_http_params.call_args.kwargs
            assert http_kwargs == {
                "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
                "headers": {"x-apikey": "vt-key"},
                "timeout": 300.0,
                "sse_read_timeout": 300.0,
            }
            assert "Accept" not in http_kwargs["headers"]
            assert mock_toolset.call_args.kwargs == {"connection_params": mock_http_params.return_value}


def test_build_toolsets_remote_secops_header_provider_caches_and_refreshes_adc():
    with patch.dict(os.environ, {}, clear=True):
        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.token = None

        tokens = iter(["test-access-token", "refreshed-test-access-token"])

        def _refresh_side_effect(_request):
            mock_creds.token = next(tokens)
            mock_creds.valid = True
            mock_creds.expired = False

        mock_creds.refresh.side_effect = _refresh_side_effect

        with patch("google.adk.tools.mcp_tool.mcp_toolset.McpToolset", side_effect=lambda **kwargs: kwargs) as mock_toolset, \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StreamableHTTPConnectionParams") as mock_http_params, \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StdioConnectionParams") as mock_stdio_params, \
             patch("google.auth.default", return_value=(mock_creds, "detected-proj")) as mock_auth_default, \
             patch("google.auth.transport.requests.Request") as mock_request_cls:
            settings = AgentSettings(
                _env_file=None,
                SECOPS_MCP_URL="  https://chronicle.us.rep.googleapis.com/mcp  ",
                CHRONICLE_PROJECT_ID="my-proj",
            )
            toolsets = build_mcp_toolsets(settings)

            assert len(toolsets) == 1
            assert mock_stdio_params.call_count == 0
            assert mock_http_params.call_count == 1
            assert mock_http_params.call_args.kwargs == {
                "url": "https://chronicle.us.rep.googleapis.com/mcp",
                "timeout": 60.0,
                "sse_read_timeout": 300.0,
            }

            toolset_kwargs = mock_toolset.call_args.kwargs
            assert toolset_kwargs["connection_params"] is mock_http_params.return_value
            header_provider = toolset_kwargs["header_provider"]
            assert callable(header_provider)

            # First call fetches ADC and refreshes initial token
            headers_first = header_provider(None)
            assert headers_first == {
                "Authorization": "Bearer test-access-token",
                "x-goog-user-project": "my-proj",
            }
            assert mock_auth_default.call_count == 1
            mock_auth_default.assert_called_once_with(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            assert mock_creds.refresh.call_count == 1
            assert mock_request_cls.call_count == 1

            # Second call with valid cached credentials reuses token without refresh()
            headers_second = header_provider(None)
            assert headers_second == {
                "Authorization": "Bearer test-access-token",
                "x-goog-user-project": "my-proj",
            }
            assert mock_auth_default.call_count == 1
            assert mock_creds.refresh.call_count == 1

            # Simulate 60-minute OAuth token expiration; next call refreshes cached creds
            mock_creds.expired = True
            mock_creds.valid = False
            headers_third = header_provider(None)
            assert headers_third == {
                "Authorization": "Bearer refreshed-test-access-token",
                "x-goog-user-project": "my-proj",
            }
            assert mock_auth_default.call_count == 1
            assert mock_creds.refresh.call_count == 2


def test_build_toolsets_remote_secops_sa_path_and_impersonation():
    with patch.dict(os.environ, {}, clear=True):
        source_creds = MagicMock(valid=True, expired=False, token="source-test-access-token")
        impersonated_creds = MagicMock(valid=True, expired=False, token="impersonated-test-access-token")

        with patch("google.adk.tools.mcp_tool.mcp_toolset.McpToolset", side_effect=lambda **kwargs: kwargs), \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StreamableHTTPConnectionParams"), \
             patch("google.adk.tools.mcp_tool.mcp_toolset.StdioConnectionParams") as mock_stdio_params, \
             patch("google.auth.load_credentials_from_file", return_value=(source_creds, "sa-proj")) as mock_load_sa, \
             patch("google.auth.impersonated_credentials.Credentials", return_value=impersonated_creds) as mock_impersonate:
            settings = AgentSettings(
                _env_file=None,
                SECOPS_MCP_URL="https://europe-west2-chronicle.googleapis.com/mcp",
                SECOPS_SA_PATH="/tmp/secops-sa.json",
                SECOPS_IMPERSONATE_SERVICE_ACCOUNT="target-sa@example.iam.gserviceaccount.com",
                GOOGLE_CLOUD_PROJECT="fallback-quota-proj",
            )
            toolsets = build_mcp_toolsets(settings)

            assert len(toolsets) == 1
            assert mock_stdio_params.call_count == 0
            headers = toolsets[0]["header_provider"](None)
            assert headers == {
                "Authorization": "Bearer impersonated-test-access-token",
                "x-goog-user-project": "fallback-quota-proj",
            }
            mock_load_sa.assert_called_once_with(
                "/tmp/secops-sa.json",
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            mock_impersonate.assert_called_once_with(
                source_credentials=source_creds,
                target_principal="target-sa@example.iam.gserviceaccount.com",
                target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            assert impersonated_creds.refresh.call_count == 0


