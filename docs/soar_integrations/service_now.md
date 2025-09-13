# ServiceNow SOAR Integration

## Overview

This document outlines the available tools (actions) for the ServiceNow integration within the SOAR platform.

## Tools

### `service_now_add_attachment`

Add attachment to a table record in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify name of the table, where is located the record to which you want to add attachment.
*   `record_sys_id` (str, required): Specify sys id of the record to which you want to add attachment.
*   `file_path` (str, required): Specify a comma-separated list of absolute paths to the files that need to be attached.
*   `mode` (Optional[List[str]], optional, default=None): Specify the mode for the action. If \"Add New Attachment\" is selected, action will add a new attachment, if it even has the same name. If \"Overwrite Existing Attachment\" is selected, action will remove other attachments with the same name and add a new attachment.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_add_comment`

Add a comment to a ServiceNow incident

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `incident_number` (str, required): Specify number of the incident. Format: INCxxxxxxx
*   `comment` (str, required): Specify what comment to add to the incident.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_add_comment_and_wait_for_reply`

Wait for new comment to be added to the given incident. Action result is the content of the new comments

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `incident_number` (str, required): Specify number of the incident. Format: INCxxxxxxx
*   `comment` (str, required): Specify what comment to add to the incident.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_add_comment_to_record`

Add a comment to a specific table record in ServiceNow. Note: Action is running as async if "Wait For Reply" is enabled, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the name of the table to which you want to add a comment or work note. Example: incident.
*   `type` (List[str], required): Specify whether comment or work note should be added to the record.
*   `record_sys_id` (str, required): Specify the record ID to which you want to add a comment or work note.
*   `text` (str, required): Specify the content of the comment or work note.
*   `wait_for_reply` (bool, required): If enabled, action will wait for reply. Note: action will track comments, if comments are sent and work notes, if work notes are sent.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_add_parent_incident`

Add the parent incident for the incidents in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `parent_incident_number` (str, required): Parent incident number. All of the incidents in the \"Child Incident Numbers\" parameter will be added as children for the parent incident. Configure this parameter in the following format: INCxxxxxxx
*   `child_incident_numbers` (str, required): Comma-separated list of numbers that are related to the incident and used as children for the parent incident. Configure this parameter in the following format: INCxxxxxxx
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_close_incident`

Close a ServiceNow incident

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `incident_number` (str, required): Specify number of the incident. Format: INCxxxxxxx
*   `close_reason` (str, required): Specify the reason, why incident was closed.
*   `resolution_code` (List[str], required): Specify the resolution code for the incident.
*   `close_notes` (str, required): Specify the close notes for the incident.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_create_alert_incident`

Create an incident related to a Siemplify alert

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `impact` (str, required): Specify impact of the incident. Possible values: 1 for High, 2 for Medium and 3 for Low.
*   `urgency` (str, required): Specify urgency of the incident. Possible values: 1 for High, 2 for Medium and 3 for Low.
*   `category` (Optional[str], optional, default=None): Specify category of the incident.
*   `assignment_group_id` (Optional[str], optional, default=None): Specify full name of the group that was assigned to the incident.
*   `assigned_user_id` (Optional[str], optional, default=None): Specify full name of the user that was assigned to the incident.
*   `description` (Optional[str], optional, default=None): Specify description of the incident.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_create_incident`

Create a new incident in the ServiceNow system

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `short_description` (str, required): Specify short description of the incident.
*   `impact` (str, required): Specify impact of the incident. Possible values: 1 for High, 2 for Medium and 3 for Low.
*   `urgency` (str, required): Specify urgency of the incident. Possible values: 1 for High, 2 for Medium and 3 for Low.
*   `category` (Optional[str], optional, default=None): Specify category of the incident.
*   `assignment_group_id` (Optional[str], optional, default=None): Specify full name of the group that was assigned to the incident.
*   `assigned_user_id` (Optional[str], optional, default=None): Specify full name or the username of the user that was assigned to the incident.
*   `description` (Optional[str], optional, default=None): Specify description of the incident.
*   `custom_fields` (Optional[str], optional, default=None): Specify a comma-separated list of fields and values. Format: field_1:value_1,field_2:value_2. You can also specify a JSON object as input. Note: this parameter has priority and all of the fields will be overwritten with the value that is provided for this parameter. Example: {\"field\":\"value\"}
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_create_record`

Create new records in different tables of Service Now.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (Optional[str], optional, default=None): Specify what table should be used to create a record.
*   `object_json_data` (Optional[Union[str, dict]], optional, default=None): Specify JSON data that is needed to create a record.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_download_attachments`

Download attachments related to a table record in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify name of the table, where the record from which you want to download attachments is located. Example: incident.
*   `record_sys_id` (str, required): Specify sys id of the record from which you want to download attachment.
*   `download_folder_path` (str, required): Specify the absolute folder path, where you want to store the downloaded attachments.
*   `overwrite` (bool, required): If enabled, action will overwrite files with the same name.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_get_child_incident_details`

Retrieve information about child incidents based on the parent incident in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `parent_incident_number` (str, required): Specify a number of the incident for which you want to retrieve child incident details. Format: INCxxxxxxx
*   `max_child_incident_to_return` (Optional[str], optional, default=None): Specify how many child incidents to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_get_cmdb_record_details`

Get detailed CMDB records from the same class in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `class_name` (str, required): Specify name of the class, from where you want to list records. Example: cmdb_ci_appl.
*   `sys_id` (str, required): Specify a comma-separated list of record sys ids for which you want to retrieve details.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many record relations per type to return.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_get_incident`

Retrieve information about a ServiceNow incident

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `incident_number` (str, required): Specify number of the incident. Format: INCxxxxxxx
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_get_oauth_token`

Get an Oauth refresh token for ServiceNow. Requires: Username, Password, Client ID and Client Secret to be provided in the configuration tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_get_record_details`

Retrieve information about specific table records in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify name of the table, where you want to search for the record. Example: incident.
*   `record_sys_id` (str, required): Specify the record ID for which you want to retrieve details.
*   `fields` (Optional[str], optional, default=None): Specify a comma-separated list of fields that should be returned for that record. If nothing is specified, action will return the default fields for that record. Example: field_1,field_2.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_get_user_details`

Retrieve information about the user by the sys_id or email in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `user_sys_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of sys_ids of the users for which you want to retrieve details. Example: sys_id_1,sys_id_2
*   `emails` (Optional[str], optional, default=None): Specify a comma-separated list of emails of the users for which you want to retrieve details. Example: email1@example.com,email2@example.com
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_list_cmdb_records`

List CMDB records from the same class in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `class_name` (str, required): Specify name of the class, from where you want to list records. Example: cmdb_ci_appl.
*   `query_filter` (Optional[str], optional, default=None): Specify query filter for the results. Visit documentation to get more details. Example of the filter: sys_idLIKE1^sys_idSTARTSWITH0.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_list_record_comments`

List comments related to a specific table record in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the name of the table for which you want to list comments or work notes. Example: incident.
*   `record_sys_id` (str, required): Specify the record ID for which you want to list comments or work notes.
*   `type` (List[str], required): Specify whether comment or work note should be listed.
*   `max_results_to_return` (Optional[str], optional, default=None): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_list_records_related_to_user`

List records from a table related to a user in ServiceNow.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify name of the table, where you want to search for related records. Example: incident.
*   `usernames` (str, required): Specify a comma-separated list of usernames for which you want to retrieve related records.
*   `max_days_backwards` (str, required): Specify how many days backwards to fetch related records.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return per user. Default: 50
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_update_incident`

Update incident information

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `incident_number` (str, required): Specify number of the incident. Format: INCxxxxxxx
*   `short_description` (Optional[str], optional, default=None): Specify short description of the incident.
*   `impact` (Optional[str], optional, default=None): Specify impact of the incident. Possible values: 1 for High, 2 for Medium and 3 for Low.
*   `urgency` (Optional[str], optional, default=None): Specify urgency of the incident. Possible values: 1 for High, 2 for Medium and 3 for Low.
*   `category` (Optional[str], optional, default=None): Specify category of the incident.
*   `assignment_group_id` (Optional[str], optional, default=None): Specify full name of the group that was assigned to the incident.
*   `assigned_user_id` (Optional[str], optional, default=None): Specify email address or the username of the user that was assigned to the incident.
*   `description` (Optional[str], optional, default=None): Specify description of the incident.
*   `incident_state` (Optional[str], optional, default=None): Status name or status id.
*   `custom_fields` (Optional[str], optional, default=None): Specify a comma-separated list of fields and values. Format: field_1:value_1,field_2:value_2. You can also specify a JSON object as input. Note: this parameter has priority and all of the fields will be overwritten with the value that is provided for this parameter. Example: {\"field\":\"value\"}
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_update_record`

Update available records in different tables of Service Now.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `object_json_data` (Union[str, dict], required): Specify JSON data that is needed to update a record.
*   `record_sys_id` (str, required): Specify Sys ID of the needed record.
*   `table_name` (Optional[str], optional, default=None): Specify what table should be used to update a record.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_wait_for_comments`

Wait for comments related to a specific table record in ServiceNow. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify the name of the table in which you want to wait for a comment or work note. Example: incident.
*   `record_sys_id` (str, required): Specify the record ID in which you want to wait for a comment or work note.
*   `type` (List[str], required): Specify for what type of object action needs to wait.
*   `wait_mode` (List[str], required): Specify the wait mode for the action. If \"Until Timeout\" is selected, action will wait until and return all of the comments in that timeframe. If \"Until First Message\" is selected, action will wait until a new message appears after action execution. If \"Until Specific Text\" is selected, action will wait until there is a message that is equal to the string provided in the \"Text\" parameter. Note: \"Text\" parameter is mandatory, if \"Until Specific Text\" is provided.
*   `text` (Optional[str], optional, default=None): Specify the text for which action needs to wait. Note: this parameter is only relevant, if \"Until Specific Text\" is selected for \"Wait Mode\" parameter.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_wait_for_field_update`

Action to wait for field update.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `table_name` (str, required): Specify what table should be used to create a record.
*   `record_sys_id` (str, required): Specify Sys ID of the needed record.
*   `field_column_name` (str, required): Specify name of the column that is expected to be updated.
*   `field_values` (str, required): Specify values that are expected in the column. Example: In Progress,Resolved.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_now_wait_for_status_update`

ServiceNow - Wait For Status Update

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `incident_number` (str, required): Specify number of the incident. Format: INCxxxxxxx
*   `statuses` (str, required): Specify what statuses of the incident are expected. Example: In Progress,Resolved.
*   `target_entities` (List[TargetEntity], optional, default=list()): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
