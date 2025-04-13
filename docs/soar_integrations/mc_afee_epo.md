# McAfee ePolicy Orchestrator (ePO) Integration

## Overview

This integration allows you to connect to McAfee ePolicy Orchestrator (ePO) to manage endpoints, execute queries, run tasks, and retrieve information about agents, events, and system status.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get Endpoint Events

Return endpoint events related to the endpoints in McAfee ePO. Supported entities: Hostname, IP and Mac Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is specified action will return all available fields.
*   `sort_field` (string, optional): Specify what field should be used for ordering of the results.
*   `sort_order` (List[Any], optional): Specify what sort order should be applied to the query.
*   `time_frame` (List[Any], optional): Specify a time frame for the events. If “Custom” is selected, you also need to provide “Start Time”.
*   `start_time` (string, optional): Specify the start time for the events. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601
*   `end_time` (string, optional): Specify the end time for the events. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time.
*   `max_events_to_return` (string, optional): Specify how many events to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including endpoint events.

### List Tasks

List available tasks in McAfee ePO.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_value` (string, optional): Specify what value should be used in the search.
*   `max_tasks_to_return` (string, optional): Specify how many tasks to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, listing available tasks.

### Get Dat Version

Retrieve DAT information from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including DAT version information.

### Run Full Scan

Run full scan on the provided endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_name` (string, required): Specify what task should be executed in order to get a full scan.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Virus Engine Agent Version

Retrieve Virus Engine agent version information from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the virus engine agent version.

### Execute Query By ID

Execute a query in McAfee ePO using query id.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query_id` (string, required): Specify the id of the query that needs to be executed.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the query execution.

### Get Last Communication Time

Retrieve information about the last communication time from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the last communication time.

### Get Agent Information

Retrieve information about endpoint's agents from McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including agent details.

### Get McAfee Epo Agent Version

Retrieve information about agent version from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the agent version.

### Ping

Test connectivity to the McAfee ePO with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Host Network IPS Status

Retrieve Network IPS information from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including Network IPS status.

### List Queries

List available queries in McAfee ePO.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied.
*   `filter_value` (string, optional): Specify what value should be used in the filter.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, listing available queries.

### Update Mcafee Agent

Update McAfee Agent on the provided endpoints in McAfee ePO. Task for Windows: DAT_Update_Windows_CWS. Task for Linux: DAT_Update_Linux_CWS. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_name` (string, required): Specify what task should be executed in order to update the McAfee Agent. Default for Windows is DAT_Update_Windows_CWS. For Linux it’s DAT_Update_Linux_CWS
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Compare Server and Agent DAT

Retrieve server and agent DAT information from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, comparing server and agent DAT versions.

### Get Host IPS Status

Retrieve IPS information from the endpoints in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including Host IPS status.

### Get System Information

Return system information about the endpoints from McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (bool, optional): If enabled, action will create an insight containing information about the endpoint.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including system information.

### Execute Entity Query

Execute an entity query in McAfee ePO. Note: this action prepares the "Where" clause based on the entities. Check documentation for additional information. Supported entities: IP, Host, User, Hash, URL.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `table_name` (string, required): Specify the name of the table from which you want to fetch results.
*   `stop_if_not_enough_entities` (bool, required): If enabled, action will not start execution, unless all of the entity types are available for the specified ".. Entity Keys". Example: if "IP Entity Key" and "File Hash Entity Key" are specified, but in the scope there are no file hashes then if this parameter is enabled, action will not execute the query.
*   `cross_entity_operator` (List[Any], required): Specify what should be the logical operator used between different entity types.
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is specified action will return all available fields.
*   `sort_field` (string, optional): Specify what field should be used for ordering of the results.
*   `sort_order` (List[Any], optional): Specify what sort order should be applied to the query.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If “Custom” is selected, you also need to provide “Start Time”.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `ip_entity_key` (string, optional): Specify what key should be used with IP entities. Please refer to the action documentation for details.
*   `hostname_entity_key` (string, optional): Specify what key should be used with Hostname entities. Please refer to the action documentation for details.
*   `file_hash_entity_key` (string, optional): Specify what key should be used with File Hash entities. Please refer to the action documentation for details.
*   `user_entity_key` (string, optional): Specify what key should be used with User entities. Please refer to the action documentation for details.
*   `url_entity_key` (string, optional): Specify what key should be used with URL entities. Please refer to the action documentation for details.
*   `email_address_entity_key` (string, optional): Specify what key should be used with Email Address (User entity with email regex) entities. Please refer to the action documentation for details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the query execution.

### Execute Custom Query

Execute a custom query in McAfee ePO.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `table_name` (string, required): Specify the name of the table from which you want to fetch results.
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is specified action will return all available fields.
*   `where_clause` (string, optional): Specify the where clause for the query. For more information please refer to the documentation portal.
*   `sort_field` (string, optional): Specify what field should be used for ordering of the results.
*   `sort_order` (List[Any], optional): Specify what sort order should be applied to the query.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the custom query execution.

### Add Tag

Add a tag to an endpoint in McAfee ePO. Note: you can only apply tags that exist in the system. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tag_name` (string, required): Specify the name of the tag that needs to be added to the endpoints.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Events For Hash

Retrieve information about events related to hashes. Note: only MD5 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fetch_events_from_ep_extended_event_table` (bool, required): If enabled, action also will use “EPExtendedEvent“ Table to find information about hashes.
*   `mark_as_suspicious` (bool, optional): If enabled, action will mark all of the hashes for which events were found as suspicious.
*   `create_insight` (bool, optional): If enabled, action will create an insight containing information about which hashes have events associated with them.
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is specified action will return all available fields.
*   `sort_field` (string, optional): Specify what field should be used for ordering of the results.
*   `sort_order` (List[Any], optional): Specify what sort order should be applied to the query.
*   `time_frame` (List[Any], optional): Specify a time frame for the events. If “Custom” is selected, you also need to provide “Start Time”.
*   `start_time` (string, optional): Specify the start time for the events. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601
*   `end_time` (string, optional): Specify the end time for the events. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time.
*   `max_events_to_return` (string, optional): Specify how many events to return per table that is queried. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hash entities are used.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including events related to the specified hashes.

### Remove Tag

Remove a tag from an endpoint in McAfee ePO. Supported entities: Hostname, IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tag_name` (string, required): Specify the name of the tag that needs to be removed from the endpoints.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the McAfee ePO integration is properly configured in the SOAR Marketplace tab.
*   Many actions support specific entity types (Hostname, IP, Mac Address, Hash, User, URL). Refer to individual action descriptions for details.
*   The `Get Events For Hash` action currently only supports MD5 hashes.
