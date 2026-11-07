# Remote MCP server for Google SecOps

The remote MCP server for Google Security Operations provides a Google-managed Streamable HTTP MCP endpoint backed by the Chronicle REST API. Instead of managing a local Python runtime, you point your MCP client or agent framework to the regional Google Cloud endpoint and authenticate with Application Default Credentials (ADC) and IAM.

## Endpoints

Use the locational endpoint (`<region>-chronicle.googleapis.com`) matching your Google SecOps tenant region, or the multi-regional endpoint where applicable:

| Region | Endpoint URL |
| :--- | :--- |
| United States (locational) | `https://us-chronicle.googleapis.com/mcp` |
| United States (multi-regional) | `https://chronicle.us.rep.googleapis.com/mcp` |
| Europe (locational) | `https://eu-chronicle.googleapis.com/mcp` |
| Single GCP region (for example, `europe-west2`, `asia-southeast1`) | `https://<region>-chronicle.googleapis.com/mcp` |

## Onboarding

### 1. Authenticate and grant IAM roles

The remote server authenticates callers with Google Cloud [Application Default Credentials (ADC)](https://docs.cloud.google.com/mcp/authenticate-mcp#user-credentials-adc-mcp-servers).

1. **Authenticate locally**: Sign in and update ADC, then set your quota project:
   ```bash
   ACCOUNT="analyst@example.com"
   PROJECT_ID="your-project-id"
   gcloud auth login "$ACCOUNT" --update-adc
   gcloud config set project "$PROJECT_ID"
   gcloud auth application-default set-quota-project "$PROJECT_ID"
   ```
   For unattended or production workloads, attach a dedicated Google Cloud service account rather than a human user credential. See [Authenticate to Google Cloud MCP servers](https://docs.cloud.google.com/mcp/authenticate-mcp#agent-identity).

2. **Grant required IAM roles** on your Google Cloud project:
   - **MCP Tool User** (`roles/mcp.toolUser`) to invoke `/mcp` tools (`mcp.tools.call`).
   - **Service Usage Consumer** (`roles/serviceusage.serviceUsageConsumer`) to validate the `x-goog-user-project` quota header.
   - **Chronicle data role** such as **Chronicle API Viewer** (`roles/chronicle.viewer`), **Chronicle API Editor** (`roles/chronicle.editor`), or **Chronicle API Admin** (`roles/chronicle.admin`). The remote MCP server enforces the caller's granular Chronicle IAM permissions on every API call.

### 2. Enable the remote MCP service

Enable `chronicle.googleapis.com/mcp` on the Google Cloud project bound to your Google SecOps tenant (requires `roles/serviceusage.serviceUsageAdmin`):

```bash
PROJECT_ID="your-project-id"
gcloud components install beta
gcloud beta services mcp enable chronicle.googleapis.com/mcp --project="$PROJECT_ID"
```

For organization-wide enablement details, see [Supported Google Cloud MCP products](https://docs.cloud.google.com/mcp/supported-products) and [Enable a remote MCP server](https://docs.cloud.google.com/mcp/configure-mcp-ai-application#enable-remote-mcp-server).

### 3. Provide tenant parameters in agent instructions

Nearly every tool on the remote MCP server requires `projectId`, `customerId`, and `region` to bind the target Google SecOps resource path (`projects/{projectId}/locations/{region}/instances/{customerId}`). Add your tenant identifiers to your agent's persistent rules or `GEMINI.md` file so the model passes them on every call:

```text
When calling tools on the Google SecOps remote MCP server, pass these tenant parameters on every tool call:
- projectId: your-project-id
- customerId: a1b2c3d4-e5f6-4321-abcd-ef1234567890
- region: us
```

### SOAR API migration status

The remote MCP server calls native Chronicle REST APIs:

- **SIEM tools** (UDM search, YARA-L 2.0 rules, curated rules, alerts, entity summaries, data tables, reference lists, feeds, parsers, and investigations) work immediately on all Google SecOps SIEM tenants.
- **SOAR tools** (cases, case alerts, playbooks, and integration actions) require your tenant to complete SOAR migration to the Chronicle API. See [Migrate Google SecOps SOAR to Google Cloud](https://docs.cloud.google.com/chronicle/docs/soar/admin-tasks/advanced/migrate-to-gcp). Tenants that have not completed migration can continue using the local [Google SecOps SOAR MCP server](servers/secops_soar_mcp.md) against `SOAR_URL`.

## Governance and security controls

- **IAM access control**: Access is governed by Google Cloud IAM (`roles/mcp.toolUser` plus Chronicle roles). See [MCP access control](https://docs.cloud.google.com/mcp/access-control).
- **Model Armor**: Sanitize MCP tool inputs and responses to mitigate prompt injection and sensitive data exposure. See [Model Armor for Google Cloud MCP](https://docs.cloud.google.com/model-armor/model-armor-mcp-google-cloud-integration).
- **Organization policies**: Restrict allowed MCP services across your Google Cloud organization with `gcp.managed.allowedMCPServices`:
  ```json
  {
    "name": "organizations/YOUR_ORG_ID/policies/gcp.managed.allowedMCPServices",
    "spec": {
      "rules": [
        {
          "enforce": true,
          "parameters": {
            "allowedServices": [
              "chronicle.googleapis.com/mcp"
            ]
          }
        }
      ]
    }
  }
  ```
  See [Control MCP use in your organization](https://docs.cloud.google.com/mcp/control-mcp-use-organization).
- **Cloud Audit Logs**: All administrative operations and MCP tool calls are recorded in Cloud Audit Logs. See [MCP audit logging](https://docs.cloud.google.com/mcp/audit-logging).

## Client configuration

### Automated setup with skills

For **Gemini CLI** and **Antigravity**, the [Google SecOps extension](google_secops_extension.md) includes interactive setup skills (`secops-setup-gemini` and `secops-setup-antigravity`) that verify ADC and write the configuration for you.

### Gemini CLI

Add `secops-hosted-mcp` to `~/.gemini/settings.json` using the built-in `google_credentials` auth provider:

```json
{
  "mcpServers": {
    "secops-hosted-mcp": {
      "httpUrl": "https://us-chronicle.googleapis.com/mcp",
      "authProviderType": "google_credentials",
      "oauth": {
        "scopes": ["https://www.googleapis.com/auth/cloud-platform"]
      },
      "timeout": 30000,
      "headers": {
        "x-goog-user-project": "your-project-id"
      },
      "excludeTools": [
        "create_feed",
        "update_feed",
        "run_parser",
        "list_feeds",
        "get_feed",
        "disable_feed",
        "enable_feed"
      ]
    }
  }
}
```

### Antigravity

Add `secops` to `~/.gemini/antigravity/mcp_config.json`:

```json
{
  "mcpServers": {
    "secops": {
      "serverUrl": "https://us-chronicle.googleapis.com/mcp",
      "authProviderType": "google_credentials",
      "headers": {
        "x-goog-user-project": "your-project-id"
      },
      "disabledTools": [
        "create_feed",
        "update_feed",
        "run_parser",
        "list_feeds",
        "get_feed",
        "disable_feed",
        "enable_feed"
      ]
    }
  }
}
```

> **Schema token tip:** Excluding the seven feed and parser administration tools (`create_feed`, `update_feed`, `run_parser`, `list_feeds`, `get_feed`, `disable_feed`, and `enable_feed`) when you are not administering log feeds reduces the remote server's eager JSON `inputSchema` payload by roughly 69% (`~42,000` tokens per session). Remove that filter whenever you need feed or parser administration tools.

### Goose

In [Goose](https://goose-docs.ai/) (`~/.config/goose/config.yaml`), configure a `streamable_http` extension and pass your bearer token and quota project header:

```yaml
extensions:
  secops-remote:
    name: Google SecOps Remote MCP
    type: streamable_http
    enabled: true
    uri: https://us-chronicle.googleapis.com/mcp
    headers:
      Authorization: "Bearer ${GCP_ACCESS_TOKEN}"
      x-goog-user-project: "your-project-id"
```

### Verify connectivity with cURL

Test your credentials and IAM bindings directly from a terminal before wiring an MCP client:

```bash
PROJECT_ID="your-project-id"
CUSTOMER_ID="a1b2c3d4-e5f6-4321-abcd-ef1234567890"
REGION="us"
ENDPOINT_URL="https://${REGION}-chronicle.googleapis.com/mcp"
ACCESS_TOKEN="$(gcloud auth application-default print-access-token)"

curl --silent --show-error --location "$ENDPOINT_URL" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-goog-user-project: $PROJECT_ID" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"list_rules\",
      \"arguments\": {
        \"projectId\": \"$PROJECT_ID\",
        \"customerId\": \"$CUSTOMER_ID\",
        \"region\": \"$REGION\"
      }
    }
  }"
```

### Google Agent Development Kit (ADK)

Connect a Python ADK agent to the remote MCP endpoint with `McpToolset` and `StreamableHTTPConnectionParams`:

```python
import google.auth
from google.auth.transport.requests import Request
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

PROJECT_ID = "your-project-id"
REGION = "us"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
FEED_ADMIN_TOOLS = {
    "create_feed",
    "update_feed",
    "run_parser",
    "list_feeds",
    "get_feed",
    "disable_feed",
    "enable_feed",
}


def get_access_token() -> str:
    creds, _ = google.auth.default(scopes=SCOPES)
    creds.refresh(Request())
    return creds.token


toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=f"https://{REGION}-chronicle.googleapis.com/mcp",
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Accept": "application/json, text/event-stream",
            "x-goog-user-project": PROJECT_ID,
        },
    ),
    tool_filter=lambda tool, ctx=None: tool.name not in FEED_ADMIN_TOOLS,
)
```

## Available tools

The remote MCP server exposes over 70 tools mapped from the Chronicle REST API across:

- **SIEM**: Natural-language-to-UDM query translation (`translate_udm_query`), UDM event search (`udm_search`), entity summaries (`summarize_entity`), IOC matches (`get_ioc_match`), SIEM alerts, YARA-L 2.0 detection rules, retrohunts, curated rules, data tables, reference lists, feeds, parsers, and Gemini investigations.
- **SOAR** (on migrated tenants): Cases (`list_cases`, `get_case`, `update_case`, `create_case_comment`, `execute_bulk_close_case`), case alerts (`list_case_alerts`), connector events, involved entities, playbooks, and integration actions.

Call `tools/list` (or run `/mcp desc` in Gemini CLI) to inspect the live schema for every tool available to your tenant.
