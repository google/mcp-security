# Splunk SOAR Integration

## Overview

This integration provides tools for interacting with Splunk from within the Chronicle SOAR platform. It allows executing queries (including entity-based queries), retrieving host events, updating notable events (Splunk ES only), submitting events, and testing connectivity.

## Tools

### `splunk_splunk_csv_viewer`

Deprecated. This action creates a CSV table based on the raw results.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `results` (str, required): Raw results.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `splunk_get_host_events`

Get events related to hosts in Splunk.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `event_per_host_limit` (str, required): Specify how many events to return per host.
*   `results_from` (str, required): Specify the start time for the events.
*   `results_to` (str, required): Specify the end time for the events.
*   `result_fields` (Optional[str], optional, default=None): Specify a comma-separated list of fields that need to be returned.
*   `index` (Optional[str], optional, default=None): Specify what index should be used, when searching for events related to the host. If nothing is provided, action will not use index.
*   `host_key` (Optional[str], optional, default=None): Specify what key should be used to get information about host events. Default: host.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `splunk_update_notable_events`

Update notable events in Splunk ES. Note: This action is only supported for Splunk ES.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `notable_event_i_ds` (str, required): Specify IDs of notable events. Example:1A082D7B-D5A1-4A2B-BB94-41C439BE3EB7@@notable@@cb87390ae72763679d3f6f8f097ebe2b,1D234D5B-1531-2D2B-BB94-41C439BE12B7@@notable@@cb87390ae72763679d3f6f8f097ebe2b
*   `status` (Optional[List[str]], optional, default=None): Specify the new status for notable events.
*   `urgency` (Optional[List[str]], optional, default=None): Specify the new urgency for the notable event.
*   `new_owner` (Optional[str], optional, default=None): Specify the new owner of the notable event.
*   `comment` (Optional[str], optional, default=None): Specify comment for the notable event.
*   `disposition` (Optional[List[str]], optional, default=None): Specify the disposition for the notable event.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `splunk_ping`

Test connectivity to the Splunk with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `splunk_splunk_query`

Execute a query in Splunk. Note: Please exclude any quotes that are part of the query string.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query that needs to be executed. Example: index="_internal". You can provide multiple queries in the same action. The format is [“query 1”, “query 2”].
*   `search_mode` (Optional[List[str]], optional, default=None): Specify the mode for search execution.
*   `results_count_limit` (Optional[str], optional, default=None): Specify how many results to return. Note: this parameter appends the “head” key word to the provided query. Default is 100.
*   `results_from` (Optional[str], optional, default=None): Specify the start time for the query. Default: -24h
*   `results_to` (Optional[str], optional, default=None): Specify the end time for the query. Default: now.
*   `result_fields` (Optional[str], optional, default=None): Specify a comma-separated list of fields that need to be returned. Note: this parameter appends "fields" key word to the provided query.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `splunk_execute_entity_query`

Execute an entity query in Splunk. Note: this action prepares the “Where” clause based on the entities. Check documentation for additional information.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query that needs to be executed without the “Where” clause. Example: index="_internal"
*   `cross_entity_operator` (List[str], required): Specify what should be the logical operator used between different entity types.
*   `search_mode` (Optional[List[str]], optional, default=None): Specify the mode for search execution.
*   `results_count_limit` (Optional[str], optional, default=None): Specify how many results to return. Note: this parameter appends the "head" key word to the provided query. Default is 100.
*   `results_from` (Optional[str], optional, default=None): Specify the start time for the query. Default: -24h
*   `results_to` (Optional[str], optional, default=None): Specify the end time for the query. Default: now.
*   `result_fields` (Optional[str], optional, default=None): Specify a comma-separated list of fields that need to be returned. Note: this parameter appends "fields" key word to the provided query.
*   `ip_entity_key` (Optional[str], optional, default=None): Specify what key should be used with IP entities. Please refer to the action documentation for details.
*   `hostname_entity_key` (Optional[str], optional, default=None): Specify what key should be used with Hostname entities, when preparing the. Please refer to the action documentation for details.
*   `file_hash_entity_key` (Optional[str], optional, default=None): Specify what key should be used with File Hash entities. Please refer to the action documentation for details.
*   `user_entity_key` (Optional[str], optional, default=None): Specify what key should be used with User entities. Please refer to the action documentation for details.
*   `url_entity_key` (Optional[str], optional, default=None): Specify what key should be used with URL entities. Please refer to the action documentation for details.
*   `email_address_entity_key` (Optional[str], optional, default=None): Specify what key should be used with Email Address entities. Please refer to the action documentation for details.
*   `stop_if_not_enough_entities` (Optional[bool], optional, default=None): If enabled, action will not start execution, unless all of the entity types are available for the specified ".. Entity Keys". Example: if "IP Entity Key" and "File Hash Entity Key" are specified, but in the scope there are no file hashes then if this parameter is enabled, action will not execute the query.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `splunk_submit_event`

Submit event to Splunk

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `index` (str, required): Specify the index, where the event should be created.
*   `event` (str, required): Specify the raw event that needs to be submitted.
*   `host` (Optional[str], optional, default=None): Specify the host that is related to the event.
*   `source` (Optional[str], optional, default=None): Specify the source of the event. Example: www.
*   `sourcetype` (Optional[str], optional, default=None): Specify the source type of the event. Example: web_event
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
