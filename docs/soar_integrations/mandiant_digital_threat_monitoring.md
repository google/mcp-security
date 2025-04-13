# Mandiant Digital Threat Monitoring

## Overview

This integration provides tools to interact with the Mandiant Digital Threat Monitoring service, allowing you to update alert statuses and test connectivity.

## Available Tools

### Update Alert

**Tool Name:** `mandiant_digital_threat_monitoring_update_alert`

**Description:** Update alert in Mandiant Digital Threat Monitoring.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert that needs to be updated.
*   `status` (Optional[List[Any]], optional): Specify the status for the alert. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `mandiant_digital_threat_monitoring_ping`

**Description:** Test connectivity to the Mandiant Digital Threat Monitoring with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
