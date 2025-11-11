# StellarCyberStarlight SOAR Integration

## Overview

This integration provides tools for interacting with Stellar Cyber Starlight from within the Chronicle SOAR platform. It allows performing simple and advanced searches across various indexes, updating security events, and testing connectivity.

## Tools

### `stellar_cyber_starlight_simple_search`

Perform simple search in Stellar Cyber Starlight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `index` (str, required): Specify in which index do you want to search. You can find a list of known indexes in the documentation.
*   `query` (str, required): Specify query filter for the search.
*   `max_results_to_return` (Optional[str], optional, default=None): Specify how many results to return in response.
*   `sort_field` (Optional[str], optional, default=None): Specify the field, which should be used for sorting.
*   `sort_order` (Optional[List[str]], optional, default=None): Specify the sort order for the result.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `stellar_cyber_starlight_ping`

Test connectivity to Stellar Cyber Starlight with parameters provided at the integration configuration page on Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `stellar_cyber_starlight_update_security_event`

Update security event in Stellar Cyber Starlight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `index` (str, required): Specify the index of the security event.
*   `id` (str, required): Specify the ID of the security event.
*   `status` (List[str], required): Specify the new status for the security event.
*   `comment` (Optional[str], optional, default=None): Specify a comment for the security event.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `stellar_cyber_starlight_advanced_search`

Perform advanced search in Stellar Cyber Starlight.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `index` (str, required): Specify in which index do you want to search. You can find a list of known indexes in the documentation.
*   `dsl_query` (str, required): Specify the json object of the DSL query that you want to execute.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
