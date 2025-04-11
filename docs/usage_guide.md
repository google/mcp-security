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

## Getting Started

### Step 1: Install the MCP Servers

Clone this repository and ensure you have the required Python dependencies installed:

```bash
git clone https://github.com/your-org/mcp-security.git
cd mcp-security
python -m pip install -e .
```

### Step 2: Configure Your MCP Client

#### For Claude Desktop:

1. Open Claude Desktop and select "Settings" from the Claude menu
2. Click on "Developer" in the lefthand bar, then click "Edit Config"
3. Add the MCP server configurations to your `claude_desktop_config.json` (see below)
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

Here's a complete reference configuration for all available MCP servers:

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
        "secops_soar_mcp.py",
        "--integrations",
        "ServiceNow,CSV,Siemplify"
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

You can enable or disable individual servers by setting `"disabled": true` for specific servers.

## Usage Examples

### Google Threat Intelligence (GTI)

```
Can you search for information about the Emotet malware family?
```

Claude will use the GTI server to search for and retrieve information about the Emotet malware family, including related IoCs, campaigns, and threat actor information.

### Chronicle Security Operations (SecOps)

```
Can you look for security events related to suspicious PowerShell usage in the last 24 hours?
```

Claude will use the Chronicle SecOps server to search for security events matching this description and present the findings.

### SecOps SOAR

```
Can you list open security cases and show me details about the highest priority one?
```

Claude will use the SecOps SOAR server to list open cases and provide details about the highest priority case.

### Security Command Center (SCC)

```
What are the top critical vulnerabilities in my GCP project 'my-project-id'?
```

Claude will use the SCC server to list high-priority vulnerabilities and provide remediation guidance.

## Troubleshooting

If you encounter issues with the MCP servers:

1. **Check authentication**: Ensure your Google Cloud credentials are properly set up
2. **Verify API keys**: Make sure all required API keys are correctly configured
3. **Check server logs**: Look for error messages in the server output
4. **Restart the client**: Sometimes restarting Claude Desktop or VS Code can resolve connection issues
5. **Update dependencies**: Make sure you have the latest version of the MCP server code and dependencies 