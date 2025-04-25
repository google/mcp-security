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

## Authentication

The server uses Google's authentication. Make sure you have either:

1. Set up Application Default Credentials (ADC)
2. Set a GOOGLE_APPLICATION_CREDENTIALS environment variable
3. Used `gcloud auth application-default login`

## Client Configuration

The configuration for Claude Desktop and cline is the same. We make use of uv to
run the mcp services locally and use the stdio transport.

### Using uv (Recommended)

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops/secops_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
        "CHRONICLE_REGION": "us"
      },
      "disabled": false,
      "autoApprove": []
    },
    "secops-soar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops-soar/secops_soar_mcp",
        "run",
        "server.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {
        "SOAR_URL": "https://yours-here.siemplify-soar.com:443",
        "SOAR_APP_KEY": "01234567-abcd-4321-1234-0123456789ab"
      },
      "disabled": false,
      "autoApprove": []
    },
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "VT_APIKEY": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
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

NOTE: `uv` also supports passing an `.env` file like so:
```
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/...",
        "run",
        "--env-file",
        "/path/to/the/repo/server/.env",
        "server.py"
      ]
```

`SOAR_APP_KEY` and `VT_APIKEY` are good candidates for `.env`


### Using pip

You can also use pip instead of uv to install and run the MCP servers. This approach uses a bash command to:
1. Change to the server directory
2. Install the package in development mode
3. Run the server binary

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
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
        "CHRONICLE_REGION": "us"
      },
      "disabled": false,
      "autoApprove": [
      ],
      "alwaysAllow": [
      ]
    },
    "gti": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/gti && pip install -e . && gti_mcp"
      ],
      "env": {
        "VT_APIKEY": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      },
      "disabled": false,
      "autoApprove": [
      ],
      "alwaysAllow": [
      ]
    },
  "secops-soar": {
      "autoApprove": [
      ],
      "disabled": false,
      "timeout": 60,
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/secops-soar && pip install -e . && python secops_soar_mcp/server.py"
      ],
      "env": {
        "SOAR_URL": "https://yours-here.siemplify-soar.com:443",
        "SOAR_APP_KEY": "01234567-abcd-4321-1234-0123456789ab"
      },
      "transportType": "stdio"
    }
  }
  }
}
```

### When to use uv vs pip

- **uv**: Recommended for most users because it offers faster package installation, better dependency resolution, and isolated environments. It also supports loading environment variables from a file.
- **pip**: Use when you prefer the standard Python package manager or when you have specific environment setup requirements.

#### `UV_ENV_FILE`

The `--env-file` option allows `uv` to use a .env file for environment variables. You can create this file or use system environment variables as described in the usage guide.

Alternatively, you can set `UV_ENV_FILE` to your `.env` file and omit the `--env-file` portion of the configuration.

Refer to the [usage guide](docs/usage_guide.md#setting-up-environment-variables) for detailed instructions on how to set up these environment variables.


### Troubleshooting

Running the MCP Server from the CLI (and outside of your MCP client) can reveal issues:
```
uv --verbose \
  --directory "/Users/dandye/Projects/google-mcp-security/server/scc" \
  run \
  --env-file "/Users/dandye/Projects/google-mcp-security/.env" \
  scc_mcp.py
```

Check your PATH(s):

```which uv``` # you may need to restart MCP Client after installing uv

```which python || which python3```

```python --version || python3 --version```



### Installing in Claude Desktop

To use the MCP servers with Claude Desktop:

1. Install Claude Desktop
2. Open Claude Desktop and select "Settings" from the Claude menu
3. Click on "Developer" in the lefthand bar, then click "Edit Config"
4. Update your `claude_desktop_config.json` with the configuration (replace paths with your actual paths)
5. Save the file and restart Claude Desktop
6. You should now see the hammer icon in the Claude Desktop interface, indicating the MCP server is active

### Installing in cline (vscode extension)

1. Install cline.bot extension in VSCode
2. Update your `cline_mcp_settings.json` with the configuration (replace paths with your actual paths)
3. Save the file and restart VS Code

## License

Apache 2.0
