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


