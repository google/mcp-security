# Alert Investigation Summary Report Runbook

## Objective

Generate a standardized report summarizing the key findings from the investigation of a specific security alert or a group of related alerts within a SOAR case. This report is intended for documentation, handover, or escalation purposes.

## Scope

This runbook covers gathering essential details about the alert(s), associated events, involved entities, basic enrichment, and producing a structured summary report in Markdown format. It does not typically involve deep-dive analysis or containment actions, which would be covered by other runbooks.

## Inputs

*   `${CASE_ID}`: The relevant SOAR case ID containing the alert(s).
*   `${ALERT_GROUP_IDENTIFIERS}`: A list of relevant alert group identifiers within the case. Alternatively, provide specific `${ALERT_IDS}`.
*   *(Optional) `${ALERT_IDS}`: Comma-separated list of specific alert IDs to focus on if `${ALERT_GROUP_IDENTIFIERS}` is not used.*
*   *(Optional) `${REPORT_FILENAME_SUFFIX}`: A suffix to append to the report filename (e.g., "initial_triage").*

## Tools

*   `secops-soar`: `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`, `get_entities_by_alert_group_identifiers`, `post_case_comment`
*   `secops-mcp`: `lookup_entity`, `search_security_events` (optional, for broader context)
*   `Google Threat Intelligence MCP server`: `get_ip_address_report`, `get_domain_report`, `get_file_report`, `get_url_report`
*   `write_to_file`

## Workflow Steps & Diagram

1.  **Receive Input & Context:** Obtain `${CASE_ID}`, `${ALERT_GROUP_IDENTIFIERS}` (or `${ALERT_IDS}`), and optionally `${REPORT_FILENAME_SUFFIX}`. Get case details using `secops-soar.get_case_full_details`.
2.  **Identify Target Alerts & Entities:**
    *   If using `${ALERT_GROUP_IDENTIFIERS}`, use `secops-soar.get_entities_by_alert_group_identifiers` to list involved entities. Use `secops-soar.list_alerts_by_case` and filter based on the group identifiers (if possible, otherwise use all alerts in the group).
    *   If using `${ALERT_IDS}`, retrieve details for those specific alerts (potentially from the `get_case_full_details` output or by iterating `list_alerts_by_case` if needed). Identify entities directly from these alerts.
    *   Compile a list of unique key entities (Users, Hosts, IPs, Hashes, Domains, URLs) involved in the target alert(s). Let this be `KEY_ENTITIES`.
3.  **Gather Alert Events:**
    *   Retrieve underlying UDM events for key alerts. Use `secops-soar.list_events_by_alert` for detailed events, or summarize event details available within the `secops-soar.get_case_full_details` output if sufficient for a summary perspective.
    *   Extract key event details (timestamps, event types, process info, network info, file info).
4.  **Enrich Key Entities:**
    *   Initialize an empty structure for enrichment findings.
    *   For each entity in `KEY_ENTITIES`:
        *   Use `secops-mcp.lookup_entity` to get SIEM context (first/last seen, related alerts).
        *   Use the appropriate `gti-mcp.get_..._report` tool based on entity type (IP, Domain, Hash, URL) to get threat intelligence reputation/context.
    *   Store enrichment summaries.
5.  **(Optional) Search Related SIEM Activity:**
    *   *(Guidance: Consider performing this step if initial enrichment reveals highly critical IOCs or if the alert context is unclear).*
        *   Perform limited `secops-mcp.search_security_events` queries around the alert timeframe for the most critical entities identified (e.g., the primary host or user) to find immediate related context beyond the specific alert events.
6.  **Synthesize & Format Report:**
    *   Create a Markdown report structure including (referencing `.clinerules/reporting_templates.md` and `.clinerules/run_books/guidelines/runbook_guidelines.md`):
        *   **Metadata:** Runbook Used, Timestamp, Case ID(s).
        *   **Case Summary:** Case ID, Name, Priority, Status (from `get_case_full_details`).
        *   **Alert(s) Summary:** List target Alert IDs, Names, Timestamps, Severities.
        *   **Key Entities Involved:** List entities from `KEY_ENTITIES` with a brief description.
        *   **Enrichment Summary:** Provide concise summaries of SIEM and GTI findings for each key entity.
        *   **Event Summary:** Briefly describe the key events triggering the alert(s). Include timestamps and event types.
        *   **(Optional) Related SIEM Activity:** Summarize findings from Step 5.
        *   **Initial Assessment/Conclusion:** A brief statement on the nature of the alert based on the gathered data (e.g., "Likely malicious activity involving...", "Appears to be benign based on...", "Requires further investigation by Tier 2...").
        *   **Workflow Diagram:** Include a Mermaid sequence diagram illustrating the steps taken during this runbook execution.
7.  **Write Report File:**
    *   Generate a timestamp string (`TIMESTAMP`, e.g., `yyyymmdd_hhmm`).
    *   Construct filename: `./reports/alert_report_${CASE_ID}_${REPORT_FILENAME_SUFFIX}_${timestamp}.md`.
    *   Use `write_to_file` with the path and formatted Markdown content.
8.  **(Optional) Update SOAR Case:**
    *   Use `secops-soar.post_case_comment` to add a comment to `${CASE_ID}` stating that the report has been generated and providing the filename, or pasting a concise summary directly.
9.  **Completion:** Conclude the runbook execution.

```{mermaid}
sequenceDiagram
    participant Analyst/User
    participant Cline as Cline (MCP Client)
    participant SOAR as secops-soar
    participant SIEM as secops-mcp
    participant GTI as Google Threat Intelligence MCP server

    Analyst/User->>Cline: Generate Alert Report\nInput: CASE_ID, ALERT_GROUP_IDS/ALERT_IDS, FILENAME_SUFFIX (opt)

    %% Step 1: Context
    Cline->>SOAR: get_case_full_details(case_id=CASE_ID)
    SOAR-->>Cline: Case Details

    %% Step 2: Identify Alerts & Entities
    alt Use Alert Group IDs
        Cline->>SOAR: get_entities_by_alert_group_identifiers(case_id=CASE_ID, alert_group_identifiers=ALERT_GROUP_IDS)
        SOAR-->>Cline: Entities List (KEY_ENTITIES)
        Cline->>SOAR: list_alerts_by_case(case_id=CASE_ID) %% Filter alerts based on group if possible
        SOAR-->>Cline: Target Alert List (A1, A2...)
    else Use Alert IDs
        Note over Cline: Extract Target Alerts (A1, A2...) from Case Details or list_alerts_by_case
        Note over Cline: Extract KEY_ENTITIES from Target Alerts
    end

    %% Step 3: Gather Alert Events
    loop For each Target Alert Ai
        Cline->>SOAR: list_events_by_alert(case_id=CASE_ID, alert_id=Ai)
        SOAR-->>Cline: Events for Alert Ai
        Note over Cline: Store key event details
    end

    %% Step 4: Enrich Key Entities
    loop For each Entity Ei in KEY_ENTITIES
        Cline->>SIEM: lookup_entity(entity_value=Ei)
        SIEM-->>Cline: SIEM Summary for Ei
        alt Entity Type is IP/Domain/Hash/URL
            Cline->>GTI: get_..._report(ioc=Ei)
            GTI-->>Cline: GTI Report Summary for Ei
        end
        Note over Cline: Store enrichment findings
    end

    %% Step 5: Optional SIEM Search
    opt Search Related Activity
        loop For critical Entity Ec in KEY_ENTITIES
            Cline->>SIEM: search_security_events(text="Activity related to Ec near alert time")
            SIEM-->>Cline: Related SIEM Events
            Note over Cline: Store summary of related activity
        end
    end

    %% Step 6 & 7: Synthesize & Write Report
    Note over Cline: Format report content (Case Summary, Alert Summary, Entities, Enrichment, Events, Assessment)
    Cline->>Cline: write_to_file(path="./reports/alert_report_...", content=ReportMarkdown)
    Note over Cline: Report file created

    %% Step 8: Optional SOAR Update
    opt Update SOAR Case
        Cline->>SOAR: post_case_comment(case_id=CASE_ID, comment="Alert report generated: alert_report_....md. Summary: [...]")
        SOAR-->>Cline: Comment Confirmation
    end

    %% Step 9: Completion
    Cline->>Analyst/User: attempt_completion(result="Alert investigation summary report generated for Case CASE_ID.")
