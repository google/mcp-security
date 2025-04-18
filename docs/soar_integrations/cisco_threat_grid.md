# Cisco Threat Grid Integration

## Overview

This integration allows you to connect to Cisco Threat Grid for malware analysis and threat intelligence. Actions include submitting files for analysis, retrieving analysis results (submissions), getting associated IPs and domains for file hashes, and testing connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cisco Threat Grid details:

*   **API Key:** Your Cisco Threat Grid API key for authentication.
*   **Server URL:** The URL of your Threat Grid instance (Cloud or On-premise, e.g., `https://panacea.threatgrid.com`).
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Get Hash Associated IPs

Get IPs associated to a given hash (SHA256, MD5, SHA1).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of IP addresses associated with the provided hash(es).

### Get Hash Associated Domains

Get domains associated to a given hash (SHA256, MD5, SHA1).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of domains associated with the provided hash(es).

### Ping

Test Connectivity to Cisco Threat Grid.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Upload Sample

Upload and analyze a sample file. Note: Action runs asynchronously. Adjust script timeout in the SOAR IDE as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): The sample file path (accessible by the SOAR server/agent). For multiple, use comma-separated values.
*   `private` (bool, required): If checked, the sample will be marked private.
*   `vm` (string, optional): The VM to run the analysis on (e.g., `win7-x64`).
*   `playbook` (string, optional): Name of a playbook to apply to this sample run (e.g., `default`).
*   `network_exit` (string, optional): Specify the Network Exit Location for outgoing traffic.
*   `linux_server_address` (string, optional): IP address of a remote Linux server where the file is located (if not local).
*   `linux_username` (string, optional): Username for the remote Linux server.
*   `linux_password` (string, optional): Password for the remote Linux server.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the submission, likely including the sample ID and analysis status.

### Get Submissions

Get submission details (analysis reports) by entity (FileHash, URL, IP Address, Domain).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark as suspicious if max threat score passes the threshold (0-100).
*   `max_submissions_to_return` (string, optional): Specify how many submissions to return per entity. Default: 10. Maximum: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash, URL, IP Address, Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the submission details and analysis reports for the specified entities.

## Notes

*   Ensure the Cisco Threat Grid integration is properly configured in the SOAR Marketplace tab with a valid API Key and Server URL.
*   The API key requires appropriate permissions within Cisco Threat Grid.
*   The `Upload Sample` action is asynchronous; analysis results might take time and may need to be checked separately or via subsequent playbook steps.
*   File paths for `Upload Sample` must be accessible from the SOAR server or agent executing the action, unless remote Linux server details are provided.
