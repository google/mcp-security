# Jira

## Overview

This integration provides tools to interact with Jira, allowing you to manage issues, users, attachments, and more within your Jira instance.

## Available Tools

### Assign Issue

**Tool Name:** `jira_assign_issue`

**Description:** Assign an issue to a specific user. (Jira username could be: name, mail, etc...). For new Jira Api, action will try to find a match for the assignee to assign an issue based on User email or displayName field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_key` (string, required): The issue key of the issue
*   `assignee` (string, required): The new assignee of the issue. Assignee can be jira username.
*   `jira_username` (Optional[str], optional): The Jira username of the initiator of the action. Note: If a username is not provided, action will not create a comment in the issue. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Upload Attachment

**Tool Name:** `jira_upload_attachment`

**Description:** Add an attachment to an issue.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_key` (string, required): The key of the issue
*   `file_paths` (string, required): The paths of the files to upload, comma separated
*   `mode` (Optional[List[Any]], optional): Specify the mode for the action. If "Add New Attachment" is selected, action will add a new attachment, if it even has the same name. If "Overwrite Existing Attachment" is selected, action will remove other attachments with the same name and add a new attachment. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Issues

**Tool Name:** `jira_get_issues`

**Description:** Get issues details by keys. (separated by comma)

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_keys` (string, required): The keys of the issues to fetch. separated by comma
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Issues

**Tool Name:** `jira_list_issues`

**Description:** Search for issues

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_names` (Optional[str], optional): The names of the projects to search in, comma separated. Defaults to None.
*   `summary` (Optional[str], optional): The summary to filter by. Defaults to None.
*   `description` (Optional[str], optional): The description to filter by. Defaults to None.
*   `issue_types` (Optional[str], optional): The issue types to filter by. Defaults to None.
*   `priorities` (Optional[str], optional): The priority to filter by. Defaults to None.
*   `created_from` (Optional[str], optional): The earliest creation date to filter by. Format: YYYY/MM/DD. If not provided, filter will not be used. Defaults to None.
*   `updated_from` (Optional[str], optional): The earliest update date to filter by. Format: YYYY/MM/DD. If not provided, filter will not be used. Defaults to None.
*   `assignees` (Optional[str], optional): The name of the assignees to filter by, comma separated. Defaults to None.
*   `reporter` (Optional[str], optional): The name of the reporters to filter by, comma separated. Defaults to None.
*   `statuses` (Optional[str], optional): The statuses to filter by, comma separated. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `jira_ping`

**Description:** Test Connectivity

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Comment

**Tool Name:** `jira_add_comment`

**Description:** Add a comment to a issue

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_key` (string, required): The issue key of the issue, i.e: ABC-123
*   `comment` (string, required): The comment content to add to the issue
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Issue

**Tool Name:** `jira_update_issue`

**Description:** Update an issue. For new Jira Api, action will try to find a match for the assignee to assign an issue based on User email or displayName field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_key` (string, required): The key of the issue to update
*   `status` (Optional[str], optional): Specify the relevant transition name, to transition this issue to the new desired status. Defaults to None.
*   `summary` (Optional[str], optional): The new summary of the issue. Defaults to None.
*   `description` (Optional[str], optional): The new description of the issue. Defaults to None.
*   `issue_type` (Optional[str], optional): The new type of the issue. Defaults to None.
*   `jira_username` (Optional[str], optional): The JIRA username of the action initiator. Note: If a username is not provided, action will not create a comment in the issue. Defaults to None.
*   `assignee` (Optional[str], optional): The new assignee of the issue. Defaults to None.
*   `components` (Optional[str], optional): The Components field of the issue. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `labels` (Optional[str], optional): The Labels field of the issue. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `custom_fields` (Optional[str], optional): Specify a JSON object containing all of the fields and values that will be updated for the issue. Note: this parameter has priority and all of the fields will be overwritten with the value that is provided for this parameter. Example: {"field":"value"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Download Attachments

**Tool Name:** `jira_download_attachments`

**Description:** Get an Issue key and download all attachments. If one of them is an EML file, download inside attachments as well

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_key` (string, required): The key of the issue
*   `download_path` (Optional[str], optional): Specify the path for the downloaded file. Note: if parameter 'Download Attachments to the Case Wall' is enabled, then this parameter is not mandatory. Defaults to None.
*   `download_attachments_to_the_case_wall` (Optional[bool], optional): If enabled, action download Jira issue attachmnets to the current Siemplify alert case wall. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Link Issues

**Tool Name:** `jira_link_issues`

**Description:** Link multiple issues in Jira.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `inward_issue_id` (string, required): Specify the inward issue id. For example, if the relation type is “Blocks”, then in the UI you would see this issue with relation "blocks".
*   `outward_issue_i_ds` (string, required): Specify a comma-separated list of outward issue ids. For example, if the relation type is “Blocks”, then in the UI you would see this issue with relation "blocked by".
*   `relation_type` (string, required): Specify the relation type that will be used to link multiple issues. A list of all available relation types are available in the action "List Relation Types".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Search Users

**Tool Name:** `jira_search_users`

**Description:** Search users in Jira. Note: Providing User Email Addresses will result in more accurate results.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `user_email_addresses` (Optional[str], optional): Specify a comma-separated list of email addresses for which you want to return the users. Defaults to None.
*   `user_names` (Optional[str], optional): Specify a comma-separated list of user display names for which you want to return the users. Defaults to None.
*   `project` (Optional[str], optional): Specify the name of the project in which you need to search for the email addresses. If provided, only Project Assignable Users will be returned. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Issue

**Tool Name:** `jira_create_issue`

**Description:** Create an issue in a project. (Jira username could be: name, mail, etc...). For new Jira Api, action will try to find a match for the assignee to assign an issue based on User email or displayName field.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_key` (string, required): The key of the project to create an issue in
*   `summary` (string, required): The summary of the issue
*   `issue_type` (string, required): The type of the issue
*   `description` (Optional[str], optional): The description of the issue. Defaults to None.
*   `jira_username` (Optional[str], optional): The Jira username of the initiator of the action. Note: If a username is not provided, action will not create a comment in the issue. Defaults to None.
*   `assignee` (Optional[str], optional): The new assignee of the issue. Defaults to None.
*   `components` (Optional[str], optional): The Components field of the issue. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `labels` (Optional[str], optional): The Labels field of the issue. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `custom_fields` (Optional[str], optional): Specify a JSON object containing all of the fields and values that will be used during issue creation. Note: this parameter has priority and all of the fields will be overwritten with the value that is provided for this parameter. Example: {"field":"value"}. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Relation Types

**Tool Name:** `jira_list_relation_types`

**Description:** List available relation types in Jira.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (Optional[List[Any]], optional): Specify the key that needs to be used to filter {item type}. Defaults to None.
*   `filter_logic` (Optional[List[Any]], optional): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `filter_value` (Optional[str], optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `max_records_to_return` (Optional[str], optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Issue

**Tool Name:** `jira_delete_issue`

**Description:** Delete an issue

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_key` (string, required): The key of the issue to delete
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Alert Issue

**Tool Name:** `jira_create_alert_issue`

**Description:** Create an alert issue

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `project_key` (string, required): The key of the project to create the issue in
*   `summary` (string, required): The summary of the issue
*   `issue_type` (string, required): The type of the issue
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
