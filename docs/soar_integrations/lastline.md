# Lastline

## Overview

This integration provides tools to interact with the Lastline analysis service (now part of VMware Carbon Black), allowing you to search analysis history and submit files or URLs for detonation.

## Available Tools

### Search Analysis History

**Tool Name:** `lastline_search_analysis_history`

**Description:** Search Lastline completed analysis tasks history. For submission either URL or Filehash in a format of md5 or sha1 can be provided. Note: Action is not working with Siemplify entities, only action input parameters are used.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_last_x_scans` (string, required): Search for report in last x analyses executed in Lastline.
*   `submission_name` (Optional[str], optional): Submission name to search for. Can be either URL or Filehash in a format of MD5 and SHA1. Defaults to None.
*   `submission_type` (Optional[List[Any]], optional): Optionally specify a submission type to search for, either URL or FileHash. Defaults to None.
*   `max_hours_backwards` (Optional[str], optional): Time frame for which to search for completed analysis tasks. Defaults to None.
*   `skip_first_x_scans` (Optional[str], optional): Skip first x scans returned by Lastline API. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including historical analysis task details.

---

### Ping

**Tool Name:** `lastline_ping`

**Description:** Test connectivity to the Lastline service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Analysis Results

**Tool Name:** `lastline_get_analysis_results`

**Description:** Enrich Siemplify FileHash or URL entities with the previously completed analysis tasks results. Note: Action supports filehash entity in md-5 and sha-1 formats. Note 2: Action always fetches the latest analysis available for the provided entity in Lastline.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if the score value for the entity is above the specified threshold.
*   `search_in_last_x_scans` (string, required): Search for report for provided entity in last x analyses executed in Lastline.
*   `create_insight` (Optional[bool], optional): Specify whether to create insight based on the report data. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on Filehash or URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including analysis results and enrichment data.

---

### Submit URL

**Tool Name:** `lastline_submit_url`

**Description:** Submit analysis task for the provided URL. Note: Action is not working with Siemplify entities, URL to analyze should be provided as action input parameter.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url_for_analysis` (string, required): Specify URL to analyze.
*   `wait_for_the_report` (Optional[bool], optional): Specify whether the action should wait for the report creation. Report also can be obtained later with Get Analysis Results action once scan is completed. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the submission status and potentially the analysis report if `wait_for_the_report` is true.

---

### Submit File

**Tool Name:** `lastline_submit_file`

**Description:** Submit analysis task for the provided URL. Note: Action is not working with Siemplify entities, full path to file to analyze should be provided as action input parameter.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): Specify full path to file to analyze.
*   `wait_for_the_report` (Optional[bool], optional): Specify whether the action should wait for the report creation. Report also can be obtained later with Get Analysis Results action once scan is completed. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the submission status and potentially the analysis report if `wait_for_the_report` is true.
