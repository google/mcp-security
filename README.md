# Google Security Operations and Threat Intelligence MCP Server

This repository contains Model Context Protocol (MCP) servers that enable MCP clients (like Claude Desktop or the cline.bot VS Code extension) to access Google's security products and services:

1. **Remote MCP Server for Google SecOps** - Fully managed, enterprise-ready MCP server (Recommended)
2. **Google Security Operations (Chronicle)** - For threat detection, investigation, and hunting
3. **Google Security Operations SOAR** - For security orchestration, automation, and response
4. **Google Threat Intelligence (GTI)** - For access to Google's threat intelligence data
5. **Security Command Center (SCC)** - For cloud security and risk management

For the new **Remote MCP Server**, please see the [launch announcement](https://security.googlecloudcommunity.com/community-blog-42/google-cloud-remote-mcp-server-for-secops-6559) and the [setup guide](docs/remote_server.md).

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

## Standalone Usage

Each MCP server can be installed and used as a standalone package.

### Installation

You can install the packages using `uv tool install` (recommended):

```bash
# Install packages
uv tool install google-secops-mcp
uv tool install gti-mcp
uv tool install scc-mcp
uv tool install secops-soar-mcp
```

Alternatively, you can use pip:

```bash
pip install google-secops-mcp
pip install gti-mcp
pip install scc-mcp
pip install secops-soar-mcp
```

### Running Standalone

After installation, you can run the servers directly using uvx:

```bash
# Run SecOps MCP server
uvx --from google-secops-mcp secops_mcp

# Run GTI MCP server
uvx gti_mcp

# Run SCC MCP server
uvx scc_mcp

# Run SecOps SOAR MCP server (with optional integrations)
uvx secops_soar_mcp --integrations CSV,OKTA
```

With environment variables:

```bash
CHRONICLE_PROJECT_ID="your-project-id" \
CHRONICLE_CUSTOMER_ID="01234567-abcd-4321-1234-0123456789ab" \
CHRONICLE_REGION="us" \
uvx secops_mcp
```

### Using with MCP Clients (Recommended)

You can configure MCP clients to use the installed packages with uvx. Here's an example configuration:

```json
{
  "mcpServers": {
    "secops": {
      "command": "uvx",
      "args": [
        "--from",
        "google-secops-mcp",
        "secops_mcp"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
        "CHRONICLE_REGION": "us"
      }
    },
    "gti": {
      "command": "uvx",
      "args": [
        "gti_mcp"
      ],
      "env": {
        "VT_APIKEY": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      }
    },
    "scc-mcp": {
      "command": "uvx",
      "args": [
        "scc_mcp"
      ],
      "env": {}
    },
    "secops-soar": {
      "command": "uvx",
      "args": [
        "secops_soar_mcp",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {
        "SOAR_URL": "https://yours-here.siemplify-soar.com:443",
        "SOAR_APP_KEY": "01234567-abcd-4321-1234-0123456789ab"
      }
    }
  }
}
```

You can also use environment files with uvx:

```json
{
  "mcpServers": {
    "secops": {
      "command": "uvx",
      "args": [
        "--env-file",
        "/path/to/.env",
        "secops_mcp"
      ]
    }
  }
}
```

## Client Configurations
The MCP servers from this repo can be used with the following clients
1. Cline, Claude Desktop, and other MCP supported clients
2. [Google ADK(Agent Development Kit)](https://google.github.io/adk-docs/) Agents (a prebuilt agent is provided, details [below](#using-the-prebuilt-google-adk-agent-as-client))
3. [Google SecOps Extension](https://google.github.io/mcp-security/google_secops_extension.html) - Install our example extension for Gemini CLI to get specialized security skills (Triage, Investigate, Hunt).

The configuration for Claude Desktop and Cline is the same (provided below for [uv](#using-uv-recommended) and [pip](#using-pip)).  We use the stdio transport.

### Using the Google ADK Autonomous SOC Agent

The repository includes a prebuilt Autonomous Security Operations Center (SOC) Agent powered by Google ADK v2 and the Model Context Protocol in [`run-with-google-adk`](./run-with-google-adk/README.md).

It can be run locally via an interactive CLI REPL or launched as a FastAPI service for Google Cloud Run:

```bash
cd run-with-google-adk
cp sample.env .env

# Interactive terminal investigation REPL
uv run mcp-security-agent chat

# Web UI and Cloud Run REST API server
uv run mcp-security-agent serve --port 8080
```

For full setup, architecture details, and Cloud Run deployment guides, see the [ADK Agent Guide](./run-with-google-adk/README.md).

## MCP Client Config Locations

MCP clients all use the same JSON configuration format (see the [MCP Server Configuration Reference](https://google.github.io/mcp-security/usage_guide.html#mcp-server-configuration-reference)), but they expect the file in different locations.

| Client Application       | Scope     | macOS / Linux Location                | Windows Location                                                                    | Notes                                                                                                                                                                                                |
| ------------------------ | --------- | ------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Gemini CLI**           | Global    | `~/.gemini/settings.json`             | `%USERPROFILE%\.gemini\settings.json`                                               | File must include `mcpServers`. Confirmed in [Google Security Ops post](https://security.googlecloudcommunity.com/google-security-operations-2/google-cloud-security-mcp-servers-in-gemini-cli-922). |
| **Claude Desktop**       | Global    | `~/Claude/claude_desktop_config.json` | `%USERPROFILE%\Claude\claude_desktop_config.json`                                   | Config accessible via *Claude > Settings > Developer > Edit Config*.                                                                                                                                 |
| **Claude Code**          | Global    | `~/.claude.json`                      | `%USERPROFILE%\.claude.json`                                                             | Primary config file for Claude Code CLI and extensions.                                                                                                                                              |
| **Cursor IDE (Global)**  | Global    | `~/.cursor/mcp.json`                  | `%USERPROFILE%\.cursor\mcp.json`                                                    | Enables MCP servers globally across all projects.                                                                                                                                                    |
| **Cursor IDE (Project)** | Project   | `<project-root>/.cursor/mcp.json`     | `<project-root>/.cursor/mcp.json`                                                   | Workspace/project-specific config file.                                                                                                                                                              |
| **VS Code (Workspace)**  | Workspace | `<project-root>/.vscode/mcp.json`     | `<project-root>/.vscode/mcp.json`                                                   | Workspace-level config used when an MCP extension (like **Cline**) is installed. Overrides global config if present.                                                                                 |
| **Cline (VS Code Ext.)** | Global    | Inside VS Code extension data         | `%APPDATA%\Code\User\globalStorage\<extension-id>\settings\cline_mcp_settings.json` | Exact path varies by VS Code variant and platform. `<extension-id>` corresponds to the installed extension folder (e.g., `saoudrizwan.claude-dev`).                                                  |

### Additional Notes for Windows

- `%USERPROFILE%` → `C:\Users\<username>`
- `%APPDATA%` → `C:\Users\<username>\AppData\Roaming`
- `<project-root>` → folder opened in VS Code or IDE for the project
- `<extension-id>` → name of the installed extension folder (e.g., `saoudrizwan.claude-dev` for Claude/Cline)

### Tip: Single Config with Symlinks

If you use multiple MCP clients, you can maintain a **single config file** and symlink it into each expected location. This avoids drift and keeps your server definitions consistent.


### Using uv (Recommended)

> [!TIP]
> **Setup Tips for MCP Client Configurations:**
> - **Absolute path to `uv`:** Desktop clients (Claude Desktop, Cursor, VS Code / Cline) do not inherit shell profile `PATH` additions. If your client reports `spawn uv ENOENT` or command not found, run `which uv` in your terminal and use the full path for `"command"` (e.g., `"/Users/<username>/.local/bin/uv"` on macOS or `"/home/<username>/.local/bin/uv"` on Linux).
> - **Script Names & Directory Levels (Copy-Paste Trap):**
>   - `secops`: points to `server/secops/secops_mcp` running `server.py`
>   - `secops-soar`: points to `server/secops-soar/secops_soar_mcp` running `server.py`
>   - `gti`: points to `server/gti/gti_mcp` running `server.py`
>   - **`scc-mcp`:** points to `server/scc` running **`scc_mcp.py`** (**Note:** `scc_mcp.py`, NOT `server.py`!).
>   - Do not set `--directory` to the top-level `server/` directory or omit the inner `_mcp` folder for SecOps/SOAR/GTI.

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
      }
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
      }
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
      }
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
      }
    }
  }
}
```

#### Passing Environment Variables via `.env` File

`uv` supports passing an `.env` file to load secrets:

> [!WARNING]
> **`--env-file` Placement:** The `--env-file` flag is an argument to `uv run`. It must be placed **after** `run` in the `args` array:
> ```json
>       "command": "uv",
>       "args": [
>         "--directory",
>         "/path/to/the/repo/server/secops/secops_mcp",
>         "run",
>         "--env-file",
>         "/path/to/the/repo/.env",
>         "server.py"
>       ]
> ```
> Placing `--env-file` before `run` (e.g. `uv --env-file run`) is invalid and causes an unrecognized argument error.

Sensitive keys like `SOAR_APP_KEY` and `VT_APIKEY` are great candidates for `.env`.


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
      "alwaysAllow": [
      ]
    },
    "scc-mcp": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/scc && pip install -e . && scc_mcp"
      ],
      "env": {
      },
      "alwaysAllow": []
    },
    "secops-soar": {
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
```

### When to use uv vs pip

- **uv (Recommended)**: Recommended for most users because it offers faster package installation, reliable dependency resolution, and isolated environments. `uv` handles per-server dependency isolation automatically without requiring you to manually create or activate virtual environments.
  - **Standalone `uv` vs. Virtual Environment:** A standalone `uv` installation (installed globally via Astral's installer) is recommended. However, running `uv` from within an existing virtual environment or using an existing venv's Python interpreter is also supported.
- **pip**: Use when you prefer the standard Python package manager or when you have specific environment setup requirements. As shown above, configuring `"command": "/bin/bash"` with `-c "cd ... && pip install -e . && ..."` bypasses `uv` and uses your default environment.

#### `UV_ENV_FILE`

The `--env-file` option allows `uv` to use a `.env` file for environment variables. You can create this file or use system environment variables as described in the usage guide.

Alternatively, you can set the `UV_ENV_FILE` environment variable to your `.env` file path and omit the `--env-file` argument in the configuration.

Refer to the [usage guide](docs/usage_guide.md#setting-up-environment-variables) for detailed instructions on how to set up these environment variables.


### Troubleshooting Setup Friction

If you run into issues when setting up the MCP servers, check these common pitfalls:

1. **Client Cannot Find `uv` (`spawn uv ENOENT` / Command Not Found):**
   - **Cause:** Desktop apps (Claude Desktop, Cursor, VS Code / Cline) do not inherit shell profile environment variables (such as `~/.local/bin` in `PATH`).
   - **Fix:** In your terminal, run `which uv`. Copy the absolute path (e.g. `/Users/<username>/.local/bin/uv` or `/usr/local/bin/uv`) and set `"command": "/absolute/path/to/uv"` in your client config JSON.

2. **Server Script or Directory Not Found (The SCC Copy-Paste Trap):**
   - **Cause:** SecOps, SecOps SOAR, and GTI run `server.py` from nested package directories (`secops_mcp`, `secops_soar_mcp`, `gti_mcp`), while SCC runs `scc_mcp.py` directly from `server/scc/`.
   - **Fix:** Check that your SCC configuration specifies `"scc_mcp.py"`, **not** `"server.py"`. Also verify that `--directory` points to the specific package directory (e.g. `server/secops/secops_mcp`), not the top-level `server/` folder.

3. **SecOps SOAR SSL Certificate Errors (`CERTIFICATE_VERIFY_FAILED`):**
   - **Cause:** On macOS, Python installations frequently do not trust system certificates by default.
   - **Fix:** Run `/Applications/Python\ 3.x/Install\ Certificates.command` (matching your Python version), or set `export SSL_CERT_FILE=$(python3 -m certifi)`.

4. **`--env-file` Syntax and Argument Order:**
   - **Fix:** `--env-file` is a flag to `uv run` and must come **after** `run` in the `args` array: `["run", "--env-file", "/path/to/.env", "server.py"]`. Placing it before `run` will produce command syntax errors.

5. **Testing Server Startup via CLI:**
   Running the MCP server directly in your terminal outside of the client helps reveal exact tracebacks:
   ```bash
   uv --verbose \
     --directory "/path/to/repo/server/scc" \
     run \
     --env-file "/path/to/repo/.env" \
     scc_mcp.py
   ```

   Check your environment and tools:
   ```bash
   which uv      # check uv binary location
   which python3 # check active python
   python3 --version
   ```



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
