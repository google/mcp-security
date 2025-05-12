### Prioritize and Investigate a Case

From a list of cases, identify cases of the highest severity and potential impact based on underlying alerts and detections. Get rule logic to validate the detections in the cases. After identifying the highest N priority cases -> Explain the entirety of the case to the analyst in the context of the underlying rule logic (explain the rule logic and how it applies to this case). Get entity context to determine if there are additional alerts, detections, or events that may not have been included in the case but are potentially applicable.

Use the tools:


 * List Cases and include the environment
 * Get Alerts in a Case
 * Get Detections in a Case
 * Get Events from Alerts and/or Detections in a Case
 * Get rule logic
 * Evaluate Alert/Event against rule logic
 * UDM search for activity from principal or target
 * **Common Steps:** `common_steps/find_relevant_soar_case.md`

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant FindCase as common_steps/find_relevant_soar_case.md

    User->>Cline: Prioritize and investigate cases
    Cline->>SOAR: list_cases()
    SOAR-->>Cline: List of cases (C1, C2... Priority P1, P2...)
    Note over Cline: Analyze cases, identify high priority (e.g., Case X based on initial priority/alerts)
    Cline->>SOAR: get_case_full_details(case_id=X)
    SOAR-->>Cline: Full details for Case X (alerts, comments, etc.)
    Note over Cline: Confirm priority based on full details. May use change_case_priority if needed.
    Cline->>SOAR: list_alerts_by_case(case_id=X)
    SOAR-->>Cline: Alerts for Case X (A1, A2...)
    Note over Cline: Initialize ALL_CASE_ENTITIES = set()
    loop For each Alert Ai in Case X
        Cline->>SOAR: list_events_by_alert(case_id=X, alert_id=Ai)
        SOAR-->>Cline: Events for Alert Ai (containing rule_id, entities E1, E2...)
        Note over Cline: Add E1, E2... to ALL_CASE_ENTITIES
        Note over Cline: Extract rule_id from event/alert data
        Cline->>SIEM: list_security_rules(rule_id=rule_id)
        SIEM-->>Cline: Rule logic/definition for rule_id
        Cline->>SIEM: list_rule_detections(rule_id=rule_id)
        SIEM-->>Cline: Detections associated with rule_id
        Note over Cline: Analyze events/detections against rule logic
        loop For each relevant Entity Ej in Events
            Cline->>SIEM: lookup_entity(entity_value=Ej)
            SIEM-->>Cline: Entity context for Ej
            Cline->>SIEM: search_security_events(text="Events involving entity Ej", hours_back=...)
            SIEM-->>Cline: Broader UDM events for Ej
        end
    end
    Note over Cline: Check for related SOAR cases using all identified entities
    Cline->>FindCase: Execute(Input: SEARCH_TERMS=list(ALL_CASE_ENTITIES), CASE_STATUS_FILTER="Opened")
    FindCase-->>Cline: Results: RELATED_SOAR_CASES
    Note over Cline: Synthesize findings, correlate rule logic with events/entities, include related cases
    Cline->>SOAR: post_case_comment(case_id=X, comment="Investigation Summary: Case X involves rule [Rule Name] triggered by events [...]. Entities [...] investigated. Related Cases: ${RELATED_SOAR_CASES}. Findings: [...]")
    SOAR-->>Cline: Comment confirmation
    Cline->>Cline: attempt_completion(result="Completed investigation for Case X. Summary posted as comment.")

```
