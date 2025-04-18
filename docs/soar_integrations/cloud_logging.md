# Google Cloud Logging Integration

## Overview

This integration allows you to connect to Google Cloud Logging to execute log queries and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Google Cloud details:

*   **Service Account Key:** A JSON key file for a Google Cloud service account. This service account needs appropriate IAM permissions to read logs from the specified project or organization (e.g., `roles/logging.viewer`).
*   **(Optional) Project ID:** The default Google Cloud Project ID to query against if not specified in the action.
*   **(Optional) Organization ID:** The default Google Cloud Organization ID to query against if not specified in the action.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the service account has the necessary permissions.)*

## Actions

### Execute Query

Use the Execute Query action to execute custom queries in Cloud Logging.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): A query to find the logs for (using Cloud Logging query language).
*   `project_id` (string, optional): The project ID to use. Overrides integration configuration if provided.
*   `organization_id` (string, optional): The organization ID to use. Overrides integration configuration if provided.
*   `time_frame` (List[Any], optional): A period to retrieve the results from (e.g., Last Hour, Last 6 Hours, Custom). If "Custom", `start_time` is required.
*   `start_time` (string, optional): The start time (ISO 8601 format). Required if `time_frame` is "Custom".
*   `end_time` (string, optional): The end time (ISO 8601 format). Uses current time if `time_frame` is "Custom" and this is empty.
*   `max_records_to_return` (string, optional): The maximum number of results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the log entries matching the query.

### Ping

Use the Ping action to test connectivity to the Cloud Logging.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the Cloud Logging integration is properly configured in the SOAR Marketplace tab with valid Google Cloud credentials (Service Account Key).
*   The service account used requires the `logging.logEntries.list` permission (typically included in roles like `roles/logging.viewer`).
*   Refer to the [Google Cloud Logging query language documentation](https://cloud.google.com/logging/docs/view/logging-query-language) for query syntax.
*   Specify either `project_id` or `organization_id` in the action or integration configuration to define the scope of the query.
