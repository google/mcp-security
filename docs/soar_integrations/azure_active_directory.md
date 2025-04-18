# Azure Active Directory Integration

## Overview

This integration allows you to connect to Azure Active Directory (Azure AD) to manage users and groups. Actions include enabling/disabling accounts, managing group memberships, resetting passwords, revoking sessions, enriching entities, and listing users/groups.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Azure Active Directory application registration details:

*   **Tenant ID:** Your Azure AD tenant identifier.
*   **Client ID:** The Application (client) ID of the registered application in Azure AD.
*   **Client Secret:** The client secret generated for the registered application.
*   **(Optional) API URL/Endpoint:** Sometimes needed if using a specific Azure cloud environment (e.g., Government Cloud), but often defaults to the standard Microsoft Graph API endpoint.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the registered application has the necessary Microsoft Graph API permissions granted for the actions you intend to use, such as `User.ReadWrite.All`, `Group.ReadWrite.All`, `Directory.ReadWrite.All`, etc.)*

## Actions

### Force Password Update

Force password update for user so the user will have to change their password on next login. Action expects Siemplify user entity in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Manager Contact Details

Get manager contact details for user. Action expects Siemplify user entity in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the manager's contact details.

### Disable Account

Disable account in Azure Active Directory. Action expects Siemplify user entity in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove User from a Group

Remove User from the specified group. Note: The user name can be provided either as a Siemplify entity or as an action input parameter. If the user name is passed to action both as an entity and input parameter - action will be executed on the input parameter. User name should be specified in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_name` (string, optional): Specify user name to remove from the target group (username@domain format, comma-separated for multiple).
*   `group_name` (string, optional): Specify group name to remove user from.
*   `group_id` (string, optional): Specify the ID of the group. Takes priority over `group_name`. Example: 00e40000-1971-439d-80fc-d0e000001dbd.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Enrich User

Enrich Siemplify User entity with information from Azure Active Directory. Action expects Siemplify user entity in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fields_to_return` (string, optional): A comma-separated list of fields that you want to return. If empty, returns default fields.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified user(s).

### Enable Account

Enable account in Azure Active Directory. Action expects Siemplify user entity in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Azure Active Directory service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Reset User Password

Change user password to the password specified in the action. User will have to change their password on next login. Action expects User entity (username@domain format) or username parameter. Input parameter takes priority.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `password` (string, required): User Authentication password.
*   `username` (string, optional): User name to change password for (username@domain format, comma-separated for multiple).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Revoke User Session

Revoke user session. Supported entities: Username, Email Address (username that matches email regex).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Groups

List Azure Active Directory groups based on the specified search criteria. Note: Action does not operate on Siemplify entities. Filtering works on the group Name field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `order_by` (List[Any], optional): Specifies the result order (Ascending/Descending). Groups are sorted by display name.
*   `results_limit` (string, optional): Specify max number of groups to return.
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains) for the Name field.
*   `filter_value` (string, optional): Specify the value to filter the Name field by.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of groups matching the criteria.

### List Members in the Group

List members in the specified Azure AD group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `group_name` (string, optional): Specify group name to list members for.
*   `group_id` (string, optional): Specify the ID of the group. Takes priority over `group_name`. Example: 00e40000-1971-439d-80fc-d0e000001dbd.
*   `filter_key` (List[Any], optional): Specify the key to filter group members by.
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains) based on `filter_key`.
*   `filter_value` (string, optional): Specify the value to filter by based on `filter_key`.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of members for the specified group(s).

### Add User To a Group

Add user to a specific Azure AD group. Action expects Siemplify user entity in username@domain format and group id in 00e40000-1971-439d-80fc-d0e000001dbd format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_id` (string, required): Azure AD group ID (e.g., 00e40000-1971-439d-80fc-d0e000001dbd).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Is User In a Group

Check if user has membership in a specific Azure AD group. Action expects Siemplify user entity in username@domain format and group id in 00e40000-1971-439d-80fc-d0e000001dbd format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_id` (string, required): Azure AD group ID (e.g., 00e40000-1971-439d-80fc-d0e000001dbd).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary indicating whether the user(s) are members of the specified group.

### Enrich Host

Enrich Siemplify Host entity with information from Azure Active Directory. Action finds a match for a provided Host entity based on the devices displayName field in Azure AD.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified host(s).

### List User's Groups Membership

List Azure AD groups user is a member of. Note: The user name can be provided either as a Siemplify entity or as an action input parameter. Input parameter takes priority. User name should be specified in username@domain format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_name` (string, optional): Specify user name (username@domain format, comma-separated for multiple).
*   `return_only_security_enabled_groups` (bool, optional): If enabled, only returns security groups.
*   `return_detailed_groups_information` (bool, optional): If enabled, returns detailed group information.
*   `filter_key` (List[Any], optional): Specify the key to filter groups by.
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains) based on `filter_key`.
*   `filter_value` (string, optional): Specify the value to filter by based on `filter_key`.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (username@domain format).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of groups the user(s) are members of.

### List Users

List Azure Active Directory users based on the specified search criteria. Note: Action does not operate on Siemplify entities. Advanced filtering works on the Username (userPrincipalName) field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter` (List[Any], optional): Specifies which fields will be included in the results. Default: all fields.
*   `order_by_field` (List[Any], optional): Specifies the field to order results by.
*   `order_by` (List[Any], optional): Specifies the result order (Ascending/Descending).
*   `results_limit` (string, optional): Specify max number of users to return.
*   `advanced_filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains) for the Username field.
*   `advanced_filter_value` (string, optional): Specify the value to filter the Username field by.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of users matching the criteria.

## Notes

*   Ensure the Azure Active Directory integration is properly configured in the SOAR Marketplace tab with the correct Tenant ID, Client ID, and Client Secret.
*   The registered Azure AD application requires appropriate Microsoft Graph API permissions for the actions used.
*   Many actions support targeting users via User Principal Name (UPN) in `username@domain` format or by Azure AD User ID. Check individual action descriptions for supported entity types and formats.
*   When both entity scope and specific identifiers (like `user_name` or `group_id`) are provided, the specific identifiers usually take precedence.
