# Palo Alto Networks NGFW Integration

## Overview

This integration allows you to connect to Palo Alto Networks Next-Generation Firewalls (NGFW) or Panorama (when managing NGFWs) to manage security policies, address groups, URL categories, and commit changes.

## Configuration

The configuration for this integration (Firewall/Panorama IP/Hostname, Username, Password/API Key) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

**Important:** Actions require specifying the target `device_name` and `vsys_name`. Default values are `localhost.localdomain` and `vsys1` respectively. You can find the correct names by browsing the firewall/Panorama configuration via the provided URLs in the action descriptions or using the device's web interface/CLI. Alternatively, you can use `shared` objects if applicable.

## Actions

### Edit Blocked Applications

Block and unblock applications within a specific security policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name (e.g., `localhost.localdomain`).
*   `vsys_name` (string, required): The target virtual system name (e.g., `vsys1`).
*   `policy_name` (string, required): The name of the security policy to modify.
*   `applications_to_block` (string, optional): Comma-separated list of application names to add to the policy's block list (e.g., `apple-siri,app2`).
*   `applications_to_un_block` (string, optional): Comma-separated list of application names to remove from the policy's block list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy modification.

### Block IPs in Policy

Block IP addresses by adding them to a security policy's source or destination list.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name.
*   `vsys_name` (string, required): The target virtual system name.
*   `policy_name` (string, required): The name of the security policy to modify.
*   `target` (string, required): Specify whether to add IPs to the `source` or `destination` list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy modification.

### Add IPs to Group

Add IP addresses to an address group object.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_group_name` (string, required): The name of the address group to modify.
*   `device_name` (string, optional): The target device name. Defaults to `localhost.localdomain`.
*   `vsys_name` (string, optional): The target virtual system name. Defaults to `vsys1`.
*   `use_shared_objects` (bool, optional): If enabled, uses shared address objects/groups instead of vsys-specific ones. Note: Does not create the group if it doesn't exist.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the group modification.

### Commit Changes

Commit configuration changes made on the firewall or Panorama.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `only_my_changes` (bool, required): Commit only the changes made by the configured user (requires admin privileges). If false, commits all pending changes.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the commit operation, including the job ID.

### Ping

Test connectivity to the Palo Alto NGFW or Panorama instance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Unblock Urls

Remove URLs from a given custom URL category.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url_category_name` (string, required): The name of the custom URL category to modify.
*   `device_name` (string, optional): The target device name. Defaults to `localhost.localdomain`.
*   `vsys_name` (string, optional): The target virtual system name. Defaults to `vsys1`.
*   `use_shared_objects` (bool, optional): If enabled, uses shared URL category instead of vsys-specific one.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the URL category modification.

### Block Urls

Add URLs to a given custom URL category. (NOTE: To actually block the URL, ensure this category is used in a security policy with a block action). URLs cannot exceed 255 characters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `url_category_name` (string, required): The name of the custom URL category to modify.
*   `device_name` (string, optional): The target device name. Defaults to `localhost.localdomain`.
*   `vsys_name` (string, optional): The target virtual system name. Defaults to `vsys1`.
*   `use_shared_objects` (bool, optional): If enabled, uses shared URL category instead of vsys-specific one.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the URL category modification.

### Remove IPs from Group

Remove IP addresses from an address group object.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_group_name` (string, required): The name of the address group to modify.
*   `device_name` (string, optional): The target device name. Defaults to `localhost.localdomain`.
*   `vsys_name` (string, optional): The target virtual system name. Defaults to `vsys1`.
*   `use_shared_objects` (bool, optional): If enabled, uses shared address objects/groups instead of vsys-specific ones.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the group modification.

### Unblock IPs in Policy

Unblock IP addresses in a policy by removing them from the source or destination list.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name.
*   `vsys_name` (string, required): The target virtual system name.
*   `policy_name` (string, required): The name of the security policy to modify.
*   `target` (string, required): Specify whether to remove IPs from the `source` or `destination` list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the policy modification.

### Get Blocked Applications

List all blocked applications in a given security policy.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `device_name` (string, required): The target device name.
*   `vsys_name` (string, required): The target virtual system name.
*   `policy_name` (string, required): The name of the security policy to query.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of applications blocked by the specified policy.

## Notes

*   Ensure the Palo Alto NGFW integration is properly configured in the SOAR Marketplace tab.
*   Specify correct `device_name` and `vsys_name` or use `use_shared_objects` where applicable.
*   Committing changes is a separate step required after making configuration modifications like adding IPs or URLs.
*   Blocking URLs requires adding them to a custom URL category that is then used in a security policy with a block action.
