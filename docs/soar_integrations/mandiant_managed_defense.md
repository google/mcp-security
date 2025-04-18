# Mandiant Managed Defense Integration

## Overview

This integration allows you to connect to Mandiant Managed Defense (MD) and perform connectivity tests.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Ping

Tests connectivity to the configured Mandiant MD service using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the Mandiant Managed Defense integration is properly configured in the SOAR Marketplace tab.
*   This integration currently only supports a `Ping` action to test connectivity.
