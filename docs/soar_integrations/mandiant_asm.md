# Mandiant Advantage Attack Surface Management (ASM)

## Overview

This integration provides tools to interact with Mandiant Advantage Attack Surface Management (ASM), allowing you to search for and manage ASM issues and entities.

## Available Tools

### Search Issues

**Tool Name:** `mandiant_asm_search_issues`

**Description:** Search Issues that match the specified criteria in the action Parameters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_i_ds` (Optional[str], optional): Specify a comma-separated list of issue ids, for which you want to return details. Defaults to None.
*   `entity_i_ds` (Optional[str], optional): Specify a comma-separated list of entity ids for which you want to find related issues. Defaults to None.
*   `entity_name` (Optional[str], optional): Specify a comma-separated list of entity names for which you want to find related issues. Defaults to None.
*   `time_parameter` (Optional[List[Any]], optional): Specify what parameter should be used for filtering time. Defaults to None.
*   `time_frame` (Optional[List[Any]], optional): Specify a time frame for the issues. If “Custom” is selected, you also need to provide “Start Time”. Defaults to None.
*   `start_time` (Optional[str], optional): Specify the start time for the results. This parameter is mandatory, if “Custom” is selected for the “Time Frame” parameter. Format: ISO 8601. Defaults to None.
*   `end_time` (Optional[str], optional): Specify the end time for the results. Format: ISO 8601. If nothing is provided and “Custom” is selected for the “Time Frame” parameter then this parameter will use current time. Defaults to None.
*   `lowest_severity_to_return` (Optional[List[Any]], optional): Specify the lowest severity that should be used to return the issues. If “Select One” is selected, this filter is not applied during the search. Defaults to None.
*   `status` (Optional[List[Any]], optional): Specify the status filter for the search. If “Select One” is selected, this filter is not applied during the search. Defaults to None.
*   `tags` (Optional[str], optional): Specify a comma-separated list of tag names, which should be used, when searching for the issues. Defaults to None.
*   `max_issues_to_return` (Optional[str], optional): Specify how many issues to return. Default: 50. Maximum is 200. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including a list of matching issues.

---

### Ping

**Tool Name:** `mandiant_asm_ping`

**Description:** Test connectivity to the MandiantASM with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Issue

**Tool Name:** `mandiant_asm_update_issue`

**Description:** Update an issue in Mandiant ASM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `issue_id` (string, required): Specify the ID of the issue that needs to be updated.
*   `status` (List[Any], required): Specify what status to set for the issues.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get ASM Entity Details

**Tool Name:** `mandiant_asm_get_asm_entity_details`

**Description:** Return information about a Mandiant ASM entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `entity_i_ds` (string, required): Specify a comma-separated list of entity IDs for which you want to fetch details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including details about the specified ASM entities.

---

### Search ASM Entities

**Tool Name:** `mandiant_asm_search_asm_entities`

**Description:** Search entities in Mandiant ASM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `entity_name` (Optional[str], optional): Specify a comma-separated list of entity names for which you want to find entities. Defaults to None.
*   `critical_or_high_issue` (Optional[bool], optional): Specify whether to include only entities with High or Critical Issues. Defaults to None.
*   `minimum_vulnerabilities_count` (Optional[str], optional): Specify how many vulnerabilities should be related to the entity for it to be returned. Defaults to None.
*   `minimum_issues_count` (Optional[str], optional): Specify how many issues should be related to the entity for it to be returned. Defaults to None.
*   `tags` (Optional[str], optional): Specify a comma-separated list of tag names, which should be used, when searching for the entities. Defaults to None.
*   `max_entities_to_return` (Optional[str], optional): Specify how many entities to return. Default: 50. Maximum is 200. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including a list of matching ASM entities.
