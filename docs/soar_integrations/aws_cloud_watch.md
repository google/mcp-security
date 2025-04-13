# AWS CloudWatch SOAR Integration

This document details the tools provided by the AWS CloudWatch SOAR integration.

## Tools

### `aws_cloud_watch_search_log_events`

Search log events in AWS CloudWatch.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `log_group` (str, required): Specify the name of the log group, where you want to search for events.
*   `log_streams` (Optional[str], optional, default=None): Specify a comma-separated list of log streams, where you want to search for events.
*   `time_frame` (Optional[List[Any]], optional, default=None): Specify a time frame for the search.
    Possible values:
    1m - 1 minute ago
    1h - 1 hour ago
    1d - 1 day ago
    Note: You can’t combine different values, like 1d2h30m.
*   `start_time` (Optional[str], optional, default=None): Specify the start time for the search. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601
*   `end_time` (Optional[str], optional, default=None): Specify the end time for the search. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time.
*   `custom_filter` (Optional[str], optional, default=None): Specify the custom filter for the search. For additional information please refer to the documentation portal.
*   `max_events_to_return` (Optional[str], optional, default=None): Specify how many events to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_cloud_watch_set_retention_policy`

Set the retention policy for log groups in AWS CloudWatch.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `log_group` (str, required): Specify the name of the log group for which you want to set the retention policy.
*   `retention_days` (List[Any], required): Specify for how many days the data should be retained in the log group.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_cloud_watch_delete_log_group`

Delete a log group in AWS CloudWatch.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `log_group_name` (str, required): Specify the name of the log group that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_cloud_watch_delete_log_stream`

Delete a log stream in a log group in AWS CloudWatch.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `log_group_name` (str, required): Specify the name of the log group that contains the log stream.
*   `log_stream_name` (str, required): Specify the name of the log stream that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_cloud_watch_list_log_streams`

List available log streams in AWS CloudWatch.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `log_groups` (str, required): Specify a comma-separated list of group names for which you want to retrieve log streams.
*   `order_by` (Optional[List[Any]], optional, default=None): Specify how the log streams should be ordered.
*   `sort_order` (Optional[List[Any]], optional, default=None): Specify how the log streams should be sorted.
*   `max_streams_to_return` (Optional[str], optional, default=None): Specify how many streams to return per log group. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `aws_cloud_watch_ping`

Test connectivity to AWS CloudWatch with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
