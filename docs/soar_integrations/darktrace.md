# Darktrace Integration

## Overview

This integration allows interaction with the Darktrace platform to retrieve endpoint information, events, model breach details, and manage model breach statuses.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Darktrace details:

*   **API URL:** The URL of your Darktrace Master instance API (e.g., `https://yourdarktrace.example.com`).
*   **Public Token:** Your public API token generated in the Darktrace UI.
*   **Private Token:** Your private API token generated in the Darktrace UI.
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API tokens have the necessary permissions for the desired API calls.)*

## Actions

### List Similar Devices

List similar devices to the endpoint in Darktrace. Supported entities: IP, Hostname, Mac Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_devices_to_return` (string, optional): Specify how many similar devices to return per entity. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address, Hostname, and MAC Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing a list of devices considered similar to the target entity/entities.

### Update Model Breach Status

Update model breach status in Darktrace.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `status` (List[Any], required): Specify what status to set for the model breach (e.g., `Acknowledged`, `Unacknowledged`, `False Positive`).
*   `model_breach_id` (string, required): Specify the ID of the model breach to update.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the status update operation.

### Execute Custom Search

Execute custom search in Darktrace using its query language.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the Darktrace query to execute.
*   `time_frame` (List[Any], optional): Specify a time frame (e.g., Last Hour, Last Day, Custom, Alert Time Till Now, etc.). If "Custom", `start_time` is required.
*   `start_time` (string, optional): Specify the start time (ISO 8601 format). Required if `time_frame` is "Custom".
*   `end_time` (string, optional): Specify the end time (ISO 8601 format). Uses current time if `time_frame` is "Custom" and this is empty.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the custom search query.

### List Endpoint Events

List latest events related to the endpoint in Darktrace. Supported entities: IP, Hostname, MacAddress. Note: events will be returned in UTC timezone.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_type` (string, required): Comma-separated list of event types (e.g., `connection`, `unusualconnection`, `newconnection`, `notice`, `devicehistory`, `modelbreach`).
*   `time_frame` (List[Any], required): Specify a time frame for the search. If "Custom", `start_time` is required.
*   `start_time` (string, optional): Specify the start time (ISO 8601 format). Required if `time_frame` is "Custom".
*   `end_time` (string, optional): Specify the end time (ISO 8601 format). Uses current time if `time_frame` is "Custom" and this is empty.
*   `max_events_to_return` (string, optional): Specify how many events to return per event type. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address, Hostname, MAC Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of events for the specified endpoint(s) and event type(s).

### Add Comment To Model Breach

Add a comment to model breach in Darktrace.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `model_breach_id` (string, required): Specify the ID of the model breach to add a comment to.
*   `comment` (string, required): Specify the comment for the model breach.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Ping

Test connectivity to the Darktrace with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enrich Entities

Enrich entities using information from Darktrace. Supported entities: IP, Hostname, MacAddress, URL (domain part is extracted).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fetch_connection_data` (bool, optional): If enabled, return additional connection information related to internal endpoints.
*   `max_hours_backwards` (string, optional): Specify how many hours backwards to fetch connection data. Default: 24.
*   `create_endpoint_insight` (bool, optional): If enabled, create an insight containing information about internal endpoints.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address, Hostname, MAC Address, URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

## Notes

*   Ensure the Darktrace integration is properly configured in the SOAR Marketplace tab with the correct API URL, Public Token, and Private Token.
*   The API tokens require appropriate permissions within the Darktrace platform for the desired actions.
*   Refer to Darktrace documentation for details on their query language used in `Execute Custom Search`.
*   Time parameters often use ISO 8601 format.
