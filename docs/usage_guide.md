# Usage guide

This guide shows how to authenticate, install, and configure the Google MCP Security servers across MCP clients and AI coding agents.

## Prerequisites

Before configuring a server, set up authentication and `uv`:

1. **Google Cloud authentication** (required for Google SecOps SIEM, Remote MCP, and Security Command Center):
   - **Interactive user credentials (recommended for local use)**: Sign in with your Google Cloud account and populate Application Default Credentials (ADC):
     ```bash
     ACCOUNT="analyst@example.com"
     PROJECT_ID="your-project-id"
     gcloud auth login "$ACCOUNT" --update-adc
     gcloud config set project "$PROJECT_ID"
     gcloud auth application-default set-quota-project "$PROJECT_ID"
     ```
   - **Service account key**: Point `GOOGLE_APPLICATION_CREDENTIALS` (or `SECOPS_SA_PATH` for `google-secops-mcp`) to a service account JSON key file.

2. **Product credentials** (for the servers you plan to enable):
   - **Google SecOps SIEM**: `CHRONICLE_PROJECT_ID`, `CHRONICLE_CUSTOMER_ID` (tenant UUID), and `CHRONICLE_REGION` (defaults to `us`).
   - **Google SecOps SOAR**: `SOAR_URL` and `SOAR_APP_KEY`.
   - **Google Threat Intelligence**: `VT_APIKEY` from your VirusTotal profile.
   - **Security Command Center**: Uses ADC and IAM permissions on your target project or organization.

3. **Python package runner (`uv`)**:
   - Install `uv` from the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) to run the MCP servers in isolated virtual environments.

## Getting started

You can connect to Google security tools in three ways:

1. **Managed remote endpoint (Google SecOps SIEM and migrated SOAR)**: Point your MCP client at the hosted Google Cloud endpoint with zero local Python processes. Follow the [Remote MCP server guide](remote_server.md).
2. **Published PyPI packages (`uvx` or `uv tool install`)**: Launch standalone `stdio` servers directly from PyPI without cloning the repository:
   - `uvx --from google-secops-mcp secops_mcp`
   - `uvx --from gti-mcp gti_mcp`
   - `uvx --from scc-mcp scc_mcp`
   - `uvx --from secops-soar-mcp secops_soar_mcp`
3. **Local Git checkout (`uv --directory`)**: Clone the repository when you want unreleased tools on `main`, local code edits, or dynamic `--integrations` marketplace loading in `secops-soar-mcp`:
   ```bash
   git clone https://github.com/google/mcp-security.git
   cd mcp-security
   ```

### Configure your MCP client

Most MCP clients use the same `command`, `args`, and `env` fields inside a JSON or YAML configuration file. Add the servers you need to your client's configuration file:

| Client or agent harness | Configuration file path | Format |
| :--- | :--- | :--- |
| [Gemini CLI](https://geminicli.com) | `~/.gemini/settings.json` | JSON (`mcpServers`) |
| [Antigravity](https://antigravity.google) | `~/.gemini/antigravity/mcp_config.json` | JSON (`mcpServers`) |
| [Goose](https://goose-docs.ai/) ([aaif-goose/goose](https://github.com/aaif-goose/goose)) | `~/.config/goose/config.yaml` | YAML (`extensions`) |
| Claude Code | `~/.claude.json` or workspace `.mcp.json` | JSON (`mcpServers`) |
| [Claude Desktop](https://claude.ai/download) | macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`<br>Windows: `%APPDATA%\Claude\claude_desktop_config.json` | JSON (`mcpServers`) |
| Cursor | `~/.cursor/mcp.json` or workspace `.cursor/mcp.json` | JSON (`mcpServers`) |
| VS Code / [Cline](https://cline.bot/) | `.vscode/mcp.json` or `cline_mcp_settings.json` ([sample config on GitHub](https://github.com/google/mcp-security/blob/main/cline_mcp_settings.json.example)) | JSON (`servers` or `mcpServers`) |
| [Google ADK security agent](adk_agent.md) | `run-with-google-adk/.env` | `.env` file (`mcp-security-agent`) |

#### Goose configuration example

In [Goose](https://goose-docs.ai/), add stdio MCP servers under `extensions` in `~/.config/goose/config.yaml`:

```yaml
extensions:
  secops:
    name: Google SecOps SIEM
    type: stdio
    enabled: true
    cmd: uvx
    args:
      - --from
      - google-secops-mcp
      - secops_mcp
    envs:
      CHRONICLE_PROJECT_ID: your-project-id
      CHRONICLE_CUSTOMER_ID: a1b2c3d4-e5f6-4321-abcd-ef1234567890
      CHRONICLE_REGION: us
  gti:
    name: Google Threat Intelligence
    type: stdio
    enabled: true
    cmd: uvx
    args:
      - --from
      - gti-mcp
      - gti_mcp
    env_keys:
      - VT_APIKEY
```

#### Prebuilt Google ADK agent

To run the repository's standalone terminal and web investigation agent instead of an external IDE client, see the [Google ADK security agent guide](adk_agent.md):

```bash
cd run-with-google-adk
cp .env.example .env
uv run mcp-security-agent chat --secops
```

## MCP server configuration reference

Choose either the PyPI (`uvx`) configuration or the local repository (`uv --directory`) configuration below. Store secrets in environment variables or an `--env-file` rather than committing API keys to disk.

> **macOS note:** If you installed `uv` with the standalone installer (`~/.local/bin/uv`), GUI apps such as Claude Desktop may not inherit `~/.local/bin` on `PATH`. Specify the absolute path `/Users/<username>/.local/bin/uv` (or `/Users/<username>/.local/bin/uvx`) in `"command"`. For Python.org macOS installers encountering certificate errors with `secops-soar`, run `/Applications/Python\ 3.12/Install\ Certificates.command` (matching your Python version) or set `SSL_CERT_FILE`.

### Option A: Run from PyPI with `uvx`

```json
{
  "mcpServers": {
    "secops": {
      "command": "uvx",
      "args": ["--from", "google-secops-mcp", "secops_mcp"],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "a1b2c3d4-e5f6-4321-abcd-ef1234567890",
        "CHRONICLE_REGION": "us"
      }
    },
    "secops-soar": {
      "command": "uvx",
      "args": ["--from", "secops-soar-mcp", "secops_soar_mcp"],
      "env": {
        "SOAR_URL": "https://your-instance.siemplify-soar.com:443",
        "SOAR_APP_KEY": "a1b2c3d4-e5f6-4321-abcd-ef1234567890"
      }
    },
    "gti": {
      "command": "uvx",
      "args": ["--from", "gti-mcp", "gti_mcp"],
      "env": {
        "VT_APIKEY": "your-virustotal-api-key"
      }
    },
    "scc-mcp": {
      "command": "uvx",
      "args": ["--from", "scc-mcp", "scc_mcp"],
      "env": {}
    }
  }
}
```

### Option B: Run from a local Git clone

Use a local checkout to run the latest `main` branch code (including SCC v2 search and compliance tools ahead of the next PyPI release) or to load marketplace integration modules via `--integrations` on `secops-soar`:

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/secops/secops_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "a1b2c3d4-e5f6-4321-abcd-ef1234567890",
        "CHRONICLE_REGION": "us"
      }
    },
    "secops-soar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/secops-soar/secops_soar_mcp",
        "run",
        "server.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {
        "SOAR_URL": "https://your-instance.siemplify-soar.com:443",
        "SOAR_APP_KEY": "a1b2c3d4-e5f6-4321-abcd-ef1234567890"
      }
    },
    "gti": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/gti/gti_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "VT_APIKEY": "your-virustotal-api-key"
      }
    },
    "scc-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/scc",
        "run",
        "scc_mcp.py"
      ],
      "env": {}
    }
  }
}
```

### Load secrets with `--env-file`

`uv run` accepts `--env-file` so you can keep API keys outside your client configuration JSON:

```json
{
  "command": "uv",
  "args": [
    "--directory",
    "/path/to/mcp-security/server/gti/gti_mcp",
    "run",
    "--env-file",
    "/path/to/secrets/.env",
    "server.py"
  ],
  "env": {}
}
```

### Setting up environment variables

#### macOS and Linux

Add the variables you need to `~/.bashrc`, `~/.zshrc`, or a per-directory `.envrc`:

```bash
# Google Security Operations SIEM
export CHRONICLE_PROJECT_ID="your-project-id"
export CHRONICLE_CUSTOMER_ID="a1b2c3d4-e5f6-4321-abcd-ef1234567890"
export CHRONICLE_REGION="us"

# Google Security Operations SOAR (pass marketplace modules with --integrations on the CLI)
export SOAR_URL="https://your-instance.siemplify-soar.com:443"
export SOAR_APP_KEY="your-soar-app-key"

# Google Threat Intelligence
export VT_APIKEY="your-virustotal-api-key"
```

Reload your shell configuration (`source ~/.bashrc` or `source ~/.zshrc`) and restart your MCP client.

#### Windows PowerShell

```powershell
$Env:CHRONICLE_PROJECT_ID = "your-project-id"
$Env:CHRONICLE_CUSTOMER_ID = "a1b2c3d4-e5f6-4321-abcd-ef1234567890"
$Env:CHRONICLE_REGION = "us"
$Env:SOAR_URL = "https://your-instance.siemplify-soar.com:443"
$Env:SOAR_APP_KEY = "your-soar-app-key"
$Env:VT_APIKEY = "your-virustotal-api-key"
```

## Usage examples

Once your MCP client connects to the servers, prompt the assistant with concrete investigation tasks:

- **Google SecOps SIEM**: `"Search UDM events from the past 24 hours for encoded PowerShell commands and summarize the affected hosts."`
- **Google SecOps SIEM (YARA-L 2.0 rules)**: `"Validate this YARA-L 2.0 detection rule and test it against the past 7 days of telemetry."`
- **Google SecOps SOAR**: `"List open high-priority SOAR cases and show full alert and entity details for the most recent case."` (See [SOAR Integrations](soar_integrations/index.md) for third-party action tools.)
- **Google Threat Intelligence**: `"Search Google Threat Intelligence for recent ransomware campaigns targeting financial services and list their associated IOCs and MITRE ATT&CK techniques."`
- **Security Command Center**: `"List the top critical vulnerability findings sorted by Attack Exposure Score in project 'your-project-id' and provide remediation steps for the top finding."`

## Troubleshooting

If a server fails to initialize or tools do not appear in your client:

1. **Verify Google Cloud ADC**: Confirm `~/.config/gcloud/application_default_credentials.json` (or `GOOGLE_APPLICATION_CREDENTIALS`) is valid by running `gcloud auth login "$ACCOUNT" --update-adc`.
2. **Verify `uv` on `PATH`**: Run `which uv` (or `where uv` on Windows) and use the full binary path in GUI client configs if needed.
3. **Check server stderr logs**: Inspect your MCP client's server log panel for startup tracebacks or missing environment variables.
4. **Restart the MCP client**: Reload or restart the client after editing configuration files or shell variables.

### Find the right `SOAR_URL` for Google SecOps SOAR

If `secops-soar` exits on startup with:

```text
Error: Failed to fetch valid scopes from SOAR, please make sure you have configured the right SOAR credentials. Shutting down...
MCP error -32000: Connection closed
```

verify that `SOAR_URL` points to your Google SecOps SOAR instance base URL rather than your SIEM URL. Use either method to locate the SOAR base URL:

1. In Google SecOps SOAR, open **Settings > Webhooks**, create a temporary webhook, and copy the scheme and host from the generated URL (for example, `https://example-instance.siemplify-soar.com`).
2. Open your browser developer tools on the **Network** tab, navigate to **Cases** in the SOAR UI, inspect a `GetCaseCardsByRequest` call, and copy the origin from its request URL.

### Corporate proxies and custom TLS certificates

All four local MCP servers honor standard `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables. When a corporate proxy performs TLS inspection with a custom root certificate authority (CA), set the CA bundle variable that matches each server's underlying HTTP or gRPC transport:

| Server | Transport library | Proxy variables | Custom TLS CA bundle variable |
| :--- | :--- | :--- | :--- |
| `secops` (`google-secops-mcp`) | `requests` (`google-secops`) | `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | `REQUESTS_CA_BUNDLE` |
| `gti` (`gti-mcp`) | `aiohttp` (`vt-py`, `trust_env=True`) | `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | `SSL_CERT_FILE` |
| `secops-soar` (`secops-soar-mcp`) | `aiohttp` (`trust_env=True`) | `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | `SSL_CERT_FILE` |
| `scc-mcp` | `grpcio` and `google-auth` (`requests`) | `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | `GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` and `REQUESTS_CA_BUNDLE` |

Pass both the proxy URLs and the CA bundle path in your MCP client's `env` block when the client does not inherit your shell environment:

```json
{
  "mcpServers": {
    "secops": {
      "command": "uvx",
      "args": ["--from", "google-secops-mcp", "secops_mcp"],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "a1b2c3d4-e5f6-4321-abcd-ef1234567890",
        "CHRONICLE_REGION": "us",
        "HTTPS_PROXY": "http://proxy.corp.example.com:8080",
        "REQUESTS_CA_BUNDLE": "/etc/ssl/certs/corp-root-ca.pem"
      }
    },
    "gti": {
      "command": "uvx",
      "args": ["--from", "gti-mcp", "gti_mcp"],
      "env": {
        "VT_APIKEY": "your-virustotal-api-key",
        "HTTPS_PROXY": "http://proxy.corp.example.com:8080",
        "SSL_CERT_FILE": "/etc/ssl/certs/corp-root-ca.pem"
      }
    }
  }
}
```
