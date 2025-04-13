# Intezer

## Overview

This integration provides tools to interact with the Intezer platform for analyzing files, URLs, and hashes, managing alerts, and indexing files.

## Available Tools

### Detonate File

**Tool Name:** `intezer_detonate_file`

**Description:** Analyze a file from Splunk vault with Intezer.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): Path to file for analyzing. Multiple values can be provided as a comma-separated string.
*   `related_alert_id` (string, optional): The alert id related to the file. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an analysis ID.

---

### Get URL Report

**Tool Name:** `intezer_get_url_report`

**Description:** Get a URL analysis report based on a URL analysis ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `analysis_id` (string, required): Specify a comma-separated list of URL Analysis IDs to run the action on. Analysis ID is case sensitive. The analysis ID is returned when submitting a URL for analysis. Multiple values can be provided as a comma-separated string.
*   `wait_for_completion` (boolean, optional): Whether to wait for the analysis to finish. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the URL analysis report.

---

### Get File Report

**Tool Name:** `intezer_get_file_report`

**Description:** Get a file analysis report based on an analysis ID or a file hash.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `analysis_id` (string, optional): Specify a comma-separated list of File Analysis IDs to run the action on. Analysis ID is case sensitive. Note: if both "Analysis ID" and "File Hash" are provided, then "File Hash" value will have priority. Multiple values can be provided as a comma-separated string. Defaults to None.
*   `file_hash` (string, optional): Specify a comma-separated list of file hashes to run the action on. File Hash is case sensitive. Note: if both "Analysis ID" and "File Hash" are provided, then "File Hash" value will have priority. Multiple values can be provided as a comma-separated string. Defaults to None.
*   `private_only` (boolean, optional): Whether to show only private reports (relevant only for hashes). Defaults to None.
*   `wait_for_completion` (boolean, optional): Whether to wait for the analysis to complete before returning the report. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the file analysis report.

---

### Get Alert

**Tool Name:** `intezer_get_alert`

**Description:** Get an ingested alert triage and response information using alert ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): The alert id to query.
*   `wait_for_completion` (boolean, optional): Whether to wait for the analysis to finish. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including alert details.

---

### Unset Index File

**Tool Name:** `intezer_unset_index_file`

**Description:** Unset file's indexing.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `sha256` (string, optional): SHA256 file to unset the indexing. Multiple values can be provided as a comma-separated string. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on Filehash entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Detonate URL

**Tool Name:** `intezer_detonate_url`

**Description:** Analyze a suspicious URL with Intezer.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url` (string, optional): URL to analyze. Multiple values can be provided as a comma-separated string. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an analysis ID.

---

### Ping

**Tool Name:** `intezer_ping`

**Description:** Test connectivity to the Intezer with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Detonate Hash

**Tool Name:** `intezer_detonate_hash`

**Description:** Analyze a file hash (SHA1, SHA256, or MD5) on Intezer Analyze.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_hash` (string, optional): Hash of the desired report. Multiple values can be provided as a comma-separated string. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on Filehash entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an analysis ID or report link.

---

### Index File

**Tool Name:** `intezer_index_file`

**Description:** Index the file's genes into the organizational database.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `index_as` (List[Any], required): Index as trusted or malicious.
*   `sha256` (string, optional): Sha256 to index. Multiple values can be provided as a comma-separated string. Defaults to None.
*   `family_name` (string, optional): Family name to index as. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on Filehash entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Submit Alert

**Tool Name:** `intezer_submit_alert`

**Description:** Submit a new alert including the raw alert information to Intezer for processing.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source` (string, required): The source of the alert.
*   `raw_alert` (string, required): Alert raw data in JSON format.
*   `alert_mapping` (string, required): Mapping to use for the alert in JSON format.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an alert ID assigned by Intezer.

---

### Submit Suspicious Email

**Tool Name:** `intezer_submit_suspicious_email`

**Description:** Submit a suspicious phishing email in a raw format (.MSG or .EML) to Intezer for processing.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email_file_path` (string, required): Path to the email file.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an analysis ID.

---

### Submit File

**Tool Name:** `intezer_submit_file`

**Description:** Submit a file for analysis.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths` (string, required): The paths of the file to analyze.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an analysis ID.

---

### Submit Hash

**Tool Name:** `intezer_submit_hash`

**Description:** Submit a hash for analysis.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on Filehash entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including an analysis ID or report link.
