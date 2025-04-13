# Fortigate

## Overview

This integration provides tools to interact with Fortigate firewalls for managing policies and address groups.

## Available Tools

### Add Entities To Policy

**Tool Name:** `fortigate_add_entities_to_policy`

**Description:** Add entities to policy in Fortigate. Supported entities: URL, IP Address. Note: action will extract domain part of URL entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Specify the name of the policy to which action should add entities.
*   `location` (List[Any], optional): Specify the location for the entities. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Policies

**Tool Name:** `fortigate_list_policies`

**Description:** List available policies in Fortigate.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter policies. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Address Groups

**Tool Name:** `fortigate_list_address_groups`

**Description:** List available address groups in Fortigate.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter address groups. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Entities From Address Group

**Tool Name:** `fortigate_remove_entities_from_address_group`

**Description:** Remove entities from the address group in Fortigate. Supported entities: URL, IP Address. Note: action will extract domain part of URL entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_group_name` (string, required): Specify the name of the address group from which action should remove entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `fortigate_ping`

**Description:** Test connectivity to the Fortigate with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Entities From Policy

**Tool Name:** `fortigate_remove_entities_from_policy`

**Description:** Remove entities from the policy in Fortigate. Supported entities: URL, IP Address. Note: action will extract domain part of URL entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Specify the name of the policy from which action should remove entities.
*   `location` (List[Any], optional): Specify the location for the entities. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Entities To Address Group

**Tool Name:** `fortigate_add_entities_to_address_group`

**Description:** Add entities to the address group in Fortigate. Supported entities: URL, IP Address. Note: action will extract domain part of URL entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_group_name` (string, required): Specify the name of the address group to which action should add entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
