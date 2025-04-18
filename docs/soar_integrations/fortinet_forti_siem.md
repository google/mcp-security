# Fortinet FortiSIEM

## Overview

This integration provides tools to interact with Fortinet FortiSIEM for querying events and enriching entities.

## Available Tools

### Ping

**Tool Name:** `fortinet_forti_siem_ping`

**Description:** Test connectivity to the FortiSIEM installation with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Simple Query

**Tool Name:** `fortinet_forti_siem_execute_simple_query`

**Description:** Execute FortiSIEM events query based on the provided parameters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is provided, action will return all fields. Defaults to None.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting. Defaults to None.
*   `sort_order` (List[Any], optional): Specify the order of sorting. Defaults to None.
*   `minimum_severity_to_fetch` (string, optional): Specify minimum event severity to fetch to Siemplify in numbers, for example 5 or 7. Defaults to None.
*   `event_types` (string, optional): Specify event types query should fetch. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `event_category` (string, optional): Specify event category query should fetch. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `event_i_ds` (string, optional): Specify optionally exact event ids query should fetch. Parameter accepts multiple values as a comma separated string. Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Example: 2021-04-23T12:38Z. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50. Defaults to None.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time". Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `fortinet_forti_siem_enrich_entities`

**Description:** Enrich entities using information from Fortinet FortiSIEM CMDB. Supported entities: Hostname, IP. Note: Hostname entity should contain the "name" of the device.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_organization` (string, optional): Specify optional target organization name to look for enrichment information in this organization only. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Custom Query

**Tool Name:** `fortinet_forti_siem_execute_custom_query`

**Description:** Execute a custom query in FortiSIEM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify a query that will be used to retrieve information about the events. Example: (relayDevIpAddr = 172.30.202.1 OR 172.30.202.2) AND (reptDevName = HOST1).
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is provided, action will return all fields. Defaults to None.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting. Defaults to None.
*   `sort_order` (List[Any], optional): Specify the order of sorting. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50. Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Example: 2021-04-23T12:38Z. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Defaults to None.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time". Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
