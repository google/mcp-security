# Runbook Guidelines

This document provides general guidelines for creating, maintaining, and executing runbooks within this security environment.

## General Principles

*   **Clarity:** Runbooks should be clear, concise, and easy to follow, even under pressure.
*   **Accuracy:** Ensure tool commands, parameters, and expected outcomes are accurate and up-to-date.
*   **Consistency:** Use consistent formatting, terminology, and structure across all runbooks.
*   **Actionability:** Focus on concrete steps and decisions analysts need to make.

## Structure

Runbooks should generally include the following sections:

*   **Objective:** What is the goal of this runbook?
*   **Scope:** What is included and excluded from this procedure?
*   **Inputs:** What information is required to start the runbook (e.g., Case ID, IOC value, User ID)? Use `${VARIABLE_NAME}` format.
*   **Tools:** List the primary MCP tools required.
*   **Workflow Steps & Diagram:** Detail the sequence of actions. **Must** include a Mermaid sequence diagram visualizing the workflow that was *actually* performed, clearly showing interactions between the Analyst/Agent, MCP Servers (e.g., `secops-soar`, `gti-mcp`), and the specific MCP tools used (e.g., `list_cases`, `get_file_report`).
*   **Completion Criteria:** How is the successful completion of the runbook determined?

## Reporting Requirements

*   **Runbook Reference:** If a runbook execution results in a generated report (e.g., investigation summary, triage report), the report **must** clearly state which runbook was used at the beginning of the report.
    *   *Example:* `**Runbook Used:** Alert Investigation Summary Report Runbook`

## Maintenance

*   Runbooks should be reviewed periodically (e.g., quarterly) to ensure they remain accurate and relevant.
*   Update runbooks promptly when tools, procedures, or configurations change.

*(Add other specific guidelines as needed)*
