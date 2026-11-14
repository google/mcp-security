# Remote MCP Server for Google Threat Intelligence

The Google Threat Intelligence (GTI) Agentic Model Context Protocol (MCP) server provides a Google-managed stateless Streamable HTTP endpoint at `https://www.virustotal.com/api/v3/agentspace/mcp/`. Instead of installing a local Python runtime, you connect your MCP client directly to the [Google Threat Intelligence Agentic platform](https://gtidocs.virustotal.com/docs/agentic-platform) with your Google Threat Intelligence API key.

When you call `ask_gti_agent` or `continue_chat`, server-side specialist threat intelligence and malware analysis agents run multi-step pivots across file reports, sandbox behavior traces, threat actors, malware families, campaigns, vulnerabilities, and indicator relationships. Each tool call returns a synthesized Markdown assessment, entity citations, and a `session_id` rather than multi-megabyte VirusTotal API v3 JSON payloads.

## Choose between the GTI and VirusTotal MCP servers

You can connect to a managed remote endpoint or run the open-source Python server locally, and you can register multiple servers side by side in one MCP client under distinct server keys such as `gti-agentic`, `virustotal`, and `gti`.

![Architecture diagram comparing an MCP client connected to three options: Remote GTI Agentic MCP over stateless Streamable HTTP with an x-apikey header for 7 specialist-agent session tools, VirusTotal AI Hosted MCP at ai.virustotal.com/mcp over Streamable HTTP with browser OAuth 2.1 for 11 direct report and scan tools, and the local gti-mcp stdio Python server using VT_APIKEY for 35+ direct VirusTotal API v3 tools.](img/gti_remote/gti_remote_vs_local.svg)

| Capability | Remote GTI Agentic (`gti-agentic`) | VirusTotal AI Hosted (`virustotal`) | Local `gti-mcp` (`gti`) |
| :--- | :--- | :--- | :--- |
| Endpoint or package | `www.virustotal.com/api/v3/agentspace/mcp/` (HTTPS) | `ai.virustotal.com/mcp` (HTTPS) | `uvx gti_mcp` (`gti-mcp` on PyPI) |
| Transport | Stateless Streamable HTTP (`POST` and SSE, trailing `/` required) | Streamable HTTP | Local `stdio` Python process |
| Authentication | `x-apikey` HTTP header (`VT_APIKEY`) | Browser OAuth 2.1 sign-in (no static API key) | `VT_APIKEY` environment variable |
| Account requirement | Google Threat Intelligence Enterprise, Enterprise Plus, or active Proof-of-Concept (PoC) license (no separate allowlist group required) | VirusTotal account via Google OAuth (free-tier quota: 60 queries per minute, 1,000 per UTC day; unknown-file uploads: 20 per minute, 500 per UTC day) | VirusTotal or Google Threat Intelligence API v3 key |
| Tool catalog | 7 session tools (`ask_gti_agent`, `continue_chat`, `list_sessions`, `get_session_history`, `delete_session`, `share_session`, `copy_shared_session`) | 11 hosted tools (`get_file_report`, `get_url_report`, `get_domain_report`, `get_ip_report`, `submit_file`, `submit_attachment`, `submit_url`, `reanalyze_domain`, `reanalyze_ip`, `get_submission`, `get_analysis`) | 35+ direct API v3 tools across Threat Collections, MITRE ATT&CK trees, Digital Threat Monitoring (DTM), standard YARA rulesets, Threat Profiles, and Indicator of Compromise (IoC) relationship graphs |
| Response format | Synthesized Markdown briefs, entity citations, and `session_id` | Structured indicator reports and scan receipts | Structured API v3 JSON objects and relationships |
| Best fit | Zero-install multi-turn threat hunting, attribution briefs, malware triage, and analyst session handoffs | Quick zero-key indicator lookups and submissions in OAuth-capable clients | Deterministic collection edits, DTM queries, standard YARA file ruleset retrieval, Threat Profile lookups, and custom Python automation |

For local `gti-mcp` installation and tool reference, see the [Google Threat Intelligence MCP server guide](servers/gti_mcp.md). For OAuth 2.1 direct report lookups without a static API key, see the **Alternative: VirusTotal AI Hosted MCP** section below and the [VirusTotal AI MCP installation guide](https://ai.virustotal.com/install.md).

## Onboarding and requirements

Verify four requirements before connecting an MCP client to `gti-agentic`:

1. **Google Threat Intelligence Enterprise, Enterprise Plus, or active PoC entitlement.** Access to the Agentic platform and its remote MCP endpoint requires an Enterprise, Enterprise Plus, or active PoC entitlement. Standard free VirusTotal API keys return an authorization error on `/api/v3/agentspace/*` routes. Accounts with an active Enterprise, Enterprise Plus, or PoC license do not require any separate MCP allowlist request or special group membership.
2. **Google Threat Intelligence API key.** Sign in to [VirusTotal](https://www.virustotal.com), click your profile avatar in the upper-right corner, and select **API Key** (`https://www.virustotal.com/gui/my-apikey`) to copy your personal key. See [How to get GTI API keys](https://gtidocs.virustotal.com/docs/how-get-gti-api-keys) for key management details.
3. **Secret storage.** Every request sent with your API key authenticates as your account and draws from your organization's quota. Export the key as an environment variable such as `VT_APIKEY` instead of committing plaintext credentials to repository files.
4. **Data handling and session sharing.** Google governs GTI Agentic prompts and outputs as tenant-isolated Customer Data under the [Google Cloud Service Specific Terms](https://cloud.google.com/terms/service-terms) and the [Google SecOps Privacy Notice](https://cloud.google.com/terms/secops/privacy-notice). Google does not review Customer Data with human reviewers, share it across customers, or use it to train foundation models, and files submitted within Agentic sessions use Private Scanning. Still, omit unnecessary personal data and raw credentials from prompts. Treat `share_session` output as sensitive: `share_session` generates a bearer `share_token` that allows another authenticated user to clone the full session history via `copy_shared_session`.

## Endpoint and transport requirements

Configure Streamable HTTP clients with these connection settings:

- **Server URL.** `https://www.virustotal.com/api/v3/agentspace/mcp/`
- **Authentication header.** `x-apikey: <YOUR_GTI_API_KEY>`
- **Transport.** Stateless Streamable HTTP using JSON-RPC 2.0 `POST` requests

The HTTP transport itself is stateless: the server neither issues nor requires an `Mcp-Session-Id` HTTP header, and each JSON-RPC `POST` authenticates independently through `x-apikey`. The server maintains investigation continuity across turns at the application layer through the `session_id` tool parameter returned by `ask_gti_agent` and passed to `continue_chat` or `get_session_history`.

Pay attention to three protocol behaviors when configuring MCP clients or custom HTTP transports:

- **Keep the trailing slash in the endpoint URL.** Sending a `POST` request to `https://www.virustotal.com/api/v3/agentspace/mcp` without the trailing `/` returns `HTTP 401` when unauthenticated and a cross-scheme `HTTP 307` redirect (`Location: http://www.virustotal.com/api/v3/agentspace/mcp/`) when authenticated. HTTP clients strip `x-apikey` across that `https` to `http` downgrade and fail with `HTTP 401`, so include the trailing `/` instead of forwarding headers across redirects.
- **Accept both JSON and event streams.** Requests must send `Accept: application/json, text/event-stream`. Standard MCP SDK transports send both media types automatically, whereas custom HTTP callers that send only `application/json` or only `text/event-stream` fail with `HTTP 406 Not Acceptable`.
- **Raise the client request timeout.** Multi-step investigations with `ask_gti_agent` and `continue_chat` typically run for 45 to 180 seconds while server-side specialist agents pivot across threat intelligence telemetry. Configure a 300-second timeout (300000 milliseconds) so complex investigations do not abort at a 30-second or 60-second client default.

## Client configuration

Prompt interactively for your API key in your shell so the secret never enters `~/.bash_history` or `~/.zsh_history` and remains available to clients that interpolate environment variables:

```bash
read -rsp "GTI API Key: " VT_APIKEY && echo && export VT_APIKEY
```

### Cursor

Add `gti-agentic` to `~/.cursor/mcp.json` (user scope) or `.cursor/mcp.json` (workspace scope) using Cursor's `${env:VT_APIKEY}` interpolation syntax:

```json
{
  "mcpServers": {
    "gti-agentic": {
      "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
      "headers": {
        "x-apikey": "${env:VT_APIKEY}"
      }
    }
  }
}
```

### VS Code

Configure `.vscode/mcp.json` with VS Code's native `inputs` and `servers` schema so VS Code prompts for your API key as a masked password input rather than storing it on disk:

```json
{
  "inputs": [
    {
      "id": "gtiApiKey",
      "type": "promptString",
      "description": "Google Threat Intelligence API key",
      "password": true
    }
  ],
  "servers": {
    "gti-agentic": {
      "type": "http",
      "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
      "headers": {
        "x-apikey": "${input:gtiApiKey}"
      }
    }
  }
}
```

### Cline

Add `gti-agentic` to `cline_mcp_settings.json` with `"type": "streamableHttp"` and a 300-second timeout. Because Cline stores the literal header value in `cline_mcp_settings.json`, restrict file permissions with `chmod 600` on that file:

```json
{
  "mcpServers": {
    "gti-agentic": {
      "type": "streamableHttp",
      "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
      "timeout": 300,
      "headers": {
        "x-apikey": "<YOUR_GTI_API_KEY>"
      }
    }
  }
}
```

### Gemini CLI

[Gemini CLI](https://geminicli.com) runs an environment sanitizer (`NEVER_ALLOWED_NAME_PATTERNS`) that strips environment variables matching `/KEY/i` (including `$VT_APIKEY`) to an empty string when expanding MCP `headers`, unless the variable name starts with `GEMINI_CLI_`. Export `GEMINI_CLI_VT_APIKEY` from your existing `VT_APIKEY` variable before starting `gemini`:

```bash
export GEMINI_CLI_VT_APIKEY="$VT_APIKEY"
```

Then configure `gti-agentic` in `~/.gemini/settings.json` with `"type": "http"` and `"url"` (older Gemini CLI releases without `"type": "http"` used `"httpUrl"` in place of `"type"` and `"url"`):

```json
{
  "mcpServers": {
    "gti-agentic": {
      "type": "http",
      "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
      "timeout": 300000,
      "headers": {
        "x-apikey": "$GEMINI_CLI_VT_APIKEY"
      }
    }
  }
}
```

### Antigravity

Add `gti-agentic` to `~/.gemini/config/mcp_config.json` (or `~/.gemini/antigravity/mcp_config.json` on older IDE builds) with `serverUrl` and `timeoutSeconds`. Because user `mcp_config.json` does not expand shell environment variables, restrict file permissions with `chmod 600 ~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "gti-agentic": {
      "serverUrl": "https://www.virustotal.com/api/v3/agentspace/mcp/",
      "timeoutSeconds": 300,
      "headers": {
        "x-apikey": "<YOUR_GTI_API_KEY>"
      }
    }
  }
}
```

### Claude Code

Export `MCP_TOOL_TIMEOUT=300000` and register the Streamable HTTP server with single-quoted `--header 'x-apikey: ${VT_APIKEY}'` so your parent shell does not expand `$VT_APIKEY` into process arguments (`ps`) or write the plaintext key into `~/.claude.json`:

```bash
export MCP_TOOL_TIMEOUT=300000
ENDPOINT_URL="https://www.virustotal.com/api/v3/agentspace/mcp/"

claude mcp add --transport http gti-agentic "$ENDPOINT_URL" \
  --header 'x-apikey: ${VT_APIKEY}'
```

You can also declare `gti-agentic` directly in `~/.claude.json` or a project `.mcp.json` file with `"type": "http"`:

```json
{
  "mcpServers": {
    "gti-agentic": {
      "type": "http",
      "url": "https://www.virustotal.com/api/v3/agentspace/mcp/",
      "headers": {
        "x-apikey": "${VT_APIKEY}"
      }
    }
  }
}
```

### Claude Desktop

For `claude_desktop_config.json` builds that require a `stdio` bridge when passing custom HTTP headers, run `mcp-remote` with `npx`. Keep `"x-apikey:${VT_APIKEY}"` without a space after `:` to prevent Windows `npx` argument splitting, and protect `claude_desktop_config.json` with `chmod 600` (or pass `mcp-remote`'s `--header-file` flag pointing to a mode 0600 file). Note that `mcp-remote` enforces a 60-second SDK request timeout; if a long `ask_gti_agent` investigation exceeds 60 seconds, call `list_sessions` and `get_session_history` to retrieve the completed response:

```json
{
  "mcpServers": {
    "gti-agentic": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://www.virustotal.com/api/v3/agentspace/mcp/",
        "--header",
        "x-apikey:${VT_APIKEY}"
      ],
      "env": {
        "VT_APIKEY": "<YOUR_GTI_API_KEY>"
      }
    }
  }
}
```

### Codex CLI

Add `gti-agentic` to `~/.codex/config.toml` so Codex CLI reads `VT_APIKEY` from your environment and allows 300 seconds per tool call:

```toml
[mcp_servers.gti-agentic]
url = "https://www.virustotal.com/api/v3/agentspace/mcp/"
env_http_headers = { "x-apikey" = "VT_APIKEY" }
tool_timeout_sec = 300
```

### Goose

In [Goose](https://goose-docs.ai/), from the [aaif-goose/goose](https://github.com/aaif-goose/goose) project, add a `streamable_http` extension to `~/.config/goose/config.yaml`. Goose expands `${VT_APIKEY}` inside `headers` only when you list `VT_APIKEY` under `env_keys` and export `VT_APIKEY` before launching the `goose` CLI (or store it in Goose's keyring for Goose Desktop):

```yaml
extensions:
  gti-agentic:
    name: Google Threat Intelligence Agentic MCP
    type: streamable_http
    enabled: true
    uri: https://www.virustotal.com/api/v3/agentspace/mcp/
    timeout: 300
    env_keys:
      - VT_APIKEY
    headers:
      x-apikey: "${VT_APIKEY}"
```

### Verify connectivity with cURL

Test your API key and entitlement from a terminal before launching an MCP client. Pass the header via `curl --config -` on standard input so `$VT_APIKEY` never appears in process arguments (`ps` or `/proc/<pid>/cmdline`):

```bash
ENDPOINT_URL="https://www.virustotal.com/api/v3/agentspace/mcp/"

printf 'header = "x-apikey: %s"\n' "$VT_APIKEY" | \
  curl --silent --show-error --config - -X POST "$ENDPOINT_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "tools/list",
      "params": {}
    }'
```

An entitled Enterprise, Enterprise Plus, or active PoC key returns HTTP 200 with an `event: message` JSON-RPC response listing all 7 tools.

### Google Agent Development Kit in Python

Connect a Python [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) agent to the remote endpoint with `McpToolset` and `StreamableHTTPConnectionParams`. Omit custom `Accept` overrides from `headers` so the MCP SDK preserves `Accept: application/json, text/event-stream`:

```python
import os
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

VT_APIKEY = os.environ["VT_APIKEY"]
GTI_AGENTIC_MCP_URL = "https://www.virustotal.com/api/v3/agentspace/mcp/"

gti_agentic_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=GTI_AGENTIC_MCP_URL,
        headers={
            "x-apikey": VT_APIKEY,
        },
        timeout=300.0,
        sse_read_timeout=300.0,
    ),
)
```

## Available tools

The remote server exposes 7 tools backed by the stateful [Google Threat Intelligence Agentic platform](https://gtidocs.virustotal.com/docs/agentic-platform):

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `ask_gti_agent` | `message` required | Starts a new natural-language investigation across IoCs, threat actors, malware families, vulnerabilities, and campaigns. Returns the synthesized analysis and a new `session_id`. |
| `continue_chat` | `session_id` required, `message` required | Sends a follow-up question in an existing `session_id` so the agent retains prior findings and citations. |
| `list_sessions` | `limit` optional, default 5 | Lists recent and active investigation sessions owned by the authenticated API key. |
| `get_session_history` | `session_id` required | Retrieves the message and event history recorded for an investigation session. |
| `delete_session` | `session_id` required | Permanently deletes a finished or temporary investigation session. |
| `share_session` | `session_id` required | Generates a `share_token` so another analyst can copy and continue the investigation session. |
| `copy_shared_session` | `share_token` required | Copies a shared session into the caller's workspace under a new `session_id` without modifying the original session. |

## Multi-turn workflow examples

`ask_gti_agent` opens an investigation session and returns a `session_id` such as `a1b2c3d4-e5f6-4321-abcd-ef1234567890`. Your MCP client passes that `session_id` to `continue_chat` on subsequent turns:

1. **IoC reputation and threat actor attribution.**
   - Turn 1 with `ask_gti_agent`: *"What is the current reputation, behavioral summary, and known threat actor attribution for SHA-256 `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c`?"*
   - Turn 2 with `continue_chat`: *"List network indicators and mutexes observed in those sandbox runs so I can hunt for them in Google SecOps Unified Data Model (UDM) events."*
2. **Recent high-detection sample triage.**
   - Turn 1 with `ask_gti_agent`: *"Triage the highest-detection samples associated with malware family RedLine submitted over the past 7 days."*
   - Turn 2 with `continue_chat`: *"Summarize recurring execution patterns from those samples, separating file and payload traits suited for standard YARA rules from host process telemetry suited for Chronicle YARA-L 2.0 UDM detection rules."*
3. **Threat actor briefings and analyst handoffs.**
   - Turn 1 with `ask_gti_agent`: *"Compile a threat brief on APT44 activity, targeted sectors, and exploited CVEs from the past 90 days."*
   - Handoff with `share_session` and `copy_shared_session`: Generate a `share_token` from the active `session_id` and record it in your incident ticket so a teammate can clone the session into their own workspace and continue investigating independently.

## Alternative: VirusTotal AI Hosted MCP (OAuth 2.1, direct report tools)

If you do not have a Google Threat Intelligence Enterprise, Enterprise Plus, or active PoC license, prefer browser OAuth 2.1 over managing a static `VT_APIKEY`, or want direct single-indicator lookup tools (`get_ip_report`, `get_file_report`, `get_domain_report`, `get_url_report`) without installing Python locally, connect to the **VirusTotal AI Hosted MCP** server at `https://ai.virustotal.com/mcp`.

- **Authentication.** Browser sign-in with Google OAuth 2.1. Remove manual `Authorization` or `x-apikey` headers from the server entry when using OAuth. You can review or revoke active OAuth sessions at [VirusTotal OAuth connections](https://ai.virustotal.com/oauth/connections).
- **Direct lookup and submission tools (11 hosted tools).** Exposes `get_file_report`, `get_url_report`, `get_domain_report`, `get_ip_report`, `submit_file`, `submit_attachment`, `submit_url`, `reanalyze_domain`, `reanalyze_ip`, `get_submission`, and `get_analysis`.
- **Rate limits and upload quotas.** Free-tier access allows 60 queries per minute and 1,000 queries per UTC day (cached and missing-report reads still consume query quota), with a separate unknown-file upload quota of 20 per minute and 500 per UTC day.
- **Submission data-sharing and URL-lookup privacy.** Standard VirusTotal uploads and URL submissions (`submit_file`, `submit_attachment`, `submit_url`, `reanalyze_domain`, `reanalyze_ip`) share submitted content with the security community and are not confidential. Use report lookup tools (`get_file_report`, `get_domain_report`, `get_ip_report`, `get_url_report`) by default, and submit files or URLs only when you explicitly intend to share them publicly. Calling `get_url_report` discloses the complete URL, including query parameters and `#fragment` values, to VTAI and VirusTotal; prefer `get_domain_report` when URLs may contain tokens, session IDs, or personal data.

### Quick client setup for `ai.virustotal.com/mcp`

- **Antigravity (`agy`).** Install the official partner plugin, start a new session, open `/mcp`, select the namespaced plugin server `virustotal_virustotal`, choose **Authenticate**, and paste any browser callback authorization code into the `/mcp` terminal dialog (never into chat):
  ```bash
  agy plugin install virustotal@antigravity-plugins-partners
  ```
- **Claude Code.** Requires Claude Code 2.1.283+ and Node.js 22+. Install the official plugin from `VirusTotal/virustotal-mcp` (or run `claude mcp add --transport http virustotal https://ai.virustotal.com/mcp`), run `/reload-plugins` (or start a new session), and authenticate from `/mcp`:
  ```bash
  claude plugin marketplace add VirusTotal/virustotal-mcp
  claude plugin install virustotal@virustotal
  ```
- **Codex CLI.** Register the remote URL and complete browser login:
  ```bash
  codex mcp add virustotal --url https://ai.virustotal.com/mcp
  codex mcp login virustotal
  ```
- **Cursor.** Add `virustotal` under `mcpServers` in `~/.cursor/mcp.json` or `.cursor/mcp.json`:
  ```json
  {
    "mcpServers": {
      "virustotal": {
        "url": "https://ai.virustotal.com/mcp"
      }
    }
  }
  ```
- **VS Code.** Add `virustotal` under `servers` with `"type": "http"` in `.vscode/mcp.json`:
  ```json
  {
    "servers": {
      "virustotal": {
        "type": "http",
        "url": "https://ai.virustotal.com/mcp"
      }
    }
  }
  ```
  Note that upstream `https://ai.virustotal.com/install.md` currently marks Cursor and VS Code VTAI OAuth workflows as unverified.

For client compatibility matrices and quota details, see the [VirusTotal AI MCP installation guide](https://ai.virustotal.com/install.md) and the [VirusTotal/virustotal-mcp GitHub repository](https://github.com/VirusTotal/virustotal-mcp).

## Troubleshooting

| Symptom | Cause | Resolution |
| :--- | :--- | :--- |
| `HTTP 401`, `HTTP 307 Temporary Redirect`, or empty tool list when URL omits `/` | Omitting `/` returns `HTTP 401` when unauthenticated and a cross-scheme `HTTP 307` redirect (`Location: http://www.virustotal.com/api/v3/agentspace/mcp/`) when authenticated; clients strip `x-apikey` across the `https` to `http` downgrade and fail with `HTTP 401` | Set the URL to `https://www.virustotal.com/api/v3/agentspace/mcp/` with the trailing `/` rather than enabling cross-redirect header forwarding. |
| `HTTP 406 Not Acceptable: Client must accept both application/json and text/event-stream` | Custom `Accept` header specifies only one media type | Send `Accept: application/json, text/event-stream`, or remove custom `Accept` overrides when using an MCP SDK transport. |
| `HTTP 401` or `HTTP 403` authorization error | Missing `x-apikey` header, unexpanded `${VT_APIKEY}` placeholder, Gemini CLI redacting non-`GEMINI_CLI_*` `headers` variables (`$VT_APIKEY` to `""`), Goose missing `env_keys: [VT_APIKEY]`, or API key without active PoC / Enterprise entitlement | Export `GEMINI_CLI_VT_APIKEY="$VT_APIKEY"` for Gemini CLI, add `env_keys: [VT_APIKEY]` in `~/.config/goose/config.yaml` for Goose, confirm your key belongs to a Google Threat Intelligence Enterprise, Enterprise Plus, or active PoC license, or switch to `https://ai.virustotal.com/mcp` with OAuth 2.1 for free-tier report lookups. |
| Gemini CLI `/mcp` reports `Disconnected` | Gemini CLI treats bare `"url"` without `"type"` as legacy SSE | Configure `"type": "http"` with `"url"` in `~/.gemini/settings.json` (or `"httpUrl"` on older Gemini CLI builds). |
| Request times out during `ask_gti_agent` or `continue_chat` | Client enforces a 30-second or 60-second request deadline (such as `mcp-remote`'s 60-second SDK timeout) | Raise the client timeout to 300 seconds (300000 milliseconds) and keep each `continue_chat` prompt focused on a single follow-up question. If a call times out after creating a session, call `list_sessions` and `get_session_history` to retrieve the finished response. |

## Related documentation

- [Agentic MCP Server Configuration](https://gtidocs.virustotal.com/docs/agentic-mcp-guide)
- [Google Threat Intelligence Agentic Platform](https://gtidocs.virustotal.com/docs/agentic-platform)
- [How to get GTI API keys](https://gtidocs.virustotal.com/docs/how-get-gti-api-keys)
- [Install VirusTotal for your agent (ai.virustotal.com/mcp)](https://ai.virustotal.com/install.md)
- [Local Google Threat Intelligence MCP server guide](servers/gti_mcp.md)
