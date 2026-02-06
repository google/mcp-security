# Google SecOps Extension

This folder contains the **Google SecOps Extension**, providing specialized skills for security operations.

## Overview

The extension `extensions/google-secops` packages setup and key security workflows into [skills](https://agentskills.io/specification). 

These skills are **Adaptive**, designed to work seamlessly with:
 *   [Google SecOps Remote MCP Server](https://google.github.io/mcp-security/docs/remote_server.html) (Preferred)
 *   **Local Python Tools** (Fallback)

This allows the skills to function in diverse environments, automatically selecting the best available tool for the job.
    
The (`.agent`) symlink makes them available as [Antigravity Agent Skills](https://antigravity.google/docs/skills) at the workspace level. You could also install/copy/symlink the skills to `~/.gemini/antigravity/skills/` to make them available globally to all workspaces.


## Prerequisites

1.  **Install Gemini CLI (Preview)**:
    ```bash
    npm install -g @google/gemini-cli@preview
    ```


2.  **GUI Login Requirement**: You MUST have logged into the Google SecOps GUI at least once before using the API/MCP server.

3.  **Enable Skills**: Ensure your `~/.gemini/settings.json` has `experimental.skills` enabled:
    ```json
    {
      "security": {
        "auth": {
          "selectedType": "gemini-api-key"
        }
      },
      "general": {
        "previewFeatures": true
      },
      "experimental": {
        "skills": true,
        "extensionConfig": true
      }
    }
    ```

Verify skills are enabled from the Gemini CLI prompt:
```
/skills list
```

## Installation

To install this extension in your Gemini CLI environment:

1.  **Navigate** to the project root.
2.  **Run**:
    ```bash
    gemini extensions install ./extensions/google-secops
    ```

You will be prompted for environment variables for the MCP configuration:

1. `PROJECT_ID` (GCP Project ID on your SecOps tenant's /settings/profile page)
2. `CUSTOMER_ID` (Your Chronicle Customer UUID)
3. `REGION` (Your Chronicle Region, e.g., `us`, `europe-west1`)
4. `SERVER_URL` (e.g. https://chronicle.northamerica-northeast2.rep.googleapis.com/mcp, https://chronicle.us.rep.googleapis.com/mcp, etc.)

> **Note**: These values are persisted in `~/.gemini/extensions/google-secops/.env` and can be referenced by skills. Also, you can change the values in this file if needed.

When using the secops-hosted-mcp MCP Server, use these parameters from the `.env` file (located at `~/.gemini/extensions/google-secops/.env`) for EVERY request:
Customer ID: ${CUSTOMER_ID}
Region: ${REGION}
Project ID: ${PROJECT_ID}

## Available Skills


### 1. Setup Assistant (Antigravity) (`secops-setup-antigravity`)
*   **Trigger**: "Help me set up Antigravity", "Configure Antigravity for SecOps".
*   **Function**: checks for Google Cloud authentication and environment variables, then merges the correct `remote-secops-investigate` and `remote-secops-admin` configuration into your Antigravity settings (`~/.gemini/antigravity/mcp_config.json`).

### 2. Alert Triage (`secops-triage`)
*   **Trigger**: "Triage alert [ID]", "Analyze case [ID]".
*   **Function**: Orchestrates a Tier 1 triage workflow by following the `triage_alerts.md` runbook. It checks for duplicates, enriches entities, and provides a classification recommendation (FP/TP).

### 3. Investigation (`secops-investigate`)
*   **Trigger**: "Investigate case [ID]", "Deep dive on [Entity]".
*   **Function**: Guides deep-dive investigations using specialized runbooks (e.g., Lateral Movement, Malware).

### 4. Threat Hunting (`secops-hunt`)
*   **Trigger**: "Hunt for [Threat]", "Search for TTP [ID]".
*   **Function**: Assists in proactive threat hunting by generating hypotheses and constructing complex UDM queries for Chronicle.

### 5. Cases (`secops-cases`)
*   **Trigger**: "List cases", "Show recent cases", "/secops:cases".
*   **Function**: Lists recent SOAR cases to verify connectivity and view case status.

## Custom Commands

You can use the following slash commands as shortcuts for common tasks:

*   `/secops:triage <ALERT_ID>`: Quickly start triaging an alert.
*   `/secops:investigate <CASE_ID>`: Start an investigation.
*   `/secops:hunt <THREAT>`: Start a threat hunt.
*   `/secops:cases`: List recent cases.

## How it Works

These skills act as **Driver Agents** that:
1.  **Read** the standardized Runbooks in `rules_bank/run_books/`.
2.  **Execute** the steps using the available MCP tools.
3.  **Standardize** the output according to SOC best practices.

### Tool Selection

The skills employ an **Adaptive Execution** strategy to ensure robustness:

1.  **Check Environment**: The skill first identifies which tools are available in the current workspace.
2.  **Prioritize Remote**: If the **Remote MCP Server** is connected, the skill uses remote tools (e.g., `list_cases`, `udm_search`) for maximum capability.
3.  **Fallback to Local**: If remote tools are unavailable, the skill attempts to use **Local Python Tools**.
    > **Note**: Local tools are not included in this extension release. To use them, you must clone the [Google SecOps MCP Repository](https://github.com/google/mcp-security) and configure the local server separately.

For a detailed mapping of Remote vs. Local capabilities, see [`TOOL_MAPPING.md`](https://github.com/google/mcp-security/blob/main/extensions/google-secops/TOOL_MAPPING.md).


## Cross-Compatibility

These skills are designed to be compatible with **Claude Code** and other AI agents. The `slash_command` and `personas` metadata in the YAML frontmatter allow other tools to index and trigger these skills effectively.

*   `slash_command`: Defines the equivalent command pattern (e.g., `/security:triage`).
*   `personas`: detailed which security personas (e.g., `threat_hunter`) are best suited for the task.


## Known Issues
* If the `SERVER_URL` requires regionalization (i.e. LEP vs REP vs MREP), it can be very difficult for the user to know what value to use.

Documentation says:
> Server URL or Endpoint: Select the regional endpoint and add /mcp at the end. For example, https://chronicle.us.rep.googleapis.com/mcp

Known-good values for Regional Endpoints (REP):
* https://chronicle.us-east1.rep.googleapis.com/mcp
* https://chronicle.africa-south1.rep.googleapis.com/mcp
* https://chronicle.asia-northeast1.rep.googleapis.com/mcp
* https://chronicle.me-central1.rep.googleapis.com/mcp
* https://chronicle.europe-west1.rep.googleapis.com/mcp
* https://chronicle.northamerica-northeast2.rep.googleapis.com/mcp
* https://chronicle.southamerica-east1.rep.googleapis.com/mcp
* https://chronicle.europe-west2.rep.googleapis.com/mcp
* ...

Known-good values for Multi-Regional Endpoints (MREP):
* https://chronicle.us.rep.googleapis.com/mcp


## References
* [Agent Skills Specification](https://agentskills.io/specification)
* [Gemini CLI Documentation](https://geminicli.com)
* [Gemini CLI Preview Features](https://geminicli.com/docs/settings/general#previewfeatures)
* [Antigravity Skills](https://antigravity.google/docs/skills)
* [Use the Google SecOps MCP server](https://docs.cloud.google.com/chronicle/docs/secops/use-google-secops-mcp)
* [Chronicle API - Regional service endpoint](https://docs.cloud.google.com/chronicle/docs/reference/rest?rep_location=us)