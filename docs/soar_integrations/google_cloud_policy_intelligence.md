# Google Cloud Policy Intelligence

## Overview

This integration provides tools to interact with the Google Cloud Policy Intelligence API for searching service account activity.

## Available Tools

### Search Service Account Activity

**Tool Name:** `google_cloud_policy_intelligence_search_service_account_activity`

**Description:** Search activity related to service accounts in Google Cloud Policy Intelligence.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `service_account_resource_name` (string, required): Specify a comma-separated list of service accounts for which you want to fetch activity.
*   `max_activities_to_return` (string, required): Specify how many activities to return. Maximum: 1000.
*   `project_id` (string, optional): Specify the name of the project, where you want to search service account activities. If nothing is provided, the project will be extracted from integration configuration. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_policy_intelligence_ping`

**Description:** Test connectivity to the Google Cloud Policy Intelligence with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
