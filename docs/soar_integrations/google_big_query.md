# Google BigQuery

## Overview

This integration provides tools to interact with Google BigQuery for executing SQL queries.

## Available Tools

### Run Custom Query

**Tool Name:** `google_big_query_run_custom_query`

**Description:** Execute queries in Google BigQuery.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the SQL query that needs to be executed.
*   `max_results_to_return` (string, optional): Specify how many results to return in the response. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Run SQL Query

**Tool Name:** `google_big_query_run_sql_query`

**Description:** Execute queries in Google BigQuery.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `dataset_name` (string, required): Specify the name of the dataset, which will be used, when executing queries.
*   `query` (string, required): Specify the SQL query that needs to be executed.
*   `max_results_to_return` (string, optional): Specify how many results to return in the response. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_big_query_ping`

**Description:** Test connectivity to the Google BigQuery with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
