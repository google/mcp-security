# Internet Storm Center

## Overview

This integration provides tools to interact with the SANS Internet Storm Center (ISC) DShield API for enriching IP address information and testing connectivity.

## Available Tools

### Ping

**Tool Name:** `internet_storm_center_ping`

**Description:** Test connectivity to the Internet Storm Center with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Enrich Entities

**Tool Name:** `internet_storm_center_enrich_entities`

**Description:** Enrich entities using information from the Internet Storm Center. Supported entities: IP Address. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. There is rate limiting for API, so make sure to put a big timeout in IDE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (boolean, optional): If enabled, action will create an insight containing all of the retrieved information about the entity. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IP Address entities. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including enrichment data for the IP address(es).
