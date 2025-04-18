# AppSheet SOAR Integration

This document details the tools provided by the AppSheet SOAR integration.

## Tools

### `app_sheet_update_record`

Update a record in a table in AppSheet.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the name of the table in which you want to update a record.
*   `record_json_object` (Union[str, dict], required): Specify the JSON object of the record that needs to be updated. You need to provide the "ID" of the record and fields that you want to update.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `app_sheet_ping`

Test connectivity to the AppSheet with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `app_sheet_search_records`

Search records in a table in AppSheet.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the name of the table for which you want to retrieve details.
*   `selector_query` (Optional[str], optional, default=None): Specify the selector query, which will be used to limit results. If nothing is provided, action will return all records.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `app_sheet_delete_record`

Delete a record in a table in AppSheet.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the JSON object of the record that needs to be deleted. You only need to provide the unique identifier key of the record.
*   `record_json_object` (Union[str, dict], required): Specify the JSON object of the record that needs to be deleted. You only need to provide the "ID" of the record.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `app_sheet_list_tables`

List available tables in an app in AppSheet.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_logic` (Optional[List[Any]], optional, default=None): Specify what filter logic should be applied.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied.
*   `max_tables_to_return` (Optional[str], optional, default=None): Specify how many tables to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `app_sheet_add_record`

Add a record to a table in AppSheet.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the JSON object of the record that needs to be updated. You need to provide the unique identifier key and fields that you want to update.
*   `record_json_object` (Union[str, dict], required): Specify the JSON object of the record that needs to be added.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
