# Runbook: Report Writing Guidelines & Template

## Objective

To provide general guidelines and a basic template structure for writing consistent and informative security reports generated from runbook executions or ad-hoc investigations.

## Scope

These guidelines apply to various report types (e.g., investigation summaries, threat hunt reports, triage reports) generated within this security environment. Specific content requirements may vary based on the report type (refer to `.clinerules/reporting_templates.md`).

## Inputs

*   `${FINDINGS}`: The synthesized data, analysis, and conclusions from the investigation/hunt.
*   `${RUNBOOK_NAME}`: The name of the runbook used (if applicable).
*   `${CASE_ID}`: Relevant SOAR Case ID(s).
*   `${MERMAID_DIAGRAM}`: The Mermaid sequence diagram illustrating the workflow performed.

## Tools

*   `write_to_file`: To save the final report.
*   *(Tools used to gather `${FINDINGS}`)*

## Workflow Steps & Diagram (Conceptual - For Writing the Report)

1.  **Gather Information:** Collect all necessary findings, analysis, context, runbook name, case ID, and the generated Mermaid diagram.
2.  **Structure Report:** Organize the information logically. Start with metadata, followed by a summary/executive summary, detailed findings, analysis, conclusions, and recommendations. Refer to `.clinerules/reporting_templates.md` for specific section requirements based on report type.
3.  **Incorporate Metadata:** Ensure the report includes:
    *   `**Runbook Used:** ${RUNBOOK_NAME}` (If applicable)
    *   **Timestamp:** Generation time (e.g., YYYY-MM-DD HH:MM Timezone)
    *   **Case ID(s):** `${CASE_ID}`
    *   **Workflow Diagram:** Embed the `${MERMAID_DIAGRAM}`.
4.  **Write Content:** Clearly articulate findings, analysis, and conclusions. Use consistent terminology. Include links back to relevant tools/platforms where appropriate (e.g., links to SOAR cases, GTI reports).
5.  **Review & Refine:** Proofread the report for clarity, accuracy, and completeness.
6.  **Save Report:** Use `write_to_file` to save the report with a standardized filename (e.g., `<report_type>_<report_name>_${CASE_ID}_${timestamp}.md`).

```{mermaid}
sequenceDiagram
    participant Analyst/Agent
    participant Cline as Cline (MCP Client)
    participant ReportingTemplates as .clinerules/reporting_templates.md

    Analyst/Agent->>Cline: Initiate Report Writing\nInput: FINDINGS, RUNBOOK_NAME, CASE_ID, MERMAID_DIAGRAM

    %% Step 1 & 2: Gather Info & Structure
    Note over Cline: Gather all necessary inputs
    Cline->>ReportingTemplates: Consult for structure based on report type
    ReportingTemplates-->>Cline: Required Sections

    %% Step 3 & 4: Incorporate Metadata & Write Content
    Note over Cline: Add Runbook Name, Timestamp, Case ID
    Note over Cline: Embed Mermaid Diagram
    Note over Cline: Write detailed findings, analysis, conclusions
    Note over Cline: Add relevant links

    %% Step 5: Review
    Note over Cline: Review for clarity, accuracy

    %% Step 6: Save Report
    Cline->>Cline: write_to_file(path="./reports/...", content=FinalReportMarkdown)
    Note over Cline: Report Saved

    Cline->>Analyst/Agent: attempt_completion(result="Report writing complete. File saved.")

```

## Completion Criteria

Report is written, reviewed, and saved in the standard format and location.
