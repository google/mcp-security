# Arcsight SOAR Integration

This document details the tools provided by the Arcsight SOAR integration.

## Tools

### `arcsight_search`

Search for available resources in ArcSight

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `search_query` (str, required): Specify the search query.
*   `max_items_to_return` (Optional[str], optional, default=None): Specify how many items to return in the response.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_get_report`

Get details about report in ArcSight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `report_full_path_uri` (str, required): Specify the URI to the report. Example: /All Reports/ArcSight Foundation/MITRE ATT&CK/Mitre ATT&CK Summary
*   `field_2` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_3` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_4` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_5` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_6` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_7` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_8` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_9` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `field_10` (Optional[str], optional, default=None): The dynamic fields for the query to generate the report
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_add_entities_to_active_list`

Add entities to the active list in ArcSight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `active_list_name` (str, required): Specify the name of the active list to which you want to add entities.
*   `entity_column` (str, required): Specify the name of the column, where entity value should be put.
*   `additional_fields` (Optional[str], optional, default=None): Specify additional fields that should be added alongside the entity in the active list. Format is a JSON object. Example: {"Column_1": "Value_1","Column_2": "Value_2"}
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_get_activelist_entries`

Retrieve active list entries in ArcSight

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `active_list_uuid` (Optional[str], optional, default=None): Specify the UUID of the active list for which you want to retrieve entries. Note: parameter “Active list UUID“ takes priority over “Active list name“. Example: HLZRc9yYBABC-lHtlf3-f0Q==
*   `active_list_name` (Optional[str], optional, default=None): Specify the name of the active list for which you want to retrieve entries. Note: parameter “Active list UUID“ takes priority over “Active list name“.
*   `map_columns` (Optional[bool], optional, default=None): If enabled, action will map columns to the values in the JSON result.
*   `max_entries_to_return` (Optional[str], optional, default=None): Specify how many entries to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_change_case_stage`

Update the stage of the case in ArcSight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `case_name` (str, required): Specify the name of the case for which you want to update the stage.
*   `stage` (str, required): Specify a new stage for the case. Possible values: INITIAL, QUEUED, CLOSED, FINAL, and FOLLOW_UP.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_get_query_results`

Get results for the provided query in ArcSight

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query_id` (Optional[str], optional, default=None): Specify the ID of the query for which you want to return results. Note: parameter “Query ID“ takes priority over “Query Name“. Example: cyUJKRz4BABCFwS9iFPq+aA==
*   `max_items_to_return` (Optional[str], optional, default=None): Specify how many items to return in the response.
*   `query_name` (Optional[str], optional, default=None): Specify the name of the query for which you want to return results. Note: parameter “Query ID“ takes priority over “Query Name“.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_list_resources`

List available queries in ArcSight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `return_active_lists` (Optional[bool], optional, default=None): If enabled, action will return available active lists.
*   `return_queries` (Optional[bool], optional, default=None): If enabled, action will return available queries
*   `return_cases` (Optional[bool], optional, default=None): If enabled, action will return available cases.
*   `return_reports` (Optional[bool], optional, default=None): If enabled, action will return available reports.
*   `max_resources_to_return` (Optional[str], optional, default=None): Specify how many resources to return per type.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_add_entries_to_activelist`

Add new entry to active list in ArcSight. Column values are separated by delimiter ‘|' and entries are separated by ‘;’ in parameter ‘Entries’. Column names are separated by delimiter ‘;’ in parameter ‘Columns’. You can also use Entries JSON instead of ‘Columns’ + 'Entries’“.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `columns` (Optional[str], optional, default=None): Specify the name of the columns, where you want to put values for the entries. Format: Column_name1;Column_name2
*   `entries` (Optional[str], optional, default=None): Specify the entries. Format entry1_value1|entry1_value2;entry2_value1|entry2_value2
*   `active_list_uuid` (Optional[str], optional, default=None): Specify the UUID of the active list, where you want to add new entries. Note: parameter “Active list UUID“ takes priority over “Active list name“. Example: HLZRc9yYBABC-lHtlf3-f0Q==
*   `active_list_name` (Optional[str], optional, default=None): Specify the name of the active list, where you want to add new entries. Note: parameter “Active list UUID“ takes priority over “Active list name“.
*   `entries_json` (Optional[Union[str, dict]], optional, default=None): Specify a list of JSON objects that contain information about the entry. Note: Combination of ‘Columns' and ‘Entries’ parameters have priority over 'Entries JSON’. Format: [{"Column_1": "Value_1", "Column_2": "Value_2"}, {"Column_1": "Value_3", "Column_2": "Value_4"}]
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arcsight_is_value_in_activelist_column`

Action checks, if entities were found in ArcSight Activelist

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `column_name` (str, required): Specify the name of the column, where you want to search for the entity.
*   `active_list_uuid` (Optional[str], optional, default=None): Specify the UUID of the active list, where you want to search for entities. Note: parameter “Active list UUID“ takes priority over “Active list name“. Example: HLZRc9yYBABC-lHtlf3-f0Q==
*   `active_list_name` (Optional[str], optional, default=None): Specify the name of the active list, where you want to search for entities. Note: parameter “Active list UUID“ takes priority over “Active list name“.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
