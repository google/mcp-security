# FireEye ETP Integration

## Overview

This integration allows you to connect to FireEye Email Threat Prevention (ETP) and test connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The `fire_eye_etp_ping` action utilizes these pre-configured settings.

## Actions

### Ping

Tests connectivity to the configured FireEye ETP instance using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action, typically indicating success or failure.

## Notes

*   This integration currently only provides a `ping` action for connectivity testing.
*   Ensure the FireEye ETP integration is properly configured in the SOAR Marketplace tab before using this action.
