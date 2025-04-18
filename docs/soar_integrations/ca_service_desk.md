# CA Service Desk Integration

## Overview

This integration allows you to connect to CA Service Desk Manager to create, update, search, and manage tickets (incidents). Actions include creating tickets, changing status, adding comments, assigning tickets, syncing history, and waiting for status changes.

## Configuration

To configure this integration within the SOAR platform, you typically need the following CA Service Desk details:

*   **Server URL:** The base URL for your CA Service Desk Manager instance (e.g., `http://casd-server/CASDM/caisd/pdmweb.exe`).
*   **Username:** The username for the integration account with appropriate permissions.
*   **Password:** The password for the integration account.
*   **Repository Name:** The name of the CA Service Desk repository to interact with (e.g., `Service Desk`).

*(Note: The exact parameter names and required details might vary depending on the specific SOAR platform configuration interface and your CA Service Desk setup.)*

## Actions

### Create Ticket

Create new ticket in CA ServiceDesk.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `summary` (string, required): Incident's summary text.
*   `description` (string, required): Incident's description text.
*   `category_name` (string, required): Incident's area name. e.g. Software.
*   `group_name` (string, required): Group name. e.g. Test.
*   `username` (string, required): User name.
*   `custom_fields` (string, optional): Specify a JSON object containing additional fields and values. Structure: `{"field":"value"}`. Overwrites other parameters if the same field is provided.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the new ticket ID.

### Wait For Status Change

Waiting until ticket status is changed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Target ticket ID.
*   `expected_ticket_status_name` (string, required): Expected status.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary indicating if the status changed to the expected value within the timeout.

### Sync Ticket History

Fetch and attach the entire ticket history to an alert.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `comment_type_field` (string, optional): Ticket type field name (e.g., `type.sym`).
*   `analyst_name_field` (string, optional): Analyst Name field name (e.g., `analyst.combo_name`).
*   `time_stamp_field` (string, optional): Time field name (e.g., `time_stamap`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the fetched history.

### Change Ticket Status

Change CA Desk Manager ticket status.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Incident number.
*   `status` (string, required): Incident status to change to (e.g., Closed).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the status change operation.

### Ping

Test Connectivity to CA Service Desk.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Add Comment

Add comment to a CA ServiceDesk incident.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Incident's ref num (e.g., 338).
*   `comment` (string, required): Comment to add to an incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Close Ticket

Close incident in CA ServiceDesk manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Incident number.
*   `close_reason` (string, required): Description which can be used in the Close activity log.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the close operation.

### Assign To Group

Assign an incident to a particular group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Incident number.
*   `group` (string, required): Group to assign the incident to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the assignment operation.

### Search Tickets

Search tickets in CA Desk Manager by field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, optional): Incident ID to filter by.
*   `summary` (string, optional): Summary content to filter by.
*   `description` (string, optional): Description content to filter by.
*   `status` (string, optional): Filter by status (e.g., Open).
*   `days_backwards` (string, optional): Get results from 'x' days backwards (e.g., 5).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of tickets matching the search criteria.

### Assign Incident To User

Assign an incident to a specific user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Incident number.
*   `username` (string, required): Username to assign the incident to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the assignment operation.

## Notes

*   Ensure the CA Service Desk integration is properly configured in the SOAR Marketplace tab with the correct Server URL, Repository Name, and credentials.
*   The integration user needs appropriate permissions within CA Service Desk to perform the desired actions (e.g., create, update, close tickets).
*   The `Wait For Status Change` action is asynchronous and depends on the SOAR platform's timeout settings.
*   The `Custom Fields` parameter in `Create Ticket` allows setting values for fields not explicitly listed as parameters, but it overwrites other provided parameters if there are overlaps.
