# AWS WAF Integration

## Overview

This integration allows you to connect to AWS WAF (Web Application Firewall) to manage Web ACLs, Rule Groups, IP Sets, and Regex Pattern Sets. You can create, update, and list these resources, as well as add or remove rules and patterns based on specific criteria or entities.

## Configuration

To configure this integration within the SOAR platform, you typically need the following AWS credentials and settings:

*   **AWS Access Key ID:** Your AWS access key.
*   **AWS Secret Access Key:** Your AWS secret key.
*   **AWS Default Region:** The AWS region where your WAF resources reside (e.g., `us-east-1`).
*   **Scope:** The scope of the WAF resources (REGIONAL or CLOUDFRONT).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Create Regex Pattern Set

Create a Regex Pattern Set in AWS WAF based on entities. Note: Regex Pattern Set can only contain 10 patterns per set and there can only be 10 Regex Pattern Sets at max.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the Regex Pattern set. Note: The name must have 1-128 characters. Valid characters: A-Z, a-z, 0-9, - (hyphen), and _ (underscore).
*   `description` (string, optional): Specify the description for the Regex Pattern set.
*   `tags` (string, optional): Specify additional tags that should be added to the Regex Pattern set. Format: key_1:value_1,key_2:value_1.
*   `domain_pattern` (bool, optional): If enabled, action will retrieve domain part out of urls and create a regex pattern based on them. Example: http://test.com/folder will be converted to a pattern ^(http)(s|)(://)(test.com).*
*   `ip_pattern` (bool, optional): If enabled, action will construct a proper regex pattern out of IP address instead of using raw value. Example: 10.0.0.1 will be converted into ^(http)(s|)(://)(10.0.0.1).*
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL and IP Address entities if corresponding pattern flags are enabled.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ARN and ID of the created set.

### Remove Rule From Rule Group

Remove a rule from the rule group in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_group_names` (string, required): Specify the comma-separated list of Rule Group names. Example: name_1,name_2
*   `rule_name` (string, required): Specify the name of the rule that should be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create Web ACL

Create a Web ACL in AWS WAF. Note: You can have only 100 Web ACLs per region.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the Web ACL. Note: The name must have 1-128 characters. Valid characters: A-Z, a-z, 0-9, - (hyphen), and _ (underscore).
*   `rule_source_type` (List[Any], required): Specify what rule type should be used (IP Set or Rule Group).
*   `rule_source_name` (string, required): Specify the name of the source (IP Set or Rule Group name).
*   `enable_sampled_requests` (bool, required): If enabled, AWS WAF will store a sampling of the web requests that match the rules.
*   `enable_cloud_watch_metrics` (bool, required): If enabled, the associated resource sends metrics to CloudWatch.
*   `cloud_watch_metric_name` (string, required): Specify the name of the CloudWatch Metric. Note: The name must have 1-128 characters. Valid characters: A-Z, a-z, 0-9, - (hyphen), and _ (underscore).
*   `default_action` (List[Any], required): Specify the default action for requests that don't match any rules (e.g., Allow, Block).
*   `rule_priority` (string, required): Specify the priority of the rule (unique within the Web ACL).
*   `ip_set_action` (List[Any], optional): Specify the action for rules based on the IP set (e.g., Allow, Block). Required if `rule_source_type` is "IP Set".
*   `description` (string, optional): Specify the description for the Web ACL.
*   `tags` (string, optional): Specify additional tags. Format: key_1:value_1,key_2:value_1.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ARN and ID of the created Web ACL.

### Add Pattern To Regex Pattern Set

Add string patterns to the Regex Pattern Set in AWS WAF. Note: Regex Pattern Set can only contain 10 patterns per set.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `regex_pattern_set_names` (string, required): Specify the comma-separated list of Regex Pattern set names. Example: name_1,name_2
*   `patterns` (string, required): Specify the comma-separated list of patterns that should be added. Example: pattern_1,pattern_2
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Create IP Set

Create an IP Set in AWS WAF, based on entities. Note: IP Set is created in the following format Siemplify_{Name}_{IP Type}.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the base name of the IP set. The final name will be `Siemplify_{Name}_{IP Type}`. Note: The name must have 1-128 characters. Valid characters: A-Z, a-z, 0-9, - (hyphen), and _ (underscore).
*   `description` (string, optional): Specify the description for the IP set.
*   `tags` (string, optional): Specify additional tags. Format: key_1:value_1,key_2:value_1.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ARN and ID of the created IP Set.

### Create Rule Group

Create a rule group in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name of the rule group. Note: The name must have 1-128 characters. Valid characters: A-Z, a-z, 0-9, - (hyphen), and _ (underscore).
*   `capacity` (string, required): Specify the capacity of the rule group (max 1500). Cannot be changed after creation.
*   `enable_sampled_requests` (bool, required): If enabled, AWS WAF will store a sampling of the web requests that match the rules.
*   `enable_cloud_watch_metrics` (bool, required): If enabled, the associated resource sends metrics to CloudWatch.
*   `cloud_watch_metric_name` (string, required): Specify the name of the CloudWatch Metric. Note: The name must have 1-128 characters. Valid characters: A-Z, a-z, 0-9, - (hyphen), and _ (underscore).
*   `description` (string, optional): Specify the description for the Rule Group.
*   `tags` (string, optional): Specify additional tags. Format: key_1:value_1,key_2:value_1.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ARN and ID of the created Rule Group.

### Ping

Test connectivity to AWS WAF with parameters provided at the integration configuration page on Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Rule From Web ACL

Remove a rule from Web ACL in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `web_acl_names` (string, required): Specify the comma-separated list of Web ACL names. Example: name_1,name_2
*   `rule_name` (string, required): Specify the name of the rule that should be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List IP Sets

List available IP Sets in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_ip_sets_to_return` (string, optional): Specify how many IP sets to return. Default is 50. Maximum is 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available IP Sets.

### List Regex Pattern Sets

List available Regex Pattern Sets in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_regex_pattern_sets_to_return` (string, optional): Specify how many Regex Pattern Sets to return. Default is 5. Maximum is 10.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available Regex Pattern Sets.

### Add Rule To Rule Group

Add a rule to the rule group in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_group_names` (string, required): Specify the comma-separated list of Rule Group names. Example: name_1,name_2
*   `rule_json_object` (Union[str, dict], required): Specify the JSON object of the rule. Refer to AWS WAF documentation for the rule structure.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Web ACLs

List available web ACLs in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_web_ac_ls_to_return` (string, optional): Specify how many Web ACLs to return. Default is 50. Maximum is 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available Web ACLs.

### List Rule Groups

List available rule groups in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_rule_groups_to_return` (string, optional): Specify how many Rule Groups to return. Default is 50. Maximum is 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available Rule Groups.

### Remove IP From IP Set

Remove IP addresses from the IP Set in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ip_set_names` (string, required): Specify the comma-separated list of IP set names. Example: name_1,name_2
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add IP To IP Set

Add IP addresses to the IP Set in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ip_set_names` (string, required): Specify the comma-separated list of IP set names. Example: name_1,name_2
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Pattern From Regex Pattern Set

Remove patterns from the Regex Pattern Set in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `regex_pattern_set_names` (string, required): Specify the comma-separated list of Regex Pattern set names. Example: name_1,name_2
*   `patterns` (string, required): Specify the comma-separated list of patterns that should be removed. Example: pattern_1,pattern_2
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Entity From Regex Pattern Set

Remove string patterns based on entities from the Regex Pattern Set in AWS WAF.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `regex_pattern_set_names` (string, required): Specify the comma-separated list of Regex Pattern set names. Example: name_1,name_2
*   `domain_pattern` (bool, optional): If enabled, action will retrieve domain part out of urls and search for a regex pattern based on them. Example: http://test.com/folder will be searched as pattern ^(http|https)(:\\/\\/)(\\Qtest.com\\E).*
*   `ip_pattern` (bool, optional): If enabled, action will search for a regex pattern out of IP address instead of raw value. Example: 10.0.0.1 will be searched as ^(http|https)(:\\/\\/)(\\Q10.0.0.1\\E).*
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL and IP Address entities if corresponding pattern flags are enabled.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Rule To Web ACL

Add a rule based on IP Sets or Rule Groups to Web ACL in AWS WAF. Note: at maximum Web ACL can contain 1500 rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `web_acl_names` (string, required): Specify the comma-separated list of Web ACL names. Example: name_1,name_2
*   `rule_source_type` (List[Any], required): Specify what rule type should be used (IP Set or Rule Group).
*   `rule_source_name` (string, required): Specify the name of the source (IP Set or Rule Group name).
*   `rule_priority` (string, required): Specify the priority of the rule (unique within the Web ACL).
*   `ip_set_action` (List[Any], optional): Specify the action for rules based on the IP set (e.g., Allow, Block). Required if `rule_source_type` is "IP Set".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Entity To Regex Pattern Set

Add string patterns based on entities to the Regex Pattern Set in AWS WAF. Note: Regex Pattern Set can only contain 10 patterns per set.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `regex_pattern_set_names` (string, required): Specify the comma-separated list of Regex Pattern set names. Example: name_1,name_2
*   `domain_pattern` (bool, optional): If enabled, action will retrieve domain part out of urls and create a regex pattern based on them. Example: http://test.com/folder will be converted to a pattern ^(http|https)(:\\/\\/)(\\Qtest.com\\E).*
*   `ip_pattern` (bool, optional): If enabled, action will construct a proper regex pattern out of IP address instead of using raw value. Example: 10.0.0.1 will be converted into ^(http|https)(:\\/\\/)(\\Q10.0.0.1\\E).*
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL and IP Address entities if corresponding pattern flags are enabled.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the AWS WAF integration is properly configured in the SOAR Marketplace tab with valid AWS credentials and region.
*   Be mindful of AWS WAF limits (e.g., number of Web ACLs, rules per Web ACL, patterns per Regex Pattern Set).
*   Actions modifying WAF configurations (e.g., adding IPs, rules, patterns) might take some time to propagate.
*   Refer to AWS WAF documentation for detailed information on rule JSON structure and naming conventions.
