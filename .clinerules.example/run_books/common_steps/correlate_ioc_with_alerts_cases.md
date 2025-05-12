# Common Step: Correlate IOC with SIEM Alerts & SOAR Cases

## Objective

Check for existing SIEM alerts and SOAR cases related to a specific Indicator of Compromise (IOC) or a list of IOCs.

## Scope

This sub-runbook executes searches using `secops-mcp.get_security_alerts` and `secops-soar.list_cases` based on provided IOCs. It returns summaries of any related alerts or cases found.

## Inputs

*   `${IOC_LIST}`: A single IOC value or a list of IOC values (e.g., ["198.51.100.10", "evil-domain.com"]).
*   *(Optional) `${TIME_FRAME_HOURS}`: Lookback period in hours for the SIEM alert search (default: 168 = 7 days).*
*   *(Optional) `${SOAR_CASE_FILTER}`: Additional filter criteria for the SOAR case search (e.g., status="OPEN").*

## Outputs

*   `${RELATED_SIEM_ALERTS}`: A list or summary of SIEM alerts found related to the IOC(s).
*   `${RELATED_SOAR_CASES}`: A list or summary of SOAR cases found related to the IOC(s).
*   `${CORRELATION_STATUS}`: Confirmation or status of the correlation attempt(s).

## Tools

*   `secops-mcp`: `get_security_alerts`
*   `secops-soar`: `list_cases`

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${IOC_LIST}`, and optional `${TIME_FRAME_HOURS}`, `${SOAR_CASE_FILTER}` from the calling runbook. Initialize `${RELATED_SIEM_ALERTS}` and `${RELATED_SOAR_CASES}` as empty lists/structures.
2.  **Correlate SIEM Alerts:**
    *   Construct a query for `secops-mcp.get_security_alerts` to search for alerts containing any IOC in `${IOC_LIST}` within the `${TIME_FRAME_HOURS}`. *Note: The exact query format depends on the tool's capabilities.*
    *   Execute the search.
    *   Store the summary of found alerts in `${RELATED_SIEM_ALERTS}`.
3.  **Correlate SOAR Cases:**
    *   Construct a filter for `secops-soar.list_cases` to search for cases containing any IOC in `${IOC_LIST}`. Combine with `${SOAR_CASE_FILTER}` if provided. *Note: The exact filter format depends on the tool's capabilities.*
    *   Execute the search.
    *   Store the summary of found cases in `${RELATED_SOAR_CASES}`.
4.  **Return Results:** Set `${CORRELATION_STATUS}` based on the success/failure of the API calls. Return `${RELATED_SIEM_ALERTS}`, `${RELATED_SOAR_CASES}`, and `${CORRELATION_STATUS}` to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant CorrelateIOC as correlate_ioc_with_alerts_cases.md (This Runbook)
    participant SIEM as secops-mcp
    participant SOAR as secops-soar

    CallingRunbook->>CorrelateIOC: Execute Correlation\nInput: IOC_LIST, TIME_FRAME_HOURS (opt), SOAR_CASE_FILTER (opt)

    %% Step 2: Correlate SIEM Alerts
    Note over CorrelateIOC: Construct SIEM alert query for IOC_LIST
    CorrelateIOC->>SIEM: get_security_alerts(query=..., hours_back=TIME_FRAME_HOURS)
    SIEM-->>CorrelateIOC: Related SIEM Alerts Summary (RELATED_SIEM_ALERTS)

    %% Step 3: Correlate SOAR Cases
    Note over CorrelateIOC: Construct SOAR case filter for IOC_LIST + optional filter
    CorrelateIOC->>SOAR: list_cases(filter=...)
    SOAR-->>CorrelateIOC: Related SOAR Cases Summary (RELATED_SOAR_CASES)

    %% Step 4: Return Results
    Note over CorrelateIOC: Set CORRELATION_STATUS
    CorrelateIOC-->>CallingRunbook: Return Results:\nRELATED_SIEM_ALERTS,\nRELATED_SOAR_CASES,\nCORRELATION_STATUS

```

## Completion Criteria

The SIEM alert search and SOAR case search have been attempted. Summaries of related alerts (`${RELATED_SIEM_ALERTS}`) and cases (`${RELATED_SOAR_CASES}`), along with the status (`${CORRELATION_STATUS}`), are available.
