# Qualys VM Integration

The Qualys Vulnerability Management (VM) integration for Chronicle SOAR allows interaction with the Qualys Cloud Platform to manage vulnerability scans, reports, and retrieve host information.

## Overview

Qualys VM is a cloud-based service that provides vulnerability scanning, assessment, and reporting capabilities. It helps organizations identify and prioritize vulnerabilities across their IT assets.

This integration typically enables Chronicle SOAR to:

*   **Launch Scans and Reports:** Initiate vulnerability scans, patch reports, compliance reports, and remediation reports.
*   **Retrieve Scan/Report Data:** Download scan results or generated reports.
*   **List Assets and Information:** List managed IPs, asset groups, scans, and reports.
*   **Enrich Host Information:** Gather vulnerability and asset details for specific hosts.

## Key Actions

The following actions are available through the Qualys VM integration:

*   **List Scans (`qualys_vm_list_scans`)**
    *   Description: List vulnerability scans launched within the past 30 days.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Patch Report (`qualys_vm_launch_patch_report`)**
    *   Description: Launch a patch report based on a template.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title for the report (max 128 chars).
        *   `report_type` (string, required): Name of the patch report template (e.g., `Qualys Patch Report`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `online`, `xml`, `csv`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override the template target.
        *   `asset_groups` (string, optional): Comma-separated asset group names to override the template target.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Download VM Scan Results (`qualys_vm_download_vm_scan_results`)**
    *   Description: Fetch vulnerability scan results by scan ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `scan_id` (string, required): Scan ID (format: `scan/{integer}.{integer}`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch VM Scan And Fetch Results (`qualys_vm_launch_vm_scan_and_fetch_results`)**
    *   Description: Launch a vulnerability scan on IP Address entities and fetch results. Adds new hosts as assets if needed (check license limits).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `processing_priority` (string, required): Scan priority (0-9, 0=No Priority, 1=Emergency, ..., 9=Low).
        *   `scan_profile` (string, required): Title of the compliance option profile (e.g., `Qualys Top 20 Options`).
        *   `title` (string, optional): Scan title (max 2000 chars).
        *   `scanner_appliance` (string, optional): Comma-separated scanner appliance names or `External`.
        *   `network` (string, optional): Network ID to filter target IPs (default `0` for Global Default Network).
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address entities to scan.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Download Report (`qualys_vm_download_report`)**
    *   Description: Fetch a previously generated report by its ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_id` (string, required): The ID of the report to download.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List IPs (`qualys_vm_list_ips`)**
    *   Description: List IP addresses defined in the user's Qualys account.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Scan Report (`qualys_vm_launch_scan_report`)**
    *   Description: Launch a scan-based report (e.g., Technical Report).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars).
        *   `report_type` (string, required): Template name (e.g., `Technical Report`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `mht`, `html`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override the template target.
        *   `asset_groups` (string, optional): Comma-separated asset group names to override the template target.
        *   `scan_reference` (string, optional): Specific scan reference (e.g., `scan/12345.67890`) to base the report on.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`qualys_vm_ping`)**
    *   Description: Test connectivity to the Qualys VM API.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Groups (`qualys_vm_list_groups`)**
    *   Description: List asset groups defined in the user's Qualys account.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Endpoint Detections (`qualys_vm_list_endpoint_detections`)**
    *   Description: List vulnerability detections for specific endpoints (IP Address, Hostname).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `status_filter` (string, optional): Comma-separated statuses (e.g., `New,Active,Re-Opened,Fixed`). Defaults to New, Active, Re-Opened.
        *   `lowest_severity_to_fetch` (List[str], optional): Minimum severity level to fetch (e.g., `["3"]`).
        *   `max_detections_to_return` (string, optional, default=50, max=200): Max detections per entity.
        *   `ingest_ignored_detections` (bool, optional): Include ignored detections.
        *   `ingest_disabled_detections` (bool, optional): Include disabled detections.
        *   `create_insight` (bool, optional): Create an insight with vulnerability information.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address or Hostname entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Reports (`qualys_vm_list_reports`)**
    *   Description: List reports available in the user's account (requires Report Share feature enabled).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Remediation Report (`qualys_vm_launch_remediation_report`)**
    *   Description: Launch a remediation ticket report based on a template.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars).
        *   `report_type` (string, required): Template name (e.g., `Tickets per Asset Group`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `mht`, `html`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override the template target.
        *   `asset_groups` (string, optional): Comma-separated asset group names to override the template target.
        *   `display_results_for_all_tickets` (bool, optional): Include all tickets, not just those assigned to the current user (default is current user).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Launch Compliance Report (`qualys_vm_launch_compliance_report`)**
    *   Description: Launch a compliance report based on a template.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `report_title` (string, required): User-defined title (max 128 chars). PCI reports use a Qualys-defined title.
        *   `report_type` (string, required): Template name (e.g., `Qualys Top 20 Report`, `Payment Card Industry (PCI)`).
        *   `output_format` (string, required): Output format (e.g., `pdf`, `mht`, `html`).
        *   `i_ps_ranges` (string, optional): Comma-separated IPs/ranges to override the template target.
        *   `asset_groups` (string, optional): Comma-separated asset group names to override the template target.
        *   `scan_reference` (string, optional): Filter report based on a specific scan reference (e.g., `scan/12345.67890`). Required for PCI reports.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich Host (`qualys_vm_enrich_host`)**
    *   Description: Enrich Hostname or IP Address entities with information from Qualys VM (requires AssetView module).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `create_insight` (bool, optional): Create an insight with the retrieved host information.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Configuration

*(Details on configuring the integration, including the Qualys API server URL, authentication credentials (username/password), and any specific SOAR platform settings, should be added here.)*
