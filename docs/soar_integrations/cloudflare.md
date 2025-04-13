# Cloudflare Integration

## Overview

This integration allows you to connect to Cloudflare to manage firewall rules and rule lists (IP and URL lists). Actions include creating, listing, and updating firewall rules, creating rule lists, and adding IPs or URLs to existing rule lists.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cloudflare details:

*   **API Token:** Your Cloudflare API token with appropriate permissions (e.g., Zone Firewall Rules:Edit, Account Firewall Rules:Edit, Account Filter Lists:Edit).
*   **Account Email:** The email address associated with your Cloudflare account.
*   **(Optional) Account ID:** Your Cloudflare Account ID. Required for account-level operations if not managing rules within a specific zone.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### List Firewall Rules

List available firewall rules in a specific Cloudflare zone.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `zone_name` (string, required): Specify the name of the zone containing the firewall rules.
*   `filter_key` (List[Any], optional): Specify the key to filter results by (e.g., `description`, `action`, `paused`).
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains).
*   `filter_value` (string, optional): Specify the value to filter by.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of firewall rules matching the criteria.

### Add IP To Rule List

Add IP addresses to a specified rule list in Cloudflare. Supported Entities: IP Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name` (string, required): Specify the name of the rule list to add items to.
*   `description` (string, optional): Specify a description for the newly added rule list items.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the operation.

### Add URL To Rule List

Add URLs to a redirect rule list in Cloudflare. Supported Entities: URL. Note: URL entities are treated as "Source URLs".

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name` (string, required): Specify the name of the rule list (must be of type `redirect`).
*   `target_url` (string, required): Specify the target URL for the redirect rule list item.
*   `description` (string, optional): Specify a description for the newly added rule list item.
*   `status_code` (List[Any], optional): Specify the redirect status code (e.g., `301`, `302`).
*   `preserve_query_string` (bool, optional): If enabled, preserve the query string during redirect.
*   `include_subdomains` (bool, optional): If enabled, the rule applies to subdomains.
*   `subpath_matching` (bool, optional): If enabled, the rule matches subpaths.
*   `preserve_path_suffix` (bool, optional): If enabled, preserve the path suffix during redirect.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities (used as source URLs).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the operation.

### Ping

Test connectivity to the Cloudflare with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Update Firewall Rule

Update an existing firewall rule in Cloudflare.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name` (string, required): Specify the name of the rule that needs to be updated.
*   `zone_name` (string, required): Specify the name of the zone containing the firewall rule.
*   `action` (List[Any], optional): Specify the action for the firewall rule (e.g., `block`, `challenge`, `allow`, `js_challenge`, `log`, `bypass`). If "Bypass", `products` parameter is required.
*   `expression` (string, optional): Specify the filter expression for the firewall rule.
*   `products` (string, optional): Comma-separated list of products to bypass (e.g., `zoneLockdown`, `uaBlock`, `bic`, `hot`, `securityLevel`, `rateLimit`, `waf`). Required if `action` is "Bypass".
*   `priority` (string, optional): Specify the priority for the firewall rule.
*   `reference_tag` (string, optional): Specify a reference tag (max 50 characters).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### Create Rule List

Create a rule list (IP or Redirect) in Cloudflare.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `name` (string, required): Specify the name for the rule list.
*   `type` (List[Any], optional): Specify the type for the rule list (`ip` or `redirect`).
*   `description` (string, optional): Specify the description for the rule list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the rule list creation, likely including the new list ID.

### Create Firewall Rule

Create a firewall rule in Cloudflare.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `zone_name` (string, required): Specify the name of the zone where the rule will be created.
*   `expression` (string, required): Specify the filter expression for the firewall rule.
*   `name` (string, optional): Specify the name for the firewall rule.
*   `action` (List[Any], optional): Specify the action for the firewall rule (e.g., `block`, `challenge`, `allow`, `js_challenge`, `log`, `bypass`). If "Bypass", `products` parameter is required.
*   `products` (string, optional): Comma-separated list of products to bypass. Required if `action` is "Bypass".
*   `priority` (string, optional): Specify the priority for the firewall rule.
*   `reference_tag` (string, optional): Specify a reference tag (max 50 characters).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the firewall rule creation, likely including the new rule ID.

## Notes

*   Ensure the Cloudflare integration is properly configured in the SOAR Marketplace tab with a valid API Token and Account Email.
*   The API token requires appropriate permissions for managing firewall rules and lists within the specified zones or account.
*   Refer to the [Cloudflare Filter expression language documentation](https://developers.cloudflare.com/ruleset-engine/rules-language/expressions/) for building filter expressions.
*   Actions modifying firewall rules or lists might take a short time to propagate across Cloudflare's network.
