# Microsoft Azure Sentinel Integration

## Overview

This integration allows you to connect to Microsoft Azure Sentinel to run KQL queries, manage alert rules and hunting rules, list incidents, and manage incident details like comments and labels.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, Subscription ID, Resource Group Name, Workspace Name, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Run KQL Query

Run Azure Sentinel KQL Query based on the provided action input parameters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `kql_query` (string, required): A KQL Query to execute in Azure Sentinel. For example, to get security alerts available in Sentinel, query will be "SecurityAlert". Use other action input parameters (time span, limit) to filter the query results. For the examples of KQL queries consider Sentinel "Logs" Web page.
*   `time_span` (string, optional): Time span to look for, use the following format: PT + number + (M, H), where M - minutes, H - hours. Use P + number + D to specify a number of days. Can be combined as P1DT1H1M - 1 day, 1 hour and 1 minute.
*   `query_timeout` (string, optional): Timeout value for the Azure Sentinel hunting rule API call. Note that Siemplify action python process timeout should be adjusted accordingly for this parameter, to not timeout action sooner than specified value because of the python process timeout.
*   `record_limit` (string, optional): How many records should be fetched. Optional parameter, if set, adds a "| limit x" to the kql query where x is the value set for the record limit. Can be removed if "limit" is already set in kql query or not needed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the KQL query execution.

### Get Alert Rule Details

Get Details of the Azure Sentinel Scheduled Alert Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_rule_id` (string, required): Alert Rule ID.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified alert rule.

### List Custom Hunting Rules

List Custom Hunting Rules available in Sentinel.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunting_rule_names_to_return` (string, optional): Names for the hunting rules action should return. Comma-separated string.
*   `fetch_specific_hunting_rule_tactics` (string, optional): What hunting rule tactics action should return. Comma-separated string.
*   `max_rules_to_return` (string, optional): How many scheduled alert rules the action should return, for example, 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of custom hunting rules matching the criteria.

### Get Incident Statistic

Get Azure Sentinel Incident Statistics.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (string, optional): Time frame in hours for which to fetch Incidents.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing incident statistics for the specified time frame.

### Create Alert Rule

Create Azure Sentinel Scheduled Alert Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `enable_alert_rule` (bool, required): Enable or disable new alert rule.
*   `name` (string, required): Display name of the new alert rule.
*   `severity` (List[Any], required): Severity of the new alert rule.
*   `query` (string, required): Query of the new alert rule.
*   `frequency` (string, required): How frequently to run the query, use the following format: PT + number + (M, H), where M - minutes, H - hours. Use P + number + D to specify a number of days. Can be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. Minimum is 5 minutes, maximum is 14 days.
*   `period_of_lookup_data` (string, required): Time of the last lookup data, use the following format: PT + number + (M, H), where M - minutes, H - hours. Use P + number + D to specify a number of days. Can be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. Minimum is 5 minutes, maximum is 14 days.
*   `trigger_operator` (List[Any], required): Trigger operator for this alert rule. Possible values are: GreaterThan, LessThan, Equal, NotEqual.
*   `trigger_threshold` (string, required): Trigger threshold for this alert rule.
*   `enable_suppression` (bool, required): Whether you want to stop running query after alert is generated.
*   `suppression_duration` (string, required): How long you want to stop running query after alert is generated, use the following format: PT + number + (M, H), where M - minutes, H - hours. Use P + number + D to specify a number of days. Can be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. Minimum is 5 minutes, maximum is 14 days.
*   `description` (string, optional): Description of the new alert rule.
*   `tactics` (string, optional): Tactics of the new alert rule. Comma-separated values.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ID of the created alert rule.

### Update Alert Rule

Update Azure Sentinel Scheduled Alert Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_rule_id` (string, required): Alert Rule ID.
*   `enable_alert_rule` (bool, optional): Enable or disable new alert rule.
*   `name` (string, optional): Display name of the new alert rule.
*   `severity` (List[Any], optional): Severity of the new alert rule.
*   `query` (string, optional): Query of the new alert rule.
*   `frequency` (string, optional): How frequently to run the query (format: PThhHmmMssS or PnDTnHnMn.nS). Minimum 5m, max 14d.
*   `period_of_lookup_data` (string, optional): Time of the last lookup data (format: PThhHmmMssS or PnDTnHnMn.nS). Minimum 5m, max 14d.
*   `trigger_operator` (List[Any], optional): Trigger operator (GreaterThan, LessThan, Equal, NotEqual).
*   `trigger_threshold` (string, optional): Trigger threshold for this alert rule.
*   `enable_suppression` (bool, optional): Whether you want to stop running query after alert is generated.
*   `suppression_duration` (string, optional): How long to stop running query after alert is generated (format: PThhHmmMssS or PnDTnHnMn.nS). Minimum 5m, max 14d.
*   `description` (string, optional): Description of the new alert rule.
*   `tactics` (string, optional): Tactics of the new alert rule. Comma-separated values.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Incidents

List Microsoft Azure Sentinel Incidents based on the provided search criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (string, optional): Time frame in hours for which to fetch Incidents.
*   `status` (string, optional): Statuses of the incidents to look for. Comma-separated string.
*   `severity` (string, optional): Severities of the incidents to look for. Comma-separated string.
*   `how_many_incidents_to_fetch` (string, optional): How many incidents to fetch.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of incidents matching the criteria.

### Add Comment to Incident

Add a comment to Azure Sentinel Incident.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_number` (string, required): Specify Incident number to add comment to.
*   `comment_to_add` (string, required): Specify comment to add to Incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Update Incident Details v2

Update Incident Details v2. Action is a Chronicle SOAR async action and can be configured for a retry for a longer period of time.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_case_number` (string, required): Specify Azure Sentinel incident number to update.
*   `title` (string, optional): Specify new title for the Azure Sentinel incident.
*   `status` (List[Any], optional): Specify new status for the Azure Sentinel incident.
*   `severity` (List[Any], optional): Specify new severity for the Azure Sentinel incident.
*   `description` (string, optional): Specify new description for the Azure Sentinel incident.
*   `assigned_to` (string, optional): Specify the user to assign the incident to.
*   `closed_reason` (List[Any], optional): If status of the incident is set to Closed, provide a Closed Reason for the incident.
*   `closing_comment` (string, optional): Optional closing comment to provide for the closed Azure Sentinel Incident.
*   `number_of_retries` (string, optional): Specify the number of retry attempts the action should make if the incident update was unsuccessful.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to Microsoft Azure Sentinel.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Custom Hunting Rule Details

Get Details of the Azure Sentinel Custom Hunting Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunting_rule_id` (string, required): Hunting Rule ID.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified custom hunting rule.

### Create Custom Hunting Rule

Create Azure Sentinel Custom Hunting Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `display_name` (string, required): Display name of the new custom hunting rule.
*   `query` (string, required): Query of the new custom hunting rule.
*   `description` (string, optional): Description of the new custom hunting rule.
*   `tactics` (string, optional): Tactics of the new custom hunting rule. Comma-separated values.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ID of the created hunting rule.

### Delete Custom Hunting Rule

Delete Azure Sentinel Custom Hunting Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunting_rule_id` (string, required): Hunting Rule ID.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Update Incident Labels

Update Incident Labels. Please consider moving to the v2 version of the action, as it is implemented as a SOAR async action and provides more consistent results.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_case_number` (string, required): Specify Azure Sentinel incident number to update with new labels.
*   `labels` (string, required): Specify new labels that should be appended to the Incident. Parameter accepts multiple values as a comma-separated string.
*   `number_of_retries` (string, optional): Specify the number of retry attempts the action should make if the incident update was unsuccessful.
*   `retry_every` (string, optional): Specify what time period in seconds action should wait between incident update retries.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Update Incident Details

Update Incident Details. Please consider moving to the v2 version of the action, as it is implemented as a SOAR async action and provides more consistent results.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_case_number` (string, required): Specify Azure Sentinel incident number to update.
*   `title` (string, optional): Specify new title for the Azure Sentinel incident.
*   `status` (List[Any], optional): Specify new status for the Azure Sentinel incident.
*   `severity` (List[Any], optional): Specify new severity for the Azure Sentinel incident.
*   `description` (string, optional): Specify new description for the Azure Sentinel incident.
*   `assigned_to` (string, optional): Specify the user to assign the incident to.
*   `closed_reason` (List[Any], optional): If status of the incident is set to Closed, provide a Closed Reason for the incident.
*   `closing_comment` (string, optional): Optional closing comment to provide for the closed Azure Sentinel Incident.
*   `number_of_retries` (string, optional): Specify the number of retry attempts the action should make if the incident update was unsuccessful.
*   `retry_every` (string, optional): Specify what time period action should wait between incident update retries.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Update Incident Labels v2

Update Incident Labels v2. Action is a Chronicle SOAR async action and can be configured for a retry for a longer period of time.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_case_number` (string, required): Specify Azure Sentinel incident number to update with new labels.
*   `labels` (string, required): Specify new labels that should be appended to the Incident. Parameter accepts multiple values as a comma-separated string.
*   `number_of_retries` (string, optional): Specify the number of retry attempts the action should make if the incident update was unsuccessful.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Alert Rules

Get Azure Sentinel Scheduled Rules list.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_rule_severity` (string, optional): Severities of the alert rules to look for. Comma-separated string.
*   `fetch_specific_alert_rule_types` (string, optional): What alert rule types action should return. Comma-separated string.
*   `fetch_specific_alert_rule_tactics` (string, optional): What alert rule tactics action should return. Comma-separated string.
*   `fetch_only_enabled_alert_rules` (bool, optional): If action should return only enabled alert rules.
*   `max_rules_to_return` (string, optional): How many scheduled alert rules the action should return, for example, 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of alert rules matching the criteria.

### Delete Alert Rule

Delete Azure Sentinel Scheduled Alert Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_rule_id` (string, required): Alert Rule ID.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Update Custom Hunting Rule

Update Azure Sentinel Custom Hunting Rule.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunting_rule_id` (string, required): Hunting Rule ID.
*   `display_name` (string, optional): Display name of the new custom hunting rule.
*   `query` (string, optional): Query of the new custom hunting rule.
*   `description` (string, optional): Description of the new custom hunting rule.
*   `tactics` (string, optional): Tactics of the new custom hunting rule. Comma-separated values.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Run Custom Hunting Rule Query

Run Custom Hunting Rule Query.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunting_rule_id` (string, required): Hunting Rule ID.
*   `timeout` (string, optional): Timeout value for the Azure Sentinel hunting rule API call.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the hunting rule query execution.

## Notes

*   Ensure the Microsoft Azure Sentinel integration is properly configured in the SOAR Marketplace tab with the necessary credentials and workspace details.
*   Several actions are asynchronous and may require adjusting script timeouts in the SOAR IDE.
*   Pay attention to the required time formats (ISO 8601 or PTnHnMn.nS) for time-related parameters.
*   V2 versions of `Update Incident Details` and `Update Incident Labels` are recommended for better consistency due to their asynchronous nature.
