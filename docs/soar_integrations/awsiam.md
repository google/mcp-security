# AWSIAM SOAR Integration

This document details the tools provided by the AWSIAM SOAR integration.

## Tools

### `awsiam_list_policies`

List all the managed policies that are available in your AWS account, including your own customer-defined managed policies and all AWS managed policies. You can filter the list of policies that are returned using the optional Only Attached, Scope, and Policy Usage parameters. For example, to list only the customer managed policies in your AWS account, set Scope to Local. To list only AWS managed policies, set Scope to AWS.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `only_attached` (Optional[bool], optional, default=None): When checked, filtering the results to only the policies that are attached to an IAM user, group or role. When unchecked, all policies will be returned.
*   `max_policies_to_return` (Optional[str], optional, default=None): Specify how many policies to return. Default is 100. Maximum is 1000.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_remove_a_user_from_a_group`

Removes the specified user from the specified IAM group. Use groups to apply the same permissions policies across multiple users at once.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_name` (str, required): The name of the group to update. Note: Group names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-.
*   `user_name` (str, required): The name of the user to remove. Note: User names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-. Comma separated values.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_create_a_group`

Create a new IAM group for your AWS account. To set up a group, you need to create the group. Then give the group permissions based on the type of work that you expect the users in the group to do. Finally, add users to the group.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_name` (str, required): Name of the group to create. Comma separated values. Note: Group names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-. Names must be unique within an account.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_ping`

Test connectivity to AWS IAM with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_list_users`

Get a list of all users in the IAM.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_users_to_return` (Optional[str], optional, default=None): Specify how many users to return. Maximum is 1000 users. Default is 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_attach_a_policy`

Attach the specified managed policy to an identity (user, group, role).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `identity_type` (List[Any], required): IAM Identity type.
*   `identity_name` (str, required): The name (friendly name, not ARN) of the identity to attach the policy to. Identity names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-.
*   `policy_name` (str, required): The name (friendly name, not ARN) of the policy to attach the policy to. Policy names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_add_a_user_to_a_group`

Adds the specified user to the specified IAM group. Use groups to apply the same permissions policies across multiple users at once.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_name` (str, required): The name of the group to update. Note: Group names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-.
*   `user_name` (str, required): The name of the user to add. Note: User names can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-. Comma separated values.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_create_a_policy`

Create an IAM customer managed policy for your AWS account. This action creates a policy version with a version identifier of v1and sets v1 as the policy's default version.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `policy_name` (str, required): Name of the policy to create. Policy name can not include spaces and must contain only alphanumeric characters and/or the following: +=.@_-. Policy names must be unique within an account.
*   `policy_document` (str, required): The JSON policy document that you want to use as the content for the new policy.
*   `description` (Optional[str], optional, default=None): Description of the policy.Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awsiam_disable_user_access`

Disable User Access in AWS by adding an explicit deny inline policy. Action works with SOAR User entity type.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
