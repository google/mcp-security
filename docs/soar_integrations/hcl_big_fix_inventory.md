# HCL BigFix Inventory

## Overview

This integration provides tools to interact with HCL BigFix Inventory for testing connectivity and enriching entities.

## Available Tools

### Ping

**Tool Name:** `hcl_big_fix_inventory_ping`

**Description:** Test connectivity to the HCL BigFix Inventory with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `hcl_big_fix_inventory_enrich_entities`

**Description:** Enrich entities using information from HCL BigFix Inventory. Supported entities: Hostname, IP Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `custom_fields` (string, optional): Specify a comma-separated list of fields that needs to be returned in addition to the ones that are returned by default. Defaults to None.
*   `create_insight` (boolean, optional): If enabled, action will create an insight containing all of the retrieved information about the entity. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
