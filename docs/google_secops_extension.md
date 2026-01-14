# Google SecOps Extension

This folder contains the **Google SecOps Extension**, providing specialized skills for security operations.

## Overview

The extension `extensions/google-secops` packages setup and key security workflows into [skills](https://agentskills.io/specification). 

The skills are designed to work seamlessly with:
 * [Gemini CLI](https://geminicli.com) and the Google SecOps Remote MCP Server.
 * [Antigravity](https://antigravity.google/docs/skills)
    
The (`.agent`) symlink makes them available as [Antigravity Agent Skills](https://antigravity.google/docs/skills) at the workspace level. You could also install/copy/symlink the skills to `~/.gemini/antigravity/skills/` to make them available globally to all workspaces.


## Prerequisites

1.  **Install Gemini CLI (Preview)**:
    ```bash
    npm install -g @google/gemini-cli@preview
    ```

2.  **Enable Skills**: Ensure your `~/.gemini/settings.json` has `experimental.skills` enabled:
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
        "skills": true
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

## Available Skills

### 1. Setup Assistant (Gemini CLI) (`secops-setup-gemini-cli`)
*   **Trigger**: "Help me set up the Gemini CLI", "Configure Gemini CLI for SecOps".
*   **Function**: checks for `uv` and Google Cloud authentication, then guides you to add the correct `secops-hosted-mcp` configuration to your Gemini settings (`~/.gemini/config.json`).

### 2. Setup Assistant (Antigravity) (`secops-setup-antigravity`)
*   **Trigger**: "Help me set up Antigravity", "Configure Antigravity for SecOps".
*   **Function**: checks for Google Cloud authentication and environment variables, then merges the correct `remote-secops-investigate` and `remote-secops-admin` configuration into your Antigravity settings (`~/.gemini/antigravity/mcp_config.json`).

### 3. Alert Triage (`secops-triage`)
*   **Trigger**: "Triage alert [ID]", "Analyze case [ID]".
*   **Function**: Orchestrates a Tier 1 triage workflow by following the `triage_alerts.md` runbook. It checks for duplicates, enriches entities, and provides a classification recommendation (FP/TP).

### 4. Investigation (`secops-investigate`)
*   **Trigger**: "Investigate case [ID]", "Deep dive on [Entity]".
*   **Function**: Guides deep-dive investigations using specialized runbooks (e.g., Lateral Movement, Malware).

### 5. Threat Hunting (`secops-hunt`)
*   **Trigger**: "Hunt for [Threat]", "Search for TTP [ID]".
*   **Function**: Assists in proactive threat hunting by generating hypotheses and constructing complex UDM queries for Chronicle.

## How it Works

These skills act as **Driver Agents** that:
1.  **Read** the standardized Runbooks in `rules_bank/run_books/`.
2.  **Execute** the steps using the available MCP tools (`secops`, `gti`, `secops-soar`).
3.  **Standardize** the output according to SOC best practices.


## Cross-Compatibility

These skills are designed to be compatible with **Claude Code** and other AI agents. The `slash_command` and `personas` metadata in the YAML frontmatter allow other tools to index and trigger these skills effectively.

*   `slash_command`: Defines the equivalent command pattern (e.g., `/security:triage`).
*   `personas`: detailed which security personas (e.g., `threat_hunter`) are best suited for the task.
