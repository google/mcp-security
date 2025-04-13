# Microsoft Defender ATP Integration

## Overview

This integration allows you to connect to Microsoft Defender for Endpoint (formerly ATP) to perform advanced hunting queries, manage alerts and indicators, retrieve machine and file information, and execute remediation actions like isolating machines or running antivirus scans.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Run Advanced Hunting Query

Run Advanced Hunting Query in Microsoft Defender ATP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Advanced hunting query to execute.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the query execution.

### Get Machine Related Alerts

Get alerts related to specific machines based on various criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `status` (string, optional): Statuses of the alert to look for. Comma-separated string.
*   `severity` (string, optional): Severities of the alert to look for. Comma-separated string.
*   `category` (string, optional): Categories of the alert to look for. Comma-separated string.
*   `incident_id` (string, optional): Microsoft Defender Incident ID for which you want to find related alerts.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of related alerts.

### Wait Task Status

Wait for the completion status of specified tasks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_i_ds` (string, required): Task IDs list. Comma-separated string.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the status of the specified tasks.

### Get File Related Machines

Get machines related to a specific file hash. Note: For this action only SHA1 is supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `machine_name` (string, optional): Full Machine Name to look for.
*   `machine_ip_address` (string, optional): Machine IP Address to look for.
*   `machine_risk_score` (string, optional): Machine risk score to look for. Comma-separated string.
*   `machine_health_status` (string, optional): Machine health status to look for. Comma-separated string.
*   `machine_os_platform` (string, optional): Machine OS platform to look for.
*   `rbac_group_id` (string, optional): RBAC Group ID to look for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash (SHA1 only) entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of machines related to the file hash.

### Get Current Task Status

Get the current status of specified tasks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_i_ds` (string, required): Task IDs list. Comma-separated string.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the current status of the specified tasks.

### Create Stop And Quarantine File Specific Machine Task

Create a task to stop and quarantine a file on specific machines.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `sha1_file_hash_to_quarantine` (string, required): SHA1 File Hash to Quarantine.
*   `comment` (string, required): Comment to associate with the action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the task creation, likely including the task ID.

### Create Isolate Machine Task

Create a task to isolate machines.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `isolation_type` (List[Any], required): Isolation type (e.g., Full, Selective).
*   `comment` (string, required): Comment why the machine needs to be isolated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the task creation, likely including the task ID.

### Update Alert

Update alert details like status, assignee, classification, and determination.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Microsoft Defender ATP Alert ID to update.
*   `status` (List[Any], optional): Status of the alert.
*   `assigned_to` (string, optional): User who is assigned to this alert.
*   `classification` (List[Any], optional): Classification to update alert with.
*   `determination` (List[Any], optional): Determination to update alert with.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### List Alerts

Get alerts based on specified criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (string, optional): Time frame in hours for which to fetch Alerts.
*   `status` (string, optional): Statuses of the alert to look for. Comma-separated string.
*   `severity` (string, optional): Severities of the alert to look for. Comma-separated string.
*   `category` (string, optional): Categories of the alert to look for. Comma-separated string.
*   `incident_id` (string, optional): Microsoft Defender Incident ID for which you want to find related alerts.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of alerts matching the criteria.

### Ping

Test Connectivity to Microsoft Defender ATP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Machine Logon Users

Get users who have logged onto specific machines.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of logged-on users for the specified machines.

### List Machines

Get machines based on specified criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `last_seen_time_frame` (string, optional): Time frame in hours for which to fetch Machines.
*   `machine_name` (string, optional): Full Machine Name to look for.
*   `machine_ip_address` (string, optional): Machine IP Address to look for.
*   `machine_risk_score` (string, optional): Machine risk score to look for. Comma-separated string.
*   `machine_health_status` (string, optional): Machine health status to look for. Comma-separated string.
*   `machine_os_platform` (string, optional): Machine OS platform to look for.
*   `rbac_group_id` (string, optional): RBAC Group ID to look for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of machines matching the criteria.

### List Indicators

List indicators in Microsoft Defender ATP based on specified filters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `indicators` (string, optional): Specify a comma-separated list of indicators that you would like to retrieve.
*   `indicator_types` (string, optional): Specify a comma-separated list of indicator types that you want to retrieve. Possible values: FileSha1, FileSha256, FileMd5, CertificateThumbprint, IpAddress, DomainName, Url.
*   `actions` (string, optional): Specify a comma-separated list of indicator actions that you want to use for filtering. Possible values: Warn,Block,Audit,Alert,AlertAndBlock,BlockAndRemediate,Allowed.
*   `severity` (string, optional): Specify a comma-separated list of severities that you want to use for filtering. Possible values: Informational,Low,Medium,High.
*   `max_results_to_return` (string, optional): Specify how many indicators to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of indicators matching the criteria.

### Submit Entity Indicators

Submit entities as indicators in Microsoft Defender ATP. Supported entities: Filehash, URL, IP Address. Note: only MD5, SHA1 and SHA256 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `action` (List[Any], required): Specify the action that needs to be applied to the entities. Note: "Block And Remediate" is supported only for filehash entities.
*   `severity` (List[Any], required): Specify the severity for the found entities.
*   `indicator_alert_title` (string, required): Specify what should be the title for the alert, if they are identified in the environment.
*   `description` (string, required): Specify the description for the entities.
*   `application` (string, optional): Specify an application that is related to the entities.
*   `recommended_action` (string, optional): Specify what should be the recommended actions for the handling of the entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the submission action.

### Get File Related Alerts

Get alerts related to a specific file hash. Note: For this action only SHA1 is supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `status` (string, optional): Statuses of the alert to look for. Comma-separated string.
*   `severity` (string, optional): Severities of the alert to look for. Comma-separated string.
*   `category` (string, optional): Categories of the alert to look for. Comma-separated string.
*   `incident_id` (string, optional): Microsoft Defender Incident ID for which you want to find related alerts.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash (SHA1 only) entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of alerts related to the file hash.

### Enrich Entities

This action allows a user to enrich Microsoft Defender ATP hosts, ips and file hashes. Note: File hash can be in sha1 or sha256 format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, IP, and FileHash (SHA1, SHA256) entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment information for the specified entities.

### Create Run Antivirus Scan Task

Create a task to run an antivirus scan on specified machines.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `antivirus_scan_type` (List[Any], required): Antivirus Scan Type (e.g., Quick, Full).
*   `comment` (string, required): Comment why an antivirus scan needs to be executed on the machine.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the task creation, likely including the task ID.

### Create Unisolate Machine Task

Create a task to remove machines from isolation.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `comment` (string, required): Comment why the machine needs to be unisolated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the task creation, likely including the task ID.

### Delete Entity Indicators

Delete entity indicators in Microsoft Defender ATP. Supported entities: Filehash, URL, IP Address. Note: only MD5, SHA1 and SHA256 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion action.

## Notes

*   Ensure the Microsoft Defender ATP integration is properly configured in the SOAR Marketplace tab.
*   Pay attention to supported entity types and hash formats (SHA1, SHA256, MD5 where applicable) for specific actions.
*   Some actions like `Get File Related Machines` currently only support SHA1 hashes.
