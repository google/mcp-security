# CB Protection Integration

## Overview

This integration allows you to connect to VMware Carbon Black App Control (formerly CB Protection) to manage file reputation, policies, and endpoint information. Actions include finding files on endpoints, blocking/unblocking hashes, analyzing files, retrieving computer information, and managing policies.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Carbon Black App Control details:

*   **Server URL:** The URL of your Carbon Black App Control server (e.g., `https://cbprotection.example.com`).
*   **API Token:** An API token generated within your Carbon Black App Control console for authentication.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API token has the necessary permissions for the actions you intend to use.)*

## Actions

### Find File

Find a file instance on multiple computers based on its hash (SHA-256).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of computers where the file hash was found.

### Unblock Hash

Unblock a hash (SHA-256) on specific policies or globally.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_names` (string, optional): Comma-separated list of policy names to unblock the hash on (e.g., `Default Policy,Local Approval Policy`). If empty, unblocks globally.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unblock operation.

### Analyze File

Analyze a file using a specified connector (e.g., Palo Alto Networks WildFire).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `connector_name` (string, required): The name of the analyzing connector (e.g., Palo Alto Networks).
*   `priority` (string, required): The priority of the analysis (-2 to 2).
*   `timeout` (string, required): Wait timeout in seconds (e.g., 120).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the analysis results from the connector.

### Get Computers By File

Get the computers on which a file with the given SHA-256 value exists.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of computers associated with the file hash.

### Ping

Test connectivity to CB Protection.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get System Info

Get information about a computer based on its hostname or IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed system information for the specified computer(s).

### Block Hash

Block a hash (SHA-256) on specific policies or globally.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_names` (string, optional): Comma-separated list of policy names to block the hash on (e.g., `Default Policy,Local Approval Policy`). If empty, blocks globally.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (SHA-256 only).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block operation.

### Change Computer Policy

Move a computer (identified by Hostname or IP) to a new policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): The new policy name (e.g., Default Policy).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy change operation.

## Notes

*   Ensure the CB Protection integration is properly configured in the SOAR Marketplace tab with the correct Server URL and API Token.
*   The API token requires appropriate permissions within Carbon Black App Control.
*   Hash-based actions (`Find File`, `Block Hash`, `Unblock Hash`, `Analyze File`, `Get Computers By File`) currently support only SHA-256 hashes.
*   Policy names provided in actions must exactly match the names configured in Carbon Black App Control.
