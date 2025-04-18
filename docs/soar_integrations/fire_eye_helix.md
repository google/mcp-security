# FireEye Helix Integration

## Overview

This integration allows you to connect to FireEye Helix and perform actions such as searching logs, managing alerts, enriching entities, and managing lists.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Index Search

Performs a search against the FireEye Helix index based on a provided query and optional time frame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): The search query (e.g., `srcserver=172.30.202.130`).
*   `time_frame` (string, optional): The time frame for the search (e.g., `7h`, `1d`). Only hours (h) and days (d) are supported.
*   `max_results_to_return` (string, optional): The maximum number of search results to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Enrich User

Fetches information about users from FireEye Helix based on User entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. User entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enriched user information.

### Close Alert

Closes a specific alert in FireEye Helix.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to close.
*   `revision_note` (string, optional): An optional note explaining the reason for closing the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Enrich Endpoint

Fetches system information about an endpoint from FireEye Helix based on its hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enriched endpoint information.

### Archive Search

Performs a search against the FireEye Helix archive based on a provided query and time frame. Note the specific time frame limitations mentioned in the arguments.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): The search query (e.g., `srcserver=172.30.202.130`).
*   `time_frame` (string, required): The time frame for the search (e.g., `7h`, `1d`). Only hours (h) and days (d) are supported. Note: The effective end time is 4 hours before the current time due to API limitations.
*   `max_results_to_return` (string, optional): The maximum number of search results to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the archive search results.

### Ping

Tests connectivity to the configured FireEye Helix instance using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get List Items

Retrieves items from a specified list within FireEye Helix, with optional filtering and sorting.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `list_short_name` (string, required): The short name of the list to retrieve items from.
*   `value` (string, optional): Filters items based on their value.
*   `type` (List[Any], optional): Filters items based on their type.
*   `sort_by` (List[Any], optional): Specifies the field to sort the results by.
*   `sort_order` (List[Any], optional): Specifies the sort order (ascending/descending).
*   `max_items_to_return` (string, optional): The maximum number of list items to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list items matching the criteria.

### Get Alert Details

Retrieves detailed information about a specific alert from FireEye Helix, including associated notes.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to retrieve details for.
*   `max_notes_to_return` (string, optional): The maximum number of associated notes to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the detailed information for the specified alert.

### Suppress Alert

Suppresses a specific alert in FireEye Helix for a defined duration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to suppress.
*   `duration` (string, required): The duration (in minutes) for which to suppress the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Lists

Retrieves information about available lists in FireEye Helix, with optional filtering and sorting.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, optional): Filters lists by name.
*   `short_name` (string, optional): Filters lists by short name.
*   `active` (boolean, optional): Filters for active lists only.
*   `internal` (boolean, optional): Filters for internal lists only.
*   `protected` (boolean, optional): Filters for protected lists only.
*   `sort_by` (List[Any], optional): Specifies the field to sort the results by.
*   `sort_order` (List[Any], optional): Specifies the sort order (ascending/descending).
*   `max_lists_to_return` (string, optional): The maximum number of lists to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing information about the lists matching the criteria.

### Add Note To Alert

Adds a note or comment to a specific alert in FireEye Helix.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to add the note to.
*   `note` (string, required): The content of the note to add.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Entities To a List

Adds SOAR entities (e.g., IPs, domains, hashes) to a specified list in FireEye Helix.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `list_short_name` (string, required): The short name of the list to add entities to.
*   `risk` (List[Any], optional): Specifies the risk level to associate with the added items.
*   `note` (string, optional): An optional note to add to the list items.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) whose identifiers will be added to the list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the FireEye Helix integration is properly configured in the SOAR Marketplace tab.
*   Some actions rely on underlying scripts executed by the SOAR platform.
*   Pay attention to the specific time frame limitations for `Index Search` and `Archive Search` as noted in their argument descriptions.
