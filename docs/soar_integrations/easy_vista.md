# EasyVista Integration

## Overview

This integration allows interaction with the EasyVista IT Service Management platform to manage service tickets. Actions include closing tickets, adding comments, retrieving ticket details, waiting for updates, and testing connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following EasyVista details:

*   **Server URL:** The URL of your EasyVista instance API endpoint (e.g., `https://mycompany.easyvista.com/api/`).
*   **Account ID:** Your EasyVista Account ID.
*   **Username:** The username for an API user account.
*   **Password:** The password for the API user account.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has the necessary permissions for the desired API operations on tickets and actions.)*

## Actions

### Close EasyVista Ticket

Close EasyVista ticket based on the provided parameters. Note: action is not working on Siemplify entities, ticket identifier (rfc_number) should be provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_identifier` (string, required): EasyVista ticket identifier (e.g., `S201001_000001`).
*   `comment` (string, optional): Comment explaining the closing of the ticket.
*   `actions_close_date` (string, optional): Closing date for open actions (Format: `MM/DD/YYYY HH:MM:SS`). Defaults to current time if format is incorrect.
*   `delete_ongoing_actions` (bool, optional): Specify whether to delete the ticket's ongoing actions on closing.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the close ticket operation.

### Add Comment to Ticket

Add a comment to the EasyVista ticket. Note: action is not working on Siemplify entities, action input parameters should be provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_identifier` (string, required): EasyVista ticket identifier to add comment to (e.g., `S201001_000001`).
*   `comment` (string, required): Comment to add to EasyVista ticket.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Get EasyVista Ticket

Get information on specific EasyVista ticket. Note: action is not working on Siemplify entities, ticket identifier (rfc_number) should be provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_identifier` (string, required): EasyVista ticket identifier to get info for (e.g., `S201001_000001`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified EasyVista ticket.

### Ping

Test connectivity to the EasyVista instance with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Wait for the Ticket Update

Action pauses the playbook execution and periodically connects to EasyVista until timeout and checks if the specified ticket got an update. Action also can monitor specific field for the update, once that field is updated - action completes and fetches back the updated ticket information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_identifier` (string, required): EasyVista ticket identifier (e.g., `S201001_000001`).
*   `field_to_monitor` (List[Any], optional): EasyVista ticket field to monitor for the update (e.g., `Status`, `Assignment Group`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the updated ticket information once the monitored field changes or the timeout is reached.

## Notes

*   Ensure the EasyVista integration is properly configured in the SOAR Marketplace tab with the correct Server URL, Account ID, Username, and Password.
*   The API user requires appropriate permissions within EasyVista to manage tickets and actions.
*   Ticket identifiers (`rfc_number`) are required for most actions and typically need to be obtained from EasyVista or previous action outputs.
*   The `Wait for the Ticket Update` action is asynchronous and relies on polling. Adjust playbook timeouts accordingly.
*   Pay attention to the required date format (`MM/DD/YYYY HH:MM:SS`) for the `Close EasyVista Ticket` action.
