# Google Security Command Center

## Overview

This integration provides tools to interact with Google Security Command Center (SCC) for managing findings and retrieving vulnerability information related to assets.

## Available Tools

### Push Finding To Pub/Sub

**Tool Name:** `google_security_command_center_push_finding_to_pub_sub`

**Description:** Utility action that will push the finding to pub/sub. Only available for SCC Enterprise.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `finding_names` (string, required): Specify a comma-separated list of finding names which you want to push. Note: finding name has the following structure: organizations/{organization_id}/sources/{source_id}/findings/{finding_id}.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_security_command_center_ping`

**Description:** Test connectivity to the Google Security Command Center with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Asset Vulnerabilities

**Tool Name:** `google_security_command_center_list_asset_vulnerabilities`

**Description:** List vulnerabilities related to the entities in Google Security Command Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `asset_resource_names` (string, required): Specify a comma-separated list of resource names of the assets for which you want to return data.
*   `timeframe` (List[Any], optional): Specify the timeframe for the vulnerabilities/misconfiguration search. Defaults to None.
*   `record_types` (List[Any], optional): Specify what kind of records should be returned. Defaults to None.
*   `output_type` (List[Any], optional): Specify what kind of output should be returned in the JSON result for the asset. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return per record type per assets: Default: 50. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update Finding

**Tool Name:** `google_security_command_center_update_finding`

**Description:** Update finding in Google Security Command Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `finding_name` (string, required): Specify a comma-separated list of finding names which you want to update. Note: finding name has the following structure: organizations/{organization_id}/sources/{source_id}/findings/{finding_id}.
*   `mute_status` (List[Any], optional): Specify the mute status for the finding. Defaults to None.
*   `state_status` (List[Any], optional): Specify the state status for the finding. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Finding Details

**Tool Name:** `google_security_command_center_get_finding_details`

**Description:** Get details about a finding in Google Security Command Center.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `finding_name` (string, required): Specify a comma-separated list of finding names for which you want to return details. Note: finding name has the following structure: organizations/{organization_id}/sources/{source_id}/findings/{finding_id}.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
