# Google Rapid Response (GRR)

## Overview

This integration provides tools to interact with Google Rapid Response (GRR) for managing hunts, clients, and flows.

## Available Tools

### List Hunts

**Tool Name:** `google_grr_list_hunts`

**Description:** Get all available hunts.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `creator` (string, optional): Return hunts created by a specified user. Defaults to None.
*   `offset` (string, optional): Specify Found hunts starting offset. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many hunts to return in the response. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Launched Flows

**Tool Name:** `google_grr_list_launched_flows`

**Description:** List flows launched on a specified client.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `offset` (string, optional): Specify Found flows starting offset. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many flows to return in the response. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Hunt Details

**Tool Name:** `google_grr_get_hunt_details`

**Description:** Get Hunt details.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunt_id` (string, required): ID of the hunt to fetch. Comma separated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_grr_ping`

**Description:** Test connectivity to the Google GRR with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Client Details

**Tool Name:** `google_grr_get_client_details`

**Description:** Get client full details.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `client_id` (string, required): ID of the client. Comma separated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Stop a Hunt

**Tool Name:** `google_grr_stop_a_hunt`

**Description:** Stopping a hunt will prevent new clients from being scheduled and interrupt in-progress flows the next time they change state. This is a hard stop, so in-progress results will be lost, but results already reported are unaffected. Once a hunt is stopped, there is no way to start it again.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunt_id` (string, required): ID of the hunt to stop. Comma separated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Start a Hunt

**Tool Name:** `google_grr_start_a_hunt`

**Description:** Use this to start a newly created hunt. New hunts are created in the PAUSED state, so you’ll need to do this to run them. Hunts that reach their client limit will also be set to PAUSED, use this to restart them after you have removed the client limit.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hunt_id` (string, required): ID of the hunt to start. Comma separated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Clients

**Tool Name:** `google_grr_list_clients`

**Description:** Search Clients in order to start interacting with them.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `offset` (string, optional): Specify Found clients starting offset. Defaults to None.
*   `max_results_to_return` (string, optional): Specify how many clients to return in the response. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
