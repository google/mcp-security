# Microsoft Graph Mail Delegated Integration

## Overview

This integration allows you to interact with Microsoft 365 mailboxes using delegated permissions via the Microsoft Graph API. It enables actions such as sending emails (including vote emails and HTML emails), managing emails (moving, deleting, marking as junk/not junk), searching emails, downloading attachments, managing tokens, and retrieving mailbox settings.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, Refresh Token, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings, specifically requiring delegated permissions.

## Actions

### Send Vote Email

Use the Send Vote Email action to send emails with the predefined answering options (Yes/No or Approve/Reject). This action uses Google SecOps HTML templates to format the email. With appropriate permissions, the action can send emails from a mailbox other than the default one. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `send_from` (string, required): An optional email address from which to send an email if permissions allow it. By default, the email is sent from the default mailbox that is specified in the integration configuration.
*   `subject` (string, required): The email subject.
*   `send_to` (string, required): A comma-separated list of email addresses for the email recipients.
*   `email_html_template` (EmailContent, required): The type of the HTML template to use. The default value is Email HTML Template.
*   `structure_of_voting_options` (List[Any], required): The structure of the vote to send to recipients (Yes/No or Approve/Reject). Default: Yes/No.
*   `attachment_location` (List[Any], required): Location where attachments are stored (GCP Bucket or Local File System). Default: GCP Bucket.
*   `cc` (string, optional): A comma-separated list of email addresses for the email CC field.
*   `bcc` (string, optional): A comma-separated list of email addresses for the email BCC field.
*   `attachments_paths` (string, optional): A comma-separated list of paths for file attachments stored on the server.
*   `reply_to_recipients` (string, optional): A comma-separated list of recipients to use in the Reply-To header.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Mark Email as Not Junk

Use the Mark Email as Not Junk action to mark emails as not junk in a specific mailbox. This action removes the sender from the list of blocked senders and moves the message to the Inbox folder. Uses the beta version of Microsoft Graph API. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_mailbox` (string, required): A mailbox to search for an email in. Accepts multiple values as a comma-separated string.
*   `folder_name` (string, required): A mailbox folder in which to search for an email (e.g., Inbox/Subfolder).
*   `mail_i_ds` (string, required): A comma-separated string of the mail IDs or internetMessageId values of the emails to mark as not junk.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Thread Reply

Use the Send Thread Reply action to send a message as a reply to the email thread. With appropriate permissions, the action can send emails from a mailbox other than the one specified in the integration configuration. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `send_from` (string, required): An optional email address from which to send emails if permissions allow it.
*   `mail_id` (string, required): The email ID or the internetMessageId value of the email to reply to.
*   `folder_name` (string, required): A mailbox folder in which to search for an email (e.g., Inbox/Subfolder).
*   `mail_content` (string, required): The email body.
*   `attachment_location` (List[Any], required): Location where attachments are stored (GCP Bucket or Local File System). Default: GCP Bucket.
*   `attachments_paths` (string, optional): A comma-separated list of paths for file attachments stored on the server.
*   `reply_all` (bool, optional): If selected, sends a reply to all recipients related to the original email. Has priority over `reply_to`.
*   `reply_to` (string, optional): A comma-separated list of emails to reply to. Ignored if `reply_all` is true.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Wait For Email From User

Use the Wait For Email From User action to wait for the user's response based on an email sent using the Send Email action. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mail_id` (string, required): The ID of the email. If sent via Send Mail, use {SendEmail.JSONResult|id} or {SendEmail.JSONResult|internetMessageId}.
*   `wait_for_all_recipients_to_reply` (bool, optional): If selected, waits for responses from all recipients until timeout.
*   `wait_stage_exclude_pattern` (string, optional): Regex to exclude specific replies (e.g., OOF messages). Works on the email body.
*   `folder_to_check_for_reply` (string, optional): Mailbox folder(s) to search for the reply (comma-separated). Default: Inbox.
*   `fetch_response_attachments` (bool, optional): If selected, fetches attachments from the reply.
*   `limit_the_amount_of_information_returned_in_the_json_result` (bool, optional): If enabled, limits JSON result to key email fields.
*   `disable_the_action_json_result` (bool, optional): If enabled, action will not return JSON result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result, including the reply details if received.

### Forward Email

Use the Forward Email action to forward emails that include previous threads. With appropriate permissions, this action can send emails from a mailbox different than the one specified in the integration configuration. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `send_from` (string, required): An optional email address from which to send an email if permissions allow it.
*   `mail_id` (string, required): The email ID or the internetMessageId value of the email to forward.
*   `subject` (string, required): The new email subject.
*   `send_to` (string, required): A comma-separated list of email addresses for the email recipients.
*   `mail_content` (string, required): The email body.
*   `attachment_location` (List[Any], required): Location where attachments are stored (GCP Bucket or Local File System). Default: GCP Bucket.
*   `folder_name` (string, optional): A mailbox folder in which to search for an email (e.g., Inbox/Subfolder).
*   `cc` (string, optional): A comma-separated list of email addresses for the email CC field.
*   `bcc` (string, optional): A comma-separated list of email addresses for the email BCC field.
*   `attachments_paths` (string, optional): A comma-separated list of paths for file attachments stored on the server.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Generate Token

Use the Generate Token action to obtain a refresh token for the integration configuration with delegated authentication. Use the authorization URL that you received in the Get Authorization action. This action doesn't run on Google SecOps entities. After generating the refresh token, configure the Refresh Token Renewal Job to keep it valid.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `authorization_url` (string, required): An authorization URL received from the Get Authorization action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the refresh token and other relevant details.

### Move Email To Folder

Use the Move Email To Folder action to move one or multiple emails from the source email folder to the other folder in the mailbox. With appropriate permissions, this action can move emails to other mailboxes. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `move_in_mailbox` (string, required): The default mailbox to execute the move operation in. Accepts multiple values comma-separated.
*   `source_folder_name` (string, required): A source folder from which to move the email (e.g., Inbox/Subfolder).
*   `destination_folder_name` (string, required): A destination folder to move the email to (e.g., Inbox/folder_name/subfolder_name). Case-insensitive.
*   `mail_i_ds` (string, optional): Filter by specific email IDs (comma-separated). If provided, ignores Subject and Sender filters.
*   `subject_filter` (string, optional): Filter by email subject (contains logic).
*   `sender_filter` (string, optional): Filter by email sender (equals logic).
*   `time_frame_minutes` (string, optional): Filter by time period in minutes.
*   `only_unread` (bool, optional): If selected, searches only for unread emails.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): Number of mailboxes per batch. Default: 25.
*   `limit_the_amount_of_information_returned_in_the_json_result` (bool, optional): If enabled, limits JSON result to key email fields.
*   `disable_the_action_json_result` (bool, optional): If enabled, action will not return JSON result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the move operation.

### Wait For Vote Email Results

Use the Wait For Vote Email Results action to wait for the user response based on the vote email sent using the Send Vote Email action. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `vote_mail_sent_from` (string, required): The mailbox from which the vote email was sent.
*   `mail_id` (string, required): The ID of the email. Use {SendVoteEmail.JSONResult|id} or {SendEmail.JSONResult|internetMessageId}.
*   `wait_for_all_recipients_to_reply` (bool, optional): If selected, waits for responses from all recipients. Default: Selected.
*   `wait_stage_exclude_pattern` (string, optional): Regex to exclude specific replies (e.g., OOF messages). Works on the email body.
*   `folder_to_check_for_reply` (string, optional): Mailbox folder(s) to search for the reply (comma-separated). Default: Inbox.
*   `folder_to_check_for_sent_mail` (string, optional): Mailbox folder(s) to search for the sent mail (comma-separated). Default: Sent Items.
*   `fetch_response_attachments` (bool, optional): If selected, fetches attachments from the reply.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the voting results.

### Send Email HTML

Use the Send Email HTML action to send emails using the Google SecOps HTML template from a specific mailbox to an arbitrary list of recipients. With appropriate permissions, the action can send emails from a mailbox other than the default one. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `send_from` (string, required): An optional email address from which to send an email if permissions allow it.
*   `subject` (string, required): The email subject.
*   `send_to` (string, required): A comma-separated list of email addresses for the email recipients.
*   `email_html_template` (EmailContent, required): The type of the HTML template to use. Default: Email HTML Template.
*   `attachment_location` (List[Any], required): Location where attachments are stored (GCP Bucket or Local File System). Default: GCP Bucket.
*   `cc` (string, optional): A comma-separated list of email addresses for the email CC field.
*   `bcc` (string, optional): A comma-separated list of email addresses for the email BCC field.
*   `attachments_paths` (string, optional): A comma-separated list of paths for file attachments stored on the server.
*   `reply_to_recipients` (string, optional): A comma-separated list of recipients to use in the Reply-To header.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Use the Ping action to test connectivity to the Microsoft Graph mail service. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Search Emails

Use the Search Emails action to execute email search in the default mailbox based on the provided search criteria. With appropriate permissions, this action can run a search in other mailboxes. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_mailbox` (string, required): The default mailbox to search in. Accepts multiple values comma-separated.
*   `folder_name` (string, required): A mailbox folder to search in (e.g., Inbox/Subfolder).
*   `subject_filter` (string, optional): Filter by email subject (contains logic).
*   `sender_filter` (string, optional): Filter by email sender (equals logic).
*   `time_frame_minutes` (string, optional): Filter by time period in minutes.
*   `max_emails_to_return` (string, optional): Number of emails to return. Default: 10.
*   `only_unread` (bool, optional): If selected, searches only for unread emails.
*   `select_all_fields_for_return` (bool, optional): If selected, returns all available fields for the email.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): Number of mailboxes per batch. Default: 25.
*   `limit_the_amount_of_information_returned_in_the_json_result` (bool, optional): If enabled, limits JSON result to key email fields.
*   `disable_the_action_json_result` (bool, optional): If enabled, action will not return JSON result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

### Save Email to the Case

Use the Save Email To The Case action to save emails or email attachments to the Google SecOps Case Wall. With appropriate permissions, this action can save emails from mailboxes other than the one provided in the integration configuration. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_mailbox` (string, required): The default mailbox to search in.
*   `mail_id` (string, required): The email ID or internetMessageId value to search for (comma-separated). Use {SendEmail.JSONResult|id} or {SendEmail.JSONResult|internetMessageId} if applicable.
*   `folder_name` (string, optional): A mailbox folder to search in (e.g., Inbox/Subfolder).
*   `save_only_email_attachments` (bool, optional): If selected, saves only attachments.
*   `attachment_to_save` (string, optional): If `save_only_email_attachments` is selected, specifies which attachments to save (comma-separated).
*   `base64_encode` (bool, optional): If selected, encodes the email file into base64 format.
*   `save_email_to_the_case_wall` (bool, optional): If selected, saves the specified email to the Case Wall.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the save operation.

### Send Email

Use the Send Email action to send emails from a specific mailbox to an arbitrary list of recipients. This action can send either plain text or HTML-formatted emails. With appropriate permissions, the action can send emails from a mailbox different than the one specified in the integration configuration. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `send_from` (string, required): An optional email address from which to send emails if permissions allow it.
*   `subject` (string, required): The email subject.
*   `send_to` (string, required): A comma-separated list of email addresses for the email recipients.
*   `mail_content` (string, required): The email body.
*   `attachment_location` (List[Any], required): Location where attachments are stored (GCP Bucket or Local File System). Default: GCP Bucket.
*   `cc` (string, optional): A comma-separated list of email addresses for the email CC field.
*   `bcc` (string, optional): A comma-separated list of email addresses for the email BCC field.
*   `attachments_paths` (string, optional): A comma-separated list of paths for file attachments stored on the server.
*   `mail_content_type` (List[Any], optional): Type of email content (Text or HTML). Default: Text.
*   `reply_to_recipients` (string, optional): A comma-separated list of recipients to use in the Reply-To header.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Mailbox Account Out Of Facility Settings

Use the Get Mailbox Account Out Of Facility Settings action to retrieve the mailbox account out of facility (OOF) settings for the Google SecOps User entity provided. Uses the beta version of Microsoft Graph API. This action runs on the Google SecOps User entity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports User entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the OOF settings for the specified user(s).

### Download Attachments from Email

Use the Download Attachments From Email action to download attachments from emails based on the criteria provided. This action doesn't run on Google SecOps entities. This action is asynchronous. Adjust the script timeout value in the Google SecOps IDE. Replaces "/" and "\" in attachment names with "_".

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_mailbox` (string, required): The default mailbox to search in. Accepts multiple values comma-separated.
*   `download_destination` (List[Any], required): Location to save attachments (GCP Bucket or Local File System). Default: GCP Bucket.
*   `download_path` (string, required): Path to download attachments to (Unix-like format, e.g., /tmp/test).
*   `folder_name` (string, optional): A mailbox folder to search in (e.g., Inbox/Subfolder).
*   `mail_i_ds` (string, optional): Filter by specific email IDs or internetMessageId values (comma-separated). If provided, ignores Subject and Sender filters.
*   `subject_filter` (string, optional): Filter by email subject (contains logic).
*   `sender_filter` (string, optional): Filter by email sender (equals logic).
*   `download_attachments_from_eml` (bool, optional): If selected, downloads attachments from EML files.
*   `download_attachments_to_unique_path` (bool, optional): If selected, downloads attachments to the unique path provided to avoid overwriting.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): Number of mailboxes per batch. Default: 25.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including paths to downloaded files.

### Delete Email

Use the Delete Email action to delete one or more emails from a mailbox based on search criteria. With appropriate permissions, this action can move emails into different mailboxes. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `delete_in_mailbox` (string, required): The default mailbox to delete from. Accepts multiple values comma-separated.
*   `folder_name` (string, required): A mailbox folder to search in (e.g., Inbox/Subfolder).
*   `mail_i_ds` (string, optional): Filter by specific email IDs (comma-separated). If provided, ignores Subject and Sender filters.
*   `subject_filter` (string, optional): Filter by email subject (contains logic).
*   `sender_filter` (string, optional): Filter by email sender (equals logic).
*   `time_frame_minutes` (string, optional): Filter by time period in minutes.
*   `only_unread` (bool, optional): If selected, searches only for unread emails.
*   `how_many_mailboxes_to_process_in_a_single_batch` (string, optional): Number of mailboxes per batch. Default: 25.
*   `limit_the_amount_of_information_returned_in_the_json_result` (bool, optional): If enabled, limits JSON result to key email fields.
*   `disable_the_action_json_result` (bool, optional): If enabled, action will not return JSON result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the delete operation.

### Mark Email as Junk

Use the Mark Email as Junk action to mark emails as junk in a specified mailbox. This action adds the email sender to the list of blocked senders and moves the message to the Junk Email folder. Uses the beta version of Microsoft Graph API. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_mailbox` (string, required): A mailbox to search for an email in. Accepts multiple values comma-separated.
*   `folder_name` (string, required): A mailbox folder in which to search for an email (e.g., Inbox/Subfolder).
*   `mail_i_ds` (string, required): A comma-separated string of the mail IDs or internetMessageId values of the emails to mark as junk.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Extract Data from Attached EML

Use the Extract Data From Attached EML action to retrieve data from the email EML attachments and return it in the action results. Supports .eml, .msg, and .ics file formats. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `search_in_mailbox` (string, required): The default mailbox to search in. Accepts multiple values comma-separated.
*   `mail_i_ds` (string, required): Filter by specific email IDs or internetMessageId values (comma-separated).
*   `folder_name` (string, optional): A mailbox folder to search in (e.g., Inbox/Subfolder).
*   `regex_map_json` (Union[str, dict], optional): JSON definition with regex to apply to attached email file and generate additional keys in the result (e.g., `{"ips": "\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b"}`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the extracted data from the EML attachments.

### Get Authorization

Use the Get Authorization action to obtain a link with the access code for the integration configuration with delegated authentication. Copy the whole link and use it in the Generate Token action to get the refresh token. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the authorization URL.

### Run Microsoft Search Query

Use the Run Microsoft Search Query action to perform a search using Microsoft Search engine based on a constructed basic or advanced query. See Microsoft Graph documentation for search concepts. This action doesn’t run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `entity_types_to_search` (string, optional): Comma-separated list of expected resource types (e.g., event, message, driveItem).
*   `fields_to_return` (string, optional): Fields to return in the response. If empty, returns all available fields.
*   `search_query` (string, optional): The query to run the search. See Microsoft Search API documentation for examples.
*   `max_rows_to_return` (string, optional): Maximum number of rows to return. Default: 25.
*   `advanced_query` (string, optional): Full search payload (JSON string) to use instead of other parameters. If provided, ignores other query parameters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results.

## Notes

*   Ensure the Microsoft Graph Mail Delegated integration is properly configured in the SOAR Marketplace tab with delegated permissions and necessary credentials (including refresh token management).
*   Many actions are asynchronous and may require adjusting script timeouts in the SOAR IDE.
*   Pay attention to required ID formats (mail ID vs. internetMessageId) and time formats.
*   Some actions use beta Microsoft Graph APIs.
