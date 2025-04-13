# Certly Integration

## Overview

This integration allows you to connect to Certly to query URL reputation and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Certly details:

*   **API Key:** Your Certly API key for authentication.
*   **(Optional) API URL:** The base URL for the Certly API, if different from the default.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Ping

Validate the asset configuration for connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Url Status

Query Certly for URL reputation.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation status and details for the specified URL(s).

## Notes

*   Ensure the Certly integration is properly configured in the SOAR Marketplace tab with a valid API Key.
*   The `Get Url Status` action specifically targets URL entities.
