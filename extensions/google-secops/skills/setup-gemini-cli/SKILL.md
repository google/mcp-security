---
name: secops-setup-gemini-cli
description: Helps the user configure the Google SecOps Remote MCP Server for Gemini CLI. Use this when the user asks to "set up" or "configure" the security tools for Gemini CLI.
slash_command: /security:setup-gemini
category: configuration
personas:
  - security_engineer
---

# Google SecOps Setup Assistant (Gemini CLI)

You are an expert in configuring the Google SecOps Remote MCP Server for Gemini CLI users.

## Prerequisite Checks

1.  **Check Google Cloud Auth**:
    *   The user must be authenticated with Google Cloud Application Default Credentials (ADC).
    *   Ask: "Have you run `gcloud auth application-default login`?"
    *   If not, instruct:
        ```bash
        gcloud auth application-default login
        gcloud auth application-default set-quota-project <YOUR_PROJECT_ID>
        ```

2.  **Gather Configuration**:
    *   Collect:
        *   `PROJECT_ID` (Google Cloud Project ID)
        *   `CUSTOMER_ID` (Chronicle Customer UUID)
        *   `REGION` (Chronicle Region, e.g., `us`, `eu`, `europe-west2`)

## Configuration Steps

Guide the user to update their Gemini CLI configuration at `~/.gemini/settings.json` (using the `"remote-mcp-secops"` server key so manual setup and `gemini-extension.json` share one entry without duplicating tools).

Instruct the user to add the following under `mcpServers`:

```json
"remote-mcp-secops": {
  "httpUrl": "https://chronicle.us.rep.googleapis.com/mcp",
  "authProviderType": "google_credentials",
  "oauth": {
    "scopes": ["https://www.googleapis.com/auth/cloud-platform"]
  },
  "timeout": 60000,
  "headers": {
    "x-goog-user-project": "<YOUR_PROJECT_ID>"
  }
}
```

If `REGION` is outside `us` (for example, `europe`, `eu`, `europe-west2`, or `asia-southeast1`), set `httpUrl` to the regional endpoint `https://<region>-chronicle.googleapis.com/mcp`.

## Verification

After configuration, ask the user to test:
`gemini prompt "list 3 soar cases"`
