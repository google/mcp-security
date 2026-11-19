"""Hermetic unit and security tests for mcp_security_agent."""

import importlib
import os
from pathlib import Path
import shutil
import sys
import tomllib

from google.adk.agents import LlmAgent
from google.adk.cli.utils.agent_loader import AgentLoader, is_single_agent_directory
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams
import pytest

import mcp_security_agent
from mcp_security_agent.agent import build_agent, root_agent

ADK_DIR = Path(__file__).resolve().parents[1]
PKG_DIR = ADK_DIR / "mcp_security_agent"
SERVER_DIR = ADK_DIR.parent / "server"

_MCP_ENV_KEYS = (
    "GOOGLE_MODEL",
    "CHRONICLE_PROJECT_ID",
    "CHRONICLE_CUSTOMER_ID",
    "CHRONICLE_REGION",
    "SECOPS_SA_PATH",
    "SECOPS_IMPERSONATE_SERVICE_ACCOUNT",
    "VT_APIKEY",
    "SOAR_URL",
    "SOAR_APP_KEY",
    "SOAR_VERIFY_SSL",
    "LOAD_SCC_MCP",
    "LOAD_SECOPS_MCP",
    "LOAD_GTI_MCP",
    "LOAD_SECOPS_SOAR_MCP",
    "SECOPS_MCP_URL",
    "SCC_MCP_URL",
    "GTI_MCP_URL",
    "SECOPS_SOAR_MCP_URL",
    "STDIO_PARAM_TIMEOUT",
)


@pytest.fixture(autouse=True)
def _clean_mcp_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in _MCP_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)


def _stdio_scripts(agent: LlmAgent) -> list[str]:
    scripts: list[str] = []
    for toolset in agent.tools:
        assert isinstance(toolset, McpToolset)
        conn = toolset.connection_params
        assert isinstance(conn, StdioConnectionParams)
        scripts.append(conn.server_params.args[-1])
    return scripts


def test_root_agent_export_and_adk_loader_discovery(monkeypatch: pytest.MonkeyPatch) -> None:
    assert isinstance(root_agent, LlmAgent)
    assert mcp_security_agent.root_agent is mcp_security_agent.agent.root_agent
    assert root_agent.name == "mcp_security_agent"

    fresh = build_agent()
    assert fresh.name == "mcp_security_agent"
    assert fresh.model == "gemini-3.1-pro-preview"
    assert fresh.tools == []

    monkeypatch.setenv("GOOGLE_MODEL", "gemini-3-flash-preview")
    assert build_agent().model == "gemini-3-flash-preview"

    monkeypatch.setenv("GOOGLE_MODEL", "   ")
    assert build_agent().model == "gemini-3.1-pro-preview"

    assert is_single_agent_directory(PKG_DIR) is True
    assert is_single_agent_directory(ADK_DIR) is False

    monkeypatch.chdir(ADK_DIR)
    loader = AgentLoader(".")
    assert "mcp_security_agent" in loader.list_agents()
    loaded = loader.load_agent("mcp_security_agent")
    assert isinstance(loaded, LlmAgent)
    assert loaded.name == "mcp_security_agent"


def test_mtls_defaults_set_on_import(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "GOOGLE_API_USE_CLIENT_CERTIFICATE",
        "GOOGLE_API_USE_MTLS_ENDPOINT",
        "CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE",
    ):
        monkeypatch.delenv(key, raising=False)

    importlib.reload(mcp_security_agent.agent)
    assert os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE") == "false"
    assert os.environ.get("GOOGLE_API_USE_MTLS_ENDPOINT") == "never"
    assert os.environ.get("CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE") == "false"

    monkeypatch.setenv("GOOGLE_API_USE_MTLS_ENDPOINT", "always")
    importlib.reload(mcp_security_agent.agent)
    assert os.environ.get("GOOGLE_API_USE_MTLS_ENDPOINT") == "always"
    importlib.reload(mcp_security_agent)


def test_secops_auto_activation_and_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHRONICLE_PROJECT_ID", "secops-proj")
    assert build_agent().tools == []

    monkeypatch.setenv("CHRONICLE_CUSTOMER_ID", "a1b2c3d4-e5f6-4321-abcd-ef1234567890")
    assert _stdio_scripts(build_agent()) == ["secops_mcp/server.py"]

    monkeypatch.setenv("LOAD_SECOPS_MCP", "false")
    assert build_agent().tools == []

    monkeypatch.delenv("CHRONICLE_PROJECT_ID")
    monkeypatch.delenv("CHRONICLE_CUSTOMER_ID")
    monkeypatch.setenv("LOAD_SECOPS_MCP", "yes")
    assert _stdio_scripts(build_agent()) == ["secops_mcp/server.py"]


@pytest.mark.parametrize("truthy", ["Y", "YES", "TRUE", "1", "true", "y"])
def test_scc_enable_flags(monkeypatch: pytest.MonkeyPatch, truthy: str) -> None:
    monkeypatch.setenv("LOAD_SCC_MCP", truthy)
    assert _stdio_scripts(build_agent()) == ["scc_mcp.py"]


def test_scc_default_off_and_url_override_disable(monkeypatch: pytest.MonkeyPatch) -> None:
    assert build_agent().tools == []
    monkeypatch.setenv("LOAD_SCC_MCP", "False")
    assert build_agent().tools == []

    monkeypatch.delenv("LOAD_SCC_MCP")
    monkeypatch.setenv("SCC_MCP_URL", "https://scc.example.com/mcp")
    assert len(build_agent().tools) == 1

    monkeypatch.setenv("LOAD_SCC_MCP", "False")
    assert build_agent().tools == []


def test_gti_auto_activation_and_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VT_APIKEY", "vt-key")
    assert _stdio_scripts(build_agent()) == ["gti_mcp/server.py"]

    monkeypatch.setenv("LOAD_GTI_MCP", "N")
    assert build_agent().tools == []

    monkeypatch.delenv("VT_APIKEY")
    monkeypatch.setenv("LOAD_GTI_MCP", "1")
    assert _stdio_scripts(build_agent()) == ["gti_mcp/server.py"]


def test_soar_auto_activation_and_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SOAR_URL", "https://soar.example.com")
    assert build_agent().tools == []

    monkeypatch.setenv("SOAR_APP_KEY", "soar-key")
    assert _stdio_scripts(build_agent()) == ["secops_soar_mcp/server.py"]

    monkeypatch.setenv("LOAD_SECOPS_SOAR_MCP", "0")
    assert build_agent().tools == []

    monkeypatch.delenv("SOAR_URL")
    monkeypatch.delenv("SOAR_APP_KEY")
    monkeypatch.setenv("LOAD_SECOPS_SOAR_MCP", "TRUE")
    assert _stdio_scripts(build_agent()) == ["secops_soar_mcp/server.py"]


def test_stdio_uv_and_python_fallback_and_entrypoints_exist(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = {
        "secops": "secops_mcp/server.py",
        "scc": "scc_mcp.py",
        "gti": "gti_mcp/server.py",
        "secops-soar": "secops_soar_mcp/server.py",
    }
    for subdir, script in expected.items():
        assert (SERVER_DIR / subdir / script).is_file()

    monkeypatch.setenv("VT_APIKEY", "vt-key")
    monkeypatch.setenv("STDIO_PARAM_TIMEOUT", "42.5")

    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/uv" if name == "uv" else None)
    conn_uv = build_agent().tools[0].connection_params
    assert isinstance(conn_uv, StdioConnectionParams)
    assert conn_uv.timeout == 42.5
    assert conn_uv.server_params.command == "uv"
    assert conn_uv.server_params.args == ["--directory", str(SERVER_DIR / "gti"), "run", "gti_mcp/server.py"]
    assert "PYTHONPATH" not in conn_uv.server_params.env

    monkeypatch.setattr(shutil, "which", lambda _name: None)
    conn_py = build_agent().tools[0].connection_params
    assert isinstance(conn_py, StdioConnectionParams)
    assert conn_py.server_params.command == sys.executable
    assert conn_py.server_params.args == [str(SERVER_DIR / "gti" / "gti_mcp/server.py")]
    assert conn_py.server_params.env["PYTHONPATH"] == str(SERVER_DIR / "gti")


@pytest.mark.parametrize(
    "url_var",
    ["SECOPS_MCP_URL", "SCC_MCP_URL", "GTI_MCP_URL", "SECOPS_SOAR_MCP_URL"],
)
@pytest.mark.parametrize(
    "valid_url",
    [
        "https://mcp.secops.example.com/mcp",
        "http://localhost:8080/mcp",
        "http://127.0.0.1:8080/mcp",
        "http://[::1]:8080/mcp",
    ],
)
def test_streamable_http_url_selection(
    monkeypatch: pytest.MonkeyPatch, url_var: str, valid_url: str
) -> None:
    monkeypatch.setenv(url_var, valid_url)
    agent = build_agent()
    assert len(agent.tools) == 1
    conn = agent.tools[0].connection_params
    assert isinstance(conn, StreamableHTTPConnectionParams)
    assert conn.url == valid_url


@pytest.mark.parametrize(
    "unsafe_url",
    [
        "file:///etc/passwd",
        "file://localhost/etc/passwd",
        "http://evil.example.com/mcp",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.5:8080/mcp",
        "http://0.0.0.0:8080/mcp",
        "http://localhost.evil.com/mcp",
        "http://localhost@evil.com/mcp",
        "ftp://localhost/mcp",
        "javascript:alert(1)",
        "https://",
        "https://user:secret@example.com/mcp",
        "https://example.com/mcp with-space",
    ],
)
def test_unsafe_mcp_urls_rejected(monkeypatch: pytest.MonkeyPatch, unsafe_url: str) -> None:
    monkeypatch.setenv("SECOPS_MCP_URL", unsafe_url)
    with pytest.raises(ValueError, match="Unsafe MCP URL"):
        build_agent()


def test_strict_subprocess_env_isolation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VT_APIKEY", "vt-secret-token")
    monkeypatch.setenv("SOAR_URL", "https://soar.example.com")
    monkeypatch.setenv("SOAR_APP_KEY", "soar-secret-key")
    monkeypatch.setenv("SOAR_VERIFY_SSL", "true")
    monkeypatch.setenv("CHRONICLE_PROJECT_ID", "secops-project")
    monkeypatch.setenv("CHRONICLE_CUSTOMER_ID", "a1b2c3d4-e5f6-4321-abcd-ef1234567890")
    monkeypatch.setenv("CHRONICLE_REGION", "us")
    monkeypatch.setenv("SECOPS_SA_PATH", "/path/to/sa.json")
    monkeypatch.setenv("SECOPS_IMPERSONATE_SERVICE_ACCOUNT", "svc@secops-project.iam.gserviceaccount.com")
    monkeypatch.setenv("LOAD_SCC_MCP", "True")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "shared-vertex-project")
    monkeypatch.setenv("UNRELATED_HOST_SECRET", "leak")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-leak")

    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/uv" if name == "uv" else None)
    agent = build_agent()
    assert len(agent.tools) == 4

    envs_by_server: dict[str, dict[str, str]] = {}
    for toolset in agent.tools:
        conn = toolset.connection_params
        assert isinstance(conn, StdioConnectionParams)
        assert conn.server_params.env is not None
        server_name = Path(conn.server_params.args[1]).name
        envs_by_server[server_name] = conn.server_params.env

    assert set(envs_by_server) == {"secops", "scc", "gti", "secops-soar"}

    for name, env in envs_by_server.items():
        assert "UNRELATED_HOST_SECRET" not in env, f"Host secret leaked into {name}"
        assert "AWS_SECRET_ACCESS_KEY" not in env, f"AWS secret leaked into {name}"
        assert env["GOOGLE_CLOUD_PROJECT"] == "shared-vertex-project"
        assert env["GOOGLE_API_USE_CLIENT_CERTIFICATE"] == "false"
        assert env["GOOGLE_API_USE_MTLS_ENDPOINT"] == "never"
        assert env["CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE"] == "false"

        if name == "gti":
            assert env["VT_APIKEY"] == "vt-secret-token"
        else:
            assert "VT_APIKEY" not in env

        if name == "secops-soar":
            assert env["SOAR_APP_KEY"] == "soar-secret-key"
            assert env["SOAR_URL"] == "https://soar.example.com"
            assert env["SOAR_VERIFY_SSL"] == "true"
        else:
            assert "SOAR_APP_KEY" not in env
            assert "SOAR_URL" not in env
            assert "SOAR_VERIFY_SSL" not in env

        if name == "secops":
            assert env["CHRONICLE_PROJECT_ID"] == "secops-project"
            assert env["CHRONICLE_CUSTOMER_ID"] == "a1b2c3d4-e5f6-4321-abcd-ef1234567890"
            assert env["CHRONICLE_REGION"] == "us"
            assert env["SECOPS_SA_PATH"] == "/path/to/sa.json"
            assert env["SECOPS_IMPERSONATE_SERVICE_ACCOUNT"] == "svc@secops-project.iam.gserviceaccount.com"
        else:
            assert "CHRONICLE_PROJECT_ID" not in env
            assert "CHRONICLE_CUSTOMER_ID" not in env
            assert "CHRONICLE_REGION" not in env
            assert "SECOPS_SA_PATH" not in env
            assert "SECOPS_IMPERSONATE_SERVICE_ACCOUNT" not in env


def test_minimal_package_footprint() -> None:
    pyproject = tomllib.loads((ADK_DIR / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    assert "scripts" not in project
    assert len(project.get("dependencies", [])) == 4

    py_files = sorted(PKG_DIR.glob("*.py"))
    assert [p.name for p in py_files] == ["__init__.py", "agent.py"]
    total_lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in py_files)
    assert total_lines <= 80

    agent_source = (PKG_DIR / "agent.py").read_text(encoding="utf-8")
    assert "dict(os.environ)" not in agent_source
    assert "os.environ.copy()" not in agent_source

    assert Path(__file__).resolve().read_text(encoding="utf-8").isascii()
    banned_terms = ("Argo" + "lis", "gemini-2.5-" + "pro")
    for owned in [
        ADK_DIR / "pyproject.toml",
        ADK_DIR / ".env.example",
        PKG_DIR / "__init__.py",
        PKG_DIR / "agent.py",
    ]:
        text = owned.read_text(encoding="utf-8")
        assert text.isascii(), f"Non-ASCII character in {owned.name}"
        for term in banned_terms:
            assert term not in text
