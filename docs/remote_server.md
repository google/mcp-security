# Remote MCP Server for Google SecOps

The **Remote MCP server for Google SecOps** simplifies the setup and usage of MCP by providing a fully-managed service. Instead of managing a local Python environment, you can point your AI agents or MCP clients to a globally-consistent and enterprise-ready endpoint.

This remote server inherits the rigorous scalability, security, and observability standards of the Google Cloud ecosystem.

## Onboarding

### Authentication and Authorization

The remote server uses [Application Default Credentials (ADC)](https://docs.cloud.google.com/mcp/authenticate-mcp#user-credentials-adc-mcp-servers).

1.  **Set up ADC**: Follow the guide to [Set up Application Default Credentials](https://docs.cloud.google.com/docs/authentication/provide-credentials-adc).
2.  **Authenticate**: Detailed instructions are in [Authenticate to Google and Google Cloud MCP servers](https://docs.cloud.google.com/mcp/authenticate-mcp).
3.  **Roles**: The caller requires the `roles/mcp.toolUser` and `roles/serviceusage.serviceUsageConsumer` roles on the billing/quota project, plus an appropriate Chronicle data role (such as `roles/chronicle.viewer`, `roles/chronicle.editor`, or `roles/chronicle.soarAdmin` when calling SOAR tools). Administrators granting MCP access need `roles/serviceusage.serviceUsageAdmin`.

For production, see [Agent identity](https://docs.cloud.google.com/mcp/authenticate-mcp#agent-identity) recommendations in [Manage MCP servers](https://docs.cloud.google.com/mcp/manage-mcp-servers).

### Enable the Service

You must enable the MCP service in your Google Cloud project.

```bash
PROJECT_ID=<your-gcp-project-id>
gcloud components install beta
gcloud beta services mcp enable chronicle.googleapis.com/mcp --project=$PROJECT_ID
```

See [Supported Products](https://docs.cloud.google.com/mcp/supported-products) and the [Enablement Guide](https://docs.cloud.google.com/mcp/configure-mcp-ai-application#enable-remote-mcp-server) for more details.

### Environment Configuration

Remote MCP servers require specific environment context for every request. It is recommended to include these in a context file (e.g., `GEMINI.md` or system prompt) for your LLM:

```text
When using the remote-mcp-secops MCP Server, use these parameters for EVERY request:
Customer ID: <UUIDv4 for your tenant>
Region: <your-region>
Project ID: <your-gcp-project-id>
```

### SOAR API Migration

The hosted MCP server uses the **Chronicle REST APIs** (OneMCP) instead of the legacy SOAR APIs.
*   **SIEM tools**: Available immediately without migration.
*   **SOAR tools**: Require migration to Chronicle API. See [SOAR migration overview](https://docs.cloud.google.com/chronicle/docs/soar/admin-tasks/advanced/migrate-to-gcp).

## Governance

### Model Armor
Optional protection to sanitize MCP tool calls and responses, mitigating prompt injection and sensitive data leakage.
*   [Model Armor for MCP guide](https://docs.cloud.google.com/model-armor/model-armor-mcp-google-cloud-integration)

### Cloud Armor
Protect the endpoint itself using DDoS protection and WAF capabilities (IP allowlists, geo-blocking).
*   [Cloud Armor integration](https://docs.cloud.google.com/chronicle/docs/soar/marketplace-integrations/google-cloud-armor)

### IAM
Access is managed via standard Google Cloud IAM.
*   Identity requires: `roles/mcp.toolUser`, `roles/serviceusage.serviceUsageConsumer`, and a Chronicle data role (such as `roles/chronicle.viewer`)
*   The server respects existing granular entitlements assigned to the identity via the Chronicle REST API.
*   [MCP Access Control](https://docs.cloud.google.com/mcp/access-control)

### Organization Policy
Restrict MCP usage across your organization. For example, to allow *only* the SecOps MCP server:

```json
{
  "name": "organizations/$ORG_ID/policies/gcp.managed.allowedMCPServices",
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
*   [Control MCP use in your organization](https://docs.cloud.google.com/mcp/control-mcp-use-organization)

### Observability
All administrative and access activities are recorded in Cloud Audit Logs.
*   [MCP Audit Logging](https://docs.cloud.google.com/mcp/audit-logging)

## Client Configuration

The remote server can be used with any MCP-compatible client. Since JSON configuration for MCP is not yet fully standardized across all clients, here are examples for common tools.

The examples below connect to the US multi-region endpoint (`https://chronicle.us.rep.googleapis.com/mcp`). For non-US Google SecOps tenants, substitute your tenant's regional endpoint (`https://<region>-chronicle.googleapis.com/mcp`, such as `https://europe-chronicle.googleapis.com/mcp` or `https://europe-west2-chronicle.googleapis.com/mcp`) so the URL matches your tenant `region`.

### Automated Setup

For **Gemini CLI** and **Antigravity**, you can use the automated setup skills provided in the [Google SecOps Extension](./google_secops_extension.md):
*   **Gemini CLI**: Use the `secops-setup-gemini-cli` skill.
*   **Antigravity**: Use the `secops-setup-antigravity` skill.

### Gemini CLI

Using the `google_credentials` auth provider (native support):

```json
{
 "mcpServers": {
   "remote-mcp-secops": {
     "httpUrl": "https://chronicle.us.rep.googleapis.com/mcp",
     "authProviderType": "google_credentials",
     "oauth": {
       "scopes": ["https://www.googleapis.com/auth/cloud-platform"]
     },
     "timeout": 60000,
     "headers": {
       "x-goog-user-project": "<YOUR_PROJECT_ID>"
     }
   }
 }
}
```

*   [Gemini CLI Configuration Guide](https://docs.cloud.google.com/mcp/configure-mcp-ai-application#gemini-cli)

### Testing with cURL

You can verify access directly without an MCP client:

```bash
curl --location 'https://chronicle.us.rep.googleapis.com/mcp' \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -H 'x-goog-user-project: <YOUR_PROJECT_ID>' \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "list_rules",
      "arguments": {
        "project_id": "<YOUR_PROJECT_ID>",
        "customer_id": "<YOUR_CUSTOMER_ID>",
        "region": "<YOUR_REGION>"
      }
    },
    "jsonrpc": "2.0",
    "id": 1
  }' -s
```

### Agent Development Kit (ADK)

Example Python configuration using `google-adk`. Use the `cloud-platform` OAuth scope so user credentials created with `gcloud auth application-default login` refresh cleanly without `invalid_scope` errors, omit custom `Accept` header overrides so the MCP SDK sends `Accept: application/json, text/event-stream`, and inject credentials via an `httpx.Auth` client factory (`create_mcp_http_client`) so both `adk web` discovery (`readonly_context=None`) and long-running tool calls refresh expired tokens off the event loop over a single pooled MCP session (or set `SECOPS_MCP_URL` in `run-with-google-adk/.env`):

```python
import asyncio
import threading
import google.auth
from google.auth.transport.requests import Request
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import create_mcp_http_client
import httpx

PROJECT_ID = "<YOUR_PROJECT_ID>"
SECOPS_MCP_URL = "https://chronicle.us.rep.googleapis.com/mcp"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def _origin(url: str | httpx.URL) -> tuple[str, str, int | None]:
    hx = httpx.URL(url) if isinstance(url, str) else url
    return (hx.scheme.lower(), (hx.host or "").lower(), hx.port)


class SecOpsGoogleAuth(httpx.Auth):
    def __init__(self, target_url: str, quota_project: str | None = None) -> None:
        self._origin = _origin(target_url)
        self._quota_project = quota_project
        self._creds = None
        self._lock = threading.Lock()

    def _get_auth_sync(self, *, force_refresh: bool = False) -> tuple[str, str | None]:
        with self._lock:
            if self._creds is None:
                self._creds, _ = google.auth.default(scopes=SCOPES)
            if force_refresh or not self._creds.valid or self._creds.expired or not self._creds.token:
                self._creds.refresh(Request())
            quota = self._quota_project or getattr(self._creds, "quota_project_id", None)
            return str(self._creds.token), quota

    async def async_auth_flow(self, request: httpx.Request):
        if _origin(request.url) != self._origin:
            yield request
            return
        token, quota = await asyncio.to_thread(self._get_auth_sync)
        request.headers["Authorization"] = f"Bearer {token}"
        if quota:
            request.headers["x-goog-user-project"] = quota
        response = yield request
        if response.status_code == 401:
            token, quota = await asyncio.to_thread(self._get_auth_sync, force_refresh=True)
            request.headers["Authorization"] = f"Bearer {token}"
            if quota:
                request.headers["x-goog-user-project"] = quota
            yield request


def _secops_client_factory(headers=None, timeout=None, auth=None) -> httpx.AsyncClient:
    client = create_mcp_http_client(
        headers=headers,
        timeout=timeout,
        auth=auth or SecOpsGoogleAuth(SECOPS_MCP_URL, PROJECT_ID),
    )
    client.follow_redirects = False
    return client


toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=SECOPS_MCP_URL,
        timeout=60.0,
        sse_read_timeout=300.0,
        httpx_client_factory=_secops_client_factory,
    ),
)
```

## Available Tools

The remote MCP server exposes a strategic subset of Chronicle REST API methods as MCP tools. The list is extensive and includes tools for:
*   SIEM (Search, Rules, Alerts, Feeds)
*   SOAR (Cases, Playbooks, Connectors) - *requires API migration*

Use the `list_tools` MCP method or your client's discovery command (e.g., `/mcp desc` in Gemini CLI) to see the full list dynamically.
