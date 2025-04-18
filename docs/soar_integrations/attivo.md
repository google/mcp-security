# Attivo SOAR Integration

This document details the tools provided by the Attivo SOAR integration.

## Tools

### `attivo_update_event`

Update event in Attivo.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `event_id` (str, required): Specify the ID of the event, which needs to be updated.
*   `status` (Optional[List[Any]], optional, default=None): Specify what status should be set for the event.
*   `comment` (Optional[str], optional, default=None): Specify a comment that needs to be added to the event.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `attivo_list_service_threat_paths`

List ThreatPaths related to services in Attivo.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `services` (str, required): Specify a comma-separated list of services for which action needs to return ThreatPaths.
*   `max_threat_paths_to_return` (Optional[str], optional, default=None): Specify how many ThreatPaths to return. If nothing is provided, action will return 50 ThreatPaths.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `attivo_ping`

Test connectivity to the Attivo with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `attivo_list_vulnerability_hosts`

List hosts related to the vulnerability in Attivo.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `vulnerabilities` (str, required): Specify a comma-separated list of vulnerabilities for which action needs to return hostnames.
*   `max_hosts_to_return` (Optional[str], optional, default=None): Specify how many hosts to return. If nothing is provided, action will return 50 hosts.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `attivo_enrich_entities`

Enrich entities using information from Attivo. Supported entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `include_threat_paths` (Optional[bool], optional, default=None): If enabled, action will return information about ThreatPaths related to the entity.
*   `include_vulnerabilities` (Optional[bool], optional, default=None): If enabled, action will return information about vulnerabilities related to the entity.
*   `include_credential_info` (Optional[bool], optional, default=None): If enabled, action will return information about credential information related to the entity.
*   `create_insights` (Optional[bool], optional, default=None): If enabled, action will create an insight containing all of the retrieved information about the entity.
*   `max_threat_paths_to_return` (Optional[str], optional, default=None): Specify how many ThreatPaths to return per entity. Default: 50.
*   `max_vulnerabilities_to_return` (Optional[str], optional, default=None): Specify how many vulnerabilities to return per entity. Default: 50.
*   `max_credentials_to_return` (Optional[str], optional, default=None): Specify how many credentials to return per entity. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `attivo_list_critical_threat_path`

List available critical ThreatPaths in Attivo.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_key` (Optional[List[Any]], optional, default=None): Specify the key that needs to be used to filter critical paths.
*   `filter_logic` (Optional[List[Any]], optional, default=None): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If “Equal“ is selected, action will try to find the exact match among results and if “Contains“ is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value  provided in the "Filter Key" parameter.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return. If nothing is provided, action will return 50 records.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
