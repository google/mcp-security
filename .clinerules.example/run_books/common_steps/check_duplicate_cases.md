# Common Step: Check for Duplicate/Similar SOAR Cases

## Objective

Identify potentially duplicate or similar existing SOAR cases based on the context of a current case or alert.

## Scope

This sub-runbook executes the `siemplify_get_similar_cases` action in the SOAR platform using specified criteria. It returns a list of potential duplicate/similar case IDs.

## Inputs

*   `${CASE_ID}`: The ID of the current case to check against.
*   `${ALERT_GROUP_IDENTIFIERS}`: Relevant alert group identifiers for the current case.
*   *(Optional) `${SIMILARITY_CRITERIA}`: A structure or set of flags indicating the criteria for similarity search (e.g., Rule Generator, Port, Entity Identifier - specific to the `siemplify_get_similar_cases` tool).* Defaults might be defined here or passed by the caller.
*   *(Optional) `${DAYS_BACK}`: How many days back to search for similar cases (default could be 7 or passed by caller).*
*   *(Optional) `${INCLUDE_OPEN}`: Boolean, whether to include open cases (default: true).*
*   *(Optional) `${INCLUDE_CLOSED}`: Boolean, whether to include closed cases (default: false).*

## Outputs

*   `${SIMILAR_CASE_IDS}`: A list of case IDs identified as potentially similar or duplicate.
*   `${SIMILARITY_CHECK_STATUS}`: Confirmation or status of the check attempt.

## Tools

*   `secops-soar`: `siemplify_get_similar_cases`

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${CASE_ID}`, `${ALERT_GROUP_IDENTIFIERS}`, and optional criteria (`${SIMILARITY_CRITERIA}`, `${DAYS_BACK}`, etc.) from the calling runbook.
2.  **Check Similar Cases:** Call `secops-soar.siemplify_get_similar_cases` with the provided inputs. Use defaults if optional inputs are not provided.
3.  **Return Results:** Store the list of similar case IDs found in `${SIMILAR_CASE_IDS}` and the status of the check in `${SIMILARITY_CHECK_STATUS}`. Return these to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant CheckDuplicates as check_duplicate_cases.md (This Runbook)
    participant SOAR as secops-soar

    CallingRunbook->>CheckDuplicates: Execute Duplicate Check\nInput: CASE_ID, ALERT_GROUP_IDS, CRITERIA (opt), DAYS_BACK (opt)...

    %% Step 2: Check Similar Cases
    Note over CheckDuplicates: Prepare arguments for siemplify_get_similar_cases
    CheckDuplicates->>SOAR: siemplify_get_similar_cases(case_id=CASE_ID, alert_group_identifiers=ALERT_GROUP_IDS, ...)
    SOAR-->>CheckDuplicates: Similar Case List (SIMILAR_CASE_IDS), Status (SIMILARITY_CHECK_STATUS)

    %% Step 3: Return Results
    CheckDuplicates-->>CallingRunbook: Return Results:\nSIMILAR_CASE_IDS,\nSIMILARITY_CHECK_STATUS

```

## Completion Criteria

The `siemplify_get_similar_cases` action has been attempted. The list of potential similar case IDs (`${SIMILAR_CASE_IDS}`) and the status (`${SIMILARITY_CHECK_STATUS}`) are available.
