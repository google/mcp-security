# Devo Integration

## Overview

This integration allows you to connect to the Devo platform to execute queries against your log data and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Devo details:

*   **API URL:** The URL of your Devo API endpoint (e.g., `https://api-us.devo.com`).
*   **API Key:** Your Devo API Key.
*   **API Secret:** Your Devo API Secret.
*   **(Optional) Token for siem.logtrust.alert.info:** A specific Devo Authentication Token if required for accessing the default alert table.
*   **(Optional) Additional Table Tokens:** You might need to configure additional tokens if you plan to query tables other than `siem.logtrust.alert.info` using the Simple Query or Advanced Query actions. Refer to Devo documentation for creating these tokens.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Ping

Test connectivity to the Devo instance with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Advanced Query

Execute an advanced query based on the provided parameters using Devo's LINQ query language. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify a query to execute against Devo instance. Example format: 'from siem.logtrust.alert.info'.
*   `time_frame` (List[Any], optional): Specify a time frame for the results (e.g., Last Hour, Last Day, Custom). If 'Custom' is selected, `start_time` is required.
*   `start_time` (string, optional): Specify the start time (ISO 8601 format, e.g., `2021-08-05T05:18:42Z`). Required if `time_frame` is "Custom".
*   `end_time` (string, optional): Specify the end time (ISO 8601 format). Uses current time if `time_frame` is "Custom" and this is empty.
*   `max_rows_to_return` (string, optional): Specify max number of rows the action should return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the advanced query.

### Simple Query

Execute a simple query based on the provided parameters. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `table_name` (string, required): Specify what table should be queried (e.g., `siem.logtrust.alert.info`).
*   `fields_to_return` (string, optional): Specify what fields to return (comma-separated). If empty, returns all fields.
*   `where_filter` (string, optional): Specify the WHERE filter for the query.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If 'Custom' is selected, `start_time` is required.
*   `start_time` (string, optional): Specify the start time (ISO 8601 format). Required if `time_frame` is "Custom".
*   `end_time` (string, optional): Specify the end time (ISO 8601 format). Uses current time if `time_frame` is "Custom" and this is empty.
*   `max_rows_to_return` (string, optional): Specify max number of rows the action should return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the simple query.

## Notes

*   Ensure the Devo integration is properly configured in the SOAR Marketplace tab with the correct API URL, API Key, and API Secret.
*   Querying tables other than `siem.logtrust.alert.info` might require generating specific Authentication Tokens in Devo and adding them to the integration configuration.
*   Refer to the [Devo LINQ documentation](https://docs.devo.com/confluence/ndt/latest/querying-data/linq-reference) for query syntax details.
*   Time parameters use ISO 8601 format (e.g., `2023-10-27T10:00:00Z`).
