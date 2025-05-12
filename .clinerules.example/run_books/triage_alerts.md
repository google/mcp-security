# Runbook: Alert Triage (Placeholder)

## Objective

*(Define the goal, e.g., To provide a standardized process for the initial assessment and triage of incoming security alerts, determining if they represent a potential threat requiring further investigation or if they can be closed as false positives/duplicates.)*

## Scope

*(Define what is included/excluded, e.g., Covers initial alert review, basic entity enrichment, and decision-making based on predefined criteria. Excludes deep investigation or containment actions.)*

## Inputs

*   `${ALERT_ID}` or `${CASE_ID}`: The identifier for the alert or case to be triaged.
*   *(Optional) `${ALERT_DETAILS}`: Initial details provided by the alerting system.*

## Tools

*   `secops-soar`: `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`, `post_case_comment`, `change_case_priority`, `siemplify_get_similar_cases`, `siemplify_close_case`, `siemplify_close_alert`
*   `secops-mcp`: `lookup_entity`, `get_ioc_matches`
*   `gti-mcp`: `get_file_report`, `get_domain_report`, `get_ip_address_report`, `get_url_report`
*   **Common Steps:** `common_steps/check_duplicate_cases.md`, `common_steps/enrich_ioc.md`, `common_steps/find_relevant_soar_case.md`, `common_steps/document_in_soar.md`, `common_steps/close_soar_artifact.md`

## Workflow Steps & Diagram

1.  **Receive Alert/Case:** Obtain the `${ALERT_ID}` or `${CASE_ID}`.
2.  **Gather Initial Context:** Use `secops-soar.get_case_full_details` or `list_alerts_by_case` / `list_events_by_alert` to understand the alert type, severity, involved entities (`KEY_ENTITIES`), and triggering events.
3.  **Check for Duplicates:** Execute `common_steps/check_duplicate_cases.md` with `${CASE_ID}`. Obtain `${SIMILAR_CASE_IDS}`.
4.  **Handle Duplicates:** If `${SIMILAR_CASE_IDS}` is not empty and duplication is confirmed by analyst:
    *   Execute `common_steps/document_in_soar.md` with `${CASE_ID}` and comment "Closing as duplicate of [Similar Case ID]".
    *   Execute `common_steps/close_soar_artifact.md` with:
        *   `${ARTIFACT_ID}` = `${CASE_ID}` (or `${ALERT_ID}`)
        *   `${ARTIFACT_TYPE}` = "Case" (or "Alert")
        *   `${CLOSURE_REASON}` = `"NOT_MALICIOUS"`
        *   `${ROOT_CAUSE}` = `"Similar case is already under investigation"`
        *   `${CLOSURE_COMMENT}` = "Closing as duplicate of [Similar Case ID]"
    *   End runbook execution.
5.  **Find Entity-Related Cases:**
    *   Execute `common_steps/find_relevant_soar_case.md` with `SEARCH_TERMS=KEY_ENTITIES` (list of entities from Step 2) and `CASE_STATUS_FILTER="Opened"`.
    *   Obtain `${ENTITY_RELATED_CASES}` (list of potentially relevant open case summaries/IDs).
6.  **(New) Alert-Specific SIEM Search:**
    *   Based on the alert type identified in Step 2, perform an initial targeted search using `secops-mcp.search_security_events` to gather immediate context. Examples:
        *   **Suspicious Login:** Search for related login events (success/failure) for the user/source IP/hostname around the alert time (e.g., last hour).
        *   **Malware Detection:** Search for process execution, file modification, or network events related to the file hash/endpoint around the alert time.
        *   **Network Alert:** Search for related network flows or DNS lookups involving the source/destination IPs/domains.
    *   Store a summary of findings in `${INITIAL_SIEM_CONTEXT}`. This helps provide more specific context before broader enrichment.
7.  **Basic Enrichment:** Initialize `ENRICHMENT_RESULTS` structure. For each entity `Ei` in `KEY_ENTITIES`:
    *   Execute `common_steps/enrich_ioc.md` with `IOC_VALUE=Ei` and appropriate `IOC_TYPE`.
    *   Store results (`GTI_FINDINGS`, `SIEM_ENTITY_SUMMARY`, `SIEM_IOC_MATCH_STATUS`) in `ENRICHMENT_RESULTS[Ei]`.
8.  **Initial Assessment:** Based on alert type, `ENRICHMENT_RESULTS`, `${ENTITY_RELATED_CASES}`, `${INITIAL_SIEM_CONTEXT}`, and potential known benign patterns (referencing `.clinerules/common_benign_alerts.md` if available), make an initial assessment:
    *   False Positive (FP)
    *   Benign True Positive (BTP - expected/authorized activity)
    *   Requires Further Investigation (True Positive - TP or Suspicious)
9.  **Action Based on Assessment:**
    *   **If FP/BTP:**
        *   Execute `common_steps/document_in_soar.md` with `${CASE_ID}` and comment explaining FP/BTP reason.
        *   **Guidance for Closure:**
            *   Choose an appropriate `${CLOSURE_REASON}` (likely `NOT_MALICIOUS`).
            *   Choose a valid `${ROOT_CAUSE}` from the SOAR platform's predefined list (e.g., `"Legit action"`, `"Normal behavior"`, `"Other"`). Use `secops-soar.get_case_settings_root_causes` to list valid options if unsure.
        *   Execute `common_steps/close_soar_artifact.md` with `${ARTIFACT_ID}` = `${CASE_ID}` (or `${ALERT_ID}`), `${ARTIFACT_TYPE}` = "Case" (or "Alert"), the chosen `${CLOSURE_REASON}`/`${ROOT_CAUSE}`, and `${CLOSURE_COMMENT}` = "Closed as FP/BTP during triage.".
    *   **If TP/Suspicious:**
        *   *(Optional)* Use `secops-soar.change_case_priority` if needed.
        *   Execute `common_steps/document_in_soar.md` with `${CASE_ID}` and comment summarizing initial findings and assessment.
        *   Escalate/assign to the appropriate next tier or trigger a relevant investigation runbook (e.g., `deep_dive_ioc_analysis.md`, `suspicious_login_triage.md`).

```{mermaid}
sequenceDiagram
    participant Analyst
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant CheckDuplicates as common_steps/check_duplicate_cases.md
    participant FindCase as common_steps/find_relevant_soar_case.md
    participant EnrichIOC as common_steps/enrich_ioc.md
    participant DocumentInSOAR as common_steps/document_in_soar.md
    participant CloseArtifact as common_steps/close_soar_artifact.md

    Analyst->>Cline: Start Alert Triage\nInput: ALERT_ID/CASE_ID

    %% Step 2: Gather Initial Context
    Cline->>SOAR: get_case_full_details / list_alerts_by_case / list_events_by_alert
    SOAR-->>Cline: Context (KEY_ENTITIES: E1, E2...)

    %% Step 3: Check for Duplicates
    Cline->>CheckDuplicates: Execute(Input: CASE_ID)
    CheckDuplicates-->>Cline: Results: SIMILAR_CASE_IDS

    %% Step 4: Handle Duplicates
    alt SIMILAR_CASE_IDS not empty & Confirmed Duplicate
        Cline->>DocumentInSOAR: Execute(Input: CASE_ID, Comment="Closing as duplicate...")
        DocumentInSOAR-->>Cline: Status
        Cline->>CloseArtifact: Execute(Input: ARTIFACT_ID=CASE_ID/ALERT_ID, TYPE=..., REASON="Duplicate"...)
        CloseArtifact-->>Cline: Status
        Cline->>Analyst: End Triage (Duplicate)
    end

    %% Step 5: Find Entity-Related Cases
    Cline->>FindCase: Execute(Input: SEARCH_TERMS=KEY_ENTITIES, CASE_STATUS_FILTER="Opened")
    FindCase-->>Cline: Results: ENTITY_RELATED_CASES

    %% Step 6: Alert-Specific SIEM Search
    Note over Cline: Construct alert-specific SIEM query based on alert type
    Cline->>SIEM: search_security_events(text=AlertSpecificQuery, hours_back=1)
    SIEM-->>Cline: Initial SIEM Context Results (INITIAL_SIEM_CONTEXT)

    %% Step 7: Basic Enrichment
    loop For each Key Entity Ei
        Cline->>EnrichIOC: Execute(Input: IOC_VALUE=Ei, IOC_TYPE=...)
        EnrichIOC-->>Cline: Results: Enrichment Data for Ei
    end

    %% Step 8: Initial Assessment
    Note over Cline: Assess: FP / BTP / TP / Suspicious based on Context, Enrichment, Related Cases & Initial SIEM Context

    %% Step 9: Action Based on Assessment
    alt FP / BTP
        Cline->>DocumentInSOAR: Execute(Input: CASE_ID, Comment="Closing as FP/BTP...")
        DocumentInSOAR-->>Cline: Status
        Cline->>CloseArtifact: Execute(Input: ARTIFACT_ID=CASE_ID/ALERT_ID, TYPE=..., REASON="FP/BTP"...)
        CloseArtifact-->>Cline: Status
        Cline->>Analyst: End Triage (FP/BTP)
    else TP / Suspicious
        opt Change Priority
             Cline->>SOAR: change_case_priority(...)
             SOAR-->>Cline: Status
        end
        Cline->>DocumentInSOAR: Execute(Input: CASE_ID, Comment="Initial Findings...")
        DocumentInSOAR-->>Cline: Status
        Note over Cline: Escalate / Assign / Trigger Next Runbook
        Cline->>Analyst: End Triage (Escalated)
    end
```

## Completion Criteria

*(Define how successful completion is determined, e.g., Alert assessed, documented, and either closed or escalated appropriately.)*
