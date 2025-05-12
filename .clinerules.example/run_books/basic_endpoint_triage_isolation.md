# Basic Endpoint Triage & Isolation Runbook

## Objective

Perform initial triage on a potentially compromised endpoint identified during an investigation, gather context from SIEM and other available tools (Vulnerability Management, EDR), and isolate the endpoint if necessary and confirmed.

## Scope

This runbook covers the initial assessment and potential network isolation of an endpoint. It does not cover deep forensic analysis or malware removal, which would typically follow in a more detailed incident response process.

## Inputs

*   `${ENDPOINT_ID}`: The identifier of the potentially compromised endpoint (e.g., hostname, IP address).
*   `${ENDPOINT_TYPE}`: The type of identifier provided (e.g., "Hostname", "IP Address").
*   `${CASE_ID}`: The relevant SOAR case ID for documentation.
*   `${ALERT_GROUP_IDENTIFIERS}`: Relevant alert group identifiers from the SOAR case.
*   *(Optional) `${REASON_FOR_TRIAGE}`: Brief description why this endpoint is being triaged.*

## Tools

*   `secops-mcp`: `search_security_events`, `lookup_entity`
*   `secops-soar`: `post_case_comment`, `get_case_full_details`
*   `scc-mcp`: `top_vulnerability_findings` (if cloud resource), `get_finding_remediation`
*   *(Potentially EDR tools if available via MCP: e.g., get_endpoint_details, isolate_endpoint)*
*   *(Potentially Vulnerability Scanner tools if available via MCP)*
*   `ask_followup_question` (To confirm isolation)

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${ENDPOINT_ID}`, `${ENDPOINT_TYPE}`, `${CASE_ID}`, `${ALERT_GROUP_IDENTIFIERS}`, and optionally `${REASON_FOR_TRIAGE}`.
2.  **Gather Initial Context:**
    *   Retrieve full case details using `secops-soar.get_case_full_details` for `${CASE_ID}`.
    *   Use `secops-mcp.lookup_entity` for `${ENDPOINT_ID}` to get a SIEM activity summary.
3.  **Check Endpoint Posture & Activity:**
    *   Search SIEM using `secops-mcp.search_security_events` for recent activity related to `${ENDPOINT_ID}` (e.g., last 24-72 hours). Look for:
        *   Suspicious process executions.
        *   Anomalous network connections (especially outbound to known bad IPs/domains).
        *   Significant alert volume associated with the endpoint.
        *   Logins from unusual users or locations.
    *   *(Optional) Check Vulnerability Status:*
        *   If cloud resource, use `scc-mcp.top_vulnerability_findings` filtering for the resource name.
        *   *(If on-prem/other VM scanner integrated: Query scanner for critical/high vulnerabilities)*.
    *   *(Optional) Check EDR Status:*
        *   *(Use EDR integration tool `get_endpoint_details` for `${ENDPOINT_ID}` to check agent status, recent EDR alerts, running processes)*.
4.  **Assess Compromise Likelihood & Need for Isolation:** Based on the gathered context, SIEM activity, vulnerability/EDR status, determine the likelihood of compromise and the urgency for isolation.
5.  **Confirm Isolation Action:** Use `ask_followup_question` to confirm with the analyst whether network isolation should be performed for `${ENDPOINT_ID}`.
6.  **Execute Isolation:**
    *   *(Requires specific EDR integration tool with isolation capability)*
    *   If confirmed "Yes":
        *   Execute the EDR `isolate_endpoint` action for `${ENDPOINT_ID}`.
7.  **Document Findings & Actions:** Record the triage findings, assessment, and isolation status/action taken for `${ENDPOINT_ID}` in the SOAR case using `secops-soar.post_case_comment`.
8.  **Next Steps / Handover:**
    *   If isolated or confirmed compromise, determine next steps: deeper forensic analysis, malware removal, re-imaging, handover to Tier 3/IR team.
    *   Document recommended next steps in the case comment.
9.  **Completion:** Conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant Analyst
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant SCC as scc-mcp %% Cloud Vuln Check
    participant EDR as EDR (Conceptual) %% EDR Tool
    participant VulnScanner as VulnScanner (Conceptual) %% VM Tool

    Analyst->>Cline: Start Endpoint Triage & Isolation\nInput: ENDPOINT_ID, ENDPOINT_TYPE, CASE_ID, ALERT_GROUP_IDS

    %% Step 2: Gather Initial Context
    Cline->>SOAR: get_case_full_details(case_id=CASE_ID)
    SOAR-->>Cline: Case Details
    Cline->>SIEM: lookup_entity(entity_value=ENDPOINT_ID)
    SIEM-->>Cline: SIEM Endpoint Summary

    %% Step 3: Check Posture & Activity
    Cline->>SIEM: search_security_events(text="Activity for endpoint ENDPOINT_ID", hours_back=72)
    SIEM-->>Cline: Detailed Endpoint Events
    opt Check Vulnerabilities
        alt Endpoint is Cloud Resource
            Cline->>SCC: top_vulnerability_findings(project_id=..., filter="resourceName=ENDPOINT_ID")
            SCC-->>Cline: Vulnerability Findings
        else On-Prem/Other VM
            Cline->>VulnScanner: (Conceptual) get_vulns(target=ENDPOINT_ID)
            VulnScanner-->>Cline: Vulnerability List
        end
    end
    opt Check EDR Status
        Cline->>EDR: (Conceptual) get_endpoint_details(endpoint=ENDPOINT_ID)
        EDR-->>Cline: EDR Status, Alerts, Processes
    end

    %% Step 4: Assess Likelihood
    Note over Cline: Analyze findings, assess compromise likelihood & need for isolation

    %% Step 5: Confirm Isolation
    Cline->>Analyst: ask_followup_question(question="Isolate endpoint ENDPOINT_ID?", options=["Yes", "No"])
    Analyst->>Cline: Confirmation (e.g., "Yes")

    %% Step 6: Execute Isolation
    alt Confirmation is "Yes"
        opt EDR Tool Available
            Cline->>EDR: (Conceptual) isolate_endpoint(endpoint=ENDPOINT_ID)
            EDR-->>Cline: Isolation Confirmation/Status
        else EDR Tool Not Available
            Note over Cline: Manual isolation required
        end
    end

    %% Step 7 & 8: Document & Next Steps
    Cline->>SOAR: post_case_comment(case_id=CASE_ID, comment="Endpoint ENDPOINT_ID triage: Findings [...]. Assessment: [...]. Isolation Action: [Yes/No/Manual]. Next Steps: [Forensics/Reimage/Monitor]")
    SOAR-->>Cline: Comment Confirmation

    %% Step 9: Completion
    Cline->>Analyst: attempt_completion(result="Basic Endpoint Triage & Isolation runbook complete for ENDPOINT_ID.")
