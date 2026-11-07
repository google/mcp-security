# Google ADK security agent

The `run-with-google-adk/` directory provides a prebuilt security operations agent (`mcp-security-agent`) built on [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) v2 and the Model Context Protocol (MCP). You can run the agent interactively in your terminal, launch its local FastAPI web console, or deploy it to Google Cloud Run.

## Prerequisites

1. **Python 3.11 or newer**
2. **[uv](https://docs.astral.sh/uv/getting-started/installation/)** (recommended) or `pip`
3. **Access to one or more Google security products**:
   - Google Security Operations SIEM (`CHRONICLE_PROJECT_ID` and `CHRONICLE_CUSTOMER_ID`)
   - Google Security Operations SOAR (`SOAR_URL` and `SOAR_APP_KEY`)
   - Google Threat Intelligence (`VT_APIKEY`)
   - Google Cloud Security Command Center (`LOAD_SCC_MCP="Y"`)
4. **Model and Google Cloud authentication**:
   - **Vertex AI (recommended for enterprise environments)**: Authenticate with your Google Cloud account and update Application Default Credentials (ADC):
     ```bash
     ACCOUNT="analyst@example.com"
     PROJECT_ID="your-project-id"
     gcloud auth login "$ACCOUNT" --update-adc
     gcloud config set project "$PROJECT_ID"
     gcloud auth application-default set-quota-project "$PROJECT_ID"
     ```
   - **Gemini Developer API**: Obtain an API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) and set `GOOGLE_API_KEY`.

## Run the agent locally

### 1. Configure your environment

Clone the repository, move into `run-with-google-adk/`, and create a `.env` file from the template:

```bash
git clone https://github.com/google/mcp-security.git
cd mcp-security/run-with-google-adk
cp .env.example .env
```

Populate `.env` with your model settings and product credentials. See [Environment variable reference](#environment-variable-reference) for every supported setting.

### 2. Verify runtime diagnostics

Run `info` to check the package version, active Gemini model, Vertex AI routing, resolved Google Cloud project, ADC file path, and enabled MCP toolsets:

```bash
uv run mcp-security-agent info
```

### 3. Start an interactive investigation

Launch the terminal REPL with the MCP toolsets you want active:

```bash
# Enable Google SecOps SIEM tools
uv run mcp-security-agent chat --secops

# Enable Google SecOps SIEM and Security Command Center with a Gemini 3 model on Vertex AI
uv run mcp-security-agent chat --secops --scc --vertex --model gemini-3.1-pro-preview
```

Pass an initial prompt on the command line to start investigating right away:

```bash
uv run mcp-security-agent chat --secops "List high-severity security alerts from the past 24 hours"
```

## CLI reference

The `mcp-security-agent` entry point exposes three subcommands.

### `mcp-security-agent info`

Prints the active runtime configuration, credential discovery status, and enabled MCP servers without starting a model session.

### `mcp-security-agent chat [PROMPT] [OPTIONS]`

Starts an interactive terminal session backed by the ADK v2 runner.

| Option | Type | Description |
| :--- | :--- | :--- |
| `PROMPT` | Argument | Optional initial prompt executed as the first turn. |
| `--secops / --no-secops` | Flag | Enable or disable Google SecOps SIEM (`server/secops`). |
| `--scc / --no-scc` | Flag | Enable or disable Security Command Center (`server/scc`). |
| `--gti / --no-gti` | Flag | Enable or disable Google Threat Intelligence (`server/gti`). |
| `--soar / --no-soar` | Flag | Enable or disable Google SecOps SOAR (`server/secops-soar`). |
| `--vertex / --no-vertex` | Flag | Route LLM calls through Vertex AI (`--vertex`) or the Gemini Developer API (`--no-vertex`). |
| `--model <name>` | String | Override `GOOGLE_MODEL` (for example, `gemini-3.1-pro-preview`). Defaults to `gemini-2.5-flash`. |
| `--project <id>` | String | Override `GOOGLE_CLOUD_PROJECT`. |
| `--customer-id <id>` | String | Override `CHRONICLE_CUSTOMER_ID`. |

### `mcp-security-agent serve [OPTIONS]`

Starts the FastAPI web console and HTTP API server.

| Option | Default | Description |
| :--- | :--- | :--- |
| `--host` | `0.0.0.0` | Network interface to bind. |
| `--port` | `8080` | Port to listen on (reads `$PORT` when set). |
| `--reload` | `False` | Enable auto-reload during local development. |
| Tool and model flags | Inherited | Accepts the same `--secops`, `--scc`, `--gti`, `--soar`, `--vertex`, `--model`, `--project`, and `--customer-id` flags as `chat`. |

## Environment variable reference

`mcp-security-agent` loads settings from environment variables and an optional `.env` file in the working directory or repository root.

```ini
# Google Cloud and Gemini model settings
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_MODEL=gemini-3.1-pro-preview
# GOOGLE_API_KEY=

# MCP server enablement (SecOps, GTI, and SOAR auto-enable when credentials are set)
LOAD_SCC_MCP=Y
# LOAD_SECOPS_MCP=Y
# LOAD_GTI_MCP=Y
# LOAD_SECOPS_SOAR_MCP=Y

# Optional remote Streamable HTTP / SSE MCP URLs
# SECOPS_MCP_URL=https://us-chronicle.googleapis.com/mcp
# SCC_MCP_URL=
# GTI_MCP_URL=
# SECOPS_SOAR_MCP_URL=

# Optional service account key or impersonation
# SECOPS_SA_PATH=/path/to/service-account.json
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
# SECOPS_IMPERSONATE_SERVICE_ACCOUNT=soc-agent@your-project-id.iam.gserviceaccount.com

# Google SecOps SIEM
CHRONICLE_PROJECT_ID=your-project-id
CHRONICLE_CUSTOMER_ID=a1b2c3d4-e5f6-4321-abcd-ef1234567890
CHRONICLE_REGION=us

# Google Threat Intelligence
VT_APIKEY=

# Google SecOps SOAR
SOAR_URL=
SOAR_APP_KEY=

# Runtime settings
STDIO_PARAM_TIMEOUT=60.0
MINIMAL_LOGGING=N
```

| Variable | Default | Description |
| :--- | :--- | :--- |
| `GOOGLE_CLOUD_PROJECT` | `None` | Google Cloud project ID for Vertex AI and Cloud Run. |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` | Vertex AI location. Set `global` when using preview Gemini 3 models such as `gemini-3.1-pro-preview`. |
| `GOOGLE_GENAI_USE_VERTEXAI` | `False` | Set `True` to route model calls through Vertex AI with ADC. Auto-enables when `GOOGLE_CLOUD_PROJECT` is set and `GOOGLE_API_KEY` is unset. |
| `GOOGLE_API_KEY` | `None` | Gemini Developer API key when `GOOGLE_GENAI_USE_VERTEXAI` is `False`. |
| `GOOGLE_MODEL` | `gemini-2.5-flash` | Model identifier passed to ADK (set `gemini-3.1-pro-preview` or `gemini-3-flash-preview` for Gemini 3). |
| `LOAD_SCC_MCP` | `False` | Enable `server/scc` using ADC. |
| `LOAD_SECOPS_MCP` | Auto | Enable `server/secops`. Defaults to `True` when both `CHRONICLE_PROJECT_ID` and `CHRONICLE_CUSTOMER_ID` are set. |
| `LOAD_GTI_MCP` | Auto | Enable `server/gti`. Defaults to `True` when `VT_APIKEY` is set. |
| `LOAD_SECOPS_SOAR_MCP` | Auto | Enable `server/secops-soar`. Defaults to `True` when both `SOAR_URL` and `SOAR_APP_KEY` are set. |
| `SECOPS_MCP_URL`, `SCC_MCP_URL`, `GTI_MCP_URL`, `SECOPS_SOAR_MCP_URL` | `None` | Connect to remote HTTP or SSE MCP endpoints instead of spawning local `stdio` subprocesses. |
| `CHRONICLE_PROJECT_ID` | `None` | Google Cloud project ID bound to your Google SecOps tenant. |
| `CHRONICLE_CUSTOMER_ID` | `None` | Google SecOps customer UUID (for example, `a1b2c3d4-e5f6-4321-abcd-ef1234567890`). |
| `CHRONICLE_REGION` | `us` | Google SecOps region (`us`, `eu`, `asia`, or regional code such as `europe-west2`). |
| `SECOPS_SA_PATH` | `None` | Optional service account JSON key path for `server/secops`. |
| `SECOPS_IMPERSONATE_SERVICE_ACCOUNT` | `None` | Optional service account email to impersonate. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Auto-discovered | Explicit credentials file path; auto-detects `.gcloud/application_default_credentials.json` if present. |
| `VT_APIKEY` | `None` | Google Threat Intelligence (VirusTotal) API key. |
| `SOAR_URL` | `None` | Base URL for your Google SecOps SOAR instance. |
| `SOAR_APP_KEY` | `None` | API key for Google SecOps SOAR. |
| `STDIO_PARAM_TIMEOUT` | `60.0` | Timeout in seconds for MCP subprocess startup and tool execution. |
| `MINIMAL_LOGGING` | `False` | Set `Y` in production to suppress prompt and query payloads in logs. |

## Run the web UI and HTTP API

Start the FastAPI server locally:

```bash
uv run mcp-security-agent serve --port 8080
```

Open `http://localhost:8080` in your browser to use the investigation console. The server exposes five HTTP endpoints:

- **`GET /`**: Serves the interactive web investigation console.
- **`GET /healthz`**: Liveness and readiness check returning `{"status": "ok"}`.
- **`GET /info`**: Returns JSON runtime metadata (version, active model, and loaded toolsets).
- **`POST /chat`**: Synchronous chat endpoint accepting `{"prompt": "string", "session_id": "optional"}`.
- **`GET /chat?message=...`**: Server-Sent Events (SSE) token-streaming endpoint.

## Deploy to Google Cloud Run

`run-with-google-adk/Dockerfile` packages `mcp-security-agent serve` for Cloud Run.

### 1. Deploy from source

Run the deployment from `run-with-google-adk/` and require IAM authentication on the Cloud Run service:

```bash
PROJECT_ID="your-project-id"
CUSTOMER_ID="a1b2c3d4-e5f6-4321-abcd-ef1234567890"
REGION="us-central1"

gcloud run deploy mcp-security-agent-service \
  --source . \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --no-allow-unauthenticated \
  --memory 2Gi \
  --set-env-vars="LOAD_SECOPS_MCP=Y,LOAD_SCC_MCP=Y,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=global,GOOGLE_MODEL=gemini-3.1-pro-preview,CHRONICLE_PROJECT_ID=$PROJECT_ID,CHRONICLE_CUSTOMER_ID=$CUSTOMER_ID,MINIMAL_LOGGING=Y"
```

### 2. Grant runtime IAM roles

Grant the Cloud Run runtime service account least-privilege roles for the enabled toolsets:

- **Vertex AI User** (`roles/aiplatform.user`) for Gemini model calls on Vertex AI.
- **Chronicle API Viewer** (`roles/chronicle.viewer`) on the Google SecOps project.
- **Security Center Findings Viewer** (`roles/securitycenter.findingsViewer`) and **Cloud Asset Viewer** (`roles/cloudasset.viewer`) when `LOAD_SCC_MCP=Y`.

### 3. Connect through the authenticated Cloud Run proxy

Grant authorized analysts **Cloud Run Invoker** (`roles/run.invoker`) and connect locally through `gcloud`:

```bash
PROJECT_ID="your-project-id"
REGION="us-central1"
gcloud run services proxy mcp-security-agent-service --project "$PROJECT_ID" --region "$REGION"
```

The authenticated service is then reachable at `http://localhost:8080`.

## Integrate custom MCP servers

You can attach internal identity providers, EDR platforms, or ticketing servers as modular sub-agents. Reference implementations live in `run-with-google-adk/sample_servers_to_integrate/`:

- `sample_servers_to_integrate/mcp_servers/` contains sample `demo_idp` and `demo_xdr` MCP servers.
- `sample_servers_to_integrate/agents/` contains `demo_idp_agent.py` and `demo_xdr_agent.py` sub-agent wrappers.

Wire custom sub-agents into `LlmAgent` inside `src/mcp_security_agent/agent.py`:

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

## Run unit tests

Run the hermetic unit test suite from `run-with-google-adk/`:

```bash
uv run --extra test pytest tests/
```
