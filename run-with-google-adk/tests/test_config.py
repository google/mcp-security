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
    with patch.dict(os.environ, {}, clear=True):
        settings = AgentSettings(_env_file=None)
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
        settings = AgentSettings(_env_file=None)
        assert settings.google_model == "gemini-2.5-pro"
        assert settings.load_secops_mcp is True
        assert settings.load_scc_mcp is True
        assert settings.secops_impersonate_service_account == "test-sa@proj.iam.gserviceaccount.com"
        assert settings.stdio_timeout_seconds == 120.5


def test_tool_auto_detection_from_credentials():
    with patch.dict(
        os.environ,
        {
            "VT_APIKEY": "valid_virustotal_api_key_12345",
            "SOAR_URL": "https://tenant.siemplify-soar.com",
            "SOAR_APP_KEY": "valid_soar_key_67890",
            "CHRONICLE_PROJECT_ID": "my-chronicle-project",
            "CHRONICLE_CUSTOMER_ID": "my-chronicle-customer-uuid",
        },
        clear=True,
    ):
        settings = AgentSettings(_env_file=None)
        assert settings.load_gti_mcp is True
        assert settings.load_secops_soar_mcp is True
        assert settings.load_secops_mcp is True
        assert settings.load_scc_mcp is False


def test_tool_auto_detection_empty_or_whitespace_values():
    with patch.dict(
        os.environ,
        {
            "VT_APIKEY": "   ",
            "SOAR_URL": "",
            "SOAR_APP_KEY": "  ",
            "CHRONICLE_PROJECT_ID": "",
            "CHRONICLE_CUSTOMER_ID": "",
        },
        clear=True,
    ):
        settings = AgentSettings(_env_file=None)
        assert settings.load_gti_mcp is False
        assert settings.load_secops_soar_mcp is False
        assert settings.load_secops_mcp is False


def test_tool_explicit_override_overrules_credentials():
    with patch.dict(
        os.environ,
        {
            "VT_APIKEY": "valid_virustotal_api_key_12345",
            "LOAD_GTI_MCP": "N",
            "SOAR_URL": "https://tenant.siemplify-soar.com",
            "SOAR_APP_KEY": "valid_soar_key_67890",
            "LOAD_SECOPS_SOAR_MCP": "False",
            "CHRONICLE_PROJECT_ID": "my-chronicle-project",
            "CHRONICLE_CUSTOMER_ID": "my-chronicle-customer-uuid",
            "LOAD_SECOPS_MCP": "0",
        },
        clear=True,
    ):
        settings = AgentSettings(_env_file=None)
        assert settings.load_gti_mcp is False
        assert settings.load_secops_soar_mcp is False
        assert settings.load_secops_mcp is False


def test_bootstrap_environment_with_api_key_preserves_gemini_api():
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "AIzaSyTestKey123", "GOOGLE_CLOUD_PROJECT": "my-gcp-proj"}, clear=True):
        settings = AgentSettings(_env_file=None)
        assert settings.google_api_key == "AIzaSyTestKey123"
        assert os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") is None
        assert os.environ.get("GOOGLE_API_KEY") == "AIzaSyTestKey123"


def test_bootstrap_environment_vertex_ai_default():
    with patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "my-gcp-proj"}, clear=True):
        settings = AgentSettings(_env_file=None)
        assert os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE"
        assert os.environ.get("GOOGLE_CLOUD_PROJECT") == "my-gcp-proj"


def test_env_files_precedence_order():
    from mcp_security_agent.config import _env_files
    # Local .env must come after parent .env so pydantic-settings gives it higher precedence
    assert _env_files[-1] == ".env"

