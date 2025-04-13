# Automox SOAR Integration

This document details the tools provided by the Automox SOAR integration.

## Tools

### `automox_list_policies`

List available policies in Automox.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_key` (Optional[List[Any]], optional, default=None): Specify the key that needs to be used to filter policy.
*   `filter_logic` (Optional[List[Any]], optional, default=None): Specify what filter logic should be applied. Filtering logic is working based on the value  provided in the “Filter Key” parameter.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If “Equal“ is selected, action will try to find the exact match among results and if “Contains“ is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value  provided in the “Filter Key” parameter.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return. If nothing is provided, action will return 50 records.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `automox_execute_policy`

Execute a policy in Automox. Supported entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `remediation_scope` (List[Any], required): Specify the remediation scope for the action. If “Only Entities” is selected, then action will execute policies only on the valid entities in the scope. If “All Devices” is selected, then action will execute the policy on all devices in the organization.
*   `policy_name` (str, required): Specify the name of the policy that needs to be executed.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `automox_ping`

Test connectivity to the Automox with parameters provided at the integration configuration page on the Marketplace tab

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `automox_enrich_entities`

Enrich entities using information from Automox. Supported entities: Hostname, IP Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `return_patches` (Optional[bool], optional, default=None): If enabled, action will return a list of patches that need to be updated on the machine. Note: action will not return patches that were installed or the ones that are currently ignored.
*   `max_patches_to_return` (Optional[str], optional, default=None): Specify how many patches to return. If nothing is provided, action will return 50 patches.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `automox_execute_device_command`

Execute a command on the endpoint in Automox. Supported entities: Hostname, IP Address. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `command` (Optional[List[Any]], optional, default=None): Specify a command that needs to be executed on the device. Note: if "Install Specific Patches" is provided, parameter "Patch Names" is mandatory.
*   `patch_names` (Optional[str], optional, default=None): Specify a comma-separated list of patches that need to be installed.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
