# Google Cloud Storage

## Overview

This integration provides tools to interact with Google Cloud Storage for managing buckets, objects, and access control lists (ACLs).

## Available Tools

### Download an Object From a Bucket

**Tool Name:** `google_cloud_storage_download_an_object_from_a_bucket`

**Description:** Download an object from a Cloud Storage bucket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `bucket_name` (string, required): Specify the name of the bucket in which the object resides.
*   `object_name` (string, required): Specify the name of the object in the bucket to download. Please note, for objects which are stored inside folders in the bucket, you should also specify the inner folder. E.g: folder/object_name.
*   `download_path` (string, required): Specify the absolute path, where to download the file. Example: /folder_1/folder_2.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Bucket Objects

**Tool Name:** `google_cloud_storage_list_bucket_objects`

**Description:** List objects stored in the Cloud Storage bucket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `bucket_name` (string, required): Specify name of the bucket from which to retrieve objects.
*   `max_objects_to_return` (string, optional): Specify how many objects to return. Defaults to None.
*   `retrieves_the_access_control_list_of_an_object` (boolean, optional): If checked, retrieve the Access Control List of an object. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Upload an Object To a Bucket

**Tool Name:** `google_cloud_storage_upload_an_object_to_a_bucket`

**Description:** Upload an object to a Cloud Storage bucket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `bucket_name` (string, required): Specify the name of the bucket in which to upload the object.
*   `source_file_path` (string, required): Specify the absolute path to the file that needs to be uploaded. Example: /loca/path/to/filename.
*   `object_name` (string, required): Specify the name of the uploaded object within the bucket.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get a Bucket’s Access Control List

**Tool Name:** `google_cloud_storage_get_a_buckets_access_control_list`

**Description:** Retrieve the access control list (ACL) for a Cloud Storage bucket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `bucket_name` (string, required): Specify name of the bucket from which to retrieve Access Control list. Comma separated names.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_storage_ping`

**Description:** Test connectivity to Google Cloud Storage with parameters provided at the integration configuration page on Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update an ACL entry on Bucket

**Tool Name:** `google_cloud_storage_update_an_acl_entry_on_bucket`

**Description:** Updates an ACL entry on the specified bucket.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `bucket_name` (string, required): Specify the name of the bucket on which you want to modify the Access Control List.
*   `entity` (string, required): The entity holding the permission. Can be user-userId, user-emailAddress, group-groupId, group-emailAddress, allUsers, or allAuthenticatedUsers. For more information, please see this reference: https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls#resource.
*   `role` (List[Any], required): The access permission for the entity. Possible values: “OWNER”, ”READER”, “WRITER”.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Buckets

**Tool Name:** `google_cloud_storage_list_buckets`

**Description:** Retrieve a list of buckets from Google Cloud Storage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_results` (string, optional): Maximum number of buckets to return. Defaults to None.
*   `project_id` (string, optional): Specify the name of the project, from where you want to retrieve a list of buckets. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Public Access From Bucket

**Tool Name:** `google_cloud_storage_remove_public_access_from_bucket`

**Description:** Remove the public access from the bucket using Google Cloud Storage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_name` (string, required): Specify the name of the bucket on which you want to modify the Access Control List.
*   `prevent_public_access_from_bucket` (boolean, required): If enabled, action will also configure the bucket in a way that will prevent possible public access.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
