# Freshworks Freshservice

## Overview

This integration provides tools to interact with Freshworks Freshservice for managing tickets, agents, requesters, and related data.

## Available Tools

### List Tickets

**Tool Name:** `freshworks_freshservice_list_tickets`

**Description:** List Freshservice tickets based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_type` (List[Any], optional): Specify ticket type to return. Defaults to None.
*   `requester` (string, optional): Specify the requester email of tickets to return. Defaults to None.
*   `include_stats` (boolean, optional): If enabled, action will return additional stats on the tickets. Defaults to None.
*   `search_for_last_x_hours` (string, optional): Specify the timeframe to search tickets for. Defaults to None.
*   `rows_per_page` (string, optional): Specify how many tickets should be returned per page for Freshservice pagination. Defaults to None.
*   `start_at_page` (string, optional): Specify starting from which page tickets should be returned with Freshservice pagination. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many tickets action should return in total. Defaults to None.
*   `workspace_id` (string, optional): Specify the ID of the workspace that should be used to list tickets. If nothing is provided, the action will list tickets only from the primary workspace. To list tickets from all workspaces provide “0” in the parameter. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Requesters

**Tool Name:** `freshworks_freshservice_list_requesters`

**Description:** List requesters registered in Freshservice based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `requester_email` (string, optional): Specify the email address to return requester records for. Defaults to None.
*   `rows_per_page` (string, optional): Specify how many requester records should be returned per page for Freshservice pagination. Defaults to None.
*   `start_at_page` (string, optional): Specify starting from which page requester records should be returned with Freshservice pagination. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many requester records action should return in total. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Ticket

**Tool Name:** `freshworks_freshservice_create_ticket`

**Description:** Create a Freshservice ticket. Note: as of now, Freshservice API supports only creation of tickets with the type "Incident" and the ticket's priority is dynamically calculated according to the "Urgency" and "Impact" values, same as in FreshService's UI. Additionally, if file attachments to add are provided, the total size of the attachments must not exceed 15MB.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subject` (string, required): Specify subject field for created ticket.
*   `description` (string, required): Specify description field for created ticket.
*   `requester_email` (string, required): Specify requester email for created ticket.
*   `priority` (List[Any], required): Specify priority to assign to the ticket.
*   `agent_assign_to` (string, optional): Specify the agent email to assign the ticket to. Defaults to None.
*   `group_assign_to` (string, optional): Specify the group name to assign the ticket to. Defaults to None.
*   `urgency` (List[Any], optional): Specify urgency to assign to the ticket. Defaults to None.
*   `impact` (List[Any], optional): Specify impact to assign to the ticket. Defaults to None.
*   `tags` (string, optional): Specify tags to assign to the ticket. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the ticket. Action appends new custom fields to any existing for a ticket. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `file_attachments_to_add` (string, optional): Specify the full path for the file to be uploaded with the ticket. Parameter accepts multiple values as a comma separated string. The total size of the attachments must not exceed 15MB. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add a Ticket Reply

**Tool Name:** `freshworks_freshservice_add_a_ticket_reply`

**Description:** Add a reply to a Freshservice ticket. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to return conversations for.
*   `reply_text` (string, required): Specify reply text to add to ticket.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Deactivate Agent

**Tool Name:** `freshworks_freshservice_deactivate_agent`

**Description:** Deactivate Freshservice agent. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `agent_id` (string, required): Specify agent id to deactivate.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Ticket Time Entry

**Tool Name:** `freshworks_freshservice_delete_ticket_time_entry`

**Description:** Delete a time entry for a Freshservice ticket. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to delete a time entry for.
*   `time_entry_id` (string, required): Specify time entry ID to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Agent

**Tool Name:** `freshworks_freshservice_create_agent`

**Description:** Create a new Freshservice Agent. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email` (string, required): Specify the email of the agent to create.
*   `first_name` (string, required): Specify the first name of the agent to create.
*   `roles` (string, required): Specify roles to add to agent. Parameter accepts multiple values as a comma separated string. Example: {'role_id':17000023338,'assignment_scope': 'entire_helpdesk'}.
*   `last_name` (string, optional): Specify the last name of the agent to create. Defaults to None.
*   `is_occasional` (boolean, optional): If enabled, agent will be created as an occasional agent, otherwise full-time agent will be created. Defaults to None.
*   `can_see_all_tickets_from_associated_departments` (boolean, optional): If enabled, agent will be able to see all tickets from Associated departments. Defaults to None.
*   `departments` (string, optional): Specify department names associated with the agent. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `location` (string, optional): Specify location name associated with the agent. Defaults to None.
*   `group_memberships` (string, optional): Specify group names agent should be a member of. Defaults to None.
*   `job_title` (string, optional): Specify agent job title. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the agent. Action appends new custom fields to any existing for an agent. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Agents

**Tool Name:** `freshworks_freshservice_list_agents`

**Description:** List Freshservice agents based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `agent_email` (string, optional): Specify the email address to return agent records for. Defaults to None.
*   `agent_state` (List[Any], optional): Specify agent states to return. Defaults to None.
*   `include_not_active_agents` (boolean, optional): If enabled, results will include not active agent records. Defaults to None.
*   `rows_per_page` (string, optional): Specify how many agent records should be returned per page for Freshservice pagination. Defaults to None.
*   `start_at_page` (string, optional): Specify starting from which page agent records should be returned with Freshservice pagination. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many agent records action should return in total. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Ticket Time Entries

**Tool Name:** `freshworks_freshservice_list_ticket_time_entries`

**Description:** List Freshservice tickets time entries based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to return time entries for.
*   `agent_email` (string, required): Specify agent email to list ticket time entries for.
*   `rows_per_page` (string, optional): Specify how many ticket time entries should be returned per page for Freshservice pagination. Defaults to None.
*   `start_at_page` (string, optional): Specify starting from which page ticket time entries should be returned with Freshservice pagination. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many ticket time entries action should return in total. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Ticket Time Entry

**Tool Name:** `freshworks_freshservice_add_ticket_time_entry`

**Description:** Add a time entry to a Freshservice ticket. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to add a time entry for.
*   `agent_email` (string, required): Specify agent email for whom to add a ticket time entry.
*   `time_spent` (string, required): Specify time spent for ticket time entry. Format: {hh:mm}.
*   `note` (string, optional): Specify a note to add to the ticket time entry. Defaults to None.
*   `billable` (boolean, optional): If enabled, ticket time entry will be marked as billable. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the ticket time entry. Action appends new custom fields to any existing for ticket time entry. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Ticket Conversations

**Tool Name:** `freshworks_freshservice_list_ticket_conversations`

**Description:** List Freshservice ticket conversations based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to return conversations for.
*   `rows_per_page` (string, optional): Specify how many ticket conversations should be returned per page for Freshservice pagination. Defaults to None.
*   `start_at_page` (string, optional): Specify starting from which page ticket conversations should be returned with Freshservice pagination. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many ticket conversations action should return in total. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Ticket Time Entry

**Tool Name:** `freshworks_freshservice_update_ticket_time_entry`

**Description:** Update a time entry for a Freshservice ticket. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to update a time entry for.
*   `time_entry_id` (string, required): Specify time entry ID to update.
*   `agent_email` (string, optional): Specify agent email for whom to change a ticket time entry. Defaults to None.
*   `note` (string, optional): Specify a note for the ticket time entry. Defaults to None.
*   `time_spent` (string, optional): Specify time spent for ticket time entry. Format: {hh:mm}. Defaults to None.
*   `billable` (boolean, optional): If enabled, ticket time entry will be marked as billable. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the ticket time entry. Action appends new custom fields to any existing for ticket time entry. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Agent

**Tool Name:** `freshworks_freshservice_update_agent`

**Description:** Update existing Freshservice Agent. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `agent_id` (string, required): Specify agent id to update.
*   `email` (string, optional): Specify the email of the agent to update. Defaults to None.
*   `first_name` (string, optional): Specify the first name of the agent to update. Defaults to None.
*   `last_name` (string, optional): Specify the last name of the agent to update. Defaults to None.
*   `is_occasional` (boolean, optional): If enabled, agent will be updated as an occasional agent, otherwise it will be a full-time agent. Defaults to None.
*   `can_see_all_tickets_from_associated_departments` (boolean, optional): If enabled, agent will be able to see all tickets from Associated departments. Defaults to None.
*   `departments` (string, optional): Specify department names associated with the agent. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `location` (string, optional): Specify location name associated with the agent. Defaults to None.
*   `group_memberships` (string, optional): Specify group names agent should be a member of. Defaults to None.
*   `roles` (string, optional): Specify roles to add to agent. Parameter accepts multiple values as a comma separated string. Example: {'role_id':170000XXXXX,'assignment_scope': 'entire_helpdesk'}. Defaults to None.
*   `job_title` (string, optional): Specify agent job title. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the agent. Action appends new custom fields to any existing for an agent. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `freshworks_freshservice_ping`

**Description:** Test connectivity to the Freshservice instance with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Requester

**Tool Name:** `freshworks_freshservice_create_requester`

**Description:** Create a new Freshservice requester. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email` (string, required): Specify the email of the requester to create.
*   `first_name` (string, required): Specify the first name of the requester to create.
*   `last_name` (string, optional): Specify the last name of the requester to create. Defaults to None.
*   `can_see_all_tickets_from_associated_departments` (boolean, optional): If enabled, requester will be able to see all tickets from associated departments. Defaults to None.
*   `departments` (string, optional): Specify department names associated with the requester. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `location` (string, optional): Specify location name associated with the requester. Defaults to None.
*   `job_title` (string, optional): Specify requester job title. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the requester. Action appends new custom fields to any existing for requester. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Deactivate Requester

**Tool Name:** `freshworks_freshservice_deactivate_requester`

**Description:** Deactivate Freshservice requester. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `requester_id` (string, required): Specify requester id to deactivate.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Ticket

**Tool Name:** `freshworks_freshservice_update_ticket`

**Description:** Update a Freshservice ticket based on provided action input parameters. Note that if new tags for the ticket are provided, due to the Freshservice API limitations action replaces existing tags in the ticket, not appending new ones to existing. Additionally, if file attachments to add are provided, the total size of the attachments must not exceed 15MB.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket id to update.
*   `status` (List[Any], optional): Specify new status for the ticket. Defaults to None.
*   `subject` (string, optional): Specify subject field to update. Defaults to None.
*   `description` (string, optional): Specify description field to update. Defaults to None.
*   `requester_email` (string, optional): Specify requester email to update. Defaults to None.
*   `agent_assign_to` (string, optional): Specify the agent email to update. Defaults to None.
*   `group_assign_to` (string, optional): Specify the group name to update. Defaults to None.
*   `priority` (List[Any], optional): Specify priority to update. Defaults to None.
*   `urgency` (List[Any], optional): Specify urgency to update. Defaults to None.
*   `impact` (List[Any], optional): Specify impact to update. Defaults to None.
*   `tags` (string, optional): Specify tags to replace in the ticket. Parameter accepts multiple values as a comma separated string. Note that due to the Freshservice API limitations action replaces existing tags in the ticket, not appending new ones to existing. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the ticket. Action appends new custom fields to any existing for a ticket. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `file_attachments_to_add` (string, optional): Specify the full path for the file to be uploaded with the ticket. Parameter accepts multiple values as a comma separated string. The total size of the attachments must not exceed 15MB. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Requester

**Tool Name:** `freshworks_freshservice_update_requester`

**Description:** Update existing Freshservice Requester. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `requester_id` (string, required): Specify requester id to update.
*   `email` (string, optional): Specify the email of the requester to update. Defaults to None.
*   `first_name` (string, optional): Specify the first name of the requester to update. Defaults to None.
*   `last_name` (string, optional): Specify the last name of the requester to update. Defaults to None.
*   `can_see_all_tickets_from_associated_departments` (boolean, optional): If enabled, requester will be able to see all tickets from associated departments. Defaults to None.
*   `departments` (string, optional): Specify department names associated with the requester. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `location` (string, optional): Specify location name associated with the requester. Defaults to None.
*   `job_title` (string, optional): Specify requester job title. Defaults to None.
*   `custom_fields` (string, optional): Specify a JSON object that contains custom fields to add to the requester. Action appends new custom fields to any existing for requester. Example format: {"key1":"value1","key2":"value2"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add a Ticket Note

**Tool Name:** `freshworks_freshservice_add_a_ticket_note`

**Description:** Add a note to a Freshservice ticket. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ticket_id` (string, required): Specify ticket ID to return conversations for.
*   `note_text` (string, required): Specify note text to add to ticket.
*   `note_type` (List[Any], optional): Specify the type of note action should add to the ticket. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
