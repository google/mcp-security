# CB Cloud Integration

## Overview

This integration allows you to connect to VMware Carbon Black Cloud to perform various actions related to device management, process searching, alert handling, and reputation management. Actions include searching processes, scanning devices, managing device quarantine and bypass modes, managing reputation overrides (for hashes, certificates, IT tools), enriching entities, updating device policies, and dismissing alerts.

## Configuration

To configure this integration within the SOAR platform, you typically need the following VMware Carbon Black Cloud details:

*   **API URL:** The base URL for your Carbon Black Cloud instance (e.g., `https://defense-prod05.conferdeploy.net`).
*   **Org Key:** Your organization key found in the Carbon Black Cloud console.
*   **API ID:** An API Key ID generated under API Access in your Carbon Black Cloud settings.
*   **API Secret Key:** The corresponding API Secret Key generated along with the API ID.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API key has the necessary permissions for the actions you intend to use, such as device actions, alert management, or watchlist management.)*

## Actions

### Execute Entity Processes Search

Execute Carbon Black Cloud Process Search based on the Siemplify Entity. Action can be used to search information about processes stored in Carbon Black Cloud with action input parameters and following Siemplify entities: IP, Host, User, Hash, Process.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `start_from_row` (string, optional): Specify from which row action should fetch data.
*   `max_rows_to_return` (string, optional): Specify how many rows action should return.
*   `create_insight` (bool, optional): If enabled, action will create a Siemplify insight based on process info from Carbon Black Cloud.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP, Host, User, Hash, Process entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Device Background Scan

Create a device background scan task on VMware Carbon Black Cloud server based on the Siemplify IP or Host Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely confirming the scan task creation.

### List Reputation Overrides

List reputation overrides configured in VMware Carbon Black Cloud. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `reputation_override_list` (List[Any], optional): Specify override list action should return (e.g., BLACK_LIST, WHITE_LIST).
*   `reputation_override_type` (List[Any], optional): Specify override type action should return (e.g., SHA256, CERT, IT_TOOL).
*   `start_from_row` (string, optional): Specify from which row action should fetch data.
*   `max_rows_to_return` (string, optional): Specify how many rows action should return.
*   `rows_sort_order` (List[Any], optional): Specify sort order for the returned rows (Ascending/Descending). Rows are sorted based on "create_time" value.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of reputation overrides matching the criteria.

### Create a Reputation Override for SHA-256 Hash

Create a Reputation Override for the provided hash in SHA-256 format. Note: The SHA-256 hash can be provided either as a Siemplify FileHash (artifact) or as an action input parameter. If the hash is passed to action both as an entity and input parameter - action will be executed on the input parameter.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filename` (string, required): Specify a corresponding file name to add to reputation override.
*   `reputation_override_list` (List[Any], required): Specify override list to create (e.g., BLACK_LIST, WHITE_LIST).
*   `sha_256_hash` (string, optional): Specify a SHA-256 hash value to create override for.
*   `description` (string, optional): Specify a description for the created reputation override.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the reputation override creation.

### Create a Reputation Override for Certificate

Create a Reputation Override for the certificate. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `signed_by` (string, required): Specify the name of the signer to add to reputation override.
*   `reputation_override_list` (List[Any], required): Specify override list to create (e.g., BLACK_LIST, WHITE_LIST).
*   `certificate_authority` (string, optional): Specify the Certificate Authority that authorizes the validity of the certificate.
*   `description` (string, optional): Specify a description for the created reputation override.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the reputation override creation.

### Quarantine Device

Create quarantine device task on the VMware Carbon Black Cloud server based on the Siemplify IP or Host Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the quarantine action.

### Ping

Test connectivity to the VMware Carbon Black Cloud.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enable Bypass Mode for Device

Create enable bypass mode task for device on VMware Carbon Black Cloud server based on Siemplify IP or Host Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create a Reputation Override for IT Tool

Create a Reputation Override for the specific IT Tool based on a file name and path. Note: The file name can be provided either as a Siemplify File (artifact) or as an action input parameter. Input parameter takes priority. File name will be appended to the File Path parameter.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): Specify a file path where corresponding IT Tool is stored on disk. Example: C:\\TMP\\
*   `reputation_override_list` (List[Any], required): Specify override list to create (e.g., BLACK_LIST, WHITE_LIST).
*   `file_name` (string, optional): Specify a corresponding file name.
*   `description` (string, optional): Specify a description for the created reputation override.
*   `include_child_processes` (bool, optional): If enabled, include IT Tool's child processes on approved list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports File entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the reputation override creation.

### Enrich Entities

Enrich Siemplify Host or IP entities based on the device information from the VMware Carbon Black Cloud.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

### Update a Policy for Device by Policy ID

Change a policy on VMware Carbon Black Cloud sensor on a host. The action scope is IP or Host entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_id` (string, required): Specify a policy ID to associate with the sensor.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy update action.

### Dismiss VMware Carbon Black Cloud Alert

Dismiss VMware Carbon Black Cloud alert. Note: action accepts alert id in format 27162661199ea9a043c11ea9a29a93652bc09fd, not in format that is shown in UI as DONAELUN.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Alert ID to dismiss on VMware Carbon Black Cloud server.
*   `reason_for_dismissal` (List[Any], required): VMware Carbon Black Cloud reason for alert dismissal.
*   `determination` (List[Any], required): Specify the determination to set for an alert (e.g., TRUE_POSITIVE, FALSE_POSITIVE).
*   `message_for_alert_dismissal` (string, optional): Message to add to alert dismissal.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the dismissal action.

### List Host Vulnerabilities

List vulnerabilities found on the host in Сarbon Black Cloud. Supported entities: IP Address and Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `severity_filter` (string, optional): Specify the comma-separated list of severities (Critical, Important, Moderate, Low). If empty, returns all.
*   `max_vulnerabilities_to_return` (string, optional): Specify how many vulnerabilities to return per host. If empty, returns all.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of vulnerabilities for the specified host(s).

### Delete a Reputation Override

Delete a Reputation Override based on the provided reputation override id. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `reputation_override_id` (string, required): Specify a Reputation Override ID to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Unquarantine Device

Create unquarantine device task on the VMware Carbon Black Cloud server based on the Siemplify IP or Host Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unquarantine action.

### Disable Bypass Mode for Device

Create disable bypass mode task for devices on the VMware Carbon Black Cloud server based on the Siemplify IP or Host Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the CB Cloud integration is properly configured in the SOAR Marketplace tab with the correct API URL, Org Key, API ID, and API Secret Key.
*   The API key used requires appropriate permissions within Carbon Black Cloud for the desired actions.
*   Some actions have specific entity type requirements (e.g., Hostname, IP Address, FileHash).
*   Reputation override actions require careful specification of override lists (BLACK_LIST/WHITE_LIST) and types (SHA256/CERT/IT_TOOL).
