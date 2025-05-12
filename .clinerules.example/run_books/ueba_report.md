# Runbook: UEBA Report Analysis (Placeholder)

## Objective

*(Define the goal, e.g., To analyze a User and Entity Behavior Analytics (UEBA) alert or report, investigate the anomalous activity, gather context, and determine if it represents a genuine threat or benign deviation.)*

## Scope

*(Define what is included/excluded, e.g., Focuses on analyzing UEBA findings, correlating with SIEM logs and user context. May involve basic enrichment but not necessarily deep endpoint forensics unless indicated.)*

## Inputs

*   `${UEBA_ALERT_ID}` or `${CASE_ID}`: Identifier for the UEBA alert or associated SOAR case.
*   `${USER_ID}`: The primary user associated with the anomalous behavior.
*   `${ENTITY_ID}`: Any primary entity (e.g., hostname, resource) associated with the behavior.
*   `${ANOMALY_DESCRIPTION}`: Description of the anomalous behavior reported by the UEBA system.
*   *(Optional) `${BASELINE_INFO}`: Information about the user's normal baseline behavior, if available.*

## Tools

*   `secops-soar`: `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`, `post_case_comment`
*   `secops-mcp`: `lookup_entity` (for user and entity), `search_security_events` (for detailed activity logs)
*   `gti-mcp`: (Relevant enrichment tools if IOCs are involved)
*   *(Potentially Identity Provider tools like `okta-mcp.lookup_okta_user`)*

## Workflow Steps & Diagram

1.  **Receive Alert/Case:** Obtain the UEBA alert details, associated user/entity, `${CASE_ID}` etc.
2.  **Gather Context:** Use `get_case_full_details` (if applicable). Use `lookup_entity` for `${USER_ID}` and `${ENTITY_ID}` to get SIEM context. *(Optional: Check IDP for user status/recent activity)*.
3.  **Analyze Specific Activity:** Use `search_security_events` to retrieve detailed logs corresponding to the timeframe and activity described in `${ANOMALY_DESCRIPTION}`.
4.  **Compare to Baseline:** Compare the observed activity against known baseline behavior (`${BASELINE_INFO}`) or historical patterns observed in SIEM logs. Identify deviations.
5.  **Enrich Associated Indicators:** If the anomalous activity involves specific IOCs (IPs, domains, files), enrich them using `lookup_entity` and GTI tools.
6.  **Synthesize Findings:** Combine UEBA anomaly details, SIEM logs, baseline comparison, and enrichment data. Determine if the activity is explainable, benign, or suspicious/malicious.
7.  **Document & Recommend:** Document findings and assessment in the SOAR case using `post_case_comment`. Recommend next steps: [Close as Benign/Explained | Monitor User/Entity | Escalate for Incident Response (Trigger relevant runbook like Compromised User Account Response)].

```{mermaid}
sequenceDiagram
    participant Analyst
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as gti-mcp
    participant IDP as Identity Provider (Optional)

    Analyst->>SOAR: Receive UEBA Alert/Case (ID, User, Entity, Anomaly Desc.)
    SOAR-->>Analyst: Alert/Case Details
    Analyst->>SOAR: get_case_full_details (Optional)
    SOAR-->>Analyst: Case Context
    Analyst->>SIEM: lookup_entity(entity_value=USER_ID)
    SIEM-->>Analyst: User SIEM Context
    Analyst->>SIEM: lookup_entity(entity_value=ENTITY_ID)
    SIEM-->>Analyst: Entity SIEM Context
    opt IDP Check
        Analyst->>IDP: lookup_user(user=USER_ID)
        IDP-->>Analyst: User IDP Context
    end
    Analyst->>SIEM: search_security_events(text="Detailed logs for anomaly timeframe/activity")
    SIEM-->>Analyst: Specific Activity Logs
    Note over Analyst: Compare activity to baseline/history
    opt IOCs Involved (I1, I2...)
        loop For each IOC Ii
            Analyst->>SIEM: lookup_entity(entity_value=Ii)
            SIEM-->>Analyst: SIEM Context for Ii
            Analyst->>GTI: get...report(ioc=Ii)
            GTI-->>Analyst: GTI Context for Ii
        end
    end
    Note over Analyst: Synthesize findings, assess activity
    Analyst->>SOAR: post_case_comment(case_id=..., comment="UEBA Analysis Summary... Assessment: [...]. Recommendation: [Close/Monitor/Escalate]")
    SOAR-->>Analyst: Comment Confirmation

```

## Completion Criteria

*(Define how successful completion is determined, e.g., UEBA alert analyzed, correlated with logs, findings documented, and appropriate next step recommended/taken.)*
