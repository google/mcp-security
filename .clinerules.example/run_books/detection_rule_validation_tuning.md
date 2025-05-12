# Detection Rule Validation & Tuning Runbook

## Objective

Analyze the performance and effectiveness of an existing SIEM detection rule, identify potential false positives/negatives, and propose tuning recommendations. Suitable for Tier 3 Analysts or Detection Engineers.

## Scope

This runbook covers the analysis of a single detection rule's historical performance and logic to suggest improvements. It does not cover the implementation of the tuning changes, which would typically be handled by Security Engineering.

## Inputs

*   `${RULE_ID}`: The unique identifier or name of the SIEM detection rule to analyze.
*   *(Optional) `${ANALYSIS_TIMEFRAME_DAYS}`: How many days of historical alert data to analyze (default: 90).*
*   *(Optional) `${REASON_FOR_REVIEW}`: Why this rule is being reviewed (e.g., high alert volume, missed detection in incident, periodic review).*
*   *(Optional) `${REVIEW_CASE_ID}`: A SOAR case ID dedicated to tracking this review.*

## Tools

*   `secops-mcp`: `list_security_rules`, `search_security_events`, `get_security_alerts`, `lookup_entity`.
*   `secops-soar`: `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`, `post_case_comment`.
*   `gti-mcp`: Various tools (`get_file_report`, `get_ip_address_report`, etc.) for enriching entities involved in true/false positive alerts.
*   *(External Resources: MITRE ATT&CK, threat intelligence reports relevant to the rule's intent).*

## Workflow Steps & Diagram

1.  **Define Scope & Context:** Obtain `${RULE_ID}`, `${ANALYSIS_TIMEFRAME_DAYS}`, `${REASON_FOR_REVIEW}`, and `${REVIEW_CASE_ID}`. Document the rule's intended purpose and the TTPs/threats it aims to detect.
2.  **Retrieve Rule Logic:**
    *   Use `secops-mcp.list_security_rules` filtering by `${RULE_ID}` (or similar mechanism) to get the current rule definition (e.g., YARA-L code).
    *   *(Alternatively, use `secops-soar.google_chronicle_get_rule_details` if applicable and provides more detailed logic).*
    *   Analyze the logic: understand the event fields, conditions, thresholds, and exceptions.
3.  **Analyze Historical Alerts:**
    *   Use `secops-mcp.get_security_alerts` or `secops-mcp.search_security_events` (querying for `metadata.rule_id = "${RULE_ID}"` or similar) covering the `${ANALYSIS_TIMEFRAME_DAYS}`.
    *   Gather statistics: total alert count, alert severity distribution, associated SOAR case statuses (True Positive, False Positive, Benign Positive, etc. - requires analyzing linked cases).
4.  **Analyze Underlying Events (Sampling):**
    *   **False Positives:** Select a representative sample of alerts closed as False Positive (FP). For each, retrieve associated events (`secops-soar.list_events_by_alert` or `secops-mcp.search_security_events`). Analyze why the rule triggered incorrectly. Look for common patterns in FPs (specific applications, user groups, network segments).
    *   **True Positives:** Select a sample of confirmed True Positive (TP) alerts. Retrieve associated events. Verify the rule logic correctly identified the malicious activity.
    *   **Benign Positives (Optional):** Analyze alerts closed as Benign Positive (e.g., authorized vulnerability scan triggering a rule). Determine if exceptions are needed.
5.  **Enrich Key Entities:**
    *   For entities (users, hosts, IPs, files) involved in both TP and FP sample events, use `secops-mcp.lookup_entity` and `gti-mcp` tools to gather context and reputation information.
6.  **Identify Potential False Negatives (Hypothesis-Based):**
    *   Based on the rule's intent, threat intelligence, and knowledge of related incidents:
        *   Formulate hypotheses about variations of the targeted activity the current rule logic might miss.
        *   Develop specific `secops-mcp.search_security_events` queries to search for evidence of these variations within the analysis timeframe.
    *   Analyze search results. If evidence of missed detections is found, document the specific event characteristics.
7.  **Synthesize Findings & Propose Tuning:**
    *   Summarize the rule's performance (alert volume, TP/FP ratio).
    *   Detail the root causes of common false positives.
    *   Document any identified false negative scenarios.
    *   Propose specific changes to the rule logic:
        *   Adding/refining exceptions (e.g., specific process paths, usernames, IP ranges).
        *   Adjusting thresholds or time windows.
        *   Changing or adding event fields/conditions.
        *   Splitting the rule into multiple, more specific rules.
8.  **Document Recommendations:**
    *   Record the complete analysis, findings, and specific tuning recommendations in the `${REVIEW_CASE_ID}` using `secops-soar.post_case_comment` or in a dedicated report. Clearly state the expected impact of the proposed changes.
9.  **Handover:** Assign the case/report to the Security Engineering team for implementation and testing of the proposed tuning changes.
10. **Completion:** Conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant Analyst/Engineer
    participant Cline as Cline (MCP Client)
    participant SIEM as secops-mcp
    participant SOAR as secops-soar
    participant GTI as gti-mcp
    participant SecEng as Security Engineering

    Analyst/Engineer->>Cline: Start Rule Validation & Tuning\nInput: RULE_ID, TIMEFRAME_DAYS, REASON, REVIEW_CASE_ID (opt)

    %% Step 1: Define Scope
    Note over Cline: Document Rule Intent, TTPs, Case ID.

    %% Step 2: Retrieve Rule Logic
    Cline->>SIEM: list_security_rules(filter=RULE_ID)
    SIEM-->>Cline: Rule Definition/Logic
    Note over Cline: Analyze rule logic

    %% Step 3: Analyze Historical Alerts
    Cline->>SIEM: get_security_alerts(rule_id=RULE_ID, hours_back=TIMEFRAME_DAYS*24)
    SIEM-->>Cline: Historical Alerts List
    Note over Cline: Analyze alert volume, severity, associated case statuses (TP/FP)

    %% Step 4: Analyze Underlying Events (Sampling)
    Note over Cline: Select sample FP alerts
    loop For each Sample FP Alert FPi
        Cline->>SOAR: list_events_by_alert(case_id=..., alert_id=FPi) %% Or SIEM search
        SOAR-->>Cline: Events for FPi
        Note over Cline: Analyze why rule triggered incorrectly
    end
    Note over Cline: Select sample TP alerts
    loop For each Sample TP Alert TPi
        Cline->>SOAR: list_events_by_alert(case_id=..., alert_id=TPi) %% Or SIEM search
        SOAR-->>Cline: Events for TPi
        Note over Cline: Verify rule logic worked correctly
    end

    %% Step 5: Enrich Key Entities
    Note over Cline: Identify key entities from sample events
    loop For each Key Entity Ei
        Cline->>SIEM: lookup_entity(entity_value=Ei)
        SIEM-->>Cline: SIEM Summary for Ei
        Cline->>GTI: get_..._report(ioc=Ei)
        GTI-->>Cline: GTI Report for Ei
    end

    %% Step 6: Identify Potential False Negatives
    Note over Cline: Formulate FN hypotheses based on rule intent & TI
    loop For each FN Hypothesis Hi
        Note over Cline: Develop SIEM query Qi for Hi
        Cline->>SIEM: search_security_events(text=Qi, hours_back=...)
        SIEM-->>Cline: Search Results for Qi
        Note over Cline: Analyze if rule should have triggered but didn't
    end

    %% Step 7: Synthesize Findings & Propose Tuning
    Note over Cline: Summarize performance, FP causes, FN scenarios
    Note over Cline: Formulate specific tuning recommendations (logic changes)

    %% Step 8 & 9: Document & Handover
    Cline->>SOAR: post_case_comment(case_id=REVIEW_CASE_ID, comment="Rule Review Summary (RULE_ID): Performance [...], FP Analysis [...], FN Analysis [...], Tuning Recommendations: [...]")
    SOAR-->>Cline: Comment Confirmation
    Note over Cline: Assign case/report to Security Engineering

    %% Step 10: Completion
    Cline->>Analyst/Engineer: attempt_completion(result="Detection Rule Validation & Tuning complete for RULE_ID. Recommendations documented and handed over.")
