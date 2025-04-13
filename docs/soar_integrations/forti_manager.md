# FortiManager

## Overview

This integration provides tools to interact with FortiManager for managing firewall policies and configurations.

## Available Tools

### Remove IP From Group

**Tool Name:** `forti_manager_remove_ip_from_group`

**Description:** Remove a firewall address object from a suitable address group and delete the firewall address object. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `adom_name` (string, required): The name of the ADOM. Default: root.
*   `address_group_name` (string, required): The name of the address group to remove the address from.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add IP To Group

**Tool Name:** `forti_manager_add_ip_to_group`

**Description:** Create a firewall address object and add it to a suitable address group. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `adom_name` (string, required): The name of the ADOM. Default: root.
*   `address_group_name` (string, required): The name of the address group to add to address object to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add URL To Url Filter

**Tool Name:** `forti_manager_add_url_to_url_filter`

**Description:** Add a new block record to a url filter by it's name. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `adom_name` (string, required): The name of the ADOM. Default: root.
*   `url_filter_name` (string, required): The name of the URL filter to add record to.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove URL From Url Filter

**Tool Name:** `forti_manager_remove_url_from_url_filter`

**Description:** Remove a block record from a url filter by it's name. Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `adom_name` (string, required): The name of the ADOM. Default: root.
*   `url_filter_name` (string, required): The name of the URL filter to remove the record from.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Task Information

**Tool Name:** `forti_manager_get_task_information`

**Description:** Get task information by ID.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `task_id` (string, required): The ID of the task to get information about.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `forti_manager_ping`

**Description:** Test integration connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Script

**Tool Name:** `forti_manager_execute_script`

**Description:** Execute existing script. Can be executed on device group and on a single device if VDOM provided.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `adom_name` (string, required): The name of the ADOM. Default: root.
*   `policy_package_name` (string, required): The full name of the package, including package name and any parent folders.
*   `script_name` (string, required): The name of the script to execute.
*   `device_name` (string, required): The name of the device to execute the script on.
*   `vdom` (string, optional): The virtual domain of the device. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
