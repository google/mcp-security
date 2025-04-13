# AWS GuardDuty SOAR Integration

This document details the tools provided by the AWS GuardDuty SOAR integration.

## Tools

### `aws_guard_duty_get_detector_details`

Retrieve an Amazon GuardDuty detector specified by the detector ID.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): The unique ID of the detector that you want to retrieve. Comma separated values
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_delete_a_trusted_ip_list`

Delete the IPSet specified by the Id.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): Specify the detector ID that should be used to delete an IP set. This parameter can be found in the "Settings" tab.
*   `trusted_ip_list_i_ds` (str, required): Specify the comma-separated list of ids of ips sets. Example: id_1,id_2
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_create_sample_findings`

Generates example findings of types specified by the list of findings.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): The unique ID of the detector to create sample findings for.
*   `finding_types` (Optional[str], optional, default=None): The types of sample findings to generate. Comma separated values. If empty, example findings of all supported finding types will be generated. Types can be found in the UI at ‘Findings’ section under ‘Finding Type’ column
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_delete_a_detector`

Delete an Amazon GuardDuty detector that is specified by the detector ID.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): The unique ID of the detector that you want to delete.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_get_all_trusted_ip_lists`

Get all trusted IP lists (IPSets) of the GuardDuty service specified by the detector ID.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): Specify the detector ID that should be used to list IP sets. This parameter can be found in the "Settings" tab.
*   `max_trusted_ip_lists_to_return` (Optional[str], optional, default=None): Specify how many Trusted IPs lists to return. Default is 50.
*   `aws_region` (Optional[str], optional, default=None): Optionally specify the AWS Region to be used in the action that can be different from the default region specified in the integration configuration page.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_get_a_trusted_ip_list`

Get details about a trusted IP list in AWS GuardDuty.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): Specify the detector ID that should be used to get an IP set. This parameter can be found in the "Settings" tab.
*   `trusted_ip_list_i_ds` (str, required): Specify the comma-separated list of ids of ips sets. Example: id_1,id_2.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_update_threat_intelligence_set`

Update a threat intelligence set in AWS GuardDuty. Note: iam:PutRolePolicy permission.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): Specify the detector ID that should be used to update a Threat Intelligence Set. This parameter can be found in the "Settings" tab.
*   `id` (str, required): Specify the ID of the Threat Intelligence set that should be updated.
*   `active` (bool, required): If enabled, the Threat Intelligence Set will be activated.
*   `name` (Optional[str], optional, default=None): Specify the new name of the Threat Intelligence Set.
*   `file_location` (Optional[str], optional, default=None): Specify a new URI location, where the file is located.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_get_finding_details`

Return detailed information about a finding in AWS Guard Duty.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `finding_i_ds` (str, required): The IDs of the findings that you want to retrieve. Comma separated ids.
*   `detector_id` (str, required): The unique ID of the detector that you want to retrieve.
*   `aws_region` (Optional[str], optional, default=None): Optionally specify the AWS Region to be used in the action that can be different from the default region specified in the integration configuration page.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_list_findings_for_a_detector`

Lists all Amazon GuardDuty findings for the specified detector ID.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): The unique ID of the detector that you want to retrieve.
*   `max_findings_to_return` (Optional[str], optional, default=None): Specify how many detectors to return. Default is 50.
*   `sort_by` (Optional[str], optional, default=None): Represents the finding attribute (for example, accountId) to sort findings by.
*   `order_by` (Optional[List[Any]], optional, default=None): The order by which the sorted findings are to be displayed.
*   `aws_region` (Optional[str], optional, default=None): Optionally specify the AWS Region to be used in the action that can be different from the default region specified in the integration configuration page.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_delete_threat_intelligence_set`

Delete a threat intelligence set in AWS GuardDuty.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): Specify the detector ID that should be used to get threat intelligence sets details. This parameter can be found in the "Settings" tab.
*   `threat_intelligence_set_i_ds` (str, required): Specify the comma-separated list of ids of threat intelligence sets. Example: id_1,id_2
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_update_findings_feedback`

Mark the specified Amazon GuardDuty findings as useful or not useful.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): The unique ID of the detector associated with the findings to update feedback for.
*   `useful` (bool, required): The feedback for the finding.
*   `findings_i_ds` (str, required): The IDs of the findings that you want to mark as useful or not useful. Comma separated ids.
*   `comment` (Optional[str], optional, default=None): Additional feedback about the GuardDuty findings.
*   `aws_region` (Optional[str], optional, default=None): Optionally specify the AWS Region to be used in the action that can be different from the default region specified in the integration configuration page.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_guard_duty_create_threat_intelligence_set`

Create a threat intelligence set in AWS GuardDuty. Note: iam:PutRolePolicy permission. Maximum number of Threat Intel sets is 6.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `detector_id` (str, required): Specify the detector ID that should be used to create a Threat Intelligence Set. This parameter can be found in the "Settings" tab.
*   `name` (str, required): Specify the name of the Threat Intelligence Set.
*   `file_format` (List[Any], required): Select the format of the file that should be used to create a threat intelligence set.
*   `file_location` (str, required): Specify the URI location, where the file is located.
*   `active` (bool, required): If enabled, the newly created Threat Intelligence Set will be activated.
*   `tags` (Optional[str], optional, default=None): Specify additional tags that should be added to the Threat Intelligence Set. Format: key_1:value_1,key_2:value_2.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
