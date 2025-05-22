# Chronicle SecOps MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google's
Chronicle Security Operations suite.
[MCP Info](https://modelcontextprotocol.io/introduction)

## Features

### Security Tools

- **`search_security_events(text, project_id=None, customer_id=None, hours_back=24, max_events=100, region=None)`**
    - Searches for security events in Chronicle using natural language. Translates the natural language query (`text`) into a UDM query and executes it.

- **`get_security_alerts(project_id=None, customer_id=None, hours_back=24, max_alerts=10, status_filter='feedback_summary.status != "CLOSED"', region=None)`**
    - Retrieves security alerts from Chronicle, filtered by time range and status.

- **`lookup_entity(entity_value, project_id=None, customer_id=None, hours_back=24, region=None)`**
    - Looks up an entity (IP, domain, hash, etc.) in Chronicle.

- **`list_security_rules(project_id=None, customer_id=None, region=None)`**
    - Lists security detection rules from Chronicle.

- **`search_security_rules(query, project_id=None, customer_id=None, region=None)`**
    - Searches security detection rules from Chronicle using regex.

- **`get_ioc_matches(project_id=None, customer_id=None, hours_back=24, max_matches=20, region=None)`**
    - Retrieves Indicators of Compromise (IoCs) matches from Chronicle within a specified time range.

- **`get_threat_intel(query, project_id=None, customer_id=None, region=None)`**
    - Get answers to general security domain questions and specific threat intelligence information using Chronicle's AI capabilities.

### API Capabilities

The MCP server provides the following capabilities:

1.  **Search Security Events**: Search for security events in Chronicle
2.  **Get Security Alerts**: Retrieve security alerts
3.  **Lookup Entity**: Look up entity information (IP, domain, hash, etc.)
4.  **List Security Rules**: List detection rules
5.  **Search Security Rules**: Searches detection rules using regex
6.  **Get IoC Matches**: Get Indicators of Compromise matches

### Example

See `example.py` for a complete example of using the MCP server.

## Configuration

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

**NOTE:** For OSX users, if you used [this one-liner](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to install uv, use the full path to the uv binary for the "command" value below, as uv will not be placed in the system path for Claude to use! For example: `/Users/yourusername/.local/bin/uv` instead of just `uv`.

#### Using uv (Recommended)

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/secops/secops_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "${CHRONICLE_PROJECT_ID}",
        "CHRONICLE_CUSTOMER_ID": "${CHRONICLE_CUSTOMER_ID}",
        "CHRONICLE_REGION": "${CHRONICLE_REGION}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

#### Using pip

You can also use pip instead of uv to install and run the MCP server:

```json
{
  "mcpServers": {
    "secops": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/secops && pip install -e . && secops_mcp"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "${CHRONICLE_PROJECT_ID}",
        "CHRONICLE_CUSTOMER_ID": "${CHRONICLE_CUSTOMER_ID}",
        "CHRONICLE_REGION": "${CHRONICLE_REGION}"
      },
      "disabled": false,
      "autoApprove": [
        "get_ioc_matches",
        "search_security_events",
        "get_security_alerts"
      ],
      "alwaysAllow": [
        "get_ioc_matches"
      ]
    }
  }
}
```

#### When to use uv vs pip

- **uv**: Recommended for most users as it provides faster package installation, better dependency resolution, and supports loading environment variables from a file with the `--env-file` option.
- **pip**: Use when you prefer the standard Python package manager or when you need specific environment setup requirements.

### Environment Variable Setup

Set up these environment variables in your system:

**For macOS/Linux:**
```bash
export CHRONICLE_PROJECT_ID="your-google-cloud-project-id"
export CHRONICLE_CUSTOMER_ID="your-chronicle-customer-id"
export CHRONICLE_REGION="us"
```

**For Windows PowerShell:**
```powershell
$Env:CHRONICLE_PROJECT_ID = "your-google-cloud-project-id"
$Env:CHRONICLE_CUSTOMER_ID = "your-chronicle-customer-id"
$Env:CHRONICLE_REGION = "us"
```

The `CHRONICLE_REGION` can be one of:
- `us` - United States (default)
- `eu` - Europe
- `asia` - Asia-Pacific

## License

Apache 2.0

## Development

The project is structured as follows:

- `server.py`: Main MCP server implementation
- `example.py`: Example usage of the MCP server 