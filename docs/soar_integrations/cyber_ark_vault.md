# CyberArk Vault Integration

## Overview

This integration allows interaction with CyberArk Vault to manage user accounts. Actions include enabling/disabling users, retrieving user details, and getting group details.

## Configuration

To configure this integration within the SOAR platform, you typically need the following CyberArk Vault details:

*   **API URL:** The base URL of your CyberArk PAM PVWA (Password Vault Web Access) API endpoint (e.g., `https://yourpvwa.example.com/PasswordVault`). This is often the same URL used for the CyberArk PAM integration.
*   **Username:** A username configured in CyberArk Vault with the necessary API permissions (typically administrative rights for user management).
*   **Password:** The password for the API user.
*   **(Optional) Authentication Method:** Specify the authentication method (e.g., `CyberArk`, `LDAP`, `Windows`). Defaults usually to `CyberArk`.
*   **(Optional) Verify SSL:** Whether to verify the PVWA server's SSL certificate.
*   **(Optional) CA Certificate File:** Path to a CA certificate file for SSL verification if using a self-signed or private CA.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has permissions to manage users and groups via the API.)*

## Actions

### Disable User

Update user attribute - disable user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_name` (string, required): Full user name as it exists in the CyberArk Vault.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the disable user operation.

### Ping

Test Connectivity to CyberArk Vault.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get User Details

Get user details from CyberArk Vault.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_name` (string, required): Full user name as it exists in the CyberArk Vault.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified user.

### Enable User

Update user attribute - enable user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_name` (string, required): Full user name as it exists in the CyberArk Vault.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the enable user operation.

### Get Group Details

Get group details from CyberArk Vault.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): Full group name as it exists in the CyberArk Vault.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified group.

## Notes

*   Ensure the CyberArk Vault integration is properly configured in the SOAR Marketplace tab with the correct API URL and credentials.
*   The API user requires appropriate permissions in CyberArk Vault for user and group management.
*   Usernames and group names must match exactly how they appear in CyberArk Vault.
