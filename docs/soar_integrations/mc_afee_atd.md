# McAfee Advanced Threat Defense (ATD) Integration

## Overview

This integration allows you to connect to McAfee Advanced Threat Defense (ATD) to submit files and URLs for analysis, retrieve reports, check hash reputations, get analyzer profiles, and test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get Report

Get report for specified task IDs.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_i_ds` (string, required): The IDs of the tasks to fetch reports for, comma separated.
*   `create_insight` (bool, optional): If enabled, action will create an insight containing all of the retrieved information about the report.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the report details.

### Ping

Test McAfee ATD connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Submit URL

Submit URL for Analysis.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `analyzer_profile_id` (string, required): The ID of the analyzer profile to analyze the urls with.
*   `create_insight` (bool, optional): If enabled, action will create an insight containing all of the retrieved information about the entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. URL entities are used.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including task IDs for the submitted URLs.

### Check Hash

Check if a hash is blacklisted.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hash entities are used.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, indicating if the hash is blacklisted.

### Get Analyzer Profiles

Get McAfee ATD Analyzer Profiles data.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, listing available analyzer profiles.

### Submit File

Submit File for Analysis.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths` (string, required): The paths of the file to submit, comma separated. Notice - some file types are not supported by ATD (i.e: CSV files).
*   `analyzer_profile_id` (string, required): The ID of the analyzer profile to analyze with.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including task IDs for the submitted files.

## Notes

*   Ensure the McAfee ATD integration is properly configured in the SOAR Marketplace tab.
*   The `Submit File` action has limitations on supported file types.
