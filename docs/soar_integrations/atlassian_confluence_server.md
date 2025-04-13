# Atlassian Confluence Server SOAR Integration

This document details the tools provided by the Atlassian Confluence Server SOAR integration.

## Tools

### `atlassian_confluence_server_get_page_by_id`

Get Atlassian Confluence Server page by id. Note: This action doesn’t run on Chronicle SOAR entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `page_id` (str, required): Specify the page id to return.
*   `expand` (Optional[str], optional, default=None): Specify the expand parameter to return additional information about the page. Parameter accepts multiple values as a comma separated list. By default with body.storage the content of the page is fetched.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `atlassian_confluence_server_get_child_pages`

Get child pages for the Atlassian Confluence Server page. Note: This action doesn’t run on Chronicle SOAR entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `page_id` (str, required): Specify the page id to return.
*   `max_records_to_return` (str, required): Specify the limit of child pages to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `atlassian_confluence_server_get_page_comments`

Get comments for the Atlassian Confluence Server page. Note: This action doesn’t run on Chronicle SOAR entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `page_id` (str, required): Specify the page id to return.
*   `max_records_to_return` (str, required): Specify the limit of child pages to return.
*   `expand` (Optional[str], optional, default=None): Specify the expand parameter to return additional information about the page. Parameter accepts multiple values as a comma separated list. By default with body.storage the content of the page is fetched.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `atlassian_confluence_server_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `atlassian_confluence_server_list_pages`

List pages available in the Atlassian Confluence Server instance based on provided criteria. Note: This action doesn’t run on Chronicle SOAR entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_key` (Optional[List[Any]], optional, default=None): Specify the key that needs to be used to filter pages.
*   `filter_logic` (Optional[List[Any]], optional, default=None): Specify what filter logic should be applied. Filtering logic is working based on the value  provided in the “Filter Key” parameter.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If “Equal“ is selected, action will try to find the exact match among results and if “Contains“ is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value  provided in the “Filter Key” parameter.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return. If nothing is provided, action will return 50 records.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
