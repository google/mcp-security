# Sophos SOAR Integration

## Overview

This integration provides tools for interacting with Sophos Central from within the Chronicle SOAR platform. It allows managing endpoints (scan, isolate, unisolate, get service status), managing alerts (list actions, execute actions), managing block/allow lists for file hashes, enriching entities, and retrieving event logs.

## Tools

### `sophos_list_alert_actions`

Retrieve actions that can be executed on the alert in Sophos.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alert_id` (str, required): Specify the ID of the alert for which you want to retrieve details.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_add_entities_to_blocklist`

Add entities to blocklist in Sophos. Supported entities: Filehash. Note: Only SHA-256 hashes are supported.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `comment` (str, required): Specify the comment explaining why the hash was sent to blocklist.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_get_services_status`

Retrieve information about services on endpoints in Sophos. Supported entities: IP Address, Hostname.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_ping`

Test connectivity to the Sophos with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_scan_endpoints`

Initiate a scan on endpoints in Sophos. Supported entities: IP Address, Hostname.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_enrich_entities`

Enrich entities using information from Sophos. Supported entities: Hostname, IP Address, File hash.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `create_insights` (Optional[bool], optional, default=None): If enabled, action will create an insight containing all of the retrieved information about the entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_add_entities_to_allowlist`

Add entities to allowlist in Sophos. Supported entities: Filehash. Note: Only SHA-256 hashes are supported.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `comment` (str, required): Specify the comment explaining why the hash was sent to allowlist.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_isolate_endpoint`

Isolate endpoints in Sophos. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `comment` (str, required): Specify the comment explaining why the isolation is needed.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_execute_alert_actions`

Initiate action execution on the alert in Sophos. Use action "List Alert Actions" to get a list of available actions for the alert.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alert_id` (str, required): Specify the ID of the alert on which you want to execute the action.
*   `action` (List[str], required): Specify an action that should be executed on the alert.
*   `message` (Optional[str], optional, default=None): Specify a message explaining why the action was executed.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_get_events_log`

Retrieve logs related to the endpoints in Sophos. Supported entities: IP Address, Hostname. Note: events are accessible from API only for 24 hours. Requires valid “SIEM API Root”, “API Key” and “Base 64 Auth Payload” provided in the integration configuration.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `timeframe` (str, required): Specify how many hours backwards events should be retrieved. Note: if the user provides more than 24 hours, action will still use 24.
*   `max_events_to_return` (Optional[str], optional, default=None): Specify how many events to return per entity. Maximum: 1000
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sophos_unisolate_endpoint`

Unisolate endpoints in Sophos. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `comment` (str, required): Specify the comment explaining why the unisolation is needed.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
