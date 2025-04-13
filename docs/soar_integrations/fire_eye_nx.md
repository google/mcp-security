# FireEye NX Integration

## Overview

This integration allows you to connect to FireEye Network Security (NX) and perform actions related to IPS policy exceptions, connectivity testing, and downloading alert artifacts.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Add IPS Policy Exception

Adds a new Intrusion Prevention System (IPS) policy exception in FireEye NX based on attacker IP entities and victim subnet information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `victim_ip_subnet` (string, required): The IP subnet of the victim for the policy exception (Format: x.x.x.x/xx, e.g., 10.0.0.1/24).
*   `interface` (List[Any], required): The interface to apply the policy exception to.
*   `mode` (List[Any], required): The mode for the policy exception.
*   `name` (string, optional): A custom name for the policy exception. If not provided, a default name like `Siemplify_{Interface}_{Mode}` is used.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. IP entities are treated as "Attacker IP Address".
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Tests connectivity to the configured FireEye NX appliance using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Download Alert Artifacts

Downloads artifacts associated with a specific alert from FireEye NX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_uuid` (string, required): The UUID of the alert whose artifacts should be downloaded.
*   `download_path` (string, required): The absolute path on the SOAR server where the artifacts should be saved.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download action, potentially including paths to the downloaded files.

## Notes

*   Ensure the FireEye NX integration is properly configured in the SOAR Marketplace tab.
*   The `Add IPS Policy Exception` action uses IP entities from the scope as the "Attacker IP Address" for the exception rule.
*   Some actions rely on underlying scripts executed by the SOAR platform.
