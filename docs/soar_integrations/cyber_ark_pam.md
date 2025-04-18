# CyberArk PAM Integration

## Overview

This integration allows interaction with CyberArk Privileged Access Management (PAM) to list accounts and retrieve account password values.

## Configuration

To configure this integration within the SOAR platform, you typically need the following CyberArk PAM details:

*   **API URL:** The base URL of your CyberArk PAM PVWA (Password Vault Web Access) API endpoint (e.g., `https://yourpvwa.example.com/PasswordVault`).
*   **Username:** A username configured in CyberArk PAM with the necessary API permissions.
*   **Password:** The password for the API user.
*   **(Optional) Authentication Method:** Specify the authentication method (e.g., `CyberArk`, `LDAP`, `Windows`). Defaults usually to `CyberArk`.
*   **(Optional) Verify SSL:** Whether to verify the PVWA server's SSL certificate.
*   **(Optional) CA Certificate File:** Path to a CA certificate file for SSL verification if using a self-signed or private CA.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has permissions to list accounts and retrieve passwords via the API.)*

## Actions

### List Accounts

List accounts available in the CyberArk PAM based on provided criteria. Note: This action doesn’t run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_query` (string, optional): Specify the search query to use (e.g., username, address).
*   `search_operator` (List[Any], optional): Specify the search operator (e.g., `contains`, `equals`).
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `records_offset` (string, optional): Specify the offset for pagination.
*   `filter_query` (string, optional): Specify a filter query (e.g., `safeName eq MySafe`, `modificationTime ge 1678886400`).
*   `saved_filter` (string, optional): Specify a saved filter name. Takes priority over `filter_query`.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of accounts matching the criteria.

### Ping

Test connectivity to the CyberArk PAM installation with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Account Password Value

Get account password value (or SSH Key) from CyberArk PAM. Note: This action doesn’t run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `account` (string, required): Specify the account ID (e.g., `12_3`) to retrieve the password value for. Get the ID from the `List Accounts` action.
*   `reason` (string, required): Specify the reason that account password value is accessed.
*   `ticketing_system_name` (string, optional): Specify the name of the ticketing system (if applicable for auditing).
*   `ticket_id` (string, optional): Specify the ticketing system ticket ID (if applicable for auditing).
*   `version` (string, optional): Specify the account password version to retrieve.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the retrieved password or SSH key value.

## Notes

*   Ensure the CyberArk PAM integration is properly configured in the SOAR Marketplace tab with the correct API URL and credentials.
*   The API user requires appropriate permissions in CyberArk PAM, including rights to list accounts and retrieve passwords (potentially requiring specific safe memberships and permissions).
*   Retrieving passwords often requires providing a reason for auditing purposes.
*   Account IDs used in `Get Account Password Value` are typically obtained from the output of the `List Accounts` action.
