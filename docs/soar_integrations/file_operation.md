# File Operation Integration

## Overview

This integration provides tools for performing various file operations, primarily focused on transferring and compressing files between Linux and Windows systems within the SOAR environment.

## Configuration

The configuration for this integration is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings. No specific parameters need to be configured within the playbook actions themselves, beyond the standard case and scope details, and the action-specific parameters.

## Actions

### Transfer File Linux To Windows

Transfers a file from a remote Linux host to a Windows share.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_linux_file_path` (string, required): The full path to the source file on the remote Linux server.
*   `source_linux_ip` (string, required): The IP address (x.x.x.x) of the source Linux server.
*   `source_linux_username` (string, required): The username for the source Linux server.
*   `source_linux_password` (string, required): The password for the source Linux server.
*   `dest_win_path` (string, required): The destination folder path on the Windows share.
*   `keep_file` (boolean, required): Indicates whether to keep the file in the source location after transfer (True) or remove it (False).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Transfer File Linux To Linux

Transfers a file from one remote Linux host to another remote Linux host.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_linux_file_path` (string, required): The full path to the source file on the source Linux server.
*   `source_linux_ip` (string, required): The IP address (x.x.x.x) of the source Linux server.
*   `source_linux_username` (string, required): The username for the source Linux server.
*   `source_linux_password` (string, required): The password for the source Linux server.
*   `dest_linux_path` (string, required): The destination folder path on the destination Linux server.
*   `dest_linux_ip` (string, required): The IP address (x.x.x.x) of the destination Linux server.
*   `dest_linux_username` (string, required): The username for the destination Linux server.
*   `dest_linux_password` (string, required): The password for the destination Linux server.
*   `keep_file` (boolean, required): Indicates whether to keep the file in the source location after transfer (True) or remove it (False).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Transfer File Windows To Linux

Transfers a file from a Windows share to a remote Linux host.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_win_file_path` (string, required): The full path to the source file on the Windows share.
*   `dest_linux_path` (string, required): The destination folder path on the remote Linux server.
*   `dest_linux_ip` (string, required): The IP address (x.x.x.x) of the destination Linux server.
*   `dest_linux_username` (string, required): The username for the destination Linux server.
*   `dest_linux_password` (string, required): The password for the destination Linux server.
*   `keep_file` (boolean, required): Indicates whether to keep the file in the source location after transfer (True) or remove it (False).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Zip Files Linux

Creates a zip file from files matching a filter within a source folder on a remote Linux host.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `server_ip` (string, required): The IP address (x.x.x.x) of the Linux server.
*   `username` (string, required): The username for the Linux server.
*   `password` (string, required): The password for the Linux server.
*   `source_folder` (string, required): The remote server folder containing the files to zip.
*   `file_filter` (string, required): Filter for files to include in the zip (e.g., `*.txt`).
*   `output_folder` (string, required): The remote server folder where the zip file will be created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Tarzip Files Windows

Compresses files matching a filter into a tar.gz file on a Windows share.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_folder` (string, optional): The full path to the folder with the relevant files.
*   `file_filter` (string, optional): Filter for files to include in the tar.gz file (e.g., `*.txt`).
*   `output_folder` (string, optional): The path to the folder where the tar.gz file will be created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Tarzip Files Linux

Creates a tar.gz file from files matching a filter within a source folder on a remote Linux host. (Note: The description says "Create zip file", but the name implies tar.gz).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `server_ip` (string, required): The IP address (x.x.x.x) of the Linux server.
*   `username` (string, required): The username for the Linux server.
*   `password` (string, required): The password for the Linux server.
*   `source_folder` (string, required): The full path to the remote server folder containing the files.
*   `file_filter` (string, required): Filter for files to include in the archive (e.g., `*.txt`).
*   `output_folder` (string, required): The remote server folder where the archive file will be created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Transfer File Windows To Windows

Transfers a file between two Windows shares.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_win_file_path` (string, required): The full path to the source file on the source Windows share.
*   `dest_win_path` (string, required): The destination folder path on the destination Windows share.
*   `keep_file` (string, required): Indicates whether to keep the file in the source location ("True") or remove it ("False").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Tests connectivity for the FileOperation integration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Zip Files Windows

Creates a zip file from files matching a filter within a source folder on a Windows share.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_folder` (string, required): The folder containing the files to zip.
*   `file_filter` (string, required): Filter for files to include in the zip file (e.g., `*.txt`).
*   `output_folder` (string, required): The folder where the zip file will be created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   This integration relies on underlying scripts (`FileOperation_Transfer File Linux To Windows`, etc.) executed via the SOAR platform's scripting capabilities.
*   Ensure appropriate network connectivity and credentials are configured for accessing source and destination systems (Linux hosts via SSH, Windows shares).
*   The `keep_file` parameter behavior (True/False vs "True"/"False") might vary slightly between actions; refer to specific action details.
