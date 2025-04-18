# Check Point Firewall Integration

## Overview

This integration allows interaction with Check Point firewalls (likely via the Management API) to perform actions such as running scripts, managing object groups (IPs, URLs), managing SAM rules, listing policies and layers, and downloading log attachments.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Check Point Management Server details:

*   **Server Address:** The IP address or hostname of your Check Point Management Server.
*   **Username:** The username for an administrator account with API access permissions.
*   **Password:** The password for the administrator account.
*   **(Optional) Port:** The port for the Management API (often defaults to 443).
*   **(Optional) Domain:** The domain name, if managing multiple domains on the Management Server.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has sufficient permissions for the desired API calls.)*

## Actions

### Run Script

Run arbitrary script with CheckPoint run-script API call. Note: action is not using Siemplify entities to operate.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `script_text` (string, required): Script to execute. For example, `fw sam command: fw sam -t 600 -I src 8.9.10.12`.
*   `target` (string, required): Specify CheckPoint device(s) to execute script on (comma-separated list, e.g., `gaia80.10`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the script execution.

### Add Url To Group

Add Url to the Checkpoint FireWall Group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ur_ls_group_name` (string, required): Specify the name of the group to which you want to add URL.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Download Log Attachment

Download log attachments from CheckPoint FireWall.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `log_i_ds` (string, required): Specify the comma-separated list of log IDs from which you want to download attachments.
*   `download_folder_path` (string, required): Specify the absolute path for the folder where the action should store the attachments.
*   `create_case_wall_attachment` (bool, optional): If enabled, action will create a case wall attachment for each successfully downloaded file (max size 3 MB).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including paths to downloaded files.

### Add a SAM Rule

Add a SAM (suspicious activity monitoring) rule for Checkpoint Firewall. Refer to Checkpoint documentation for `fw sam` command criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `security_gateway_to_create_sam_rule_on` (string, required): Specify the name of Security Gateway to create a rule for.
*   `action_for_the_matching_connections` (List[Any], required): Specify the action (e.g., `drop`, `reject`).
*   `how_to_track_matching_connections` (List[Any], required): Specify tracking option (e.g., `log`, `alert`).
*   `source_ip` (string, optional): Specify the source IP.
*   `source_netmask` (string, optional): Specify the source netmask.
*   `destination_ip` (string, optional): Specify the destination IP.
*   `destination_netmask` (string, optional): Specify the destination netmask.
*   `port` (string, optional): Specify the port number (e.g., `5005`).
*   `protocol` (string, optional): Specify the protocol name (e.g., `TCP`).
*   `expiration` (string, optional): Specify rule duration in seconds (e.g., `4`). If empty, rule never expires.
*   `close_connections` (bool, optional): Specify if existing matching connections should be closed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities for source/destination.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the SAM rule creation.

### Add Ip To Group

Add IP to the Checkpoint FireWall Group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `blacklist_group_name` (string, required): Specify the name of the group to which you want to add IP address.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test Connectivity to Check Point Firewall Management Server.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### List Policies On Site

Retrieve all existing policies (Access Control and Threat Prevention packages).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_policies_to_return` (string, optional): Specify how many policies to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of policies.

### Remove SAM Rule

Remove a SAM (suspicious activity monitoring) rule from Checkpoint Firewall. Note: you need to match the current rule parameters exactly to remove it.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `security_gateway` (string, required): Specify the name of Security Gateway from where to remove SAM Rule.
*   `action_for_the_matching_connections` (List[Any], required): Specify the action of the rule to remove.
*   `how_to_track_matching_connections` (List[Any], required): Specify the tracking option of the rule to remove.
*   `source_ip` (string, optional): Specify the source IP of the rule to remove.
*   `source_netmask` (string, optional): Specify the source netmask of the rule to remove.
*   `destination_ip` (string, optional): Specify the destination IP of the rule to remove.
*   `destination_netmask` (string, optional): Specify the destination netmask of the rule to remove.
*   `port` (string, optional): Specify the port number of the rule to remove.
*   `protocol` (string, optional): Specify the protocol name of the rule to remove.
*   `close_connections` (bool, optional): Specify if the rule to remove included closing connections.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities for source/destination.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the SAM rule removal.

### Show Logs

Retrieve logs from CheckPoint FireWall based on the filter.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (List[Any], required): Specify what time frame should be used for log retrieval (e.g., Last Hour, Last Day, Custom).
*   `log_type` (List[Any], required): Specify what type of logs should be returned (e.g., Firewall, Audit).
*   `query_filter` (string, optional): Specify the query filter (Check Point syntax) to return logs.
*   `max_logs_to_return` (string, optional): Specify how many logs to return. Maximum is 100 (Checkpoint limitation).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the retrieved logs.

### Remove Url From Group

Remove URL from the Checkpoint FireWall Group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ur_ls_group_name` (string, required): Specify the name of the group from which you want to remove URL.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove IP From Group

Remove IP from the Checkpoint FireWall Group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `blacklist_group_name` (string, required): Specify the name of the group from which you want to remove IP address.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Layers On Site

Retrieve all of the available Access Control and Threat Prevention layers.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_layers_to_return` (string, optional): Specify how many layers to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available layers.

## Notes

*   Ensure the Check Point Firewall integration is properly configured in the SOAR Marketplace tab with the correct Management Server details and credentials.
*   The user account used requires sufficient permissions in the Check Point Management API.
*   Actions often require publishing changes in the Check Point Management Console to take effect on gateways.
*   Refer to Check Point documentation for specific command syntax (e.g., `fw sam`) and API object structures.
