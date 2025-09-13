# Sumo Logic Cloud SIEM Integration

This document describes the available tools for the Sumo Logic Cloud SIEM integration within the SecOps SOAR MCP Server.

## Configuration

Ensure the Sumo Logic Cloud SIEM integration is configured in the SOAR platform with the necessary API credentials (Access ID, Access Key) and deployment endpoint.

## Available Tools

### sumo_logic_cloud_siem_add_tags_to_insight
- **Description:** Add tags to a specific insight in Sumo Logic Cloud SIEM.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `insight_id` (str, required): Specify the ID of the insight to add tags to.
    - `tags` (str, required): Specify a comma-separated list of tags to add to the insight.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the action execution.

### sumo_logic_cloud_siem_ping
- **Description:** Test connectivity to the Sumo Logic Cloud SIEM instance configured in the SOAR platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### sumo_logic_cloud_siem_update_insight
- **Description:** Update the status and assignee of an insight in Sumo Logic Cloud SIEM.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `insight_id` (str, required): Specify the ID of the insight to update.
    - `status` (List[str], required): Specify the new status for the insight (refer to Sumo Logic documentation for valid statuses).
    - `assignee_type` (List[str], required): Specify the assignee type ("user" or "team").
    - `assignee` (str, optional): Specify the assignee identifier (username or team ID). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the update operation.

### sumo_logic_cloud_siem_enrich_entities
- **Description:** Enrich entities (Hostname, User, IP address) using information from Sumo Logic Cloud SIEM.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `create_insight` (bool, optional): If enabled, create an insight containing retrieved information. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the enrichment results.

### sumo_logic_cloud_siem_add_comment_to_insight
- **Description:** Add a comment to a specific insight in Sumo Logic Cloud SIEM.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `insight_id` (str, required): Specify the ID of the insight to add a comment to.
    - `comment` (str, required): Specify the comment text to add.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the action execution.

### sumo_logic_cloud_siem_search_entity_signals
- **Description:** Search for signals related to entities (IP Address, Hostname, Username) in Sumo Logic Cloud SIEM within a specified timeframe and severity threshold.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `lowest_severity_to_return` (str, optional): Specify the lowest severity number (max 10) to include in results. Defaults to None (no severity filter).
    - `time_frame` (List[str], optional): Specify a time frame (e.g., ["Last 24 Hours"], ["Custom"], ["5 Minutes Around Alert Time"]). If "Custom", `start_time` is required. Defaults to None.
    - `start_time` (str, optional): Specify the start time (ISO 8601 format). Mandatory if `time_frame` is "Custom". Defaults to None.
    - `end_time` (str, optional): Specify the end time (ISO 8601 format). If `time_frame` is "Custom" and not provided, uses current time. Defaults to None.
    - `max_signals_to_return` (str, optional): Specify max signals per entity (Default: 50). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the signals found for the specified entities.
