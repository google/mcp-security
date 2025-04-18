# Illusive Networks

## Overview

This integration provides tools to interact with the Illusive Networks platform for managing deceptive users and servers, listing deceptive items, enriching entities, and running forensic scans on endpoints.

## Available Tools

### Remove Deceptive Server

**Tool Name:** `illusive_networks_remove_deceptive_server`

**Description:** Remove deceptive server from Illusive Networks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `server_name` (string, required): Specify the name of the deceptive server that needs to be removed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Deceptive User

**Tool Name:** `illusive_networks_remove_deceptive_user`

**Description:** Remove deceptive user from Illusive Networks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `username` (string, required): Specify the username of the deceptive user that needs to be removed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `illusive_networks_ping`

**Description:** Test connectivity to the Illusive Networks with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Deceptive Items

**Tool Name:** `illusive_networks_list_deceptive_items`

**Description:** List available deceptive items in Illusive Networks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `deceptive_type` (List[Any], required): Specify what kind of deceptive items should be returned.
*   `deceptive_state` (List[Any], required): Specify what kind of deceptive items should be returned based on state.
*   `max_items_to_return` (string, optional): Specify how many items to return. Default: 50. If nothing is specified, action will return all items. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `illusive_networks_enrich_entities`

**Description:** Enrich entities using information from Illusive Networks. Supported entities: Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Deceptive User

**Tool Name:** `illusive_networks_add_deceptive_user`

**Description:** Add deceptive users in Illusive Networks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `username` (string, required): Specify the username for the new deceptive user.
*   `password` (string, required): Specify the password for the new deceptive user.
*   `dns_domain` (string, optional): Specify the domain name for the new deceptive user. Defaults to None.
*   `policy_names` (string, optional): Specify a comma-separated list of policies that need to be applied to the new deceptive user. If nothing is provided action will use by default all policies. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Run Forensic Scan

**Tool Name:** `illusive_networks_run_forensic_scan`

**Description:** Run forensic scan on the endpoint in the Illusive Networks. Works with IP and Hostname entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `include_system_information` (boolean, required): If enabled, action will return system information.
*   `include_prefetch_files_information` (boolean, required): If enabled, action will return information about prefetch files.
*   `include_add_remove_programs_information` (boolean, required): If enabled, action will return information about add-remove programs.
*   `include_startup_processes_information` (boolean, required): If enabled, action will return information about startup processes.
*   `include_user_assist_programs_information` (boolean, required): If enabled, action will return information about user-assist programs.
*   `include_powershell_history_information` (boolean, required): If enabled, action will return information about powershell history.
*   `include_running_processes_information` (boolean, optional): If enabled, action will return information about running processes. Defaults to None.
*   `max_items_to_return` (string, optional): Specify how many items to return. If nothing is provided, action will return everything. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Deceptive Server

**Tool Name:** `illusive_networks_add_deceptive_server`

**Description:** Add deceptive servers in Illusive Networks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `server_name` (string, required): Specify what kind of deceptive items should be returned.
*   `service_types` (string, required): Specify a comma-separated list of service types for new deceptive server.
*   `policy_names` (string, optional): Specify a comma-separated list of policies that need to be applied to the new deceptive server. If nothing is provided action will use by default all policies. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
