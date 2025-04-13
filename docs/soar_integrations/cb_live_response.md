# CB Live Response Integration

## Overview

This integration allows you to connect to VMware Carbon Black Cloud's Live Response feature to perform actions directly on endpoints. Actions include managing files (list, download, upload, delete), managing processes (list, kill), creating memory dumps, and executing files.

## Configuration

To configure this integration within the SOAR platform, you typically need the following VMware Carbon Black Cloud details (similar to CB Cloud/CB Defense):

*   **API URL:** The base URL for your Carbon Black Cloud instance (e.g., `https://defense-prod05.conferdeploy.net`).
*   **Org Key:** Your organization key found in the Carbon Black Cloud console.
*   **API ID:** An API Key ID generated under API Access in your Carbon Black Cloud settings (ensure it has Live Response permissions).
*   **API Secret Key:** The corresponding API Secret Key generated along with the API ID.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API key has the necessary Live Response permissions enabled.)*

## Actions

### Create Memdump

Create memdump on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `file_name` (string, optional): Specify the file name for memdump creation (case insensitive). Can be a full path (e.g., `C:\dumps\memory.dmp`), overriding `remote_directory_path`. Can also be provided via a File entity.
*   `remote_directory_path` (string, optional): Specify the directory path on the remote host to store the memdump (e.g., `C:\TMP\`). Used if `file_name` is not a full path.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the memdump creation task.

### Ping

Test connectivity to the VMware Carbon Black Endpoint Standard Live Response with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Execute File

Execute file on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `file_name` (string, optional): Specify the file name to execute (case insensitive). Can be a full path. Can also be provided via a File entity.
*   `remote_directory_path` (string, optional): Specify the remote directory path for the file to execute (e.g., `C:\TMP\`). Used if `file_name` is not a full path.
*   `output_log_file_on_remote_host` (string, optional): Specify the output log file action should save the redirected output to (e.g., `C:\TMP\cmdoutput.log`).
*   `command_arguments_to_pass_to_file` (string, optional): Specify the command arguments to pass for executing the file (e.g., `/C whoami` for `cmd.exe`).
*   `wait_for_the_result` (bool, optional): If enabled, action will wait for the command to complete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the file execution task.

### List Processes

List processes running on endpoint based on the provided Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `process_name` (string, optional): Process name to search for on the host.
*   `how_many_records_to_return` (string, optional): How many records per entity action should return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes found.

### Kill Process

Kill process on a host based on the Siemplify Host or IP entity. Note: The Process name can be provided either as a Siemplify entity (artifact) or as an action input parameter. Input parameter takes priority.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `process_name` (string, optional): Process name to search PID for and kill.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname, IP Address, and Process entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the kill process operation.

### List Files

List files on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `remote_directory_path` (string, required): Specify the target directory path action should list (e.g., `C:\TMP\` or `/tmp/`).
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `max_rows_to_return` (string, optional): Specify how many rows action should return.
*   `start_from_row` (string, optional): Specify from which row action should start to return data.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of files in the specified directory.

### Download File

Download a file from a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `local_directory_path` (string, required): Specify the local directory path action should save the file to (e.g., `/tmp/`).
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `file_name` (string, optional): Specify the file name to download (case insensitive). Can be a full path. Can also be provided via a File entity.
*   `remote_directory_path` (string, optional): Specify the remote directory path action should take to download the file (e.g., `C:\TMP\`). Used if `file_name` is not a full path.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including the local path where the file was saved (often appended with hostname/IP for uniqueness).

### List Files in Cloud Storage

List files in the VMware Carbon Black Cloud file storage for an existing live response session based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `max_rows_to_return` (string, optional): Specify how many rows action should return.
*   `start_from_row` (string, optional): Specify from which row action should start to return data.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of files available in the session's cloud storage.

### Put File

Put (upload) a file on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `destination_directory_path` (string, required): Specify the target directory path action should upload the file to (e.g., `C:\TMP\`).
*   `file_name` (string, optional): Specify the file name to upload (case insensitive). Can be a full path. Can also be provided via a File entity.
*   `source_directory_path` (string, optional): Specify the source directory path action should take to get the file to upload (e.g., `/tmp/`). Used if `file_name` is not a full path.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the upload operation.

### Delete File

Delete a file from a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `remote_directory_path` (string, optional): Specify the remote directory path to file to delete (e.g., `C:\TMP\`). Used if `file_name` is not a full path.
*   `file_name` (string, optional): Specify the file name to delete (case insensitive). Can be a full path. Can also be provided via a File entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Delete File from Cloud Storage

Delete a file from the VMware Carbon Black Cloud file storage for an existing live response session based on the Siemplify Host or IP entity. Note: This action requires API v6.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `check_for_active_session_x_times` (string, required): How many attempts action should make to get active session for the entity. Check is made every 2 seconds.
*   `file_name` (string, optional): Specify the file name to delete (case insensitive). Can be provided via a File entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation from cloud storage.

## Notes

*   Ensure the CB Live Response integration is properly configured in the SOAR Marketplace tab with the correct API URL, Org Key, API ID, and API Secret Key.
*   The API key used requires **Live Response** permissions within Carbon Black Cloud.
*   Most actions require an active Live Response session to the target endpoint. The `check_for_active_session_x_times` parameter controls the retry attempts for establishing this session.
*   File paths can often be specified as full paths in the `file_name` parameter or by combining `file_name` and a directory path parameter.
*   When downloading files to the SOAR server from multiple endpoints, filenames are often appended with the hostname/IP to prevent overwrites.
