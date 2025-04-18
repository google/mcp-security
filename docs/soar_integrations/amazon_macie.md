# Amazon Macie SOAR Integration

This document details the tools provided by the Amazon Macie SOAR integration.

## Tools

### `amazon_macie_get_findings`

Get Amazon Macie findings based on specified Finding ID. Note: Action is not working with Siemplify Entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `finding_id` (str, required): Finding ID to get details for. Parameter can take multiple values as a comma separated string.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `amazon_macie_list_findings`

List Amazon Macie findings based on the specified action input parameters.  Note: Action is not working with Siemplify entities, only with action input parameters.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `finding_type` (Optional[str], optional, default=None): Finding type to search for, for example SensitiveData:S3Object/Credentials or SensitiveData:S3Object/Multiple. Parameter accepts multiple values as a comma separated string. If nothing is specified - return all types of findings.
*   `time_frame` (Optional[str], optional, default=None): Specify a time frame in hours for which to fetch findings.
*   `severity` (Optional[str], optional, default=None): Finding severity to search - High, Medium or Low. Parameter accepts multiple values as a comma separated string. If nothing is specified - return all findings regardless of severity.
*   `include_archived_findings` (Optional[bool], optional, default=None): Specify whether to include archived findings in results or not.
*   `record_limit` (Optional[str], optional, default=None): Specify how many records can be returned by the action.
*   `sort_by` (Optional[str], optional, default=None): Specify a parameter for sorting the data, eg updatedAt
*   `sort_order` (Optional[List[Any]], optional, default=None): Sort order.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `amazon_macie_delete_custom_data_identifier`

Delete Amazon Macie Custom Data Identifier. Note: Action is not working with Siemplify Entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `custom_data_identifier_id` (str, required): Amazon Macie custom data identifier id to delete.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `amazon_macie_disable_macie`

Disable Amazon Macie service. Note: Action is not working with Siemplify Entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `amazon_macie_ping`

Test connectivity to the Amazon Macie service with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `amazon_macie_enable_macie`

Enable Amazon Macie service. Note: Action is not working with Siemplify Entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `amazon_macie_create_custom_data_identifier`

Create Amazon Macie Custom Data Identifier. Note: Action is not working with Siemplify Entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `custom_data_identifier_name` (str, required): Amazon Macie new custom data identifier name.
*   `custom_data_identifier_regular_expression` (str, required): Amazon Macie new custom data identifier regular expression, eg I[a@]mAB[a@]dRequest
*   `custom_data_identifier_description` (Optional[str], optional, default=None): Amazon Macie new custom data identifier description.
*   `custom_data_identifier_keywords` (Optional[str], optional, default=None): Amazon Macie new custom data identifier keywords.
*   `custom_data_identifier_ignore_words` (Optional[str], optional, default=None): Amazon Macie new custom data identifier ignore words.
*   `custom_data_identifier_maximum_match_distance` (Optional[str], optional, default=None): Amazon Macie new custom data identifier maximum match distance. Default value is 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
