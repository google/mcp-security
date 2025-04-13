# Microsoft 365 Defender Integration

## Overview

This integration allows you to connect to Microsoft 365 Defender to manage incidents, execute hunting queries, and test connectivity.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Update Incident

Update incident in Microsoft 365 Defender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the id of the incident that needs to be updated.
*   `status` (List[Any], optional): Specify what status to set for the incident.
*   `classification` (List[Any], optional): Specify what classification to set for the incident.
*   `determination` (List[Any], optional): Specify what determination to set for the incident. Note: determination can only be set when classification is true positive.
*   `assign_to` (string, optional): Specify to whom to assign this incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### Execute Query

Execute hunting query in Microsoft 365 Defender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `table_names` (string, required): Specify what tables should be queried.
*   `query` (string, optional): Specify the query that needs to be executed. Use this parameter to provide |where clauses. Note: you don’t need to provide time filter, limiting and sorting.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time".
*   `start_time` (string, optional): Specify the start time for the results. Format: ISO 8601. Mandatory if Time Frame is "Custom".
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. Uses current time if Time Frame is "Custom" and this is empty.
*   `fields_to_return` (string, optional): Specify what fields to return.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting.
*   `sort_order` (List[Any], optional): Specify the order of sorting.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results.

### Add Comment To Incident

Add comment to incident in Microsoft 365 Defender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the id of the incident that needs to be updated.
*   `comment` (string, required): Specify the comment that needs to be added to the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Microsoft 365 Defender with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Execute Entity Query

Execute a hunting query based on entities in Microsoft 365 Defender. Note: this action prepares a where filter based on entities. Supported entities: IP, Host, User, Hash, URL.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `table_names` (string, required): Specify what tables should be queried.
*   `stop_if_not_enough_entities` (bool, required): If enabled, action will not start execution unless all specified entity types are available in the scope.
*   `cross_entity_operator` (List[Any], required): Specify the logical operator (AND/OR) used between different entity types.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, provide "Start Time".
*   `start_time` (string, optional): Specify the start time for the results. Format: ISO 8601. Mandatory if Time Frame is "Custom".
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. Uses current time if Time Frame is "Custom" and this is empty.
*   `fields_to_return` (string, optional): Specify what fields to return.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting.
*   `sort_order` (List[Any], optional): Specify the order of sorting.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `ip_entity_key` (string, optional): Specify the key for IP entities.
*   `hostname_entity_key` (string, optional): Specify the key for Hostname entities.
*   `file_hash_entity_key` (string, optional): Specify the key for File Hash entities.
*   `user_entity_key` (string, optional): Specify the key for User entities.
*   `url_entity_key` (string, optional): Specify the key for URL entities.
*   `email_address_entity_key` (string, optional): Specify the key for Email Address entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results based on entities.

### Execute Custom Query

Execute a custom hunting query in Microsoft 365 Defender.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the query that needs to be executed. Use this parameter to provide |where clauses. Note: you don’t need to provide limiting ("top" keyword).
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the custom query execution.

## Notes

*   Ensure the Microsoft 365 Defender integration is properly configured in the SOAR Marketplace tab.
*   Pay attention to required time formats (ISO 8601) for time-related parameters.
*   The `Update Incident` action has specific requirements for setting the `determination` field based on the `classification`.
*   The `Execute Entity Query` action automatically constructs the `where` clause based on provided entities and keys.
