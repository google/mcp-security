# FireEye HX Integration

## Overview

This integration allows you to connect to FireEye HX (Endpoint Security) and perform actions related to hosts, alerts, alert groups, and indicators of compromise (IOCs).

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Is Contain Malware Alerts

Checks if malware alerts are listed for the provided Host or IP entities on the FireEye HX server.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result, indicating whether malware alerts were found for the specified entities.

### Cancel Host Contain

Creates a task to cancel the containment of a host on the FireEye HX server based on IP or Hostname entities. Note: This action is not supported for Linux hosts by FireEye HX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Host Alert Groups

Lists alert groups related to a specific host (identified by Hostname or IP Address entity) in FireEye HX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `acknowledgment_filter` (List[Any], optional): Filters alert groups based on acknowledgment status (e.g., "Acknowledged", "Unacknowledged", "All").
*   `max_alert_groups_to_return` (string, optional): The maximum number of alert groups to return per entity. Defaults to 20.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing a list of alert groups associated with the specified host(s).

### Contain Host

Creates a task to contain a host on the FireEye HX server based on IP or Hostname entities. Note: This action is not supported for Linux hosts by FireEye HX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `approve_containment` (boolean, required): If True, the containment request is automatically approved. If False, it requires manual approval in the FireEye HX console.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, indicating if the containment task was created.

### Get Host Info

Enriches Host or IP entities with information retrieved from the FireEye HX server.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enriched host information.

### Get Alert Group Details

Retrieves full details for one or more alert groups specified by their IDs.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_group_id` (string, required): A comma-separated list of Alert Group IDs to retrieve details for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information for the specified alert group(s).

### Ping

Tests connectivity to the configured FireEye HX server using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Alerts in Alert Group

Retrieves all alerts belonging to one or more specified alert groups.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_group_id` (string, required): A comma-separated list of Alert Group IDs for which to retrieve alerts.
*   `limit` (string, optional): The maximum number of alerts to return per alert group. Defaults to 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the alerts found within the specified alert group(s).

### Acknowledge Alert Groups

Acknowledges or unacknowledges specified alert groups in FireEye HX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_groups_i_ds` (string, required): A comma-separated list of Alert Group IDs to acknowledge or unacknowledge.
*   `acknowledgment` (List[Any], required): Specifies whether to "Acknowledge" or "Unacknowledge" the alert groups.
*   `acknowledgment_comment` (string, optional): An optional comment to add to the acknowledgment status.
*   `limit` (string, optional): The maximum number of alert group listings to return in the result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get List of File Acquisitions For Host

Retrieves a list of file acquisition tasks requested for a specific host (identified by Hostname or IP entity) from the FireEye HX server.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_term` (string, optional): A search term to filter the file acquisitions (can be any condition value).
*   `limit` (string, optional): The maximum number of acquisition records to return (e.g., 100).
*   `filter_field` (string, optional): Filters results by a specific field value (e.g., `external_id`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of file acquisition tasks for the specified host(s).

### Get Alerts

Retrieves FireEye HX alerts based on specified search conditions and associated Host or IP entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `limit` (string, optional): The maximum number of alerts to return (e.g., 100).
*   `has_share_mode` (List[Any], optional): Filters alerts by indicator share mode ("any", "restricted", "unrestricted").
*   `alert_resolution_status` (List[Any], optional): Filters alerts by resolution status ("any", "active_threat", "alert", "block", "partial_block").
*   `alert_reported_in_last_x_hours` (string, optional): Filters alerts reported within the last X hours (e.g., "4").
*   `alert_source` (List[Any], optional): Filters alerts by source ("any", "exd", "mal", "ioc").
*   `alert_id` (string, optional): Retrieves a specific alert by its identifier.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Hostname or IP Address entities are expected.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the alerts matching the specified criteria.

### Get Indicators

Retrieves information about Indicators of Compromise (IOCs) from the FireEye HX server based on various search parameters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `indicator_category` (string, optional): Filters indicators by category.
*   `search_term` (string, optional): A general search term (name, category, signature, source, condition value).
*   `limit` (string, optional): The maximum number of indicators to return (e.g., 100).
*   `share_mode` (List[Any], optional): Filters indicators by share mode ("any", "restricted", "unrestricted", "visible").
*   `sort_by_field` (string, optional): Sorts results by the specified field (ascending).
*   `created_by` (string, optional): Filters indicators by author.
*   `has_associated_alerts` (boolean, optional): If True, returns only indicators with associated alerts.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing information about the matching IOCs.

### Get Indicator

Retrieves detailed information about a specific indicator identified by its category and name URI names.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `indicator_category` (string, required): The `uri_name` of the indicator category (obtainable from "Get Indicators").
*   `indicator_name` (string, required): The `uri_name` of the indicator (obtainable from "Get Indicators").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified indicator.

## Notes

*   Ensure the FireEye HX integration is properly configured in the SOAR Marketplace tab.
*   Host containment actions (`Contain Host`, `Cancel Host Contain`) are not supported for Linux hosts via the API.
*   Some actions rely on underlying scripts executed by the SOAR platform.
