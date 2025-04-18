# Humio

## Overview

This integration provides tools to interact with Humio for searching events using simple or custom queries.

## Available Tools

### Execute Custom Search

**Tool Name:** `humio_execute_custom_search`

**Description:** Search events using custom query in Humio.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `repository_name` (string, required): Specify the name of the repository that should be searched.
*   `query` (string, required): Specify the query that needs to be executed in Humio. Note: "head()" function shouldn't be a part of this string.
*   `max_results_to_return` (string, optional): Specify how many results the action should return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `humio_ping`

**Description:** Test connectivity to the Humio with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Simple Search

**Tool Name:** `humio_execute_simple_search`

**Description:** Search events based on parameters in Humio.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `repository_name` (string, required): Specify the name of the repository that should be searched.
*   `query_filter` (string, optional): Specify the query that should be executed during the search. Note: functions "head()" and "select()" shouldn't be provided. Defaults to None.
*   `time_frame` (List[Any], optional): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time". Defaults to None.
*   `start_time` (string, optional): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601. Defaults to None.
*   `end_time` (string, optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time. Defaults to None.
*   `fields_to_return` (string, optional): Specify what fields to return. If nothing is provided, action will return all fields. Defaults to None.
*   `sort_field` (string, optional): Specify what parameter should be used for sorting. By default the query sorts data by timestamp in the ascending order. Defaults to None.
*   `sort_field_type` (List[Any], optional): Specify the type of the field that will be used for sorting. This parameter is needed to ensure that the correct results are returned. Defaults to None.
*   `sort_order` (List[Any], optional): Specify the order of sorting. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
