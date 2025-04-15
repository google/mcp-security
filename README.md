# Google Security Operations and Threat Intelligence MCP Server

This repository contains Model Context Protocol (MCP) servers that enable MCP clients (like Claude Desktop or the cline.bot VS Code extension) to access Google's security products and services:

1. **Google Security Operations (Chronicle)** - For threat detection, investigation, and hunting
2. **Google Security Operations SOAR** - For security orchestration, automation, and response
3. **Google Threat Intelligence (GTI)** - For access to Google's threat intelligence data
4. **Security Command Center (SCC)** - For cloud security and risk management

Each server can be enabled and run separately, allowing flexibility for environments that don't require all capabilities.

## Documentation

Comprehensive documentation is available in the `docs` folder. You can:

1. Read the markdown files directly in the repository
2. View the documentation website at [https://google.github.io/mcp-security/](https://google.github.io/mcp-security/)
3. Generate HTML documentation locally using Sphinx (see instructions in the docs folder)

The documentation covers:
- Detailed information about each MCP server
- Configuration options and requirements
- Usage examples and best practices

To get started with the documentation, see [docs/index.md](docs/index.md).

## Installation

## Authentication

The server uses Google's authentication. Make sure you have either:

1.  Set up Application Default Credentials (ADC)
2.  Set a GOOGLE_APPLICATION_CREDENTIALS environment variable
3.  Used `gcloud auth application-default login`

## Client Configuration

The configuration for Claude Desktop and cline is the same. We make use of uv to
run the mcp services locally and use the stdio transport.

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops",
        "run",
        "secops_mcp.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "${CHRONICLE_PROJECT_ID}",
        "CHRONICLE_CUSTOMER_ID": "${CHRONICLE_CUSTOMER_ID}",
        "CHRONICLE_REGION": "${CHRONICLE_REGION}"
      },
      "disabled": false,
      "autoApprove": []
    },
    "secops-soar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops-soar",
        "run",
        "secops_soar_mcp.py"
      ],
      "env": {
        "SOAR_URL": "${SOAR_URL}",
        "SOAR_APP_KEY": "${SOAR_APP_KEY}"
      },
      "disabled": false,
      "autoApprove": []
    },
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/gti",
        "run",
        "gti.py"
      ],
      "env": {
        "VT_APIKEY": "${VT_APIKEY}"
      },
      "disabled": false,
      "autoApprove": []
    },
    "scc-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/scc",
        "run",
        "scc_mcp.py"
      ],
      "env": {
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Refer to the [usage guide](docs/usage_guide.md#setting-up-environment-variables) for detailed instructions on how to set up these environment variables.

### Installing in Claude Desktop

To use the MCP servers with Claude Desktop:

1.  Install Claude Desktop

1.  Open Claude Desktop and select "Settings" from the Claude menu

1.  Click on "Developer" in the lefthand bar, then click "Edit Config"

1.  Update your `claude_desktop_config.json` with the configuration (replace
    paths with your actual paths):

1.  Save the file and restart Claude Desktop

1.  You should now see the hammer icon in the Claude Desktop interface,
    indicating the MCP server is active

### Installing in cline (vscode extension)

1.  Install cline.bot extension in VSCode.

1.  Update your `cline_mcp_settings.json` with the configuration (replace paths
    with your actual paths):

1.  Save the file and restart Claude Desktop

## License

Apache 2.0
