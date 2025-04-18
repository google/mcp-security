# Okta Integration

## Overview

This integration allows you to connect to Okta to manage users, groups, roles, identity providers, and perform various administrative actions via the Okta API.

## Configuration

The configuration for this integration (Okta Domain URL, API Token, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### List Providers

List identity providers (IdPs) in your organization.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, optional): Search the name property for a match.
*   `type` (string, optional): Filter by IdP type.
*   `limit` (string, optional): Max amount of results to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of identity providers.

### Assign Role

Assign a role to a user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `role_types` (string, required): The type of role to assign to the users.
*   `user_i_ds` (string, optional): IDs of users in Okta (comma-separated).
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the role assignment.

### Unassign Role

Unassign a role from a user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `role_i_ds_or_names` (string, required): IDs or names of roles in Okta (comma-separated).
*   `user_i_ds` (string, optional): IDs of users in Okta (comma-separated).
*   `is_id` (bool, optional): Whether the `role_ids_or_names` parameter contains IDs (true) or names (false/omitted).
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the role unassignment.

### Disable User

Disables the specified user (suspend or deactivate).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_i_ds_or_logins` (string, optional): IDs or logins (email/shortname) of users in Okta (comma-separated).
*   `is_deactivate` (bool, optional): Whether to deactivate (true) or only suspend (false/omitted) the user.
*   `send_email_if_deactivate` (bool, optional): Whether to send an email after deactivating.
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs/Logins.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID or login).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the disable operation.

### Get User

Get information about a user by ID or login.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_ids_or_logins` (string, optional): IDs or logins (email/shortname) of users in Okta (comma-separated).
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs/Logins.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID or login).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the user details.

### Ping

Test Connection With Okta.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### List User Groups

Get the groups that the user is a member of.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_i_ds_or_logins` (string, optional): IDs or logins of users in Okta (comma-separated).
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs/Logins.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID or login).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of groups the user belongs to.

### Get Group

Get information about a group by ID or name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_ids_or_names` (string, required): IDs or names of groups in Okta (comma-separated).
*   `is_id` (bool, optional): Whether the `group_ids_or_names` parameter contains IDs (true) or names (false/omitted).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the group details.

### Add Group

Add a group in Okta.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_name` (string, required): The name of the group in Okta.
*   `group_description` (string, optional): The description for the group.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the group creation, likely including the new group ID.

### Reset Password

Generate a one-time token that can be used to reset a user's password.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_i_ds_or_logins` (string, optional): IDs or logins of users in Okta (comma-separated).
*   `send_email` (bool, optional): Whether to send an email for the password reset (true) or return the token (false/omitted).
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs/Logins.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID or login).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result, potentially including the reset token if `send_email` is false.

### List Roles

Lists all roles assigned to a user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_i_ds` (string, optional): IDs of users in Okta (comma-separated).
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of roles assigned to the user(s).

### Enable User

Enables the specified user (unsuspend or activate).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_i_ds_or_logins` (string, optional): IDs or logins of users in Okta (comma-separated).
*   `is_activate` (bool, optional): Whether to activate (true) the user or just unsuspend (false/omitted).
*   `send_email_if_activate` (bool, optional): Whether to send an email after activating.
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs/Logins.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID or login).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the enable operation.

### Set Password

Set the password of a user without validating existing credentials.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `new_password` (string, required): The new password.
*   `user_i_ds_or_logins` (string, optional): IDs or logins of users in Okta (comma-separated).
*   `add_10_random_chars` (bool, optional): Whether to add extra random characters to the password.
*   `also_run_on_scope` (bool, optional): Whether to run on entities as well as the input User IDs/Logins.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities (expects ID or login).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the password set operation.

### List Users

Get the list of users based on search criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, optional): Search for a match in firstname, lastname, or email.
*   `filter` (string, optional): Custom search query for a subset of properties.
*   `search` (string, optional): Custom search query for most properties.
*   `limit` (string, optional): Max amount of results to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of users matching the criteria.

## Notes

*   Ensure the Okta integration is properly configured in the SOAR Marketplace tab with the correct Okta domain and API token.
*   Many actions support targeting users via ID or login (email/shortname). Check the `also_run_on_scope` parameter to control whether the action runs on entities from the scope in addition to explicitly provided IDs/logins.
*   Role and Group actions can often target by ID or Name; use the `is_id` parameter where applicable to specify the identifier type.
