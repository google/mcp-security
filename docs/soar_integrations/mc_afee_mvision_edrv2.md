# McAfee MVISION EDR V2 Integration

## Overview

This integration allows you to connect to McAfee MVISION EDR V2 to create investigations based on IP addresses and hostnames, and to test connectivity.

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

Test Connectivity to McAfee MVISION EDR V2.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the McAfee MVISION EDR V2 integration is properly configured in the SOAR Marketplace tab.
*   The `Create Investigation` action operates on Hostname or IP address entities within the specified scope.
