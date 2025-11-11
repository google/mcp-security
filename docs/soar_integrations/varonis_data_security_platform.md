# Varonis Data Security Platform Integration

This document describes the available tools for the Varonis Data Security Platform integration within the SecOps SOAR MCP Server. Varonis provides data security and threat detection capabilities.

## Configuration

Ensure the Varonis Data Security Platform integration is configured in the SOAR platform with the necessary API credentials and server details.

## Available Tools

### varonis_data_security_platform_update_alert
- **Description:** Update the status and optionally the closing reason of one or more alerts in the Varonis Data Security Platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `alert_guid` (str, required): Specify the GUID(s) of the alert(s) to update. Multiple GUIDs can be provided as a comma-separated string.
    - `alert_status` (List[str], required): Specify the new status for the alert(s) (refer to Varonis documentation for valid statuses).
    - `closing_reason` (List[str], optional): Specify the closing reason if the `alert_status` is set to "closed". Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the update operation.

### varonis_data_security_platform_ping
- **Description:** Test connectivity to the Varonis Data Security Platform instance configured in the SOAR platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.
