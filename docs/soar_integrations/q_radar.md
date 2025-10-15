# QRadar Integration

The IBM QRadar integration for Chronicle SOAR provides extensive capabilities to interact with the QRadar SIEM platform. This includes searching events and flows using AQL, managing reference data collections (sets, maps, tables), updating offenses, and retrieving rule information.

## Overview

IBM QRadar is a Security Information and Event Management (SIEM) platform that collects log data and network flows, correlates events, detects offenses, and provides tools for investigation and compliance reporting.

This integration enables Chronicle SOAR to:

*   **Execute AQL Queries:** Run custom or predefined Ariel Query Language (AQL) searches against QRadar event and flow data.
*   **Manage Reference Data:** List, query, and potentially modify QRadar reference sets, maps, and tables, which are often used for lookups, correlation, and enrichment within QRadar rules.
*   **Manage Offenses:** Retrieve information about QRadar offenses, update their status, add notes, and assign them.
*   **Enrichment:** Enrich SOAR entities by querying related events, flows, or reference data in QRadar.
*   **Rule Information:** Retrieve details about QRadar rules, including MITRE ATT&CK mapping via the Use Case Manager application.

## Key Actions

The following actions are available through the QRadar integration:

*   **List Reference Maps (`q_radar_list_reference_maps`)**
    *   Description: List reference maps available in QRadar, with filtering options.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `number_of_elements_to_return` (string, required): Maximum number of maps to return.
        *   `fields_to_return` (string, optional): Comma-separated list of fields to return.
        *   `filter_condition` (string, optional): Filter condition (e.g., `element_type = ALNIC`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Reference Maps of Sets (`q_radar_list_reference_maps_of_sets`)**
    *   Description: List reference maps of sets available in QRadar, with filtering options.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `number_of_elements_to_return` (string, required): Maximum number of maps of sets to return.
        *   `fields_to_return` (string, optional): Comma-separated list of fields to return.
        *   `filter_condition` (string, optional): Filter condition (e.g., `element_type = ALN`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **QRadar AQL Search (`q_radar_q_radar_aql_search`)**
    *   Description: Run an arbitrary AQL query against QRadar. Returns results in CSV format.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `query_format` (string, required): The AQL query string (e.g., `Select * from flows limit 10 last 10 minutes`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Similar Events Query (`q_radar_similar_events_query`)**
    *   Description: Execute a predefined AQL query to find events related to IP Address, Hostname, or Username entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `events_limit_to_fetch` (string, required): Maximum number of events to return (e.g., `25`).
        *   `time_delta_in_minutes` (string, optional): Fetch events from the last X minutes (e.g., `10`).
        *   `fields_to_display` (string, optional): Additional event fields to return (comma-separated).
        *   `hostname_field_name` (string, optional): Custom field name representing hostname in events.
        *   `source_ip_address_field_name` (string, optional): Custom field name representing source IP.
        *   `destination_ip_address_field_name` (string, optional): Custom field name representing destination IP.
        *   `username_field_name` (string, optional): Custom field name representing username.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address, Hostname, or Username entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Lookup for a Value in Reference Tables (`q_radar_lookup_for_a_value_in_reference_tables`)**
    *   Description: Check if a specific value exists within any key in a named reference table.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): The name of the reference table.
        *   `value` (string, required): The value to check for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Add Offense Note (`q_radar_add_offense_note`)**
    *   Description: Add a textual note to a specific QRadar offense.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `offense_id` (string, required): The ID of the QRadar offense.
        *   `note_text` (string, required): The text content of the note.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Lookup for a Value in Reference Set (`q_radar_lookup_for_a_value_in_reference_set`)**
    *   Description: Check if a specific value exists within a named reference set.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): The name of the reference set.
        *   `value` (string, required): The value to check for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Lookup for a Key in Reference Map of Sets (`q_radar_lookup_for_a_key_in_reference_map_of_sets`)**
    *   Description: Check if a specific key exists within a named reference map of sets.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): The name of the reference map of sets.
        *   `key` (string, required): The key to check for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`q_radar_ping`)**
    *   Description: Test connectivity to the QRadar instance API.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **QRadar Simple AQL Search (`q_radar_q_radar_simple_aql_search`)**
    *   Description: Execute a structured AQL query based on provided parameters (table, fields, filter, time, sort, limit).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `table_name` (List[str], required): Table to query (e.g., `["events"]`, `["flows"]`).
        *   `fields_to_return` (string, optional): Comma-separated fields to return (default is all).
        *   `where_filter` (string, optional): AQL WHERE clause content (without the `WHERE` keyword).
        *   `time_frame` (List[str], optional): Predefined time frame or `Custom`.
        *   `start_time` (string, optional): Start time (ISO-8601) if `time_frame` is `Custom`.
        *   `end_time` (string, optional): End time (ISO-8601) if `time_frame` is `Custom` (defaults to now).
        *   `sort_field` (string, optional): Field to sort results by.
        *   `sort_order` (List[str], optional): Sort order (e.g., `["ASC"]`, `["DESC"]`). Requires `sort_field`.
        *   `max_results_to_return` (string, optional, default=50): Maximum results to return.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Similar Flows Query (`q_radar_similar_flows_query`)**
    *   Description: Execute a predefined AQL query to find flows related to IP Address entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `flows_limit_to_fetch` (string, required): Maximum number of flows to return (e.g., `10`).
        *   `time_delta_in_minutes` (string, optional): Fetch flows from the last X minutes (e.g., `10`).
        *   `fields_to_display` (string, optional): Additional flow fields to return (comma-separated).
        *   `source_ip_address_field_name` (string, optional): Custom field name representing source IP.
        *   `destination_ip_address_field_name` (string, optional): Custom field name representing destination IP.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Rule MITRE Coverage (`q_radar_get_rule_mitre_coverage`)**
    *   Description: Get MITRE ATT&CK details for specified QRadar rules using the Use Case Manager application.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `rule_names` (string, required): Comma-separated list of rule names.
        *   `create_insight` (bool, optional): Create an insight with the MITRE coverage information.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Reference Sets (`q_radar_list_reference_sets`)**
    *   Description: List reference sets available in QRadar, with filtering options.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `number_of_elements_to_return` (string, required): Maximum number of sets to return.
        *   `fields_to_return` (string, optional): Comma-separated list of fields to return.
        *   `filter_condition` (string, optional): Filter condition (e.g., `element_type = IP`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Reference Tables (`q_radar_list_reference_tables`)**
    *   Description: List reference tables available in QRadar, with filtering options.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `number_of_elements_to_return` (string, required): Maximum number of tables to return.
        *   `fields_to_return` (string, optional): Comma-separated list of fields to return.
        *   `filter_condition` (string, optional): Filter condition (e.g., `element_type = ALNIC`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Lookup for a Value in Reference Map (`q_radar_lookup_for_a_value_in_reference_map`)**
    *   Description: Check if a specific value exists for any key within a named reference map.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): The name of the reference map.
        *   `value` (string, required): The value to check for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Update Offense (`q_radar_update_offense`)**
    *   Description: Update the status, assignment, closing reason, follow-up flag, or protected status of a QRadar offense.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `offense_id` (string, required): The ID of the QRadar offense to update.
        *   `status` (List[str], required): New status (e.g., `["OPEN"]`, `["CLOSED"]`).
        *   `assigned_to` (string, optional): User login to assign the offense to.
        *   `closing_reason` (string, optional): Required if status is `CLOSED`. QRadar closing reason name.
        *   `follow_up` (bool, optional): Mark offense for follow-up.
        *   `protected` (bool, optional): Mark offense as protected.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Lookup for a Key in Reference Map (`q_radar_lookup_for_a_key_in_reference_map`)**
    *   Description: Check if a specific key exists within a named reference map.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): The name of the reference map.
        *   `key` (string, required): The key to check for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Lookup for a Value in Reference Map of Sets (`q_radar_lookup_for_a_value_in_reference_map_of_sets`)**
    *   Description: Check if a specific value exists within the set associated with any key in a named reference map of sets.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): The name of the reference map of sets.
        *   `value` (string, required): The value to check for.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Configuration

*(Details on configuring the integration, including the QRadar Console IP/Hostname, API Username/Password or Authorized Service Token, Server Certificate validation options, and any specific SOAR platform settings, should be added here.)*
