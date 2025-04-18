# Cuckoo Sandbox Integration

## Overview

This integration allows you to connect to a Cuckoo Sandbox instance to submit files and URLs for analysis, retrieve analysis reports, and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cuckoo Sandbox details:

*   **API URL:** The base URL of your Cuckoo Sandbox API endpoint (e.g., `http://cuckoo.local:8090/`).
*   **(Optional) API Token:** An API token if your Cuckoo instance requires authentication for API access.
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate if using HTTPS.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Get Report

Get report of a particular task by id (async). Waits for the analysis task to complete before retrieving the report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_id` (string, required): The Cuckoo task ID (e.g., `10`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the Cuckoo analysis report for the specified task ID.

### Detonate File

Submit a file for analysis and get a report (async). This action uploads the file, waits for analysis completion, and returns the report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths` (string, required): The path of the file to submit (accessible by the SOAR server/agent).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports File entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the analysis report for the submitted file.

### Ping

Test Connectivity to the Cuckoo Sandbox API.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Detonate Url

Send a URL for analysis and get a report (async). This action submits the URL, waits for analysis completion, and returns the report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the analysis report for the submitted URL.

## Notes

*   Ensure the Cuckoo integration is properly configured in the SOAR Marketplace tab with the correct API URL and API Token (if required).
*   File paths for the `Detonate File` action must be accessible from the SOAR server or agent executing the action.
*   Detonation actions (`Detonate File`, `Detonate Url`) and `Get Report` are asynchronous and may take significant time depending on the Cuckoo analysis duration. Adjust playbook timeouts accordingly.
