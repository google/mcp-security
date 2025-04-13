# Ivanti Endpoint Manager

## Overview

This integration provides tools to interact with Ivanti Endpoint Manager, allowing you to manage endpoints, execute tasks, list vulnerabilities, and more.

## Available Tools

### List Delivery Methods

**Tool Name:** `ivanti_endpoint_manager_list_delivery_methods`

**Description:** List available delivery methods in Ivanti Endpoint Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `type` (Optional[List[Any]], optional): Specify the delivery type that needs to be returned. Defaults to None.
*   `filter_logic` (Optional[List[Any]], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (Optional[str], optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among items and if "Contains" is selected, action will try to find items that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Defaults to None.
*   `max_delivery_methods_to_return` (Optional[str], optional): Specify how many delivery methods to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Task

**Tool Name:** `ivanti_endpoint_manager_execute_task`

**Description:** Execute task in Ivanti Endpoint Manager. Supported entities: Hostname, IP address, MAC Address. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `delivery_method` (string, required): Specify the name of the delivery method that will be used during task execution.
*   `package` (string, required): Specify the name of the package that will be used during task execution.
*   `wake_up_machines` (bool, required): If enabled, action will wake up the machine during task execution.
*   `common_task` (bool, required): If enabled, action will mark this task as common.
*   `only_initiate` (bool, required): If enabled, action will only initiate the task execution without waiting for results.
*   `task_name` (Optional[str], optional): Specify the name of the task. If nothing is provided the action will use the "Siemplify Execute Task" name. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Column Sets

**Tool Name:** `ivanti_endpoint_manager_list_column_sets`

**Description:** List available column sets in Ivanti Endpoint Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (Optional[List[Any]], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (Optional[str], optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among items and if "Contains" is selected, action will try to find items that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Defaults to None.
*   `max_column_sets_to_return` (Optional[str], optional): Specify how many column sets to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Query

**Tool Name:** `ivanti_endpoint_manager_execute_query`

**Description:** Execute query in Ivanti Endpoint Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the name of the query that you want to execute.
*   `max_results_to_return` (Optional[str], optional): Specify how many results to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Endpoint Vulnerabilities

**Tool Name:** `ivanti_endpoint_manager_list_endpoint_vulnerabilities`

**Description:** List vulnerabilities on the endpoints in Ivanti Endpoint Manager. Supported entities: IP Address, Mac Address, Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `severity_filter` (Optional[str], optional): Specify a comma-separated list of severities that will be used, when returning information about vulnerabilities. If nothing is provided, action will return all vulnerabilities. Possible values: ServicePack, Critical, High, Medium, Low, N/A, Unknown. Defaults to None.
*   `max_vulnerabilities_to_return` (Optional[str], optional): Specify how many vulnerabilities to return per entity. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Column Set Fields

**Tool Name:** `ivanti_endpoint_manager_list_column_set_fields`

**Description:** List available fields in column sets in Ivanti Endpoint Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `column_set` (string, required): Specify the name of the column set for which you want to return fields.
*   `filter_logic` (Optional[List[Any]], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (Optional[str], optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among items and if "Contains" is selected, action will try to find items that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Defaults to None.
*   `max_fields_to_return` (Optional[str], optional): Specify how many column sets to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `ivanti_endpoint_manager_ping`

**Description:** Test connectivity to the Ivanti Endpoint Manager with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Scan Endpoints

**Tool Name:** `ivanti_endpoint_manager_scan_endpoints`

**Description:** Scan endpoints for vulnerabilities in Ivanti Endpoint Manager. Supported entities: IP Address, Mac Address, Hostname. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `only_initiate` (bool, required): If enabled, action will only initiate the task execution without waiting for results.
*   `task_name` (Optional[str], optional): Specify the name of the scan vulnerabilities task. If nothing is provided the action will use the "Siemplify Scan Endpoints" name. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Queries

**Tool Name:** `ivanti_endpoint_manager_list_queries`

**Description:** List available queries in Ivanti Endpoint Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (Optional[List[Any]], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (Optional[str], optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among items and if "Contains" is selected, action will try to find items that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Defaults to None.
*   `max_queries_to_return` (Optional[str], optional): Specify how many queries to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Packages

**Tool Name:** `ivanti_endpoint_manager_list_packages`

**Description:** List available packages in Ivanti Endpoint Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_logic` (Optional[List[Any]], optional): Specify what filter logic should be applied. Defaults to None.
*   `filter_value` (Optional[str], optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among items and if "Contains" is selected, action will try to find items that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Defaults to None.
*   `max_packages_to_return` (Optional[str], optional): Specify how many packages to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `ivanti_endpoint_manager_enrich_entities`

**Description:** Enrich entities using information from Ivanti Endpoint Manager. Supported entities: IP Address, Hostname, MAC Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `custom_column_set` (Optional[str], optional): If specified, action will also try to return information about endpoints using custom column sets. If not specified, action will only return basic information. Defaults to None.
*   `create_insight` (Optional[bool], optional): If enabled, action will create an insight containing all of the retrieved information about the entity. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
