# AWSS3 SOAR Integration

This document details the tools provided by the AWSS3 SOAR integration.

## Tools

### `awss3_list_bucket_objects`

List objects in the bucket from AWS S3.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `bucket_name` (str, required): Specify name of the bucket from which to retrieve objects.
*   `max_objects_to_return` (Optional[str], optional, default=None): Specify how many objects to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awss3_ping`

Test connectivity to AWS S3 with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awss3_list_buckets`

Retrieve a list of buckets from AWS S3.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awss3_set_bucket_policy`

Set a policy in the bucket from AWS S3.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `bucket_name` (str, required): Specify the name of the bucket on which you want to update the policy.
*   `policy_json_object` (Union[str, dict], required): Specify the JSON object of the policy that you want to set for the bucket. Examples can be found here: https://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awss3_download_file_from_bucket`

Download file from bucket in AWS S3.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `bucket_file_path` (str, required): Specify the path of the file in the bucket. Example: s3://siemplify/syslog/log.txt
*   `download_path` (str, required): Specify the absolute path, where to download the file. Example: /folder_1/folder_2/filename
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awss3_upload_file_to_bucket`

Upload file to bucket in AWS S3.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_path` (str, required): Specify the absolute path to the file that needs to be uploaded. Example: /folder_1/folder_2/filename
*   `bucket_upload_path` (str, required): Specify the path in the bucket to where the path should be uploaded. Example: s3://siemplify/syslog/log.txt
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `awss3_get_bucket_policy`

Retrieve information about the bucket policy from AWS S3.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `bucket_name` (str, required): Specify name of the bucket from which to retrieve policy information.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
