# IPVoid

## Overview

This integration provides tools to interact with the IPVoid service for querying Whois information and checking IP reputation against various blacklists.

## Available Tools

### Ping

**Tool Name:** `ip_void_ping`

**Description:** Test Connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### WhoIs

**Tool Name:** `ip_void_who_is`

**Description:** Query the Whois database to find information about a particular domain name or an IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on Domain or IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the Whois information for the provided domain or IP address.

---

### Get IP Reputation

**Tool Name:** `ip_void_get_ip_reputation`

**Description:** Scan an IP address through multiple DNS-based blacklists (DNSBL) and IP reputation services, to facilitate the detection of IP addresses involved in malware incidents and spamming activities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): IP risk threshold.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the IP reputation details, including blacklist checks and risk score.
