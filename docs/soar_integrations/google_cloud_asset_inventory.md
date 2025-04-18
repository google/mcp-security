# Google Cloud Asset Inventory

## Overview

This integration provides tools to interact with the Google Cloud Asset Inventory API for retrieving information about cloud resources and service account roles.

## Available Tools

### Get Resource Snapshot

**Tool Name:** `google_cloud_asset_inventory_get_resource_snapshot`

**Description:** Get information about the resource using Google Cloud Asset Inventory.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_names` (string, required): Specify a comma-separated list of resources for which you want to fetch details.
*   `fields_to_return` (string, optional): Specify a comma-separated list of fields to return. Note: every field should be in format with "assets.{field}". Example of values: assets.asset.name, assets.asset.assetType,assets.asset.resource.data. Note: assets.asset.name will always be returned. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Resource

**Tool Name:** `google_cloud_asset_inventory_enrich_resource`

**Description:** Enrich information about a Google Cloud resource using Google Cloud Asset Inventory.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `resource_names` (string, required): Specify a comma-separated list of resources for which you want to fetch details.
*   `fields_to_return` (string, optional): Specify a comma-separated list of fields to return. Example of values: assetType,project,folders,organization,displayName,description,location,labels,networkTags,kmsKeys,createTime,updateTime,state,additionalAttributes, parentFullResourceName, parentAssetType. Note: name will always be returned. There is also an option to provide more advanced filters. For example, if you want to return a specific key from the "additionalAttributes" you can provide "additionalAttributes.{key}". Also, if you want to exclude a specific key from "additionalAttributes",then you can provide "-additionalAttributes.{key}". Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_asset_inventory_ping`

**Description:** Test connectivity to the Google Cloud Asset Inventory with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Service Account Roles

**Tool Name:** `google_cloud_asset_inventory_list_service_account_roles`

**Description:** List roles related to the Google Cloud service account using Google Cloud Asset Inventory.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `service_accounts` (string, required): Specify a comma-separated list of service accounts for which you want to fetch details.
*   `max_roles_to_return` (string, required): Specify how many roles related to the service account to return.
*   `max_permissions_to_return` (string, required): Specify how many permissions related to the service account to return.
*   `check_roles` (string, optional): Specify a comma-separated list of roles that you want to check in relation to the service account. Example: roles/cloudasset.owner. Defaults to None.
*   `check_permissions` (string, optional): Specify a comma-separated list of permission that you want to check in relation to the service account. Example: cloudasset.assets.listResource. Defaults to None.
*   `expand_permissions` (boolean, optional): If enabled, action will return information about all of the unique permissions related to the resource. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
