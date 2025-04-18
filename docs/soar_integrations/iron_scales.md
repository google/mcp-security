# IronScales

## Overview

This integration provides tools to interact with the IronScales email security platform, allowing you to manage incidents and retrieve mitigation details.

## Available Tools

### Get Incident Mitigation Details

**Tool Name:** `iron_scales_get_incident_mitigation_details`

**Description:** Get latest company mitigation details. Results are limited to the latest 1000 incidents, a message will appear displaying if the amount of incidents in the period is over this limit.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `period` (List[Any], required): Specify the time period for which you would like to get incident mitigation details for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Mitigations Per Mailbox

**Tool Name:** `iron_scales_get_mitigations_per_mailbox`

**Description:** Get details of mitigations per mailbox.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incidents_i_ds` (string, required): Provide a comma separated list of incident IDs to search for.
*   `max_pages_to_fetch` (string, required): Specify the maximum number of pages you would like to fetch.
*   `period` (Optional[List[Any]], optional): Specify the time period for which you would like to get mitigations per mailbox for. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `iron_scales_ping`

**Description:** Test connectivity to the IronScales with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Incident Details

**Tool Name:** `iron_scales_get_incident_details`

**Description:** Get full incident details from IronScales.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incidents_i_ds` (string, required): Specify IDs of incidents to fetch details for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Mitigation Impersonation Details

**Tool Name:** `iron_scales_get_mitigation_impersonation_details`

**Description:** Get latest company impersonation incidents. Results are limited to the latest 1000 incidents, a message will appear displaying if the amount of incidents in the period is over this limit. Please note that the IDs returned here are of impersonation attempts, not incidents or reports, so searching these IDs in other endpoints will not return the expected incidents.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `period` (List[Any], required): Specify the time period for which you would like to get mitigation impersonation details for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Classify Incident

**Tool Name:** `iron_scales_classify_incident`

**Description:** Change incidents classification.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incidents_i_ds` (string, required): Specify IDs of incidents to classify.
*   `new_classification` (List[Any], required): Specify the new classification for these incidents. Note: For Phishing Attack classification enter “Attack”, for False positive: “False Positive”, for spam: “Spam”.
*   `classifying_user_email` (string, required): Specify which user is performing the classification by providing his mail address. Note: This email address should be recognized by IronScales.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
