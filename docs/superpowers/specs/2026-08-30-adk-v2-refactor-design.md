# Modernized ADK v2.x MCP Security Agent Architecture Design

**Status:** Approved  
**Author:** Dan Dye (`@dandye`) & Jetski  
**Target Worktree:** `/usr/local/google/home/dandye/Projects/mcp-security__worktrees/refactor_run_with_adk_v2`  
**Branch:** `refactor/run-with-adk-v2`  
**Date:** 2026-08-30  

---

## 1. Overview & Objectives

The existing `run-with-google-adk/` implementation suffers from architectural fragmentation, legacy relative path resolution (`../../../...`), custom schema workarounds (`MCPToolSetWithSchemaAccess`), and outdated dependencies (`google-adk==1.3.0`).

This redesign modernizes `run-with-google-adk/` into a first-class Python package (`mcp_security_agent`) powered by **Google ADK v2.x**, native MCP toolsets, validated Pydantic settings, and dual entry points (an interactive terminal CLI REPL and a FastAPI web / Cloud Run server).

---

## 2. Package & Directory Structure

```text
run-with-google-adk/
├── pyproject.toml                     # Standard PEP 621 build configuration, dependencies, and CLI entry points
├── Dockerfile                         # Production multi-stage container for Cloud Run
├── README.md                          # Comprehensive documentation for CLI, Web UI, and Cloud Run deployment
├── sample.env                         # Template environment variables file
├── src/
│   └── mcp_security_agent/
│       ├── __init__.py                # Package exports and version metadata
│       ├── __main__.py                # Module executable entry point (`python -m mcp_security_agent`)
│       ├── cli.py                     # Command-line interface (`chat`, `serve`, `info`, `eval`)
│       ├── config.py                  # Pydantic Settings model with validated environment and .env loading
│       ├── agent.py                   # ADK v2.x LlmAgent definition, system prompt, and runtime lifecycle
│       ├── toolsets.py                # Native ADK MCP toolset manager (Stdio subprocess & SSE/HTTP remote)
│       ├── callbacks.py               # Request context trimming, security state injection, and logging
│       ├── state.py                   # Session state, investigation context, and memory persistence
│       └── server/                    # FastAPI web server and Cloud Run / Agent Engine endpoints
│           ├── __init__.py
│           ├── app.py                 # FastAPI application factory and lifecycle hooks
│           ├── routes.py              # Chat endpoints, health checks, and SSE streaming
│           └── static/                # Static assets for the web UI
└── tests/
    ├── conftest.py                    # Pytest fixtures for mocked MCP servers and LLM responses
    ├── test_config.py                 # Tests for settings validation and fallback resolution
    ├── test_toolsets.py               # Tests for Stdio and SSE MCP connection builders
    ├── test_agent.py                  # Tests for agent initialization and callback execution
    └── test_cli.py                    # Tests for CLI subcommands (`chat`, `serve`, `info`)
```

---

## 3. Detailed Component Design

### 3.1. Dependency Modernization (`pyproject.toml`)
* **Core Agent Framework:** `google-adk>=2.0.0`
* **Model Engine:** `google-genai>=1.20.0`, `google-cloud-aiplatform>=1.97.0`
* **Type Validation & Settings:** `pydantic>=2.0.0`, `pydantic-settings>=2.0.0`
* **Web & API Server:** `fastapi>=0.115.0`, `uvicorn>=0.30.0`
* **MCP Protocol:** `mcp>=1.0.0,<2.0.0`
* **CLI Utility:** `typer>=0.12.0` or standard `argparse`

### 3.2. Configuration & Settings (`config.py`)
Centralized using `pydantic_settings.BaseSettings`:
* **Project & Cloud:** `google_cloud_project`, `google_cloud_location`, `use_vertex_ai`, `google_api_key`, `google_model` (default: `gemini-2.5-flash`).
* **MCP Server Flags & Endpoints:**
  * `load_secops_mcp: bool` / `secops_mcp_url: str | None` / `secops_mcp_command: str`
  * `load_scc_mcp: bool` / `scc_mcp_url: str | None` / `scc_mcp_command: str`
  * `load_gti_mcp: bool` / `gti_mcp_url: str | None` / `gti_mcp_command: str`
  * `load_secops_soar_mcp: bool` / `secops_soar_mcp_url: str | None` / `secops_soar_mcp_command: str`
* **Credentials:** Support for `SECOPS_SA_PATH`, `GOOGLE_APPLICATION_CREDENTIALS`, and `SECOPS_IMPERSONATE_SERVICE_ACCOUNT`.
* **Logging & Behavior:** `log_level`, `minimal_logging`, `stdio_timeout_seconds`.

### 3.3. Multi-Transport Toolset Manager (`toolsets.py`)
Replaces `MCPToolSetWithSchemaAccess` with native ADK v2.x toolsets:
* **Stdio Transport:** Automatically resolves server package commands (`uv run --directory ...`, `python -m secops_mcp.server`, etc.) without fragile relative directory stepping.
* **Remote SSE/HTTP Transport:** Connects to remote Cloud Run or hosted MCP instances via `SseConnectionParams` / `HttpConnectionParams`.
* **Graceful Degradation:** If an MCP server fails to start or credentials are missing, logs an informative warning rather than crashing the entire agent runtime.

### 3.4. Agent & Callbacks (`agent.py`, `callbacks.py`)
* Constructs `LlmAgent` using ADK v2.x APIs.
* **System Prompt:** Comprehensive SOC investigation instructions, including UDM search strategies, IoC analysis, SCC finding remediation, and SOAR case triage.
* **Callbacks:**
  * `before_model_callback`: Trims excessive token payloads and formats tool outputs.
  * `after_model_callback`: Formats final markdown and logs telemetry.

### 3.5. Dual Serving Interfaces (`cli.py`, `server/`)
* **Terminal REPL (`mcp-security-agent chat`):**
  * Rich terminal UI with streaming responses, formatted tables, and command history.
  * Interactive slash commands: `/help`, `/tools`, `/clear`, `/exit`.
* **FastAPI Server (`mcp-security-agent serve`):**
  * `/chat` REST endpoint for web clients and automation pipelines.
  * `/chat/stream` SSE endpoint for streaming responses.
  * `/healthz` for Cloud Run readiness and liveness probes.
  * Static file serving for web UI.

---

## 4. Test Plan & Verification

1. **Hermetic Unit Tests:**
   * `tests/test_config.py`: Verifies environment variable loading and validation.
   * `tests/test_toolsets.py`: Verifies Stdio and SSE connection parameters generation.
   * `tests/test_agent.py`: Verifies agent lifecycle, prompt construction, and callback invocation with mocked LLM.
   * `tests/test_cli.py`: Verifies CLI parser and command routing.
2. **Integration Verification:**
   * Test local interactive CLI chat session.
   * Test FastAPI `/healthz` and `/chat` endpoints locally.
   * Test Docker container build.
