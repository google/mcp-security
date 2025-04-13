# Mimecast Integration

## Overview

This integration allows you to connect to Mimecast to search archive emails, manage held messages (release/reject), manage sender lists (permit/block), and test connectivity.

## Configuration

The configuration for this integration (Application ID, Application Key, Access Key, Secret Key, Base URL, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Advanced Archive Search

Search archive emails using a custom XML query in Mimecast. Note: when providing time make sure to take in the account timezones. For ease of use, Siemplify instance and Mimecast instance should be in the same timezone.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `xml_query` (string, required): Specify an XML query that should be used when searching for archive emails. Please visit Mimecast documentation for more details on query structure.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Release Message

Release message in Mimecast. Note: only messages with status "Held" can be released.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): Specify the ID of the message that needs to be released.
*   `release_to_sandbox` (bool, optional): If enabled, action will release the message to the sandbox.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the release operation.

### Reject Message

Reject message in Mimecast. Note: only messages with status "Held" can be rejected.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): Specify the ID of the message that needs to be rejected.
*   `note` (string, optional): Specify an additional note containing an explanation regarding why the message was rejected.
*   `reason` (List[Any], optional): Specify the reason for rejection.
*   `notify_sender` (bool, optional): If enabled, action will notify the sender about rejection.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the rejection operation.

### Permit Sender

Permit sender in Mimecast for a specific recipient.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `sender` (string, required): Specify the email address of the sender to permit.
*   `recipient` (string, required): Specify the email address of the recipient to permit the sender for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Block Sender

Block sender in Mimecast for a specific recipient.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `sender` (string, required): Specify the email address of the sender to block.
*   `recipient` (string, required): Specify the email address of the recipient to block the sender for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Mimecast with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Simple Archive Search

Search archive emails using defined parameters in Mimecast. Note: when providing time make sure to take in the account timezones. For ease of use, Siemplify instance and Mimecast instance should be in the same timezone.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `fields_to_return` (string, required): Specify a comma-separated list of fields that needs to be returned.
*   `time_frame` (List[Any], required): Specify a time frame for the search. If "Custom" is selected, provide "Start Time".
*   `mailboxes` (string, optional): Specify a comma-separated list of mailboxes that need to be searched.
*   `from_` (string, optional): Specify a comma-separated list of email addresses from which the emails were sent.
*   `to` (string, optional): Specify a comma-separated list of email addresses to which the emails were sent.
*   `subject` (string, optional): Specify a subject that needs to be searched.
*   `start_time` (string, optional): Specify the start time for the search. Format: ISO 8601. Mandatory if Time Frame is "Custom".
*   `end_time` (string, optional): Specify the end time for the search. Format: ISO 8601. Uses current time if Time Frame is "Custom" and this is empty.
*   `max_emails_to_return` (string, optional): Specify how many emails to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Report Message (Deprecated)

Deprecated. Report message in Mimecast. Note: only messages with status "Held", "Archived", "Bounced" can be reported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): Specify the ID of the message that needs to be reported.
*   `comment` (string, optional): Specify the comment for the report.
*   `report_as` (List[Any], optional): Specify the report type for the message.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the Mimecast integration is properly configured in the SOAR Marketplace tab.
*   Be mindful of timezones when specifying time ranges in search actions.
*   The `Release Message` and `Reject Message` actions only work on messages currently in a "Held" state.
*   The `Report Message` action is deprecated.
