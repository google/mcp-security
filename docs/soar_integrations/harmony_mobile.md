# Harmony Mobile

## Overview

This integration provides tools to interact with Check Point Harmony Mobile for enriching device information.

## Available Tools

### Ping

**Tool Name:** `harmony_mobile_ping`

**Description:** Test connectivity to the Harmony Mobile with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `harmony_mobile_enrich_entities`

**Description:** Enrich entities using information from Harmony Mobile. Supported entities: Hostname. Note: Hostname entity should contain the "name" of the device.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (boolean, optional): If enabled, action will create an insight containing all of the retrieved information about the entity. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
