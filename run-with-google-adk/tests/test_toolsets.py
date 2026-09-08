"""Unit tests for mcp_security_agent.toolsets."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Mock google.adk.tools.mcp_tool.mcp_toolset
mock_mcp_toolset_mod = MagicMock()
mock_adk = MagicMock()
mock_adk_tools = MagicMock()
mock_adk_tools_mcp = MagicMock()

sys.modules["google.adk"] = mock_adk
sys.modules["google.adk.tools"] = mock_adk_tools
sys.modules["google.adk.tools.mcp_tool"] = mock_adk_tools_mcp
sys.modules["google.adk.tools.mcp_tool.mcp_toolset"] = mock_mcp_toolset_mod

from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import build_mcp_toolsets


def test_build_toolsets_none_enabled():
    settings = AgentSettings()
    toolsets = build_mcp_toolsets(settings)
    assert toolsets == []


def test_build_toolsets_stdio_secops_and_scc():
    settings = AgentSettings(LOAD_SECOPS_MCP="Y", LOAD_SCC_MCP="Y")
    mock_mcp_toolset_mod.McpToolset = MagicMock(side_effect=lambda connection_params: f"Toolset({connection_params})")
    
    toolsets = build_mcp_toolsets(settings)
    assert len(toolsets) == 2
    assert mock_mcp_toolset_mod.StdioConnectionParams.call_count == 2
