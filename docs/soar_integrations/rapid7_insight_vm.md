# Rapid7 InsightVM Integration

The Rapid7 InsightVM integration for Chronicle SOAR allows interaction with the InsightVM vulnerability management platform. This enables launching scans, retrieving scan results and reports, listing assets, and enriching host information directly from SOAR workflows.

## Overview

Rapid7 InsightVM provides vulnerability assessment, prioritization, and remediation tracking across cloud, virtual, remote, local, and containerized infrastructure. It helps organizations discover, assess, prioritize, and remediate vulnerabilities.

This integration typically enables Chronicle SOAR to:

*   **Manage Scans:** List recent scans, launch new vulnerability scans for specific sites or assets, and retrieve scan results.
*   **Manage Reports:** Launch various report types (patch, scan, remediation, compliance) and download completed reports.
*   **Asset Information:** List IPs and asset groups managed by InsightVM, and enrich host entities with asset details.
*   **Vulnerability Information:** List vulnerability detections for specific endpoints.

## Key Actions

The following actions are available through the Rapid7 InsightVM integration:

*   **List Scans (`rapid7_insight_vm_list_scans`)**
    *   Description: List scans launched within a specified number of days back.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `days_backwards` (string, required): Number of days back to fetch scans from.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Patch Report (`rapid7_insight_vm_launch_patch_report`)**
    *   Description: Launch a patch report based on a template.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars).
        *   `report_type` (string, required): Template name (e.g., `Qualys Patch Report` - *Note: Example seems incorrect, likely should be InsightVM template*).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `online`, `xml`, `csv`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override template target.
        *   `asset_groups` (string, optional): Comma-separated asset groups to override template target.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Download VM Scan Results (`rapid7_insight_vm_download_vm_scan_results`)**
    *   Description: Fetch vulnerability scan results by scan ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `scan_id` (string, required): The ID of the scan whose results are to be downloaded.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch VM Scan And Fetch Results (`rapid7_insight_vm_launch_vm_scan_and_fetch_results`)**
    *   Description: Launch a vulnerability scan on IP Address entities and optionally fetch results.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `processing_priority` (string, required): Scan priority (0-9).
        *   `scan_profile` (string, required): Title of the compliance option profile (*Note: Example seems Qualys-specific, likely should be InsightVM scan template*).
        *   `title` (string, optional): Scan title (max 2000 chars).
        *   `scanner_appliance` (string, optional): Comma-separated scanner appliance names or `External`.
        *   `network` (string, optional): Network ID for filtering target IPs.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address entities to scan.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Download Report (`rapid7_insight_vm_download_report`)**
    *   Description: Fetch a previously generated report by its ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_id` (string, required): The ID of the report to download.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List IPs (`rapid7_insight_vm_list_ips`)**
    *   Description: List IP addresses known to the InsightVM instance.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Scan Report (`rapid7_insight_vm_launch_scan_report`)**
    *   Description: Launch a scan-based report.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars).
        *   `report_type` (string, required): Template name (e.g., `Technical Report`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `mht`, `html`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override template target.
        *   `asset_groups` (string, optional): Comma-separated asset groups to override template target.
        *   `scan_reference` (string, optional): Specific scan reference ID to base the report on.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`rapid7_insight_vm_ping`)**
    *   Description: Test connectivity to the Rapid7 InsightVM API.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Groups (`rapid7_insight_vm_list_groups`)**
    *   Description: List asset groups defined in the InsightVM account.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Endpoint Detections (`rapid7_insight_vm_list_endpoint_detections`)**
    *   Description: List vulnerability detections for specific endpoints (IP Address, Hostname).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `status_filter` (string, optional): Comma-separated statuses (e.g., `New,Active,Re-Opened,Fixed`).
        *   `lowest_severity_to_fetch` (List[str], optional): Minimum severity level (e.g., `["3"]`).
        *   `max_detections_to_return` (string, optional, default=50, max=200): Max detections per entity.
        *   `ingest_ignored_detections` (bool, optional): Include ignored detections.
        *   `ingest_disabled_detections` (bool, optional): Include disabled detections.
        *   `create_insight` (bool, optional): Create an insight with vulnerability information.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address or Hostname entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Reports (`rapid7_insight_vm_list_reports`)**
    *   Description: List reports available in the user's account.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Remediation Report (`rapid7_insight_vm_launch_remediation_report`)**
    *   Description: Launch a remediation ticket report based on a template.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars).
        *   `report_type` (string, required): Template name (e.g., `Tickets per Asset Group`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `mht`, `html`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override template target.
        *   `asset_groups` (string, optional): Comma-separated asset groups to override template target.
        *   `display_results_for_all_tickets` (bool, optional): Include all tickets (default is current user's).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Compliance Report (`rapid7_insight_vm_launch_compliance_report`)**
    *   Description: Launch a compliance report based on a template.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars).
        *   `report_type` (string, required): Template name (e.g., `PCI Attestation Report`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `mht`, `html`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override template target.
        *   `asset_groups` (string, optional): Comma-separated asset groups to override template target.
        *   `scan_reference` (string, optional): Specific scan reference ID to base the report on.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich Asset (`rapid7_insight_vm_enrich_asset`)**
    *   Description: Enrich Hostname or IP Address entities with asset information from InsightVM.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `create_insight` (bool, optional): Create an insight with the retrieved asset information.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Configuration

*(Details on configuring the integration, including the Rapid7 InsightVM Console URL, API credentials (username/password), and any specific SOAR platform settings like SSL verification, should be added here.)*
