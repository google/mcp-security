# Cofense Triage Integration

## Overview

This integration allows you to connect to Cofense Triage to manage reported emails (reports), threat indicators, playbooks, and categories. Actions include adding tags/comments to reports, categorizing reports, executing playbooks, listing playbooks and categories, retrieving report details (headers, reporters, related indicators), downloading report components (email, preview), and enriching entities (URLs, domains, hashes).

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cofense Triage details:

*   **API URL:** The base URL of your Cofense Triage instance (e.g., `https://triage.cofense.com`).
*   **API Token:** An API token generated within Cofense Triage for authentication.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API token has the necessary permissions for the desired actions.)*

## Actions

### Add Tags To Report

Add tags to a report in Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the id of the report to which you want to add tags.
*   `tags` (string, required): Specify a comma-separated list of tags that need to be applied to the report.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the tag addition operation.

### Categorize Report

Categorize a report in Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the id of the report to categorize.
*   `category_name` (string, required): Specify the name of the category to apply. Use "List Categories" action to find available categories.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the categorization operation.

### Execute Playbook

Initiate a playbook execution in Cofense Triage for a specific report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the ID of the report on which you want to execute the playbook.
*   `playbook_name` (string, required): Specify the name of the playbook that needs to be executed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the playbook execution initiation.

### List Playbooks

List available playbooks in Cofense Triage, with optional filtering.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key to filter playbooks by (e.g., `name`).
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains). Note: "Equals" is case-sensitive, "Contains" is case-insensitive.
*   `filter_value` (string, optional): Specify the value to filter by.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50. Maximum: 200.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of playbooks matching the criteria.

### List Reports Related To Threat Indicators

List reports related to threat indicators (entities) in Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_case_wall_table` (bool, optional): If enabled, creates a case wall table with report information.
*   `max_reports_to_return` (string, optional): Specify how many reports to return per entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports various indicator types (IP, URL, Hash, Domain, etc.).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of related reports for the specified indicators.

### Get Report Headers

Return information about the header related to the report from Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the id of the report for which you want to retrieve headers.
*   `max_headers_to_return` (string, optional): Specify how many headers to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the header information for the specified report.

### Ping

Test connectivity to the Cofense Triage with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Domain Details

Return information about the domain from Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details about the specified domain(s).

### Get Report Reporters

Return information about the reporter related to the report from Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the id of the report for which you want to retrieve reporters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing information about the reporter(s) of the specified report.

### List Categories

List available categories in Cofense Triage, with optional filtering.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `names` (string, optional): Comma-separated list of category names to filter by.
*   `lowest_score_to_fetch` (string, optional): Specify the lowest accepted score for the category (can be negative).
*   `only_malicious` (bool, optional): If enabled, only return malicious categories.
*   `only_archived` (bool, optional): If enabled, only return archived categories.
*   `only_non_archived` (bool, optional): If enabled, return only non-archived categories.
*   `only_non_malicious` (bool, optional): If enabled, return only non-malicious categories.
*   `max_categories_to_return` (string, optional): Specify how many categories to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of categories matching the criteria.

### Get Threat Indicator Details

Return information about the entities based on the threat indicator details from Cofense Triage. Note: Only MD5 and SHA256 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports various indicator types (IP, URL, Hash, Domain, etc.).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing details about the specified threat indicators.

### Download Report Preview

Download image preview from the email related to the report from Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the ID of the report containing the preview.
*   `download_folder` (string, required): Specify the absolute path to the download folder. Filename will be `{report_id}.<format>`.
*   `image_format` (List[Any], required): Specify the format of the image (e.g., `png`, `jpg`).
*   `overwrite` (bool, optional): If enabled, overwrite existing file with the same name.
*   `create_insight` (bool, optional): If enabled, create an insight containing the raw email (if applicable, might be incorrect description).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including the path to the downloaded preview image.

### Download Report Email

Download raw email related to the report from Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_id` (string, required): Specify the ID of the report containing the raw email.
*   `download_folder` (string, required): Specify the absolute path to the download folder. Filename will be `{report_id}.eml`.
*   `overwrite` (bool, optional): If enabled, overwrite existing file with the same name.
*   `create_insight` (bool, optional): If enabled, create an insight containing the raw email.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including the path to the downloaded EML file.

### EnrichURL

Return information about the URL from Cofense Triage.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `risk_score_threshold` (string, required): Specify the risk score threshold (0-100) to label the URL as suspicious.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data (risk score, category, etc.) for the specified URL(s).

## Notes

*   Ensure the Cofense Triage integration is properly configured in the SOAR Marketplace tab with a valid API Token and Server URL.
*   The API token requires appropriate permissions within Cofense Triage for the desired actions.
*   File paths for download/upload actions must be accessible from the SOAR server or agent executing the action.
*   Hash enrichment currently supports only MD5 and SHA256.
