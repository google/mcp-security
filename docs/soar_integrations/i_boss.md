# iBoss Cloud Security

## Overview

This integration provides tools to interact with the iBoss Cloud Security platform for managing policy block lists and performing URL lookups and recategorization.

## Available Tools

### List Policy Block List Entries

**Tool Name:** `i_boss_list_policy_block_list_entries`

**Description:** Return iBoss Block List entries in a specific group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `category_id` (string, required): Specify in which policy category do you want to list Block List entries.
*   `max_entries_to_return` (string, optional): Specify how many entries to return. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove URL from Policy Block List

**Tool Name:** `i_boss_remove_url_from_policy_block_list`

**Description:** Remove URL from iBoss Block List.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `category_id` (string, required): Specify from which policy category do you want to remove the URL.
*   `start_port` (string, optional): Specify start port related to the URL that needs to be deleted. This parameter is mandatory, if the desired URL has a defined start port. This is an IBoss limitation. Defaults to None.
*   `end_port` (string, optional): Specify end port related to the URL that needs to be deleted. This parameter is mandatory, if the desired URL has a defined end port. This is an IBoss limitation. Defaults to None.
*   `strip_scheme` (boolean, optional): If enabled, action will strip the scheme related to the URL. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### URL Lookup

**Tool Name:** `i_boss_url_lookup`

**Description:** Perform URL Lookup.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `group_id` (string, optional): Specify for which group to perform a URL Lookup. If nothing is specified, “Default” group will be used. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including categorization information.

---

### URL Recategorization

**Tool Name:** `i_boss_url_recategorization`

**Description:** Submit URL for recategorization.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `i_boss_ping`

**Description:** Test connectivity to the iBoss with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove IP from Policy Block List

**Tool Name:** `i_boss_remove_ip_from_policy_block_list`

**Description:** Remove IP from iBoss Block List.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `category_id` (string, required): Specify from which policy category do you want to remove IP.
*   `start_port` (string, optional): Specify start port related to the IP that needs to be deleted. This parameter is mandatory, if the desired URL has a defined start port. This is an IBoss limitation. Defaults to None.
*   `end_port` (string, optional): Specify end port related to the IP that needs to be deleted. This parameter is mandatory, if the desired IP has a defined end port. This is an IBoss limitation. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add IP to Policy Block List

**Tool Name:** `i_boss_add_ip_to_policy_block_list`

**Description:** Add IP to iBoss Block List.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `category_id` (string, required): Specify to which policy category you want to add the IP.
*   `priority` (string, required): Specify priority of the IP that needs to be blocked.
*   `direction` (List[Any], required): Specify what is the direction of the IP.
*   `start_port` (string, optional): Specify the start port related to the IP that needs to be blocked. Note: if only "Start Port" or "End Port" is specified, the value will be added to both action parameters. Defaults to None.
*   `end_port` (string, optional): Specify the end port related to the IP that needs to be blocked. Note: if only "Start Port" or "End Port" is specified, the value will be added to both action parameters. Defaults to None.
*   `note` (string, optional): Add a note related to the IP that needs to be blocked. Defaults to None.
*   `is_regular_expression` (boolean, optional): If enabled, IP will be considered as a regular expression. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add URL to Policy Block List

**Tool Name:** `i_boss_add_url_to_policy_block_list`

**Description:** Add URL to iBoss Block List.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `category_id` (string, required): Specify to which policy category you want to add the URL.
*   `priority` (string, required): Specify priority of the URL that needs to be blocked.
*   `direction` (List[Any], required): Specify what is the direction of the URL.
*   `start_port` (string, optional): Specify the start port related to the URL that needs to be blocked. Note: if only "Start Port" or "End Port" is specified, the value will be added to both action parameters. Defaults to None.
*   `end_port` (string, optional): Specify the end port related to the URL that needs to be blocked. Note: if only "Start Port" or "End Port" is specified, the value will be added to both action parameters. Defaults to None.
*   `note` (string, optional): Add a note related to the URL that needs to be blocked. Defaults to None.
*   `is_regular_expression` (boolean, optional): If enabled, URL will be considered as a regular expression. Defaults to None.
*   `strip_scheme` (boolean, optional): If enabled, action will strip the scheme related to the URL. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on URL entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
