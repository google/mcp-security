# McAfee Active Response Integration

## Overview

This integration allows you to connect to McAfee Active Response to perform searches using specified collectors and filters, and to test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Search

Provides search capabilities within McAfee Active Response using specified collectors and filters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `collectors` (string, required): The collectors to search in.
*   `filter_collector` (string, optional): The collector filter.
*   `filter_by` (string, optional): The field to filter by.
*   `filter_operator` (string, optional): The operator of the filter. Must be one of: `GreaterEqualThan`, `GreaterThan`, `LessEqualThan`, `LessThan`, `Equals`, `Contains`, `StartWith`, `EndsWith`, `Before`, `After`.
*   `filter_value` (string, optional): The filter value.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the search action execution.

### Ping

Tests connectivity to the configured McAfee Active Response service using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the McAfee Active Response integration is properly configured in the SOAR Marketplace tab.
