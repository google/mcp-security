# Runbook: APT Threat Hunt

## Objective

Proactively hunt for Tactics, Techniques, and Procedures (TTPs) and Indicators of Compromise (IOCs) associated with a specific Advanced Persistent Threat (APT) group based on threat intelligence.

## Scope

Focuses on SIEM log analysis and GTI correlation for specific TTPs and IOCs related to the target APT group. Excludes deep endpoint forensics unless findings warrant escalation.

## Inputs

*   `${THREAT_ACTOR_ID}`: GTI Collection ID or name of the target APT group.
*   `${HUNT_TIMEFRAME_HOURS}`: Lookback period in hours (e.g., 168 for 7 days).
*   *(Optional) `${TARGET_SCOPE_QUERY}`: UDM query fragment to narrow scope (e.g., specific host group, network segment).*
*   *(Optional) `${HUNT_HYPOTHESIS}`: Specific hypothesis guiding the hunt (e.g., "Searching for FIN11 exploiting MFT servers").*
*   *(Optional) `${RELEVANT_GTI_REPORTS}`: Comma-separated list of relevant GTI report IDs.*
*   *(Optional) `${HUNT_CASE_ID}`: SOAR case ID for tracking.*

## Tools

*   `gti-mcp`: `get_collection_report`, `get_entities_related_to_a_collection`, `get_collection_timeline_events`, `get_collection_mitre_tree`, `search_threat_actors` (if starting with name)
*   `secops-mcp`: `search_security_events`, `lookup_entity`, `get_ioc_matches`
*   `secops-soar`: `post_case_comment`, `list_cases`
*   `write_to_file`
*   **Common Steps:** `common_steps/find_relevant_soar_case.md`, `common_steps/generate_report_file.md`

## Workflow Steps & Diagram

1.  **Identify Actor & Gather Intelligence:**
    *   If starting with a name, use `gti-mcp.search_threat_actors` to find the `${THREAT_ACTOR_ID}`.
    *   Retrieve details about `${THREAT_ACTOR_ID}` using `gti-mcp.get_collection_report`.
    *   Analyze known TTPs using `gti-mcp.get_collection_mitre_tree`.
    *   Analyze timelines using `gti-mcp.get_collection_timeline_events`. *(Note: This may return no results for some actors).*
    *   Gather associated IOCs (IPs, domains, hashes, URLs) using `gti-mcp.get_entities_related_to_a_collection` for relevant relationship types (e.g., files, domains, urls). *(Note: Not all relationship types may yield results).* Let this be `GTI_IOC_LIST`.
2.  **Check SIEM IOC Matches:** Use `secops-mcp.get_ioc_matches` covering `${HUNT_TIMEFRAME_HOURS}` to see if any IOCs related to the actor are already flagged by integrated feeds. Correlate with `GTI_IOC_LIST`.
3.  **IOC-Based Search (SIEM):**
    *   For each relevant IOC type (e.g., IPs, domains, hashes, URLs) derived from `GTI_IOC_LIST`:
        *   Construct appropriate UDM queries for `secops-mcp.search_security_events`.
        *   Execute the search over `${HUNT_TIMEFRAME_HOURS}`.
        *   Analyze results for any hits. Let findings be `IOC_SEARCH_FINDINGS`. Document negative results as well.
4.  **TTP-Based Search (SIEM):**
    *   **Develop Queries:** Based on the MITRE techniques identified in Step 1 and the `${HUNT_HYPOTHESIS}` (if provided), formulate specific `secops-mcp.search_security_events` UDM queries targeting indicators for the most relevant TTPs.
        *   *Suggestion:* Use `gti-mcp.get_threat_intel` for specific TTP IDs identified in Step 1 to get detection ideas.
        *   Combine technique-specific queries with `${TARGET_SCOPE_QUERY}` if provided.
    *   **Execute Queries:** Run the developed TTP queries over `${HUNT_TIMEFRAME_HOURS}`. Iterate on queries if initial results are negative but the hypothesis remains strong.
    *   Analyze results for anomalies or suspicious patterns matching the TTPs. Let findings be `TTP_SEARCH_FINDINGS`. Document negative results as well.
5.  **Enrich Findings:**
    *   If hits are found (`IOC_SEARCH_FINDINGS` or `TTP_SEARCH_FINDINGS`):
        *   Identify key involved IOCs and associated entities (hosts, users). Let these be `FOUND_IOCS` and `FOUND_ENTITIES`.
        *   For each item in `FOUND_IOCS` and `FOUND_ENTITIES`:
            *   Use `secops-mcp.lookup_entity` to get SIEM context.
            *   Use relevant `gti-mcp` tools (`get_ip_address_report`, `get_domain_report`, etc.) to get GTI context.
        *   Let combined enrichment results be `ENRICHMENT_RESULTS`.
6.  **Check Related SOAR Cases:**
    *   If `FOUND_IOCS` or `FOUND_ENTITIES` are identified:
        *   Execute `common_steps/find_relevant_soar_case.md` with `SEARCH_TERMS` = list of `FOUND_IOCS` + `FOUND_ENTITIES` and `CASE_STATUS_FILTER="Opened"`.
        *   Obtain `${RELATED_SOAR_CASES}` (list of potentially relevant open case summaries/IDs).
7.  **Synthesize & Document:**
    *   Combine all findings: GTI intelligence, IOC match results, IOC search findings (positive and negative), TTP search findings (positive and negative), enrichment results (`ENRICHMENT_RESULTS`), and related SOAR cases (`${RELATED_SOAR_CASES}`).
    *   Document findings, queries used, and analysis in `${HUNT_CASE_ID}` (if provided) using `secops-soar.post_case_comment`.
8.  **Generate Report:**
    *   Structure a Markdown report summarizing the hunt (referencing `.clinerules/reporting_templates.md` and `.clinerules/run_books/guidelines/runbook_guidelines.md`). Include:
        *   Metadata (Runbook Used, Timestamp, Case ID if applicable).
        *   Hunt Objective/Hypothesis.
        *   Scope (`${TARGET_SCOPE_QUERY}`) & Timeframe (`${HUNT_TIMEFRAME_HOURS}`).
        *   Threat Actor Summary (from GTI).
        *   Key TTPs Investigated.
        *   IOCs Searched.
        *   SIEM Queries Used (IOC & TTP based).
        *   Findings (IOC Matches, IOC Search Hits, TTP Search Hits, Enrichment, Related SOAR Cases). **Crucially, include negative findings** (searches performed that yielded no results).
        *   Analysis & Conclusion.
        *   Recommendations/Escalation (if applicable).
        *   Workflow Diagram (Mermaid).
    *   **Execute Report Generation:** Call `common_steps/generate_report_file.md` with the synthesized report content, `REPORT_TYPE="apt_hunt_report"`, and `REPORT_NAME_SUFFIX=${THREAT_ACTOR_ID}`.
9.  **Escalation/Conclusion:** Escalate confirmed threats or conclude the hunt based on findings. Update `${HUNT_CASE_ID}` status if applicable.

```{mermaid}
sequenceDiagram
    participant Analyst/Hunter
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar
    participant FindCase as common_steps/find_relevant_soar_case.md
    participant GenerateReport as common_steps/generate_report_file.md

    Analyst/Hunter->>Cline: Start APT Hunt\nInput: THREAT_ACTOR_ID, HUNT_TIMEFRAME_HOURS, ...

    %% Step 1: Intelligence Gathering
    opt Actor Name Provided instead of ID
        Cline->>GTI: search_threat_actors(query=ActorName)
        GTI-->>Cline: THREAT_ACTOR_ID
    end
    Cline->>GTI: get_collection_report(id=THREAT_ACTOR_ID)
    GTI-->>Cline: Actor Details
    Cline->>GTI: get_collection_mitre_tree(id=THREAT_ACTOR_ID)
    GTI-->>Cline: Actor TTPs
    Cline->>GTI: get_collection_timeline_events(id=THREAT_ACTOR_ID)
    GTI-->>Cline: Timeline (Optional - May be empty)
    Note over Cline: Gather IOCs for each relevant type (files, domains, urls...)
    loop For each IOC Relationship R
        Cline->>GTI: get_entities_related_to_a_collection(id=THREAT_ACTOR_ID, relationship_name=R)
        GTI-->>Cline: Associated IOCs for type R (GTI_IOC_LIST)
    end

    %% Step 2: Check SIEM IOC Matches
    Cline->>SIEM: get_ioc_matches(hours_back=HUNT_TIMEFRAME_HOURS)
    SIEM-->>Cline: SIEM IOC Match Results
    Note over Cline: Correlate matches with GTI_IOC_LIST

    %% Step 3: IOC-Based Search (SIEM)
    loop For each IOC Type/Value Ii in GTI_IOC_LIST
        Note over Cline: Construct UDM query Qi for IOC Ii
        Cline->>SIEM: search_security_events(text=Qi, hours_back=HUNT_TIMEFRAME_HOURS)
        SIEM-->>Cline: IOC Search Results for Ii (IOC_SEARCH_FINDINGS)
    end

    %% Step 4: TTP-Based Search (SIEM)
    Note over Cline: Develop TTP-based UDM queries Qt based on MITRE techniques & Hypothesis (Use get_threat_intel if needed)
    loop For each TTP Query Qt
        Cline->>SIEM: search_security_events(text=Qt, hours_back=HUNT_TIMEFRAME_HOURS)
        SIEM-->>Cline: TTP Search Results for Qt (TTP_SEARCH_FINDINGS)
    end

    %% Step 5: Enrich Findings
    opt Hits Found (IOC or TTP)
        Note over Cline: Identify key Found_IOCs and Found_Entities (E1, E2...)
        loop For each Found Item Fi (IOC or Entity)
            Cline->>SIEM: lookup_entity(entity_value=Fi)
            SIEM-->>Cline: SIEM Summary for Fi
            Cline->>GTI: get_..._report(ioc=Fi) %% Use appropriate GTI tool
            GTI-->>Cline: GTI Enrichment for Fi (ENRICHMENT_RESULTS)
        end
    end

    %% Step 6: Check Related SOAR Cases
    opt Hits Found
        Note over Cline: Prepare list of Found_IOCs + Found_Entities
        Cline->>FindCase: Execute(Input: SEARCH_TERMS=[Found List], CASE_STATUS_FILTER="Opened")
        FindCase-->>Cline: Results: RELATED_SOAR_CASES
    end

    %% Step 7: Document in SOAR (Optional)
    opt HUNT_CASE_ID provided
        Note over Cline: Synthesize findings including RELATED_SOAR_CASES
        Cline->>SOAR: post_case_comment(case_id=HUNT_CASE_ID, comment="APT Hunt Summary...")
        SOAR-->>Cline: Comment Confirmation
    end

    %% Step 8: Generate Report
    Note over Cline: Synthesize all findings (positive & negative, incl. related cases) into Markdown report content
    Cline->>GenerateReport: Execute(Input: REPORT_CONTENT, REPORT_TYPE="apt_hunt_report", REPORT_NAME_SUFFIX=THREAT_ACTOR_ID)
    GenerateReport-->>Cline: Results: REPORT_FILE_PATH, WRITE_STATUS

    %% Step 9: Escalation/Conclusion
    alt Confirmed Threat Found via Hunt
        Note over Cline: Escalate findings (Create/Update Incident Case)
        Cline->>Analyst/Hunter: attempt_completion(result="APT Hunt complete. Threat found and escalated. Report generated at REPORT_FILE_PATH.")
    else No Threat Found
        Cline->>Analyst/Hunter: attempt_completion(result="APT Hunt complete. No significant findings. Report generated at REPORT_FILE_PATH.")
    end
```

## Completion Criteria

Intelligence gathered, IOCs and TTPs searched in SIEM, findings analyzed and enriched (if applicable), results documented in SOAR (optional), and a final report generated. Appropriate escalation or conclusion based on findings.
