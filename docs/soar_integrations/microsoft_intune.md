# Microsoft Intune Integration

## Overview

This integration allows you to connect to Microsoft Intune to manage devices, including actions like remote lock, sync, locate, wipe, reset passcode, list devices, and test connectivity.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Remote Lock Managed Device

Remote lock managed device. The action starts the task; check status using "Get Managed Device". Supports Hostname or Host ID entities/parameters. Host ID takes priority if both are provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `host_name` (string, optional): Comma-separated list of host names to run the action on. Case insensitive. If not running on a hostname entity, can use this or Host ID.
*   `host_id` (string, optional): Comma-separated list of host ids to run the action on. Takes priority over Host Name if both are provided.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and Host ID entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Managed Devices

List managed devices available in the Microsoft Intune instance based on provided criteria. Note: This action doesn't run on Chronicle SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter managed devices.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equals, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50. Maximum: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of managed devices matching the criteria.

### Sync Managed Device

Sync managed device with the Microsoft Intune service. Supports Hostname or Host ID entities/parameters. Host ID takes priority if both are provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `host_name` (string, optional): Comma-separated list of host names to run the action on. Case insensitive.
*   `host_id` (string, optional): Comma-separated list of host ids to run the action on. Takes priority over Host Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and Host ID entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Microsoft Intune service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Locate Managed Device

Locate managed device with the Microsoft Intune service. The action starts the task; check status using "Get Managed Device". Supports Hostname or Host ID entities/parameters. Host ID takes priority if both are provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `host_name` (string, optional): Comma-separated list of host names to run the action on. Case insensitive.
*   `host_id` (string, optional): Comma-separated list of host ids to run the action on. Takes priority over Host Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and Host ID entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Wipe Managed Device

Wipe managed device with the Microsoft Intune service. Supports Hostname or Host ID entities/parameters. Host ID takes priority if both are provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `host_name` (string, optional): Comma-separated list of host names to run the action on. Case insensitive.
*   `host_id` (string, optional): Comma-separated list of host ids to run the action on. Takes priority over Host Name.
*   `keep_enrollment_data` (bool, optional): If enabled, keep enrollment data on the device.
*   `keep_user_data` (bool, optional): If enabled, keep user data on the device.
*   `persist_esim_data_plan` (bool, optional): If enabled, persist esim data plan for the device.
*   `mac_os_unlock_code` (string, optional): Specify if applicable Mac OS unlock code.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and Host ID entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Managed Device

Get managed device information from the Microsoft Intune service, including information on specific actions (e.g., locate device in "deviceActionResults"). Supports Hostname or Host ID entities/parameters. Host ID takes priority if both are provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `host_name` (string, optional): Specify the host name to run the action on. Case insensitive.
*   `host_id` (string, optional): Specify the host id to run the action on. Takes priority over Host Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and Host ID entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the managed device information.

### Reset Managed Device Passcode

Reset managed device passcode. The action starts the task; check status using "Get Managed Device". Supports Hostname or Host ID entities/parameters. Host ID takes priority if both are provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `host_name` (string, optional): Comma-separated list of host names to run the action on. Case insensitive.
*   `host_id` (string, optional): Comma-separated list of host ids to run the action on. Takes priority over Host Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and Host ID entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the Microsoft Intune integration is properly configured in the SOAR Marketplace tab.
*   Many actions support targeting devices via Hostname or Host ID, with Host ID taking precedence if both are supplied.
*   Some actions (Remote Lock, Locate Device, Reset Passcode) initiate tasks. Use the "Get Managed Device" action to check the status of these tasks via the `deviceActionResults` field in the response.
