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
            result = runner.invoke(app, ["chat", "--secops", "--no-scc", "test query"])
            assert result.exit_code == 0
            assert "Active MCP Toolsets:" in result.stdout
            assert "SecOps SIEM" in result.stdout
            assert len(agent_mod.root_agent.tools) == 1
            assert sys.modules["mcp_security_agent"].root_agent == agent_mod.root_agent

            result_no_secops = runner.invoke(app, ["chat", "--no-secops", "--no-scc", "test query"])
            assert result_no_secops.exit_code == 0
            assert "No MCP tools are currently enabled" in result_no_secops.stdout
            assert len(agent_mod.root_agent.tools) == 0


def test_cli_chat_config_flags():
    import os
    import mcp_security_agent.agent as agent_mod
    mock_adk_cli = MagicMock()
    async def fake_run_once(*args, **kwargs):
        return 0
    mock_adk_cli.run_once_cli = fake_run_once

    with patch.dict(os.environ, {}, clear=True):
        with patch.dict("sys.modules", {"google.adk.cli.cli": mock_adk_cli}):
            result = runner.invoke(app, [
                "chat",
                "--vertex",
                "--model", "gemini-2.5-pro",
                "--project", "test-project-123",
                "--customer-id", "cust-uuid-456",
                "test query"
            ])
            assert result.exit_code == 0
            assert os.environ["GOOGLE_GENAI_USE_VERTEXAI"] == "TRUE"
            assert os.environ["GOOGLE_MODEL"] == "gemini-2.5-pro"
            assert os.environ["GOOGLE_CLOUD_PROJECT"] == "test-project-123"
            assert os.environ["CHRONICLE_PROJECT_ID"] == "test-project-123"
            assert os.environ["CHRONICLE_CUSTOMER_ID"] == "cust-uuid-456"
            assert agent_mod.root_agent.model == "gemini-2.5-pro"


def test_cli_serve_command():
    import os
    mock_uvicorn = MagicMock()
    with patch.dict(os.environ, {"PORT": "9090"}, clear=True):
        with patch.dict("sys.modules", {"uvicorn": mock_uvicorn}):
            result = runner.invoke(app, ["serve"])
            assert result.exit_code == 0
            assert "Starting MCP Security Agent server on 0.0.0.0:9090" in result.stdout
            mock_uvicorn.run.assert_called_once()
            _, kwargs = mock_uvicorn.run.call_args
            assert kwargs["port"] == 9090

    mock_uvicorn.reset_mock()
    with patch.dict(os.environ, {}, clear=True):
        with patch.dict("sys.modules", {"uvicorn": mock_uvicorn}):
            result = runner.invoke(app, ["serve", "--port", "7070", "--reload"])
            assert result.exit_code == 0
            assert "Starting MCP Security Agent server on 0.0.0.0:7070" in result.stdout
            mock_uvicorn.run.assert_called_once()
            args, kwargs = mock_uvicorn.run.call_args
            assert args[0] == "mcp_security_agent.server.app:create_app"
            assert kwargs["factory"] is True
            assert kwargs["port"] == 7070
            assert kwargs["reload"] is True



