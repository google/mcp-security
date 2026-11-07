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
cp .env.example .env
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

### `.env.example` Template

```properties
# Google Cloud & LLM Settings
GOOGLE_CLOUD_PROJECT=
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY=
GOOGLE_MODEL=gemini-2.5-flash

# MCP Server Enablement Flags
# (SCC uses Google Cloud ADC. SecOps, GTI, and SOAR auto-enable when credentials below are populated.
# You can explicitly set LOAD_*_MCP to Y or N to override auto-detection.)
LOAD_SCC_MCP=Y
# LOAD_SECOPS_MCP=
# LOAD_GTI_MCP=
# LOAD_SECOPS_SOAR_MCP=

# Credentials & Service Account Impersonation
SECOPS_SA_PATH=
GOOGLE_APPLICATION_CREDENTIALS=
SECOPS_IMPERSONATE_SERVICE_ACCOUNT=

# Google SecOps (Chronicle SIEM) Settings - Populating enables SecOps MCP
CHRONICLE_PROJECT_ID=
CHRONICLE_CUSTOMER_ID=
CHRONICLE_REGION=us

# Google Threat Intelligence (GTI / VirusTotal) - Populating enables GTI MCP
VT_APIKEY=

# SecOps SOAR Settings - Populating enables SOAR MCP
SOAR_URL=
SOAR_APP_KEY=

# Runtime Settings
STDIO_PARAM_TIMEOUT=60.0
MINIMAL_LOGGING=N
MCP_AGENT_SESSION_SECRET=
MCP_AGENT_IAP_AUDIENCE=
MCP_AGENT_REQUIRE_IAP=False
```

### Environment Variable Reference

| Variable | Default | Description |
| :--- | :--- | :--- |
| `GOOGLE_CLOUD_PROJECT` | None | Google Cloud Project ID for Vertex AI and Cloud Run deployment. |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` | Google Cloud region for Vertex AI endpoints. |
| `GOOGLE_GENAI_USE_VERTEXAI`| `False` | Set `True` to route LLM requests through Vertex AI (uses ADC). Set `False` to use Gemini API (requires `GOOGLE_API_KEY`). |
| `GOOGLE_API_KEY` | None | Gemini API Key (required when `GOOGLE_GENAI_USE_VERTEXAI=False`). |
| `GOOGLE_MODEL` | `gemini-2.5-flash` | Gemini model name (e.g. `gemini-2.5-flash`, `gemini-2.5-pro`). |
| `LOAD_SCC_MCP` | `False` | Enables Security Command Center MCP (`server/scc`). Uses ADC. |
| `LOAD_SECOPS_MCP` | Auto | Enables Chronicle SIEM MCP. Auto-enables if `CHRONICLE_PROJECT_ID` and `CUSTOMER_ID` are set. |
| `LOAD_GTI_MCP` | Auto | Enables Google Threat Intelligence MCP. Auto-enables if `VT_APIKEY` is set. |
| `LOAD_SECOPS_SOAR_MCP` | Auto | Enables SecOps SOAR MCP. Auto-enables if `SOAR_URL` and `SOAR_APP_KEY` are set. |
| `CHRONICLE_PROJECT_ID` | None | GCP project ID hosting Chronicle SIEM. |
| `CHRONICLE_CUSTOMER_ID` | None | Chronicle Customer ID (UUID). |
| `CHRONICLE_REGION` | `us` | Chronicle regional gateway (`us`, `europe`, `asia`). |
| `VT_APIKEY` | None | VirusTotal / GTI API Key (presence auto-activates GTI tools). |
| `SOAR_URL` | None | Instance URL for SecOps SOAR (presence auto-activates SOAR tools). |
| `SOAR_APP_KEY` | None | API Key for SecOps SOAR. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Auto-detected | Path to service account key file or local `.gcloud/application_default_credentials.json`. |
| `STDIO_PARAM_TIMEOUT` | `60.0` | Timeout in seconds for MCP subprocess initialization and tool execution. |
| `MINIMAL_LOGGING` | `False` | Reduces logging verbosity to suppress sensitive query content in production. |
| `MCP_AGENT_SESSION_SECRET` | Random 32 bytes | HMAC-SHA256 signing secret for `mcp_agent_session` cookies. Configure a shared secret across instances in multi-replica deployments. |
| `MCP_AGENT_IAP_AUDIENCE` | None | Target audience string for Google Cloud Identity-Aware Proxy (IAP) (format: `/projects/<PROJECT_NUMBER>/global/backendServices/<SERVICE_ID>`). When configured, incoming requests must include a cryptographically verified `X-Goog-Iap-Jwt-Assertion` ES256 token matching this audience. |
| `MCP_AGENT_REQUIRE_IAP` | `False` | When `True`, enforces that all non-probe endpoints must be authenticated via Identity-Aware Proxy. Requires `MCP_AGENT_IAP_AUDIENCE` to be set. |

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
* **`GET /get_session`**: Issues a `session_id` and sets an `HttpOnly`, `SameSite=Lax` HMAC-SHA256 signed capability cookie (`mcp_agent_session`) binding the client to `(user_id, session_id)`.
* **`POST /chat`**: Primary chat endpoint accepting JSON requests (`{"prompt": "..."}`). For streaming SSE responses, supply the HTTP header `Accept: text/event-stream`.

### Session Authorization and Identity Binding

Session endpoints bind `(user_id, session_id)` ownership to the caller before creating or resuming ADK sessions:

* **Signed capability cookie mode (default).** `GET /get_session` issues an `HttpOnly`, `SameSite=Lax` HMAC-SHA256 signed `mcp_agent_session` cookie (`Secure` when served over HTTPS or `X-Forwarded-Proto: https`) and records session ownership on the server. The bundled web UI uses same-origin `fetch`, so browsers send this cookie automatically. Direct API callers can use single-turn `POST /chat` (`{"prompt": "..."}`) without cookies or explicit IDs, which mints a new session and returns a signed cookie for follow-up turns. Requests to `/chat` with a missing cookie on stateful turns, a tampered HMAC signature, mismatched `user_id`, or another client's `session_id` return `HTTP 403`. Set `MCP_AGENT_SESSION_SECRET` to a shared secret when running multiple replicas behind a load balancer; when unset, each process generates a random 32-byte key at startup.
* **Browser CSRF and Same-Origin protection.** The server validates browser `Sec-Fetch-Site` (rejecting `cross-site` and `same-site`) and `Origin` headers against the target host (or `X-Forwarded-Host` behind IAP) on session and chat endpoints to protect against cross-site request forgery.
* **Cryptographic Identity-Aware Proxy (IAP) mode.** When `MCP_AGENT_IAP_AUDIENCE` or `MCP_AGENT_REQUIRE_IAP` is configured, the server cryptographically verifies incoming `X-Goog-Iap-Jwt-Assertion` ES256 tokens against Google's public key endpoint (`https://www.gstatic.com/iap/verify/public_key-jwk`), validating the audience, issuer (`https://cloud.google.com/iap`), algorithm, key ID, and expiry. The verified email is bound to the session. Unsigned headers such as `X-Goog-Authenticated-User-Email` are ignored entirely.

---

## Deploying to Google Cloud Run

The package includes a production-ready [`Dockerfile`](./Dockerfile) configured to run `mcp-security-agent serve` on Cloud Run.

### 1. Build and Deploy

Define your configuration variables first:

```bash
PROJECT_ID="YOUR_PROJECT_ID"
REGION="us-central1"
SERVICE_NAME="mcp-security-agent-service"
```

Deploy the service directly from the repository root:

```bash
gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --project "$PROJECT_ID" \
  --no-allow-unauthenticated \
  --set-env-vars="LOAD_SECOPS_MCP=Y,LOAD_SCC_MCP=Y,GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,CHRONICLE_PROJECT_ID=$PROJECT_ID,CHRONICLE_CUSTOMER_ID=YOUR_CUSTOMER_ID"
```

### 2. IAM Roles

Ensure the runtime Service Account used by Cloud Run has the appropriate IAM permissions:
* **Chronicle API Viewer** (`roles/chronicle.viewer`) on the project hosting Chronicle.
* **Security Center Finding Viewer** (`roles/securitycenter.findingsViewer`) for SCC findings.
* **Vertex AI User** (`roles/aiplatform.user`) for Vertex AI model execution.

### 3. Restricting Access in Production

Two primary production deployment architectures are supported:

#### Option A: Cloud Run with IAM Invoker Authentication

Calls to Cloud Run are authenticated at the Google Cloud IAM boundary.
1. In Cloud Run, select the service and navigate to **Security** -> **Require authentication**.
2. Grant `Cloud Run Invoker` (`roles/run.invoker`) to authorized users or groups.
3. Configure a shared `MCP_AGENT_SESSION_SECRET` across replicas in Secret Manager.
4. Authorized users can securely access the service locally via proxy:
   ```bash
   gcloud run services proxy "$SERVICE_NAME" --project "$PROJECT_ID" --region "$REGION"
   ```
   The service is reachable at `http://localhost:8080`.

#### Option B: Cloud Run behind Identity-Aware Proxy (IAP) & Load Balancer

1. Deploy Cloud Run with ingress restricted to internal and load balancer traffic (`--ingress=internal-and-cloud-load-balancing`).
2. Front Cloud Run with an External Application Load Balancer and enable Identity-Aware Proxy (IAP) on the backend service.
3. Retrieve your IAP audience string: `/projects/<PROJECT_NUMBER>/global/backendServices/<SERVICE_ID>`.
4. Configure container environment variables in Secret Manager:
   * `MCP_AGENT_IAP_AUDIENCE`: `/projects/<PROJECT_NUMBER>/global/backendServices/<SERVICE_ID>`
   * `MCP_AGENT_REQUIRE_IAP`: `True`
   * `MCP_AGENT_SESSION_SECRET`: Shared secret across replicas
5. The container cryptographically verifies each caller's `X-Goog-Iap-Jwt-Assertion` ES256 signature and binds the verified enterprise identity to all sessions.

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
uv run --extra test pytest tests/
```

All unit tests run hermetically using mocked MCP connection parameters and simulated LLM responses.



