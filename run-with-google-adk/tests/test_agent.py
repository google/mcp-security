"""Unit tests for mcp_security_agent.agent."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Mock google.adk.agents.llm_agent and google.adk.tools.mcp_tool
mock_llm_agent_mod = MagicMock()
mock_adk = MagicMock()
mock_adk_agents = MagicMock()

sys.modules["google.adk"] = mock_adk
sys.modules["google.adk.agents"] = mock_adk_agents
sys.modules["google.adk.agents.llm_agent"] = mock_llm_agent_mod

from mcp_security_agent.config import AgentSettings
from mcp_security_agent.agent import create_security_agent, SOC_AGENT_SYSTEM_PROMPT


def test_create_security_agent():
    settings = AgentSettings(GOOGLE_MODEL="gemini-2.5-flash")
    mock_agent_instance = MagicMock()
    mock_llm_agent_mod.LlmAgent = MagicMock(return_value=mock_agent_instance)

    agent = create_security_agent(settings)
    assert agent == mock_agent_instance
    mock_llm_agent_mod.LlmAgent.assert_called_once()
    _, kwargs = mock_llm_agent_mod.LlmAgent.call_args
    assert kwargs["name"] == "SecurityOperationsAgent"
    assert kwargs["model"] == "gemini-2.5-flash"
    assert kwargs["instruction"] == SOC_AGENT_SYSTEM_PROMPT
