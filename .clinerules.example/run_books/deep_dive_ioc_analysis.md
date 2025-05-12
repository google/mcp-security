# Deep Dive IOC Analysis Runbook

## Objective

Perform an exhaustive analysis of a single, potentially critical Indicator of Compromise (IOC) escalated from Tier 1 or identified during an investigation. This goes beyond the basic enrichment done by Tier 1, leveraging advanced tool features and pivoting techniques.

## Scope

This runbook covers in-depth analysis of a single IOC (IP, Domain, Hash, URL) using available GTI and SIEM tools to uncover related infrastructure, activity, and context.

## Inputs

*   `${IOC_VALUE}`: The specific IOC value (e.g., "198.51.100.10", "evil-domain.com", "abcdef123456...", "http://bad.url/path").
*   `${IOC_TYPE}`: The type of IOC (e.g., "IP Address", "Domain", "File Hash", "URL").
*   `${CASE_ID}`: The relevant SOAR case ID for documentation.
*   `${ALERT_GROUP_IDENTIFIERS}`: Relevant alert group identifiers from the SOAR case.
*   *(Optional) `${TIME_FRAME_HOURS}`: Lookback period in hours for SIEM searches (default: 168 = 7 days).*
*   *(Optional) `${SKIP_SOAR}`: Boolean, set to true if no CASE_ID is provided and SOAR documentation should be skipped.*

## Tools

*   `gti-mcp`: `get_ip_address_report`, `get_domain_report`, `get_file_report`, `get_url_report`, `get_entities_related_to_an_ip_address`, `get_entities_related_to_a_domain`, `get_entities_related_to_a_file`, `get_entities_related_to_an_url`, `get_file_behavior_summary` (optional for hashes), `get_collection_report` (optional).
*   `secops-mcp`: `lookup_entity`, `search_security_events`, `get_security_alerts`.
*   `secops-soar`: `post_case_comment`, `get_case_full_details`, `list_cases`.
*   `write_to_file` (for local report generation if skipping SOAR).
*   **Common Steps:** `common_steps/pivot_on_ioc_gti.md`, `common_steps/enrich_ioc.md`, `common_steps/correlate_ioc_with_alerts_cases.md`, `common_steps/find_relevant_soar_case.md`, `common_steps/document_in_soar.md`, `common_steps/generate_report_file.md`.

## Workflow Steps & Diagram

1.  **Receive Input & Context:** Obtain `${IOC_VALUE}`, `${IOC_TYPE}`, optionally `${CASE_ID}`, `${ALERT_GROUP_IDENTIFIERS}`, `${TIME_FRAME_HOURS}`, `${SKIP_SOAR}`. If `${CASE_ID}` is provided and `${SKIP_SOAR}` is not true, get case details via `secops-soar.get_case_full_details`.
2.  **Detailed GTI Report:**
    *   Use the appropriate `gti-mcp.get_..._report` tool based on `${IOC_TYPE}` to retrieve the full GTI analysis report (`${GTI_REPORT_DETAILS}`) for `${IOC_VALUE}`.
    *   Record key details: reputation, classifications, first/last seen dates, associated threats (malware families, actors - `${ASSOCIATED_THREAT_IDS}`), key behaviors (if file hash).
3.  **GTI Pivoting:**
    *   Execute `common_steps/pivot_on_ioc_gti.md` with `${IOC_VALUE}`, `${IOC_TYPE}`, and relevant `${RELATIONSHIP_NAMES}` (determined based on IOC type and report details). Obtain `${RELATED_ENTITIES}`.
    *   *(Optional: If IOC is File Hash, use `gti-mcp.get_file_behavior_summary`)*.
4.  **Deep SIEM Search:**
    *   Use `secops-mcp.search_security_events` with detailed UDM queries covering `${TIME_FRAME_HOURS}` (default 168). Search for:
        *   Activity directly involving `${IOC_VALUE}`.
        *   Activity involving significant IOCs from `${RELATED_ENTITIES}`.
    *   Analyze event details (`${SIEM_SEARCH_RESULTS}`).
    *   **Identify observed related IOCs:** Note any IOCs from `${RELATED_ENTITIES}` that were actually found in the `${SIEM_SEARCH_RESULTS}`. Let this list be `${OBSERVED_RELATED_IOCS}`.
5.  **SIEM Context & Correlation:**
    *   Initialize `SIEM_ENRICHMENT_RESULTS`.
    *   **Prioritize observed IOCs:** For each key IOC `Ki` (including `${IOC_VALUE}` and IOCs in `${OBSERVED_RELATED_IOCS}`):
        *   Execute `common_steps/enrich_ioc.md` with `IOC_VALUE=Ki` and appropriate `IOC_TYPE`. Store results in `SIEM_ENRICHMENT_RESULTS[Ki]`.
    *   *(Note: For related IOCs from GTI not observed in SIEM searches, enrichment can be skipped or performed with lower priority if analyst deems necessary).*
    *   Execute `common_steps/correlate_ioc_with_alerts_cases.md` with `IOC_LIST` containing `${IOC_VALUE}` and `${OBSERVED_RELATED_IOCS}`. Obtain `${RELATED_SIEM_ALERTS}` and `${RELATED_SOAR_CASES_CORRELATION}`.
    *   **Broader Case Search:** Execute `common_steps/find_relevant_soar_case.md` with `SEARCH_TERMS` = list of `${IOC_VALUE}` + `${OBSERVED_RELATED_IOCS}` + key entities from `${SIEM_SEARCH_RESULTS}` (e.g., involved hosts/users) and `CASE_STATUS_FILTER="Opened"`. Obtain `${RELATED_SOAR_CASES_BROAD}`.
6.  **(Optional) Enrich Associated Threats:**
    *   If `${ASSOCIATED_THREAT_IDS}` were identified in Step 2:
        *   For each Threat ID `Ti` in `${ASSOCIATED_THREAT_IDS}`:
            *   Use `gti-mcp.get_collection_report` with `id=Ti` to get context on the associated malware/actor. Store in `${ASSOCIATED_THREAT_DETAILS}`.
7.  **Synthesize & Document/Report:**
    *   Combine all findings: `${GTI_REPORT_DETAILS}`, `${RELATED_ENTITIES}`, `${SIEM_SEARCH_RESULTS}`, `SIEM_ENRICHMENT_RESULTS`, `${RELATED_SIEM_ALERTS}`, `${RELATED_SOAR_CASES_CORRELATION}`, `${RELATED_SOAR_CASES_BROAD}`, `${ASSOCIATED_THREAT_DETAILS}` (optional).
    *   Assess the overall impact and scope. Identify potentially compromised assets or users. Formulate `ASSESSMENT` and `RECOMMENDATION`.
    *   **If `${CASE_ID}` provided and `${SKIP_SOAR}` is not true:**
        *   Prepare `COMMENT_TEXT` summarizing the deep dive: "Deep Dive Analysis for `${IOC_VALUE}` (`${IOC_TYPE}`): GTI Details: [...]. GTI Pivots found: [...]. SIEM Search revealed: [...]. SIEM Enrichment (Observed): [...]. Related Alerts: [...]. Related Cases (Correlation): [...]. Related Cases (Broad Search): [...]. Associated Threats: [...]. Assessment: `${ASSESSMENT}`. Recommendation: `${RECOMMENDATION}`".
        *   Execute `common_steps/document_in_soar.md` with `${CASE_ID}` and `${COMMENT_TEXT}`. Obtain `${COMMENT_POST_STATUS}`.
    *   **Else (No CASE_ID or SKIP_SOAR is true):**
        *   Prepare `REPORT_CONTENT` similar to `COMMENT_TEXT` but formatted for a standalone Markdown report, including a Mermaid diagram of the workflow performed.
        *   Execute `common_steps/generate_report_file.md` with `REPORT_CONTENT`, `REPORT_TYPE="deep_dive_ioc"`, `REPORT_NAME_SUFFIX=${IOC_VALUE}`. Obtain `${REPORT_FILE_PATH}` and `${WRITE_STATUS}`.
8.  **Completion:** Conclude the runbook execution. Inform analyst of completion status and report location (SOAR comment or local file path).

```{mermaid}
sequenceDiagram
    participant Analyst
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant PivotOnIOC as common_steps/pivot_on_ioc_gti.md
    participant SIEM as secops-mcp
    participant EnrichIOC as common_steps/enrich_ioc.md
    participant CorrelateIOC as common_steps/correlate_ioc_with_alerts_cases.md
    participant FindCase as common_steps/find_relevant_soar_case.md
    participant DocumentInSOAR as common_steps/document_in_soar.md
    participant GenerateReport as common_steps/generate_report_file.md
    participant SOAR as secops-soar %% Underlying tool for documentation & context

    Analyst->>Cline: Start Deep Dive IOC Analysis\nInput: IOC_VALUE, IOC_TYPE, CASE_ID (opt), SKIP_SOAR (opt), ...

    %% Step 1: Context
    opt CASE_ID provided AND SKIP_SOAR is false
        Cline->>SOAR: get_case_full_details(case_id=CASE_ID)
        SOAR-->>Cline: Case Details
    end

    %% Step 2: Detailed GTI Report
    Cline->>GTI: get_..._report(ioc=IOC_VALUE) %% Based on IOC_TYPE
    GTI-->>Cline: Detailed GTI Report (GTI_REPORT_DETAILS, ASSOCIATED_THREAT_IDS)

    %% Step 3: GTI Pivoting
    Note over Cline: Determine relevant RELATIONSHIP_NAMES
    Cline->>PivotOnIOC: Execute(Input: IOC_VALUE, IOC_TYPE, RELATIONSHIP_NAMES)
    PivotOnIOC-->>Cline: Results: RELATED_ENTITIES
    opt IOC_TYPE is File Hash
        Cline->>GTI: get_file_behavior_summary(hash=IOC_VALUE)
        GTI-->>Cline: File Behavior Summary
    end

    %% Step 4: Deep SIEM Search
    Note over Cline: Construct UDM queries for IOC_VALUE and RELATED_ENTITIES
    Cline->>SIEM: search_security_events(text=Query1, hours_back=TIME_FRAME_HOURS)
    SIEM-->>Cline: SIEM Search Results 1
    Cline->>SIEM: search_security_events(text=Query2, hours_back=TIME_FRAME_HOURS)
    SIEM-->>Cline: SIEM Search Results 2 (SIEM_SEARCH_RESULTS)
    Note over Cline: Identify OBSERVED_RELATED_IOCS from SIEM_SEARCH_RESULTS

    %% Step 5: SIEM Context & Correlation
    Note over Cline: Initialize SIEM_ENRICHMENT_RESULTS
    Note over Cline: Prepare prioritized IOC list (IOC_VALUE + OBSERVED_RELATED_IOCS)
    loop For each prioritized IOC Ki
        Cline->>EnrichIOC: Execute(Input: IOC_VALUE=Ki, IOC_TYPE=...)
        EnrichIOC-->>Cline: Results: Store in SIEM_ENRICHMENT_RESULTS[Ki]
    end
    Cline->>CorrelateIOC: Execute(Input: IOC_LIST=[Prioritized List], TIME_FRAME_HOURS)
    CorrelateIOC-->>Cline: Results: RELATED_SIEM_ALERTS, RELATED_SOAR_CASES_CORRELATION
    Note over Cline: Prepare broader search list (IOCs + key entities from SIEM results)
    Cline->>FindCase: Execute(Input: SEARCH_TERMS=[Broad List], CASE_STATUS_FILTER="Opened")
    FindCase-->>Cline: Results: RELATED_SOAR_CASES_BROAD

    %% Step 6: Optional Threat Enrichment
    opt ASSOCIATED_THREAT_IDS exist
        loop For each Threat ID Ti
            Cline->>GTI: get_collection_report(id=Ti)
            GTI-->>Cline: Associated Threat Details
        end
    end

    %% Step 7: Synthesize & Document/Report
    Note over Cline: Synthesize all findings, assess impact, prepare COMMENT_TEXT or REPORT_CONTENT with Recommendation
    alt CASE_ID provided AND SKIP_SOAR is false
        Cline->>DocumentInSOAR: Execute(Input: CASE_ID, COMMENT_TEXT)
        DocumentInSOAR-->>Cline: Results: COMMENT_POST_STATUS
        Cline->>Analyst: attempt_completion(result="Deep Dive IOC Analysis complete for IOC_VALUE. Findings documented in case CASE_ID.")
    else No CASE_ID or SKIP_SOAR is true
        Note over Cline: Prepare REPORT_CONTENT including Mermaid diagram
        Cline->>GenerateReport: Execute(Input: REPORT_CONTENT, REPORT_TYPE="deep_dive_ioc", REPORT_NAME_SUFFIX=IOC_VALUE)
        GenerateReport-->>Cline: Results: REPORT_FILE_PATH, WRITE_STATUS
        Cline->>Analyst: attempt_completion(result="Deep Dive IOC Analysis complete for IOC_VALUE. Report generated at REPORT_FILE_PATH.")
    end
