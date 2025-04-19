# Using the Google Security MCP Servers

This guide will help you get started with using the MCP servers to access Google's security products and services from Claude Desktop or other MCP-compatible clients.

## Prerequisites

Before you begin, make sure you have:

1. **Google Cloud Authentication** set up using one of these methods:
   - Application Default Credentials (ADC)
   - GOOGLE_APPLICATION_CREDENTIALS environment variable
   - `gcloud auth application-default login`

2. **Service-specific API keys** (as needed):
   - VirusTotal API key for Google Threat Intelligence
   - SOAR application key for SecOps SOAR
   - Chronicle customer ID and project ID for Chronicle SecOps

3. **An MCP client** such as:
   - Claude Desktop
   - cline.bot VS Code extension

4. **Python environment tools**:
   - `uv` - The Python package installer used to run the MCP servers with isolated environments

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-org/mcp-security.git
cd mcp-security
```

No additional installation is needed as `uv` will handle dependencies when running the servers.

### Step 2: Configure Your MCP Client

#### For Claude Desktop:

1. Open Claude Desktop and select "Settings" from the Claude menu
2. Click on "Developer" in the lefthand bar, then click "Edit Config"
3. Add the MCP server configurations to your `claude_desktop_config.json` (see configuration reference below)
4. Save the file and restart Claude Desktop
5. Look for the hammer icon indicating the MCP servers are active

#### For cline.bot VS Code Extension:

1. Install the cline.bot extension in VS Code
2. Update your `cline_mcp_settings.json` with the appropriate configuration
3. Restart VS Code

### Step 3: Using the Tools

Once configured, you can interact with the MCP servers by asking Claude to perform specific security tasks:

- "Can you look up information about this IP address: 8.8.8.8"
- "Check if there are any recent security alerts in my Chronicle instance"
- "Search for threats related to ransomware in Google Threat Intelligence"
- "Find and remediate critical vulnerabilities in my GCP project"

## MCP Server Configuration Reference

Here's a complete reference configuration for all available MCP servers. We strongly recommend using environment variables instead of hardcoding sensitive information like API keys:

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
    },
    "secops-soar": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/secops-soar",
        "run",
        "secops_soar_mcp.py",
        "--integrations",
        "${SOAR_INTEGRATIONS}"
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
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/gti/gti_mcp",
        "run",
        "server.py"
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
        "--env-file=/path/to/your/env",
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

Then restart your terminal or run `source ~/.bashrc` (or equivalent).

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