# Micro Focus ITSMA Integration

## Overview

This integration allows you to connect to Micro Focus IT Service Management Automation (ITSMA) to create and update incidents, and test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Update Incident

Update an existing incident in Micro Focus ITSMA.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): The ID of the incident to update.
*   `display_label` (string, optional): The updated display label of the incident.
*   `description` (string, optional): The updated description of the incident.
*   `impact_scope` (string, optional): The updated impact score of the incident.
*   `urgency` (string, optional): The updated urgency of the incident.
*   `service_id` (string, optional): The updated Id of the category of the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test Connectivity to Micro Focus ITSMA.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Create Incident

Create a new incident in Micro Focus ITSMA.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `display_label` (string, required): The display label of the incident.
*   `description` (string, required): The description of the incident.
*   `impact_scope` (string, required): The impact scope of the incident.
*   `urgency` (string, required): The urgency of the incident.
*   `service_id` (string, required): The id of the category of the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ID of the created incident.

### Update Incident External Status

Update the external status for an incident in Micro Focus ITSMA.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): The ID of the incident.
*   `status` (string, required): The updated external status of the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the Micro Focus ITSMA integration is properly configured in the SOAR Marketplace tab.
