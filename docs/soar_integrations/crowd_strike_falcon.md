# CrowdStrike Falcon Integration

## Overview

This integration allows interaction with the CrowdStrike Falcon platform to manage endpoints, detections, incidents, IOCs, and run response actions. Actions include managing host containment, updating detections/incidents, managing custom IOCs, running scripts/commands, submitting files/URLs for analysis, and retrieving host/vulnerability information.

## Configuration

To configure this integration within the SOAR platform, you typically need the following CrowdStrike Falcon API details:

*   **API URL:** The base URL for your CrowdStrike Falcon API (e.g., `https://api.crowdstrike.com`, `https://api.us-2.crowdstrike.com`, `https://api.eu-1.crowdstrike.com`, `https://api.laggar.gcw.crowdstrike.com`).
*   **Client ID:** Your CrowdStrike Falcon API Client ID.
*   **Client Secret:** Your CrowdStrike Falcon API Client Secret.
*   **(Optional) Customer ID (CID):** Required for certain actions if managing multiple customers (MSSP).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API client has the necessary permissions (scopes) assigned for the desired actions, e.g., Hosts:Read/Write, Detections:Read/Write, Incidents:Read/Write, IOCs:Read/Write, Real Time Response:Read/Write/Admin, Falcon Sandbox:Read/Write, etc.)*

## Actions

### Add Comment to Detection

Add a comment to the detection in Crowdstrike Falcon.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `detection_id` (string, required): Specify the id of the detection to which you want to add a comment.
*   `comment` (string, required): Specify the comment that needs to be added to the detection.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Submit URL

Submit urls to a sandbox in Crowdstrike. Note: This action requires a Falcon Sandbox license.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ur_ls` (string, required): Specify the URLs that need to be submitted (comma-separated for multiple).
*   `sandbox_environment` (List[Any], optional): Specify the sandbox environment for the analysis (e.g., Windows 7 64-bit).
*   `network_environment` (List[Any], optional): Specify the network environment for the analysis.
*   `check_duplicate` (bool, optional): If enabled, checks if the URL was previously submitted and returns the existing report.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the submission, likely including submission IDs or analysis status.

### Update Incident

Update incident status and assignment in Crowdstrike.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the ID of the incident that needs to be updated.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `status` (List[Any], optional): Specify the status for the incident (e.g., `New`, `InProgress`, `Closed`).
*   `assign_to` (string, optional): Specify the name or email of the analyst to assign the incident to. Use "Unassign" to remove assignment. Format: "{first name} {last name}".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the incident update operation.

### Run Script

Execute a PowerShell script on the endpoints in Crowdstrike using Real-time Response. Note: Action runs asynchronously.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `script_name` (string, optional): The name of a pre-uploaded script file to execute. Either `script_name` or `raw_script` is required.
*   `raw_script` (string, optional): Raw PowerShell script payload to execute. Takes priority over `script_name` if both are provided.
*   `hostname` (string, optional): Comma-separated list of hostnames to run the script on (in addition to entities).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the script execution initiation.

### Execute Command

Execute commands on the hosts in Crowdstrike Falcon using Real-time Response.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `command` (string, required): Specify what command to execute on the hosts (e.g., `ls`, `ps`, `put <filename>`).
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `admin_command` (bool, optional): If enabled, execute commands with admin permissions (needed for commands like `put`).
*   `hostname` (string, optional): Comma-separated list of hostnames to run the command on (in addition to entities).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the command execution.

### Close Detection

Close a Crowdstrike Falcon detection. Note: `Update Detection` action is preferred.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `detection_id` (string, required): Specify the ID of the detection to close.
*   `hide_detection` (bool, optional): If enabled, hide the detection in the UI.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the close operation.

### Add Incident Comment

Add comment to incident in Crowdstrike.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the ID of the incident to update.
*   `comment` (string, required): Specify the comment for the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Update Alert

Update an alert's status, verdict, or assignment in Crowdstrike.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert to update.
*   `status` (List[Any], optional): Specify the status for the alert (e.g., `new`, `in_progress`, `closed`).
*   `verdict` (List[Any], optional): Specify the verdict for the alert (e.g., `true_positive`, `false_positive`).
*   `assign_to` (string, optional): Specify the name or email of the analyst to assign the alert to. Use "Unassign" to remove assignment.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the alert update operation.

### List Hosts

List available hosts in Crowdstrike Falcon, with optional filtering.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `filter_logic` (List[Any], optional): Specify filter logic (e.g., `Equals`, `Contains`).
*   `filter_value` (string, optional): Specify the value to filter hosts by (field depends on logic, often hostname or IP).
*   `max_hosts_to_return` (string, optional): Specify how many hosts to return. Default: 50. Maximum: 1000.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of hosts matching the criteria.

### Add Identity Protection Detection Comment

Add a comment to identity protection detection in Crowdstrike. Requires Identity Protection license.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `detection_id` (string, required): Specify the ID of the identity protection detection.
*   `comment` (string, required): Specify the comment for the detection.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Get Hosts by IOC (Deprecated)

DEPRECATED. List hosts related to the IOCs in Crowdstrike Falcon.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, URL, IP Address, Hash (MD5, SHA256).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of hosts associated with the IOCs.

### Ping

Test Connectivity to CrowdStrike Falcon.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Contain Endpoint

Contain endpoint in Crowdstrike Falcon. Supported entities: Hostname and IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `fail_if_timeout` (bool, optional): If enabled, action will fail if not all endpoints were contained within the timeout.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the containment operation.

### Add Alert Comment

Add a comment to alert in Crowdstrike.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert to update.
*   `comment` (string, required): Specify the comment for the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Update IOC Information

Update information about custom IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash (MD5, SHA256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `description` (string, optional): Specify a new description for custom IOCs.
*   `source` (string, optional): Specify the source for custom IOCs.
*   `expiration_days` (string, optional): Specify the amount of days till expiration.
*   `detect_policy` (bool, optional): If enabled, identified IOCs will send a notification. Otherwise, no action is taken.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, URL, IP Address, Hash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the IOC update operation.

### Download File

Download files from the hosts in Crowdstrike Falcon using Real-time Response. Supported entities: File Name, IP Address and Hostname. Note: Requires both File Name and IP/Hostname entity. Downloaded file is password-protected zip ("infected").

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `download_folder_path` (string, required): Specify the path to the folder where the file should be stored.
*   `overwrite` (bool, required): If enabled, overwrite the file if it already exists.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Requires File Name and (Hostname or IP Address) entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including the path to the downloaded zip file.

### Get Event Offset

Retrieve the event offset used by the Event Streaming Connector. Note: action starts processing events from 30 days ago.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_events_to_process` (string, required): Specify how many events the action needs to process starting from the offset.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the event offset.

### Upload IOCs

Add custom IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash (MD5, SHA256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `platform` (string, required): Comma-separated list of platforms (Windows, Linux, Mac).
*   `severity` (List[Any], required): Specify the severity for the IOC (e.g., `High`, `Medium`).
*   `comment` (string, optional): Specify a comment with more context related to IOC.
*   `host_group_name` (string, optional): Specify the name of the host group to apply the IOC to.
*   `action` (List[Any], optional): Specify the action (`Detect`, `Block`). Note: "Block" only applies to hashes; defaults to "Detect" for others.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, URL, IP Address, Hash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the IOC upload operation.

### Get Host Information

Retrieve information about the hostname from Crowdstrike Falcon. Supported entities: Hostname, IP Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `create_insight` (bool, optional): If enabled, create insights containing host information.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified host(s).

### On-Demand Scan

Scan the endpoint on demand in Crowdstrike. Note: only Windows hosts are supported. Action runs asynchronously. Requires Falcon Spotlight license.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths_to_scan` (string, required): Comma-separated list of paths to scan.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `file_paths_to_exclude_from_scan` (string, optional): Comma-separated list of paths to exclude.
*   `host_group_name` (string, optional): Comma-separated list of host group names to scan.
*   `scan_description` (string, optional): Description for the scan. Defaults to "Scan initialized by Chronicle SecOps."
*   `cpu_priority` (List[Any], optional): CPU priority for the scan (e.g., `Low`, `Medium`, `High`).
*   `sensor_anti_malware_detection_level` (List[Any], optional): Sensor AV detection level.
*   `sensor_anti_malware_prevention_level` (List[Any], optional): Sensor AV prevention level.
*   `cloud_anti_malware_detection_level` (List[Any], optional): Cloud AV detection level.
*   `cloud_anti_malware_prevention_level` (List[Any], optional): Cloud AV prevention level.
*   `quarantine_hosts` (bool, optional): If enabled, quarantine hosts as part of scanning.
*   `create_endpoint_notification` (bool, optional): If enabled, create an endpoint notification for the scan.
*   `max_scan_duration` (string, optional): Max scan duration in hours. If empty, runs continuously.
*   `hostname` (string, optional): Comma-separated list of hostnames to scan (in addition to entities).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the scan initiation.

### Update Identity Protection Detection

Update an identity protection detection in Crowdstrike. Note: requires an Identity Protection license.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `detection_id` (string, required): Specify the ID of the identity protection detection to update.
*   `status` (List[Any], optional): Specify the status for the detection (e.g., `new`, `closed`).
*   `assign_to` (string, optional): Specify the name or email of the analyst to assign the detection to. Use "Unassign" to remove assignment.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### Get Process Name By IOC (Deprecated)

DEPRECATED. Retrieve processes related to the IOCs and provided devices in Crowdstrike Falcon.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `devices_names` (string, required): Specify a comma-separated list of devices to search on.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, URL, IP Address, Hash (MD5, SHA256).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes related to the IOCs on the specified devices.

### Delete IOC

Delete custom IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash (MD5, SHA256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, URL, IP Address, Hash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the IOC deletion operation.

### List Uploaded IOCs

List available custom IOCs in CrowdStrike Falcon, with optional filtering.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ioc_type_filter` (string, optional): Comma-separated list of IOC types to return (e.g., `ipv4`, `ipv6`, `md5`, `sha256`, `domain`). If empty, returns all types.
*   `value_filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains).
*   `value_filter_string` (string, optional): Specify the string value to filter IOCs by.
*   `max_io_cs_to_return` (string, optional): Specify how many IOCs to return. Default: 50. Maximum: 500.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of custom IOCs matching the criteria.

### Submit File

Submit files to a sandbox in Crowdstrike. Note: Requires Falcon Sandbox license. Refer to documentation for supported file formats.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths` (string, required): Specify the file paths to the files that need to be submitted (comma-separated for multiple).
*   `sandbox_environment` (List[Any], optional): Specify the sandbox environment for the analysis.
*   `network_environment` (List[Any], optional): Specify the network environment for the analysis.
*   `archive_password` (string, optional): Password for archive files.
*   `document_password` (string, optional): Password for Adobe or Office files (max 32 characters).
*   `check_duplicate` (bool, optional): If enabled, check for previous submissions and return existing report.
*   `comment` (string, optional): Specify a comment for the submission.
*   `confidential_submission` (bool, optional): If enabled, the file is only shown to users within your customer account.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the file submission, likely including submission IDs or analysis status.

### Update Detection

Update detection status or assignment in Crowdstrike Falcon.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `detection_id` (string, required): Specify the ID of the detection to update.
*   `status` (List[Any], required): Specify the new status for the detection (e.g., `new`, `in_progress`, `true_positive`, `false_positive`, `ignored`).
*   `assign_detection_to` (string, optional): Specify the email address of the user to assign the detection to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the detection update operation.

### List Host Vulnerabilities

List vulnerabilities found on the host in Crowdstrike Falcon. Supported entities: IP Address and Hostname. Note: requires Falcon Spotlight license and permissions.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `severity_filter` (string, optional): Comma-separated list of severities (Critical, High, Medium, Low, Unknown). If empty, returns all.
*   `create_insight` (bool, optional): If enabled, create an insight per entity with vulnerability statistics.
*   `max_vulnerabilities_to_return` (string, optional): Specify how many vulnerabilities to return per host. If empty, returns all.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of vulnerabilities for the specified host(s).

### Lift Contained Endpoint

Lift endpoint containment in Crowdstrike Falcon. Supported entities: Hostname and IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): Specify the Customer ID (CID) if applicable (MSSP).
*   `fail_if_timeout` (bool, optional): If enabled, action fails if containment is not lifted on all endpoints within the timeout.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the lift containment operation.

## Notes

*   Ensure the CrowdStrike Falcon integration is properly configured in the SOAR Marketplace tab with the correct API URL, Client ID, and Client Secret.
*   The API Client requires appropriate permissions (scopes) for the desired actions.
*   Some actions require specific licenses (e.g., Falcon Sandbox, Falcon Spotlight, Identity Protection).
*   Real-time Response (RTR) actions like `Run Script`, `Execute Command`, `Download File` require the Falcon agent to be active and connected. These actions might run asynchronously.
*   Hash-based IOC actions support MD5 and SHA256.
