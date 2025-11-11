# Snowflake SOAR Integration

## Overview

This integration provides tools for interacting with Snowflake data warehouses from within the Chronicle SOAR platform. It allows testing connectivity and executing both simple and custom SQL queries against specified databases, schemas, and tables.

## Tools

### `snowflake_ping`

Test connectivity to the Snowflake with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `snowflake_execute_simple_query`

Execute a query based on parameters in Snowflake. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `database` (str, required): Specify the name of the database in which you want to execute the query.
*   `table` (str, required): Specify the name of the table in which you want to execute the query.
*   `schema` (Optional[str], optional, default=None): Specify the name of the schema in which you want to execute the query.
*   `where_filter` (Optional[str], optional, default=None): Specify the WHERE filter for the query that needs to be executed. Note: you don't need to limit and sort. Also, you don’t need to provide WHERE string in the payload. Only single quotes are supported in the query.
*   `fields_to_return` (Optional[str], optional, default=None): Specify what fields to return. If nothing is provided action will return all fields. Wildcard character is supported.
*   `sort_field` (Optional[str], optional, default=None): Specify what parameter should be used for sorting.
*   `sort_order` (Optional[List[str]], optional, default=None): Specify the order of sorting.
*   `max_results_to_return` (Optional[str], optional, default=None): Specify how many results to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `snowflake_execute_custom_query`

Execute a custom query in Snowflake. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query that needs to be executed in Snowflake. Note: query shouldn't contain LIMIT keyword, because it’s added automatically. Only single quotes are supported in the query.
*   `database` (str, required): Specify the name of the database in which you want to execute the query.
*   `schema` (Optional[str], optional, default=None): Specify the name of the schema in which you want to execute the query.
*   `max_results_to_return` (Optional[str], optional, default=None): Specify how many results to return for the query. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
