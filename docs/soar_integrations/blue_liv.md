# BlueLiv Integration

## Overview

This integration allows you to connect to the BlueLiv Threat Intelligence platform to enrich entities, manage threat labels and comments, list threats, and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following BlueLiv details:

*   **API Key:** Your BlueLiv API key for authentication.
*   **(Optional) API URL:** The base URL for the BlueLiv API, if different from the default.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Add Labels to Threats

Add specified labels to specified threat resource IDs within a given module.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `module_type` (string, required): Specify the module type the resource belongs to.
*   `module_id` (string, required): Specify the module ID the resource belongs to.
*   `resource_id` (string, required): Specify the Resource IDs (comma-separated) to add the labels to.
*   `label_names` (string, required): Specify the label names (comma-separated) to apply. Case-sensitive.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the label addition operation.

### Ping

Test connectivity to the BlueLiv with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Add Comment to a Threat

Add a text comment to a specific threat resource.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `module_type` (string, required): Specify the module type the resource belongs to.
*   `module_id` (string, required): Specify the module ID the resource belongs to.
*   `resource_id` (string, required): Specify the Resource ID to add the comment to.
*   `comment_text` (string, required): Provide the comment text to add.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition operation.

### List Entity Threats

List threats related to entities in Blueliv, with optional filtering by label or module. Supported entities: All.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `label_filter` (string, optional): Comma-separated list of labels to filter threats (OR logic).
*   `module_filter` (string, optional): Comma-separated list of modules to filter threats.
*   `max_threats_to_return` (string, optional): Specify how many threats to return per entity. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of threats related to the specified entities.

### Mark Threat as a Favorite

Mark or unmark a specified threat as a favorite in BlueLiv.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `module_type` (string, required): Specify the module type the resource belongs to.
*   `module_id` (string, required): Specify the module ID the resource belongs to.
*   `resource_id` (string, required): Specify the Resource ID of the threat.
*   `favorite_status` (List[Any], required): Specify the Favorite status to apply (e.g., Favorite, Not Favorite).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the favorite status update.

### Enrich Entities

Enrich entities using information from Threat Context module of Blueliv. Supported entities: IP, Hash (MD5, SHA1, SHA256, SHA512), URL, Threat Actor, Threat Campaign, Threat Signature, CVE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `lowest_score_to_mark_as_suspicious` (string, required): Specify the lowest score (max 10) for the entity to be marked as suspicious.
*   `create_insight` (bool, optional): If enabled, action will create insights containing information about entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

### Remove Labels From Threats

Remove specified labels from specified threat resource IDs within a given module.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `module_type` (string, required): Specify the module type the resource belongs to.
*   `module_id` (string, required): Specify the module ID the resource belongs to.
*   `resource_id` (string, required): Specify a comma-separated list of resource IDs from which you want to remove labels.
*   `label_names` (string, required): Specify a comma-separated list of labels that need to be removed. Case-sensitive.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the label removal operation.

## Notes

*   Ensure the BlueLiv integration is properly configured in the SOAR Marketplace tab with a valid API Key.
*   Actions often require specifying `module_type`, `module_id`, and `resource_id` to target specific threats.
*   Label operations are case-sensitive.
*   The `Enrich Entities` action supports various IOC types and allows setting a suspicion threshold based on the BlueLiv score.
