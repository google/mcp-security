# ArcSight Logger SOAR Integration

This document details the tools provided by the ArcSight Logger SOAR integration.

## Tools

### `arc_sight_logger_send_query`

Send a query to get information about related events from ArcSight Logger event log manager.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query to send to ArcSight Logger event search.
*   `max_events_to_return` (Optional[str], optional, default=None): Specify the amount of events to return. Limit is 10000. This is ArcSight Logger limitation.
*   `time_frame` (Optional[str], optional, default=None): Specify the time frame which will be used to fetch events.
    Possible values:
    1m - 1 minute ago
    1h - 1 hour ago
    1d - 1 day ago
    Note: You can’t combine different values, like 1d2h30m.
*   `fields_to_fetch` (Optional[str], optional, default=None): Specify what fields to fetch from ArcSight Logger. If nothing is specified, then all of the available fields will be returned.
*   `include_raw_event_data` (Optional[bool], optional, default=None): If enabled, raw event data is included in the response.
*   `local_search_only` (Optional[bool], optional, default=None): Indicates that ArcSight Logger event search is local only, and does not include ArcSight Logger peers. Set to false if you want to include peers in the event search.
*   `discover_fields` (Optional[bool], optional, default=None): Indicates that the ArcSight Logger search should try to discover fields in the events found.
*   `sort` (Optional[str], optional, default=None): Specify what sorting method to use.
    Possible values:
    ascending
    descending
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `arc_sight_logger_ping`

Test connectivity to ArcSight Logger with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
