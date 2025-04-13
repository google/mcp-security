# CB Response Integration

## Overview

This integration allows you to connect to VMware Carbon Black EDR (formerly CB Response) to manage endpoints, processes, binaries, and alerts. Actions include isolating/unisolating hosts, blocking/unblocking hashes, searching processes and binaries, enriching entities, managing watchlists, and resolving alerts.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Carbon Black EDR details:

*   **Server URL:** The URL of your Carbon Black EDR server (e.g., `https://cbresponse.example.com`).
*   **API Token:** An API token generated within your Carbon Black EDR console for authentication.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API token has the necessary permissions for the actions you intend to use.)*

## Actions

### Hosts By Process

Get hosts that are related to a particular process.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Process entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of hosts associated with the specified process(es).

### Isolate Host

Isolate an endpoint from the network.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the isolation operation.

### Unblock Hash

Unblock a hash (MD5, SHA1, SHA256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unblock operation.

### Process Free Query

List processes by free query.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Query to execute in process search (e.g., `process_name:python.exe`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes matching the query.

### Enrich Binary

Enrich hash with binary info from CB Response.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified hash(es).

### Unisolate Host

Rejoin an endpoint to the network.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unisolate operation.

### Enrich Process

Enrich process entity with data from CB Response.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Process entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified process(es).

### Ping

Test Connectivity to CB Response.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get FileMod Data For Process

Get file modification data for a process by its ID and segment ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `process_id` (string, required): Process unique ID.
*   `segment_id` (string, required): Segment ID (e.g., 1).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing file modification events associated with the process segment.

### Resolve Alert

Resolve an alert. Note: Carbon Black Response REST-API returns a successful answer even if the alert that you tried to resolve doesn’t exist.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The ID of the alert to resolve.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the resolve operation.

### List Processes

List processes that are related to given entities (Hostname, IP Address).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes associated with the specified entities.

### Kill Process

Kill a process on a particular host based on Process ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Process entities (requires Process ID).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the kill process operation.

### Get License

Get the current license from CB Response.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details about the current CB Response license.

### Get Process Tree Data

Get process tree data for process by id (JSON).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `process_id` (string, required): Process unique ID.
*   `segment_id` (string, required): Segment ID (e.g., 1).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the process tree data in JSON format.

### Binary Free Query

List binaries by free query.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Query to execute (e.g., `md5:* AND original_filename:<file-name>`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of binaries matching the query.

### Get System Info

Get system information for a sensor from CB Response and enrich entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing system information and enrichment data for the specified sensor(s).

### Create Watchlist

Create a watchlist for processes (type = events) or for binaries (type = modules).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_name` (string, required): Name of this watchlist.
*   `query` (string, required): The raw Carbon Black query that this watchlist matches.
*   `watchlist_type` (string, required): The type of watchlist (e.g., `modules`, `events`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the watchlist creation.

### Block Hash

Block a hash (MD5, SHA1, SHA256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block operation.

### Download Binary

Download a binary based on its hash (MD5, SHA1, SHA256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, potentially including the file content or path.

## Notes

*   Ensure the CB Response integration is properly configured in the SOAR Marketplace tab with the correct Server URL and API Token.
*   The API token requires appropriate permissions within Carbon Black EDR for the desired actions.
*   Refer to Carbon Black EDR documentation for query syntax details used in search actions.
*   Some actions have specific entity requirements (e.g., Process GUID for `Get Events Associated With Process by Process Guid`).
