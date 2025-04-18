# Netskope Integration

## Overview

This integration allows you to connect to Netskope to manage quarantined files, list alerts, events, and clients, and test connectivity.

## Configuration

The configuration for this integration (Netskope Tenant URL, API Token, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Block File

Block a quarantined file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_id` (string, required): ID of a file, needed to identify a file.
*   `quarantine_profile_id` (string, required): ID of a quarantine profile.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the block operation.

### List Quarantined Files

List quarantined files within a specified time range.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `start_time` (string, optional): Restrict events to those that have timestamps greater than this (unixtime). Needed only if time period is not passed.
*   `end_time` (string, optional): Restrict events to those that have timestamps less than this (unixtime). Needed only if time period is not passed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of quarantined files.

### List Alerts

List alerts based on specified criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, optional): Filter for cloud app events in the alerts database.
*   `type` (string, optional): Filter by alert type (e.g., anomaly, policy, Malware, DLP).
*   `time_period` (string, optional): Time period to search (milliseconds backwards, e.g., 3600, 86400).
*   `start_time` (string, optional): Start timestamp (unixtime). Used if `time_period` is not passed.
*   `end_time` (string, optional): End timestamp (unixtime). Used if `time_period` is not passed.
*   `is_acknowledged` (bool, optional): Filter by acknowledged status.
*   `limit` (string, optional): Number of results to return. Default: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of alerts matching the criteria.

### Allow File

Allow a quarantined file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_id` (string, required): ID of a file, needed to identify a file.
*   `quarantine_profile_id` (string, required): ID of a quarantine profile.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the allow operation.

### Ping

Test connectivity to Netskope.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### List Events

List events based on specified criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, optional): Filter for cloud app events in the events database.
*   `type` (string, optional): Filter by event type (page, application, audit, infrastructure).
*   `time_period` (string, optional): Time period to search (milliseconds backwards, e.g., 3600, 86400).
*   `start_time` (string, optional): Start timestamp (unixtime). Used if `time_period` is not passed.
*   `end_time` (string, optional): End timestamp (unixtime). Used if `time_period` is not passed.
*   `limit` (string, optional): Number of results to return. Default: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of events matching the criteria.

### Download File

Download a quarantined file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_id` (string, required): ID of a file, needed to identify a file.
*   `quarantine_profile_id` (string, required): ID of a quarantine profile.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, potentially including file content or path.

### List Clients

List clients based on specified criteria.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, optional): Filter for all entries in the database.
*   `limit` (string, optional): Number of results to return. Default: 25.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of clients matching the criteria.

## Notes

*   Ensure the Netskope integration is properly configured in the SOAR Marketplace tab with the correct Tenant URL and API Token.
*   Time-based filters can use either `time_period` (relative milliseconds) or `start_time`/`end_time` (absolute unixtime).
*   File actions require both `file_id` and `quarantine_profile_id`.
