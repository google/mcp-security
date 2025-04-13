# FireEye AX Integration

## Overview

This integration allows you to connect to a FireEye AX (Malware Analysis) appliance to perform actions such as submitting files and URLs for analysis, retrieving appliance details, and testing connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get Appliance Details

Retrieves information about the configured FireEye AX appliance, including available VM profiles and applications which can be useful for submission actions.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details about the appliance.

### Ping

Tests connectivity to the configured FireEye AX appliance using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action, typically indicating success or failure.

### Submit URL

Submits a URL (or multiple URLs via entities) for analysis by the FireEye AX appliance. This action runs asynchronously.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `vm_profile` (string, required): The virtual machine profile to use for analysis (obtainable via "Get Appliance Details").
*   `create_insight` (boolean, required): If enabled, creates a SOAR insight with the analysis results.
*   `application_id` (string, optional): The specific application ID to use for analysis (obtainable via "Get Appliance Details"). Defaults to automatic selection by FireEye AX.
*   `priority` (List[Any], optional): Sets the submission priority ("Normal" or "Urgent").
*   `force_rescan` (boolean, optional): If enabled, forces FireEye AX to rescan the URL even if previously analyzed.
*   `analysis_type` (List[Any], optional): Specifies the analysis type ("Live" or "Sandbox").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. URLs from entities will be submitted.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the submission action, including submission status and potentially analysis IDs.

### Submit File

Submits one or more files (specified by path) for analysis by the FireEye AX appliance. This action runs asynchronously.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths` (string, required): A comma-separated list of absolute file paths on the SOAR server for submission.
*   `vm_profile` (string, required): The virtual machine profile to use for analysis (obtainable via "Get Appliance Details").
*   `create_insight` (boolean, required): If enabled, creates a SOAR insight with the analysis results.
*   `application_id` (string, optional): The specific application ID to use for analysis (obtainable via "Get Appliance Details"). Defaults to automatic selection by FireEye AX.
*   `priority` (List[Any], optional): Sets the submission priority ("Normal" or "Urgent").
*   `force_rescan` (boolean, optional): If enabled, forces FireEye AX to rescan the submitted file(s) even if previously analyzed.
*   `analysis_type` (List[Any], optional): Specifies the analysis type ("Live" or "Sandbox").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the submission action, including submission status and potentially analysis IDs.

## Notes

*   The `Submit URL` and `Submit File` actions are asynchronous. You may need to adjust script timeout values in the SOAR platform IDE accordingly to allow sufficient time for analysis completion.
*   Ensure the FireEye AX integration is properly configured in the SOAR Marketplace tab with valid credentials and appliance details before using these actions.
*   Use the `Get Appliance Details` action to discover available `vm_profile` and `application_id` values specific to your appliance configuration.
