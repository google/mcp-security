# Common Step: Enrich IOC (GTI + SIEM)

## Objective

Perform standardized initial enrichment for a single Indicator of Compromise (IOC) using Google Threat Intelligence (GTI) and Chronicle SIEM lookup tools.

## Scope

This sub-runbook covers retrieving the primary GTI report for the IOC, performing a basic SIEM entity lookup, and checking against recent SIEM IOC matches. It returns structured data for use in the calling runbook.

## Inputs

*   `${IOC_VALUE}`: The specific IOC value (e.g., "198.51.100.10", "evil-domain.com", "abcdef123456...", "http://bad.url/path").
*   `${IOC_TYPE}`: The type of IOC ("IP Address", "Domain", "File Hash", "URL").

## Outputs

*   `${GTI_FINDINGS}`: Summary of key findings from the relevant GTI report (e.g., reputation, classification, key relationships).
*   `${SIEM_ENTITY_SUMMARY}`: Summary from the SIEM entity lookup (e.g., first/last seen, related alerts).
*   `${SIEM_IOC_MATCH_STATUS}`: Boolean or indicator (Yes/No) if the IOC was found in recent SIEM IOC matches.

## Tools

*   `gti-mcp`: `get_ip_address_report`, `get_domain_report`, `get_file_report`, `get_url_report`
*   `secops-mcp`: `lookup_entity`, `get_ioc_matches`

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${IOC_VALUE}` and `${IOC_TYPE}` from the calling runbook.
2.  **GTI Enrichment:**
    *   Based on `${IOC_TYPE}`, call the appropriate `gti-mcp` tool (`get_ip_address_report`, `get_domain_report`, `get_file_report`, or `get_url_report`) with `${IOC_VALUE}`.
    *   Store the summary output in `${GTI_FINDINGS}`.
    *   **Error Handling:** If the GTI tool fails (e.g., due to API quota limits or the IOC not being found), note this limitation in `${GTI_FINDINGS}` (e.g., "GTI lookup failed: Quota Exceeded") and proceed. Rely more heavily on SIEM context in subsequent steps.
3.  **SIEM Context - Entity Lookup:**
    *   Call `secops-mcp.lookup_entity` with `entity_value=${IOC_VALUE}`.
    *   Store the summary output in `${SIEM_ENTITY_SUMMARY}`.
4.  **SIEM Context - IOC Match Check:**
    *   Call `secops-mcp.get_ioc_matches`.
    *   Check if `${IOC_VALUE}` exists in the results.
    *   Store the result (Yes/No) in `${SIEM_IOC_MATCH_STATUS}`.
5.  **Return Results:** Provide `${GTI_FINDINGS}`, `${SIEM_ENTITY_SUMMARY}`, and `${SIEM_IOC_MATCH_STATUS}` back to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant EnrichIOC as enrich_ioc.md (This Runbook)
    participant GTI as gti-mcp
    participant SIEM as secops-mcp

    CallingRunbook->>EnrichIOC: Execute Enrichment\nInput: IOC_VALUE, IOC_TYPE

    %% Step 2: GTI Enrichment
    alt IOC_TYPE is IP Address
        EnrichIOC->>GTI: get_ip_address_report(ip_address=IOC_VALUE)
        GTI-->>EnrichIOC: IP Report Summary (GTI_FINDINGS)
    else IOC_TYPE is Domain
        EnrichIOC->>GTI: get_domain_report(domain=IOC_VALUE)
        GTI-->>EnrichIOC: Domain Report Summary (GTI_FINDINGS)
    else IOC_TYPE is File Hash
        EnrichIOC->>GTI: get_file_report(hash=IOC_VALUE)
        GTI-->>EnrichIOC: File Report Summary (GTI_FINDINGS)
    else IOC_TYPE is URL
        EnrichIOC->>GTI: get_url_report(url=IOC_VALUE)
        GTI-->>EnrichIOC: URL Report Summary (GTI_FINDINGS)
    end

    %% Step 3: SIEM Entity Lookup
    EnrichIOC->>SIEM: lookup_entity(entity_value=IOC_VALUE)
    SIEM-->>EnrichIOC: SIEM Entity Summary (SIEM_ENTITY_SUMMARY)

    %% Step 4: SIEM IOC Match Check
    EnrichIOC->>SIEM: get_ioc_matches()
    SIEM-->>EnrichIOC: List of Recent IOC Matches
    Note over EnrichIOC: Check if IOC_VALUE is in list. Set SIEM_IOC_MATCH_STATUS (Yes/No).

    %% Step 5: Return Results
    EnrichIOC-->>CallingRunbook: Return Results:\nGTI_FINDINGS,\nSIEM_ENTITY_SUMMARY,\nSIEM_IOC_MATCH_STATUS

```

## Completion Criteria

GTI enrichment, SIEM entity lookup, and SIEM IOC match check completed. Structured results (`${GTI_FINDINGS}`, `${SIEM_ENTITY_SUMMARY}`, `${SIEM_IOC_MATCH_STATUS}`) are available.
