# McAfee Enterprise Security Manager (ESM) Integration

## Overview

This integration allows you to connect to McAfee Enterprise Security Manager (ESM) to send queries, manage watchlists, retrieve similar events, and test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Send Advanced Query To ESM

Send an advanced query to ESM using a JSON payload. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed. Please refer to the documentation portal for more information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query_payload` (string, required): Specify the JSON object that would need to be executed. Note: action will at max return only 200 results.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Values To Watchlist

Add values to a watchlist in McAfee ESM. Note: McAfee ESM will allow values of the invalid type to be passed, for example, API will not raise error adding hash to the IP watchlist. Please pay attention to the input.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_name` (string, required): Specify the name of the watchlist that needs to be updated.
*   `values_to_add` (string, required): Specify a comma-separated list of values that need to be added to a watchlist.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Query To ESM

Send a query to ESM with specified filters and time range. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_range` (List[Any], required): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time".
*   `filter_field_name` (string, required): Specify the field name that will be used for filtering.
*   `filter_operator` (List[Any], required): Specify the operator that should be used in the filter.
*   `filter_values` (string, required): Specify a comma-separated list of values that will be used in the filter.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time.
*   `fields_to_fetch` (string, optional): Specify a comma-separated list of fields that should be returned. If nothing is provided, action will use the predefined fields.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting. Note: this parameter expects the field in the format {table}.{key name}. If the parameter is provided in another format, action will skip it. Example: Alert.LastTime.
*   `sort_order` (List[Any], optional): Specify the order of sorting.
*   `query_type` (List[Any], optional): Specify what needs to be queried.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50. Maximum: 200.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the query execution.

### Remove Values From Watchlist

Remove values from a watchlist in McAfee ESM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_name` (string, required): Specify the name of the watchlist that needs to be updated.
*   `values_to_remove` (string, required): Specify a comma-separated list of values that need to be removed from a watchlist.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Entity Query To ESM

Send a query to ESM based on entities. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ip_address_entity_key` (string, required): Specify the key that will be used with the IP Address entity during filtering. Note: if invalid key is provided, the action will still return results, but they will be unexpected.
*   `hostname_entity_key` (string, required): Specify the key that will be used with the Hostname entity during filtering. Note: if invalid key is provided, the action will still return results, but they will be unexpected.
*   `time_range` (List[Any], required): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time".
*   `filter_field_name` (string, required): Specify the field name that will be used for filtering.
*   `filter_operator` (List[Any], required): Specify the operator that should be used in the filter.
*   `filter_values` (string, required): Specify a comma-separated list of values that will be used in the filter.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time.
*   `fields_to_fetch` (string, optional): Specify a comma-separated list of fields that should be returned. If nothing is provided, action will use the predefined fields.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting. Note: this parameter expects the field in the format {table}.{key name}. If the parameter is provided in another format, action will skip it. Example: Alert.LastTime.
*   `sort_order` (List[Any], optional): Specify the order of sorting.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50. Maximum: 200.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the entity query execution.

### Ping

Test connectivity to McAfee ESM with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Similar Events

Get events related to the entities in McAfee ESM. Supported entities: Hostname, IP Address, User. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hours_back` (string, required): Specify how many hours backwards to search.
*   `ips_id` (string, optional): Specify the IP SID for the search.
*   `result_limit` (string, optional): Specify how many results to return. Max: 200 per entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including similar events.

## Notes

*   Ensure the McAfee ESM integration is properly configured in the SOAR Marketplace tab.
*   Several actions (`Send Advanced Query To ESM`, `Send Query To ESM`, `Send Entity Query To ESM`, `Get Similar Events`) run asynchronously and may require adjusting script timeouts in the SOAR IDE.
*   Query actions have a maximum result limit (typically 200).
*   Be mindful of watchlist value types when using `Add Values To Watchlist`.
