# Exchange Integration

## Overview

This integration allows you to connect to Microsoft Exchange and perform various email-related actions, including sending emails (plain text, HTML, vote mails), searching emails, managing attachments, managing inbox rules (add/remove domains/senders, list, delete), blocking/unblocking senders, moving emails, extracting EML data, managing Out Of Facility (OOF) settings, and handling OAuth authentication tokens.

## Configuration

The configuration for this integration (API endpoint, credentials, authentication method like OAuth or Basic) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings. Specific permissions like EDiscovery Group, Author permissions, or impersonation might be required for certain actions, as noted in their descriptions.

## Actions

### Unblock Sender by Message ID

Unmarks an email as junk based on its Message ID and removes the sender from the "Blocked Senders List". Optionally moves the email back to the inbox.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `move_items_back_to_inbox` (bool, required): Should the action move the specified messages back to the inbox folder.
*   `message_i_ds` (string, optional): Filter condition, specify emails with which email ids to find. Should accept comma separated list of message ids to unmark as junk. If message id is provided, subject, sender and recipient filters are ignored.
*   `mailboxes_list_to_perform_on` (string, optional): Filter condition, If you have a specific list of mailboxes you would like to conduct the operation on, for better timing, please provide them here. Should accept a comma separated list of mail addresses to unmark the messages as junk in. If a mailboxes list is provided, "Perform Action in all Mailboxes" parameter will be ignored.
*   `folder_name` (string, optional): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `subject_filter` (string, optional): Filter condition, specify subject to search for emails.
*   `sender_filter` (string, optional): Filter condition, specify who should be the sender of needed emails.
*   `recipient_filter` (string, optional): Filter condition, specify who should be the recipient of needed emails.
*   `unmark_all_matching_emails` (bool, optional): Filter condition, specify if action should Unmark all matched by criteria emails from the mailbox or Unmark only first match.
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, move to junk and block sender emails in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `time_frame_minutes` (string, optional): Filter condition, specify in what time frame in minutes should action look for emails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Mail

Send Email from specific mailbox to an arbitrary list of recipients. Action can be used to inform users about specific alerts created in the Siemplify or inform about the results of processing of specific alerts.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subject` (string, required): The mail subject part.
*   `send_to` (string, required): Arbitrary comma separated list of email addresses for the email recipients. For example: user1@company.co, user2@company.co.
*   `mail_content` (EmailContent, required): The email body part.
*   `cc` (string, optional): Arbitrary comma separated list of email addresses to be put in the CC field of email. Format is the same as for the "Send to" field.
*   `bcc` (string, optional): Arbitrary comma separated list of email addresses to be put in the BCC field of email. Format is the same as for the "Send to" field.
*   `attachments_paths` (string, optional): Comma separated list of attachments file paths stored on the server for addition to the email. For example: C:\\<Siemplify work dir>\\file1.pdf, C:\\<Siemplify work dir>\\image2.jpg.
*   `reply_to_recipients` (string, optional): Specify a comma-separated list of recipients that will be used in the "Reply-To" header. Note: The Reply-To header is added when the originator of the message wants any replies to the message to go to that particular email address rather than the one in the "From:" address.
*   `base64_encoded_certificate` (string, optional): Specify a base64 encoded certificate that will be used to either encrypt or sign the email. Note: for signing you need to also provide "Base64 Encoded Signature". For encryption, only this parameter needs to have a value.
*   `base64_encoded_signature` (string, optional): Specify a base64 encoded signature that will be used to sign the email. Note: "Base64 Encoded Certificate" needs to be provided as well for signature to work and contain the signing certificate.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Domains to Exchange-Siemplify Inbox Rules

Creates or updates an inbox rule to filter emails based on sender domains.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_add_domains_to` (List[Any], required): Specify the rule to add the Domains to. If the rule doesn't exist - action will create it where it's missing.
*   `domains` (string, optional): Specify the Domains you would like to add to the rule, in a comma separated list.
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Thread Reply

Send a message as a reply to the email thread.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): Specify the ID of the message to which you want to send a reply.
*   `folder_name` (string, required): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `content` (EmailContent, required): Specify the content of the reply.
*   `reply_all` (bool, required): If enabled, action will send a reply to all recipients related to the original email. Note: this parameter has priority over “Reply To“ parameter.
*   `attachments_paths` (string, optional): Specify a comma separated list of attachments file paths stored on the server for addition to the email.
*   `reply_to` (string, optional): Specify a comma-separated list of emails to which you want to send this reply. If nothing is provided and “Reply All“ is disabled, action will only send a reply to the sender of the email. If “Reply All“ is enabled, action will ignore this parameter.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Search Mails

Search for specific emails in configured mailbox using multiple provided search criteria. Action return information on found in mailbox emails in JSON format.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, optional): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `message_i_ds` (string, optional): Specify a comma-separated list of message ids that need to be searched. Note: this filter has priority over the other ones.
*   `subject_filter` (string, optional): Filter condition, specify what subject to search for emails.
*   `sender_filter` (string, optional): Filter condition, specify who should be the sender of needed emails.
*   `recipient_filter` (string, optional): Filter condition, specify who should be the recipient of needed emails.
*   `time_frame_minutes` (string, optional): Filter condition, specify in what time frame in minutes should action look for emails.
*   `only_unread` (bool, optional): Filter condition, specify if search should look only for unread emails.
*   `max_emails_to_return` (string, optional): Return max X emails as an action result.
*   `search_in_all_mailboxes` (bool, optional): If checked, search in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Search in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `mailboxes` (string, optional): Specify a comma-separated list of mailboxes that need to be searched. This parameter has priority over "Search in all mailboxes".
*   `start_time` (string, optional): Specify the start time for the email search. Format: ISO 8601. This parameter has a priority over "Time Frame (minutes)".
*   `end_time` (string, optional): Specify the end time for the email search. Format: ISO 8601. If nothing is provided and "Start Time" is valid then this parameter will use current time.
*   `body_regex_filter` (string, optional): Specify a regex pattern that needs to be searched in body part of the email.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Wait for Vote Mail Results

Fetches the responses of a vote mail sent by the "Send Vote Mail" action, waiting for replies.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `vote_mail_message_id` (string, required): Message_id of the vote email, which current action would be waiting for. If message has been sent using Send Vote Mail action, please select SendVoteMail.JSONResult|message_id field as a placeholder.
*   `mail_recipients` (string, required): Comma-separated list of recipient emails, response from which current action would be waiting for. Please select SendVoteMail.JSONResult|to_recipients field as a placeholder.
*   `folder_to_check_for_reply` (string, required): Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `folder_to_check_for_sent_mail` (string, required): Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the sent mail in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive.
*   `how_long_to_wait_for_recipient_reply_minutes` (string, required): How long in minutes to wait for the user's reply before marking it timed out.
*   `wait_for_all_recipients_to_reply` (bool, optional): Parameter can be used to define if there are multiple recipients - should the Action wait for responses from all of recipients until timeout, or Action should wait for first reply to proceed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Generate Token

For integration configuration with Oauth authentication, get a refresh token using the authorization URL received in the Get Authorization action.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `authorization_url` (string, required): Use the authorization URL received in the Get Authorization URL action to request a refresh token.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Vote Mail

Send emails with easy answering options, to allow stakeholders to be combined in the automated processes without accessing the Siemplify UI.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subject` (string, required): The mail subject part.
*   `send_to` (string, required): Arbitrary comma separated list of email addresses for the email recipients. For example: user1@company.co, user2@company.co.
*   `question_or_decision_description` (EmailContent, required): The question you would like to ask, or describe the decision you would like the recipient to be able to respond to.
*   `structure_of_voting_options` (List[Any], required): Choose the structure of the vote to be sent to the recipients.
*   `cc` (string, optional): Arbitrary comma separated list of email addresses to be put in the CC field of email. Format is the same as for the "Send to" field.
*   `bcc` (string, optional): Arbitrary comma separated list of email addresses to be put in the BCC field of email. Format is the same as for the "Send to" field.
*   `attachments_paths` (string, optional): Comma separated list of attachments file paths stored on the server for addition to the email. For example: C:\\<Siemplify work dir>\\file1.pdf, C:\\<Siemplify work dir>\\image2.jpg.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Exchange-Siemplify Inbox Rules

Lists Exchange-Siemplify inbox rules for specified mailboxes.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name_to_list` (List[Any], required): Specify the Rule name you would like to list from the relevant mailboxes.
*   `mailboxes_list_to_perform_on` (string, optional): Filter condition, If you have a specific list of mailboxes you would like to conduct the operation on, for better timing, please provide them here. Should accept a comma separated list of mail addresses to list the rules from. If a mailboxes list is provided, "Perform Action in all Mailboxes" parameter will be ignored.
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Exchange-Siemplify Inbox Rules

Deletes specified Exchange-Siemplify inbox rules from mailboxes.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_name_to_delete` (List[Any], required): Specify the Rule name you would like to completely delete from the relevant mailboxes.
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Move Mail To Folder

Move one or multiple emails from source email folder to another folder in mailbox.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_folder_name` (string, required): Source folder to move emails from. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `destination_folder_name` (string, required): Destination folder to move emails to. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `source_mailbox` (string, optional): Specify the source mailbox to move the email from. Parameter accepts multiple values as a comma-separated string. If multiple values are provided, matching emails are copied from every accessible specified mailbox.
*   `destination_mailbox` (string, optional): Specify the destination mailbox to move the matching emails to.
*   `message_i_ds` (string, optional): Filter condition, specify emails with which email ids to find. Should accept comma separated multiple message ids. If message id is provided, subject filter is ignored.
*   `subject_filter` (string, optional): Filter condition, specify what subject to search for emails.
*   `only_unread` (bool, optional): Filter condition, specify if search should look only for unread emails.
*   `move_in_all_mailboxes` (bool, optional): If checked, search and move emails in all mailboxes accessible with current impersonalization settings. If the source or destination mailbox is specified, this parameter is ignored. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Move in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `time_frame_minutes` (string, optional): Filter condition, specify in what time frame in minutes should action look for emails.
*   `limit_the_amount_of_information_returned_in_the_json_result` (bool, optional): If enabled, the amount of information returned by the action will be limited only to the key email fields.
*   `disable_the_action_json_result` (bool, optional): If enabled, action will not return JSON result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Email And Wait

Send email and wait for a reply.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subject` (string, required): The subject of the email.
*   `send_to` (string, required): Recipient email address. Multiple addresses can be separated by commas.
*   `mail_content` (EmailContent, required): Email body.
*   `cc` (string, optional): CC email address. Multiple addresses can be separated by commas.
*   `bcc` (string, optional): BCC email address. Multiple addresses can be separated by commas.
*   `fetch_response_attachments` (bool, optional): Allows attachment of files from response mail.
*   `folder_to_check_for_reply` (string, optional): Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to Microsoft Exchange instance with parameters provided at the integration configuration page on Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Extract EML Data

Extract data from email's EML attachments.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): e.g. <1701cf01ba314032b2f1df43262a7723@gmail.com>.
*   `folder_name` (string, optional): Folder to fetch from. Default is Inbox. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `regex_map_json` (Union[str, dict], optional): e.g. {"ips": "\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b"}.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Domains from Exchange-Siemplify Inbox Rules

Removes specified domains from existing Exchange-Siemplify inbox rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_remove_domains_from` (List[Any], required): Specify the rule to remove the Domains from. If the rule doesn’t exist - action will do nothing.
*   `domains` (string, optional): Specify the Domains you would like to remove from the rule, in a comma separated list.
*   `remove_domains_from_all_available_rules` (bool, optional): Specify whether action should look for the provided domains in all of Siemplify inbox rules.
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Senders from Exchange-Siemplify Inbox Rules

Removes specified senders (email addresses) from existing Exchange-Siemplify inbox rules. Can optionally remove the sender's domain from corresponding domain rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_remove_senders_from` (List[Any], required): Specify the rule to remove the Senders from. If the rule doesn't exist - action will do nothing.
*   `senders` (string, optional): Specify the Senders you would like to remove from the rule, in a comma separated list. If no parameter will be provided, action will work with entities.
*   `remove_senders_from_all_available_rules` (bool, optional): Specify whether action should look for the provided Senders in all of Siemplify inbox rules.
*   `should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well` (bool, optional): Specify whether the action should automatically take the domains of the provided email addresses and remove them as well from the corresponding domain rules (same rule action for domains).
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Save Mail Attachments To The Case

Save email attachments from email stored in monitored mailbox to the Case Wall.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `message_id` (string, required): Message id to find an email to download attachments from.
*   `attachment_to_save` (string, optional): If parameter is not specified - save all email attachments to the case wall. If parameter specified - save only matching attachment to the case wall.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Download Attachments

Download email attachments from email to specific file path on Siemplify server.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `download_path` (string, required): File path on the server where to download the email attachments.
*   `message_i_ds` (string, optional): Filter condition, specify emails with which email ids to find. Should accept comma separated multiple message ids. If message id is provided, subject filter is ignored.
*   `subject_filter` (string, optional): Filter condition to search emails by specific subject.
*   `sender_filter` (string, optional): Filter condition to search emails by specific sender.
*   `only_unread` (bool, optional): If checked, download attachments only from unread emails.
*   `download_attachments_from_eml` (bool, optional): If checked, download attachments also from attached EML files.
*   `download_attachments_to_unique_path` (bool, optional): If checked, download attachments to unique path under file path provided in “Download Path“ parameter to avoid previously downloaded attachments overwrite.
*   `search_in_all_mailboxes` (bool, optional): If checked, search in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Search in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `mailboxes` (string, optional): Specify a comma-separated list of mailboxes that need to be searched. This parameter has priority over "Search in all mailboxes".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Mail HTML

Send an email with HTML template content.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subject` (string, required): The subject of the email.
*   `send_to` (string, required): Recipient email address. Multiple addresses can be separated by commas.
*   `mail_content` (EmailContent, required): Mail body.
*   `cc` (string, optional): CC email address. Multiple addresses can be separated by commas.
*   `bcc` (string, optional): BCC email address. Multiple addresses can be separated by commas.
*   `attachments_paths` (string, optional): Full path to attachments to be uploaded. Comma sepreated. e.g. C:\\Desktop\\x.txt,C:\\Desktop\\sample.txt.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete Mail

Delete one or multiple email from the mailbox that matches search criterias. Delete can be done for the first email that matched the search criteria, or it can be done for all matching emails.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, optional): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `message_i_ds` (string, optional): Filter condition, specify emails with which email ids to find. Should accept comma separated list of message ids to search for. If message id is provided, subject, sender and recipient filters are ignored.
*   `mailboxes` (string, optional): Specify a comma-separated list of mailboxes that need to be searched. This parameter has priority over “Delete in all mailboxes“.
*   `subject_filter` (string, optional): Filter condition, specify subject to search for emails.
*   `sender_filter` (string, optional): Filter condition, specify who should be the sender of needed emails.
*   `recipient_filter` (string, optional): Filter condition, specify who should be the recipient of needed emails.
*   `delete_all_matching_emails` (bool, optional): Filter condition, specify if action should delete all matched by criteria emails from the mailbox or delete only first match.
*   `delete_from_all_mailboxes` (bool, optional): If checked, delete emails in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Delete from all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `time_frame_minutes` (string, optional): Filter condition, specify in what time frame in minutes should action look for emails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Mail EML File

Fetch message EML file.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): Message ID of the email.
*   `base64_encode` (bool, required): Whether to base64 encode the EML file content.
*   `folder_name` (string, optional): Folder to fetch from. Default is Inbox. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the EML content.

### Get Account Out Of Facility Settings

Get account out of facility (OOF) settings for the provided Siemplify User entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. User entity should be the target.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the OOF settings.

### Add Senders to Exchange-Siemplify Inbox Rule

Adds specified senders (email addresses) to an Exchange-Siemplify inbox rule. Can optionally add the sender's domain to corresponding domain rules.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule_to_add_senders_to` (List[Any], required): Specify the rule to add the sender to. If the rule doesn't exist - action will create it where it's missing.
*   `senders` (string, optional): Specify the Senders you would like to add to the rule, in a comma separated list. If no parameter will be provided, action will work with User entities.
*   `should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well` (bool, optional): Specify whether the action should automatically take the domains of the provided email addresses and add them as well to the corresponding domain rules (same rule action for domains).
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, action will be performed in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Authorization

For integration configuration with Oauth authentication, run the action and browse to the received URL to get a link with access code. That link needs to be provided to the Generate Token action next to get the refresh token.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the authorization URL.

### Block Sender by Message ID

Marks an email as junk based on its Message ID, adds the sender to the "Blocked Senders List", and optionally moves the email to the Junk folder.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `move_item_to_junk_folder` (bool, required): Should the action move the specified messages to the junk folder.
*   `message_i_ds` (string, optional): Filter condition, specify emails with which message ids to find. Should accept comma separated list of message ids to mark as junk. If message id is provided, subject, sender and recipient filters are ignored.
*   `mailboxes_list_to_perform_on` (string, optional): Filter condition, If you have a specific list of mailboxes you would like to conduct the operation on, for better timing, please provide them here. Should accept a comma separated list of mail addresses, to mark the messages as junk in. If a mailboxes list is provided, "Perform Action in all Mailboxes" parameter will be ignored.
*   `folder_name` (string, optional): Parameter can be used to specify email folder on the mailbox to search for the emails. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `subject_filter` (string, optional): Filter condition, specify subject to search for emails.
*   `sender_filter` (string, optional): Filter condition, specify who should be the sender of needed emails.
*   `recipient_filter` (string, optional): Filter condition, specify who should be the recipient of needed emails.
*   `mark_all_matching_emails` (bool, optional): Filter condition, specify if action should Mark all matched by criteria emails from the mailbox or Mark only first match.
*   `perform_action_in_all_mailboxes` (bool, optional): If checked, move to junk and block sender emails in all mailboxes accessible with current impersonalization settings. If delegated access is used, implicitly specify the mailboxes to search in the "Mailboxes" parameter.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): In case "Perform action in all mailboxes" is checked, action works in batches, this parameter controls how many mailboxes action should process in single batch (single connection to mail server).
*   `time_frame_minutes` (string, optional): Filter condition, specify in what time frame in minutes should action look for emails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Wait for mail from user

Wait for user's response based on an email sent via Send Email action.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mail_message_id` (string, required): Message_id of the email, which current action would be waiting for. If message has been sent using Send Email action, please select SendEmail.JSONResult|message_id field as a placeholder.
*   `mail_date` (string, required): Send timestamp of the email, which current action would be waiting for. If message has been sent using Send Email action, please select SendEmail.JSONResult|email_date field as a placeholder.
*   `mail_recipients` (string, required): Comma-separated list of recipient emails, response from which current action would be waiting for. If message has been sent using Send Email action, please select Select SendEmail.JSONResult|to_recipients field as a placeholder.
*   `how_long_to_wait_for_recipient_reply_minutes` (string, required): How long in minutes to wait for the user's reply before marking it timed out.
*   `wait_for_all_recipients_to_reply` (bool, optional): Parameter can be used to define if there are multiple recipients - should the Action wait for responses from all of recipients until timeout, or Action should wait for first reply to proceed.
*   `wait_stage_exclude_pattern` (string, optional): Regular expression to exclude specific replies from the wait stage. Works with body part of email. Example is, to exclude automatic Out-Of-Office emails to be considered as recipient reply, and instead wait for actual user reply.
*   `folder_to_check_for_reply` (string, optional): Parameter can be used to specify mailbox email folder (mailbox that was used to send the email with question) to search for the user reply in this folder. Parameter should also accept comma separated list of folders to check the user response in multiple folders. Parameter is case sensitive. '/' separator can be used to specify a subfolder to search in, example: Inbox/Subfolder.
*   `fetch_response_attachments` (bool, optional): If selected, if recipient replies with attachment - fetch recipient response and add it as attachment for the action result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the reply content if received.

## Notes

*   Ensure the Exchange integration is properly configured in the SOAR Marketplace tab, including authentication method and necessary permissions (e.g., impersonation, EDiscovery).
*   Some actions require specific Exchange Server versions (e.g., 2013+ for blocking/unblocking senders).
*   Actions involving multiple mailboxes might require impersonation permissions and can be time-consuming; adjust script timeouts accordingly.
*   Pay attention to parameter descriptions for specific formatting requirements (e.g., comma-separated lists, folder paths with '/').
*   OAuth authentication requires a two-step process using `Get Authorization` and `Generate Token` actions.
