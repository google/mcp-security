# Google Security Operations and Threat Intelligence MCP Server

This repository contains three separate MCP servers that enable MCP clients to
access Google Security Operations, Google Security Operations SOAR, and Google
Threat Intelligence API services.

To easily support environments that do not have all three, individual servers
can be enabled and run separately.

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
        "CHRONICLE_PROJECT_ID": "your-google-cloud-project-id",
        "CHRONICLE_CUSTOMER_ID": "your-chronicle-customer-id",
        "CHRONICLE_REGION": "us"
      }
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
        "SOAR_URL": "your-soar-url",
        "SOAR_APP_KEY": "your-soar-app-key"
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
        "VT_API_KEY": "your-vt-api-key"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

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
