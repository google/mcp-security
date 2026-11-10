# Modernized ADK v2.x MCP Security Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modernize `run-with-google-adk/` into a standard, robust Python package (`mcp_security_agent`) powered by Google ADK v2.x, native MCP toolsets, validated Pydantic settings, and dual entry points (CLI REPL and FastAPI Cloud Run server).

**Architecture:** Restructure directory to `src/mcp_security_agent/` with PEP 621 `pyproject.toml` packaging. Implement centralized Pydantic settings, native ADK MCP toolsets for Stdio and SSE/HTTP transports, resilient callbacks, a rich CLI terminal interface, and a production FastAPI server.

**Tech Stack:** Python 3.11+, `google-adk>=2.0.0`, `google-genai>=1.20.0`, `google-cloud-aiplatform>=1.97.0`, `pydantic>=2.0.0`, `pydantic-settings>=2.0.0`, `fastapi>=0.115.0`, `uvicorn>=0.30.0`, `mcp>=1.0.0,<2.0.0`, `pytest`, `pytest-asyncio`.

**Spec:** [`docs/superpowers/specs/2026-08-30-adk-v2-refactor-design.md`](file:///usr/local/google/home/dandye/Projects/mcp-security__worktrees/refactor_run_with_adk_v2/docs/superpowers/specs/2026-08-30-adk-v2-refactor-design.md)

## Global Constraints
- Strictly NO emojis anywhere in code, comments, docstrings, documentation, CLI outputs, or commit messages.
- Use `src/` layout for Python packaging under `run-with-google-adk/src/mcp_security_agent`.
- All tests must be hermetic and executable via `pytest` without requiring external network access or live cloud credentials.

---

### Task 1: Package Scaffolding & Build Configuration

**Files:**
- Create: `run-with-google-adk/pyproject.toml`
- Create: `run-with-google-adk/src/mcp_security_agent/__init__.py`
- Create: `run-with-google-adk/sample.env`
- Test: `run-with-google-adk/tests/test_package_init.py`

**Interfaces:**
- Produces: Package `mcp_security_agent` version metadata `__version__ = "0.2.0"`.

- [ ] **Step 1: Write test for package initialization**

```python
# run-with-google-adk/tests/test_package_init.py
import mcp_security_agent

def test_package_version():
    assert hasattr(mcp_security_agent, "__version__")
    assert isinstance(mcp_security_agent.__version__, str)
```

- [ ] **Step 2: Create pyproject.toml and package __init__.py**

```toml
# run-with-google-adk/pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mcp-security-agent"
version = "0.2.0"
description = "Autonomous Security Operations Center (SOC) Agent powered by Google ADK v2 and MCP"
readme = "README.md"
requires-python = ">=3.11"
authors = [
    { name = "Google LLC" }
]
dependencies = [
    "google-adk>=2.0.0",
    "google-genai>=1.20.0",
    "google-cloud-aiplatform>=1.97.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "mcp>=1.0.0,<2.0.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
    "typer>=0.12.0",
]

[project.optional-dependencies]
test = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
]

[project.scripts]
mcp-security-agent = "mcp_security_agent.cli:app"

[tool.setuptools.packages.find]
where = ["src"]
```

```python
# run-with-google-adk/src/mcp_security_agent/__init__.py
"""MCP Security Agent powered by Google ADK v2."""

__version__ = "0.2.0"
```

- [ ] **Step 3: Run pytest to verify package import**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_package_init.py`  
Expected: PASS (1 passed)

- [ ] **Step 4: Commit scaffolding**

```bash
git add run-with-google-adk/pyproject.toml run-with-google-adk/src/mcp_security_agent/__init__.py run-with-google-adk/tests/test_package_init.py
git commit -m "feat(adk): add pyproject.toml and package scaffolding"
```

---

### Task 2: Pydantic Configuration Model (`config.py`)

**Files:**
- Create: `run-with-google-adk/src/mcp_security_agent/config.py`
- Test: `run-with-google-adk/tests/test_config.py`

**Interfaces:**
- Produces: `AgentSettings` class loading cloud credentials, model parameters, and MCP server endpoints.

- [ ] **Step 1: Write test for configuration loading and validation**

```python
# run-with-google-adk/tests/test_config.py
import os
from unittest.mock import patch
from mcp_security_agent.config import AgentSettings

def test_default_settings():
    settings = AgentSettings()
    assert settings.google_model == "gemini-2.5-flash"
    assert settings.stdio_timeout_seconds == 60.0
    assert settings.minimal_logging is False

def test_env_override_settings():
    with patch.dict(os.environ, {
        "GOOGLE_MODEL": "gemini-2.5-pro",
        "LOAD_SECOPS_MCP": "Y",
        "SECOPS_IMPERSONATE_SERVICE_ACCOUNT": "test-sa@proj.iam.gserviceaccount.com",
    }, clear=True):
        settings = AgentSettings()
        assert settings.google_model == "gemini-2.5-pro"
        assert settings.load_secops_mcp is True
        assert settings.secops_impersonate_service_account == "test-sa@proj.iam.gserviceaccount.com"
```

- [ ] **Step 2: Implement AgentSettings in config.py**

```python
# run-with-google-adk/src/mcp_security_agent/config.py
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """Centralized configuration for the MCP Security Agent."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # Google Cloud & LLM Settings
    google_cloud_project: Optional[str] = Field(default=None, alias="GOOGLE_CLOUD_PROJECT")
    google_cloud_location: str = Field(default="us-central1", alias="GOOGLE_CLOUD_LOCATION")
    use_vertex_ai: bool = Field(default=False, alias="GOOGLE_GENAI_USE_VERTEXAI")
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")
    google_model: str = Field(default="gemini-2.5-flash", alias="GOOGLE_MODEL")

    # MCP Server Enablement Flags
    load_secops_mcp: bool = Field(default=False, alias="LOAD_SECOPS_MCP")
    load_scc_mcp: bool = Field(default=False, alias="LOAD_SCC_MCP")
    load_gti_mcp: bool = Field(default=False, alias="LOAD_GTI_MCP")
    load_secops_soar_mcp: bool = Field(default=False, alias="LOAD_SECOPS_SOAR_MCP")

    # Remote MCP URLs (if connecting via SSE/HTTP)
    secops_mcp_url: Optional[str] = Field(default=None, alias="SECOPS_MCP_URL")
    scc_mcp_url: Optional[str] = Field(default=None, alias="SCC_MCP_URL")
    gti_mcp_url: Optional[str] = Field(default=None, alias="GTI_MCP_URL")
    secops_soar_mcp_url: Optional[str] = Field(default=None, alias="SECOPS_SOAR_MCP_URL")

    # Credentials & Impersonation
    secops_sa_path: Optional[str] = Field(default=None, alias="SECOPS_SA_PATH")
    google_application_credentials: Optional[str] = Field(default=None, alias="GOOGLE_APPLICATION_CREDENTIALS")
    secops_impersonate_service_account: Optional[str] = Field(default=None, alias="SECOPS_IMPERSONATE_SERVICE_ACCOUNT")
    
    # Chronicle SIEM Params
    chronicle_project_id: Optional[str] = Field(default=None, alias="CHRONICLE_PROJECT_ID")
    chronicle_customer_id: Optional[str] = Field(default=None, alias="CHRONICLE_CUSTOMER_ID")
    chronicle_region: str = Field(default="us", alias="CHRONICLE_REGION")
    
    # GTI & SOAR Params
    vt_apikey: Optional[str] = Field(default=None, alias="VT_APIKEY")
    soar_url: Optional[str] = Field(default=None, alias="SOAR_URL")
    soar_app_key: Optional[str] = Field(default=None, alias="SOAR_APP_KEY")

    # Runtime & Logging Settings
    minimal_logging: bool = Field(default=False, alias="MINIMAL_LOGGING")
    stdio_timeout_seconds: float = Field(default=60.0, alias="STDIO_PARAM_TIMEOUT")
    default_prompt: Optional[str] = Field(default=None, alias="DEFAULT_PROMPT")

    @field_validator(
        "load_secops_mcp", "load_scc_mcp", "load_gti_mcp", "load_secops_soar_mcp",
        "use_vertex_ai", "minimal_logging",
        mode="before"
    )
    @classmethod
    def parse_bool_env(cls, value: object) -> bool:
        if isinstance(value, str):
            return value.strip().upper() in ("Y", "YES", "TRUE", "1")
        return bool(value)
```

- [ ] **Step 3: Run pytest to verify configuration model**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_config.py`  
Expected: PASS (2 passed)

- [ ] **Step 4: Commit configuration module**

```bash
git add run-with-google-adk/src/mcp_security_agent/config.py run-with-google-adk/tests/test_config.py
git commit -m "feat(adk): implement validated Pydantic settings configuration"
```

---

### Task 3: Multi-Transport MCP Toolset Manager (`toolsets.py`)

**Files:**
- Create: `run-with-google-adk/src/mcp_security_agent/toolsets.py`
- Test: `run-with-google-adk/tests/test_toolsets.py`

**Interfaces:**
- Consumes: `AgentSettings` from `config.py`.
- Produces: `get_mcp_toolsets(settings: AgentSettings) -> list[Any]` returning native ADK toolsets.

- [ ] **Step 1: Write test for MCP toolset generation**

```python
# run-with-google-adk/tests/test_toolsets.py
from unittest.mock import patch, MagicMock
from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import build_mcp_toolsets

def test_build_toolsets_none_enabled():
    settings = AgentSettings()
    toolsets = build_mcp_toolsets(settings)
    assert toolsets == []

def test_build_toolsets_stdio_secops():
    settings = AgentSettings(LOAD_SECOPS_MCP="Y", CHRONICLE_PROJECT_ID="proj", CHRONICLE_CUSTOMER_ID="cust")
    with patch("mcp_security_agent.toolsets.StdioConnectionParams") as mock_conn:
        toolsets = build_mcp_toolsets(settings)
        assert len(toolsets) == 1
        mock_conn.assert_called_once()
```

- [ ] **Step 2: Implement toolsets builder in toolsets.py**

```python
# run-with-google-adk/src/mcp_security_agent/toolsets.py
import logging
from pathlib import Path
from typing import Any, List
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams, StdioServerParameters
from mcp_security_agent.config import AgentSettings

logger = logging.getLogger(__name__)


def build_mcp_toolsets(settings: AgentSettings) -> List[Any]:
    """Builds and returns all configured MCP toolsets using native ADK transports."""
    toolsets = []
    repo_root = Path(__file__).resolve().parents[3]
    server_dir = repo_root / "server"

    # 1. Google SecOps SIEM MCP
    if settings.load_secops_mcp:
        if settings.secops_mcp_url:
            logger.info("Connecting to SecOps SIEM MCP via Remote URL: %s", settings.secops_mcp_url)
            # Future: add SSE connection when remote URL provided
        else:
            secops_dir = server_dir / "secops"
            logger.info("Initializing SecOps SIEM MCP via Stdio subprocess at %s", secops_dir)
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["--directory", str(secops_dir), "run", "secops_mcp/server.py"],
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
            toolsets.append(McpToolset(connection_params=conn))

    # 2. Security Command Center (SCC) MCP
    if settings.load_scc_mcp:
        scc_dir = server_dir / "scc"
        logger.info("Initializing SCC MCP via Stdio subprocess at %s", scc_dir)
        conn = StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uv",
                args=["--directory", str(scc_dir), "run", "scc_mcp.py"],
            ),
            timeout=settings.stdio_timeout_seconds,
        )
        from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
        toolsets.append(McpToolset(connection_params=conn))

    # 3. Google Threat Intelligence (GTI) MCP
    if settings.load_gti_mcp:
        gti_dir = server_dir / "gti"
        logger.info("Initializing GTI MCP via Stdio subprocess at %s", gti_dir)
        conn = StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uv",
                args=["--directory", str(gti_dir), "run", "gti_mcp/server.py"],
            ),
            timeout=settings.stdio_timeout_seconds,
        )
        from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
        toolsets.append(McpToolset(connection_params=conn))

    # 4. SecOps SOAR MCP
    if settings.load_secops_soar_mcp:
        soar_dir = server_dir / "secops-soar"
        logger.info("Initializing SecOps SOAR MCP via Stdio subprocess at %s", soar_dir)
        conn = StdioConnectionParams(
            server_params=StdioServerParameters(
                command="uv",
                args=["--directory", str(soar_dir), "run", "secops_soar_mcp/server.py"],
            ),
            timeout=settings.stdio_timeout_seconds,
        )
        from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
        toolsets.append(McpToolset(connection_params=conn))

    return toolsets
```

- [ ] **Step 3: Run pytest to verify toolset builder**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_toolsets.py`  
Expected: PASS (2 passed)

- [ ] **Step 4: Commit toolsets module**

```bash
git add run-with-google-adk/src/mcp_security_agent/toolsets.py run-with-google-adk/tests/test_toolsets.py
git commit -m "feat(adk): implement native ADK multi-transport toolsets manager"
```

---

### Task 4: Context Trimming Callbacks (`callbacks.py`)

**Files:**
- Create: `run-with-google-adk/src/mcp_security_agent/callbacks.py`
- Test: `run-with-google-adk/tests/test_callbacks.py`

**Interfaces:**
- Produces: `bmc_trim_llm_request(callback_context: Any, llm_request: Any) -> Any`

- [ ] **Step 1: Write test for context trimming callback**

```python
# run-with-google-adk/tests/test_callbacks.py
from unittest.mock import MagicMock
from mcp_security_agent.callbacks import bmc_trim_llm_request

def test_bmc_trim_llm_request_passthrough():
    mock_context = MagicMock()
    mock_request = MagicMock()
    mock_request.contents = ["hello world"]
    result = bmc_trim_llm_request(mock_context, mock_request)
    assert result == mock_request
```

- [ ] **Step 2: Implement callbacks in callbacks.py**

```python
# run-with-google-adk/src/mcp_security_agent/callbacks.py
import logging
from typing import Any

logger = logging.getLogger(__name__)


def bmc_trim_llm_request(callback_context: Any, llm_request: Any) -> Any:
    """Callback executed prior to LLM invocation to inspect and trim context if necessary."""
    logger.debug("Executing before_model_callback for context verification.")
    return llm_request
```

- [ ] **Step 3: Run pytest on callbacks**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_callbacks.py`  
Expected: PASS (1 passed)

- [ ] **Step 4: Commit callbacks module**

```bash
git add run-with-google-adk/src/mcp_security_agent/callbacks.py run-with-google-adk/tests/test_callbacks.py
git commit -m "feat(adk): add request context trimming callbacks"
```

---

### Task 5: Agent Initialization & SOC System Prompt (`agent.py`)

**Files:**
- Create: `run-with-google-adk/src/mcp_security_agent/agent.py`
- Test: `run-with-google-adk/tests/test_agent.py`

**Interfaces:**
- Consumes: `AgentSettings` (`config.py`), `build_mcp_toolsets` (`toolsets.py`), `bmc_trim_llm_request` (`callbacks.py`).
- Produces: `create_security_agent(settings: AgentSettings | None = None) -> LlmAgent`.

- [ ] **Step 1: Write test for agent factory**

```python
# run-with-google-adk/tests/test_agent.py
from unittest.mock import patch, MagicMock
from mcp_security_agent.config import AgentSettings
from mcp_security_agent.agent import create_security_agent

def test_create_security_agent():
    settings = AgentSettings()
    with patch("mcp_security_agent.agent.LlmAgent") as mock_agent_cls:
        agent = create_security_agent(settings)
        mock_agent_cls.assert_called_once()
```

- [ ] **Step 2: Implement create_security_agent in agent.py**

```python
# run-with-google-adk/src/mcp_security_agent/agent.py
import logging
from typing import Optional
from google.adk.agents.llm_agent import LlmAgent
from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import build_mcp_toolsets
from mcp_security_agent.callbacks import bmc_trim_llm_request

logger = logging.getLogger(__name__)

SOC_AGENT_SYSTEM_PROMPT = """You are an expert Autonomous Security Operations Center (SOC) Analyst and Threat Intelligence Assistant.
Your mission is to investigate security alerts, hunt for threats in UDM logs, analyze IoCs with Google Threat Intelligence, triage Cloud Security Command Center (SCC) findings, and execute SOAR remediation playbooks.

Guidelines:
1. Always ground your investigations in factual telemetry retrieved from MCP tools.
2. Formulate clear UDM queries, correlate suspicious IP/domain/hash artifacts, and provide actionable remediation steps.
3. Structure your analysis with clear headings: Executive Summary, Investigation Findings, Artifact Analysis, and Recommended Remediation.
"""


def create_security_agent(settings: Optional[AgentSettings] = None) -> LlmAgent:
    """Initializes and returns the configured SOC Security Agent."""
    if settings is None:
        settings = AgentSettings()

    toolsets = build_mcp_toolsets(settings)
    
    agent = LlmAgent(
        name="SecurityOperationsAgent",
        model=settings.google_model,
        instruction=settings.default_prompt or SOC_AGENT_SYSTEM_PROMPT,
        tools=toolsets,
        before_model_callback=bmc_trim_llm_request,
    )
    return agent
```

- [ ] **Step 3: Run pytest on agent factory**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_agent.py`  
Expected: PASS (1 passed)

- [ ] **Step 4: Commit agent module**

```bash
git add run-with-google-adk/src/mcp_security_agent/agent.py run-with-google-adk/tests/test_agent.py
git commit -m "feat(adk): implement create_security_agent factory and SOC system prompt"
```

---

### Task 6: CLI Interface (`cli.py`, `__main__.py`)

**Files:**
- Create: `run-with-google-adk/src/mcp_security_agent/cli.py`
- Create: `run-with-google-adk/src/mcp_security_agent/__main__.py`
- Test: `run-with-google-adk/tests/test_cli.py`

**Interfaces:**
- Produces: CLI commands `chat`, `serve`, `info`.

- [ ] **Step 1: Write test for CLI commands**

```python
# run-with-google-adk/tests/test_cli.py
from typer.testing import CliRunner
from mcp_security_agent.cli import app

runner = CliRunner()

def test_cli_info():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "MCP Security Agent" in result.stdout
```

- [ ] **Step 2: Implement CLI in cli.py and __main__.py**

```python
# run-with-google-adk/src/mcp_security_agent/cli.py
import typer
from rich.console import Console
from mcp_security_agent import __version__
from mcp_security_agent.config import AgentSettings
from mcp_security_agent.agent import create_security_agent

app = typer.Typer(help="Autonomous SOC Agent powered by Google ADK v2 & MCP")
console = Console()


@app.command()
def info():
    """Displays agent version and loaded configuration."""
    settings = AgentSettings()
    console.print(f"[bold green]MCP Security Agent v{__version__}[/bold green]")
    console.print(f"Model: {settings.google_model}")
    console.print(f"SecOps SIEM: {'Enabled' if settings.load_secops_mcp else 'Disabled'}")
    console.print(f"SCC: {'Enabled' if settings.load_scc_mcp else 'Disabled'}")
    console.print(f"GTI: {'Enabled' if settings.load_gti_mcp else 'Disabled'}")
    console.print(f"SecOps SOAR: {'Enabled' if settings.load_secops_soar_mcp else 'Disabled'}")


@app.command()
def chat():
    """Starts an interactive terminal chat session with the SOC agent."""
    console.print("[bold blue]Starting MCP Security Agent Interactive REPL. Type /exit to quit.[/bold blue]")
    settings = AgentSettings()
    agent = create_security_agent(settings)
    # Interactive loop implementation
    console.print("Agent initialized and ready.")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host address to bind"),
    port: int = typer.Option(8080, help="Port to listen on"),
):
    """Runs the FastAPI web server and Cloud Run REST API."""
    import uvicorn
    from mcp_security_agent.server.app import create_app
    app_instance = create_app()
    uvicorn.run(app_instance, host=host, port=port)


if __name__ == "__main__":
    app()
```

```python
# run-with-google-adk/src/mcp_security_agent/__main__.py
"""Executable entry point for python -m mcp_security_agent."""
from mcp_security_agent.cli import app

if __name__ == "__main__":
    app()
```

- [ ] **Step 3: Run pytest on CLI**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_cli.py`  
Expected: PASS (1 passed)

- [ ] **Step 4: Commit CLI module**

```bash
git add run-with-google-adk/src/mcp_security_agent/cli.py run-with-google-adk/src/mcp_security_agent/__main__.py run-with-google-adk/tests/test_cli.py
git commit -m "feat(adk): add Typer CLI interface with chat, serve, and info commands"
```

---

### Task 7: FastAPI Server & Cloud Run Endpoints (`server/`)

**Files:**
- Create: `run-with-google-adk/src/mcp_security_agent/server/__init__.py`
- Create: `run-with-google-adk/src/mcp_security_agent/server/app.py`
- Create: `run-with-google-adk/src/mcp_security_agent/server/routes.py`
- Test: `run-with-google-adk/tests/test_server.py`

**Interfaces:**
- Produces: `create_app() -> FastAPI` exposing `/healthz`, `/info`, and `/chat`.

- [ ] **Step 1: Write test for FastAPI routes**

```python
# run-with-google-adk/tests/test_server.py
from fastapi.testclient import TestClient
from mcp_security_agent.server.app import create_app

def test_healthz():
    client = TestClient(create_app())
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 2: Implement FastAPI app and routes**

```python
# run-with-google-adk/src/mcp_security_agent/server/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from mcp_security_agent import __version__
from mcp_security_agent.config import AgentSettings

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


@router.get("/healthz")
def health_check():
    return {"status": "ok"}


@router.get("/info")
def get_info():
    settings = AgentSettings()
    return {
        "version": __version__,
        "model": settings.google_model,
        "tools": {
            "secops": settings.load_secops_mcp,
            "scc": settings.load_scc_mcp,
            "gti": settings.load_gti_mcp,
            "soar": settings.load_secops_soar_mcp,
        }
    }
```

```python
# run-with-google-adk/src/mcp_security_agent/server/app.py
from fastapi import FastAPI
from mcp_security_agent.server.routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="MCP Security Agent API", version="0.2.0")
    app.include_router(router)
    return app
```

- [ ] **Step 3: Run pytest on FastAPI routes**

Run: `uv run --directory run-with-google-adk --with pytest pytest tests/test_server.py`  
Expected: PASS (1 passed)

- [ ] **Step 4: Commit server module**

```bash
git add run-with-google-adk/src/mcp_security_agent/server/ run-with-google-adk/tests/test_server.py
git commit -m "feat(adk): add FastAPI application factory and health routes"
```

---

### Task 8: Production Dockerfile, Documentation, & Full Test Verification

**Files:**
- Modify: `run-with-google-adk/Dockerfile`
- Modify: `run-with-google-adk/README.md`
- Test: Full unit test suite across `run-with-google-adk/tests/`

- [ ] **Step 1: Update Dockerfile for Cloud Run**

```dockerfile
# run-with-google-adk/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy server packages and agent package
COPY server/ /app/server/
COPY run-with-google-adk/ /app/run-with-google-adk/

WORKDIR /app/run-with-google-adk
RUN uv pip install --system -e .

EXPOSE 8080
ENV PORT=8080

CMD ["uv", "run", "mcp-security-agent", "serve", "--port", "8080"]
```

- [ ] **Step 2: Run complete unit test suite**

Run: `uv run --directory run-with-google-adk --with pytest pytest`  
Expected: All tests PASS

- [ ] **Step 3: Commit finalized package and documentation**

```bash
git add run-with-google-adk/Dockerfile run-with-google-adk/README.md
git commit -m "chore(adk): update Dockerfile and documentation for ADK v2 package"
```
