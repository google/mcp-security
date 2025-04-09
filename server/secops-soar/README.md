This is a personal project.

# Chronicle SecOps SOAR MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google's
Chronicle Security Operations SOAR suite.
[MCP Info](https://modelcontextprotocol.io/introduction)

## Installing in Claude Desktop

To use this MCP server with Claude Desktop:

1.  Install Claude Desktop

2.  Open Claude Desktop and select "Settings" from the Claude menu

3.  Click on "Developer" in the lefthand bar, then click "Edit Config"

4.  Update your `claude_desktop_config.json` with the following configuration
    (replace paths with your actual paths):

```json
{
  "mcpServers": {
    "secops-soar": {
      "command": "/path/to/your/uv",
      "args": [
        "--directory",
        "/path/to/your/mcp-secops-soar",
        "run",
        "secops_soar_mcp.py"
      ],
      "env": {
        "SOAR_URL": "your-soar-url",
        "SOAR_APP_KEY": "your-soar-app-key"
      }
    }
  }
}
```

To have the MCP server provide tools for specific marketplace integrations, use the `integrations` flag followed by a comma-separated string of the desired integration names. For example, for the `ServiceNow`, `CSV`, and `Siemplify` integrations:
```json
{
  "mcpServers": {
    "secops-soar": {
      "command": "/path/to/your/uv",
      "args": [
        "--directory",
        "/path/to/your/mcp-secops-soar",
        "run",
        "secops_soar_mcp.py",
        "--integrations",
        "ServiceNow,CSV,Siemplify"
      ],
      "env": {
        "SOAR_URL": "your-soar-url",
        "SOAR_APP_KEY": "your-soar-app-key"
      }
    }
  }
}
```

1.  Make sure to update:

    -   The path to `uv` (use `which uv` to find it)
    -   The directory path to where this repository is cloned
    -   Your SOAR URL and AppKey

2.  Save the file and restart Claude Desktop

3.  You should now see the hammer icon in the Claude Desktop interface,
    indicating the MCP server is active

## Features

### Security Tools

-   TBD

## Installation


### Manual Installation

1.  Install the package:

```bash
pip install -e .
```

1.  Set up your environment variables:

```bash
export TBD
```

## Requirements

-   Python 3.11+
-   SOAR URL and AppKey

## Usage

### Running the MCP Server

```bash
python secops_soar_mcp.py
```

### API Capabilities

The MCP server provides the following capabilities:


## License

Apache 2.0

## Development

The project is structured as follows:

-   `secops_soar_mcp.py`: Main MCP server implementation
