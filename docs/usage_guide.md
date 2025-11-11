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
   - `uv` - [The Python package installer](https://docs.astral.sh/uv/) used to run the MCP servers with isolated environments
     - See [Installing uv](https://docs.astral.sh/uv/getting-started/installation/) on the [Astral docs site](https://docs.astral.sh/uv/)

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/google/mcp-security.git
cd mcp-security
```

No additional installation is needed as `uv` will handle dependencies when running the servers.

### Step 2: Configure Your MCP Client


#### For Prebuilt Google ADK Agent as a client:

Detailed instructions are provided [here](https://github.com/google/mcp-security/#using-the-prebuilt-google-adk-agent-as-client)


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

Here's a complete reference configuration for all available MCP servers. However, we strongly recommend using environment variables instead of hardcoding sensitive information like API keys:

**NOTE:** For OSX users, if you used [this one-liner](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to install uv, use the full path to the uv binary for the "command" value below, as uv will not be placed in the system path for Claude to use! For example: `/Users/yourusername/.local/bin/uv` instead of just `uv`.

Additionally, for the secops-soar MCP server, you will need use the CA list bundled with the certifi package. This can be done via the following command. Change the Python minor version to match whatever version you are currently running. (ex. `Python\ 3.11`):
`/Applications/Python\ 3.12/Install\ Certificates.command`

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
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Using .env and Env Vars

`uv` supports passing an `.env` file like so:
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

The `--env-file` option in the configuration allows `uv` to use a .env file for environment variables. Make sure to create this file with your sensitive information, or use system environment variables as described below.

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

You can enable or disable individual servers by setting `"disabled": true` for specific servers.

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

If you encounter issues with the MCP servers:

1. **Check authentication**: Ensure your Google Cloud credentials are properly set up
2. **Verify API keys**: Make sure all required API keys are correctly configured
3. **Check server logs**: Look for error messages in the server output
4. **Restart the client**: Sometimes restarting the LLM Desktop or VS Code can resolve connection issues
5. **Verify uv installation**: Ensure that `uv` is properly installed and accessible in your PATH
