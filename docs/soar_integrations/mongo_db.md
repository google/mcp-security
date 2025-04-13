# MongoDB Integration

## Overview

This integration allows you to connect to a MongoDB database to execute queries and test connectivity.

## Configuration

The configuration for this integration (Connection String, Username, Password, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Ping

Test connectivity to MongoDB using the provided configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Free Query

Run a MongoDB query on a specified database and collection.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `database_name` (string, required): The DB name to run the query on.
*   `collection_name` (string, required): The collection name to run the query on.
*   `query` (string, required): The key-value query (e.g., `{"key": "value"}`).
*   `return_a_single_json_result` (bool, optional): If enabled, returns a single JSON result instead of multiple results.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results.

## Notes

*   Ensure the MongoDB integration is properly configured in the SOAR Marketplace tab with the correct connection string and credentials.
*   The `Free Query` action requires a valid MongoDB query document format.
