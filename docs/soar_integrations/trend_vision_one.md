# Trend Vision One Integration

This document describes the available tools for the Trend Vision One integration within the SecOps SOAR MCP Server. Trend Vision One is a platform for XDR (Extended Detection and Response).

## Configuration

Ensure the Trend Vision One integration is configured in the SOAR platform with the necessary API token and region details.

## Available Tools

### trend_vision_one_execute_email
- **Description:** Execute an action (e.g., delete, quarantine) on an email message identified by its ID. This action runs asynchronously.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `message_id` (str, required): Specify the ID of the message to act upon.
    - `action` (List[str], optional): Specify the action for the email (refer to Trend Vision One documentation for valid actions). Defaults to None.
    - `mailbox` (str, optional): Specify the mailbox related to the message. Defaults to None.
    - `description` (str, optional): Specify a description for the performed action. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the action initiation.

### trend_vision_one_execute_custom_script
- **Description:** Execute a predefined custom script on specified endpoints (Hostname, IP address). This action runs asynchronously.
- **Supported Entities:** Hostname, IP Address
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `script_name` (str, required): Specify the name of the custom script to execute.
    - `script_parameters` (str, optional): Specify parameters for the script. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the Hostname or IP Address. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the script execution initiation.

### trend_vision_one_ping
- **Description:** Test connectivity to the Trend Vision One instance configured in the SOAR platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### trend_vision_one_submit_url
- **Description:** Submit a URL entity for analysis in Trend Vision One. This action runs asynchronously.
- **Supported Entities:** URL
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the URL. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the URL submission initiation.

### trend_vision_one_enrich_entities
- **Description:** Enrich entities (Hostname, IP address) using information from Trend Vision One.
- **Supported Entities:** Hostname, IP Address
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the Hostname or IP Address. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the enrichment results.

### trend_vision_one_update_workbench_alert
- **Description:** Update the status of a workbench alert in Trend Vision One.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `alert_id` (str, required): Specify the ID of the workbench alert to update.
    - `status` (List[str], required): Specify the new status for the alert (refer to Trend Vision One documentation for valid statuses).
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the update operation.

### trend_vision_one_isolate_endpoint
- **Description:** Isolate endpoints (IP Address, Hostname) in Trend Vision One. This action runs asynchronously.
- **Supported Entities:** IP Address, Hostname
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `description` (str, optional): Specify the reasoning for isolating the endpoints. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the Hostname or IP Address. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the isolation initiation.

### trend_vision_one_submit_file
- **Description:** Submit a local file for analysis to Trend Vision One. This action runs asynchronously.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `file_paths` (str, required): Specify a comma-separated list of absolute paths on the SOAR server filesystem for the files to be submitted.
    - `archive_password` (str, optional): Specify the password if the file is an archive. Defaults to None.
    - `document_password` (str, optional): Specify the password if the file is a document. Defaults to None.
    - `arguments` (str, optional): Specify arguments for the submitted file execution in the sandbox. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the file submission initiation.

### trend_vision_one_unisolate_endpoint
- **Description:** Remove endpoints (IP Address, Hostname) from isolation in Trend Vision One. This action runs asynchronously.
- **Supported Entities:** IP Address, Hostname
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `description` (str, optional): Specify the reasoning for unisolating the endpoints. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the Hostname or IP Address. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the unisolation initiation.
