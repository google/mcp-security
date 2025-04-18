# CB Enterprise EDR Integration

## Overview

This integration allows you to connect to VMware Carbon Black Enterprise EDR to search for process activity, enrich hashes, and retrieve events associated with specific processes.

## Configuration

To configure this integration within the SOAR platform, you typically need the following VMware Carbon Black Enterprise EDR details:

*   **API URL:** The base URL for your Carbon Black EDR server (e.g., `https://your-cb-edr.example.com`).
*   **API Token:** An API token generated within your Carbon Black EDR console for authentication.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API token has the necessary permissions for the actions you intend to use, such as process search and event retrieval.)*

## Actions

### Enrich Hash

Enrich Siemplify File hash entity based on the information from the VMware Carbon Black Enterprise EDR. Note: Action accepts file hashes only in SHA256 format!

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified SHA256 hash(es), such as process information where the hash was observed.

### Process Search

Search information about process activity on the host with CB sensor based on the provided search parameters. The action accepts Host Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_limit` (string, required): Specify how many records can be returned by the action.
*   `query` (string, optional): Query to execute in process search. For example, `process_name:svchost.exe` or `process_hash:9520a99e77d6196d0d09833146424113`.
*   `time_frame` (string, optional): Specify a time frame in hours for which to fetch alerts (e.g., `24`).
*   `sort_by` (string, optional): Specify a parameter for sorting the data (e.g., `last_update`).
*   `sort_order` (List[Any], optional): Sort order (Ascending/Descending).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the process search results matching the criteria.

### Ping

Test connectivity to the VMware Carbon Black Enterprise EDR with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Events Associated With Process by Process Guid

Get events associated with specific processes based on the information from the VMware Carbon Black Enterprise EDR. This action can get more detailed results on specific process activity than “Process Search” action. Note for the action to work, Siemplify process artifact passed to action should be a process guid type.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `process_guid` (string, required): Specify a process guid to search events for.
*   `query` (string, required): Query to execute within the process events. For example, `netconn_action:ACTION_CONNECTION_CREATE OR netconn_action:ACTION_CONNECTION_ESTABLISHED`.
*   `record_limit` (string, required): Specify how many records can be returned by the action.
*   `search_criteria` (string, optional): Specify a search criteria for the request. Currently, only `event_type` values are accepted (e.g., `netconn`, comma-separated for multiple).
*   `time_frame` (string, optional): Specify a time frame in hours for which to fetch events.
*   `sort_by` (string, optional): Specify a parameter for sorting the data.
*   `sort_order` (List[Any], optional): Sort order (Ascending/Descending).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Process entities (GUID format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the events associated with the specified process GUID(s).

## Notes

*   Ensure the CB Enterprise EDR integration is properly configured in the SOAR Marketplace tab with the correct API URL and API Token.
*   The API token requires appropriate permissions within Carbon Black EDR.
*   The `Enrich Hash` action specifically requires SHA256 hashes.
*   The `Get Events Associated With Process by Process Guid` action requires the Process entity identifier to be the Carbon Black process GUID.
*   Refer to Carbon Black EDR documentation for query syntax details.
