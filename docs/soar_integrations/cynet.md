# Cynet 360 Integration

## Overview

This integration allows interaction with the Cynet 360 platform to perform endpoint remediation actions, retrieve file information, and check remediation status.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cynet 360 details:

*   **Server Address:** The URL of your Cynet 360 console (e.g., `https://mycompany.cynet.com`).
*   **Port:** The port for the Cynet API (usually 443).
*   **Username:** The username for an API user account.
*   **Password:** The password for the API user account.
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has the necessary permissions for the desired API operations, such as remediation actions and file queries.)*

## Actions

### Quarantine Hash In Hosts

Quarantine file remediation action based on file hash.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the quarantine action, likely including a remediation task ID.

### Hash Query

Retrieve all information about a specific file based on its hash.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the file associated with the hash.

### Remediation Status

Get remediation status based on remediation ID obtained from other Cynet actions (like Quarantine Hash In Hosts).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `remediation_id` (string, required): The remediation task ID (e.g., `312`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the status details of the specified remediation task.

### Ping

Test Connectivity to Cynet 360.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Kill Hash In Hosts

Kill process file remediation action based on file hash.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the kill process action, likely including a remediation task ID.

### Delete Hash In Hosts

Delete file remediation action based on file hash.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the delete file action, likely including a remediation task ID.

## Notes

*   Ensure the Cynet integration is properly configured in the SOAR Marketplace tab with the correct Server Address, Port, Username, and Password.
*   The API user requires appropriate permissions within Cynet 360 for remediation and query actions.
*   Remediation actions (Quarantine, Kill, Delete) target files based on their hash across hosts where the file is found.
*   Use the `Remediation Status` action with the ID returned by remediation actions to check if the task completed successfully.
