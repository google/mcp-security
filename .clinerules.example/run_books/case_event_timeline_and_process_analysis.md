## Case Event Timeline & Process Analysis Workflow

Objective: Generate a detailed timeline of events for a specific SOAR case (`${CASE_ID}`), including the **full process execution chain** leading to the alerted activity. Classify relevant processes as legitimate, LOLBIN, or malicious using GTI enrichment. Optionally enrich with MITRE TACTICs and generate a markdown report summarizing the findings. Optionally convert the report to PDF and attempt to attach it to the SOAR case.

Uses Tools:

*   `secops-soar.get_case_full_details` (Provides initial context and alerts)
*   `secops-soar.list_events_by_alert`
*   **`secops-mcp.search_security_events` (Crucial for finding parent process launch events)**
*   `secops-soar.google_chronicle_list_events` (To get broader asset context)
*   `secops-soar.google_chronicle_get_rule_details` (Optional, for specific rule context)
*   `secops-soar.google_chronicle_get_detection_details` (Optional, for specific detection context)
*   `gti-mcp.get_file_report` (for process hash classification)
*   `secops-mcp.get_threat_intel` (for MITRE TACTIC mapping/general enrichment)
*   `siemplify_create_gemini_case_summary` (Optional, for AI-generated summary)
*   `write_to_file` (for report generation)
*   `execute_command` (using `pandoc` for PDF conversion)
*   `secops-soar.post_case_comment` (to note report location/attach if possible)
*   `ask_followup_question` (for report format/content/attachment/SOAR actions confirmation)
*   `attempt_completion`
*   *(Optional SOAR Actions based on user confirmation):* `siemplify_case_tag`, `siemplify_change_priority`, `siemplify_add_general_insight`, `siemplify_update_case_description`, `siemplify_assign_case`, `siemplify_raise_incident`, `siemplify_create_gemini_case_summary`

**Workflow Steps & Diagram:**

1.  Get full case details (including alerts and comments) for `${CASE_ID}` using `get_case_full_details`.
2.  For each alert obtained in Step 1, list the associated events using `list_events_by_alert`.
3.  (Optional) If alert/event data contains specific Chronicle Rule IDs or Detection IDs, use `google_chronicle_get_rule_details` or `google_chronicle_get_detection_details` for more context.
4.  Extract key process information (PID, Parent PID, Hash, Path, CmdLine) and involved assets (Hostnames, IPs) from the events obtained in Step 2.
5.  **CRITICAL STEP: Find Parent Process Chain:** Iteratively search for `PROCESS_LAUNCH` events to trace the parent process chain backward from the initial alert events.
    *   **Start:** Identify the parent process PID (or `productSpecificProcessId`) from the initial alert events (Step 2). Let this be `Current_Parent_PID`. Identify the timestamp of the *child* process launch (`Child_Timestamp`).
    *   **Iterate:**
        *   Search SIEM (`secops-mcp.search_security_events`) for `PROCESS_LAUNCH` events where the *target* process PID matches `Current_Parent_PID`.
        *   **Time Window:** Use a focused time window around `Child_Timestamp` (e.g., +/- 15 minutes or +/- 1 hour).
        *   **Identifiers:** Attempt searches using both the principal hostname (if known) and principal IP address associated with the child process.
        *   **Store:** If the launch event for `Current_Parent_PID` is found, store its details (parent PID, command line, timestamp, etc.) in the process chain data. Update `Current_Parent_PID` to the *newly found parent's PID* and update `Child_Timestamp` to the timestamp of the event just found. Repeat the search.
        *   **Stop:** Continue iterating backward until a known root process (e.g., `explorer.exe`, `services.exe`) is reached, the parent PID is null/invalid, or the search yields no results within a reasonable timeframe.
    *   **Troubleshooting:** If `search_security_events` fails, times out, or returns no results:
        *   Try broadening the time window for the specific parent search (e.g., +/- 1 hour, +/- 6 hours). Be aware this may increase noise.
        *   Consider using `secops-soar.google_chronicle_list_events` filtered for `metadata.event_type = "PROCESS_LAUNCH"` on the specific asset around the expected time as an alternative.
        *   If parent process launch events are still elusive, consider searching for other related activity (e.g., user logins, network connections) associated with the parent process around its estimated start time to infer context.
        *   **Acknowledge Limitations:** Note that tracing the full chain might not always be possible due to log availability, timing discrepancies, unusual process IDs (e.g., PID 4), or processes starting before the log retention/search window.
    *   Store all found launch event details chronologically.
6.  (Optional) For key involved assets identified in Step 4, use `google_chronicle_list_events` to get broader event context for those assets around the alert time.
7.  Enrich process hashes using GTI (`get_file_report`) to classify processes (Legitimate, LOLBIN, Malicious).
8.  (Optional) Enrich activities with potential MITRE TACTICs using `get_threat_intel`.
9.  Synthesize the collected data (case details, alert events, parent process events, asset events, enrichments), sorting events chronologically.
10. (Optional) Generate an AI summary using `siemplify_create_gemini_case_summary`.
11. Format the report in Markdown, ensuring it **MUST** include:
    *   A summary section (incorporating initial case details and optionally the Gemini summary).
    *   A **Process Execution Tree (Text)** showing the parent-child chain *as determined*. If the full chain could not be traced, clearly indicate where the tracing stopped (e.g., `[PID ???]`).
    *   A **Process Execution Tree (Diagram)** using Mermaid (`graph LR`), similarly reflecting the extent of the traced chain.
    *   An **Event Timeline Table** including timestamps, classifications, and optional MITRE TACTICs/time deltas.
    *   An analysis section.
    *   *(Report Limitation Note):* If the full process chain could not be determined, explicitly state this limitation in the report summary or analysis section.
12. Ask the user to confirm report generation and format preferences (e.g., include time delta, include Gemini summary).
13. Write the Markdown report to a timestamped file (e.g., `./reports/case_${CASE_ID}_timeline_${timestamp}.md`).
14. (Optional, based on user feedback) Convert the Markdown report to PDF using `pandoc` via `execute_command`.
15. (Optional, based on user feedback) Attempt to attach the PDF to the SOAR case. *Note: Direct PDF attachment might require specific SOAR tools not always available. If attachment fails, post a comment with the local path to the MD/PDF report.*
16. (Optional, based on user feedback) Ask the user if they want to perform additional SOAR actions (tagging, priority change, insight, description update, assignment, incident declaration).
17. (Optional, based on user feedback) Execute selected SOAR actions.
18. Conclude with `attempt_completion`.

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as gti-mcp

    User->>Cline: Generate timeline for Case `${CASE_ID}` with full process tree

    %% Step 1: Get Initial Case Details & Alerts
    Cline->>SOAR: get_case_full_details(case_id=`${CASE_ID}`)
    SOAR-->>Cline: Case Details, List of Alerts (A1, A2...), Comments

    Note over Cline: Initialize timeline_data = [], process_chain = {}, assets = set()
    Note over Cline: Use Alerts (A1, A2...) from get_case_full_details response

    %% Step 2 & 3: Get Events & Optional Rule/Detection Details
    loop For each Alert Ai
        Cline->>SOAR: list_events_by_alert(case_id=`${CASE_ID}`, alert_id=Ai)
        SOAR-->>Cline: Events for Alert Ai (E1, E2...)
        Note over Cline: Extract Process Info (PID P1, Parent PID PP1, Hash H1...), Assets (Host H, IP I...) & store in timeline_data, process_chain, assets
        Note over Cline: Extract Rule ID Ri, Detection ID Di if available
        opt Rule ID Ri available
            Cline->>SOAR: google_chronicle_get_rule_details(rule_id=Ri, ...)
            SOAR-->>Cline: Rule Details
        end
        opt Detection ID Di available
            Cline->>SOAR: google_chronicle_get_detection_details(detection_id=Di, ...)
            SOAR-->>Cline: Detection Details
        end
        alt Process Hash H1 available
            Cline->>GTI: get_file_report(hash=H1)
            GTI-->>Cline: GTI Report for Hash H1 -> Classify P1
        end
    end

    %% Step 5: Find Parent Processes
    Note over Cline: **CRITICAL: Find Parent Processes**
    Note over Cline: Current PID = PP1 (from initial events)
    loop While Current PID is valid & not root
        Cline->>SIEM: search_security_events(text="PROCESS_LAUNCH for target PID Current PID")
        SIEM-->>Cline: Launch Event (Parent PID PP_Next, CmdLine...)
        Note over Cline: Store launch event in timeline_data
        Note over Cline: Add Current PID, PP_Next to process_chain
        Note over Cline: Current PID = PP_Next
    end

    %% Step 6: Optional Asset Event Search
    opt Assets identified
        loop For each Asset As in assets
            Cline->>SOAR: google_chronicle_list_events(target_entities=[{Identifier: As, ...}], time_frame=...)
            SOAR-->>Cline: Broader events for Asset As
            Note over Cline: Add relevant asset events to timeline_data
        end
    end

    Note over Cline: Sort timeline_data by time

    %% Step 8: Optional MITRE Enrichment
    Note over Cline: (Optional) Enrich with MITRE TACTICs
    loop For each relevant entry in timeline_data
        Cline->>SIEM: get_threat_intel(query="MITRE TACTIC for [activity description]")
        SIEM-->>Cline: Potential TACTIC(s)
    end

    %% Step 10: Optional Gemini Summary
    opt Generate Gemini Summary
        Cline->>SOAR: siemplify_create_gemini_case_summary(case_id=`${CASE_ID}`, ...)
        SOAR-->>Cline: Gemini Summary Text
    end

    %% Step 12: Confirm Report Generation
    Cline->>User: ask_followup_question(question="Generate MD report (incl. Process Trees)? Include delta/Gemini?", options=["Yes, include delta", "Yes, exclude delta", "Yes, include Gemini", "Yes, include All", "No Report"])
    User->>Cline: Confirmation (e.g., "Yes, exclude delta")

    alt Report Confirmed ("Yes...")
        %% Step 13: Write MD Report
        Note over Cline: Format report content (MUST include Trees & Table, optionally Gemini Summary)
        Cline->>Cline: write_to_file(path="./reports/case_${CASE_ID}_timeline_${timestamp}.md", content=...)
        Note over Cline: MD Report file created.

        %% Step 14 & 15: Confirm PDF/Attach
        Cline->>User: ask_followup_question(question="Convert report to PDF and attach/comment in SOAR?", options=["Yes", "No"])
        User->>Cline: Confirmation (e.g., "Yes")

        alt PDF & Attach/Comment Confirmed
            Cline->>Cline: execute_command(pandoc MD_PATH -o PDF_PATH ...)
            Note over Cline: PDF Generated locally.
            Note over Cline: Attempt SOAR attachment (Tool dependent)
            Cline->>SOAR: post_case_comment(case_id=`${CASE_ID}`, comment="Generated report. PDF available at: PDF_PATH") %% Fallback if attach fails
            SOAR-->>Cline: Comment Confirmation

            %% Step 16 & 17: Optional SOAR Actions
            Cline->>User: ask_followup_question(question="Perform additional SOAR actions?", options=["Tag Case", "Change Priority", "Add Insight", "Update Description", "Assign Case", "Raise Incident", "None"])
            User->>Cline: SOAR Action Choice (e.g., "Tag Case")
            alt SOAR Action Chosen != "None"
                %% Execute chosen SOAR action(s)
                Cline->>SOAR: [Chosen SOAR Tool](case_id=`${CASE_ID}`, ...)
                SOAR-->>Cline: Action Confirmation
            end
            Cline->>Cline: attempt_completion(result="Timeline analysis complete. Report generated (MD/PDF). SOAR case updated. Optional actions performed.")

        else PDF & Attach/Comment Not Confirmed
            %% Step 16 & 17: Optional SOAR Actions (No PDF/Attach)
            Cline->>User: ask_followup_question(question="Perform additional SOAR actions?", options=["Tag Case", "Change Priority", "Add Insight", "Update Description", "Assign Case", "Raise Incident", "None"])
            User->>Cline: SOAR Action Choice (e.g., "None")
             alt SOAR Action Chosen != "None"
                %% Execute chosen SOAR action(s)
                Cline->>SOAR: [Chosen SOAR Tool](case_id=`${CASE_ID}`, ...)
                SOAR-->>Cline: Action Confirmation
            end
            Cline->>Cline: attempt_completion(result="Timeline analysis complete. MD Report generated. Optional actions performed.")
        end
    else Report Not Confirmed ("No Report")
        Cline->>Cline: attempt_completion(result="Timeline analysis complete. No report generated.")
    end
```
