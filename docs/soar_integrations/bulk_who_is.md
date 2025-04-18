# Bulk Whois Integration

## Overview

This integration allows you to connect to a Bulk WHOIS provider to perform WHOIS lookups for domains and IP addresses.

## Configuration

To configure this integration within the SOAR platform, you typically need the following details from your Bulk WHOIS provider:

*   **API Key:** Your API key provided by the Bulk WHOIS service for authentication.
*   **(Optional) API URL:** The base URL for the Bulk WHOIS API, if different from the provider's default.

*(Note: The exact parameter names and required details might vary depending on the specific Bulk WHOIS provider and the SOAR platform configuration interface.)*

## Actions

### WhoIs Details

Get domain/IP Whois info.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the WHOIS information for the specified domain(s) or IP address(es).

### Ping

Test Connectivity to the Bulk WHOIS provider.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the Bulk Whois integration is properly configured in the SOAR Marketplace tab with a valid API Key.
*   The `WhoIs Details` action supports both Domain and IP Address entities.
