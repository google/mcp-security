# Google Alert Center

## Overview

This integration provides tools to interact with the Google Alert Center API for managing alerts.

## Available Tools

### Ping

**Tool Name:** `google_alert_center_ping`

**Description:** Test connectivity to the Google Alert Center with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Alert

**Tool Name:** `google_alert_center_delete_alert`

**Description:** Delete an alert in Google Alert Center. Note: it takes 30 days for the alert to fully disappear in Google Alert Center, before that they can still be recovered.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the id of the alert that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
