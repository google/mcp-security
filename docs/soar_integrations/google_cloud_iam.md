# Google Cloud IAM

## Overview

This integration provides tools to interact with Google Cloud Identity and Access Management (IAM) for managing service accounts, roles, and policies.

## Available Tools

### Enable Service Account

**Tool Name:** `google_cloud_iam_enable_service_account`

**Description:** Enable service account. Supported entities: Username, Deployment. Note: the supported formats for entities are IAM service account email and resource name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Service Account

**Tool Name:** `google_cloud_iam_create_service_account`

**Description:** Create a Google Cloud IAM Service Account.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `service_account_id` (string, required): Specify service account id to create.
*   `project_id` (string, optional): Specify the name of the project to create service accounts in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `service_account_display_name` (string, optional): Specify service account display name to create. Defaults to None.
*   `service_account_description` (string, optional): Specify service account description to create. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Service Account IAM Policy

**Tool Name:** `google_cloud_iam_get_service_account_iam_policy`

**Description:** Gets the access control policy for the service account. Supported entities: Username, Deployment. Note: the supported formats for entities are IAM service account email and resource name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_iam_ping`

**Description:** Test connectivity to the Google Cloud IAM service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Role

**Tool Name:** `google_cloud_iam_create_role`

**Description:** Create a Google Cloud IAM Role.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `role_id` (string, required): Specify role id for newly created IAM role.
*   `role_definition` (string, required): Specify JSON policy document to use as the role definition.
*   `project_id` (string, optional): Specify the name of the project, where you want to create the role. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Role

**Tool Name:** `google_cloud_iam_delete_role`

**Description:** Delete a Google Cloud IAM Role.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `role_id` (string, required): Specify role id for newly created IAM role.
*   `project_id` (string, optional): Specify the name of the project, where you want to delete the role. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `google_cloud_iam_enrich_entities`

**Description:** Enrich Siemplify User entities with service accounts information from Google Cloud IAM. Supported entities: Username, Deployment. Note: the supported formats for entities are IAM service account email and resource name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Disable Service Account

**Tool Name:** `google_cloud_iam_disable_service_account`

**Description:** Disable service account. Supported entities: Username, Deployment. Note: the supported formats for entities are IAM service account email and resource name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Service Account

**Tool Name:** `google_cloud_iam_delete_service_account`

**Description:** Delete service account. Supported entities: Username, Deployment. Note: the supported formats for entities are IAM service account email and resource name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Roles

**Tool Name:** `google_cloud_iam_list_roles`

**Description:** List Google Cloud IAM roles based on the specified search criteria. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_id` (string, optional): Specify the name of the project, where you want to list the roles. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `view` (List[Any], optional): Specify which view should be used to return role information. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many roles the action should return. Defaults to None.
*   `list_custom_roles_only` (boolean, optional): If enabled, action will return only custom roles defined for the current project or orgranization. Defaults to None.
*   `show_deleted` (boolean, optional): If enabled, action will also return deleted roles. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Service Accounts

**Tool Name:** `google_cloud_iam_list_service_accounts`

**Description:** List service accounts available in Google Cloud IAM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_id` (string, optional): Specify the name of the project to list service accounts in. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `service_account_display_name` (string, optional): Specify service account display name to return. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `service_account_email` (string, optional): Specify service account email to return. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `max_rows_to_return` (string, optional): Specify how many service accounts the action should return. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Set Service Account IAM Policy

**Tool Name:** `google_cloud_iam_set_service_account_iam_policy`

**Description:** Sets the access control policy on the specified service account. Supported entities: Username, Deployment. Note: the supported formats for entities are IAM service account email and resource name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy` (string, required): Specify JSON policy document to set for service account.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
