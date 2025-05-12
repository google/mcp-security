# Runbook: Create Investigation Report

## Objective

Consolidate findings from a completed or ongoing investigation involving various security tools (e.g., SecOps SIEM/SOAR, GTI, SCC, Okta, Crowdstrike) into a comprehensive report suitable for stakeholders or post-incident review. This runbook focuses on the reporting process itself, assuming the core investigation steps have largely been completed.

## Scope

*   **In Scope:** Gathering case context, synthesizing existing findings (from case details, comments, or provided summaries), structuring the report according to templates, generating the report file, attempting to attach it to the SOAR case (with fallback), and optionally handling external uploads.
*   **Out of Scope:** Performing the primary investigation itself (this runbook reports *on* an investigation), deep forensic analysis, executing containment/remediation actions.

## Inputs

*   `${CASE_ID}` (Mandatory): The SOAR case ID for which the report is being generated.
*   *(Optional) `${ALERT_GROUP_IDENTIFIERS}`: Relevant alert group identifiers if needed for specific SOAR actions.*
*   *(Optional) `${INVESTIGATION_SUMMARY}`: Pre-existing summary of findings if available.*
*   *(Optional) `${KEY_ENTITIES}`: List of key entities (users, hosts, IOCs) that were the focus of the investigation.*
*   *(Optional) `${INCLUDE_TOOLS}`: List of tools whose findings should be summarized (e.g., ["SIEM", "GTI", "Okta"]).*
*   *(Optional) `${REPORT_FILENAME_SUFFIX}`: A suffix for the report filename (defaults to `${CASE_ID}`).*

## Tools

**Required for Reporting Workflow:**
*   `secops-soar`: `get_case_full_details`, `post_case_comment`
*   `write_to_file`
*   `ask_followup_question`

**Summarized From (Examples - Actual tools depend on the investigation):**
*   `secops-mcp`: `lookup_entity`, `search_security_events`
*   `gti-mcp`: Various `get_*_report` tools
*   `scc-mcp`: `search_scc_findings`
*   `okta-mcp`: `lookup_okta_user`
*   `crowdstrike-mcp`: `get_host_details`

**Conceptual/Optional (Availability Varies):**
*   `secops-soar`: `siemplify_add_attachment_to_case` (or similar attachment tool)
*   `google-drive-mcp`: `upload_to_drive`
*   `gcs-mcp`: `upload_to_gcs`

## Workflow Steps

1.  **Gather Case Context & Identify Key Entities:** Retrieve full details for `${CASE_ID}` using `secops-soar.get_case_full_details`. Extract relevant alerts, comments, existing entities, priority/status, and **explicitly identify the key entities/IOCs** that are central to the investigation based on this initial context.
2.  **Synthesize Findings:** Combine information from Step 1 with optional inputs (`${INVESTIGATION_SUMMARY}`, `${KEY_ENTITIES}`, `${INCLUDE_TOOLS}`). Review case comments and alert details to reconstruct the investigation narrative and key findings.
    *   **Note on Tool Limitations:** Be aware that direct searches for specific artifacts (like event IDs) or lookups for certain entity types (like hostnames without full paths) might fail or return limited information. If primary methods fail, adapt the investigation by using alternative approaches, such as searching SIEM logs based on related entities (IPs, users) and relevant timeframes, or performing broader lookups.
3.  **Structure Report:** Organize the synthesized information according to standard templates. **Refer to `.clinerules/reporting_templates.md` and `.clinerules/run_books/guidelines/runbook_guidelines.md`**. Key sections should include: Executive Summary, Investigation Timeline (high-level), Involved Entities & Enrichment Summary, Analysis/Root Cause (if determined), Actions Taken (summary), Recommendations/Lessons Learned.
4.  **Generate Mermaid Diagram:** Create a Mermaid sequence diagram summarizing the *actual investigation workflow* performed for this case, including any alternative steps taken or tool failures encountered. The diagram should reflect reality, not just the ideal path.
5.  **Manual Review & Redaction:** **CRITICAL STEP:** Prompt the analyst to review the drafted report content for accuracy and to **manually redact or defang any sensitive data** (e.g., PII, internal hostnames if required, specific credentials) before proceeding. Use `ask_followup_question` to get confirmation that redaction is complete.
6.  **Format Final Report:** Compile the reviewed/redacted information and the Mermaid diagram into the final Markdown report content.
7.  **Write Report File:** Execute `common_steps/generate_report_file.md` with the final report content, `REPORT_TYPE="investigation_report"`, and `REPORT_NAME_SUFFIX=${CASE_ID}` (or `${REPORT_FILENAME_SUFFIX}`). Obtain `${REPORT_FILE_PATH}` and `${WRITE_STATUS}`.
8.  **Attempt SOAR Attachment:**
    *   *(If `siemplify_add_attachment_to_case` or similar tool exists)* Attempt to attach the generated file (`${REPORT_FILE_PATH}`) to the SOAR case `${CASE_ID}`.
    *   **If Attachment Fails or Tool Unavailable:** Execute `common_steps/document_in_soar.md` with `${CASE_ID}` and `COMMENT_TEXT="Investigation report generated: `${REPORT_FILE_PATH}`. Attachment failed or not available. Summary: [Include brief summary here]."`. Obtain `${COMMENT_POST_STATUS}`.
    *   **If Attachment Succeeds:** Execute `common_steps/document_in_soar.md` with `${CASE_ID}` and `COMMENT_TEXT="Investigation report attached successfully: `${REPORT_FILE_PATH}`."`. Obtain `${COMMENT_POST_STATUS}`.
9.  **Confirm Optional External Upload:** Use `ask_followup_question` to ask the user: "Upload the redacted report file (`${REPORT_FILE_PATH}`) to Google Drive or GCS?". Options: ["Yes, Drive", "Yes, GCS", "No"]. Obtain `${UPLOAD_CHOICE}`.
10. **Execute External Upload (Optional):**
    *   If `${UPLOAD_CHOICE}` is "Yes, Drive" *(and Drive tool exists)*: Execute `google-drive-mcp.upload_to_drive` with `${REPORT_FILE_PATH}`.
    *   If `${UPLOAD_CHOICE}` is "Yes, GCS" *(and GCS tool exists)*: Execute `gcs-mcp.upload_to_gcs` with `${REPORT_FILE_PATH}`.
    *   Document upload status/location via `common_steps/document_in_soar.md`.
11. **Completion:** Conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as gti-mcp
    participant SCC as scc-mcp
    participant Okta as okta-mcp
    participant CS as crowdstrike-mcp
    participant Drive as google-drive-mcp
    participant GCS as gcs-mcp

    User->>Cline: Request Investigation Report for Case X
    Cline->>SOAR: list_alerts_by_case(case_id=X)
    SOAR-->>Cline: Alerts for Case X (containing entities E1, E2...)
    loop For each relevant Entity Ei
        Cline->>SIEM: lookup_entity(entity_value=Ei)
        SIEM-->>Cline: SIEM context for Ei
        Cline->>GTI: get_file_report/get_domain_report(entity=Ei)
        GTI-->>Cline: GTI context for Ei
        Cline->>SCC: search_scc_findings(query=Ei)
        SCC-->>Cline: SCC findings for Ei
        Cline->>Okta: lookup_okta_user(user=Ei)
        Okta-->>Cline: Okta user details for Ei
        Cline->>CS: get_host_details(host=Ei)
        CS-->>Cline: CrowdStrike host details for Ei
    end
    Note over Cline: Synthesize findings, redact/defang sensitive data
    Cline->>Cline: Create report content (e.g., report_content)
    Cline->>Cline: write_to_file(path="investigation_report_case_X.md", content=report_content)
    Note over Cline: Report created locally
    Cline->>SOAR: siemplify_add_attachment_to_case(case_id=X, file_path="investigation_report_case_X.md")
    SOAR-->>Cline: Attachment confirmation
    Cline->>User: ask_followup_question(question="Upload redacted report to Drive/GCS?", options=["Yes, Drive", "Yes, GCS", "No"])
    User->>Cline: Response (e.g., "Yes, Drive")
    alt Upload Confirmed
        alt Upload to Drive
            Cline->>Drive: upload_to_drive(file_path="investigation_report_case_X.md", destination="Reports Folder")
            Drive-->>Cline: Drive upload confirmation
        else Upload to GCS
            Cline->>GCS: upload_to_gcs(file_path="investigation_report_case_X.md", bucket="security-reports", object_name="case_X_report.md")
            GCS-->>Cline: GCS upload confirmation
        end
    end
    Cline->>Cline: attempt_completion(result="Investigation report created, attached to Case X, and optionally uploaded.")

```

## Completion Criteria

Investigation findings synthesized, report structured according to guidelines, content reviewed/redacted by analyst, report file generated locally, and SOAR case updated with attachment status or fallback comment. Optional external upload handled if requested and possible.
