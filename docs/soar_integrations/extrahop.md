# ExtraHop Integration

## Overview

This integration provides connectivity testing capabilities for ExtraHop within the SOAR platform. It allows verifying that the connection parameters configured in the Marketplace tab are correct and the SOAR instance can communicate with the ExtraHop instance.

## Configuration

The configuration for this integration is managed within the SOAR platform's Marketplace tab. The `extrahop_ping` action utilizes these pre-configured settings (like API endpoint, credentials, etc.) to test the connection. No specific parameters need to be configured within the playbook action itself, beyond the standard case and scope details.

## Actions

### Extrahop Ping

Tests the connectivity to the configured ExtraHop instance. This action is useful for validating the integration setup and ensuring communication is possible before attempting more complex operations (if other actions were available).

**Arguments:**

*   `case_id` (string, required): The ID of the case context for this action.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups associated with the case.
*   `target_entities` (List[TargetEntity], optional): A list of specific target entities (Identifier, EntityType) to associate with the action execution log. If provided, the `scope` parameter is ignored. Defaults to an empty list.
*   `scope` (string, optional): Defines the scope for the action if `target_entities` is not provided. Valid values are typically "All entities" or specific predefined scopes within the SOAR platform. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action, typically indicating success or failure and potentially including a message.

## Notes

*   This integration currently only provides a `ping` action for connectivity testing.
*   Ensure the ExtraHop integration is properly configured in the SOAR Marketplace tab before using this action.
