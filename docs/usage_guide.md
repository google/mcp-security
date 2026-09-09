# Using the Google Security MCP Servers

This guide will help you get started with using the MCP servers to access Google's security products and services from Claude Desktop or other MCP-compatible clients.

## Prerequisites

Before you begin, make sure you have:

1. **Google Cloud Authentication** set up using one of these two methods:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to a service account key file
   - Application Default Credentials (ADC) configured with:
     - `gcloud config set project ...`  # needed when switching projects
     - `gcloud auth application-default set-quota-project ...` # needed when switching projects
     - `gcloud auth application-default login`

2. **Service-specific API keys** (as needed):
   - VirusTotal API key for Google Threat Intelligence (as env var `VT_APIKEY`)
   - SOAR application key for SecOps SOAR (as env var `SOAR_APP_KEY`)
   - Chronicle customer ID (`CHRONICLE_CUSTOMER_ID`) and project ID (`CHRONICLE_PROJECT_ID`) for Chronicle SecOps.
     - `CHRONICLE_REGION` is also needed if not=`us`.

3. **An MCP client** such as:
   - [Claude Desktop](https://claude.ai/download)
   - [cline.bot](https://cline.bot/) [VS Code extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
   - [Google ADK(Agent Development Kit)](https://google.github.io/adk-docs/) based agent (a prebuilt one is provided)

4. **Python environment tools**:
   - `uv` - [The Python package installer and runner](https://docs.astral.sh/uv/) used to run the MCP servers with isolated environments
     - See [Installing uv](https://docs.astral.sh/uv/getting-started/installation/) on the [Astral docs site](https://docs.astral.sh/uv/) for official installation options (`curl -LsSf https://astral.sh/uv/install.sh | sh` on macOS/Linux or `irm https://astral.sh/uv/install.ps1 | iex` on Windows).
     - **Is uv from a virtual environment acceptable?** Yes, using `uv` from an existing virtual environment or pointing to a venv's Python binary works. However, installing `uv` standalone globally is strongly recommended because `uv run` handles per-server dependency isolation automatically without requiring you to manually create or manage virtual environments for each server.
     - **Is an absolute path to uv required?** In terminal shells, `uv` is typically found on your `PATH`. However, desktop GUI clients (Claude Desktop, Cursor, VS Code / Cline launched from desktop shortcuts or OS menus) often do **not** inherit interactive shell `PATH` exports (such as `~/.local/bin`). If your client reports `spawn uv ENOENT` or "command not found", you must specify the absolute path to `uv` (find it by running `which uv` in your terminal, e.g., `/Users/<username>/.local/bin/uv` or `/home/<username>/.local/bin/uv`).

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/google/mcp-security.git
cd mcp-security
```

No additional installation is needed as `uv` will handle dependencies when running the servers.

### Step 2: Configure Your MCP Client


#### For Prebuilt Google ADK Agent as a Client:

The repository provides a prebuilt Autonomous Security Operations Center (SOC) Agent powered by Google ADK v2.x and MCP in [`run-with-google-adk/`](../run-with-google-adk/README.md).

```bash
cd run-with-google-adk
cp sample.env .env

# Interactive terminal investigation REPL
uv run mcp-security-agent chat

# Web UI and Cloud Run API server
uv run mcp-security-agent serve --port 8080
```

For complete configuration and deployment details, see the [ADK Agent Guide](../run-with-google-adk/README.md).


#### For Claude Desktop:

1. Open Claude Desktop and select "Settings" from the Claude menu
2. Click on "Developer" in the lefthand bar, then click "Edit Config"
3. Add the MCP server configurations to your `claude_desktop_config.json` (see configuration reference below)
4. Save the file and restart Claude Desktop
5. Look for the hammer icon indicating the MCP servers are active

#### For cline.bot VS Code Extension:

1. Install the [cline.bot](https://cline.bot/) [extension in VS Code](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. Update your `cline_mcp_settings.json` with the appropriate configuration. See [sample on GitHub](https://github.com/google/mcp-security/blob/main/cline_mcp_settings.json.example)
3. Restart VS Code

### Step 3: Using the Tools

Once configured, you can interact with the MCP servers by asking Claude to perform specific security tasks:

- "Can you look up information about this IP address: 8.8.8.8"
- "Check if there are any recent security alerts in my Chronicle instance"
- "Search for threats related to ransomware in Google Threat Intelligence"
- "Find and remediate critical vulnerabilities in my GCP project"

## MCP Server Configuration Reference

Here's a complete reference configuration for all available MCP servers. However, we strongly recommend using environment variables instead of hardcoding sensitive information like API keys.

> [!IMPORTANT]
> **Key Configuration Details to Prevent Common Setup Errors:**
> 1. **Absolute path to `uv` for GUI clients:** Desktop applications like Claude Desktop, Cursor, or VS Code / Cline often fail to locate `uv` in your shell `PATH` (resulting in `spawn uv ENOENT`). Run `which uv` in your terminal and replace `"command": "uv"` with the full absolute path (e.g., `"/Users/yourusername/.local/bin/uv"` on macOS or `"/home/yourusername/.local/bin/uv"` on Linux).
> 2. **Directory paths and script entry points (Copy-Paste Trap):**
>    - **SecOps:** `--directory` points to `/path/to/the/repo/server/secops/secops_mcp` running `server.py`.
>    - **SecOps SOAR:** `--directory` points to `/path/to/the/repo/server/secops-soar/secops_soar_mcp` running `server.py`.
>    - **GTI:** `--directory` points to `/path/to/the/repo/server/gti/gti_mcp` running `server.py`.
>    - **SCC:** `--directory` points to `/path/to/the/repo/server/scc` running `scc_mcp.py` (**Notice:** `scc_mcp.py`, NOT `server.py`!).
>    - **Do NOT** set `--directory` to `/path/to/the/repo/server/` or omit the nested `_mcp` directory for SecOps/SOAR/GTI. Doing so causes `Failed to run 'server.py': No such file or directory`.
> 3. **SecOps SOAR CA Certificates:** For `secops-soar`, Python may need CA certificates bundled with `certifi`. On macOS, run `/Applications/Python\ 3.x/Install\ Certificates.command` (matching your Python version), or ensure `SSL_CERT_FILE` points to certifi's CA bundle.

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
      "env": {}
    }
  }
}
```

### Environment Variables: Inline `"env"` vs. `--env-file`

You can supply environment variables to MCP servers in one of two ways:

1. **Inline via `"env"` block (Standard MCP Client Config):**
   Set variables directly in your client's JSON configuration under `"env"`:
   ```json
   "env": {
     "CHRONICLE_PROJECT_ID": "your-project-id",
     "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
     "CHRONICLE_REGION": "us"
   }
   ```

2. **Via `.env` file using `uv run --env-file`:**
   Keep sensitive credentials in an `.env` file on disk rather than hardcoding them in the client JSON config.

> [!WARNING]
> **`--env-file` Flag Placement:**
> In `uv`, `--env-file` is a flag for the `run` command. It must be placed **after** `run` in the `args` array:
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
> **Syntax Error:** Putting `--env-file` before `run` (e.g., `uv --env-file ... run`) is invalid syntax and `uv` will exit with an unrecognized option error. Alternatively, you can set the environment variable `UV_ENV_FILE=/path/to/.env` in your system environment.

### Setting Up Environment Variables

#### For macOS/Linux:

Add these lines to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file:

```bash
# Google Security Operations (Chronicle)
export CHRONICLE_PROJECT_ID="your-google-cloud-project-id"
export CHRONICLE_CUSTOMER_ID="your-chronicle-customer-id"
export CHRONICLE_REGION="us"

# SOAR
export SOAR_URL="your-soar-url"
export SOAR_APP_KEY="your-soar-app-key"
export SOAR_INTEGRATIONS="ServiceNow,CSV,Siemplify"

# Google Threat Intelligence
export VT_APIKEY="your-vt-api-key"
```

Then restart your terminal, restart VS Code, or run `source ~/.bashrc` (or equivalent).

#### For Windows:

Set environment variables using the System Properties dialog:

1. Search for "environment variables" in the Start menu
2. Click "Edit the system environment variables"
3. Click the "Environment Variables" button
4. Add new variables with the appropriate names and values

Or set them via PowerShell:

```powershell
$Env:CHRONICLE_PROJECT_ID = "your-google-cloud-project-id"
$Env:CHRONICLE_CUSTOMER_ID = "your-chronicle-customer-id"
$Env:CHRONICLE_REGION = "us"
$Env:SOAR_URL = "your-soar-url"
$Env:SOAR_APP_KEY = "your-soar-app-key"
$Env:VT_APIKEY = "your-vt-api-key"
```

## Usage Examples

### Google Threat Intelligence (GTI)

```
Can you search for information about the Emotet malware family?
```

The LLM will use the GTI server to search for and retrieve information about the Emotet malware family, including related IoCs, campaigns, and threat actor information.

### Chronicle Security Operations (SecOps)

```
Can you look for security events related to suspicious PowerShell usage in the last 24 hours?
```

The LLM will use the Chronicle SecOps server to search for security events matching this description and present the findings.

### SecOps SOAR

```
Can you list open security cases and show me details about the highest priority one?
```

The LLM will use the SecOps SOAR server to list open cases and provide details about the highest priority case.

For details on configuring and using specific SOAR integrations, refer to the [SOAR Integrations documentation](./soar_integrations/index.md).

### Security Command Center (SCC)

```
What are the top critical vulnerabilities in my GCP project 'my-project-id'?
```

The LLM will use the SCC server to list high-priority vulnerabilities and provide remediation guidance.

## Troubleshooting

If you encounter issues with the MCP servers, review the common setup friction points below:

### 1. Desktop Client Cannot Find `uv` (`spawn uv ENOENT` or "Command not found")

**Symptom:**
When starting Claude Desktop, Cursor, or VS Code, the client console or logs report `spawn uv ENOENT` or indicates that the `uv` executable cannot be found.

**Cause:**
Desktop GUI applications launched from the macOS Dock, Spotlight, or Linux desktop managers do not run inside an interactive login shell. Therefore, they do not inherit `PATH` modifications added to `~/.bashrc`, `~/.zshrc`, or `~/.profile` (such as `~/.local/bin`).

**Solution:**
1. In your terminal, find the full absolute path to `uv`:
   ```bash
   which uv
   # macOS/Linux output example: /Users/username/.local/bin/uv or /usr/local/bin/uv
   # Windows PowerShell: (Get-Command uv).Source
   ```
2. Replace `"command": "uv"` with the absolute path in your client configuration JSON:
   ```json
   "command": "/Users/username/.local/bin/uv"
   ```

### 2. Script or Directory Not Found: Common Path & Copy-Paste Gotchas

**Symptom:**
The server fails to start with errors such as:
- `error: Failed to run 'server.py': No such file or directory`
- `error: Failed to run 'scc_mcp.py': No such file or directory`

**Causes & Solutions:**
- **The SCC Copy-Paste Trap:** SecOps, SecOps SOAR, and GTI all run `server.py` from their nested package directory. SCC runs `scc_mcp.py` directly from `server/scc/`. If you copy-pasted the `secops` block for SCC, verify that the last argument is `"scc_mcp.py"`, **not** `"server.py"`.
- **Wrong `--directory` Depth:**
  - `secops`: must point to `<repo>/server/secops/secops_mcp`
  - `secops-soar`: must point to `<repo>/server/secops-soar/secops_soar_mcp`
  - `gti`: must point to `<repo>/server/gti/gti_mcp`
  - `scc`: must point to `<repo>/server/scc`
  - **Do NOT** set `--directory` to `<repo>/server/` or `<repo>/server/secops` (missing the inner `secops_mcp/`).

### 3. SecOps SOAR: SSL Certificate Verification & `certifi`

**Symptom:**
SecOps SOAR client fails with SSL certificate verification errors (e.g. `[SSL: CERTIFICATE_VERIFY_FAILED]` or certificate authority unknown) when connecting to the SOAR instance.

**Cause:**
On macOS, Python installations often do not use the system keychain root certificates by default, requiring certificates from the `certifi` package to be installed.

**Solution:**
1. Run the Python certificate installation script for your installed Python version:
   ```bash
   /Applications/Python\ 3.12/Install\ Certificates.command
   # or Python 3.11:
   /Applications/Python\ 3.11/Install\ Certificates.command
   ```
2. Alternatively, configure the `SSL_CERT_FILE` environment variable to point to the `certifi` bundle:
   ```bash
   export SSL_CERT_FILE=$(python3 -m certifi)
   ```
   Or add `SSL_CERT_FILE` directly inside the `"env"` object of your MCP client settings for `secops-soar`.

### 4. SecOps SOAR: Finding the Correct `SOAR_URL`

If the SecOps SOAR server starts and then shuts down with an error like this:

```text
Error: Failed to fetch valid scopes from SOAR, please make sure you have configured the right SOAR credentials. Shutting down...
MCP error -32000: Connection closed
```

check that `SOAR_URL` is set to your Google SecOps SOAR base URL, not your Backstory URL. The SOAR APIs used by this server are specific to the SOAR platform, so they are not listed in a Backstory tenant's Swagger documentation.

If you are not sure which URL to use, try one of these options:

1. In Google SecOps SOAR, go to **Settings > Webhooks**, create a new webhook with any parameters, and copy the base URL from the generated webhook URL. For example: `https://s4i0z.siemplify-soar.com`.
2. Open your browser developer tools, go to the **Network** tab, and navigate to **Cases** in the SOAR UI. Look for a request such as `GetCaseCardsByRequest`, open the **Headers** tab, and copy the base URL from that request. For example: `https://s4i0z.siemplify-soar.com`.

After updating `SOAR_URL`, restart your MCP client so it picks up the new environment variable.

### 5. Flag Placement Errors with `--env-file`

**Symptom:**
`uv` rejects the command line with an error about unrecognized or misplaced options.

**Solution:**
Ensure `--env-file` is placed **after** `run` in the `args` array:
```json
"args": [
  "--directory",
  "/path/to/server/secops/secops_mcp",
  "run",
  "--env-file",
  "/path/to/.env",
  "server.py"
]
```

### 6. Fallback: Bypassing `uv` Using `/bin/bash`

If you are in an environment where desktop clients cannot find `uv` or you prefer to use a standard Python virtual environment, you can bypass `uv` and execute via `/bin/bash -c`:

```json
{
  "mcpServers": {
    "secops": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/repo/server/secops && pip install -e . && secops_mcp"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "01234567-abcd-4321-1234-0123456789ab",
        "CHRONICLE_REGION": "us"
      }
    }
  }
}
```
Alternatively, if you already have a virtual environment created:
```json
"args": [
  "-c",
  "source /path/to/repo/.venv/bin/activate && cd /path/to/repo/server/secops/secops_mcp && python server.py"
]
```
