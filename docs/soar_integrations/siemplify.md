# Siemplify SOAR Integration

This document details the tools provided by the Siemplify SOAR integration, which allow interaction with the core Siemplify platform functionalities.

## Overview

The Siemplify integration provides actions to manage cases, alerts, entities, playbooks, and other core SOAR objects directly within Chronicle SOAR workflows. This enables meta-playbooking, custom list management, context sharing, and interaction with Siemplify's native features.

## Tools

### `siemplify_get_similar_cases`

Search for similar cases and return their Ids

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `rule_generator` (bool, required): Search for similar cases by the same Rule Generator. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `port` (bool, required): Search for similar cases by the same Port number. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `category_outcome` (bool, required): Search for similar cases by the same Category Outcome. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `entity_identifier` (bool, required): Search for similar cases containing the same Entity Identifier. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `days_back` (str, required): Defines how many days back the search should look for similar cases.
*   `include_open_cases` (Optional[bool], optional, default=None): Search open cases
*   `include_closed_cases` (Optional[bool], optional, default=None): Search closed cases
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_mark_as_important`

Mark case as important

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_create_or_update_entity_properties`

Create\Change properties for entities in an entity scope.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `entity_field` (str, required): Field that has to be created or updated.
*   `field_value` (str, required): Value that has to be set to the field.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_change_priority`

Automatically change case priority to the given input

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `priority` (str, required): Priority, which should be set for the case.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_create_gemini_case_summary`

Create a summary of the case using Gemini AI.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_set_risk_score`

Set risk score for a SOAR case. Note: This action is only supported from Chronicle SOAR version 6.3.6 and higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `risk_score` (str, required): Specify risk score that needs to be set.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_set_custom_fields`

Preview. Set values for custom fields.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `custom_fields_data` (str, required): The values to update for the custom fields. You can update multiple custom fields in a single action run.
*   `append_values` (Optional[bool], optional, default=None): If selected, the action appends the inputs from the "Custom Fields Data" parameter to the existing values of the custom fields. If not selected, the action overwrites the existing values with the inputs from the "Custom Fields Data" parameter. Not selected by default.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_set_case_sla`

Set the SLA for a case. This action has the highest priority and it will override the existing SLA defined for the specific case.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `sla_period` (str, required): The period of time after which the SLA is in breach.
*   `sla_time_unit` (List[str], required): Specify the unit for SLA Time.
*   `sla_time_to_critical_period` (str, required): The period of time after which the SLA enters the critical period.
*   `sla_time_to_critical_unit` (List[str], required): Specify the unit for SLA Time To Critical.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_is_in_custom_list`

Check whether an Entity Identifier is part of a predefined dynamic categorized Custom List

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `category` (str, required): Custom list category.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_test_siemplify_proxy`

Test connection to a given endpoint using proxy settings configured in Siemplify.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `endpoint_url` (str, required): The endpoint to try to connect to
*   `http_method` (str, required): The HTTP method to use when connecting to the endpoint
*   `verify_ssl` (bool, required): Whether to verify SSL certificate or not.
*   `body` (Optional[str], optional, default=None): The body of the HTTP request
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_case_tag`

Add given tag to the case the current alert is grouped to

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `tag` (str, required): Tag to be added to the case.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_close_alert`

Closes the current alert

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `reason` (str, required): Alert closure reason.
*   `root_cause` (str, required): Root cause of the alert closure.
*   `comment` (str, required): Comment content.
*   `assign_to_user` (Optional[Any], optional, default=None): User that the closed case will be assigned to.
*   `tags` (Optional[str], optional, default=None): Comma separated tags values.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_add_to_custom_list`

Add an Entity Identifier to a categorized Custom List, in order to perform future comparisons in other actions.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `category` (str, required): Custom list category to be used.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_case_comment`

Add a comment to the case the current alert has been grouped to

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `comment` (str, required): Comment to be added to the case.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_permitted_alert_time`

Check case time according to a given time condition

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `permitted_start_time` (str, required): Start of the timeframe, when alerts are allowed. For example: 9:55:24
*   `permitted_end_time` (str, required): End of the timeframe, when alerts are allowed. For example: 17:23:21
*   `input_timezone` (str, required): Timezone name. For example: UTC
*   `monday` (Optional[bool], optional, default=None):
*   `tuesday` (Optional[bool], optional, default=None):
*   `wednesday` (Optional[bool], optional, default=None):
*   `thursday` (Optional[bool], optional, default=None):
*   `friday` (Optional[bool], optional, default=None):
*   `saturday` (Optional[bool], optional, default=None):
*   `sunday` (Optional[bool], optional, default=None):
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_open_web_url`

Generate a browser link

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `title` (str, required): Title for URL.
*   `url` (str, required): Target URL.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_change_case_stage`

Change case stage to handling

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `stage` (str, required): Stage to which the case should be moved to.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_add_general_insight`

Add a general insight configurable message to the case

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `title` (str, required): The title of the insight.
*   `message` (str, required): The message that will be placed on the insight.
*   `triggered_by` (Optional[str], optional, default=None): A description for the cause of this insight
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_resume_alert_sla`

Automatically resume the alert SLA

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_instruction`

Set an instruction for the analyst

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `instruction` (str, required): Instruction content.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_get_case_details`

This action will get all the data from a case and return a JSON result.  The result includes comments, entity information, insights, playbooks that ran, alert information and events.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `fields_to_return` (Optional[str], optional, default=None): Specify a comma-separated list of fields that need to be returned. If nothing is provided, all fields are returned. Getting nested values can be done using \"Nested Keys Delimiter\" value to chain nested keys and list indexes. For example, if the delimiter is \".\": key_1.nested_key_1.0.nested_key_2, key_2, key_3.1.nested_key_1
*   `nested_keys_delimiter` (Optional[str], optional, default=None): The delimiter to split nested keys. If missing or not provided fetching nested keys is not possible. Cannot be a comma (\",\")
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_set_scope_context_value`

Action sets a value for a key specified that is stored in the Siemplify database. Available scopes to get context values for: Alert, Case, Global. Action is not working on Siemplify entities. Note: Key Name parameter is case insensitive.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `context_scope` (List[str], required): Specify the Siemplify context scope to return context keys for.
*   `key_name` (str, required): Specify the key name to set context value for.
*   `key_value` (str, required): Specify the value to store under the specified key.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_add_tags_to_similar_cases`

Add tags to similar cases and return their Ids

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `rule_generator` (bool, required): Search for similar cases by the same Rule Generator. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `port` (bool, required): Search for similar cases by the same Port number. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `category_outcome` (bool, required): Search for similar cases by the same Category Outcome. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `entity_identifier` (bool, required): Search for similar cases containing the same Entity Identifier. Note: All these search criteria are joined using logical 'AND' condition and will be used in the same search.
*   `days_back` (str, required): Defines how many days back the search should look for similar cases.
*   `tags` (str, required): Specify a comma-separated list of tags that you want to add to similar cases.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_add_entity_insight`

Add an insight configurable message to each targeted entity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `message` (str, required): Message content to be added.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_attach_playbook_to_alert`

Attach a specific playbook to an alert

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `playbook_name` (str, required): Playbook, which should be attached to an alert.
*   `allow_duplicates` (Optional[bool], optional, default=None): If selected, action will allow the same playbook to be attached multiple times to the alert.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_close_case`

Closes the case the current alert has been grouped to

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `reason` (str, required): Closure reason.
*   `root_cause` (str, required): Root cause of the case closure.
*   `comment` (str, required): Comment content.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_assign_case`

Assign case to specific user or usergroup

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `assigned_user` (str, required): User or Usergroup to whom a case should be assigned.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_wait_for_custom_fields`

Preview. Wait for custom fields values to continue playbook execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `custom_fields_data` (str, required): The conditions that are required for the custom fields for the action to resume running a playbook. Configure the custom field names and their required values as a JSON object.
If you set conditions for multiple fields, the action waits for all fields to match their respective conditions.
The action behavior depends on the input that you provide.
For the action to resume running a playbook with any value in a custom field, configure an empty string for the custom field as follows:
{
“Custom Field”: “”
}
For the action to resume running a playbook when the custom field equals to a specific value (“Value 1”), specify the value for the custom field as follows:
{
“Custom Field”: “Value 1”
}
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_create_entity`

Creates an entity and adds to requested alert. Note - Please make sure to read our documentation regarding the differences in the delimiter’s behavior, between different Siemplify’s platform versions 5.6.0 inclusive and 5.6.2 exclusive, here: https://cloud.google.com/chronicle/docs/soar/marketplace-integrations/siemplify#create-entity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `entities_identifies` (str, required): Entity identifier or comma-separated list of identifiers (Example: value1,value2,value3).
*   `entity_type` (str, required): Siemplify entity type. Example: HOSTNAME / USERNAME / etc.
*   `is_internal` (bool, required): Mark if entities are part of an internal network.
*   `is_suspicious` (bool, required): Mark if entities are suspicious.
*   `delimiter` (Optional[str], optional, default=None): Provide a delimiter character, with which the action will split the input it gets into a number of entities instead of a single one. If no value will be provided, action will not perform any splitting on the input, and it will be handled as a single entity. Note - Please make sure to read our documentation regarding the differences in the delimiter's behavior, between different Siemplify's platform versions 5.6.0 inclusive and 5.6.2 exclusive.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_update_case_description`

Ability to set Case Description from playbooks.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `description` (str, required): Specify what description should be set for the case.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_raise_incident`

Raise case incident (Note - Used to mark critical true positive cases)

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `soc_role` (Optional[Any], optional, default=None): Role to which the case should be assigned.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_run_remote`

Run remote action via publisher

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `publisher_name` (str, required): Publisher instance name to be used.
*   `remote_integration_name` (str, required): Remote integration name to be used.
*   `remote_action_name` (str, required): Remote action name to be used.
*   `remote_context_data` (str, required): Remote action context data.
*   `remote_action_script` (str, required): Remote action script content to be executed.
*   `agent_id` (str, required): Action's target agent id.
*   `installed_integrations_shared_folder` (str, required): Installed Integrations Shared Folder
*   `verify_ssl` (Optional[bool], optional, default=None): Enables\Disables SSL Verification between Siemplify's machine and the remote Publisher
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_pause_alert_sla`

Automatically pause the alert SLA

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `message` (Optional[str], optional, default=None): Pause Reason
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_remove_from_custom_list`

Remove an Entity Identifier from a categorized Custom List, in order to perform future comparisons in other actions.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `category` (str, required): Custom list category to be used.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_change_alert_priority`

Automatically change the alert priority to the given input. Note: This action is compatible only with Siemplify version 5.6 and higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alert_priority` (str, required): Priority to which the alert should be moved to.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_set_alert_sla`

Set the SLA for an alert. This action has the highest priority and it will override the existing SLA defined for the specific alert.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `sla_period` (str, required): The period of time after which the SLA is in breach.
*   `sla_time_unit` (List[str], required): Specify the unit for SLA Time.
*   `sla_time_to_critical_period` (str, required): The period of time after which the SLA enters the critical period.
*   `sla_time_to_critical_unit` (List[str], required): Specify the unit for SLA Time To Critical.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_get_connector_context_value`

Action gets a value stored under a specified key in the Siemplify database for a connector context. Action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `connector_identifier` (str, required): Specify connector identifier to list context keys for. Parameter works together with "Connector Identifier Filter Logic" parameter
*   `key_name` (str, required): Optionally specify the key name to get context value for.
*   `create_case_wall_table` (Optional[bool], optional, default=None): If enabled, the case wall table will be created as part of action results.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_get_scope_context_value`

Action gets a value stored under a specified key in the Siemplify database. Available scopes to get context values for: Alert, Case, Global. Action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `context_scope` (List[str], required): Specify the Siemplify context scope to return context keys for.
*   `key_name` (str, required): Optionally specify the key name to get context value for.
*   `create_case_wall_table` (Optional[bool], optional, default=None): If enabled, the case wall table will be created as part of action results.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_remove_tag`

Remove tags from a case.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `tag` (str, required): Specify the tag that needs to be removed. Comma seperated values.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
