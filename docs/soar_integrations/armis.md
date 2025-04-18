# Armis SOAR Integration

This document details the tools provided by the Armis SOAR integration.

## Tools

### `armis_ping`

Test connectivity to the Armis with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `armis_update_alert_status`

Update status of the alert in Armis.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alert_id` (str, required): Specify the id of the alert for which you want to update status.
*   `status` (Optional[List[Any]], optional, default=None): Specify what status should be set for the alert.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `armis_enrich_entities`

Enrich entities using information from Armis. Supported entities: IP, Mac Address.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `create_endpoint_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight containing information about the endpoints.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `armis_list_alert_connections`

List connections related to the alert in Armis.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `alert_id` (str, required): Specify the id of the alert for which you want to pull connections data.
*   `lowest_severity_to_fetch` (Optional[List[Any]], optional, default=None): Specify the lowest severity of the connections that should be used when fetching them.
*   `max_connections_to_return` (Optional[str], optional, default=None): Specify how many connections to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
