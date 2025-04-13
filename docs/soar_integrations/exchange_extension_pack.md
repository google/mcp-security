# Exchange Extension Pack Integration

## Overview

This integration extends the capabilities of the standard Exchange integration by providing actions to manage Exchange Mail Flow Rules (Transport Rules) and Compliance Searches within Exchange Online or on-premises Exchange Server. It allows adding/removing senders and domains to specific mail flow rules, listing/deleting these rules, running compliance searches, fetching their results, purging results, and deleting the searches.

## Configuration

This integration utilizes the same configuration as the base Exchange integration (API endpoint, credentials, authentication method) managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings. Specific permissions like Organization Management or EDiscovery roles might be required for certain actions, as noted in their descriptions and the official Microsoft documentation.

## Actions

### Add Senders to Exchange-Siemplify Mail Flow Rule

Adds specified senders (email addresses) to an Exchange-Siemplify mail flow rule. If the rule doesn't exist, it will be created. Can optionally add the sender's domain to corresponding domain rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_add_senders_to` (List[Any], required): Specify the rule to add the sender to. If the rule doesn't exist - action will create it where it's missing.
*   `email_addresses` (string, optional): Specify the email addresses you would like to add to the rule, in a comma separated list. If no parameter will be provided, action will work with User entities.
*   `should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well` (bool, optional): Specify whether the action should automatically take the domains of the provided email addresses and add them as well to the corresponding domain rules (same rule action for domains).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Fetch Compliance Search Results

Fetch results for the completed Compliance Search.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `compliance_search_name` (string, required): Name for the Compliance Search. Note that name shouldn't contain special characters.
*   `max_emails_to_return` (string, optional): Specify how many emails action can return.
*   `remove_compliance_search_once_action_completes` (bool, optional): Specify whether action should remove from Exchange server the search action and any related fetch or purge tasks once the action completes.
*   `create_case_wall_output_table` (bool, optional): Specify if action should create case wall output table. If Max Emails To Return is set to a bigger number, its recommended to uncheck this to increase action performance.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the search results. Note: Maximum of 200 elements will be displayed in the case wall table, but the actual search might have more findings.

### Remove Domains from Exchange-Siemplify Mail Flow Rules

Removes specified domains from existing Exchange-Siemplify mail flow rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_remove_domains_from` (List[Any], required): Specify the rule to remove the Domains from. If the rule doesn't exist - action will do nothing.
*   `domains` (string, optional): Specify the Domains you would like to remove from the rule, in a comma separated list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Compliance Search

Delete Compliance Search and any associated fetch results or purge emails tasks.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `compliance_search_name` (string, required): Name for the Compliance Search. Note that name shouldn't contain special characters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Purge Compliance Search Results

Purge emails found by the completed Compliance Search.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `compliance_search_name` (string, required): Name for the Compliance Search. Note that name shouldn't contain special characters.
*   `perform_a_hard_delete_for_deleted_emails` (bool, optional): Specify whether HardDelete should be performed. This option is applies only to O365 and mark emails for permanent removal from the mailbox.
*   `remove_compliance_search_once_action_completes` (bool, optional): Specify whether action should remove from Exchange server the search action and any related fetch or purge tasks once the action completes.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Domains to Exchange-Siemplify Mail Flow Rules

Creates or updates a mail flow rule to filter emails based on sender domains.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_add_domains_to` (List[Any], required): Specify the rule to add the Domains to. If the rule doesn't exist - action will create it where it's missing.
*   `domains` (string, optional): Specify the Domains you would like to add to the rule, in a comma separated list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Senders from Exchange-Siemplify Mail Flow Rules

Removes specified senders (email addresses) from existing Exchange-Siemplify mail flow rules. Can optionally remove the sender's domain from corresponding domain rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_remove_senders_from` (List[Any], required): Specify the rule to remove the Senders from. If the rule doesn't exist - action will do nothing.
*   `email_addresses` (string, optional): Specify the email addresses you would like to remove from the rule, in a comma separated list. If no parameter will be provided, action will work with entities.
*   `should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well` (bool, optional): Specify whether the action should automatically take the domains of the provided email addresses and remove them as well from the corresponding domain rules (same rule action for domains).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Exchange or O365 server with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Run Compliance Search

Run Exchange Compliance Search based on the provided search conditions. If the fetch compliance search results checkbox is set, action returns the search results similarly to the fetch compliance search results action.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `compliance_search_name` (string, required): Name for the Compliance Search. Note that name shouldn't contain special characters.
*   `location_to_search_emails_in` (string, required): Location to search emails in, can be one of the following: Comma separate list of mailboxes. A distribution group or mail-enabled security group All - for all mailboxes in organization.
*   `subject_filter` (string, optional): Filter condition, specify what subject to search for emails.
*   `sender_filter` (string, optional): Filter condition, specify who should be the sender of needed emails.
*   `recipient_filter` (string, optional): Filter condition, specify who should be the recipient of needed emails.
*   `operator` (List[Any], optional): Operator to use to construct query from conditions above.
*   `time_frame_hours` (string, optional): Time frame interval in hours to search for emails.
*   `fetch_compliance_search_results` (bool, optional): Specify whether the action should immediately fetch the compliance search results. Note that maximum of 200 elements will be displayed, but actual search can have more findings that are shown.
*   `max_emails_to_return` (string, optional): Specify how many emails action can return.
*   `create_case_wall_output_table` (bool, optional): Specify if action should create case wall output table. If Max Emails To Return is set to a bigger number, its recommended to uncheck this to increase action performance.
*   `advanced_query` (string, optional): Instead of subject, sender or recipient filters, provide a query you want to run compliance search on. Consider https://docs.microsoft.com/en-us/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference and https://docs.microsoft.com/en-us/exchange/message-properties-indexed-by-exchange-search-exchange-2013-help?redirectedfrom=MSDN for reference on query syntax.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Exchange-Siemplify Mail Flow Rules

Lists Exchange-Siemplify mail flow rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name_to_list` (List[Any], required): Specify the Rule name you would like to list.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Exchange-Siemplify Mail Flow Rules

Deletes specified Exchange-Siemplify mail flow rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name_to_delete` (List[Any], required): Specify the Rule name you would like to completely delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   This integration requires Organization Management permissions in Exchange/O365 for managing mail flow rules and Compliance Search permissions (e.g., eDiscovery Manager) for compliance search actions. Refer to Microsoft documentation for detailed permission requirements.
*   Actions modifying mail flow rules can impact email delivery across the organization. Use with caution.
*   Compliance Search actions can be resource-intensive on the Exchange server, especially when searching across all mailboxes.
*   The `Fetch Compliance Search Results` action has a display limit (e.g., 200 items) in the SOAR UI, but the underlying search may contain more results.
