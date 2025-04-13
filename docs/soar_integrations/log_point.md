# LogPoint

## Overview

This integration provides tools to interact with the LogPoint SIEM platform, allowing you to execute queries, manage incidents, and list repositories.

## Available Tools

### List Repos

**Tool Name:** `log_point_list_repos`

**Description:** List available repos in Logpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_repos_to_return` (Optional[str], optional): Specify how many reports should be returned. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including a list of available repositories.

---

### Execute Query

**Tool Name:** `log_point_execute_query`

**Description:** Execute search query in Logpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the query that needs to be executed in Logpoint.
*   `time_frame` (List[Any], required): Specify the time frame for the query. If “Custom” is selected, you need to also provide start time and end time.
*   `start_time` (Optional[str], optional): Specify the start time for the query. Format: YYYY-MM-DDThh:mm:ssZ or timestamp. Defaults to None.
*   `end_time` (Optional[str], optional): Specify the end time for the query.Format: YYYY-MM-DDThh:mm:ssZ or timestamp. If nothing is provided action will use current time as end time. Defaults to None.
*   `repos` (Optional[str], optional): Specify a comma-separated list of names of the repos. If nothing is provided, action will search in all repos. Defaults to None.
*   `max_results_to_return` (Optional[str], optional): Specify how many results should be returned. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the query results.

---

### Ping

**Tool Name:** `log_point_ping`

**Description:** Test connectivity to the Logpoint with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Incident Status

**Tool Name:** `log_point_update_incident_status`

**Description:** Update incident status in Logpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the id of the incident, which you want to update.
*   `action` (List[Any], required): Specify the action for the incident.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Execute Entity Query

**Tool Name:** `log_point_execute_entity_query`

**Description:** Execute query in Logpoint based on entities. Currently supported entity types: User, IP, Email Address, URL, File Hash, Hostname. Note: Email Address is a User entity that matches the format of email address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the query that needs to be executed. Please refer to the action documentation for details.
*   `time_frame` (List[Any], required): Specify the time frame for the query. If “Custom” is selected, you need also provide start time, end time by default will be current time.
*   `stop_if_not_enough_entities` (bool, required): If enabled, action will not start execution, unless all of the entity types are available for the specified ".. Entity Keys". Example: if "IP Entity Key" and "File Hash Entity Keys" are specified, but in the scope there are no file hashes then if this parameter is enabled, action will not execute the query.
*   `cross_entity_operator` (List[Any], required): Specify what should be the logical operator used between different entity types.
*   `start_time` (Optional[str], optional): Specify the start time for the query. Format: YYYY-MM-DDThh:mm:ssZ or timestamp. Defaults to None.
*   `end_time` (Optional[str], optional): Specify the end time for the query. Format: YYYY-MM-DDThh:mm:ssZ or timestamp. If nothing is provided action will use current time as end time. Defaults to None.
*   `repos` (Optional[str], optional): Specify a comma-separated list of names of the repos. If nothing is provided, action will search in all repos. Defaults to None.
*   `ip_entity_key` (Optional[str], optional): Specify what key should be used with IP entities. Please refer to the action documentation for details. Defaults to None.
*   `hostname_entity_key` (Optional[str], optional): Specify what key should be used with Hostname entities, when preparing the filter. Please refer to the action documentation for details. Defaults to None.
*   `file_hash_entity_key` (Optional[str], optional): Specify what key should be used with File Hash entities. Please refer to the action documentation for details. Defaults to None.
*   `user_entity_key` (Optional[str], optional): Specify what key should be used with User entities. Please refer to the action documentation for details. Defaults to None.
*   `url_entity_key` (Optional[str], optional): Specify what key should be used with URL entities. Please refer to the action documentation for details. Defaults to None.
*   `email_address_entity_key` (Optional[str], optional): Specify what key should be used with Email Address entities. Please refer to the action documentation for details. Defaults to None.
*   `max_results_to_return` (Optional[str], optional): Specify how many results should be returned. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the query results based on entity filters.
