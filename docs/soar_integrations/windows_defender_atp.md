# Windows Defender ATP Integration

The Microsoft Defender for Endpoint (formerly Windows Defender ATP) integration for Chronicle SOAR allows interaction with Microsoft's endpoint security platform. This enables querying endpoint data, managing alerts and incidents, and taking response actions on devices directly from SOAR workflows.

## Overview

Microsoft Defender for Endpoint (MDE) is a comprehensive endpoint security platform offering endpoint protection (EPP), endpoint detection and response (EDR), vulnerability management, mobile threat defense, and more. It provides deep visibility into endpoint activities and tools to investigate and respond to threats.

This integration typically enables Chronicle SOAR to:

*   **Manage Alerts/Incidents:** Retrieve alerts and incidents from MDE, update their status (e.g., classification, determination, assignment), and add comments.
*   **Endpoint Isolation:** Isolate potentially compromised devices from the network or remove them from isolation.
*   **Run Scans:** Initiate antivirus scans on specific endpoints.
*   **Indicator Blocking:** Block or allow specific indicators (file hashes, IP addresses, URLs, domains) via MDE's custom indicator capabilities.
*   **Retrieve Endpoint Information:** Get details about specific devices managed by MDE, including OS, health state, risk level, and logged-on users.
*   **Advanced Hunting:** Execute Kusto Query Language (KQL) queries against MDE's advanced hunting data.
*   **Live Response Actions:** Potentially run scripts, collect forensic data, or stop processes on endpoints (depending on API capabilities and integration implementation).

## Key Actions

The following actions are available through the Microsoft Defender for Endpoint (MicrosoftDefenderATP) integration:

*   **Run Advanced Hunting Query (`microsoft_defender_atp_run_advanced_hunting_query`)**
    *   Description: Execute a Kusto Query Language (KQL) query against MDE's advanced hunting data.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `query` (string, required): Advanced hunting query (KQL) to execute.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Machine Related Alerts (`microsoft_defender_atp_get_machine_related_alerts`)**
    *   Description: Get alerts related to specific machines (Hostname/IP entities).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `status` (string, optional): Comma-separated list of alert statuses to filter by.
        *   `severity` (string, optional): Comma-separated list of alert severities to filter by.
        *   `category` (string, optional): Comma-separated list of alert categories to filter by.
        *   `incident_id` (string, optional): Filter alerts related to a specific MDE Incident ID.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Wait Task Status (`microsoft_defender_atp_wait_task_status`)**
    *   Description: Wait for the completion of specific MDE background tasks (e.g., scan, isolation).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `task_i_ds` (string, required): Comma-separated list of MDE Task IDs to wait for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get File Related Machines (`microsoft_defender_atp_get_file_related_machines`)**
    *   Description: Get machines where a specific file (SHA1 hash entity) has been observed.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `machine_name` (string, optional): Filter by full machine name.
        *   `machine_ip_address` (string, optional): Filter by machine IP address.
        *   `machine_risk_score` (string, optional): Filter by comma-separated machine risk scores.
        *   `machine_health_status` (string, optional): Filter by comma-separated machine health statuses.
        *   `machine_os_platform` (string, optional): Filter by machine OS platform.
        *   `rbac_group_id` (string, optional): Filter by RBAC Group ID.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash entities (SHA1 only).
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Current Task Status (`microsoft_defender_atp_get_current_task_status`)**
    *   Description: Get the current status of specific MDE background tasks.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `task_i_ds` (string, required): Comma-separated list of MDE Task IDs.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Create Stop And Quarantine File Specific Machine Task (`microsoft_defender_atp_create_stop_and_quarantine_file_specific_machine_task`)**
    *   Description: Create a task to stop execution of a file (by SHA1 hash) and quarantine it on specific machines (Hostname/IP entities).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `sha1_file_hash_to_quarantine` (string, required): SHA1 hash of the file to stop and quarantine.
        *   `comment` (string, required): Comment to associate with the action.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Create Isolate Machine Task (`microsoft_defender_atp_create_isolate_machine_task`)**
    *   Description: Create a task to isolate specific machines (Hostname/IP entities) from the network.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `isolation_type` (string, required): Type of isolation (e.g., `Full`, `Selective`).
        *   `comment` (string, required): Comment explaining the reason for isolation.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Update Alert (`microsoft_defender_atp_update_alert`)**
    *   Description: Update the status, assignment, classification, or determination of an MDE alert.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `alert_id` (string, required): The MDE Alert ID to update.
        *   `status` (List[str], optional): New status (e.g., `["InProgress"]`, `["Resolved"]`).
        *   `assigned_to` (string, optional): User principal name to assign the alert to.
        *   `classification` (List[str], optional): New classification (e.g., `["TruePositive"]`, `["FalsePositive"]`).
        *   `determination` (List[str], optional): New determination (e.g., `["Malware"]`, `["NotMalware"]`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Alerts (`microsoft_defender_atp_list_alerts`)**
    *   Description: Retrieve a list of MDE alerts based on specified filters.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `time_frame` (string, optional): Time frame in hours to fetch alerts from.
        *   `status` (string, optional): Comma-separated list of alert statuses to filter by.
        *   `severity` (string, optional): Comma-separated list of alert severities to filter by.
        *   `category` (string, optional): Comma-separated list of alert categories to filter by.
        *   `incident_id` (string, optional): Filter alerts related to a specific MDE Incident ID.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`microsoft_defender_atp_ping`)**
    *   Description: Test connectivity to the Microsoft Defender for Endpoint API.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Machine Logon Users (`microsoft_defender_atp_get_machine_logon_users`)**
    *   Description: Get users who have logged onto specific machines (Hostname/IP entities).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Machines (`microsoft_defender_atp_list_machines`)**
    *   Description: Retrieve a list of machines managed by MDE based on specified filters.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `last_seen_time_frame` (string, optional): Time frame in hours for last seen machines.
        *   `machine_name` (string, optional): Filter by full machine name.
        *   `machine_ip_address` (string, optional): Filter by machine IP address.
        *   `machine_risk_score` (string, optional): Filter by comma-separated machine risk scores.
        *   `machine_health_status` (string, optional): Filter by comma-separated machine health statuses.
        *   `machine_os_platform` (string, optional): Filter by machine OS platform.
        *   `rbac_group_id` (string, optional): Filter by RBAC Group ID.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Indicators (`microsoft_defender_atp_list_indicators`)**
    *   Description: List custom indicators configured in MDE based on specified filters.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `indicators` (string, optional): Comma-separated list of specific indicator values to retrieve.
        *   `indicator_types` (string, optional): Comma-separated list of indicator types (e.g., `FileSha1,IpAddress,Url`).
        *   `actions` (string, optional): Comma-separated list of indicator actions (e.g., `Warn,Block,Allowed`).
        *   `severity` (string, optional): Comma-separated list of indicator severities (e.g., `Informational,High`).
        *   `max_results_to_return` (string, optional, default=50): Maximum indicators to return.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Submit Entity Indicators (`microsoft_defender_atp_submit_entity_indicators`)**
    *   Description: Submit entities (FileHash, URL, IP Address) as custom indicators to MDE.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `action` (List[str], required): Action to apply (e.g., `["AlertAndBlock"]`, `["Allowed"]`).
        *   `severity` (List[str], required): Severity for the indicator (e.g., `["High"]`).
        *   `indicator_alert_title` (string, required): Title for alerts generated by this indicator.
        *   `description` (string, required): Description for the indicator.
        *   `application` (string, optional): Related application.
        *   `recommended_action` (string, optional): Recommended handling actions.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash (MD5, SHA1, SHA256), URL, or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get File Related Alerts (`microsoft_defender_atp_get_file_related_alerts`)**
    *   Description: Get alerts related to a specific file (SHA1 hash entity).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `status` (string, optional): Comma-separated list of alert statuses to filter by.
        *   `severity` (string, optional): Comma-separated list of alert severities to filter by.
        *   `category` (string, optional): Comma-separated list of alert categories to filter by.
        *   `incident_id` (string, optional): Filter alerts related to a specific MDE Incident ID.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash entities (SHA1 only).
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich Entities (`microsoft_defender_atp_enrich_entities`)**
    *   Description: Enrich Host, IP, or FileHash (SHA1/SHA256) entities with information from MDE.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname, IP Address, or FileHash entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Create Run Antivirus Scan Task (`microsoft_defender_atp_create_run_antivirus_scan_task`)**
    *   Description: Create a task to run an antivirus scan on specific machines (Hostname/IP entities).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `antivirus_scan_type` (List[str], required): Type of scan (e.g., `["Quick"]`, `["Full"]`).
        *   `comment` (string, required): Comment explaining the reason for the scan.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Create Unisolate Machine Task (`microsoft_defender_atp_create_unisolate_machine_task`)**
    *   Description: Create a task to remove specific machines (Hostname/IP entities) from network isolation.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `comment` (string, required): Comment explaining the reason for unisolation.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname or IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Delete Entity Indicators (`microsoft_defender_atp_delete_entity_indicators`)**
    *   Description: Delete custom indicators (FileHash, URL, IP Address) from MDE.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash (MD5, SHA1, SHA256), URL, or IP Address entities to delete as indicators.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Use Cases

*   **Alert Triage and Enrichment:** Ingest MDE alerts into SOAR, enrich associated entities (hosts, users, IPs, hashes), and update the alert status in MDE based on investigation findings.
*   **Automated Endpoint Containment:** Automatically isolate devices based on high-confidence MDE alerts or correlation with other security events.
*   **Indicator Blocking:** When malicious indicators are identified (from threat intel, sandbox analysis, etc.), automatically block them across all endpoints using the MDE integration.
*   **Threat Hunting:** Use SOAR playbooks to run scheduled or ad-hoc advanced hunting queries in MDE to proactively search for threats.
*   **Vulnerability Management:** Correlate MDE vulnerability data with alerts or asset information.

## Configuration

*(Details on configuring the integration, including setting up an Azure AD App Registration with the necessary API permissions (e.g., `Machine.ReadWrite.All`, `Alert.ReadWrite.All`, `AdvancedHunting.Read.All`, `Ti.ReadWrite`), obtaining Tenant ID, App ID, and App Secret, and configuring settings within the SOAR platform, should be added here.)*
