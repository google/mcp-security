# Vectra Integration

This document describes the available tools for the Vectra integration within the SecOps SOAR MCP Server. Vectra provides AI-driven threat detection and response for network, cloud, and SaaS environments.

## Configuration

Ensure the Vectra integration is configured in the SOAR platform with the necessary API token and Vectra instance URL.

## Available Tools

### vectra_enrich_endpoint
- **Description:** Fetch endpoint's system information from Vectra by its hostname or IP address.
- **Supported Entities:** Hostname, IP Address
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the Hostname or IP Address. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the system information for the endpoint.

### vectra_update_note
- **Description:** Update the note associated with a specific endpoint or detection in Vectra.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `item_type` (List[str], required): Select the item type ("endpoint" or "detection") to update the note for.
    - `item_id` (str, required): Specify the ID of the detection or endpoint.
    - `note` (str, required): Specify the content of the note to add or update.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the note update operation.

### vectra_ping
- **Description:** Test connectivity to the Vectra instance configured in the SOAR platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### vectra_remove_tags
- **Description:** Remove specified tags from an endpoint or detection in Vectra.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `item_type` (List[str], required): Select the item type ("endpoint" or "detection") from which to remove tags.
    - `item_id` (str, required): Specify the ID of the detection or endpoint.
    - `tags` (str, required): Specify the comma-separated list of tags to remove (e.g., "tag1,tag2").
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the tag removal operation.

### vectra_get_triage_rule_details
- **Description:** Get detailed information about one or more triage rules in Vectra by their IDs.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `triage_rule_i_ds` (str, required): Specify a comma-separated list of triage rule IDs (e.g., "28,29").
    - `create_insights` (bool, optional): If enabled, create a separate insight for each processed triage rule. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the details of the specified triage rules.

### vectra_update_detection_status
- **Description:** Update the status of a specific detection in Vectra.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `detection_id` (str, required): Specify the ID of the detection to update.
    - `status` (List[str], required): Specify the new status for the detection (refer to Vectra documentation for valid statuses).
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the status update operation.

### vectra_add_tags
- **Description:** Add tags to an endpoint or detection in Vectra.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `item_type` (List[str], required): Select the item type ("endpoint" or "detection") to add tags to.
    - `item_id` (str, required): Specify the ID of the detection or endpoint.
    - `tags` (str, required): Specify the comma-separated list of tags to add (e.g., "tag1,tag2").
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the tag addition operation.
