# Cisco Firepower Management Center (FMC) Integration

## Overview

This integration allows interaction with Cisco Firepower Management Center (FMC) to manage network objects, URL objects, port objects, and run scripts. Actions include blocking/unblocking IPs and URLs by adding/removing them from groups, blocking/unblocking ports, listing objects within groups, and executing arbitrary scripts on managed devices.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cisco FMC details:

*   **Server Address:** The IP address or hostname of your Cisco FMC.
*   **Username:** The username for an account with API access permissions.
*   **Password:** The password for the API user account.
*   **(Optional) Domain:** The domain name if using multi-domain management.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has sufficient permissions for the desired API calls, including read/write access to network objects, URL objects, port objects, and potentially script execution privileges.)*

## Actions

### Get Ports List By Name

Get list of blocked ports for specific group by its name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `port_group_name` (string, required): The name of the needed ports group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of ports within the specified group.

### Block Address

Block IP address by assigning it to a network group attached to a policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `network_group_name` (string, required): Network object group name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block operation.

### Block URL

Block URL by assigning it to a URL group attached to a policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url_group_name` (string, required): URL group object name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block operation.

### Get URL List By Name

Get list of URLs for specific group by its name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url_group_name` (string, required): The name of the needed URL group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of URLs within the specified group.

### Unblock Port

Remove port from a group of blocked ports.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `port_group_name` (string, required): Name of the port object group.
*   `port` (string, required): Target port to unblock (e.g., `9856`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unblock operation.

### Block Port

Block port by assigning it to a port group attached to a policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `port_group_name` (string, required): Name of the port object group.
*   `port` (string, required): Port to block (e.g., `9856`).
*   `port_protocol` (string, required): Target port protocol (e.g., `TCP`, `UDP`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block operation.

### Ping

Test Connectivity to Cisco Firepower Management Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Unblock URL

Remove URL from a group of blocked URLs.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url_group_name` (string, required): URL group object name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unblock operation.

### Unblock Address

Unblock address in Cisco Firepower by removing it from a network group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `network_group_name` (string, required): Network object group name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unblock operation.

### Get Addresses List By Name

Get list of blocked addresses in a specific network group by its name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `network_group_name` (string, required): The name of the needed network group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of IP addresses/networks within the specified group.

### Run Script

Run arbitrary script with CheckPoint run-script API call. Note: action is not using Siemplify entities to operate. *(Note: Description seems incorrect, likely runs script on Cisco FMC/FTD)*

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `script_text` (string, required): Script to execute.
*   `target` (string, required): Specify Cisco device(s) to execute script on (comma-separated list).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the script execution.

## Notes

*   Ensure the Cisco Firepower Management Center integration is properly configured in the SOAR Marketplace tab with the correct FMC address and credentials.
*   The user account requires sufficient privileges in FMC to perform API operations (e.g., read/write network objects, deploy policies).
*   Changes made via the API (like adding IPs/URLs to groups) typically require a subsequent deployment action on the FMC to take effect on the managed Firepower devices. This deployment step is usually performed manually in the FMC UI or via separate API calls not included in this basic integration.
*   Group names used in actions must exactly match the names configured in FMC.
