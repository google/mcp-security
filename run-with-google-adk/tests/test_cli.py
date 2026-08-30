"""Unit tests for mcp_security_agent.cli."""

import sys
from pathlib import Path
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
