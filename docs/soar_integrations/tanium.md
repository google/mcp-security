# Tanium SOAR Integration

## Overview

This document outlines the tools (actions) available within the Tanium integration for Chronicle SOAR. These tools allow interaction with Tanium for endpoint management, investigation, and response tasks.

## Tools

### `tanium_create_question`

Create a new Tanium question based on the specified parameters, and the question is immediately asked. Action returns question id that can be passed to “Get Question Results” action to get question results. Note that the action is not working with Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `question_text` (str, required): Specify the contents of Tanium question. Example: Get Operating System from all machines
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_quarantine_endpoint`

Quarantine the endpoints in Tanium. Action works with Tanium Threat Response API. Supported Entities: Hostname, IP Address. Note: Action is running as async, if "Only Initiate" is set to false, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `package_names` (str, required): Specify a JSON object containing all of the package names for each OS.
*   `only_initiate` (Optional[bool], optional, default=None): If enabled, action will only initiate the task execution without waiting for results.
*   `package_parameters` (Optional[str], optional, default="[...]"): Specify a JSON object containing all of the parameters for the package being deployed. If nothing is provided, action will use the default payload.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_get_task_details`

Retrieve details about a task in Tanium. Action works with Tanium Threat Response API. Note: Action is running as async, if "Wait For Completion" is enabled, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `task_i_ds` (str, required): Specify a comma-separated list of task ids for which you want to fetch details.
*   `wait_for_completion` (Optional[bool], optional, default=None): If enabled, action will wait for the task to have status "Completed", "Incomplete", "Error".
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_list_endpoint_events`

List events related to the endpoints from Tanium. Action works with Tanium Threat Response API. Supported Entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `event_type` (Optional[List[str]], optional, default=None): Specify the type of the event that needs to be returned.
*   `time_frame` (Optional[List[str]], optional, default=None): Specify a time frame for the results. If "Alert Time Till Now" is selected, action will use start time of the alert as start time for the search and end time will be current time. If "30 Minutes Around Alert Time" is selected, action will search the alerts 30 minutes before the alert happened till the 30 minutes after the alert has happened. Same idea applies to "1 Hour Around Alert Time" and "5 Minutes Around Alert Time". If "Custom" is selected, you also need to provide "Start Time".
*   `start_time` (Optional[str], optional, default=None): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601
*   `end_time` (Optional[str], optional, default=None): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time.
*   `sort_field` (Optional[str], optional, default=None): Specify what parameter should be used for sorting.
*   `sort_order` (Optional[List[str]], optional, default=None): Specify the order of sorting.
*   `max_events_to_return` (Optional[str], optional, default=None): Specify how many events to return per entity. Default: 50. Maximum: 500.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_get_question_results`

Fetch results for the Tanium question. Action is a Siemplify async action. Note that the action is not working with Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `question_id` (str, required): Specify Tanium question id to get results for.
*   `max_rows_to_return` (str, required): Specify the max number of rows action should return for the question.
*   `create_case_wall_table` (Optional[bool], optional, default=None): If enabled, action will create a case wall table as part of action results.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_ping`

Test connectivity to the Tanium installation with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_create_connection`

Create connection to the endpoint in Tanium. Supported Entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_list_connections`

List endpoint connections in Tanium.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_enrich_entities`

Enrich entities using information from Tanium. Supported entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `additional_fields` (Optional[str], optional, default=None): Specify additional fields to fetch from Tanium for entity enrichment. Parameter accepts multiple values as a comma separated string.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_download_file`

Download a file from endpoints in Tanium. Action works with Tanium Threat Response API. Supported Entities: Hostname, IP Address. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_paths` (str, required): Specify the absolute path of the files on the endpoint that needs to be downloaded.
*   `download_folder_path` (str, required): Specify the path to the folder, where you want to store the files.
*   `overwrite` (Optional[bool], optional, default=None): If enabled, action will overwrite the file with the same name.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tanium_delete_file`

Delete a file from endpoints in Tanium. Action works with Tanium Threat Response API. Supported Entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_paths` (str, required): Specify the absolute path of the files on the endpoint that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
