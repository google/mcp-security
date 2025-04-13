# F5 BIG-IP iControl API Integration

## Overview

This integration allows you to interact with F5 BIG-IP devices using the iControl REST API. It provides actions to manage network objects like data groups (address lists, port lists) and iRules.

## Configuration

The configuration for this integration (BIG-IP address, username, password) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Add IP To Data Group

Add IP addresses to an internal data group in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `data_group_name` (string, required): Specify the name of the data group to which you want to add IP addresses.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create Data Group

Create an internal data group in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `type` (List[Any], required): Specify the type for the data group (e.g., ip, string).
*   `name` (string, required): Specify the name of the data group that needs to be created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add IP To Address List

Add IP addresses to an address list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_list_name` (string, required): Specify the name of the address list to which you want to add IP addresses.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Port To Port List

Add ports to a port list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `port_list_name` (string, required): Specify the name of the port list to which you want to add ports.
*   `ports` (string, required): Specify a comma-separated list of ports that need to be added.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Port From Port List

Remove ports from a port list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `port_list_name` (string, required): Specify the name of the port list from which you want to remove ports.
*   `ports` (string, required): Specify a comma-separated list of ports that need to be removed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create iRule

Create an iRule in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the iRule that needs to be created.
*   `rule` (string, required): Specify the rule (TCL script content) that needs to be executed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Address Lists

List available address lists in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equal, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter. Filtering is based on the address list name.
*   `max_address_lists_to_return` (string, optional): Specify how many address lists to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the list of address lists.

### Update iRule

Update an existing iRule in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the iRule that needs to be updated.
*   `rule` (string, required): Specify the new rule (TCL script content) that needs to be executed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove IP From Address List

Remove IP addresses from an address list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_list_name` (string, required): Specify the name of the address list from which you want to remove IP addresses.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete iRule

Delete an iRule in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the iRule that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the F5 BIG-IP with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Data Group

Delete an internal data group in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the data group that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create Address List

Create an address list in F5 BIG-IP. Note: address list requires at least one IP address entity in scope during creation.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the address list that needs to be created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Requires at least one IP address entity.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Port Lists

List available port lists in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equal, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter. Filtering is based on the port list name.
*   `max_port_lists_to_return` (string, optional): Specify how many port lists to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the list of port lists.

### Create Port List

Create a port list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the port list that needs to be created. Note: name shouldn't contain whitespace. This is F5 BIG-IP limitation.
*   `ports` (string, required): Specify a comma-separated list of ports that will be a part of the new port list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Port List

Delete a port list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the port list that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Address List

Delete an address list in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the address list that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List iRules

List available iRules in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equal, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter. Filtering is based on the iRule name.
*   `max_i_rules_to_return` (string, optional): Specify how many iRules to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the list of iRules.

### List Data Groups

List available internal data groups in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equal, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter. Filtering is based on the data group name.
*   `max_data_groups_to_return` (string, optional): Specify how many data groups to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the list of data groups.

### Remove IP From Data Group

Remove IP addresses from an internal data group in F5 BIG-IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `data_group_name` (string, required): Specify the name of the data group from which you want to remove IP addresses.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the F5 BIG-IP iControl API integration is properly configured in the SOAR Marketplace tab.
*   Some actions only support internal data groups.
*   Creating an address list requires at least one IP address entity in scope.
*   Port list names cannot contain whitespace due to F5 BIG-IP limitations.
