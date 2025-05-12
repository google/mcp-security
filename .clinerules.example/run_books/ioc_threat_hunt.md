# Runbook: IOC Threat Hunt (Placeholder)

## Objective

*(Define the goal, e.g., To proactively hunt for specific Indicators of Compromise (IOCs) across the environment based on threat intelligence feeds, recent incidents, or specific hypotheses.)*

## Scope

*(Define what is included/excluded, e.g., Focuses on searching SIEM and potentially other log sources for specific IOC values (IPs, domains, hashes, URLs). May include basic enrichment of findings.)*

## Inputs

*   `${IOC_LIST}`: Comma-separated list of IOC values to hunt for.
*   `${IOC_TYPES}`: Corresponding comma-separated list of IOC types (e.g., "IP Address, Domain, File Hash").
*   `${HUNT_TIMEFRAME_HOURS}`: Lookback period in hours (e.g., 72, 168).
*   *(Optional) `${HUNT_CASE_ID}`: SOAR case ID for tracking.*
*   *(Optional) `${REASON_FOR_HUNT}`: Brief description why these IOCs are being hunted.*

## Tools

*   `secops-mcp`: `search_security_events`, `lookup_entity`, `get_ioc_matches`
*   `gti-mcp`: (Relevant enrichment tools like `get_ip_address_report`, `get_domain_report`, etc.)
*   `secops-soar`: `post_case_comment` (for documenting hunt/findings)

## Workflow Steps & Diagram

1.  **Receive Inputs:** Obtain `${IOC_LIST}`, `${IOC_TYPES}`, `${HUNT_TIMEFRAME_HOURS}`, etc.
2.  **Initial Check (Optional):** Use `secops-mcp.get_ioc_matches` to see if any IOCs in the list have recent matches in the SIEM's integrated feeds.
3.  **Iterative SIEM Search:**
    *   For each IOC in `${IOC_LIST}`:
        *   Construct appropriate UDM queries for `secops-mcp.search_security_events` based on the IOC value and type.
        *   Execute the search over `${HUNT_TIMEFRAME_HOURS}`.
        *   Analyze results for any hits (e.g., network connections, file executions, DNS lookups).
4.  **Enrich Findings:**
    *   If hits are found for an IOC:
        *   Use `secops-mcp.lookup_entity` for the IOC and any involved entities (hosts, users).
        *   Use relevant `gti-mcp` tools to enrich the IOC itself.
5.  **Document Hunt & Findings:**
    *   Use `secops-soar.post_case_comment` in `${HUNT_CASE_ID}` (if provided) or a dedicated hunt case.
    *   Document: IOCs Hunted, Timeframe, Queries Used, Summary of Findings (including IOCs with no hits), Details of any confirmed hits and enrichment data.
6.  **Escalate or Conclude:**
    *   If confirmed malicious activity related to the hunted IOCs is found, escalate by creating/updating an incident case.
    *   If no significant findings, conclude the hunt and document it.

```{mermaid}
sequenceDiagram
    participant Analyst/Hunter
    participant Cline as Cline (MCP Client)
    participant SIEM as secops-mcp
    participant GTI as gti-mcp
    participant SOAR as secops-soar

    Analyst/Hunter->>Cline: Start IOC Threat Hunt\nInput: IOC_LIST, IOC_TYPES, HUNT_TIMEFRAME_HOURS, ...

    %% Step 2: Initial Check (Optional)
    opt Check IOC Matches
        Cline->>SIEM: get_ioc_matches(hours_back=HUNT_TIMEFRAME_HOURS)
        SIEM-->>Cline: Recent IOC Matches
        Note over Cline: Correlate with IOC_LIST
    end

    %% Step 3: Iterative SIEM Search
    loop For each IOC Ii in IOC_LIST
        Note over Cline: Construct UDM query Qi for Ii
        Cline->>SIEM: search_security_events(text=Qi, hours_back=HUNT_TIMEFRAME_HOURS)
        SIEM-->>Cline: Search Results for Ii
        Note over Cline: Analyze results for hits
    end

    %% Step 4: Enrich Findings
    opt Hits Found for IOC Ij (Involved Entities E1, E2...)
        Cline->>SIEM: lookup_entity(entity_value=Ij)
        SIEM-->>Cline: SIEM Summary for Ij
        Cline->>GTI: get_..._report(ioc=Ij)
        GTI-->>Cline: GTI Enrichment for Ij
        loop For each Involved Entity Ek (E1, E2...)
            Cline->>SIEM: lookup_entity(entity_value=Ek)
            SIEM-->>Cline: SIEM Summary for Ek
        end
    end

    %% Step 5: Document Hunt
    Cline->>SOAR: post_case_comment(case_id=HUNT_CASE_ID, comment="IOC Hunt Summary: IOCs [...], Findings [...], Enrichment [...]")
    SOAR-->>Cline: Comment Confirmation

    %% Step 6: Escalate or Conclude
    alt Confirmed Activity Found
        Note over Cline: Escalate findings (Create/Update Incident Case)
        Cline->>Analyst/Hunter: attempt_completion(result="IOC Hunt complete. Findings escalated.")
    else No Significant Findings
        Cline->>Analyst/Hunter: attempt_completion(result="IOC Hunt complete. No significant findings. Hunt documented.")
    end
```

## Completion Criteria

*(Define how successful completion is determined, e.g., All IOCs searched, results analyzed, findings documented/escalated.)*
