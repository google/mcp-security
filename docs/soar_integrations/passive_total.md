# PassiveTotal Integration

## Overview

This integration allows you to connect to RiskIQ PassiveTotal to perform WHOIS lookups and reputation checks for domains, IP addresses, and hosts.

## Configuration

The configuration for this integration (PassiveTotal API Username, API Key) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### WhoIs Scan Domain

Perform a RiskIQ domain WHOIS query.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the WHOIS information for the specified domain(s).

### Ping

Test Connectivity to PassiveTotal.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### WhoIs Address Reputation

Request address reputation from RiskIQ PassiveTotal.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation information for the specified IP address(es).

### WhoIs Scan Address

Perform a RiskIQ address (IP) WHOIS query.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the WHOIS information for the specified IP address(es).

### Whois Host Reputation

Request host reputation from RiskIQ PassiveTotal.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation information for the specified host(s).

## Notes

*   Ensure the PassiveTotal integration is properly configured in the SOAR Marketplace tab with a valid API Username and Key.
*   Actions support different entity types (Domain, IP Address, Hostname). Refer to individual action descriptions.
