# F5 BIG-IQ Integration

## Overview

This integration allows you to connect to F5 BIG-IQ and perform actions such as retrieving event logs by blocking ID, changing policy enforcement modes, and testing connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get Event Logs By Blocking ID

Get event logs by its blocking ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `blocking_id` (string, required): The blocking ID to retrieve event logs for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the event logs.

### Ping

BIG-IQ connectivity test.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Change Policy Enforcement Mode

Change the enforcement mode of a policy by its ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_id` (string, required): The ID of the policy to modify.
*   `enforcement_mode` (string, required): The desired enforcement mode (e.g., blocking, transparent).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the F5 BIG-IQ integration is properly configured in the SOAR Marketplace tab.
