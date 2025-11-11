# SentinelOne V2 SOAR Integration

This document details the tools provided by the SentinelOne V2 SOAR integration.

## Overview

SentinelOne is an endpoint security platform that provides prevention, detection, and response capabilities across endpoints. This V2 integration allows Chronicle SOAR to interact with SentinelOne agents and the management console using updated APIs for investigation and response actions.

## Tools

### `sentinel_one_v2_add_threat_note`

Add a note to the threat in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threat_id` (str, required): Specify the id of the threat for which you want to add a note.
*   `note` (str, required): Specify the note that needs to be added to the threat.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_resolve_threat`

Resolve threats in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threat_i_ds` (str, required): Specify a comma-separated list of threat IDs that need to be resolved.
*   `annotation` (Optional[str], optional, default=None): Specify an annotation describing, why the threat can be resolved.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_blacklist`

Get a list of all the items available in the blacklist in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `hash` (Optional[str], optional, default=None): Specify a comma-separated list of hashes that need to be checked in blacklist. Only hashes that were found will be returned. If nothing is specified here action will return all hashes. Note: if "Hash" parameter is provided then "Limit" parameter is ignored.
*   `site_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of site ids, which should be used to return blacklist items.
*   `group_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of group ids, which should be used to return blacklist items.
*   `account_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of account ids, which should be used to return blacklist items.
*   `limit` (Optional[str], optional, default=None): Specify how many blacklist items should be returned. Note: if "Hash" parameter has values, then this parameter is ignored. Maximum is 1000.
*   `query` (Optional[str], optional, default=None): Specify the query that needs to be used in order to filter the results.
*   `use_global_blacklist` (Optional[bool], optional, default=None): If enabled, action will also return hashes from the global blacklist.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_create_hash_exclusion_record`

Add hash to the exclusion list in SentinelOne. Note: Only SHA1 hashes are supported.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `operation_system` (str, required): Specify the OS for the hash. Possible values: windows, windows_legacy, macos, linux.
*   `site_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of site ids, where hash needs to be sent to the exclusion list.
*   `group_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of group ids, where hash needs to be sent to the exclusion list.
*   `account_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of account ids, where hash needs to be sent to the exclusion list.
*   `description` (Optional[str], optional, default=None): Specify additional information related to the hash.
*   `add_to_global_exclusion_list` (Optional[bool], optional, default=None): If enabled, action will add the hash to the global exclusion list. Note: when this parameter is enabled, parameters “Site IDs“, “Group IDs“ and “Account IDs“ are ignored.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_system_status`

Fetch system status.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_disconnect_agent_from_network`

Disconnect agent from network by it's host name or IP address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_events_for_endpoint_hours_back`

Retrieve information about the latest events on the endpoint. Works with IP and Hostname entities.Note: this action uses an endpoint that has rate limiting. Only one endpoint can be processed per minute․

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `hours_back` (str, required): Specify how many hours backwards to fetch events.
*   `events_amount_limit` (Optional[str], optional, default=None): Specify how many events to return per event type. Default: 50.
*   `include_file_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about file events.
*   `include_indicator_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about indicator events.
*   `include_dns_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about DNS events.
*   `include_network_actions_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about “network actions“ events.
*   `include_url_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about URL events.
*   `include_registry_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about registry events.
*   `include_scheduled_task_events_information` (Optional[bool], optional, default=None): If enabled, action will also query information about scheduled task events.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_create_path_exclusion_record`

Add path to the exclusion list in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `path` (str, required): Specify the path that needs to be added to the exclusion list.
*   `operation_system` (str, required): Specify the OS for the path. Possible values: windows, windows_legacy, macos, linux.
*   `site_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of site ids, where path needs to be sent to the exclusion list.
*   `group_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of group ids, where path needs to be sent to the exclusion list.
*   `account_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of account ids, where path needs to be sent to the exclusion list.
*   `description` (Optional[str], optional, default=None): Specify additional information related to the path.
*   `add_to_global_exclusion_list` (Optional[bool], optional, default=None): If enabled, action will add the path to the global exclusion list. Note: when this parameter is enabled, parameters “Site IDs“, “Group IDs“ and “Account IDs“ are ignored.
*   `include_subfolders` (Optional[bool], optional, default=None): If enabled, action will include subfolders for the provided path. This feature only works, if user provides folder path and not file path.
*   `mode` (Optional[List[str]], optional, default=None): Specify what mode should be used for the excluded path.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_deep_visibility_query_result`

Retrieve information about deep visibility query results. Note: this action should be used in combination with “Initiate Deep Visibility Query“.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query_id` (str, required): Specify the ID of the query for which you want to return results. This ID is available in the JSON result of the action “Initiate Deep Visibility Query“ as “query_id“ parameter.
*   `limit` (Optional[str], optional, default=None): Specify how many events to return. Default: 50. Maximum is 100.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_initiate_deep_visibility_query`

Initiate a Deep Visibility Query search. Returns query id, which should be used in the action "Get Deep Visibility Query Result".

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query for the search.
*   `start_date` (Optional[str], optional, default=None): Specify the start date for the search. If nothing is specified, action will fetch events from 30 days ago.
*   `end_date` (Optional[str], optional, default=None): Specify the end date for the search. If nothing is specified, action will use current time.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_threats`

Retrieve information about threats in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `mitigation_status` (Optional[str], optional, default=None): Specify the comma-separated list of threat statuses. Only threats that match the statuses will be returned. Possible values: mitigated, active, blocked, suspicious, suspicious_resolved
*   `created_until` (Optional[str], optional, default=None): Specify the end time for the threats. Example: 2020-03-02T21:30:13.014874Z
*   `created_from` (Optional[str], optional, default=None): Specify the start time for the threats. Example: 2020-03-02T21:30:13.014874Z
*   `resolved_threats` (Optional[bool], optional, default=None): If enabled, action will only return resolved threats.
*   `threat_display_name` (Optional[str], optional, default=None): Specify a display name of the threat that you want to return. Partial name will also work.
*   `limit` (Optional[str], optional, default=None): Specify how many threats to return. Default: 10.
*   `api_version` (Optional[List[str]], optional, default=None): Specify what version of API to use in the action. If nothing is provided connector will use version 2.1. Note: JSON result structure is different between API versions. It is recommended to use the latest one.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_enrich_endpoint`

Enrich information about the endpoint by IP address or Hostname.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `create_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight with information about endpoints.
*   `only_infected_endpoints_insights` (Optional[bool], optional, default=None): If enabled, action will only create insights for the infected endpoints.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_initiate_full_scan`

Initiate a full disk scan on the endpoint in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_mark_as_threat`

Marks suspicious threats as a true positive threat in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threat_i_ds` (str, required): Specify a comma-separated list of threat IDs that should be marked.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_ping`

Test integration connectivity.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_delete_hash_blacklist_record`

Delete hashes from a blacklist in SentinelOne. Note: Only SHA1 hashes are supported.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `site_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of site ids, from where the hash needs to be removed.
*   `group_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of group ids, from where the hash needs to be removed.
*   `account_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of account ids, from where the hash needs to be removed.
*   `remove_from_global_black_list` (Optional[bool], optional, default=None): If enabled, action will remove the hash from the global black list. Note: when this parameter is enabled, parameters "Site IDs", "Group IDs" and "Account IDs" are ignored.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_system_version`

Fetch system version.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_update_incident_status`

Update threat incident status in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threat_id` (str, required): Specify a comma-separated list of threat ids for which you want to update the incident status.
*   `status` (List[str], required): Specify the incident status.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_mitigate_threat`

Executes mitigation actions on the threats in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `mitigation_action` (List[str], required): Specify the mitigation actions for the provided threats.
*   `threat_i_ds` (str, required): Specify a comma-separated list of threat IDs that should be mitigated.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_download_threat_file`

Download file related to threat in SentinelOne. Note: Your user role must have permissions to Fetch Threat File - Admin, IR Team, SOC.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threat_id` (str, required): Specify the id of the threat for which you want to download the file.
*   `password` (str, required): Specify the password for the zip that contains the threat file. Password requirements: At least 10 characters. Three of these: uppercase, lowercase, digits, special symbols. Maximum length is 256 characters.
*   `download_folder_path` (str, required): Specify the path to the folder, where you want to store the threat file.
*   `overwrite` (bool, required): If enabled, action will overwrite the file with the same name.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_agent_status`

Retrieve information about the status of the agents on the endpoints based on the IP or Hostname entity.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_list_sites`

List available sites in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_key` (Optional[List[str]], optional, default=None): Specify the key that needs to be used to filter sites.
*   `filter_logic` (Optional[List[str]], optional, default=None): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value  provided in the "Filter Key" parameter.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_create_hash_blacklist_record`

Add hashes to a blacklist in SentinelOne. Note: Only SHA1 hashes are supported.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `operating_system` (str, required): Specify the OS for the hash. Possible values: windows, windows_legacy, macos, linux.
*   `add_to_global_black_list` (bool, required): If enabled, action will add the hash to the global blacklist. Note: when this parameter is enabled, parameters “Site IDs“, “Group IDs“ and “Account IDs“ are ignored.
*   `site_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of site ids, where hash needs to be sent to the blacklist.
*   `group_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of group ids, where hash needs to be sent to the blacklist.
*   `account_i_ds` (Optional[str], optional, default=None): Specify a comma-separated list of account ids, where hash needs to be sent to the blacklist.
*   `description` (Optional[str], optional, default=None): Specify additional information related to the hash.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_reconnect_agent_to_the_network`

Reconnect disconnected endpoint to the network. Works with Hostname and IP entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_application_list_for_endpoint`

Retrieve information about available applications on the endpoint by IP or Hostname.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_applications_to_return` (Optional[str], optional, default=None): Specify how many applications to return. If nothing is specified action will return all of the applications.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_hash_reputation`

Retrieve information about the hashes from SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `reputation_threshold` (Optional[str], optional, default=None): Specify what should be the reputation threshold in order it to be marked as suspicious. If nothing is provided, action will not mark entites as suspicious. Maximum: 10.
*   `create_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight containing information about the reputation.
*   `only_suspicious_hashes_insight` (Optional[bool], optional, default=None): If enabled, action will only create insight for hashes that have higher or equal reputation to “Reputation Threshold“ value.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_get_group_details`

Retrieve detailed information about the provided groups.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_names` (str, required): Specify a comma-separated list of group names for which you want to retrieve details.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_update_analyst_verdict`

Update analyst verdict of the threat in SentinelOne.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threat_id` (str, required): Specify a comma-separated list of threat ids for which you want to update the analyst verdict.
*   `analyst_verdict` (List[str], required): Specify the analyst verdict.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sentinel_one_v2_move_agents`

Move agents to the provided group. This action works with Hostname and IP address entities. Note: the group should be from the same site.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_id` (Optional[str], optional, default=None): Specify the ID of the group, where to move the agents.
*   `group_name` (Optional[str], optional, default=None): Specify the name of the group, where to move the agents. Note: if both Group ID and Group Name are provided, action will put “Group ID“ in the priority.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
