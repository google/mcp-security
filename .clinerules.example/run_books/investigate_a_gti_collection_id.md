# Investigate Google Threat Intelligence Collection ID (Enhanced)

Objective: Investigate Google Threat Intelligence Collection ID provided by the user `${COLLECTION_ID}`. Enrich findings with detailed entity reports and correlate with the local environment (SIEM/SOAR). Create a timestamped markdown report summarizing findings, correlations, and recommended actions.

Instructions:

1.  **Initial Collection Context:**
    *   Use the `get_collection_report` tool from the `Google Threat Intelligence MCP server` (gti-mcp).
    *   Provide the argument: `id`: `${COLLECTION_ID}`.
    *   Record the collection details, especially the `collection_type`.

2.  **Define Relationships to Investigate:**
    *   Based on the `collection_type` (from Step 1), determine a prioritized list of relevant relationships. (Default: `["associations", "attack_techniques", "domains", "files", "ip_addresses", "urls", "threat_actors", "malware_families", "software_toolkits", "campaigns", "vulnerabilities", "reports", "suspected_threat_actors"]`, but can be narrowed). Let's call this `RELATIONSHIP_LIST`.

3.  **Iterative GTI Relationship Investigation:**
    *   Initialize an empty data structure (e.g., `gti_findings`) to store results.
    *   Loop through each `relationship_name` in `RELATIONSHIP_LIST`.
    *   Use the `get_entities_related_to_a_collection` tool (gti-mcp).
    *   Arguments: `id`: `${COLLECTION_ID}`, `relationship_name`: current relationship name.
    *   Store the results in `gti_findings` under the corresponding `relationship_name`.

4.  **Detailed GTI Entity Enrichment:**
    *   Initialize an empty data structure (e.g., `enriched_entities`) to store detailed reports.
    *   Iterate through key entity types found in `gti_findings` (e.g., domains, files, ip_addresses).
    *   For each entity found:
        *   If it's a domain, use `get_domain_report` (gti-mcp) with the domain name. Store the result.
        *   If it's a file (hash), use `get_file_report` (gti-mcp) with the hash. Store the result.
        *   If it's an IP address, use `get_ip_address_report` (gti-mcp) with the IP. Store the result.
        *   *(Add other relevant enrichment tools if needed, e.g., `get_url_report`)*.

5.  **Local Environment Correlation (SIEM/SOAR):**
    *   Initialize an empty data structure (e.g., `local_findings`) to store correlation results.
    *   Iterate through key IOCs found (domains, files, IPs from `gti_findings`).
    *   For each IOC:
        *   Use `lookup_entity` (secops-mcp) with `entity_value` = IOC. Store summary.
        *   Use `search_security_events` (secops-mcp) with `text` query related to the IOC (e.g., "Events involving IP 1.2.3.4"). Store key event findings.
    *   *(Optional: Check if related threat actors/campaigns match existing SOAR cases using `list_cases` (secops-soar) with appropriate filters)*.

6.  **Data Synthesis and Formatting:**
    *   Initialize an empty markdown string for the report content.
    *   Add a main title and summary section mentioning the Collection ID.
    *   **Add "Key Findings & Recommendations" section:** Summarize critical entities, highlight correlations between GTI and local findings, and list actionable next steps.
    *   Iterate through `gti_findings` and `enriched_entities`:
        *   Add sections for each relationship type investigated.
        *   List entities found. For enriched entities, include key details from their detailed reports (Step 4). Note relationships with no findings.
    *   Add a "Local Environment Correlation" section:
        *   Summarize results from `lookup_entity` and `search_security_events` for each checked IOC. Highlight any matches or significant activity.

7.  **Report Creation:**
    *   Generate a timestamp string (`yyyymmdd_hhmm`).
    *   Construct filename: `./reports/enhanced_report_${COLLECTION_ID}_${timestamp}.md`.
    *   Use the `write_to_file` tool.
    *   Arguments: `path`: constructed filename, `content`: complete formatted markdown string.

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    User->>Cline: Investigate GTI Collection ID `${COLLECTION_ID}` (Enhanced)

    %% Step 1: Initial Collection Context
    Cline->>GTI: get_collection_report(id=`${COLLECTION_ID}`)
    GTI-->>Cline: Collection Details (Type: T)

    %% Step 2 & 3: Define & Investigate Relationships
    Note over Cline: Determine RELATIONSHIP_LIST based on Type T
    loop For each relationship_name in RELATIONSHIP_LIST
        Cline->>GTI: get_entities_related_to_a_collection(id=`${COLLECTION_ID}`, relationship_name=...)
        GTI-->>Cline: Related Entities (E1, E2...) for relationship
        Note over Cline: Store entities in gti_findings
    end

    %% Step 4: Detailed GTI Entity Enrichment
    Note over Cline: Initialize enriched_entities
    loop For each key Entity Ei in gti_findings (Files, Domains, IPs)
        alt Entity is File (Hash H)
            Cline->>GTI: get_file_report(hash=H)
            GTI-->>Cline: File Report for H
            Note over Cline: Store in enriched_entities
        else Entity is Domain (D)
            Cline->>GTI: get_domain_report(domain=D)
            GTI-->>Cline: Domain Report for D
            Note over Cline: Store in enriched_entities
        else Entity is IP Address (IP)
            Cline->>GTI: get_ip_address_report(ip_address=IP)
            GTI-->>Cline: IP Report for IP
            Note over Cline: Store in enriched_entities
        end
    end

    %% Step 5: Local Environment Correlation
    Note over Cline: Initialize local_findings
    loop For each key IOC Ii from gti_findings (Files, Domains, IPs)
        Cline->>SIEM: lookup_entity(entity_value=Ii)
        SIEM-->>Cline: SIEM Entity Summary for Ii
        Note over Cline: Store in local_findings
        Cline->>SIEM: search_security_events(text="Events involving Ii")
        SIEM-->>Cline: Relevant SIEM Events for Ii
        Note over Cline: Store in local_findings
    end
    %% Optional SOAR Check (Conceptual)
    %% Cline->>SOAR: list_cases(filter="Related to Campaign/Actor from GTI")
    %% SOAR-->>Cline: Potentially related SOAR cases

    %% Step 6 & 7: Synthesize Report and Write File
    Note over Cline: Synthesize report content from gti_findings, enriched_entities, local_findings
    Note over Cline: Include Key Findings & Recommendations
    Cline->>Cline: write_to_file(path="./reports/enhanced_report_${COLLECTION_ID}_${timestamp}.md", content=...)
    Note over Cline: Report file created

    Cline->>User: attempt_completion(result="Enhanced investigation complete. Report generated.")
