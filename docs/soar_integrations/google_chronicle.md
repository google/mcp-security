# Google Chronicle

## Overview

This integration provides tools to interact with Google Chronicle for managing rules, detections, reference lists, querying events, listing assets and IOCs, and enriching entities.

## Available Tools

### Get Rule Details

**Tool Name:** `google_chronicle_get_rule_details`

**Description:** Fetch information about a rule in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_id` (string, required): Specify the ID of the rule for which you want to fetch details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Detection Details

**Tool Name:** `google_chronicle_get_detection_details`

**Description:** Fetch information about a detection in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_id` (string, required): Specify the ID of the rule, which is related to the detection.
*   `detection_id` (string, required): Specify the ID of the detection for which you want to fetch details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute UDM Query

**Tool Name:** `google_chronicle_execute_udm_query`

**Description:** Execute custom UDM query in Google Chronicle. Note: 120 action executions are allowed per hour.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the query that needs to be executed in Chronicle.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Alert Time Till Now" is selected, action will use start time of the alert as start time for the search and end time will be current time. If "30 Minutes Around Alert Time" is selected, action will search the alerts 30 minutes before the alert happened till the 30 minutes after the alert has happened. Same idea applies to "1 Hour Around Alert Time" and "5 Minutes Around Alert Time". If "Custom" is selected, you also need to provide "Start Time". Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Note: The maximum time window (start time to end time) is 90 days. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Note: The maximum time window (start time to end time) is 90 days. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many results to return for the query. Default: 50. Maximum: 10000. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Values From Reference List

**Tool Name:** `google_chronicle_remove_values_from_reference_list`

**Description:** Remove values from a reference list in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `reference_list_name` (string, required): Specify the display name of the reference list that needs to be updated.
*   `values` (string, required): Specify a comma-separated list of values that need to be removed from a reference list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Values To Reference List

**Tool Name:** `google_chronicle_add_values_to_reference_list`

**Description:** Add values to a reference list in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `reference_list_name` (string, required): Specify the display name of the reference list that needs to be updated.
*   `values` (string, required): Specify a comma-separated list of values that need to be added to a reference list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List IOCs

**Tool Name:** `google_chronicle_list_io_cs`

**Description:** List all of the IoCs discovered within your enterprise within the specified time range.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `start_time` (string, optional): Fetches IOC Domain from the specified time. Value should be in RFC 3339 format (e.g. 2018-11-05T12:00:00Z). If not supplied, the default is the UTC time corresponding to 3 days earlier than current time. Defaults to None.
*   `max_io_cs_to_fetch` (string, optional): Specify the maximum number of IoCs to return. You can specify between 1 and 10,000. The default is 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich IP

**Tool Name:** `google_chronicle_enrich_ip`

**Description:** Enrich IP entities using information from IOCs in Google Chronicle. Supported entities: IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `lowest_suspicious_severity` (List[Any], required): Specify the lowest severity that should be associated with IP in order to mark it suspicious.
*   `mark_suspicious_n_a_severity` (boolean, required): If enabled, action will mark the entity as suspicious, if information about severity is not available.
*   `create_insight` (boolean, optional): If enabled, action will create an insight containing information about the entities. Defaults to None.
*   `only_suspicious_insight` (boolean, optional): If enabled, action will only create an insight for entities that are marked as suspicious. Note: "Create Insight" parameter needs to be enabled. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_chronicle_ping`

**Description:** Test connectivity to the Google Chronicle with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Events

**Tool Name:** `google_chronicle_list_events`

**Description:** List events on the particular asset in the specified time frame. Supported entities: IP Address, Mac Address, Hostname. Note: action can only fetch 10000 events. Make sure to narrow down the timeframe for better results.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `output` (List[Any], required): Specify what should be the output for this action.
*   `event_types` (string, optional): Specify a comma-separated list of the event types that need to be returned. If nothing is provided, action will fetch all event types. Possible values: EVENTTYPE_UNSPECIFIED, PROCESS_UNCATEGORIZED, PROCESS_LAUNCH, PROCESS_INJECTION, PROCESS_PRIVILEGE_ESCALATION, PROCESS_TERMINATION, PROCESS_OPEN, PROCESS_MODULE_LOAD, REGISTRY_UNCATEGORIZED, REGISTRY_CREATION, REGISTRY_MODIFICATION, REGISTRY_DELETION, SETTING_UNCATEGORIZED, SETTING_CREATION, SETTING_MODIFICATION, SETTING_DELETION, MUTEX_UNCATEGORIZED, MUTEX_CREATION, FILE_UNCATEGORIZED, FILE_CREATION, FILE_DELETION, FILE_MODIFICATION, FILE_READ, FILE_COPY, FILE_OPEN, FILE_MOVE, FILE_SYNC, USER_UNCATEGORIZED, USER_LOGIN, USER_LOGOUT, USER_CREATION, USER_CHANGE_PASSWORD, USER_CHANGE_PERMISSIONS, USER_STATS, USER_BADGE_IN, USER_DELETION, USER_RESOURCE_CREATION, USER_RESOURCE_UPDATE_CONTENT, USER_RESOURCE_UPDATE_PERMISSIONS, USER_COMMUNICATION, USER_RESOURCE_ACCESS, USER_RESOURCE_DELETION, GROUP_UNCATEGORIZED, GROUP_CREATION, GROUP_DELETION, GROUP_MODIFICATION, EMAIL_UNCATEGORIZED, EMAIL_TRANSACTION, EMAIL_URL_CLICK, NETWORK_UNCATEGORIZED, NETWORK_FLOW, NETWORK_CONNECTION, NETWORK_FTP, NETWORK_DHCP, NETWORK_DNS, NETWORK_HTTP, NETWORK_SMTP, STATUS_UNCATEGORIZED, STATUS_HEARTBEAT, STATUS_STARTUP, STATUS_SHUTDOWN, STATUS_UPDATE, SCAN_UNCATEGORIZED, SCAN_FILE, SCAN_PROCESS_BEHAVIORS, SCAN_PROCESS, SCAN_HOST, SCAN_VULN_HOST, SCAN_VULN_NETWORK, SCAN_NETWORK, SCHEDULED_TASK_UNCATEGORIZED, SCHEDULED_TASK_CREATION, SCHEDULED_TASK_DELETION, SCHEDULED_TASK_ENABLE, SCHEDULED_TASK_DISABLE, SCHEDULED_TASK_MODIFICATION, SYSTEM_AUDIT_LOG_UNCATEGORIZED, SYSTEM_AUDIT_LOG_WIPE, SERVICE_UNSPECIFIED, SERVICE_CREATION, SERVICE_DELETION, SERVICE_START, SERVICE_STOP, SERVICE_MODIFICATION, GENERIC_EVENT, RESOURCE_CREATION, RESOURCE_DELETION, RESOURCE_PERMISSIONS_CHANGE, RESOURCE_READ, RESOURCE_WRITTEN, ANALYST_UPDATE_VERDICT, ANALYST_UPDATE_REPUTATION, ANALYST_UPDATE_SEVERITY_SCORE, ANALYST_UPDATE_STATUS, ANALYST_ADD_COMMENT. Defaults to None.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time". Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Note: value "now" can also be used. Defaults to None.
*   `reference_time` (string, optional): Specify the reference time for the event search. Format: YYYY-MM-DDThh:mmTZD. Note: if nothing is provided, action will use end time as reference time. Defaults to None.
*   `max_events_to_return` (string, optional): Specify how many events to process per entity type. Default: 100. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Retrohunt

**Tool Name:** `google_chronicle_execute_retrohunt`

**Description:** Execute a rule retrohunt in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_id` (string, required): Specify the ID of the rule for which you want to run retrohunt.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If “Alert Time Till Now” is selected, action will use start time of the alert as start time for the search and end time will be current time. If “30 Minutes Around Alert Time” is selected, action will search the alerts 30 minutes before the alert happened till the 30 minutes after the alert has happened. Same idea applies to “1 Hour Around Alert Time” and “5 Minutes Around Alert Time”. If “Custom” is selected, you also need to provide “Start Time”. Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Is Value In Reference List

**Tool Name:** `google_chronicle_is_value_in_reference_list`

**Description:** Check, if provided values are found in reference lists in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `reference_list_names` (string, required): Specify a comma-separated list of display names of the reference list that needs to be searched.
*   `values` (string, required): Specify a comma-separated list of values that need to be searched in reference lists.
*   `case_insensitive_search` (boolean, optional): If enabled, action will perform case insensitive matching. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Assets

**Tool Name:** `google_chronicle_list_assets`

**Description:** List assets in Google Chronicle based on the related entities in the specified time frame. Supported entities: URL, IP Address, File hash. Only MD5, SHA-1 or SHA-256 hashes are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_hours_backwards` (string, optional): Specify how many hours backwards to fetch the assets. Default: 1 hour. Defaults to None.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time". If the "Max Hours Backwards" parameter is provided then action will use the "Max Hours Backwards" parameter to provide a time filter. This is done for backwards compatibility. Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Defaults to None.
*   `max_assets_to_return` (string, optional): Specify how many assets to return in the response. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Lookup Similar Alerts

**Tool Name:** `google_chronicle_lookup_similar_alerts`

**Description:** Lookup similar alerts in Google Chronicle. Supported Chronicle alert types: RULE, EXTERNAL, IOC. Note: this action can only work with alerts that come from the "Chronicle Alerts Connector". Note: action can only fetch 10000 alerts. Make sure to narrow down the timeframe for better results.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `io_cs_assets` (string, required): Specify a comma-separated list of IOCs or assets that you want to find in the alerts. Note: action will perform a different search for each item provided.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Alert Time Till Now" is selected, action will use start time of the alert as start time for the search and end time will be current time. If "30 Minutes Around Alert Time" is selected, action will search the alerts 30 minutes before the alert happened till the 30 minutes after the alert has happened. Same idea applies to "1 Hour Around Alert Time" and "5 Minutes Around Alert Time". Defaults to None.
*   `similarity_by` (List[Any], optional): Specify what attributes need to be used, when the action is to search for similar alerts. If "Alert Name and Alert Type" is selected, action will try to find all of the alerts that have the same alert name and IOCs/Assets for the underlying alert type. If "Product" is selected, then action will try to find all of the alerts that originate from the same product and have the same IOCs/Assets, action will search among both "EXTERNAL" and "Rule" alerts. If "Only IOCs/Assets" is enabled, action will match the similarity only based upon the items provided in the parameter "IOCs/Assets", action will search among both "EXTERNAL" and "Rule" alerts. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Domain

**Tool Name:** `google_chronicle_enrich_domain`

**Description:** Enrich domains using information from IOCs in Google Chronicle. Supported entities: Hostname, URL (action extracts domain part).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `lowest_suspicious_severity` (List[Any], required): Specify the lowest severity that should be associated with domain in order to mark it suspicious.
*   `mark_suspicious_n_a_severity` (boolean, required): If enabled, action will mark the entity as suspicious, if information about severity is not available.
*   `create_insight` (boolean, optional): If enabled, action will create an insight containing information about the entities. Defaults to None.
*   `only_suspicious_insight` (boolean, optional): If enabled, action will only create an insight for entities that are marked as suspicious. Note: "Create Insight" parameter needs to be enabled. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Reference Lists

**Tool Name:** `google_chronicle_get_reference_lists`

**Description:** Get available reference lists in Google Chronicle.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter reference lists. Name option refers to a display name of the reference list. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If “Equal“ is selected, action will try to find the exact match among results and if “Contains“ is selected, action will try to find results that contain that substring. “Equal” works with “title” parameter, while “Contains” works with all values in response. If nothing is provided in this parameter, the filter will not be applied. Defaults to None.
*   `expanded_details` (boolean, optional): If enabled, action will return detailed information about the reference lists. Defaults to None.
*   `max_reference_lists_to_return` (string, optional): Specify how many reference lists to return. Default: 100. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
