# Common Step: Confirm Action with User

## Objective

Ask the user a follow-up question to confirm whether a specific action should be taken before proceeding.

## Scope

This sub-runbook executes the `ask_followup_question` tool with a provided question and optional response options. It returns the user's response to the calling runbook.

## Inputs

*   `${QUESTION_TEXT}`: The specific question to ask the user (e.g., "Isolate endpoint ENDPOINT_ID?", "Proceed with containment for IOC_VALUE?").
*   *(Optional) `${RESPONSE_OPTIONS}`: A list of predefined options for the user to choose from (e.g., ["Yes", "No"], ["Disable Account", "Reset Password", "Monitor Only"]).*

## Outputs

*   `${USER_RESPONSE}`: The response provided by the user to the question.

## Tools

*   `ask_followup_question`

## Workflow Steps & Diagram

1.  **Receive Input:** Obtain `${QUESTION_TEXT}` and optionally `${RESPONSE_OPTIONS}` from the calling runbook.
2.  **Ask Question:** Call `ask_followup_question` with `question=${QUESTION_TEXT}` and `options=${RESPONSE_OPTIONS}` (if provided).
3.  **Return Response:** Store the user's response in `${USER_RESPONSE}` and return it to the calling runbook.

```{mermaid}
sequenceDiagram
    participant CallingRunbook
    participant ConfirmAction as confirm_action.md (This Runbook)
    participant User

    CallingRunbook->>ConfirmAction: Execute Confirmation\nInput: QUESTION_TEXT, RESPONSE_OPTIONS (opt)

    %% Step 2: Ask Question
    ConfirmAction->>User: ask_followup_question(question=QUESTION_TEXT, options=RESPONSE_OPTIONS)
    User-->>ConfirmAction: User Response (USER_RESPONSE)

    %% Step 3: Return Response
    ConfirmAction-->>CallingRunbook: Return Response:\nUSER_RESPONSE

```

## Completion Criteria

The `ask_followup_question` action has been executed. The user's response (`${USER_RESPONSE}`) is available.
