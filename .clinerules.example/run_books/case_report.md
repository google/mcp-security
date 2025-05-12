# Runbook: Generate Case Investigation Report (Placeholder)

## Objective

*(Define the goal, e.g., To consolidate findings from a completed investigation for a specific SOAR case into a comprehensive report suitable for stakeholders or post-incident review.)*

## Scope

*(Define what is included/excluded, e.g., Summarizes key alerts, events, entity analysis, enrichment, actions taken, and conclusions for a single case. Does not typically involve new investigation steps.)*

## Inputs

*   `${CASE_ID}`: The SOAR case ID for which the report is being generated.
*   *(Optional) `${REPORT_FILENAME_SUFFIX}`: A suffix for the report filename.*
*   *(Optional) `${ADDITIONAL_CONTEXT}`: Any specific points or findings the analyst wants to ensure are included.*

## Tools

*   `secops-soar`: `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`, `post_case_comment` (Potentially others depending on what needs summarizing)
*   `secops-mcp`: `lookup_entity`, `search_security_events` (If summarizing previous searches)
*   `gti-mcp`: Various `get_*_report` tools (If summarizing previous enrichment)
*   `write_to_file`

## Workflow Steps & Diagram

1.  **Gather Case Data:** Retrieve all relevant data for `${CASE_ID}` using `get_case_full_details` (includes basic case info, alerts, comments). Potentially re-run `list_events_by_alert` for key alerts if needed.
2.  **Synthesize Findings:** Review case comments, alert details, event summaries, and previous enrichment data associated with the case.
3.  **Structure Report:** Organize the information according to a standard template (referencing `.clinerules/reporting_templates.md`). Key sections might include: Executive Summary, Timeline of Key Events, Involved Entities & Enrichment, Analysis/Root Cause (if determined), Actions Taken, Recommendations/Lessons Learned.
4.  **Generate Mermaid Diagram:** Create a Mermaid sequence diagram summarizing the *investigation workflow* that was performed for this case (which tools were used in what order).
5.  **Format Report:** Compile the synthesized information and the Mermaid diagram into a final Markdown report.
6.  **Write Report File:** Save the report using `write_to_file` with a standardized name (e.g., `./reports/case_report_${CASE_ID}_${timestamp}.md`).
7.  **(Optional) Update Case:** Add a comment to the SOAR case indicating the report has been generated and its location using `post_case_comment`.

```{mermaid}
sequenceDiagram
    participant Analyst/User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp %% Example servers used during investigation
    participant GTI as gti-mcp  %% Example servers used during investigation

    Analyst/User->>Cline: Generate Case Report\nInput: CASE_ID, ...

    %% Step 1: Gather Case Data
    Cline->>SOAR: get_case_full_details(case_id=CASE_ID)
    SOAR-->>Cline: Case Details, Alerts, Comments
    %% Potentially re-run list_events_by_alert if needed

    %% Step 2: Synthesize Findings
    Note over Cline: Review all gathered data (comments, events, enrichment from investigation)

    %% Step 3 & 4: Structure Report & Generate Diagram
    Note over Cline: Organize report sections (Exec Summary, Timeline, Entities, Analysis, Actions...)
    Note over Cline: Create Mermaid diagram summarizing investigation steps

    %% Step 5 & 6: Format & Write Report
    Note over Cline: Compile final Markdown content
    Cline->>Cline: write_to_file(path="./reports/case_report_...", content=ReportMarkdown)
    Note over Cline: Report file created

    %% Step 7: Optional SOAR Update
    opt Update SOAR Case
        Cline->>SOAR: post_case_comment(case_id=CASE_ID, comment="Case report generated: case_report_....md")
        SOAR-->>Cline: Comment Confirmation
    end

    Cline->>Analyst/User: attempt_completion(result="Case investigation report generated for Case CASE_ID.")

```

## Completion Criteria

*(Define how successful completion is determined, e.g., Report generated containing key investigation elements, report saved, case optionally updated.)*
