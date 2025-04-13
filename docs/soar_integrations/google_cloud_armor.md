# Google Cloud Armor

## Overview

This integration provides tools to interact with the Google Cloud Armor service for managing security policies and rules.

## Available Tools

### Create a Security Policy

**Tool Name:** `google_cloud_armor_create_a_security_policy`

**Description:** Create a security policy in the Google Cloud Armor service. This action doesn't run on Google SecOps SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_json` (Union[str, dict], required): The JSON definition of the policy to create. For more information about policies, see [REST Resource: securityPolicies](https://cloud.google.com/compute/docs/reference/rest/v1/securityPolicies).
*   `region` (string, optional): The region to create a policy in. If no value is provided, the global-level security policy is created. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Update a Security Policy

**Tool Name:** `google_cloud_armor_update_a_security_policy`

**Description:** Update the existing security policy in the Google Cloud Armor service. The action cannot update rules in a policy. To add a rule to the related policy, use the Add a Rule to a Security Policy action. This action doesn't run on Google SecOps SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Security policy name to update.
*   `policy_json` (Union[str, dict], required): JSON definition of the policy to update. For more information about the policy updates, see [Method: securityPolicies.patch](https://cloud.google.com/compute/docs/reference/rest/v1/securityPolicies/patch). You cannot update rules with this action. To add a rule to a policy, use the Add a Rule to a Security Policy action.
*   `region` (string, optional): Region for the updated policy. If no value is provided, the global-level security policy is created. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_cloud_armor_ping`

**Description:** Test connectivity to the Google Cloud Armor service with parameters provided at the integration configuration page.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add a Rule to a Security Policy

**Tool Name:** `google_cloud_armor_add_a_rule_to_a_security_policy`

**Description:** Add a new rule to the security policy in the Google Cloud Armor service. This action doesn't run on Google SecOps SOAR entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Security policy name to add a new rule to.
*   `rule_json` (Union[str, dict], required): JSON definition of the rule to add. For more information about adding a rule to a policy, see [Method: securityPolicies.addRule](https://cloud.google.com/compute/docs/reference/rest/v1/securityPolicies/addRule).
*   `region` (string, optional): Region for the policy to add the rule in. If no value is provided, the rule is added to the global-level security policy. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
