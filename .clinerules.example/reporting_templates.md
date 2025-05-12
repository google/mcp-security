# Reporting Templates & Guidelines

This file outlines standard formats and required elements for common reports generated during security operations.

## General Report Metadata Requirements

*   **Runbook Reference:** All reports generated via runbook execution **must** clearly state which runbook was used at the beginning of the report.
    *   *Example:* `**Runbook Used:** Alert Investigation Summary Report Runbook`
*   **Timestamp:** Include a generation timestamp in a consistent format (e.g., YYYY-MM-DD HH:MM Timezone).
*   **Case ID:** Reference the relevant SOAR Case ID(s).
*   **Workflow Diagram:** Include a Mermaid sequence diagram from the executed runbook, showing the actual MCP Servers and Tools used.

## Common Report Types (Placeholders - To be defined)

### Daily SOC Summary

*   *(Define required sections, e.g., Key Metrics, Notable Alerts, Ongoing Incidents, Shift Handover Notes)*

### Post-Incident Report

*   *(Define required sections, e.g., Executive Summary, Incident Timeline, Root Cause Analysis, Impact Assessment, Actions Taken, Lessons Learned, Recommendations)*

### Threat Hunt Summary Report

*   *(Define required sections, e.g., Hunt Hypothesis, Scope, Timeframe, Queries Used, Findings (Positive/Negative), Enrichment Details, Recommendations/Escalation)*

### Vulnerability Triage Report

*   *(Define required sections, e.g., Vulnerability Details (CVE), Affected Assets, GTI/SIEM Context, Remediation Steps, Prioritization)*

*(Add other relevant report templates as needed)*
