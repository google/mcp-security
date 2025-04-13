# AlienVault Anywhere SOAR Integration

This document details the tools provided by the AlienVault Anywhere SOAR integration.

## Tools

### `alien_vault_anywhere_get_alarm_details`

Retrieve details for an alarm by ID

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alarm_id` (str, required): The alarm ID. Can be obtained by running connector.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `alien_vault_anywhere_ping`

Test connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `alien_vault_anywhere_list_events`

Search for AlienVault events.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `account_name` (Optional[str], optional, default=None): The account name.
*   `event_name` (Optional[str], optional, default=None): The name of the event.
*   `source_name` (Optional[str], optional, default=None): The source name.
*   `start_time` (Optional[str], optional, default=None): Filtered results will include events that occurred after this timestamp. format: DD/MM/YYYY
*   `end_time` (Optional[str], optional, default=None): Filtered results will include events that occurred before this timestamp. format: DD/MM/YYYY
*   `suppressed` (Optional[bool], optional, default=None): Whether to filter events by the suppressed flag.
*   `events_limit` (Optional[str], optional, default=None): Maximum number of events to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
