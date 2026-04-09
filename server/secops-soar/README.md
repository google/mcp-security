# Chronicle SecOps SOAR MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google's
Chronicle Security Operations SOAR suite.
[MCP Info](https://modelcontextprotocol.io/introduction)

## Features

### Core Tools (Case Management & Entities)

- **`list_cases()`** - Lists available cases in the SOAR platform.
- **`post_case_comment(case_id, comment)`** - Adds a textual comment to a specific case.
- **`list_alerts_by_case(case_id)`** - Lists all alerts associated with a specific case ID.
- **`list_alert_group_identifiers_by_case(case_id)`** - Lists the unique group identifiers for alerts within a specific case.
- **`list_events_by_alert(case_id, alert_id)`** - Lists the events associated with a particular alert within a given case.
- **`change_case_priority(case_id, case_priority)`** - Modifies the priority level of a specific case.
- **`get_entities_by_alert_group_identifiers(case_id, alert_group_identifiers)`** - Retrieves entities involved in one or more alert groups.
- **`get_entity_details(entity_identifier, entity_type, entity_environment)`** - Fetches detailed information about a specific entity.
- **`search_entity(term=None, type=None, is_suspicious=None, is_internal_asset=None, is_enriched=None, network_name=None, environment_name=None)`** - Searches for entities within the SOAR platform.
- **`get_case_full_details(case_id)`** - Retrieves comprehensive details for a single case.

### Dynamic Integration Tools (Marketplace)

This server can dynamically load additional tools based on integrations enabled via the `--integrations` command-line flag when the server is started. These tools correspond to modules found in the `marketplace/` directory.

Available integrations include:
- ServiceNow
- CSV
- Jira
- Slack
- Email
- VirusTotal
- Active Directory
- Microsoft Defender ATP
- And many more

## Installing in Claude Desktop

To use this MCP server with Claude Desktop:

1.  Install Claude Desktop

2.  Open Claude Desktop and select "Settings" from the Claude menu

3.  Click on "Developer" in the lefthand bar, then click "Edit Config"

4.  Update your `claude_desktop_config.json` with the following configuration
    (replace paths with your actual paths):
    
    **NOTE:** For OSX users, if you used [this one-liner](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to install uv, use the full path to the uv binary for the "command" value below, as uv will not be placed in the system path for Claude to use! For example: `/Users/yourusername/.local/bin/uv` instead of just `uv`.

    Additionally, for the secops-soar MCP server, you will need use the CA list bundled with the certifi package. This can be done via the following command. Change the Python minor version to match whatever version you are currently running. (ex. `Python\ 3.11`):
    `/Applications/Python\ 3.12/Install\ Certificates.command`

```json
{
  "mcpServers": {
    "secops-soar": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/secops-soar/secops_soar_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "SOAR_URL": "${SOAR_URL}",
        "SOAR_APP_KEY": "${SOAR_APP_KEY}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

To have the MCP server provide tools for specific marketplace integrations, use the `integrations` flag followed by a comma-separated string of the desired integration names. For example, for the `ServiceNow`, `CSV`, and `Siemplify` integrations:
```json
{
  "mcpServers": {
    "secops-soar": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/secops-soar/secops_soar_mcp",
        "run",
        "server.py",
        "--integrations",
        "ServiceNow,CSV,Siemplify"
      ],
      "env": {
        "SOAR_URL": "${SOAR_URL}",
        "SOAR_APP_KEY": "${SOAR_APP_KEY}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Environment Variable Setup

Set up these environment variables in your system:

**For macOS/Linux:**
```bash
export SOAR_URL="your-soar-url"
export SOAR_APP_KEY="your-soar-app-key"
export SOAR_INTEGRATIONS="ServiceNow,CSV,Siemplify"
```

**For Windows PowerShell:**
```powershell
$Env:SOAR_URL = "your-soar-url"
$Env:SOAR_APP_KEY = "your-soar-app-key"
$Env:SOAR_INTEGRATIONS = "ServiceNow,CSV,Siemplify"
```

## Requirements

-   Python 3.11+
-   SOAR URL and AppKey

## Troubleshooting

### SSL Certificate Verification Error

If you see an error like:

```
SSL certificate verification failed when connecting to SOAR.
```

or the older generic message:

```
Failed to fetch valid scopes from SOAR
```

This is typically caused by Python not having access to the correct CA (Certificate Authority) certificates. This is especially common on **macOS**.

**Fix for macOS:**

Run the `Install Certificates.command` script that ships with your Python installation. Replace `3.12` with your actual Python minor version:

```bash
/Applications/Python\ 3.12/Install\ Certificates.command
```

This installs the [`certifi`](https://pypi.org/project/certifi/) CA bundle, which Python needs for SSL/TLS verification.

**Fix for all platforms:**

```bash
pip install --upgrade certifi
```

Then restart the MCP server.

For further details, see the [usage guide](https://google.github.io/mcp-security/usage_guide.html#mcp-server-configuration-reference).

### Connection Error

If you see:

```
Failed to connect to SOAR at '<your-url>'.
```

Verify that:
1. The `SOAR_URL` environment variable is set correctly (e.g., `https://yours-here.siemplify-soar.com:443`).
2. The SOAR server is reachable from your network.
3. Any required VPN or proxy is active.

### Invalid Credentials

If you see:

```
Failed to fetch valid scopes from SOAR.
```

Verify that:
1. `SOAR_URL` is set and correct.
2. `SOAR_APP_KEY` is set and valid.

## License

Apache 2.0

## Development

The project is structured as follows:

-   `server.py`: Main MCP server implementation
-   `marketplace/`: Directory containing integration modules
