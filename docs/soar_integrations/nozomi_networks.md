:# Nozomi Networks Integration

## Overview

This integration allows you to connect to Nozomi Networks devices to execute CLI commands, run queries, list vulnerabilities, enrich entities, and test connectivity.

## Configuration

The configuration for this integration (Device URL, API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Run a CLI Command

Run a CLI command on Nozomi Networks device. Note: Nozomi API doesn't provide validation for executed CLI commands; ensure the provided command is correct. This action does not operate on Siemplify Entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `cli_command` (string, required): Specify a CLI Command to execute.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the command execution.

### Run a Query

Run a query on Nozomi Networks device. Note: Action does not operate on Siemplify Entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify a query to execute (e.g., `alerts | head 10`).
*   `record_limit` (string, optional): Limits the number of records returned. Adds `| head <limit>` to the query if provided (default 10). If empty, returns all results. Negative values ignored.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results.

### List Vulnerabilities

List vulnerabilities discovered by Nozomi device based on provided parameters. Note: Action does not operate on Siemplify entities, only action input parameters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_limit` (string, required): Specify how many records can be returned.
*   `ip_address` (string, optional): List vulnerabilities for the provided IP address (comma-separated).
*   `cve_score` (string, optional): Minimum CVE score (0-10).
*   `vulnerability_name_contains` (string, optional): Filter vulnerabilities whose name contains this string.
*   `cve_id` (string, optional): Filter by specific CVE ID (e.g., CVE-2020-1207, comma-separated).
*   `include_vulnerabilities_that_marked_as_resolved` (bool, optional): Include vulnerabilities marked as resolved.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of vulnerabilities matching the criteria.

### Ping

Test connectivity to the Nozomi Networks instance with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enrich Entities

Enrich Siemplify Host or IP entities based on the information from the Nozomi Networks device.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `additional_fields_to_add_to_enrichment` (string, optional): Comma-separated list of fields from the Nodes query to add to the default enrichment fields.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Host and IP entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

## Notes

*   Ensure the Nozomi Networks integration is properly configured in the SOAR Marketplace tab.
*   Some actions do not operate on Siemplify entities directly but rely on action parameters (e.g., `Run a CLI Command`, `Run a Query`, `List Vulnerabilities`).
*   The `Run a CLI Command` action does not validate the command syntax before execution.
