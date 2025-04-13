# Cybereason Integration

## Overview

This integration allows interaction with the Cybereason platform to manage endpoints (sensors), Malops (Malicious Operations), reputation lists, and perform investigations. Actions include isolating/unisolating machines, managing file/IP/domain reputations, querying processes and files, managing Malops (get details, add comments, update status, list remediations, remediate), and retrieving sensor details.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cybereason details:

*   **Server Address:** The URL of your Cybereason console (e.g., `https://mycompany.cybereason.net`).
*   **Port:** The port for the Cybereason API (usually 443).
*   **Username:** The username for an API user account.
*   **Password:** The password for the API user account.
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has the necessary permissions for the desired API operations.)*

## Actions

### List Reputation Items

List information about items with reputation (blacklist/whitelist) in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains).
*   `filter_value` (string, optional): Specify the value to filter by (e.g., a specific hash, IP, or domain).
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of reputation items matching the criteria.

### Execute Custom Investigation Search

Execute investigation search based on parameters in Cybereason. This action supports nested queries for different item types.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query_filters_json` (Union[str, dict], required): Specify the query JSON. Follows the pattern `"{API field} {Operator} {Value}"`. Supports complex nested queries. Refer to Cybereason documentation for API fields and operators.
*   `fields_to_return` (string, required): Comma-separated list of API field names to return.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the custom investigation query.

### Prevent File

Add hash to a blacklist in Cybereason. Supported entities: File Hash. Note: only MD5 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (MD5 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the blacklist operation.

### Get Sensor Details

Get sensor details of entities in Cybereason. Supported entities: Hostname, IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (bool, optional): If enabled, create an insight containing sensor information.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details about the Cybereason sensor(s) on the specified host(s).

### Add Comment To Malop

Add a comment to an existing malop in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop to add a comment to.
*   `comment` (string, required): Specify the comment for the malop.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Unisolate Machine

Unisolate a machine in Cybereason. Supported entities: Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unisolate operation.

### Set Reputation

Set a reputation (blacklist/whitelist) for entity in Cybereason. Supported entities: File Hash (MD5, SHA1), IP Address, URL (domain part is extracted).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `reputation_list_type` (List[Any], required): Specify the reputation (`blacklist` or `whitelist`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash (MD5, SHA1), IP Address, URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the reputation update.

### Is Probe Connected

Check the connectivity of the endpoint (sensor) to Cybereason. Supported entities: Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary indicating the connectivity status of the sensor(s).

### List Malop Remediations

List available remediations for a malop in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop for which you want to list available remediations.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available remediation actions for the specified malop.

### Allow File

Remove hash from a blacklist in Cybereason. Supported entities: File Hash. Note: only MD5 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (MD5 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of removing the hash from the blacklist.

### Clear Reputation

Clear the reputation (remove from blacklist/whitelist) of the entity in Cybereason. Supported entities: File Hash (MD5, SHA1), IP Address, URL (domain part is stripped).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash (MD5, SHA1), IP Address, URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of clearing the reputation.

### Ping

Test connectivity to the Cybereason with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### List Malop Affected Machines

List machines affected by the Malop in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop for which you want to return affected machines.
*   `results_limit` (string, required): Specify how many results to return. Default: 100.
*   `create_hostname_entity` (bool, optional): If enabled, create a Hostname entity for each affected machine.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of machines affected by the specified malop.

### List Processes

List processes based on provided criteria in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `results_limit` (string, required): Specify how many processes to return.
*   `process_name` (string, optional): Comma-separated list of process names to filter by.
*   `machine_name` (string, optional): Comma-separated list of machine names to filter by.
*   `has_suspicions` (bool, optional): If enabled, only return suspicious processes.
*   `has_incoming_connection` (bool, optional): If enabled, only return processes with incoming connections.
*   `has_outgoing_connection` (bool, optional): If enabled, only return processes with outgoing connections.
*   `has_external_connection` (bool, optional): If enabled, only return processes with external connections.
*   `unsigned_process_with_unknown_reputation` (bool, optional): If enabled, only return unsigned processes with unknown reputation.
*   `running_from_temporary_folder` (bool, optional): If enabled, only return processes running from a temporary folder.
*   `privilege_escalation` (bool, optional): If enabled, only return processes with escalated privileges.
*   `malicious_use_of_ps_exec` (bool, optional): If enabled, only return processes related to malicious PsExec use.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes matching the criteria.

### Remediate Malop

Perform remediation action on the malop in Cybereason. Note: Action runs asynchronously. Use "List Malop Remediations" to get available remediation IDs.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop to remediate.
*   `remediation_unique_i_ds` (string, required): Comma-separated list of remediation action unique IDs to execute.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the remediation initiation.

### Execute Simple Investigation Search

Execute investigation search based on parameters in Cybereason. Note: Does not support nested queries. Only one data type (e.g., machines, users) can be queried at once. Use "Execute Custom Investigation Search" for nested queries.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fields_to_return` (string, required): Comma-separated list of API field names to return.
*   `request_type` (List[Any], optional): Specify what should be queried (e.g., `machines`, `users`).
*   `query_filters` (string, optional): Specify the query filter(s). Follows `"{API field} {Operator} {Value}"` pattern. Use new lines for multiple filters.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the simple investigation query.

### Enrich Entities

Enrich entities using information from Cybereason. Supported entities: Hostname, IP Address (external), File Hash (MD5, SHA1), URL (domain part is extracted).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insights` (bool, optional): If enabled, create an insight for each enriched entity.
*   `only_malicious_entity_insight` (bool, optional): If enabled, create insights only for entities classified as malicious (ransomware, maltool, unwanted, malware, blacklist). Affects IP, Hash, URL; Hostname insights are always created if `create_insights` is enabled.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

### List files

Get information about files from Cybereason based on hash or general query.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `results_limit` (string, required): Specify how many files to return.
*   `file_hash` (string, optional): Comma-separated list of file hashes (MD5, SHA1) to search for. If provided, `results_limit` is ignored for these specific hashes.
*   `fields_to_return` (string, optional): Comma-separated list of API field names to return. If empty, uses predefined defaults.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing information about the specified files.

### Get Malop

Retrieve detailed information about a malop in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop for which you want to return details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified malop.

### List Malop Processes

List processes related to the Malop in Cybereason.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop for which you want to return related processes.
*   `results_limit` (string, required): Specify how many results to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of processes associated with the specified malop.

### Isolate Machine

Isolate a machine in Cybereason. Supported entities: Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the isolation operation.

### Update Malop Status

Update status for the Malop in Cybereason. Note: detection malops support only "Remediated", "Not Relevant" or "Open" statuses.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malop_id` (string, required): Specify the ID of the malop that needs to be updated.
*   `status` (List[Any], required): Specify the new status for the malop (e.g., `OPEN`, `CLOSED`, `REMEDIATED`, `NOT_RELEVANT`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the status update operation.

## Notes

*   Ensure the Cybereason integration is properly configured in the SOAR Marketplace tab with the correct Server Address, Port, Username, and Password.
*   The API user requires appropriate permissions within Cybereason for the desired actions.
*   Hash-based actions often have limitations (e.g., MD5 only for `Prevent File`, MD5/SHA1 for `Set Reputation`/`Clear Reputation`).
*   Refer to Cybereason API documentation for specific query syntax and field names used in investigation searches.
*   Actions like `Remediate Malop` and `Execute Query` run asynchronously; adjust playbook timeouts as needed.
