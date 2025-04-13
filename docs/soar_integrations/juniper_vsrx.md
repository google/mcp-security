# Juniper vSRX

## Overview

This integration provides tools to interact with Juniper vSRX firewalls, allowing you to manage address sets and test connectivity.

## Available Tools

### Add IP To Address Set

**Tool Name:** `juniper_vsrx_add_ip_to_address_set`

**Description:** Add IP address to an address set.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_set_name` (string, required): The name of the address set to add the IP to.
*   `zone_name` (Optional[str], optional): The name of the security zone. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove IP From Address Set

**Tool Name:** `juniper_vsrx_remove_ip_from_address_set`

**Description:** Remove IP address from address set.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `address_set_name` (string, required): The name of the address set to remove the IP from.
*   `zone_name` (Optional[str], optional): The name of the security zone. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `juniper_vsrx_ping`

**Description:** Test integration connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
