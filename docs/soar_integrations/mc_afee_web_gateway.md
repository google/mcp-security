# McAfee Web Gateway Integration

## Overview

This integration allows you to connect to McAfee Web Gateway to manage network object groups, block/unblock IPs, and test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Unblock IP

Delete IP addresses from an "IP range"-type group. *Please note - This group should be a part of rule used to block IP addresses.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): The group name to unblock the IP in.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Item From Group

Remove a network object from a group (ip, url, etc.). *Please note - that each group is type stricted.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): The group name.
*   `item_to_delete` (string, required): The item to delete from the group. Default: x.x.x.x/32.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test Connectivity to McAfee Web Gateway.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Insert Item To Group

Insert a network object to a group (ip, url, etc.). *Please note - that each group is type stricted.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): The group name.
*   `item_to_insert` (string, required): The item ot insert to the group. Default: x.x.x.x/24.
*   `description` (string, optional): The entry description.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Block IP

Insert IP addresses to an "IP range"-type group (Note - This group should be a part of rule used to block IP addresses).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): The group name.
*   `description` (string, optional): The entry description.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the McAfee Web Gateway integration is properly configured in the SOAR Marketplace tab.
*   Actions involving group manipulation are type-strict; ensure the item type matches the group type.
*   Blocking/Unblocking actions typically operate on IP address entities within the specified scope and require the target group to be part of an active blocking rule.
