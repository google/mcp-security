"""Unit tests for mcp_security_agent.cli."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Autonomous Security Operations Center" in result.stdout


def test_cli_info():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "MCP Security Agent v0.2.0" in result.stdout
    assert "Model:" in result.stdout
    assert "Project:" in result.stdout
    assert "ADC:" in result.stdout



def test_cli_chat_query():
    mock_adk_cli = MagicMock()
    async def fake_run_once(*args, **kwargs):
        return 0
    mock_adk_cli.run_once_cli = fake_run_once

    with patch.dict("sys.modules", {"google.adk.cli.cli": mock_adk_cli}):
        result = runner.invoke(app, ["chat", "list 1 page of rules"])
        assert result.exit_code == 0


def test_cli_chat_tool_flags():
    import os
    import mcp_security_agent.agent as agent_mod
    mock_adk_cli = MagicMock()
    async def fake_run_once(*args, **kwargs):
        return 0
    mock_adk_cli.run_once_cli = fake_run_once

    with patch.dict(os.environ, {}, clear=True):
        with patch.dict("sys.modules", {"google.adk.cli.cli": mock_adk_cli}):
            result = runner.invoke(app, ["chat", "--secops", "test query"])
            assert result.exit_code == 0
            assert "Active MCP Toolsets:" in result.stdout
            assert "SecOps SIEM" in result.stdout
            assert len(agent_mod.root_agent.tools) == 1
            assert sys.modules["mcp_security_agent"].root_agent == agent_mod.root_agent

            result_no_secops = runner.invoke(app, ["chat", "--no-secops", "test query"])
            assert result_no_secops.exit_code == 0
            assert "No MCP tools are currently enabled" in result_no_secops.stdout
            assert len(agent_mod.root_agent.tools) == 0

