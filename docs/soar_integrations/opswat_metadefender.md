# OPSWAT MetaDefender Integration

## Overview

This integration allows you to connect to OPSWAT MetaDefender to scan file hashes and test connectivity.

## Configuration

The configuration for this integration (MetaDefender URL, API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Scan Hash

Scan hash file in Opswat Metadefender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the scan results for the provided file hash(es).

### Ping

Test Connectivity to OPSWAT MetaDefender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the OPSWAT MetaDefender integration is properly configured in the SOAR Marketplace tab with the correct URL and API Key.
*   The `Scan Hash` action operates on FileHash entities within the specified scope.
