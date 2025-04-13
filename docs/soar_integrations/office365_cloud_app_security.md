# Microsoft Defender for Cloud Apps (formerly Office 365 Cloud App Security) Integration

## Overview

This integration allows you to connect to Microsoft Defender for Cloud Apps to retrieve user and IP-related activities, manage IP address ranges, close alerts, list files, and test connectivity.

## Configuration

The configuration for this integration (API URL, API Token, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get User related activities

View activities related to a user within a specified time frame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (string, required): Specify the value in hours ago to fetch activities for.
*   `activity_display_limit` (string, optional): Limit on the number of activities to display.
*   `product_name` (string, optional): Filter activities by a specific connected app (e.g., "Office 365"). The name is mapped to the product code internally.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the user-related activities.

### Create IP Address Range

Create IP address range in Microsoft Defender for Cloud Apps.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name for the IP address range.
*   `category` (List[Any], required): Specify the category for the IP address range.
*   `subnets` (string, required): Specify a comma-separated list of subnets (e.g., 192.168.1.0/24,10.0.0.0/8).
*   `organization` (string, optional): Specify the organization for the IP address range.
*   `tags` (string, optional): Specify a comma-separated list of tags for the IP address range.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the IP address range creation.

### Close Alert

Close alert in Microsoft Defender for Cloud Apps.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert that needs to be closed.
*   `state` (List[Any], required): Specify the state of the alert (e.g., Benign, True Positive).
*   `comment` (string, optional): Specify a comment about why the alert is closed.
*   `reason` (List[Any], optional): Specify a reason why the alert should be closed (not applicable if state is "True Positive").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the close alert operation.

### Remove IP From IP Address Range

Remove IP address from IP address range in Microsoft Defender for Cloud Apps. Supported entities: IP address. Note: action can only remove exact matches.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name for the IP address range that needs to be updated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the removal operation.

### Ping

Test connectivity to Microsoft Defender for Cloud Apps.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Bulk Resolve Alert (Deprecated)

Deprecated. Please refer to action "Close Alert".

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Alert Unique Identifier. Can take multiple IDs which are comma separated.
*   `comment` (string, optional): A comment to explain why alerts are resolved.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add IP To IP Address Range

Add IP address to IP address range in Microsoft Defender for Cloud Apps. Supported entities: IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name for the IP address range that needs to be updated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the addition operation.

### Get IP related activities

View activities related to an IP address within a specified time frame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (string, required): Specify the value in hours ago to fetch activities for.
*   `activity_display_limit` (string, optional): Limit on the number of activities to display.
*   `product_name` (string, optional): Filter activities by a specific connected app (e.g., "Office 365"). The name is mapped to the product code internally.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the IP-related activities.

### Enrich Entities

Enrich entities using information from Microsoft Defender for Cloud Apps. Supported entities: Username.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

### List Files

List available files in Microsoft Defender for Cloud Apps based on specified filters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key to filter files (e.g., File Type, Share Status, File Name, ID).
*   `filter_logic` (List[Any], optional): Specify filter logic (e.g., Equals, Contains). Note: Contains logic only works for File Name and ID.
*   `filter_value` (string, optional): Specify the value to filter by.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50. Note: Contains logic only searches the first 1000 results.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of files matching the criteria.

### Dismiss Alert (Deprecated)

Deprecated. Please refer to action "Close Alert".

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Alert Unique Identifier. Takes a single alert ID.
*   `comment` (string, optional): A comment to explain why an alert is dismissed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the Microsoft Defender for Cloud Apps integration is properly configured in the SOAR Marketplace tab with a valid API Token.
*   The actions `Bulk Resolve Alert` and `Dismiss Alert` are deprecated; use `Close Alert` instead.
*   The `Remove IP From IP Address Range` action only removes exact IP address matches, not ranges defined by CIDR notation within the range.
