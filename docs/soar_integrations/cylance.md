# Cylance Integration

## Overview

This integration allows interaction with BlackBerry CylancePROTECT to manage endpoint policies, zones, threat data, and global safe/quarantine lists.

## Configuration

To configure this integration within the SOAR platform, you typically need the following CylancePROTECT details:

*   **API URL:** The base URL for your Cylance console API (e.g., `https://protectapi.cylance.com`).
*   **Tenant ID:** Your unique Cylance Tenant ID.
*   **Application ID:** An Application ID generated for API access within the Cylance console.
*   **Application Secret:** The corresponding Application Secret.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API credentials have the necessary permissions for the desired actions, such as managing devices, policies, and threat data.)*

## Actions

### Add To Global List

Add a hash (SHA256) to one of the two global lists: GlobalSafe or GlobalQuarantine.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `list_type` (string, required): The list to add the hash to (e.g., `GlobalSafe`, `GlobalQuarantine`).
*   `category` (string, optional): The category of the hash.
*   `reason` (string, optional): The reason for adding the hash to the list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the operation.

### Get Threat

Enrich a hash (SHA256) with data from Cylance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if the threat Cylance score pass the given threshold (e.g., `3`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing threat details and enrichment data for the specified hash(es).

### Get Threats

Retrieve a list of all available threats detected in the system.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of all threats.

### Ping

Test connectivity to Cylance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enrich Entities

Enrich hostnames and IP addresses with additional device data from Cylance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified host(s)/IP(s).

### Get Global List

Retrieve a list of all hashes in the specified global list (GlobalSafe or GlobalQuarantine).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `list_type` (string, required): Name of the global list (e.g., `GlobalSafe`, `GlobalQuarantine`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of hashes in the specified global list.

### Change Zone

Change zone for an endpoint (group of endpoints) identified by Hostname or IP Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `zones_to_add` (string, optional): Comma-separated list of Zone names to add the endpoint(s) to.
*   `zones_to_remove` (string, optional): Comma-separated list of Zone names to remove the endpoint(s) from.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the zone change operation.

### Delete From Global List

Remove a hash (SHA256) for the specified global list (GlobalSafe or GlobalQuarantine).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `list_type` (string, required): The list to delete the hash from (e.g., `GlobalSafe`, `GlobalQuarantine`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Change Policy

Change the policy of an endpoint (identified by Hostname or IP Address) to an existing policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): The name of the new policy to apply.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy change operation.

### Get Threat Devices

Get threats associated to a particular hostname or an IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of threats associated with the specified device(s).

### Get Threat Download Link

Action fetches The URL you can use to download the file associated with a threat hash (SHA256). The action only provides the URL, it does not download the file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threat_sha256_hash` (string, optional): Comma-separated list of Threat SHA256 hashes. If empty, uses FileHash entities from the scope.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the download URL(s) for the specified threat hash(es).

## Notes

*   Ensure the Cylance integration is properly configured in the SOAR Marketplace tab with the correct API URL, Tenant ID, Application ID, and Application Secret.
*   The API credentials require appropriate permissions within the Cylance console.
*   Hash-based actions primarily use SHA256.
*   Policy and Zone names must match exactly how they appear in the Cylance console.
