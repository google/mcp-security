# Runbook: SOC Analyst Standard Workflow Guide

## Objective

To serve as a central **navigational guide** for Security Operations Center (SOC) Analysts (primarily Tier 1 and Tier 2), outlining the standard high-level workflow for handling incoming alerts and cases. This runbook directs analysts to the appropriate detailed runbooks for specific tasks like triage, enrichment, investigation, and closure.

## Scope

Provides a high-level overview of the standard alert/case handling process. It links to specific, detailed runbooks for execution steps. It does **not** contain the detailed execution steps itself but acts as a starting point and process map.

## Inputs

*   Typically none directly needed to consult this guide. The starting point is usually a new alert or assigned case in the SOAR platform.

## Tools

This guide references workflows that utilize tools across the security stack, primarily:
*   `secops-soar` (Case Management, Basic Actions)
*   `secops-mcp` (SIEM Lookups, Event Search)
*   `gti-mcp` (Threat Intelligence Enrichment)

## Workflow Steps & Diagram

The standard workflow generally follows these phases. Refer to the linked runbooks for detailed steps and tool usage.

1.  **Monitor & Assign:** Regularly check the SOAR platform (`secops-soar.list_cases`) for new or assigned alerts/cases.
2.  **Initial Triage & Context:** Assess alert severity, type, and gather initial case details (`secops-soar.get_case_full_details`). **Decision Point:** Is this potentially a duplicate?
    *   Refer to: `.clinerules/run_books/triage_alerts.md`
    *   Refer to: `.clinerules/run_books/common_steps/check_duplicate_cases.md`
3.  **Basic Enrichment:** Gather initial context on key Indicators of Compromise (IOCs) identified in the alert/case.
    *   Refer to: `.clinerules/run_books/basic_ioc_enrichment.md`
4.  **Assess & Investigate:** Based on triage and enrichment, determine the nature of the alert. **Decision Point:** Is this a False Positive (FP), Benign True Positive (BTP), or does it require further investigation (True Positive/Suspicious)?
    *   **If FP/BTP:** Proceed to Step 6 (Documentation & Closure).
    *   **If TP/Suspicious:** Proceed to Step 5 (Specific Investigation).
5.  **Specific Investigation (Tier 1/2):** Follow dedicated runbooks based on the alert type or findings. Examples:
    *   Suspicious Login: `.clinerules/run_books/suspicious_login_triage.md`
    *   Phishing Report: `.clinerules/run_books/irps/phishing_response.md` (Initial steps)
    *   Malware Alert: `.clinerules/run_books/malware_triage.md`
    *   IOC Investigation: `.clinerules/run_books/deep_dive_ioc_analysis.md` (Tier 2+)
    *   Timeline Analysis: `.clinerules/run_books/case_event_timeline_and_process_analysis.md` (Tier 2+)
6.  **Documentation:** Document all findings, analysis steps, and conclusions clearly in the SOAR case (`secops-soar.post_case_comment`).
    *   Refer to guidelines: `.clinerules/run_books/guidelines/report_writing.md`
7.  **Escalation or Closure:** **Decision Point:** Based on the full investigation, should the case be escalated or closed?
    *   **Escalate:** Assign the case to Tier 2/3 or a specialized team (e.g., IR, Forensics) with a summary of findings.
    *   **Close:** If determined to be FP, BTP, or fully resolved at the current tier.
        *   Refer to: `.clinerules/run_books/common_steps/close_soar_artifact.md`

```{mermaid}
sequenceDiagram
    participant Analyst
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as gti-mcp
    participant Runbooks as .clinerules/run_books/

    Analyst->>SOAR: 1. Monitor Alert Queue (list_cases)
    SOAR-->>Analyst: New/Assigned Alerts/Cases
    Analyst->>Runbooks: 2. Consult triage_alerts.md / check_duplicate_cases.md
    Analyst->>SOAR: Get Case/Alert Details (get_case_full_details, list_alerts_by_case)
    SOAR-->>Analyst: Details (IOCs: I1, I2...)
    Analyst->>Runbooks: 3. Consult basic_ioc_enrichment.md
    loop For each Key IOC Ii
        Analyst->>SIEM: lookup_entity(entity_value=Ii)
        SIEM-->>Analyst: SIEM Context
        Analyst->>GTI: get...report(ioc=Ii)
        GTI-->>Analyst: GTI Context
    end
    Note over Analyst: 4. Assess: FP/BTP or Investigate Further?
    alt FP/BTP
         Analyst->>Runbooks: 6. Consult report_writing.md guidelines
         Analyst->>SOAR: Document Findings (post_case_comment)
         Analyst->>Runbooks: 7. Consult close_soar_artifact.md
         Analyst->>SOAR: Close Case/Alert
    else Investigate Further (TP/Suspicious)
        Analyst->>Runbooks: 5. Consult specific runbook (e.g., malware_triage.md)
        Note over Analyst: Follow specific runbook steps...
        Analyst->>Runbooks: 6. Consult report_writing.md guidelines
        Analyst->>SOAR: Document Findings (post_case_comment)
        Note over Analyst: 7. Decision: Escalate or Close?
        alt Escalate
            Analyst->>SOAR: Assign Case to Tier 2/3
        else Close (Resolved)
            Analyst->>Runbooks: Consult close_soar_artifact.md
            Analyst->>SOAR: Close Case/Alert
        end
    end

```

## Common Scenario Entry Points

*   **Phishing Report:** Start with `triage_alerts.md`, then proceed to `.clinerules/run_books/irps/phishing_response.md`.
*   **Malware Alert (Hash Provided):** Start with `triage_alerts.md`, then proceed to `.clinerules/run_books/malware_triage.md`.
*   **Suspicious Login Alert:** Start with `triage_alerts.md`, then proceed to `.clinerules/run_books/suspicious_login_triage.md`.
*   **General IOC Investigation:** Start with `triage_alerts.md`, then `basic_ioc_enrichment.md`, potentially followed by `deep_dive_ioc_analysis.md`.

## Completion Criteria

The analyst has successfully navigated the standard workflow using this guide, consulted the appropriate detailed runbooks, and reached a documented decision point (closure or escalation) for the alert/case being handled.
