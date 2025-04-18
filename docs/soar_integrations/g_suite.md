# Google Workspace (G Suite)

## Overview

This integration provides tools to interact with Google Workspace (formerly G Suite) for managing users, groups, organizational units (OUs), and related settings via the Admin SDK Directory API.

## Available Tools

### Create OU

**Tool Name:** `g_suite_create_ou`

**Description:** Create a new organizational unit.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, required): The unique ID for the customer's G Suite account, 'my_customer' alias can also be used to represent your account's customerId.
*   `parent_ou_path` (string, required): The full path to the organizational unit's parent OU.
*   `name` (string, optional): Display name of the new OU. Defaults to None.
*   `description` (string, optional): Description of the new OU. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Revoke User Session

**Tool Name:** `g_suite_revoke_user_session`

**Description:** Use the Revoke User Sessions action to revoke the user web and device sessions and reset their sign-in cookies using Google Workspace. This action runs on the Google SecOps User entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_email_addresses` (string, optional): A comma-separated list of users to sign out. The action runs the values from this parameter with User entities. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update User

**Tool Name:** `g_suite_update_user`

**Description:** Update a Google Workspace Directory user. Note: action is not working on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email_address` (string, required): A comma-separated list of primary email addresses that will be used to identify users that need to be updated.
*   `change_password_at_next_login` (boolean, required): Whether to force the user to change his password on next login.
*   `given_name` (string, optional): The user's first name. Defaults to None.
*   `family_name` (string, optional): The user's last name. Defaults to None.
*   `password` (string, optional): The password of the user. Defaults to None.
*   `phone` (string, optional): The phone number of the user. Defaults to None.
*   `gender` (string, optional): The gender of the user. Valid values: female, male, other, unknown. Defaults to None.
*   `department` (string, optional): The name of the department of the user. Defaults to None.
*   `organization` (string, optional): The name of the organization of the user. Defaults to None.
*   `user_status` (List[Any], optional): Specify if user status should be updated to blocked or unblocked. By default action is no changing the user status. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List OU Of Account

**Tool Name:** `g_suite_list_ou_of_account`

**Description:** List the organizational units of an account.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, required): The unique ID for the customer's G Suite account, 'my_customer' alias can also be used to represent your account's customerId.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Members From Group

**Tool Name:** `g_suite_remove_members_from_group`

**Description:** Remove members from a group. Action runs on Google SecOps User entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_email_address` (string, required): Email of the group to remove the members from.
*   `user_email_addresses` (string, optional): A comma-separated list of users that you want to remove from the group. Note: values from this parameter will be executed alongside User Entities. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Group Members

**Tool Name:** `g_suite_list_group_members`

**Description:** List the members of a group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_email_address` (string, required): Email address of the group.
*   `include_derived_membership` (boolean, required): Whether to list indirect memberships.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Group

**Tool Name:** `g_suite_delete_group`

**Description:** Delete a Google Workspace Directory Group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_email_address` (string, required): Email of the group to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete OU

**Tool Name:** `g_suite_delete_ou`

**Description:** Delete an organizational unit.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, required): The unique ID for the customer's G Suite account, 'my_customer' alias can also be used to represent your account's customerId.
*   `ou_path` (string, required): The full path to the organizational unit. If organizational unit is located under root (/) path, provide just organizational unit name, without path.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Group

**Tool Name:** `g_suite_create_group`

**Description:** Create a new group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email_address` (string, required): Email address of the new group.
*   `name` (string, optional): Display name of the new group. Defaults to None.
*   `description` (string, optional): Description of the new group. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `g_suite_ping`

**Description:** Test connectivity to Google Workspace.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete User

**Tool Name:** `g_suite_delete_user`

**Description:** Delete a user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email_address` (string, required): The email address of the user to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Members To Group

**Tool Name:** `g_suite_add_members_to_group`

**Description:** Add members to a group. Action runs on Google SecOps User entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_email_address` (string, required): Email of the group to add the members to.
*   `user_email_addresses` (string, optional): A comma-separated list of users that you want to add to the group. Note: values from this parameter will be executed alongside User Entities. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `g_suite_enrich_entities`

**Description:** Enrich Google SecOps User entities with information from Google Workspace.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update OU

**Tool Name:** `g_suite_update_ou`

**Description:** Update an organizational unit.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, required): The unique ID for the customer's G Suite account, 'my_customer' alias can also be used to represent your account's customerId.
*   `ou_path` (string, required): The full path to the organizational unit. If organizational unit is located under root (/) path, provide just organizational unit name, without path.
*   `name` (string, optional): Display name of the OU. Defaults to None.
*   `description` (string, optional): Description of the OU. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List User Privileges

**Tool Name:** `g_suite_list_user_privileges`

**Description:** List roles and privileges related to the user using Google Workspace. Supported entities: User.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_roles_to_return` (string, required): Specify how many roles related to the user to return.
*   `max_privileges_to_return` (string, required): Specify how many privileges related to the user to return.
*   `user_email_addresses` (string, optional): A comma-separated list of users that you want to check privileges for. Note: values from this parameter will be executed alongside User Entities. Defaults to None.
*   `check_roles` (string, optional): Specify a comma-separated list of roles that you want to check in relation to the user. Defaults to None.
*   `check_privileges` (string, optional): Specify a comma-separated list of permission that you want to check in relation to the user. Note: "Expand Privileges" needs to be enabled for this parameter to work. If there are values inside the "Check Roles" parameter, action will check the privileges only among those roles. Defaults to None.
*   `include_inherited_roles` (boolean, optional): If enabled, action will additionally return user roles that were inherited from groups. Defaults to None.
*   `expand_privileges` (boolean, optional): If enabled, action will return information about all of the unique privileges related to the user. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create User

**Tool Name:** `g_suite_create_user`

**Description:** Create a new user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `given_name` (string, required): The user's first name.
*   `family_name` (string, required): The user's last name.
*   `password` (string, required): The password of the new user.
*   `email_address` (string, required): The user's primary email address.
*   `change_password_at_next_login` (boolean, required): Whether to force the user to change his password on next login.
*   `phone` (string, optional): The phone number of the user. Defaults to None.
*   `gender` (string, optional): The gender of the user. Valid values: female, male, other, unknown. Defaults to None.
*   `department` (string, optional): The name of the department of the user. Defaults to None.
*   `organization` (string, optional): The name of the organization of the user. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Group Details

**Tool Name:** `g_suite_get_group_details`

**Description:** Retrieve information about a group using Google Workspace.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_email_addresses` (string, required): A comma-separated list of group emails that you want to examine.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Group Privileges

**Tool Name:** `g_suite_list_group_privileges`

**Description:** List roles and privileges related to the group using Google Workspace.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_email_addresses` (string, required): A comma-separated list of groups that you want to examine.
*   `max_roles_to_return` (string, required): Specify how many roles related to the group to return.
*   `max_privileges_to_return` (string, required): Specify how many privileges related to the group to return.
*   `check_roles` (string, optional): Specify a comma-separated list of roles that you want to check in relation to the group. Defaults to None.
*   `check_privileges` (string, optional): Specify a comma-separated list of permission that you want to check in relation to the group. Note: "Expand Privileges" needs to be enabled for this parameter to work. If there are values inside the "Check Roles" parameter, action will check the privileges only among those roles. Defaults to None.
*   `expand_privileges` (boolean, optional): If enabled, action will return information about all of the unique privileges related to the group. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Users

**Tool Name:** `g_suite_list_users`

**Description:** List users present in account.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `customer_id` (string, optional): The unique ID for the customer's G Suite account, 'my_customer' alias can also be used to represent your account's customerId. Defaults to None.
*   `domain` (string, optional): Specify a domain to search for users in. Defaults to None.
*   `manager_email` (string, optional): The email address of a user's direct manager. Defaults to None.
*   `return_only_admin_accounts` (boolean, optional): Specify whether to return only admin accounts. Defaults to None.
*   `return_only_delegated_admin_accounts` (boolean, optional): Specify whether to return only delegated admin accounts. Defaults to None.
*   `return_only_suspended_users` (boolean, optional): Specify whether to return only suspended accounts. Defaults to None.
*   `org_unit_path` (string, optional): The full path of an org unit to retrieve users from. This matches all org unit chains under the target. Defaults to None.
*   `department` (string, optional): The department within the organization to retrieve users from. Defaults to None.
*   `record_limit` (string, optional): Specify how many records can be returned by the action. Defaults to None.
*   `custom_query_parameter` (string, optional): Optional. Specify custom query parameter you want to add to the list users search call. For example, orgName='Human Resources'. For reference on which fields can be used see https://developers.google.com/admin-sdk/directory/v1/guides/search-users#fields. Note: when providing the 'Custom Query Parameter', make sure that you are not providing 'email' field alongside 'Email Addresses' parameter as the generated query will not work. Defaults to None.
*   `return_only_users_without_2fa` (boolean, optional): If enabled, action will only return users that don't have 2fa enabled. Defaults to None.
*   `email_addresses` (string, optional): Specify a comma-separated list of email addresses that need to be searched for. Note: if 'Email Addresses' parameter is used, then 'Record Limit' parameter is ignored. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
