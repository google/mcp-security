# SiemplifyUtilities SOAR Integration

## Overview

This integration provides a collection of utility tools for common tasks within the Chronicle SOAR platform, such as parsing EML files, performing list operations, joining query strings, counting items, managing files, filtering JSON data, and interacting with entities and deployment settings.

## Tools

### `siemplify_utilities_parse_eml_to_json`

Parse EML to JSON

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `eml_content` (str, required): The base64 encoded content of the EML file.
*   `blacklisted_headers` (Optional[str], optional, default=None): Headers to exclude from the response.
*   `use_blacklist_as_whitelist` (Optional[bool], optional, default=None): To only include the listed headers.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_list_operations`

Provide operations on lists.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `first_list` (Optional[str], optional, default=None): Comma separated string list. For example: value1,value2,value3.
*   `second_list` (Optional[str], optional, default=None): Comma separated string list. For example: value1,value2,value3.
*   `delimiter` (Optional[str], optional, default=None): Define a symbol, which is used for separation of values in both lists.
*   `operator` (Optional[str], optional, default=None): Has to be one of the following: intersection, union, subtract or xor.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_query_joiner`

Form query string from given parameters.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `values` (str, required): Comma separated string list. For example: value1,value2,value3.
*   `query_field` (str, required): Query target field ex. SrcIP, DestHost, etc..
*   `query_operator` (str, required): Query operator(OR, AND, etc.)
*   `add_quotes` (Optional[bool], optional, default=None): If enabled, action will add quotes to every item in the "Values" list.
*   `add_double_quotes` (Optional[bool], optional, default=None): If enabled, action will add double quotes to every item in the "Values" list.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_count_list`

Count the number of items on a list - separated by a configurable delimiter.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `input_string` (Optional[str], optional, default=None): Comma separated string list. For example: value1,value2,value3.
*   `delimiter` (Optional[str], optional, default=None): Define a symbol, which is used for separation of values from the input list.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_export_entities_as_open_ioc_file`

Export entities as OpenIOC file. Supported entities: Filehash, IP address, URL, Hostname, User.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `export_folder_path` (str, required): Specify the folder that should store the OpenIOC files.
*   `ioc_name` (Optional[str], optional, default=None): Specify the name of the IOC.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_extract_top_from_json`

The action gets Json as input, sort it by a specific key and return the TOP x of the relevant branches

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `json_data` (Union[str, dict], required): JSON data to process.
*   `key_to_sort_by` (str, required): Nested key separated by dots. Use * as a wildcard. Example: Host.*.wassap_list.Severity
*   `field_type` (str, required): The type of the field to sort by. Valid values: int (numeric field), string (a text field) or date
*   `reverse_desc_to_asc` (Optional[bool], optional, default=None): Sort results by DESC or ASC (Z -> A).
*   `top_rows` (Optional[str], optional, default=None): Retrieve number of rows from JSON to process.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_get_deployment_url`

Get the URL that leads back to the instance this action is running on.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_delete_file`

Delete file on the filesystem.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_path` (str, required): Specify the absolute file path for the file that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_filter_json`

Filter JSON dict

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `json_data` (Union[str, dict], required): The json dict data to filter.
*   `condition_path` (str, required): The path to the field to filter by, dot separated.
*   `condition_operator` (str, required): The condition operator. Can be one of the following: = / != / > / < / >= / <= / in / not in.
*   `condition_value` (str, required): The value of the condition to filter by.
*   `root_key_path` (Optional[str], optional, default=None): The path to the Root Key. Note: The system uses dot notation for JSON search. For example: json.message.status.
*   `output_path` (Optional[str], optional, default=None): The path to the desired results in the filtered dict, dot separated.
*   `delimeter` (Optional[str], optional, default=None): The delimiter to join the values in the output path. Default: comma.
*   `escape_json_data_input` (Optional[bool], optional, default=None): If enabled, the action will try to escape input inside JSON Data, if it couldn't detect a valid JSON immediately. Note: escaping operation is unstable and should be used with caution. If the parameter is disabled, action will never try to escape the JSON Data.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_utilities_count_entities_in_scope`

Count the number of entities from a specific scope.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `entity_type` (str, required): The type of the target entities.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
