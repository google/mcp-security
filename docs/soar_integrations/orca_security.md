# Orca Security Integration

## Overview

This integration allows you to connect to Orca Security to retrieve details about vulnerabilities and assets, update alerts, scan assets, and test connectivity.

## Configuration

The configuration for this integration (Orca Security URL, API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get Vulnerability Details

Retrieve information about vulnerabilities from Orca Security based on CVE IDs.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cve_i_ds` (string, required): Specify a comma-separated list of CVEs that need to be enriched.
*   `fields_to_return` (string, optional): Specify a comma-separated list of fields to return (uses flattened JSON keys, e.g., `object_id`).
*   `output` (List[Any], optional): Specify output type ("JSON" or "CSV"). CSV creates a file in the execution folder.
*   `create_insight` (bool, optional): If enabled, creates an insight for every enriched vulnerability.
*   `max_assets_to_return` (string, optional): Specify how many assets related to the CVE to return. Default: 50. Maximum: 10000.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports CVE entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing vulnerability details and related assets, or a path to a CSV file if specified.

### Update Alert

Update alert status, snooze state, or initiate verification in Orca Security.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert needs to be updated.
*   `verify_alert` (bool, optional): If enabled, initiates the verification process for the alert.
*   `snooze_state` (List[Any], optional): Specify the snooze state for the alert.
*   `snooze_days` (string, optional): Specify how many days alert needs to be snoozed (mandatory if Snooze State is "Snooze"). Default: 1 day.
*   `status` (List[Any], optional): Specify what status to set for the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### Get Compliance Info

Get information about compliance based on selected frameworks in Orca Security.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (bool, required): If enabled, action will create an insight containing information about compliance.
*   `framework_names` (string, optional): Specify the names of the frameworks (comma-separated). If empty, returns info for all selected frameworks.
*   `max_frameworks_to_return` (string, optional): Specify how many frameworks to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing compliance information for the specified frameworks.

### Scan Assets

Scan assets in Orca Security. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `asset_i_ds` (string, required): Specify a comma-separated list of asset ids for which you want to return details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the scan initiation.

### Ping

Test connectivity to the Orca Security with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Add Comment To Alert

Add a comment to alert in Orca Security.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert to which action needs to add a comment.
*   `comment` (string, required): Specify the comment that needs to be added to alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the comment addition.

### Get Asset Details

Retrieve information about assets in Orca Security.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `asset_i_ds` (string, required): Specify a comma-separated list of asset ids for which you want to return details.
*   `lowest_severity_for_vulnerabilities` (List[Any], required): Lowest severity that needs to be used to fetch vulnerabilities.
*   `return_vulnerabilities_information` (bool, optional): If enabled, action will return vulnerabilities related to the asset.
*   `max_vulnerabilities_to_fetch` (string, optional): Specify how many vulnerabilities to return per asset. Default: 50. Maximum: 100.
*   `create_insight` (bool, optional): If enabled, action will create an insight for every enriched asset.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details for the specified assets, potentially including related vulnerabilities.

## Notes

*   Ensure the Orca Security integration is properly configured in the SOAR Marketplace tab with the correct URL and API Key.
*   The `Scan Assets` action runs asynchronously. Monitor its progress separately if needed.
*   The `Get Vulnerability Details` action supports filtering fields using flattened JSON notation (e.g., `object_id` for `{"object": {"id": 123}}`).
