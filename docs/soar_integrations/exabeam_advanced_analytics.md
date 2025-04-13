# Exabeam Advanced Analytics Integration

## Overview

This integration allows you to connect to Exabeam Advanced Analytics and perform actions such as listing watchlists and their items, creating/deleting watchlists, adding/removing entities from watchlists, adding comments to entities, and enriching entities with Exabeam data.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### List Watchlist Items

List available items in watchlists from Exabeam Advanced Analytics.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_titles` (string, required): Specify a comma-separated list of watchlist titles for which you want to return items.
*   `max_items_to_return` (string, optional): Specify how many watchlist items should be returned.
*   `max_days_backwards` (string, optional): Specify how many days backwards to list watchlists. Default: 1.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Watchlist

Delete a watchlist in Exabeam Advanced Analytics.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_title` (string, required): Specify the title of the watchlist that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Exabeam Advanced Analytics with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Enrich Entities

Enrich entities using the information from Exabeam Advanced Analytics. Supported entities: Hostname, IP and User. Event time frame parameter works with hours.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `return_entity_timeline` (bool, required): If enabled, action will return the timeline for the entity.
*   `event_time_frame` (string, optional): Specify the frame for the events that you want to see in hours.
*   `only_anomaly_events` (bool, optional): If enabled, action will only return events that are considered to be anomalies.
*   `lowest_event_risk_score_to_fetch` (string, optional): Specify what should be the lowest risk score of the event in order to ingest it. If nothing is specified, action will not do any filtering.
*   `return_comments` (bool, optional): If enabled, action will return comments related to the entity.
*   `create_insight` (bool, optional): If enabled, action will create an insight per entity.
*   `max_events_to_return` (string, optional): Specify how many events should be returned. If nothing is specified, action will return all of the events.
*   `max_comments_to_return` (string, optional): Specify how many comments to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create Watchlist

Create a watchlist in Exabeam Advanced Analytics.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `title` (string, required): Specify the title of the watchlist.
*   `category` (List[Any], required): Specify the category for the watchlist.
*   `access_control` (List[Any], required): Specify the access control for the watchlist.
*   `description` (string, optional): Specify description for the watchlist.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Comments To Entity

Add comments to entities in Exabeam Advanced Analytics. Supported entities: Hostname, IP and User.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `comment` (string, required): Specify the comment that needs to be added to the entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Entity From Watchlist

Remove entities from the watchlist in Exabeam Advanced Analytics. Note: Watchlists with category 'AssetLabels' and 'UserLabels' are not supported in this action.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_title` (string, required): Specify the title of the watchlist from which you want to remove entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Entity To Watchlist

Add entities to the watchlist in Exabeam Advanced Analytics. Note: Watchlists with category 'AssetLabels' and 'UserLabels' are not supported in this action.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `watchlist_title` (string, required): Specify the title of the watchlist of which you want to add entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Watchlists

List available watchlists in Exabeam Advanced Analytics.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_watchlists_to_return` (string, optional): Specify how many watchlists should be returned.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the Exabeam Advanced Analytics integration is properly configured in the SOAR Marketplace tab.
*   Some actions have limitations regarding watchlist categories (e.g., 'AssetLabels', 'UserLabels').
