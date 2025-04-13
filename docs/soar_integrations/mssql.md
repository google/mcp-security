# Microsoft SQL Server (MSSQL) Integration

## Overview

This integration allows you to connect to a Microsoft SQL Server database to execute SQL queries and test connectivity.

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
*   `commit` (bool, optional): If set to true, will commit the changes to the DB (for INSERT, UPDATE, DELETE statements).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results (for SELECT statements) or the status of the operation.

### Ping

Test connectivity to the configured SQL Server instance and database.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `database_name` (string, required): The database name to test the connection against.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the MSSQL integration is properly configured in the SOAR Marketplace tab with the correct server details, database name, and credentials.
*   Use the `Commit` parameter carefully when executing data modification queries (INSERT, UPDATE, DELETE).
