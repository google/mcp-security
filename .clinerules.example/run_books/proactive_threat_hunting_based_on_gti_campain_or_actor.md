## Proactive Threat Hunting based on GTI Campaign/Actor

Objective: Given a GTI Campaign or Threat Actor Collection ID (`${GTI_COLLECTION_ID}`), proactively search the local environment (SIEM) for related IOCs and TTPs (approximated by searching related entities). If any IOCs from the report are also found in the SecOps tenant (confirmed presence), perform deeper enrichment on those specific IOCs using GTI and check for related SIEM alerts or SOAR cases. Once done, summarize findings in a markdown report. Provide as much detail as possible.

Uses Tools:

*   `gti-mcp.get_collection_report`
*   `gti-mcp.get_entities_related_to_a_collection` (Initial IOC gathering)
*   `gti-mcp.get_collection_timeline_events` (for TTP context)
*   `secops-mcp.get_ioc_matches` (Initial SIEM check)
*   `secops-mcp.lookup_entity` (SIEM check for specific IOCs)
*   `secops-mcp.search_security_events` (SIEM check for specific IOCs)
*   **`gti-mcp.get_domain_report` / `get_file_report` / `get_ip_address_report` / `get_url_report` (Deeper GTI enrichment for *found* IOCs)**
*   **`gti-mcp.get_entities_related_to_a_domain/file/ip/url` (Pivot on *found* IOCs)**
*   **`secops-mcp.get_security_alerts` (Check related SIEM alerts for *found* IOCs/hosts)**
*   **(Optional) `gti-mcp.get_file_behavior_summary` (For found file hashes)**
*   `write_to_file` (for report generation)
*   `secops-soar`: `post_case_comment` (optional), `list_cases`
*   `ask_followup_question`
*   **Common Steps:** `common_steps/find_relevant_soar_case.md`

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar
    participant FindCase as common_steps/find_relevant_soar_case.md

    User->>Cline: Hunt for Campaign/Actor: `${GTI_COLLECTION_ID}`
    Cline->>GTI: get_collection_report(id=`${GTI_COLLECTION_ID}`)
    GTI-->>Cline: Collection Details (Name, Type, Description)
    Cline->>GTI: get_collection_timeline_events(id=`${GTI_COLLECTION_ID}`)
    GTI-->>Cline: Timeline Events (TTP Context)

    Note over Cline: Identify relevant IOC relationships (files, domains, ips, urls)
    loop For each IOC Relationship R
        Cline->>GTI: get_entities_related_to_a_collection(id=`${GTI_COLLECTION_ID}`, relationship_name=R)
        GTI-->>Cline: List of IOCs (e.g., Hashes H1, Domains D1, IPs IP1...)
    end

    Note over Cline: Initialize local_hunt_findings
    Cline->>SIEM: get_ioc_matches(hours_back=72)
    SIEM-->>Cline: Recent IOC Matches in SIEM (Matches M1, M2...)
    Note over Cline: Identify key IOCs from GTI (I1, I2...) and SIEM matches (M1, M2...)

    Note over Cline: Phase 1: Lookup key/prioritized IOCs
    loop For each prioritized IOC Ii (from GTI/SIEM Matches)
        Cline->>SIEM: lookup_entity(entity_value=Ii, hours_back=72)
        SIEM-->>Cline: SIEM Summary for Ii
        Note over Cline: Record IOCs with confirmed presence (P1, P2...)
    end

    Note over Cline: Phase 2: Deeper investigation for IOCs with confirmed presence (P1, P2...)
    loop For each Present IOC Pi
        Note over Cline: Search SIEM Events
        Cline->>SIEM: search_security_events(text="Events involving Pi", hours_back=72)
        SIEM-->>Cline: Relevant SIEM Events for Pi (Note involved hosts Hi)
        Note over Cline: Store significant event findings

        Note over Cline: Deeper GTI Enrichment & Pivoting
        alt IOC Pi is Domain
            Cline->>GTI: get_domain_report(domain=Pi)
            GTI-->>Cline: Detailed Domain Report
            Cline->>GTI: get_entities_related_to_a_domain(domain=Pi, relationship_name="resolutions")
            GTI-->>Cline: Related IPs
            Cline->>GTI: get_entities_related_to_a_domain(domain=Pi, relationship_name="communicating_files")
            GTI-->>Cline: Related Files
        else IOC Pi is File Hash
            Cline->>GTI: get_file_report(hash=Pi)
            GTI-->>Cline: Detailed File Report
            Cline->>GTI: get_entities_related_to_a_file(hash=Pi, relationship_name="contacted_domains")
            GTI-->>Cline: Related Domains
            Cline->>GTI: get_entities_related_to_a_file(hash=Pi, relationship_name="contacted_ips")
            GTI-->>Cline: Related IPs
            %% Optional: Cline->>GTI: get_file_behavior_summary(hash=Pi)
            %% GTI-->>Cline: Behavior Summary
        else IOC Pi is IP Address
            Cline->>GTI: get_ip_address_report(ip_address=Pi)
            GTI-->>Cline: Detailed IP Report
            Cline->>GTI: get_entities_related_to_an_ip_address(ip_address=Pi, relationship_name="resolutions")
            GTI-->>Cline: Related Domains
            Cline->>GTI: get_entities_related_to_an_ip_address(ip_address=Pi, relationship_name="communicating_files")
            GTI-->>Cline: Related Files
        end
        Note over Cline: Store enrichment and pivot findings

        Note over Cline: Check Related SIEM Alerts & SOAR Cases
        Cline->>SIEM: get_security_alerts(query="alert contains Pi or involves host Hi", hours_back=72)
        SIEM-->>Cline: Related SIEM Alerts (Store findings)
        Note over Cline: Prepare search terms (Pi + Hi)
        Cline->>FindCase: Execute(Input: SEARCH_TERMS=[Pi, Hi], CASE_STATUS_FILTER="Opened")
        FindCase-->>Cline: Results: RELATED_SOAR_CASES (Store findings)
    end

    Note over Cline: Synthesize GTI context, IOCs, TTPs, SIEM findings, Enrichment, Related Alerts & Cases
    Cline->>User: ask_followup_question(question="Hunt found potential activity related to `${GTI_COLLECTION_ID}`. Create/Update SOAR Case or Generate Report?", options=["Create New Case", "Update Case [ID]", "Generate Report", "Do Nothing"])
    User->>Cline: Response (e.g., "Generate Report")

    alt Output Action Confirmed
        alt Create/Update Case
            Note over Cline: Prepare summary comment for SOAR
            Cline->>SOAR: post_case_comment(case_id=[New/Existing ID], comment="Proactive Hunt Summary for `${GTI_COLLECTION_ID}`: Found IOCs [...] in SIEM. Events [...] observed. GTI Context: [...].")
            SOAR-->>Cline: Comment confirmation
            Cline->>Cline: attempt_completion(result="Proactive threat hunt for `${GTI_COLLECTION_ID}` complete. Findings summarized. SOAR case created/updated.")
        else Generate Report
            Note over Cline: Synthesize report content
            Cline->>Cline: write_to_file(path="./reports/proactive_hunt_report_${GTI_COLLECTION_ID}_${timestamp}.md", content=...)
            Note over Cline: Report file created locally.
            Cline->>Cline: attempt_completion(result="Proactive threat hunt for `${GTI_COLLECTION_ID}` complete. Report generated.")
        else Do Nothing
             Cline->>Cline: attempt_completion(result="Proactive threat hunt for `${GTI_COLLECTION_ID}` complete. Findings summarized. No output action taken.")
        end
    end
