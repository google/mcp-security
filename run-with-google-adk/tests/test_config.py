"""Unit tests for mcp_security_agent.config."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.config import AgentSettings


def test_default_settings():
    settings = AgentSettings()
    assert settings.google_model == "gemini-2.5-flash"
    assert settings.stdio_timeout_seconds == 60.0
    assert settings.minimal_logging is False
    assert settings.load_secops_mcp is False


def test_env_override_settings():
    with patch.dict(
        os.environ,
        {
            "GOOGLE_MODEL": "gemini-2.5-pro",
            "LOAD_SECOPS_MCP": "Y",
            "LOAD_SCC_MCP": "True",
            "SECOPS_IMPERSONATE_SERVICE_ACCOUNT": "test-sa@proj.iam.gserviceaccount.com",
            "STDIO_PARAM_TIMEOUT": "120.5",
        },
        clear=True,
    ):
        settings = AgentSettings()
        assert settings.google_model == "gemini-2.5-pro"
        assert settings.load_secops_mcp is True
        assert settings.load_scc_mcp is True
        assert settings.secops_impersonate_service_account == "test-sa@proj.iam.gserviceaccount.com"
        assert settings.stdio_timeout_seconds == 120.5
