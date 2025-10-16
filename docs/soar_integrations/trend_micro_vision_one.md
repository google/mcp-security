# Trend Micro Vision One SOAR Integration

## Overview

This document outlines the tools available for the Trend Micro Vision One integration within the SOAR platform. These tools allow interaction with the Trend Micro Vision One API for managing endpoints, emails, files, URLs, and workbench alerts.

## Tools

### `trend_vision_one_execute_email`

Execute email action on the endpoint in Trend Vision One. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `message_id` (str, required): Specify the ID of the message that needs to be used in the action.
*   `action` (List[str], optional, default=None): Specify the action for the email.
*   `mailbox` (str, optional, default=None): Specify the mailbox related to the message.
*   `description` (str, optional, default=None): Specify a description for the performed action.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_execute_custom_script`

Execute custom script on the endpoint in Trend Vision One. Supported entities: Hostname, IP address. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `script_name` (str, required): Specify the name of the script that needs to be executed on the endpoints.
*   `script_parameters` (str, optional, default=None): Specify the parameters for the script.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_ping`

Test connectivity to the Trend Vision One with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_submit_url`

Submit url in Trend Vision One. Supported entities: URL. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_enrich_entities`

Enrich entities using information from Trend Vision One. Supported entities: Hostname, IP address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_update_workbench_alert`

Update a workbench alert in Trend Vision One.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alert_id` (str, required): Specify the ID of the alert needs to be updated.
*   `status` (List[str], required): Specify what status to set for the alert.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_isolate_endpoint`

Isolate endpoints in Trend Vision One. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `description` (str, optional, default=None): Specify the reasoning for the isolation of the endpoints.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_submit_file`

Submit file in Trend Vision One. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_paths` (str, required): Specify a comma-separated list of paths for the files that need to be submitted.
*   `archive_password` (str, optional, default=None): Specify the password for the archive.
*   `document_password` (str, optional, default=None): Specify the password for the document.
*   `arguments` (str, optional, default=None): Specify the arguments for the submitted file.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `trend_vision_one_unisolate_endpoint`

Unisolate endpoints in Trend Vision One. Supported entities: IP Address, Hostname. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `description` (str, optional, default=None): Specify the reasoning for the unisolation of the endpoints.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
