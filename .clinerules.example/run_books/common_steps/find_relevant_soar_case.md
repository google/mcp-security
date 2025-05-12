# Common Step: Find Relevant SOAR Case

## Objective

Identify existing SOAR cases that are potentially relevant to the current investigation based on specific indicators (e.g., IOCs, hostnames, usernames).

## Scope

This sub-runbook executes searches within the SOAR platform's case list based on provided search terms. It returns a list of potentially relevant case IDs. It may involve retrieving basic details for filtering if many initial matches are found.

## Inputs

*   `${SEARCH_TERMS}`: A list of values to search for within cases (e.g., ["e323c6aee8b172b57203a7e478c1caca", "mikeross-pc"]).
*   *(Optional) `${SEARCH_FIELDS}`: A list of fields to search within (e.g., ["entity", "displayName", "description"]). Defaults may vary based on SOAR capabilities.*
*   *(Optional) `${CASE_STATUS_FILTER}`: Filter for case status (e.g., "Opened", "Closed"). Defaults to "Opened".*
*   *(Optional) `${TIME_FRAME_HOURS}`: Lookback period for case creation/update time (if supported by the filter).*
*   *(Optional) `${MAX_RESULTS}`: Maximum number of cases to return.*

## Outputs

*   `${RELEVANT_CASE_IDS}`: A list of case IDs identified as potentially relevant.
*   `${RELEVANT_CASE_SUMMARIES}`: (Optional) A list of brief summaries (ID, DisplayName, Priority) for the found cases.
*   `${FIND_CASE_STATUS}`: Confirmation or status of the search attempt(s).

## Tools

*   `secops-soar`: `list_cases`
*   *(Optional) `secops-soar`: `get_case_full_details` (Potentially used internally if initial list is large and needs filtering based on deeper entity checks)*

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${SEARCH_TERMS}` and optional filters from the calling runbook. Initialize `${RELEVANT_CASE_IDS}` and `${RELEVANT_CASE_SUMMARIES}` as empty.
2.  **Construct Filter:** Create a filter string or structure suitable for the `secops-soar.list_cases` tool based on `${SEARCH_TERMS}`, `${SEARCH_FIELDS}`, `${CASE_STATUS_FILTER}`, and `${TIME_FRAME_HOURS}`. *Note: The exact filter construction is highly dependent on the specific SOAR API capabilities exposed by the `list_cases` tool.* This might involve searching across multiple fields or making multiple calls if necessary.
    *   **Limitation Note:** The current `secops-soar.list_cases` tool may have limited or no capability to directly filter cases based on the *presence* of specific entity values (like IPs, hostnames, users) within the case's alerts or events. Filters might only apply to top-level case fields (e.g., name, description, status).
    *   **Workaround:** If searching for entity relevance, consider:
        *   Using broader filters (e.g., time range, alert type) and then manually reviewing the returned cases or using Step 5 (Refine Results) with `get_case_full_details`.
        *   Performing correlation outside this step (e.g., searching SIEM for the entity and checking if related events belong to a SOAR case).
3.  **Execute Search:** Call `secops-soar.list_cases` with the constructed filter and `${MAX_RESULTS}`.
4.  **Process Results:** Extract the IDs and potentially basic details (DisplayName, Priority) from the returned cases. Store IDs in `${RELEVANT_CASE_IDS}` and summaries in `${RELEVANT_CASE_SUMMARIES}`.
5.  **(Optional) Refine Results:** If the initial search returns too many results, potentially use `get_case_full_details` on a subset to perform more specific checks (e.g., verify if a specific entity is truly present within the alerts/events of the case) and refine the `${RELEVANT_CASE_IDS}` list.
6.  **Return Results:** Set `${FIND_CASE_STATUS}` based on the success/failure of the API calls. Return `${RELEVANT_CASE_IDS}`, `${RELEVANT_CASE_SUMMARIES}`, and `${FIND_CASE_STATUS}` to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant FindCase as find_relevant_soar_case.md (This Runbook)
    participant SOAR as secops-soar

    CallingRunbook->>FindCase: Execute Find Relevant Case\nInput: SEARCH_TERMS, FILTERS (opt)...

    %% Step 2: Construct Filter
    Note over FindCase: Construct filter for list_cases based on SEARCH_TERMS and filters

    %% Step 3: Execute Search
    FindCase->>SOAR: list_cases(filter=..., limit=MAX_RESULTS)
    SOAR-->>FindCase: List of potentially relevant cases

    %% Step 4: Process Results
    Note over FindCase: Extract IDs and Summaries into RELEVANT_CASE_IDS, RELEVANT_CASE_SUMMARIES

    %% Step 5: Optional Refinement (Conceptual)
    opt Initial results need refinement
        loop For subset of found cases
            FindCase->>SOAR: get_case_full_details(case_id=...)
            SOAR-->>FindCase: Detailed Case Info
            Note over FindCase: Filter RELEVANT_CASE_IDS based on details
        end
    end

    %% Step 6: Return Results
    Note over FindCase: Set FIND_CASE_STATUS
    FindCase-->>CallingRunbook: Return Results:\nRELEVANT_CASE_IDS,\nRELEVANT_CASE_SUMMARIES,\nFIND_CASE_STATUS

```

## Completion Criteria

The `list_cases` search has been attempted based on the provided terms. A list of potentially relevant case IDs (`${RELEVANT_CASE_IDS}`) and summaries (`${RELEVANT_CASE_SUMMARIES}`), along with the status (`${FIND_CASE_STATUS}`), are available.
