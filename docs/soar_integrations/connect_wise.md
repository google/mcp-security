# ConnectWise Integration

## Overview

This integration allows you to connect to ConnectWise Manage to create, update, retrieve, and manage service tickets.

## Configuration

To configure this integration within the SOAR platform, you typically need the following ConnectWise Manage details:

*   **Server URL:** The URL of your ConnectWise Manage instance (e.g., `na.myconnectwise.net`, `eu.myconnectwise.net`, or your on-premise URL).
*   **Company ID:** Your ConnectWise Company ID.
*   **Public Key:** Your ConnectWise Manage API Public Key.
*   **Private Key:** Your ConnectWise Manage API Private Key.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API Member used has the necessary permissions for Service Ticket management.)*

## Actions

### Create Ticket

Create a ConnectWise ticket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `company` (string, required): Company identifier (name or ID).
*   `board` (string, required): Board name.
*   `summary` (string, required): Specify the summary for the new ticket (max 100 characters, will be truncated).
*   `status` (string, required): Status name (e.g., `Unassigned`).
*   `priority` (string, required): Priority name (e.g., `Priority 3 - Normal Response`).
*   `owner_name` (string, optional): ConnectWise member name to assign this ticket to (e.g., `connectwise_user_1`).
*   `email_note_cc` (string, optional): Comma-separated list of email addresses to receive note updates.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ticket creation, likely including the new ticket ID.

### Add Comment To Ticket

Add new comment to a ticket in ConnectWise.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): ConnectWise ticket ID (e.g., `608718`).
*   `comment` (string, required): Comment content to attach to a ticket.
*   `internal` (bool, optional): If checked, mark the comment as internal.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Get Ticket

Get ConnectWise ticket by ID and attach ticket JSON as a file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Fetch ticket by ID.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the ticket details (often attached as JSON).

### Create Alerts Ticket

Create a ConnectWise ticket for each new Siemplify alert.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `company` (string, required): Company identifier.
*   `board` (string, required): Board name.
*   `status` (string, required): Status name (e.g., `Unassigned`).
*   `priority` (string, required): Priority name (e.g., `Priority 3 - Normal Response`).
*   `initial_description` (string, required): Initial description text for the ticket (often populated with alert details).
*   `owner_name` (string, optional): ConnectWise member name to assign this ticket to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ticket creation for the alert(s).

### Ping

Test Connectivity to ConnectWise Manage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Close Ticket

Close ConnectWise ticket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): ConnectWise ticket ID (e.g., `608718`).
*   `custom_close_status` (string, optional): Specify a custom closed status name if different from the default (e.g., `Completed`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the close operation.

### Add Attachment To Ticket

Add an attachment to the ticket in ConnectWise.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filename` (string, required): Specify the filename for the attachment (including extension). This is also used as the title.
*   `base64_encoded_file` (string, required): Specify the base64 encoded file content.
*   `ticket_id` (string, required): Specify the ID of the ticket to add the attachment to.
*   `allow_only_owner_update` (bool, optional): If enabled, only allow the owner to update the attachment.
*   `display_in_customer_portal` (bool, optional): If enabled, display the attachment in the customer portal.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the attachment upload.

### Update Ticket

Update ticket details in ConnectWise.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Ticket ID to be updated (e.g., `609620`).
*   `summary` (string, optional): Specify the updated summary (max 100 characters).
*   `type_name` (string, optional): Type name (e.g., `Application`).
*   `sub_type_name` (string, optional): SubType name (e.g., `Adobe`).
*   `item_name` (string, optional): Item name (e.g., `Development`).
*   `owner_name` (string, optional): ConnectWise member name to assign the ticket to.
*   `board` (string, optional): Board name.
*   `priority` (string, optional): Priority name (e.g., `Priority 3 - Normal Response`).
*   `status` (string, optional): New ticket status (e.g., `In Progress (plan of action)`).
*   `email_note_cc` (string, optional): Comma-separated list of email addresses to receive note updates.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ticket update operation.

### Delete Ticket

Delete ConnectWise ticket by ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Ticket ID to be deleted (e.g., `607167`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

## Notes

*   Ensure the ConnectWise integration is properly configured in the SOAR Marketplace tab with the correct Server URL, Company ID, Public Key, and Private Key.
*   The API Member associated with the keys needs appropriate permissions for Service Ticket management.
*   Board names, Status names, Priority names, etc., must match the values configured in your ConnectWise Manage instance.
*   Ticket summaries are truncated at 100 characters by the API.
