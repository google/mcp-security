# LogRhythm

## Overview

This integration provides tools to interact with the LogRhythm SIEM platform, allowing you to manage cases, alarms, evidence, and enrich entities.

## Available Tools

### Add Alarm To Case

**Tool Name:** `log_rhythm_add_alarm_to_case`

**Description:** Add alarm to case in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alarm_i_ds` (string, required): Specify a comma-separated list of alarms that need to be added to the case.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Download Case Files

**Tool Name:** `log_rhythm_download_case_files`

**Description:** Download files related to the case in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `download_folder_path` (string, required): Specify the path to the folder, where you want to store the case files.
*   `overwrite` (bool, required): If enabled, action will overwrite the file with the same name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Entity Events

**Tool Name:** `log_rhythm_list_entity_events`

**Description:** List events related to entities in LogRhythm. Supported entities: Hostname, IP Address, User, CVE, Hash, URL. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `time_frame` (Optional[List[Any]], optional): Specify a time frame for the results. If “Custom” is selected, you also need to provide “Start Time”. Defaults to None.
*   `start_time` (Optional[str], optional): Specify the start time for the results. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601. Example: 2021-04-23T12:38Z. Defaults to None.
*   `end_time` (Optional[str], optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time. Defaults to None.
*   `sort_order` (Optional[List[Any]], optional): Specify the sorting logic for the query. Defaults to None.
*   `max_events_to_return` (Optional[str], optional): Specify how many events to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including a list of events related to the specified entities.

---

### Get Alarm Details

**Tool Name:** `log_rhythm_get_alarm_details`

**Description:** Get alarm details in LogRhythm

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alarm_i_ds` (string, required): Specify a comma-separated list of alarm IDs for which we need to retrieve details.
*   `max_events_to_fetch` (Optional[str], optional): Specify how many events to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including detailed information about the specified alarms.

---

### Ping

**Tool Name:** `log_rhythm_ping`

**Description:** Test connectivity to the LogRhythm with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Note To Case

**Tool Name:** `log_rhythm_add_note_to_case`

**Description:** Add a note to the case in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `note` (string, required): Specify a note that should be added to the case.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Case

**Tool Name:** `log_rhythm_update_case`

**Description:** Update a case in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (Optional[str], optional): Specify a new name for the case. Defaults to None.
*   `priority` (Optional[List[Any]], optional): Specify a new priority for the case. Defaults to None.
*   `due_date` (Optional[str], optional): Specify a new due date for the case. Format: ISO 8601. Example: 2021-04-23T12:38Z. Defaults to None.
*   `description` (Optional[str], optional): Specify a new description for the case. Defaults to None.
*   `resolution` (Optional[str], optional): Specify how the case was resolved. Defaults to None.
*   `status` (Optional[List[Any]], optional): Specify the new status for the case. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Create Case

**Tool Name:** `log_rhythm_create_case`

**Description:** Create a case in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name for the case.
*   `priority` (List[Any], required): Specify the priority for the case.
*   `due_date` (Optional[str], optional): Specify the due date for the case. Format: ISO 8601. Example: 2021-04-23T12:38Z. Defaults to None.
*   `description` (Optional[str], optional): Specify a description for the case. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the ID of the newly created case.

---

### Add Comment To Alarm

**Tool Name:** `log_rhythm_add_comment_to_alarm`

**Description:** Add comment to alarm in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alarm_id` (string, required): Specify the ID of the alarm to which you need to add a comment in LogRhythm.
*   `comment` (string, required): Specify a comment that needs to be added to the alarm.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Case Evidence

**Tool Name:** `log_rhythm_list_case_evidence`

**Description:** List case evidence in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `status_filter` (Optional[str], optional): Specify a comma-separated list of status filters for the evidence. Possible values: pending, completed, failed. If nothing is provided, action will return evidence from all statuses. Defaults to None.
*   `type_filter` (Optional[str], optional): Specify a comma-separated list of type filters for the evidence. Possible values: alarm, userEvents, log, note, file. If nothing is provided, action will return evidence from all types. Defaults to None.
*   `max_evidences_to_return` (Optional[str], optional): Specify how much evidence to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including a list of case evidence items.

---

### Attach File To Case

**Tool Name:** `log_rhythm_attach_file_to_case`

**Description:** Attach file to case in LogRhythm. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_paths` (string, required): Specify a comma-separate list of absolute file paths.
*   `note` (Optional[str], optional): Specify a note that should be added to the case alongside the file. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Alarm

**Tool Name:** `log_rhythm_update_alarm`

**Description:** Update Alarm in LogRhythm.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alarm_id` (string, required): Specify the ID of the alarm that needs to be updated in LogRhythm.
*   `status` (Optional[List[Any]], optional): Specify the status for the alarm. Defaults to None.
*   `risk_score` (Optional[str], optional): Specify a new risk score for the alarm. Maximum: 100. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `log_rhythm_enrich_entities`

**Description:** Enrich entities using information from LogRhythm. Supported entities: Hostname, IP Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (Optional[bool], optional): If enabled, action will create an insight containing all of the retrieved information about the entity. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including enrichment data for the specified entities.
