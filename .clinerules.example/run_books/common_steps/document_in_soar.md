# Common Step: Document Findings/Actions in SOAR Case

## Objective

Add a standardized comment to a specified SOAR case to document findings, actions taken, or recommendations.

## Scope

This sub-runbook executes the `post_case_comment` action in the SOAR platform. It assumes the comment content is provided by the calling runbook.

## Inputs

*   `${CASE_ID}`: The SOAR case ID to add the comment to.
*   `${COMMENT_TEXT}`: The full text of the comment to be added.
*   *(Optional) `${ALERT_GROUP_IDENTIFIERS}`: Relevant alert group identifiers if required by the specific SOAR tool implementation, passed from the calling runbook.*

## Outputs

*   `${COMMENT_POST_STATUS}`: Confirmation or status of the comment posting attempt (e.g., Success, Failure, API response).

## Tools

*   `secops-soar`: `post_case_comment`

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${CASE_ID}`, `${COMMENT_TEXT}`, and optionally `${ALERT_GROUP_IDENTIFIERS}` from the calling runbook.
2.  **Post Comment:** Call `secops-soar.post_case_comment` with `case_id=${CASE_ID}` and `comment=${COMMENT_TEXT}` (and `alert_group_identifiers` if needed).
3.  **Return Status:** Store the result/status of the API call in `${COMMENT_POST_STATUS}` and return it to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant DocumentInSOAR as document_in_soar.md (This Runbook)
    participant SOAR as secops-soar

    CallingRunbook->>DocumentInSOAR: Execute Documentation\nInput: CASE_ID, COMMENT_TEXT, ALERT_GROUP_IDS (opt)

    %% Step 2: Post Comment
    DocumentInSOAR->>SOAR: post_case_comment(case_id=CASE_ID, comment=COMMENT_TEXT, ...)
    SOAR-->>DocumentInSOAR: Comment Post Result (COMMENT_POST_STATUS)

    %% Step 3: Return Status
    DocumentInSOAR-->>CallingRunbook: Return Status:\nCOMMENT_POST_STATUS

```

## Completion Criteria

The `post_case_comment` action has been attempted. The status (`${COMMENT_POST_STATUS}`) is available.
