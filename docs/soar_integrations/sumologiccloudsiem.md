# SumoLogicCloudSIEM SOAR Integration

## Overview
This document outlines the tools available in the Sumo Logic Cloud SIEM SOAR integration. These tools allow interaction with Sumo Logic Cloud SIEM for managing insights, enriching entities, and searching signals.

## Tools

### `sumo_logic_cloud_siem_add_tags_to_insight`
Add tags to insight in Sumo Logic Cloud SIEM.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `insight_id` (str, required): Specify the ID of the insight to which action needs to add tags.
*   `tags` (str, required): Specify a comma-separated list of tags that needs to be added in insight.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `sumo_logic_cloud_siem_ping`
Test connectivity to the Sumo Logic Cloud SIEM with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `sumo_logic_cloud_siem_update_insight`
Update insight status in Sumo Logic Cloud SIEM.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `insight_id` (str, required): Specify the ID of the insight needs to be updated.
*   `status` (List[str], required): Specify what status to set for the insight.
*   `assignee_type` (List[str], required): Specify the assignee type for the "Assignee" parameter.
*   `assignee` (Optional[str], optional, default=None): Specify the assignee identifier.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `sumo_logic_cloud_siem_enrich_entities`
Enrich entities using information from Sumo Logic Cloud SIEM. Supported entities: Hostname, User, IP address.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `create_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight containing all of the retrieved information about the entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `sumo_logic_cloud_siem_add_comment_to_insight`
Add a comment to insight in Sumo Logic Cloud SIEM.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `insight_id` (str, required): Specify the ID of the insight to which action needs to add a comment.
*   `comment` (str, required): Specify the comment that needs to be added in insight.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `sumo_logic_cloud_siem_search_entity_signals`
Search signals related to entities in Sumo Logic Cloud SIEM. Supported entities: IP Address, Hostname, Username.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `lowest_severity_to_return` (Optional[str], optional, default=None): Specify the lowest severity number that will be used to return signals. Maximum: 10.
*   `time_frame` (Optional[List[str]], optional, default=None): Specify a time frame for the results. If "Custom" is selected, you also need to provide "Start Time". If "30 Minutes Around Alert Time" is selected, action will search the alerts 30 minutes before the alert happened till the 30 minutes after the alert has happened. Same idea applies to "1 Hour Around Alert Time" and "5 Minutes Around Alert Time".
*   `start_time` (Optional[str], optional, default=None): Specify the start time for the results. This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter. Format: ISO 8601
*   `end_time` (Optional[str], optional, default=None): Specify the end time for the results. Format: ISO 8601. If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter will use current time.
*   `max_signals_to_return` (Optional[str], optional, default=None): Specify how many signals to return per entity. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.
