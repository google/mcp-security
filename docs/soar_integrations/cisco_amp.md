# Cisco AMP Integration

## Overview

This integration allows you to connect to Cisco Secure Endpoint (formerly Cisco AMP for Endpoints) to manage endpoints, file lists, policies, and groups. Actions include isolating/unisolating machines, managing file lists, retrieving computer/group/policy information, and finding computers based on network activity or file observations.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cisco Secure Endpoint details:

*   **API Host:** The hostname of your Cisco Secure Endpoint cloud console (e.g., `api.amp.cisco.com`, `api.apjc.amp.cisco.com`, `api.eu.amp.cisco.com`).
*   **Client ID:** Your 3rd party API client ID generated in the Secure Endpoint console.
*   **API Key:** Your API key associated with the Client ID.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API credentials have the necessary permissions for the desired actions.)*

## Actions

### Get Computers By Network Activity (URL)

Fetch a list of computers that have connected to the given hostname or URL.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of computers that connected to the specified URL/Hostname.

### Get Computers By Network Activity (Ip)

Fetch a list of computers that have connected to the given IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of computers that connected to the specified IP address.

### Add File To File List

Add a SHA-256 hash to a specific file list (e.g., a custom blacklist).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_list_name` (string, required): The name of the target file list (e.g., `File Blacklist`).
*   `description` (string, required): Description of the file being added.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of adding the hash to the file list.

### Unisolate Machine

Stop isolation of Machine by connector guid.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Requires Connector GUID entity.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unisolate operation.

### Get Groups

Get group details.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details of the groups in the Cisco Secure Endpoint environment.

### Get Computers By File Hash

Fetch a list of computers that have observed files with the given SHA-256 value.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of computers that observed the specified file hash.

### Get File Lists By Policy

Get the file lists that are assigned in a policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): The name of the policy (e.g., Triage).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the file lists associated with the specified policy.

### Create Group

Create a new group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): The name of the new group.
*   `group_description` (string, required): The description of the new group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the group creation, likely including the new group GUID.

### Get Computers By File Name

Fetch a list of computers that have observed files with the given file name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports File entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of computers that observed the specified file name.

### Ping

Test connectivity to Cisco AMP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get File List Items

Get the items (SHA-256 hashes) listed in a given file list.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_list_name` (string, required): The name of the file list (e.g., File Blacklist).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of SHA-256 hashes in the specified file list.

### Get Policies

Get policy details.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details of the policies in the Cisco Secure Endpoint environment.

### Get Computer Info

Get details about a computer based on its connector GUID, hostname, or IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities (which are used to find the connector GUID).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified computer(s).

### Isolate Machine

Isolate Machine by connector guid.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Requires Connector GUID entity.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the isolation operation.

## Notes

*   Ensure the Cisco AMP integration is properly configured in the SOAR Marketplace tab with the correct API Host, Client ID, and API Key.
*   The API credentials require appropriate permissions within Cisco Secure Endpoint.
*   Actions involving file hashes typically expect SHA-256.
*   Isolation/Unisolation actions require the target machine's Connector GUID. You might need to use `Get Computer Info` first to retrieve this if you only have the hostname or IP.
