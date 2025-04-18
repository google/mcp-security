# Microsoft Graph Security Integration

## Overview

This integration allows you to connect to the Microsoft Graph Security API to manage security alerts and incidents, kill user sessions, and test connectivity. It utilizes application permissions.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings, specifically requiring **application permissions**.

## Actions

### List Incidents

List security incidents from Microsoft Graph based on provided criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter incidents.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equals, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of incidents matching the criteria.

### Kill User Session

The action invalidates all the refresh tokens issued to applications for a user, by resetting the signInSessionsValidFromDateTime user property to the current date-time.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_principal_name_id` (string, required): The user's username used during sign in or the user Unique ID provided by Azure AD.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Update Alert

Update an editable alert property in Microsoft Graph Security.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to update.
*   `assigned_to` (string, optional): Name of the analyst the alert is assigned to.
*   `closed_date_time` (string, optional): Time at which the alert was closed (ISO 8601 format, UTC). E.g., '2014-01-01T00:00:00Z'.
*   `comments` (string, optional): Analyst comments on the alert (comma-separated). Allowed values: "Closed in IPC", "Closed in MCAS".
*   `feedback` (string, optional): Analyst feedback (unknown, truePositive, falsePositive, benignPositive).
*   `status` (string, optional): Alert lifecycle status (unknown, newAlert, inProgress, resolved).
*   `tags` (string, optional): User-definable labels (comma-separated).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### Get Alert

Retrieve the properties and relationships of an alert by ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to retrieve.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified alert.

### List Alerts

Get all alerts based on specified filters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter alerts.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equals, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of alerts matching the criteria.

### Ping

Test Connectivity to Microsoft Graph Security.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Add Alert Comment

Add a comment to the alert in Microsoft Graph.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert that needs to be updated.
*   `comment` (string, required): Specify the comment for the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Administrator Consent

Run the action and browse to the received URL TO grant the permissions your app needs at the Azure portal.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `redirect_url` (string, required): Use the redirect url you registered to request an authorization.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the administrator consent URL.

### Get Incident

Get details of a security incident by an incident ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the ID of the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified incident.

## Notes

*   Ensure the Microsoft Graph Security integration is properly configured in the SOAR Marketplace tab with **application permissions** and necessary credentials.
*   This integration uses application permissions, suitable for automated workflows without direct user interaction.
*   The `Get Administrator Consent` action is typically used during initial setup to grant the required application permissions.
