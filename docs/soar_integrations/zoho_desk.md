# Zoho Desk Integration

This document describes the available tools for the Zoho Desk integration within the SecOps SOAR MCP Server. Zoho Desk is a customer support and helpdesk ticketing system.

## Configuration

Ensure the Zoho Desk integration is configured in the SOAR platform. This typically requires setting up an OAuth client in Zoho Desk and providing the Client ID, Client Secret, and generating a Refresh Token using the `zoho_desk_get_refresh_token` action or manually. You will also need your Zoho Desk Portal/Organization ID.

## Available Tools

### zoho_desk_create_ticket
- **Description:** Create a new ticket in Zoho Desk with specified details.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `title` (str, required): Specify the title for the ticket.
    - `description` (str, required): Specify the description of the ticket.
    - `department_name` (str, required): Specify the name of the department to create the ticket in.
    - `contact` (str, required): Specify the email of the contact for the ticket.
    - `assignee_type` (List[str], optional): Specify assignee type ("Agent" or "Team"). If selected, `assignee_name` is required. Defaults to None.
    - `assignee_name` (str, optional): Name/email of the agent or team name to assign. Required if `assignee_type` is set. Defaults to None.
    - `priority` (List[str], optional): Specify ticket priority (e.g., ["High"], ["Medium"]). Defaults to None.
    - `classification` (List[str], optional): Specify ticket classification (e.g., ["Problem"], ["Feature"]). Defaults to None.
    - `channel` (List[str], optional): Specify ticket channel (e.g., ["Email"], ["Phone"]). Defaults to None.
    - `category` (str, optional): Specify the category for the ticket. Defaults to None.
    - `sub_category` (str, optional): Specify the subcategory for the ticket. Defaults to None.
    - `due_date` (str, optional): Specify the due date (ISO 8601 format, e.g., "2022-07-06T07:05:43Z"). Defaults to None.
    - `custom_fields` (str, optional): JSON object string containing custom fields (use API names for keys). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the details of the created ticket.

### zoho_desk_get_ticket_details
- **Description:** Get detailed information, including comments, for one or more tickets from Zoho Desk by their IDs.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `ticket_i_ds` (str, required): Comma-separated list of Zoho Desk ticket IDs.
    - `create_insight` (bool, optional): If enabled, create an insight with ticket information. Defaults to None.
    - `additional_fields_to_return` (str, optional): Comma-separated list of additional fields to include (e.g., "contacts,assignee,team"). Defaults to None.
    - `fetch_comments` (bool, optional): If enabled, fetch comments associated with the tickets. Defaults to None.
    - `max_comments_to_return` (str, optional): Max comments per ticket (Default: 50, Max: 100). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the details for the requested tickets.

### zoho_desk_add_comment_to_ticket
- **Description:** Add a comment (public or private) to an existing ticket in Zoho Desk. Runs asynchronously if `wait_for_reply` is enabled.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `ticket_id` (str, required): The ID of the ticket to add a comment to.
    - `text` (str, required): The content of the comment.
    - `visibility` (List[str], optional): Specify comment visibility (e.g., ["Public"], ["Private"]). Defaults to None.
    - `type` (List[str], optional): Specify comment type (e.g., ["Comment"], ["Note"]). Defaults to None.
    - `wait_for_reply` (bool, optional): If enabled, the action waits for a reply (makes it async). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the result of the comment addition.

### zoho_desk_mark_ticket_as_spam
- **Description:** Mark a ticket as spam in Zoho Desk. Optionally, mark the associated contact as a spammer.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `ticket_id` (str, required): The ID of the ticket to mark as spam.
    - `mark_contact` (bool, optional): If enabled, mark the ticket's contact as a spammer. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the result of the operation.

### zoho_desk_get_refresh_token
- **Description:** Helper action to obtain a Zoho Desk refresh token using an authorization code generated from the Zoho developer console via the authorization link. This token is needed for the integration configuration.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `authorization_link` (str, required): The authorization link generated for the integration setup.
    - `authorization_code` (str, required): The authorization code obtained after authorizing via the link.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the obtained refresh token.

### zoho_desk_ping
- **Description:** Test connectivity to Zoho Desk using the configured credentials.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### zoho_desk_update_ticket
- **Description:** Update various fields of an existing ticket in Zoho Desk.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `ticket_id` (str, required): The ID of the ticket to update.
    - `title` (str, optional): New title for the ticket. Defaults to None.
    - `description` (str, optional): New description for the ticket. Defaults to None.
    - `department_name` (str, optional): New department name. Defaults to None.
    - `contact` (str, optional): New contact email. Defaults to None.
    - `assignee_type` (List[str], optional): New assignee type ("Agent" or "Team"). Requires `assignee_name`. Defaults to None.
    - `assignee_name` (str, optional): New assignee name/email or team name. Defaults to None.
    - `resolution` (str, optional): Resolution text for the ticket. Defaults to None.
    - `priority` (List[str], optional): New priority. Defaults to None.
    - `status` (List[str], optional): New status (e.g., ["Open"], ["Closed"]). Defaults to None.
    - `mark_state` (List[str], optional): New mark state (e.g., ["Spam"]). Defaults to None.
    - `classification` (List[str], optional): New classification. Defaults to None.
    - `channel` (List[str], optional): New channel. Defaults to None.
    - `category` (str, optional): New category. Defaults to None.
    - `sub_category` (str, optional): New subcategory. Defaults to None.
    - `due_date` (str, optional): New due date (ISO 8601 format). Not applicable if status is "On Hold". Defaults to None.
    - `custom_fields` (str, optional): JSON object string for updating custom fields (use API names). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities. Defaults to empty list.
    - `scope` (str, optional): Defines the scope ("All entities"). Defaults to "All entities".
- **Returns:** (dict) A dictionary containing the result of the update operation.
