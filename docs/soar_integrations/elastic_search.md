# Elasticsearch Integration

## Overview

This integration allows interaction with an Elasticsearch cluster to perform searches using Lucene query string syntax or Elasticsearch Domain Specific Language (DSL).

## Configuration

To configure this integration within the SOAR platform, you typically need the following Elasticsearch details:

*   **Server Address:** The URL of your Elasticsearch cluster (e.g., `https://my-elastic.example.com:9200`).
*   **Username:** The username for authenticating to Elasticsearch.
*   **Password:** The password for the Elasticsearch user.
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate.
*   **(Optional) CA Certificate File:** Path to a CA certificate file for SSL verification if using a self-signed or private CA.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user account has the necessary permissions to search the intended indices.)*

## Actions

### Simple ES Search

Searches through everything in Elasticsearch using Lucene query string syntax and returns results in a dictionary format. This action supports only queries without a time range. Use "Advanced ES Search" for time-based queries.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `index` (string, optional): Search pattern for an Elasticsearch index (e.g., `my-index-*`, `specific-index-2023.10.27`). Supports wildcards (`*`).
*   `query` (string, optional): The search query in Lucene syntax (e.g., `level:error`, `message:"login failed"`). Defaults to `*` (match all).
*   `limit` (string, optional): Limits the document return count (e.g., `10`). `0` means no limit.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Advanced ES Search

Execute a structured Elasticsearch query using Lucene syntax with time range filtering. Returns results as a dictionary. Use this action when time range filtering is needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `index` (string, optional): Search pattern for an Elasticsearch index.
*   `query` (string, optional): The search query in Lucene syntax.
*   `limit` (string, optional): Limits the document return count. `0` means no limit.
*   `display_field` (string, optional): Limits the returned fields (e.g., `level`, `message`). Default `*` returns all fields.
*   `search_field` (string, optional): Search field for free text queries when the query doesn't specify a field. Default is `_all`.
*   `timestamp_field` (string, optional): The field to use for time-based filtering. Default is `@timestamp`.
*   `oldest_date` (string, optional): Start date/time for the search (ISO 8601 format like `YYYY-MM-DDTHH:MM:SSZ` or relative like `now-1d`).
*   `earliest_date` (string, optional): End date/time for the search (ISO 8601 format or relative).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results matching the query and time range.

### Ping

Verifies connectivity to Elasticsearch server.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### DSL Search

Execute an Elasticsearch Domain Specific Language (DSL) query. Fetches data from the past 24 hours by default.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `index` (string, optional): Search pattern for an Elasticsearch index.
*   `query` (string, optional): The DSL query (must be valid JSON or `*`).
*   `limit` (string, optional): Limits the document return count. `0` means no limit.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the DSL query.

## Notes

*   Ensure the Elasticsearch integration is properly configured in the SOAR Marketplace tab with the correct Server Address and credentials.
*   The user account requires appropriate read permissions for the target Elasticsearch indices.
*   Familiarize yourself with [Lucene Query Syntax](https://www.elastic.co/guide/en/kibana/current/lucene-query.html) for `Simple ES Search` and `Advanced ES Search`.
*   Familiarize yourself with [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html) for `DSL Search`.
*   Time-based filtering in `Advanced ES Search` uses the specified `Timestamp Field` (defaulting to `@timestamp`) and supports both absolute (ISO 8601) and relative date math expressions (e.g., `now-1h`).
