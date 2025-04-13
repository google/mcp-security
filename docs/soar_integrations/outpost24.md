# Outpost24 Integration

## Overview

This integration allows you to connect to Outpost24 to enrich entities (IP Address, Hostname) with vulnerability finding information and test connectivity.

## Configuration

The configuration for this integration (Outpost24 URL, API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Ping

Test connectivity to the Outpost24 with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enrich Entities

Enrich entities using information from Outpost24. Supported entities: IP Address, Hostname.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `finding_risk_level_filter` (string, optional): Comma-separated list of risk levels to filter findings (Initial, Recommendation, Low, Medium, High, Critical). If empty, fetches all levels.
*   `max_findings_to_return` (string, optional): Max number of findings to process per entity. Default: 100.
*   `return_finding_information` (bool, optional): If enabled, retrieves information about findings found on the endpoint.
*   `finding_type` (List[Any], optional): Specify what kind of findings should be returned.
*   `create_insight` (bool, optional): If enabled, creates an insight containing retrieved information about the entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities, potentially including related findings.

## Notes

*   Ensure the Outpost24 integration is properly configured in the SOAR Marketplace tab with the correct URL and API Key.
*   The `Enrich Entities` action allows filtering findings based on risk level and type.
