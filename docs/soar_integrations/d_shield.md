# DShield Integration

## Overview

This integration allows you to connect to the SANS Internet Storm Center's DShield API to query IP address reputation information.

## Configuration

This integration does not require specific configuration parameters on the Marketplace tab. It uses the public DShield API.

## Actions

### Get Ip Info

Query DShield for information about external IP addresses.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation information (e.g., attack count, network details, country) for the specified IP address(es).

### Ping

Test Connectivity to the DShield API.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   This integration utilizes the public DShield API and does not require specific API keys or credentials.
*   The primary action is `Get Ip Info` which targets IP Address entities.
