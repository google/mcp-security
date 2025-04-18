# MySQL Integration

## Overview

This integration allows you to connect to a MySQL database to execute SQL queries and test connectivity.

## Configuration

The configuration for this integration (Server Address, Port, Database Name, Username, Password, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Run SQL Query

Run a SQL query against the specified database.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `database_name` (string, required): The DB name to run the query on.
*   `query` (string, required): The SQL query to run (e.g., `SELECT * FROM MyTable WHERE ID = 1`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results (for SELECT statements) or the status of the operation.

### Ping

Test connectivity to the configured MySQL instance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the MySQL integration is properly configured in the SOAR Marketplace tab with the correct server details, database name, and credentials.
*   The `Run SQL Query` action executes the provided SQL statement. Be cautious when running data modification queries (INSERT, UPDATE, DELETE). Unlike the MSSQL integration, there is no explicit `commit` parameter mentioned, implying auto-commit might be the default behavior or handled by the underlying script/driver.
