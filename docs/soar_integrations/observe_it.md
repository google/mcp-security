# ObserveIT Integration

## Overview

This integration allows you to connect to ObserveIT (now part of Proofpoint) to test connectivity.

## Configuration

The configuration for this integration (ObserveIT URL, API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Ping

Test connectivity to the ObserveIT instance with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the ObserveIT integration is properly configured in the SOAR Marketplace tab.
*   This integration currently only supports a `Ping` action.
