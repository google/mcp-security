# Google ADK security agent starter

`run-with-google-adk` provides a minimal [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) v2 `root_agent` package (`mcp_security_agent`). It connects Gemini on Vertex AI (`gemini-3.8-flash`) to the Google Cloud Security Model Context Protocol (MCP) servers in this repository through `McpToolset`.

The package exports `root_agent` and `build_agent()` directly for ADK's built-in tooling without custom web-server or session-management code:

- Local terminal investigations: `uv run adk run mcp_security_agent`
- Local single-developer UI: `uv run adk web` on `127.0.0.1:8000`
- Production multi-user hosting: managed Vertex AI Agent Engine and Gemini Enterprise

## Prerequisites and setup

1. Install Python 3.11 or newer and [`uv`](https://docs.astral.sh/uv/getting-started/installation/).
2. Enable the Vertex AI API in your Google Cloud project and authenticate Application Default Credentials (ADC):

   ```bash
   PROJECT_ID="your-gcp-project-id"
   gcloud config set project "$PROJECT_ID"
   gcloud auth application-default login
   gcloud auth application-default set-quota-project "$PROJECT_ID"
   ```

3. Copy the environment template in `run-with-google-adk` and populate your Vertex AI and MCP credentials:

   ```bash
   cd run-with-google-adk
   cp .env.example .env
   ```

4. Edit `.env` with your Google Cloud project ID and the credentials for the security products you want to attach. For example, to query a production or test Google SecOps tenant with `gemini-3.8-flash`:

   ```ini
   GOOGLE_GENAI_USE_VERTEXAI=True
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   GOOGLE_CLOUD_LOCATION=global
   GOOGLE_MODEL=gemini-3.8-flash

   CHRONICLE_PROJECT_ID=your-secops-project-id
   CHRONICLE_CUSTOMER_ID=a1b2c3d4-e5f6-4321-abcd-ef1234567890
   CHRONICLE_REGION=us
   ```

   `mcp_security_agent` loads `.env` without overriding variables already exported in your shell. Each MCP server activates automatically when its required credentials or remote MCP URL are present.

## Run locally

### Local CLI

Start an interactive terminal session with `adk run`:

```bash
cd run-with-google-adk
uv run adk run mcp_security_agent
```

### Local developer UI

Launch ADK's local developer UI on `http://127.0.0.1:8000` and select `mcp_security_agent`:

```bash
cd run-with-google-adk
uv run adk web
```

> **Note:** `adk web` is intended for local single-developer testing on `127.0.0.1:8000`. For shared team or production environments, deploy to Vertex AI Agent Engine and Gemini Enterprise.

## Environment variables and credential isolation

The table below lists every variable in `.env.example`:

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `GOOGLE_GENAI_USE_VERTEXAI` | `True` | Route Gemini requests through Vertex AI. |
| `GOOGLE_CLOUD_PROJECT` | *(empty)* | Google Cloud project ID for Vertex AI model calls and default ADC context. |
| `GOOGLE_CLOUD_LOCATION` | `global` | Vertex AI endpoint location (for example, `global` or `us-central1`). |
| `GOOGLE_MODEL` | `gemini-3.8-flash` | Gemini model identifier passed to `LlmAgent`. |
| `CHRONICLE_PROJECT_ID` | *(empty)* | Google Cloud project ID associated with your Google SecOps SIEM tenant. |
| `CHRONICLE_CUSTOMER_ID` | *(empty)* | Google SecOps customer UUID, such as `a1b2c3d4-e5f6-4321-abcd-ef1234567890`. |
| `CHRONICLE_REGION` | `us` | Google SecOps regional API endpoint, such as `us` or `eu`. |
| `VT_APIKEY` | *(empty)* | API key for the Google Threat Intelligence (VirusTotal) MCP server. |
| `SOAR_URL` | *(empty)* | Base URL for your Google SecOps SOAR instance, such as `https://example.siemplify-soar.com:443`. |
| `SOAR_APP_KEY` | *(empty)* | API application key for the Google SecOps SOAR MCP server. |
| `LOAD_SCC_MCP` | `False` | Set to `True` to attach the local Security Command Center MCP server, which authenticates through ADC. |
| `LOAD_SECOPS_MCP` | *(empty / auto)* | Optional `True` or `False` override for the Google SecOps SIEM MCP toolset. Auto-enables when `CHRONICLE_PROJECT_ID` and `CHRONICLE_CUSTOMER_ID` or `SECOPS_MCP_URL` are set. |
| `LOAD_GTI_MCP` | *(empty / auto)* | Optional `True` or `False` override for the Google Threat Intelligence MCP toolset. Auto-enables when `VT_APIKEY` or `GTI_MCP_URL` is set. |
| `LOAD_SECOPS_SOAR_MCP` | *(empty / auto)* | Optional `True` or `False` override for the Google SecOps SOAR MCP toolset. Auto-enables when `SOAR_URL` and `SOAR_APP_KEY` or `SECOPS_SOAR_MCP_URL` are set. |
| `SECOPS_MCP_URL` | *(empty)* | Optional remote Streamable HTTP MCP URL for Google SecOps, such as `https://chronicle.us.rep.googleapis.com/mcp`. |
| `SCC_MCP_URL` | *(empty)* | Optional remote Streamable HTTP MCP URL for Security Command Center. |
| `GTI_MCP_URL` | *(empty)* | Optional remote Streamable HTTP MCP URL for Google Threat Intelligence. |
| `SECOPS_SOAR_MCP_URL` | *(empty)* | Optional remote Streamable HTTP MCP URL for Google SecOps SOAR. |
| `STDIO_PARAM_TIMEOUT` | `60.0` | Startup timeout in seconds for local `stdio` MCP subprocesses. |

### Least-privilege subprocess credential isolation

When `mcp_security_agent` launches local `stdio` MCP servers from `../server/`, it never copies `os.environ` wholesale into child processes. Instead, `agent.py` constructs a minimal runtime allowlist (`PATH`, `HOME`, `USER`, `VIRTUAL_ENV`, `SSL_CERT_FILE`, `SSL_CERT_DIR`, `REQUESTS_CA_BUNDLE`, `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `http_proxy`, `https_proxy`, `no_proxy`, `GOOGLE_APPLICATION_CREDENTIALS`, `CLOUDSDK_CONFIG`, `GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_QUOTA_PROJECT`, plus mTLS defaults `GOOGLE_API_USE_CLIENT_CERTIFICATE=false`, `GOOGLE_API_USE_MTLS_ENDPOINT=never`, and `CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE=false`) and merges only the secret keys owned by that specific MCP server:

- `secops` receives `CHRONICLE_PROJECT_ID`, `CHRONICLE_CUSTOMER_ID`, `CHRONICLE_REGION`, and optional `SECOPS_SA_PATH` and `SECOPS_IMPERSONATE_SERVICE_ACCOUNT` variables.
- `gti` receives `VT_APIKEY`.
- `secops-soar` receives `SOAR_URL`, `SOAR_APP_KEY`, and optional `SOAR_VERIFY_SSL`.
- `scc` receives only the base runtime and ADC allowlist.

Unrelated environment variables in your shell stay out of every MCP child process, and credentials for one security product are never exposed to another server's subprocess. When a `*_MCP_URL` variable is set, `agent.py` connects over `StreamableHTTPConnectionParams` and rejects non-HTTPS URLs except on loopback hosts (`localhost`, `127.0.0.1`, and `[::1]`).

## Production deployment

Deploy `mcp_security_agent` to managed **Vertex AI Agent Engine** and surface it through **Gemini Enterprise** instead of operating custom web-server code.

### Deploy to Vertex AI Agent Engine

For managed cloud deployments, configure remote HTTPS MCP endpoints where available, such as the hosted [Google SecOps Remote MCP Server](../docs/remote_server.md) via `SECOPS_MCP_URL="https://chronicle.us.rep.googleapis.com/mcp"`, and run `adk deploy agent_engine`:

```bash
cd run-with-google-adk

PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
STAGING_BUCKET="gs://your-adk-staging-bucket"

uv run adk deploy agent_engine \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --staging_bucket="$STAGING_BUCKET" \
  --display_name="mcp-security-agent" \
  mcp_security_agent
```

### Registering with Gemini Enterprise

After deploying to Vertex AI Agent Engine, you can register the deployed Reasoning Engine resource in **Gemini Enterprise** to provide:

- Managed web chat interface and agent discovery for SOC teams.
- Google Cloud IAM and Workforce Identity integration with managed `VertexAiSessionService` state persistence.
- Cloud Audit Logs, VPC Service Controls support, and OAuth credential delegation for hosted Google Cloud MCP endpoints.

## Run hermetic tests

Run the unit test suite from `run-with-google-adk`:

```bash
cd run-with-google-adk
uv run --extra test pytest tests/
```

The test suite runs offline without live cloud credentials and verifies ADK `AgentLoader` discovery, credential-based server activation, `LOAD_*_MCP` overrides, `*_MCP_URL` scheme and loopback validation, and per-subprocess secret isolation.

## Alternative MCP harnesses

If you want an interactive CLI or IDE workflow for these MCP servers without maintaining a Python ADK package, consider these harnesses:

- **[Google SecOps Gemini CLI Extension](../docs/google_secops_extension.md).** Prebuilt alert triage, investigation, and threat-hunting skills for Gemini CLI in `extensions/google-secops`.
- **[Antigravity](https://antigravity.google/docs/skills).** Agentic IDE and workspace environment supported by the `secops-setup-antigravity` setup skill and `.agent` skill definitions in this repository.
- **[Goose](https://goose-docs.ai/).** Open-source local developer agent with native `stdio` and Streamable HTTP MCP client support (`https://goose-docs.ai/`).
