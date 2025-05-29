# StealthwatchV6-10 SOAR Integration

## Overview

This integration provides tools for interacting with Cisco Stealthwatch version 6.10 from within the Chronicle SOAR platform. It allows searching for security events and network flows associated with specific hosts or IP addresses, and testing connectivity.

## Tools

### `stealthwatch_v6_10_search_events`

Get a host's security events for a given time frame

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `timeframe` (str, required): Time frame in hours.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `stealthwatch_v6_10_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `stealthwatch_v6_10_search_flows`

Get flows by IP address for a given time frame

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `timeframe` (str, required): Time frame in hours(e.g: 3).
*   `limit` (str, required): The limit of the received flow.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
