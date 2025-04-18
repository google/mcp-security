# CSV Integration

## Overview

This integration provides utilities for working with CSV files directly on the SOAR server's filesystem. Actions include searching for entities or strings within CSV files and saving JSON data to a CSV file.

## Configuration

This integration does not require specific configuration parameters on the Marketplace tab. It operates directly on file paths provided within the actions. Ensure the SOAR agent/server has the necessary file system permissions to read from and write to the specified paths.

## Actions

### CSV Search by Entity

Search for entities in CSV files and enrich them.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `csv_path` (string, required): Specify the file path to the CSV file or a folder path containing CSV files. If a folder is provided, the action iterates over all CSV files within it.
*   `file_encoding_types` (string, required): A comma-separated list of CSV encoding types (e.g., `utf-8`, `latin-1`, `iso-8859-1`, `utf-16`). The action tries decoding using these types in the specified order.
*   `csv_column` (string, optional): Comma-separated list of column names to search within. If empty, searches all columns.
*   `days_back` (string, optional): Specify how many days back to process CSV files based on modification time.
*   `mark_as_suspicious` (bool, optional): If enabled, mark the entity as suspicious if found in the file.
*   `return_the_first_row_only` (bool, optional): If enabled, only return the first matching row found in the first matching file.
*   `enrich_entities` (bool, optional): If enabled, add information from the matching CSV row to the entity's enrichment data.
*   `create_insight` (bool, optional): If enabled, create an insight if the entity is found.
*   `fields_to_return` (string, optional): Comma-separated list of column names whose values should be returned in the result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to search for.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the rows from the CSV file(s) where the entities were found, along with enrichment status.

### Ping

Test Connectivity (Placeholder action, likely checks basic file system access or integration status).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Save Json To CSV

Save JSON object to a CSV file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `json_object` (Union[str, dict], required): Specify the JSON object (as a string or direct JSON) to save as CSV. Assumes a list of flat dictionaries for proper CSV conversion.
*   `file_path` (string, required): Specify the absolute file path for the newly created CSV file. If only a filename is provided, it defaults to the `/tmp/` folder.
*   `overwrite` (bool, optional): If enabled, overwrite the existing file if it exists.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the save operation, including the path to the created CSV file.

### CSV Search by String

Search for strings in CSV files.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `csv_path` (string, required): Specify the file path to the CSV file or a folder path containing CSV files.
*   `search_value` (string, required): Specify the string to search for. If `search_multiple_strings` is enabled, this is treated as a comma-separated list.
*   `file_encoding_types` (string, required): Comma-separated list of CSV encoding types to try (e.g., `utf-8`, `latin-1`).
*   `csv_column` (string, optional): Comma-separated list of column names to search within. If empty, searches all columns.
*   `days_back` (string, optional): Specify how many days back to process CSV files based on modification time.
*   `return_the_first_row_only` (bool, optional): If enabled, only return the first matching row found in the first matching file.
*   `fields_to_return` (string, optional): Comma-separated list of column names whose values should be returned.
*   `search_multiple_strings` (bool, optional): If enabled, treat `search_value` as a comma-separated list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the rows from the CSV file(s) where the string(s) were found.

## Notes

*   This integration operates on the local filesystem of the SOAR server/agent. Ensure appropriate file paths and permissions are set.
*   Provide multiple encoding types in `file_encoding_types` if unsure about the exact encoding of the CSV files.
*   The `Save Json To CSV` action works best with a JSON structure representing a list of flat objects (key-value pairs).
