# Stellar Cyber Starlight Integration

This document describes the available tools for the Stellar Cyber Starlight integration within the SecOps SOAR MCP Server. Stellar Cyber Starlight is an Open XDR platform.

## Configuration

Ensure the Stellar Cyber Starlight integration is configured in the SOAR platform with the necessary API credentials and instance details.

## Available Tools

### stellar_cyber_starlight_simple_search
- **Description:** Perform a simple search within a specified index in Stellar Cyber Starlight.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `index` (str, required): Specify the index to search within (refer to Stellar Cyber documentation for known indexes).
    - `query` (str, required): Specify the query filter for the search.
    - `max_results_to_return` (str, optional): Specify the maximum number of results to return. Defaults to None.
    - `sort_field` (str, optional): Specify the field to sort results by. Defaults to None.
    - `sort_order` (List[str], optional): Specify the sort order (e.g., ["asc"], ["desc"]). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the search results.

### stellar_cyber_starlight_ping
- **Description:** Test connectivity to the Stellar Cyber Starlight instance configured in the SOAR platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### stellar_cyber_starlight_update_security_event
- **Description:** Update the status and optionally add a comment to a specific security event in Stellar Cyber Starlight.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `index` (str, required): Specify the index of the security event.
    - `id` (str, required): Specify the ID of the security event to update.
    - `status` (List[str], required): Specify the new status for the security event (refer to Stellar Cyber documentation for valid statuses).
    - `comment` (str, optional): Specify a comment to add to the security event. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the update operation.

### stellar_cyber_starlight_advanced_search
- **Description:** Perform an advanced search using a DSL (Domain Specific Language) query in Stellar Cyber Starlight.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `index` (str, required): Specify the index to search within.
    - `dsl_query` (str, required): Specify the JSON object representing the DSL query.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the results of the advanced search.
