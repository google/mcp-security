# SpyCloud SOAR Integration

## Overview

This integration provides tools for interacting with SpyCloud from within the Chronicle SOAR platform. It allows listing breaches associated with entities (IP, Username, Email, Domain), listing available breach catalogs, and testing connectivity.

## Tools

### `spy_cloud_list_entity_breaches`

Return information about breaches related to entities. Supported entity types: IP Address, Username, Email Address (Username entity that matches email regex), Domain (action will strip domain part from URL entity).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `time_frame` (List[str], required): Specify a time frame for the search. If "Custom" is selected, you also need to provide "Start Time".
*   `catalog_filter` (Optional[str], optional, default=None): Specify the name of the category in which you want to search for breaches.
*   `start_time` (Optional[str], optional, default=None): Specify the start time for the search. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Note: action will only take the datetime for action execution.
*   `end_time` (Optional[str], optional, default=None): Specify the end time for the search. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Note: action will only take the datetime for action execution.
*   `max_breaches_to_return` (Optional[str], optional, default=None): Specify how many breaches to return per entity. Default: 1. Maximum: 1000.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `spy_cloud_ping`

Test connectivity to the SpyCloud with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `spy_cloud_list_catalogs`

List available catalogs in SpyCloud.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `time_frame` (List[str], required): Specify a time frame for the search. If "Custom" is selected, you also need to provide "Start Time".
*   `filter_logic` (Optional[List[str]], optional, default=None): Specify what filter logic should be applied.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. "Equal" works with "title" parameter, while "Contains" works with all values in response. If nothing is provided in this parameter, the filter will not be applied.
*   `start_time` (Optional[str], optional, default=None): Specify the start time for the search. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601
*   `end_time` (Optional[str], optional, default=None): Specify the end time for the search. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time.
*   `max_catalogs_to_return` (Optional[str], optional, default=None): Specify how many catalogs to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
