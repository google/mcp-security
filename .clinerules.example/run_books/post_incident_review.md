# Post-Incident Review (PIR) Runbook

## Objective

To provide a structured process for conducting post-incident reviews (PIRs) after significant security incidents, analyzing the incident timeline, response effectiveness, identifying root causes, and capturing lessons learned to improve future prevention, detection, and response capabilities.

## Scope

This runbook outlines the process for conducting a PIR meeting, analyzing incident data, documenting findings, and tracking recommendations. It assumes the primary incident response (following relevant IRPs like malware, phishing, ransomware, compromised user) is complete or nearing completion.

## Inputs

*   `${CASE_ID}`: The SOAR case ID of the incident being reviewed.
*   `${INCIDENT_REPORT_PATH}`: Path to the final incident report (if generated separately).
*   *(Optional) `${KEY_STAKEHOLDERS}`: List of individuals/teams required for the PIR meeting (e.g., SOC Manager, IR Lead, Involved Analysts, Security Engineering Rep, CTI Rep, potentially affected Business Unit Rep).*
*   *(Optional) `${INCIDENT_TIMELINE}`: Pre-compiled timeline of key events.*

## Tools

*   `secops-soar`: `get_case_full_details`, `post_case_comment` (for accessing case data and documenting PIR outcomes).
*   *(Potentially other tools for accessing incident reports or metrics if stored elsewhere)*.
*   **Referenced Runbooks:** IRPs (`malware_incident_response.md`, `phishing_response.md`, etc. - specifically the Phase 7 feedback section), `reporting_templates.md`.

## Workflow Steps & Diagram

1.  **Schedule PIR Meeting:** Identify key stakeholders (`${KEY_STAKEHOLDERS}`) based on the incident's nature and impact. Schedule the PIR meeting, allowing sufficient time for preparation.
2.  **Gather Incident Data:**
    *   Retrieve comprehensive case details using `secops-soar.get_case_full_details` for `${CASE_ID}`. Pay close attention to comments, timeline information, actions taken, and any feedback already documented in the Phase 7 section of the relevant IRP.
    *   Review the final incident report (`${INCIDENT_REPORT_PATH}`) if available.
    *   Compile a detailed incident timeline (`${INCIDENT_TIMELINE}`) if not already available.
3.  **Conduct PIR Meeting:**
    *   **Review Timeline:** Walk through the incident timeline from initial detection to recovery.
    *   **Analyze Response:** Discuss the effectiveness of each phase (Identification, Containment, Eradication, Recovery).
        *   What worked well?
        *   What challenges were encountered?
        *   Were runbooks followed? Were they effective? (Reference Phase 7 feedback).
        *   Were tools used effectively? Any tool limitations or failures?
    *   **Root Cause Analysis:** Discuss the likely root cause(s) of the incident (e.g., vulnerability exploited, credential compromise, user action).
    *   **Identify Gaps:** Identify specific gaps in prevention, detection, response processes, or tool capabilities.
    *   **Brainstorm Recommendations:** Collaboratively develop specific, measurable, achievable, relevant, and time-bound (SMART) recommendations for improvement.
4.  **Document PIR Findings & Recommendations:**
    *   Consolidate the discussion points, identified gaps, root cause analysis, and recommendations.
    *   Structure the findings according to a standard PIR report template (potentially defined in `.clinerules/reporting_templates.md`).
5.  **Assign & Track Recommendations:**
    *   Assign owners and target completion dates for each recommendation.
    *   Establish a mechanism for tracking the implementation status of recommendations (e.g., within the SOAR case, a separate tracking system).
6.  **Update Documentation:**
    *   Based on findings, update relevant runbooks, policies, or procedures. Trigger updates to detection rules via the appropriate process (e.g., notify Detection Engineering).
7.  **Finalize PIR Documentation:**
    *   Add the PIR summary and recommendations to the SOAR case (`${CASE_ID}`) using `secops-soar.post_case_comment`.
    *   Store any formal PIR report in the designated repository.
8.  **Completion:** Conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant PIR_Lead/Analyst
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant Stakeholders as Key Stakeholders
    participant Documentation as Runbooks/Policies
    participant TrackingSystem as Recommendation Tracking

    PIR_Lead/Analyst->>Cline: Start Post-Incident Review\nInput: CASE_ID, REPORT_PATH (opt), STAKEHOLDERS (opt)

    %% Step 1: Schedule Meeting
    Note over PIR_Lead/Analyst: Identify & Schedule Stakeholders

    %% Step 2: Gather Data
    Cline->>SOAR: get_case_full_details(case_id=CASE_ID)
    SOAR-->>Cline: Case Details, Comments, Phase 7 Feedback
    Note over Cline: Review Incident Report (REPORT_PATH)
    Note over Cline: Compile Detailed Timeline

    %% Step 3: Conduct PIR Meeting
    PIR_Lead/Analyst->>Stakeholders: Conduct PIR Meeting
    Note over Stakeholders: Review Timeline\nAnalyze Response\nRoot Cause Analysis\nIdentify Gaps\nBrainstorm Recommendations

    %% Step 4: Document Findings
    Note over PIR_Lead/Analyst: Consolidate PIR discussion into findings/recommendations document

    %% Step 5: Assign & Track Recommendations
    PIR_Lead/Analyst->>TrackingSystem: Assign Owners & Dates to Recommendations

    %% Step 6: Update Documentation
    PIR_Lead/Analyst->>Documentation: Initiate updates to Runbooks, Policies, Detections

    %% Step 7: Finalize PIR Documentation
    Cline->>SOAR: post_case_comment(case_id=CASE_ID, comment="PIR Summary: Root Cause [...], Gaps [...], Recommendations [...]")
    SOAR-->>Cline: Comment Confirmation
    Note over PIR_Lead/Analyst: Store formal PIR report

    %% Step 8: Completion
    Cline->>PIR_Lead/Analyst: attempt_completion(result="Post-Incident Review process complete for Case CASE_ID. Findings documented and recommendations tracked.")

```

## Completion Criteria

PIR meeting conducted, findings and recommendations documented, recommendations assigned and tracked, relevant documentation updates initiated, and PIR summary added to the SOAR case.
