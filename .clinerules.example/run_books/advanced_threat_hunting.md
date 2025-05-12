# Advanced Threat Hunting (Hypothesis-Driven) Runbook

## Objective

Conduct proactive, hypothesis-driven threat hunts based on broad threat intelligence (e.g., a new actor report, a novel technique description) or observed anomalies, going beyond pre-defined TTP hunts. Suitable for Tier 3 Analysts or dedicated Threat Hunters.

## Scope

This runbook outlines a flexible framework for advanced threat hunting, emphasizing iterative investigation and deep analysis using available tools.

## Inputs

*   `${HUNT_HYPOTHESIS}`: A clear statement of the hunt's objective (e.g., "Suspected use of DNS tunneling for C2 based on recent actor TTPs", "Anomalous PowerShell execution patterns on critical servers", "Evidence of living-off-the-land techniques bypassing EDR").
*   *(Optional) `${RELEVANT_GTI_REPORTS}`: Comma-separated list of GTI Collection IDs or report names providing context.*
*   *(Optional) `${TARGET_SCOPE_QUERY}`: UDM query fragment to narrow the initial search scope.*
*   `${TIME_FRAME_HOURS}`: Lookback period in hours for SIEM/log searches (can be adjusted during the hunt, default: 168 = 7 days).
*   *(Optional) `${HUNT_CASE_ID}`: A SOAR case ID dedicated to tracking this hunt.*

## Tools

*   `gti-mcp`: All tools, especially `get_collection_report`, `get_entities_related_to_a_collection`, `get_collection_timeline_events`, `search_threats`, `get_threat_intel`.
*   `secops-mcp`: `search_security_events` (Extensive use), `lookup_entity`, `get_ioc_matches`.
*   `secops-soar`: `post_case_comment`, `list_cases`, `get_case_full_details`.
*   `bigquery`: `execute-query` (For large-scale or complex data analysis).
*   *(Potentially EDR, Cloud, Identity tools if integrated via MCP)*.

## Workflow Steps & Diagram

1.  **Define Hypothesis & Scope:** Clearly articulate the `${HUNT_HYPOTHESIS}`. Define the initial `${TARGET_SCOPE_QUERY}` and `${TIME_FRAME_HOURS}`. Identify relevant GTI reports (`${RELEVANT_GTI_REPORTS}`). Create or identify a `${HUNT_CASE_ID}` for documentation.
2.  **Deep Intelligence Analysis (GTI/External):**
    *   Thoroughly review relevant GTI reports (`get_collection_report`).
    *   Explore related entities, TTPs, and timelines (`get_entities_related_to_a_collection`, `get_collection_timeline_events`, `get_collection_mitre_tree`).
    *   Use `get_threat_intel` for specific technique details.
    *   *(Manual Step: Consult external TI sources, MITRE ATT&CK, research papers).*
3.  **Develop Initial Hunt Queries:**
    *   Based on the hypothesis and intelligence, formulate initial advanced queries for `secops-mcp.search_security_events` or `bigquery.execute-query`. Focus on behavioral indicators, anomalies, or specific TTP artifacts.
    *   Combine with `${TARGET_SCOPE_QUERY}`.
4.  **Iterative Search & Analysis:**
    *   Execute initial queries.
    *   Analyze results, looking for outliers, suspicious correlations, or patterns matching the hypothesis.
    *   **Pivot:** Based on initial findings (e.g., suspicious hosts, users, processes, network connections), refine the hypothesis and develop new, more targeted queries. Adjust scope and timeframe as needed.
    *   Repeat search and analysis iteratively.
5.  **Advanced Enrichment:**
    *   For any suspicious entities identified during the iterative search:
        *   Perform deep enrichment using `secops-mcp.lookup_entity`.
        *   Perform multi-step pivoting in GTI (`get_entities_related_to_a_...`).
        *   Check against known IOC matches (`secops-mcp.get_ioc_matches`).
        *   *(Leverage EDR/Cloud/Identity tools if applicable)*.
6.  **Synthesize & Document:**
    *   Continuously document the hunt process, queries used, analysis steps, findings (positive and negative), and enrichment results within the `${HUNT_CASE_ID}` using `secops-soar.post_case_comment`.
    *   Structure findings clearly, linking evidence back to the hypothesis.
7.  **Action / Handover / Conclude:**
    *   **If a confirmed threat is found:** Escalate immediately. Create a new incident case or link findings to an existing one. Hand over details to the Incident Response team.
    *   **If suspicious activity requires further monitoring:** Document recommendations and potentially configure specific monitoring alerts.
    *   **If hunt yields valuable insights but no active threat:** Document findings and propose new detection rules or improvements to Security Engineering.
    *   **If hunt is inconclusive:** Document the process, negative findings, and any limitations encountered. Conclude the hunt.
8.  **Completion:** Finalize documentation in the `${HUNT_CASE_ID}` and conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant Analyst/Hunter
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar
    participant BigQuery as bigquery (Optional)
    participant OtherTools as EDR/Cloud/IDP (Optional)
    participant IR_Team as Incident Response
    participant SecEng as Security Engineering

    Analyst/Hunter->>Cline: Start Advanced Threat Hunt\nInput: HUNT_HYPOTHESIS, GTI_REPORTS (opt), SCOPE (opt), TIME_FRAME, HUNT_CASE_ID (opt)

    %% Step 1: Define Scope & Case
    Note over Cline: Define Hypothesis, Scope, Timeframe. Create/Identify HUNT_CASE_ID.

    %% Step 2: Deep Intelligence Analysis
    loop For each GTI Report R
        Cline->>GTI: get_collection_report(id=R)
        GTI-->>Cline: Report Details
        Cline->>GTI: get_entities_related_to_a_collection(id=R, ...)
        GTI-->>Cline: Related Entities/TTPs
        Cline->>GTI: get_collection_timeline_events(id=R)
        GTI-->>Cline: Timeline
    end
    Cline->>GTI: get_threat_intel(query="Details on relevant TTPs")
    GTI-->>Cline: TTP Context

    %% Step 3: Develop Initial Queries
    Note over Cline: Formulate advanced SIEM/BigQuery queries based on Hypothesis & TI

    %% Step 4: Iterative Search & Analysis
    loop Until Hunt Concluded
        Cline->>SIEM: search_security_events(text=Query, hours_back=...)
        SIEM-->>Cline: Search Results
        opt Use BigQuery
            Cline->>BigQuery: execute-query(query=BQ_Query)
            BigQuery-->>Cline: BQ Results
        end
        Note over Cline: Analyze results, identify leads (Leads L1, L2...)
        Note over Cline: Refine Hypothesis, Develop New Queries based on Leads
        break If No More Leads or Hunt Time Limit Reached
    end

    %% Step 5: Advanced Enrichment
    opt Suspicious Leads Found (L1, L2...)
        loop For each Lead Li
            Cline->>SIEM: lookup_entity(entity_value=Li)
            SIEM-->>Cline: SIEM Summary
            Cline->>GTI: get_..._report / get_entities_related_to_a_...(ioc=Li)
            GTI-->>Cline: GTI Enrichment & Pivot Results
            opt Use Other Tools
                 Cline->>OtherTools: Query EDR/Cloud/IDP for Li
                 OtherTools-->>Cline: Additional Context
            end
        end
    end

    %% Step 6: Synthesize & Document
    Note over Cline: Continuously document process, queries, findings in HUNT_CASE_ID
    Cline->>SOAR: post_case_comment(case_id=HUNT_CASE_ID, comment="Hunt Update: Query [...], Findings [...], Enrichment [...]")
    SOAR-->>Cline: Comment Confirmation

    %% Step 7 & 8: Action / Handover / Conclude
    alt Confirmed Threat Found
        Note over Cline: Escalate to Incident Response
        Cline->>IR_Team: Handover Findings
        Cline->>Analyst/Hunter: attempt_completion(result="Advanced Hunt complete. Confirmed threat found and escalated.")
    else Suspicious Activity Found
        Note over Cline: Recommend monitoring or new detections
        Cline->>SecEng: Propose New Detection Logic
        Cline->>Analyst/Hunter: attempt_completion(result="Advanced Hunt complete. Suspicious activity documented. Recommendations made.")
    else Inconclusive / Negative Findings
        Note over Cline: Document negative results and limitations
        Cline->>Analyst/Hunter: attempt_completion(result="Advanced Hunt complete. No significant findings. Hunt documented.")
    end
```