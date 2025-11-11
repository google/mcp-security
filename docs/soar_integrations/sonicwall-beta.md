# SonicWall-Beta SOAR Integration

## Overview

This integration (Beta) provides tools for interacting with SonicWall firewalls from within the Chronicle SOAR platform. It allows managing network objects like Address Groups and URI Lists/Groups, creating CFS Profiles, and testing connectivity. Note: Some actions require specific SonicOS versions and may commit uncommitted changes on the device.

## Tools

### `sonic_wall_beta_add_ip_to_address_group`

Add IP address to specific SonicWall Address Group. Caution: Successful action execution commits all uncommitted changes. This is a SonicWall limitation.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_name` (str, required): Specify to which group you want to add IP address. Groups that contain unicode characters are not supported. This is a SonicWall limitation.
*   `ip_zone` (str, required): Specify the zone of the IP address that you want to add.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_list_uri_groups`

List SonicWall URI Groups. Requires SonicOS 6.5.3 or higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_uri_groups_to_return` (Optional[str], optional, default=None): Specify how many URI Groups to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_list_address_groups`

List SonicWall Address Groups.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `address_type` (Optional[List[str]], optional, default=None): Specify which address type should be using for address groups.
*   `max_address_groups_to_return` (Optional[str], optional, default=None): Specify how many address groups to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_ping`

Test connectivity to the SonicWall with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_add_uri_list_to_uri_group`

Add URI List to SonicWall URI Group. Caution: Successful action execution commits all uncommitted changes. This is a SonicWall limitation. Requires SonicOS 6.5.3 or higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `uri_list_name` (str, required): Specify which URI List you want to add the URI Group. URI Lists that contain unicode characters are not supported. This is a SonicWall limitation.
*   `uri_group_name` (str, required): Specify to which URI Group you want to add the URI List. URI Groups that contain unicode characters are not supported. This is a SonicWall limitation.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_remove_ip_from_address_group`

Remove IP address from specific SonicWall Address Group. Caution: Successful action execution commits all uncommitted changes. This is a SonicWall limitation.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `group_name` (str, required): Specify from which group you want to remove the IP address. Groups that contain unicode characters are not supported. This is a SonicWall limitation.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_remove_url_from_uri_list`

Remove URL from specific SonicWall URI List. Caution: Successful action execution commits all uncommitted changes. This is a SonicWall limitation. Requires SonicOS 6.5.3 or higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `uri_list_name` (str, required): Specify to which URI List you want to add the URL. URI lists that contain unicode characters are not supported. This is a SonicWall limitation.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_create_cfs_profile`

Create SonicWall CFS Profile. Caution: Successful action execution commits all uncommitted changes. This is a SonicWall limitation. Requires SonicOS 6.5.3 or higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `name` (str, required): Specify the name of the CFS Profile. Unicode characters are not supported. This is a SonicWall limitation.
*   `search_order` (List[str], required): Specify the search order for the CFS Profile.
*   `operation_for_forbidden_uri` (List[str], required): Specify the operation for forbidden URI for the CFS Profile.
*   `enable_smart_filter` (bool, required): Enable Smart Filter.
*   `enable_google_safe_search` (bool, required): Enable Google Safe Search.
*   `enable_youtube_restricted_mode` (bool, required): Enable Youtube Restricted Mode.
*   `enable_bing_safe_search` (bool, required): Enable Bing Safe Search.
*   `allowed_uri_list_or_group` (Optional[str], optional, default=None): Specify the allowed URI list or group for the CFS Profile. URI List with unicode characters is not supported. This is a SonicWall limitation.
*   `forbidden_uri_list_or_group` (Optional[str], optional, default=None): Specify the forbidden URI list or group for the CFS Profile. Unicode characters are not supported. This is a SonicWall limitation.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_add_url_to_uri_list`

Add URL to specific SonicWall URI List. Caution: Successful action execution commits all uncommitted changes. This is a SonicWall limitation. Requires SonicOS 6.5.3 or higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `uri_list_name` (str, required): Specify to which URI List you want to add the URL. URI lists that contain unicode characters are not supported. This is a SonicWall limitation.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `sonic_wall_beta_list_uri_lists`

List SonicWall URI Lists. Requires SonicOS 6.5.3 or higher.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_uri_lists_to_return` (Optional[str], optional, default=None): Specify how many URI Lists to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
