# Palo Alto Panorama Integration

## Overview

This integration allows you to connect to Palo Alto Networks Panorama to manage security policies, address groups, URL categories across device groups, commit changes, push configurations, and query logs.

## Configuration

The configuration for this integration (Panorama IP/Hostname, Username, Password/API Key) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

**Important:** Actions require specifying the target `device_name` (usually `localhost.localdomain` for Panorama itself) and `device_group_name`. You can find the correct names by browsing the Panorama configuration via the provided URLs in the action descriptions or using the Panorama web interface/CLI.

## Actions

### Edit Blocked Applications

Block and unblock applications within a specific security policy in a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name (e.g., `localhost.localdomain`).
*   `device_group_name` (string, required): Specify name of the device group.
*   `policy_name` (string, required): Specify name of the policy.
*   `applications_to_block` (string, optional): Comma-separated list of application names to add to the policy's block list (e.g., `apple-siri,app2`).
*   `applications_to_un_block` (string, optional): Comma-separated list of application names to remove from the policy's block list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy modification.

### Block IPs in Policy

Block IP addresses by adding them to a security policy's source or destination list within a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name.
*   `device_group_name` (string, required): Specify name of the device group.
*   `policy_name` (string, required): Specify name of the policy.
*   `target` (string, required): Specify whether to add IPs to the `source` or `destination` list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy modification.

### Get Correlated Traffic Between IPs

Returns correlated network traffic logs from Palo Alto Panorama between Source IP Address and Destination IP Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_ip` (string, required): Specify source IP.
*   `destination_ip` (string, required): Specify destination IP.
*   `max_hours_backwards` (string, optional): Specify the amount of hours from where to fetch logs.
*   `max_logs_to_return` (string, optional): Specify how many logs to return. Maximum is 1000.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the correlated traffic logs.

### Add IPs to Group

Add IP addresses to an address group object within a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): Specify name of the device.
*   `device_group_name` (string, required): Specify name of the device group.
*   `address_group_name` (string, required): Specify name of the address group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the group modification.

### Search logs

Search logs in Palo Alto Panorama based on the query and log type.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `log_type` (List[Any], required): Specify which log type should be returned (e.g., traffic, threat).
*   `query` (string, optional): Specify the query filter (e.g., `(addr.src in 10.0.0.1)`).
*   `max_hours_backwards` (string, optional): Specify the amount of hours from where to fetch logs.
*   `max_logs_to_return` (string, optional): Specify how many logs to return. Maximum is 1000.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the log search results.

### Commit Changes

Commit configuration changes made on Panorama. NOTICE! For using Only My Changes option, the user must be an admin.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `only_my_changes` (bool, required): Commit only the changes made by the configured user (requires admin privileges).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the commit operation, including the job ID.

### Ping

Test connectivity to Panorama.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Unblock Urls

Remove URLs from a given custom URL category within a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): Specify name of the device.
*   `device_group_name` (string, required): Specify name of the device group.
*   `url_category_name` (string, required): Specify name of the URL Category.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the URL category modification.

### Push Changes

Push committed changes to a device group in Palo Alto Panorama. Note: It can take several minutes before changes are pushed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_group_name` (string, required): The device group to push changes to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the push operation, including the job ID.

### Block Urls

Add URLs to a given custom URL category within a device group. (NOTE: To actually block the URL, create a policy and add the desired URL category to it.). URLs cannot exceed 255 characters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): Specify name of the device.
*   `device_group_name` (string, required): Specify name of the device group.
*   `url_category_name` (string, required): Specify name of the URL Category.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the URL category modification.

### Remove IPs from Group

Remove IP addresses from an address group object within a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): Specify name of the device.
*   `device_group_name` (string, required): Specify name of the device group.
*   `address_group_name` (string, required): Specify name of the address group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the group modification.

### Unblock IPs in Policy

Unblock IP addresses in a policy by removing them from the source or destination list within a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name.
*   `device_group_name` (string, required): Specify name of the device group.
*   `policy_name` (string, required): Specify name of the policy.
*   `target` (string, required): Specify whether to remove IPs from the `source` or `destination` list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy modification.

### Get Blocked Applications

List all blocked applications in a given security policy within a device group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): Specify name of the device.
*   `device_group_name` (string, required): Specify name of the device group.
*   `policy_name` (string, required): Specify name of the policy.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of applications blocked by the specified policy.

## Notes

*   Ensure the Palo Alto Panorama integration is properly configured in the SOAR Marketplace tab.
*   Specify correct `device_name` (usually `localhost.localdomain`) and `device_group_name`.
*   Configuration changes (adding IPs/URLs, modifying policies) require a separate `Commit Changes` action followed by a `Push Changes` action to take effect on managed firewalls.
*   Blocking URLs requires adding them to a custom URL category that is then used in a security policy with a block action.
