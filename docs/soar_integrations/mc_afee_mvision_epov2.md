# McAfee MVISION ePO V2 Integration

## Overview

This integration allows you to connect to McAfee MVISION ePO V2 to manage devices and tags, create investigations, and test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Create Investigation

Create investigations for IP addresses and hostnames.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `case_type` (List[Any], required): Defines the type of alert.
*   `priority` (List[Any], required): Assigns a priority to the investigation.
*   `hint` (string, optional): Automatically links related investigations and avoids creating many cases from multiple alerts related to the same incident. If the same hint is used, the evidences will be added to the already existing investigation.
*   `name` (string, optional): Gives the investigation a meaningful name. If the name is missing, a default case name is assigned.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Host entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ID of the created investigation.

### Ping

Test Connectivity to McAfee MVISION ePO V2.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Add Tag To Device

Add tag to the device in McAfee MVISION ePO V2.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tag_name` (string, required): Specify what tag you want to add to endpoint.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Host entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Devices

List devices that are available in McAfee MVISION ePO V2.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_devices_to_return` (string, optional): Specify how many devices to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, listing available devices.

### List Tags

List tags that are available in McAfee MVISION ePO V2.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_tags_to_return` (string, optional): Specify how many tags to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, listing available tags.

### Remove Tag From Device

Remove tag from the device in McAfee MVISION ePO V2.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tag_name` (string, required): Specify what tag you want to remove from endpoint.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Host entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Enrich Endpoint

Fetch device's system information by its hostname or IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Host entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including endpoint system information.

## Notes

*   Ensure the McAfee MVISION ePO V2 integration is properly configured in the SOAR Marketplace tab.
*   Actions typically operate on Hostname or IP address entities within the specified scope.
