# Falcon Sandbox Integration

## Overview

This integration allows you to connect to CrowdStrike Falcon Sandbox to submit files and URLs for analysis, search for existing reports based on various indicators, and retrieve analysis results.

## Configuration

The configuration for this integration (API endpoint, API key) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings. Note that some features, like fetching reports immediately after submission, might require a premium API key.

## Actions

### Search

Search Falcon Sandbox databases for existing scan reports and information about files and URLs based on various criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_name` (string, optional): Filename e.g. invoice.exe.
*   `file_type` (string, optional): e.g. docx.
*   `file_type_description` (string, optional): e.g. PE32 executable.
*   `verdict` (string, optional): e.g. 1 (1=whitelisted, 2=no verdict, 3=no specific threat, 4=suspicious, 5=malicious).
*   `av_multiscan_range` (string, optional): e.g. 50-70 (min 0, max 100).
*   `av_family_substring` (string, optional): e.g. Agent.AD, nemucod.
*   `hashtag` (string, optional): e.g. ransomware.
*   `port` (string, optional): e.g. 8080.
*   `host` (string, optional): x.x.x.x.
*   `domain` (string, optional): e.g. checkip.dyndns.org.
*   `http_request_substring` (string, optional): e.g. google.
*   `similar_samples` (string, optional): e.g. <sha256>.
*   `sample_context` (string, optional): e.g. <sha256>.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Analyze File

Submit a file for analysis and optionally fetch the report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): The full path of the file to analyze.
*   `environment` (string, required): Environment ID. e.g. 100 (100=Windows 7 32 bit).
*   `include_report` (bool, optional): If enabled, action will fetch report related to the attachment. Note: this feature requires a premium key.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the submission details (like Job ID) and potentially the analysis report if requested and available.

### Wait For Job and Fetch Report

Wait for a scan job (submitted via Analyze File or Analyze File Url) to complete and fetch the scan report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `job_id` (string, required): The job id to fetch report for. For multiple, use comma separated values.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the analysis report(s) for the specified job ID(s).

### Ping

Test connectivity to Falcon Sandbox.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Analyze File Url

Submit a file by URL for analysis and fetch report.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_url` (string, required): The url to the file to analyze. e.g. http://tamzamaninda.net/office/Document.zip.
*   `environment` (string, required): Environment ID. e.g. 100 (100=Windows 7 32 bit).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the submission details (like Job ID) and potentially the analysis report.

### Get Hash Scan Report

Fetch hybrid analysis reports and enrich file hash entities based on existing reports in Falcon Sandbox.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the analysis reports found for the provided file hashes.

### Scan URL

Scan URL/domain for analysis.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if number of av detection is equal or above the given threshold.
*   `environment` (List[Any], required): The environment to use for the scan.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the scan submission and potentially enrichment data.

### Submit File

Submit files for analysis. This action differs from "Analyze File" as it doesn't automatically fetch the report. Use "Wait For Job and Fetch Report" subsequently.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): The full path of the file to analyze. For multiple, use comma separated values.
*   `environment` (List[Any], required): The environment to use for the scan.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the submission details, including the Job ID.

## Notes

*   Ensure the Falcon Sandbox integration is properly configured in the SOAR Marketplace tab with a valid API key.
*   Some actions or features (like immediate report fetching) may require a premium Falcon Sandbox API key.
*   Refer to the Falcon Sandbox documentation for valid Environment IDs.
