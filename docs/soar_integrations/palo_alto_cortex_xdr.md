# Palo Alto Cortex XDR Integration

## Overview

This integration allows you to connect to Palo Alto Networks Cortex XDR to manage incidents, endpoints, and block lists. Actions include updating incidents, isolating/unisolating endpoints, managing hash block lists, enriching entities, querying incident data, retrieving agent reports, and testing connectivity.

## Configuration

The configuration for this integration (API URL, API Key, API Key ID, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Add Hashes to Block List

Adds SHA256 file hashes to a block list. Note: Only SHA256 format is supported. Files already on allow/block lists are ignored.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `comment` (string, optional): Additional comment regarding the action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash (SHA256) entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block list update operation.

### Update an Incident

Updates specific fields of a Cortex XDR incident, such as status, severity, and assignee.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): The ID of the incident to be updated.
*   `assigned_user_name` (string, optional): The updated full name of the incident assignee.
*   `severity` (List[Any], optional): Administrator-defined severity (e.g., low, medium, high, critical).
*   `status` (List[Any], optional): Updated incident status (e.g., new, under_investigation, resolved).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the incident update operation.

### Ping

Test connectivity to Palo Alto Cortex XDR.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Endpoint Agent Report

Get the agent report for an endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the agent report details for the specified endpoint(s).

### Query

Get data of a specific incident including alerts and key artifacts.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): The ID of the incident for which you want to retrieve data.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed data for the specified incident.

### Resolve an Incident

Resolves (closes) a specific XDR incident with a resolution status and comment.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): The ID of the incident to be updated.
*   `status` (List[Any], required): Updated incident status (typically a resolved status like 'resolved_benign', 'resolved_false_positive', etc.).
*   `resolve_comment` (string, optional): Descriptive comment explaining the incident change/resolution.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the incident resolution operation.

### Enrich Entities

Enrich Siemplify Host and IP entities based on the information from the Palo Alto Cortex XDR.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

### Isolate Endpoint

Isolate an endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the isolation operation.

### Unisolate Endpoint

Unisolate an endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unisolation operation.

## Notes

*   Ensure the Palo Alto Cortex XDR integration is properly configured in the SOAR Marketplace tab with the correct API details.
*   The `Add Hashes to Block List` action specifically requires SHA256 hashes.
*   Endpoint actions typically support targeting via Hostname or IP Address entities.
