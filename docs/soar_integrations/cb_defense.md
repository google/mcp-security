# CB Defense Integration

## Overview

This integration allows you to connect to VMware Carbon Black Endpoint Standard (formerly CB Defense) to manage policies, rules, devices, and events. Actions include creating/deleting policies, adding/removing rules from policies, getting device info and events, and changing device policies.

## Configuration

To configure this integration within the SOAR platform, you typically need the following VMware Carbon Black Endpoint Standard (CB Defense) details:

*   **API URL:** The base URL for your Carbon Black Cloud instance (e.g., `https://defense-prod05.conferdeploy.net`). This is often the same URL used for CB Cloud.
*   **Connector ID:** An API Connector ID generated under API Access in your Carbon Black Cloud settings (often labeled as type 'API').
*   **API Secret Key:** The corresponding API Secret Key generated along with the Connector ID.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API key has the necessary permissions for the actions you intend to use, such as managing alerts, policies, or device actions within CB Defense.)*

## Actions

### Delete Policy

Delete a policy from Cb Defense.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Policy name to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Delete Rule From Policy

Remove a rule from an existing policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Policy name from which to remove the rule.
*   `rule_id` (string, required): Rule ID to remove (e.g., 1).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the rule removal operation.

### Get Events

Get events by entity within a specified timeframe.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `timeframe` (string, required): Timeframe of the search (e.g., 3h, 1d).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports various entity types like IP, Hostname, Hash, User, Process.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of events associated with the entities within the timeframe.

### Ping

Test Connectivity to CB Defense.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Processes

List processes by device within a specified timeframe.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `timeframe` (string, required): Timeframe of the search (e.g., 3h, 1d).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes for the specified devices within the timeframe.

### Create Policy

Create a new Policy on Cb Defense.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Name for the policy.
*   `policy_description` (string, required): A description of the policy.
*   `priority_level` (string, required): The priority score associated with sensors assigned to this policy (e.g., LOW, MEDIUM, HIGH, MISSION_CRITICAL).
*   `policy_details` (string, required): The policy details (likely a JSON string representing the policy configuration).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy creation, likely including the new policy ID.

### Get Device Info

Get information about a device based on IP or Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified device(s).

### Change Policy

Change device policy based on IP or Hostname entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): The new policy name to apply (e.g., TEST_Policy).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy change operation.

## Notes

*   Ensure the CB Defense integration is properly configured in the SOAR Marketplace tab with the correct API URL, Connector ID, and API Secret Key.
*   The API key used requires appropriate permissions within Carbon Black Cloud for the desired actions (e.g., policy management, device actions, event search).
*   Timeframe parameters typically accept formats like '3h' (3 hours) or '1d' (1 day).
*   Refer to Carbon Black Cloud documentation for details on policy configuration structure (`policy_details` parameter).
