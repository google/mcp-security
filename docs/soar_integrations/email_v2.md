# Email V2 Integration

## Overview

This integration provides comprehensive email functionality, allowing interaction with mail servers via SMTP (for sending) and IMAP (for reading, searching, managing emails). Actions include sending emails, replying to threads, forwarding, searching, moving, deleting emails, downloading attachments, and waiting for replies.

## Configuration

To configure this integration within the SOAR platform, you typically need the following details for both sending (SMTP) and receiving/managing (IMAP):

**SMTP (Sending):**

*   **SMTP Server Address:** Hostname or IP address of the outgoing mail server.
*   **SMTP Port:** Port for the SMTP server (e.g., 587, 465, 25).
*   **SMTP Username:** Username for SMTP authentication.
*   **SMTP Password:** Password for SMTP authentication.
*   **Sender Address:** The email address to send emails from.
*   **(Optional) Use SSL/TLS:** Enable SSL/TLS encryption for SMTP.

**IMAP (Receiving/Managing):**

*   **IMAP Server Address:** Hostname or IP address of the incoming mail server.
*   **IMAP Port:** Port for the IMAP server (e.g., 993, 143).
*   **IMAP Username:** Username for IMAP authentication (can be the same as SMTP).
*   **IMAP Password:** Password for IMAP authentication (can be the same as SMTP).
*   **(Optional) Use SSL:** Enable SSL encryption for IMAP.

*(Note: The exact parameter names and required fields might vary slightly depending on the specific SOAR platform configuration interface and your email provider's requirements.)*

## Actions

### Send Thread Reply

Send a message as a reply to the email thread. Requires IMAP configuration to find the original message. Requires SMTP configuration to send the reply.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `message_id` (string, required): Specify the Message-ID of the email to reply to.
*   `folder_name` (string, required): Comma-separated list of mailbox folders to search for the original email (e.g., `INBOX`, `"[Gmail]/All Mail"`). Folder names must match exactly (use quotes if spaces exist).
*   `content` (EmailContent, required): Specify the content (body) of the reply.
*   `attachment_paths` (string, optional): Comma-separated list of file paths on the SOAR server for attachments.
*   `reply_all` (bool, optional): If enabled, reply to all recipients of the original email (overrides `reply_to`).
*   `reply_to` (string, optional): Comma-separated list of specific email addresses to reply to (used if `reply_all` is disabled or empty). Defaults to original sender if empty.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the send reply operation.

### Wait for Email from User

Wait for user's response based on an email sent via Send Email action. Requires IMAP configuration. This is an asynchronous action.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `email_message_id` (string, required): Message-ID of the email sent that you are waiting for a reply to (use placeholder from `Send Email` action result).
*   `email_date` (string, required): Send timestamp of the email sent (use placeholder from `Send Email` action result).
*   `email_recipients` (string, required): Comma-separated list of recipient emails you expect a reply from (use placeholder from `Send Email` action result).
*   `wait_stage_timeout_minutes` (string, required): How long in minutes to wait for a reply before timing out.
*   `wait_for_all_recipients_to_reply` (bool, optional): If multiple recipients, wait for all to reply (True) or just the first (False/default).
*   `wait_stage_exclude_pattern` (string, optional): Regex pattern to exclude certain replies (e.g., Out-of-Office) based on email body content.
*   `folder_to_check_for_reply` (string, optional): Comma-separated list of folders in the *sending* mailbox to check for replies. Case-sensitive.
*   `fetch_response_attachments` (bool, optional): If selected, download attachments from the reply email to the case wall.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reply email details (if received) or a timeout status.

### Forward Email

Forward email including previous messages. Requires IMAP (to find original) and SMTP (to send forward).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Comma-separated list of mailbox folders to search for the email to forward.
*   `message_id_of_email_to_forward` (string, required): Message-ID of the email to forward.
*   `recipients` (string, required): Comma-separated list of email addresses to forward the email to.
*   `subject` (string, required): The subject line for the forwarded email.
*   `cc` (string, optional): Comma-separated list of CC recipients.
*   `bcc` (string, optional): Comma-separated list of BCC recipients.
*   `content` (EmailContent, optional): The body/content to add *above* the forwarded message. Supports HTML templates.
*   `return_message_id_for_the_forwarded_email` (bool, optional): If selected, return the Message-ID of the newly sent forwarded email.
*   `attachments_paths` (string, optional): Comma-separated list of *additional* file paths on the SOAR server to attach.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the forward operation.

### Save Email Attachments To Case

Save email attachments from email stored in monitored mailbox to the Case Wall. Requires IMAP configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Comma-separated list of mailbox folders to search for the email.
*   `message_id` (string, optional): Message-ID of the email to download attachments from. If provided, other filters are ignored.
*   `attachment_to_save` (string, optional): If specified (comma-separated), save only matching attachment filenames. Otherwise, saves all attachments.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result, potentially listing saved attachments.

### Move Email To Folder

Searches for emails in the source folder(s), then moves emails matching the search criteria to the target folder. Requires IMAP configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `source_folder_name` (string, required): Comma-separated list of source mailbox folders to search in.
*   `destination_folder_name` (string, required): Destination folder to move emails to.
*   `message_i_ds` (string, optional): Comma-separated list of Message-IDs to find. If provided, other filters are ignored.
*   `subject_filter` (string, optional): Filter emails by subject line content.
*   `only_unread` (bool, optional): If enabled, only search for unread emails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the move operation.

### Ping

Test Connectivity. Requires IMAP or SMTP configuration to be set up.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action (tests connection based on configured protocols).

### Send Email

Send email message. Requires SMTP configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `recipients` (string, required): Comma-separated list of email addresses for the recipients.
*   `subject` (string, required): The email subject.
*   `content` (EmailContent, required): The email body content. Supports HTML templates.
*   `cc` (string, optional): Comma-separated list of CC recipients.
*   `bcc` (string, optional): Comma-separated list of BCC recipients.
*   `return_message_id_for_the_sent_email` (bool, optional): If selected, return the Message-ID of the sent email (useful for `Wait for Email from User`).
*   `attachments_paths` (string, optional): Comma-separated list of file paths on the SOAR server for attachments.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the send operation, potentially including the Message-ID.

### DownloadEmailAttachments

Download email attachments from email to specific file path on Siemplify server. Requires IMAP configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Comma-separated list of mailbox folders to search in.
*   `download_path` (string, required): File path on the SOAR server where attachments should be downloaded.
*   `message_i_ds` (string, optional): Comma-separated list of Message-IDs to find. If provided, subject filter is ignored.
*   `subject_filter` (string, optional): Filter emails by subject line content.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, including paths to downloaded files.

### Delete Email

Delete one or multiple email from the mailbox that matches search criteria. Delete can be done for the first email that matched the search criteria, or it can be done for all matching emails. Requires IMAP configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Comma-separated list of mailbox folders to search in.
*   `message_i_ds` (string, optional): Comma-separated list of Message-IDs to delete. If provided, other filters are ignored.
*   `subject_filter` (string, optional): Filter emails by subject line content.
*   `sender_filter` (string, optional): Filter emails by sender address.
*   `recipient_filter` (string, optional): Filter emails by recipient address.
*   `days_back` (string, optional): Filter emails within the last N days (0 means today).
*   `delete_all_matching_emails` (bool, optional): If enabled, delete all matching emails; otherwise, delete only the first match.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the delete operation.

### Search Email

Search email messages based on criteria. Requires IMAP configuration.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `folder_name` (string, required): Comma-separated list of mailbox folders to search in.
*   `time_frame_minutes` (string, required): Specify the time frame in minutes backwards to search.
*   `max_emails_to_return` (string, required): Return max X emails as an action result.
*   `subject_filter` (string, optional): Filter emails by subject line content.
*   `sender_filter` (string, optional): Filter emails by sender address.
*   `recipient_filter` (string, optional): Filter emails by recipient address.
*   `only_unread` (bool, optional): If enabled, search only for unread emails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of emails matching the search criteria.

## Notes

*   This integration requires proper configuration of either SMTP, IMAP, or both, depending on the actions used.
*   Ensure the provided credentials have the necessary permissions on the mail server.
*   Folder names must match exactly as they appear on the mail server (case-sensitivity may vary by server). Use quotes for folder names with spaces (e.g., `"[Gmail]/Sent Mail"`).
*   Message IDs are crucial for actions like replying, forwarding, and downloading attachments from specific emails. These are often obtained from previous actions like `Search Email` or `Send Email`.
*   The `Wait for Email from User` action is asynchronous and depends on polling intervals and timeouts configured in the SOAR platform.
