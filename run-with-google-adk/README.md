# Google ADK Security Agent Guide

This guide provides instructions on how to run the Autonomous Security Operations Center (SOC) Agent powered by Google ADK v2 and the Model Context Protocol (MCP), both locally via an interactive CLI and deployed to Google Cloud Run.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quickstart: Running Agent Locally](#quickstart-running-agent-locally)
3. [CLI Commands & Options](#cli-commands--options)
4. [Configuration & Environment Variables](#configuration--environment-variables)
5. [Running the Web UI & API Server](#running-the-web-ui--api-server)
6. [Deploying to Google Cloud Run](#deploying-to-google-cloud-run)
7. [Integrating Custom MCP Servers](#integrating-custom-mcp-servers)
8. [Testing & Verification](#testing--verification)

---

## Prerequisites

1. **Python 3.11+**
2. [**uv**](https://docs.astral.sh/uv/) (recommended) or `pip`
3. **Google Cloud Account / Project** with access to one or more of:
   * Google SecOps (Chronicle SIEM)
   * Google Cloud Security Command Center (SCC)
   * Google Threat Intelligence (GTI / VirusTotal)
   * Google SecOps SOAR (Siemplify)
4. **Authentication**:
   * For Google Cloud services (Chronicle, SCC, Vertex AI): Authenticate using Application Default Credentials:
     ```bash
     gcloud auth application-default login
     ```
   * Alternatively, to use the Gemini Developer API without Vertex AI, obtain an API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) and configure `GOOGLE_API_KEY`.

---

## Quickstart: Running Agent Locally

### 1. Setup Environment

```bash
cd run-with-google-adk

# Copy the sample environment template
cp sample.env .env
```

Configure your credentials and project IDs in `.env` (see [Configuration](#configuration--environment-variables)).

### 2. Verify Diagnostics

Run `info` to verify package installation, active model, resolved GCP project/ADC credentials, and configured MCP servers:

```bash
uv run mcp-security-agent info
```

### 3. Launch Interactive Chat

Start an interactive threat investigation session with your desired MCP toolsets:

```bash
# Enable Chronicle SIEM MCP tools (alerts, UDM search, rules)
uv run mcp-security-agent chat --secops

# Enable both SecOps SIEM and Security Command Center (SCC)
uv run mcp-security-agent chat --secops --scc
```

You can also provide an initial prompt directly on the command line:

```bash
uv run mcp-security-agent chat --secops "List recent critical security alerts from the past 24 hours"
```

## CLI Commands & Options

The package provides the `mcp-security-agent` CLI entry point.

### `mcp-security-agent info`
Displays current runtime diagnostics:
* Package version
* Active Gemini model & Vertex AI status
* Resolved Google Cloud Project ID and Application Default Credentials (ADC) path
* Toolset status for each supported MCP server

### `mcp-security-agent chat [PROMPT] [OPTIONS]`
Starts an interactive terminal REPL for security investigations.

| Option | Type | Description |
| :--- | :--- | :--- |
| `PROMPT` | Argument | Optional initial prompt to execute immediately upon startup. |
| `--secops / --no-secops` | Flag | Enable or disable Chronicle SIEM MCP (`server/secops`). |
| `--scc / --no-scc` | Flag | Enable or disable Security Command Center MCP (`server/scc`). |
| `--gti / --no-gti` | Flag | Enable or disable Google Threat Intelligence MCP (`server/gti`). |
| `--soar / --no-soar` | Flag | Enable or disable SecOps SOAR MCP (`server/secops-soar`). |
| `--vertex / --no-vertex` | Flag | Toggle Vertex AI (`--vertex`) vs Gemini Developer API (`--no-vertex`). |
| `--model <name>` | String | Override Gemini model name (default: `gemini-2.5-flash`). |
| `--project <id>` | String | Override Google Cloud Project ID. |
| `--customer-id <id>` | String | Override Chronicle Customer ID. |

### `mcp-security-agent serve [OPTIONS]`
Launches the FastAPI application for web UI access or Cloud Run hosting.

| Option | Default | Description |
| :--- | :--- | :--- |
| `--host` | `0.0.0.0` | Network interface to bind to. |
| `--port` | `8080` | Port to listen on (reads `$PORT` environment variable if set). |
| `--reload` | `False` | Enable auto-reload for local development. |
| Tool flags | | Supports the same tool toggles as `chat` (`--secops`, `--scc`, `--gti`, `--soar`, etc.). |

---

## Configuration & Environment Variables

The agent reads configuration from environment variables and an optional `.env` file located in the working directory.

### `sample.env` Template

```properties
# Google Cloud & LLM Settings
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_MODEL=gemini-2.5-flash

# MCP Server Enablement Flags (Y/N or True/False)
LOAD_SECOPS_MCP=Y
LOAD_SCC_MCP=Y
LOAD_GTI_MCP=N
LOAD_SECOPS_SOAR_MCP=N

# Credentials & Service Account Impersonation
SECOPS_SA_PATH=
GOOGLE_APPLICATION_CREDENTIALS=
SECOPS_IMPERSONATE_SERVICE_ACCOUNT=

# Google SecOps (Chronicle SIEM) Settings
CHRONICLE_PROJECT_ID=your-chronicle-project-id
CHRONICLE_CUSTOMER_ID=your-chronicle-customer-id
CHRONICLE_REGION=us

# Google Threat Intelligence (GTI / VirusTotal)
VT_APIKEY=your-virustotal-api-key

# SecOps SOAR Settings
SOAR_URL=https://your-soar-tenant.siemplify-soar.com
SOAR_APP_KEY=your-soar-app-key

# Runtime Settings
STDIO_PARAM_TIMEOUT=60.0
MINIMAL_LOGGING=N
```

### Environment Variable Reference

| Variable | Default | Description |
| :--- | :--- | :--- |
| `GOOGLE_CLOUD_PROJECT` | None | Google Cloud Project ID for Vertex AI and Cloud Run deployment. |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` | Google Cloud region for Vertex AI endpoints. |
| `GOOGLE_GENAI_USE_VERTEXAI`| `False` | Set `True` to route LLM requests through Vertex AI (uses ADC). Set `False` to use Gemini API (requires `GOOGLE_API_KEY`). |
| `GOOGLE_API_KEY` | None | Gemini API Key (required when `GOOGLE_GENAI_USE_VERTEXAI=False`). |
| `GOOGLE_MODEL` | `gemini-2.5-flash` | Gemini model name (e.g. `gemini-2.5-flash`, `gemini-2.5-pro`). |
| `LOAD_SECOPS_MCP` | `False` | Enables Chronicle SIEM MCP (`server/secops`). |
| `LOAD_SCC_MCP` | `False` | Enables Security Command Center MCP (`server/scc`). |
| `LOAD_GTI_MCP` | `False` | Enables Google Threat Intelligence MCP (`server/gti`). |
| `LOAD_SECOPS_SOAR_MCP` | `False` | Enables SecOps SOAR MCP (`server/secops-soar`). |
| `CHRONICLE_PROJECT_ID` | None | GCP project ID hosting Chronicle SIEM. |
| `CHRONICLE_CUSTOMER_ID` | None | Chronicle Customer ID (UUID). |
| `CHRONICLE_REGION` | `us` | Chronicle regional gateway (`us`, `europe`, `asia`). |
| `VT_APIKEY` | None | VirusTotal / GTI API Key. |
| `SOAR_URL` | None | Instance URL for SecOps SOAR (Siemplify). |
| `SOAR_APP_KEY` | None | API Key for SecOps SOAR. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Auto-detected | Path to service account key file or local `.gcloud/application_default_credentials.json`. |
| `STDIO_PARAM_TIMEOUT` | `60.0` | Timeout in seconds for MCP subprocess initialization and tool execution. |
| `MINIMAL_LOGGING` | `False` | Reduces logging verbosity to suppress sensitive query content in production. |

---

## Running the Web UI & API Server

The built-in FastAPI server provides an interactive web dashboard and REST / Server-Sent Events (SSE) API endpoints.

```bash
uv run mcp-security-agent serve --port 8080
```

Open `http://localhost:8080` in your browser to access the SOC Agent UI.

### REST & Streaming Endpoints

* **`GET /`**: Serves the bundled web landing page and interactive investigation console.
* **`GET /healthz`**: Liveness & readiness probe returning `{"status": "ok"}` for Cloud Run.
* **`GET /info`**: Returns JSON metadata including package version, active model, and toolset configurations.
* **`POST /chat`**: Synchronous chat endpoint accepting `{"prompt": "string", "session_id": "optional"}`.
* **`GET /chat/stream?prompt=...`**: Server-Sent Events (SSE) token streaming endpoint.

---

## Deploying to Google Cloud Run

The package includes a production-ready [`Dockerfile`](./Dockerfile) configured to run `mcp-security-agent serve` on Cloud Run.

### 1. Build and Deploy

Deploy the service directly from the repository root:

```bash
gcloud run deploy mcp-security-agent-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="LOAD_SECOPS_MCP=Y,LOAD_SCC_MCP=Y,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,CHRONICLE_PROJECT_ID=YOUR_PROJECT_ID,CHRONICLE_CUSTOMER_ID=YOUR_CUSTOMER_ID"
```

### 2. IAM Roles

Ensure the runtime Service Account used by Cloud Run has the appropriate IAM permissions:
* **Chronicle API Viewer** (`roles/chronicle.viewer`) on the project hosting Chronicle.
* **Security Center Finding Viewer** (`roles/securitycenter.findingsViewer`) for SCC findings.
* **Vertex AI User** (`roles/aiplatform.user`) for Vertex AI model execution.

### 3. Restricting Access in Production

To protect the service in production:
1. In Cloud Run, select `mcp-security-agent-service` and navigate to **Security**.
2. Select **Require authentication**.
3. Under **Permissions**, grant `Cloud Run Invoker` (`roles/run.invoker`) to authorized users.
4. Authorized users can securely access the service locally via proxy:
   ```bash
   gcloud run services proxy mcp-security-agent-service --project YOUR_PROJECT_ID --region us-central1
   ```
   The service will then be reachable at `http://localhost:8080`.

### 4. Memory Limits & Logging Verbosity

* If MCP toolsets process large result sets, consider increasing container memory in Cloud Run Settings to 1 GiB or 2 GiB.
* In production, set `MINIMAL_LOGGING=Y` to suppress full LLM prompt/response logging and reduce Cloud Logging costs.

## Integrating Custom MCP Servers

You can integrate custom security products (such as internal IdPs, custom EDRs, or ticketing systems) using modular sub-agents.

Reference implementations are provided in [`sample_servers_to_integrate/`](./sample_servers_to_integrate/):
* **Sample MCP Servers**: [`sample_servers_to_integrate/mcp_servers/`](./sample_servers_to_integrate/mcp_servers/) (`demo_idp` and `demo_xdr`).
* **Sample Sub-Agents**: [`sample_servers_to_integrate/agents/`](./sample_servers_to_integrate/agents/) (`demo_idp_agent.py` and `demo_xdr_agent.py`).

To attach them to the primary agent in [`src/mcp_security_agent/agent.py`](./src/mcp_security_agent/agent.py):

```python
from sample_servers_to_integrate.agents.demo_idp_agent import create_demo_idp_agent
from sample_servers_to_integrate.agents.demo_xdr_agent import create_demo_xdr_agent

idp_agent = create_demo_idp_agent()
xdr_agent = create_demo_xdr_agent()

agent = LlmAgent(
    name="SecurityOperationsAgent",
    model=settings.google_model,
    instruction=settings.default_prompt or SOC_AGENT_SYSTEM_PROMPT,
    tools=toolsets,
    sub_agents=[sub for sub in [idp_agent, xdr_agent] if sub is not None],
    before_model_callback=bmc_trim_llm_request,
)
```

Configure credentials in `.env`:
```properties
LOAD_XDR_MCP=Y
XDR_CLIENT_ID=demo_client_id
XDR_CLIENT_SECRET=demo_client_secret

LOAD_IDP_MCP=Y
IDP_CLIENT_ID=demo_client_id
IDP_CLIENT_SECRET=demo_client_secret
```

Sample reference interfaces:

**Sample XDR Integration:**
![](./static/demo-xdr.png)

**Sample IDP Integration:**
![](./static/demo-idp.png)

---

## Testing & Verification

Run the hermetic test suite:

```bash
uv run pytest tests/
```

All 21 unit tests run hermetically using mocked MCP connection parameters and simulated LLM responses.



