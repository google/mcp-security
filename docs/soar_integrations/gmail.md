# Gmail

## Overview

This integration provides tools to interact with Gmail for sending emails, managing labels, searching messages, and handling email threads.

## Available Tools

### Send Thread Reply

**Tool Name:** `gmail_send_thread_reply`

**Description:** Use the Send Thread Reply action to send a message as a reply to the email thread. This action doesn’t run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `internet_message_id` (string, required): An internet message ID of the email to search for.
*   `mail_content` (EmailContent, required): The body of an email.
*   `reply_to` (string, optional): A comma-separated list of emails to send the reply to. If you don’t provide any value and the Reply All checkbox is clear, the action only sends a reply to the original email sender. If you select the Reply All parameter, the action ignores this parameter. Defaults to None.
*   `reply_all` (boolean, optional): If selected, the action sends a reply to all recipients related to the original email. Not selected by default. This parameter has a priority over the Reply To parameter. Defaults to None.
*   `attachments_paths` (string, optional): A comma-separated string of paths for file attachments stored on the Google SecOps server. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Add Email Label

**Tool Name:** `gmail_add_email_label`

**Description:** Use the Add Email Label action to add a label to the specified email. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `label` (string, required): A label to update the email with. This parameter accepts multiple values as a comma-separated list. Action will create labels, if they don’t exist in the mailbox.
*   `labels_filter` (string, optional): A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don’t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3. Defaults to None.
*   `internet_message_id` (string, optional): An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Labels Filter, Subject Filter, Sender Filter, and Time Frame (minutes) parameters. Defaults to None.
*   `subject_filter` (string, optional): A filter condition that specifies the email subject to search for. This filter uses the “contains” logic and requires you to specify search items in full words. This filter doesn’t support partial matches. Defaults to None.
*   `sender_filter` (string, optional): A filter condition that specifies the email sender to search for. This filter uses the “equals” logic. Defaults to None.
*   `time_frame_minutes` (string, optional): A filter condition that specifies the timeframe in minutes to search for emails. Defaults to None.
*   `email_status` (List[Any], optional): A status of the email to search for. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Forward Email

**Tool Name:** `gmail_forward_email`

**Description:** Use the Forward Email action to forward emails, including emails with previous threads. This action doesn’t run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `internet_message_id` (string, required): An internet message ID of the email to search for.
*   `send_to` (string, required): A comma-separated list of email addresses for the email recipients, such as user1@example.com, user2@example.com.
*   `subject` (string, required): A new subject for the email to forward.
*   `mail_content` (EmailContent, required): The body of an email.
*   `cc` (string, optional): A comma-separated string of email addresses for the carbon copy (CC) email recipients, such as user1@example.com, user2@example.com. Defaults to None.
*   `bcc` (string, optional): A comma-separated string of email addresses for the blind carbon copy (BCC) email recipients, such as user1@example.com, user2@example.com. Defaults to None.
*   `attachments_paths` (string, optional): A comma-separated string of paths for file attachments stored on the Google SecOps server. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Search For Emails

**Tool Name:** `gmail_search_for_emails`

**Description:** Use the Search for Emails action to execute email search in a specified mailbox using the provided search criteria. With appropriate permissions, this action can run a search in other mailboxes. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration. This parameter accepts multiple values as a comma-separated string.
*   `labels_filter` (string, optional): A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don’t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3. Defaults to None.
*   `internet_message_id` (string, optional): An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Subject Filter, Sender Filter, Labels Filter, Recipient Filter, Time Frame (minutes), and Email Status parameters. Defaults to None.
*   `subject_filter` (string, optional): A filter condition that specifies the email subject to search for. Defaults to None.
*   `sender_filter` (string, optional): A filter condition that specifies the email sender to search for. Defaults to None.
*   `recipient_filter` (string, optional): A filter condition that specifies the email recipient to search for. Defaults to None.
*   `time_frame_minutes` (string, optional): A filter condition that specifies the timeframe in minutes to search for emails. Defaults to None.
*   `email_status` (List[Any], optional): A status of the email to search for. Defaults to None.
*   `headers_to_return` (string, optional): A comma-separated list of headers to return in the action output. The action always returns the following headers: date, from, to, cc, bcc, in-reply-to, reply-to, message-id and subject headers. If you don’t provide any value, the action returns all headers.This parameter is case sensitive. Defaults to None.
*   `return_email_body` (boolean, optional): If selected, the action returns the full body content of an email in the action output. If not selected, the information about the attachment names in the email is unavailable. Defaults to None.
*   `max_emails_to_return` (string, optional): The maximum number of emails for the action to return. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Wait For Thread Reply

**Tool Name:** `gmail_wait_for_thread_reply`

**Description:** Use the Wait For Thread Reply action to wait for the user's reply based on an email sent using the Send Email action. This action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to wait for a reply in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `internet_message_id` (string, required): The internet message ID of an email for the action to wait for. If the message was sent using the Send Email action, configure this parameter using the following placeholder: SendEmail.JSONResult|message_id. To retrieve an internet message ID, use the Search for Emails action.
*   `wait_for_all_recipients_to_reply` (boolean, optional): If selected, the action waits for responses from all recipients until reaching timeout. Not selected by default. Defaults to None.
*   `fetch_response_attachments` (boolean, optional): If selected and the recipient reply contains attachments, the action retrieves email attachments and adds them as an attachment to the Case Wall in Google SecOps. Not selected by default. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Remove Email Label

**Tool Name:** `gmail_remove_email_label`

**Description:** Use the Remove Email Label action to remove a label from the specified email. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn't run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `label` (string, required): A label to remove from an email. This parameter accepts multiple values as a comma-separated list.
*   `labels_filter` (string, optional): A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don’t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3. Defaults to None.
*   `internet_message_id` (string, optional): An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Labels Filter, Subject Filter, Sender Filter, and Time Frame (minutes) parameters. Defaults to None.
*   `subject_filter` (string, optional): A filter condition that specifies the email subject to search for. This filter uses the “contains” logic and requires you to specify search items in full words. This filter doesn’t support partial matches. Defaults to None.
*   `sender_filter` (string, optional): A filter condition that specifies the email sender to search for. This filter uses the “equals” logic. Defaults to None.
*   `time_frame_minutes` (string, optional): A filter condition that specifies the timeframe in minutes to search for emails. Defaults to None.
*   `email_status` (List[Any], optional): A status of the email to search for. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `gmail_ping`

**Description:** Use the Ping action to test connectivity to Gmail.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Save Email To The Case

**Tool Name:** `gmail_save_email_to_the_case`

**Description:** Use the Save Email To The Case action to save email or email attachments to the action Case Wall in Google SecOps. This action doesn’t run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `internet_message_id` (string, required): An internet message ID of the email to search for.
*   `save_only_email_attachments` (boolean, optional): If selected, the action saves only attachments from the specified email. Not selected by default. Defaults to None.
*   `attachment_to_save` (string, optional): If you selected the “Save Only Email Attachments” parameter, the action only saves attachments that this parameter specifies. This parameter accepts multiple values as a comma-separated string. Defaults to None.
*   `base64_encode` (boolean, optional): If selected, the action encodes the email file into a base64 format. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Send Email

**Tool Name:** `gmail_send_email`

**Description:** Use the Send Email action to send an email based on the provided parameters. This action is not running on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to send an email from, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration.
*   `subject` (string, required): The subject for an email to send.
*   `send_to` (string, required): A comma-separated string of email addresses for the email recipients, such as user1@example.com, user2@example.com.
*   `mail_content` (EmailContent, required): The body of an email.
*   `cc` (string, optional): A comma-separated string of email addresses for the carbon copy (CC) email recipients, such as user1@example.com, user2@example.com. Defaults to None.
*   `bcc` (string, optional): A comma-separated string of email addresses for the blind carbon copy (BCC) email recipients, such as user1@example.com, user2@example.com. Defaults to None.
*   `attachments_paths` (string, optional): A comma-separated string of paths for file attachments stored on the Google SecOps server. Defaults to None.
*   `reply_to_recipients` (string, optional): A comma-separated list of recipients to use in the “Reply-To” header. Use the “Reply-To” header to redirect reply emails to the specific email address instead of the sender address that is stated in the “From” field. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Delete Email

**Tool Name:** `gmail_delete_email`

**Description:** Use the Delete Email action to delete one or multiple emails from the mailbox based on the provided search criteria. By default, this action moves emails to Trash. You can configure the action to delete emails forever instead of moving them to Trash. The Delete Email action is asynchronous. Adjust the action timeout in the Google SecOps IDE accordingly. This action doesn’t run on Google SecOps entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `mailbox` (string, required): A mailbox to search the email in, such as user@example.com. By default, the action uses the default mailbox that you configured for the integration. This parameter accepts multiple values as a comma-separated string.
*   `labels_filter` (string, optional): A filter condition that specifies the email labels to search for. This parameter accepts multiple values as a comma-separated string. You can search for emails with specific labels, such as label1, label2. To search for emails that don’t possess the specific label, use the following format: -label1. You can configure this parameter to search for emails with and without specific labels in one string, such as label1, -label2, label3. Defaults to None.
*   `internet_message_id` (string, optional): An internet message ID of the email to search for. This parameter accepts multiple values as a comma-separated string. If you provide the internet message ID, the action ignores the Subject Filter, Sender Filter, Labels Filter, and Time Frame (minutes) parameters. Defaults to None.
*   `subject_filter` (string, optional): A filter condition that specifies the email subject to search for. This filter uses the “contains” logic and requires you to specify search items in full words. This filter doesn’t support partial matches. Defaults to None.
*   `sender_filter` (string, optional): A filter condition that specifies the email sender to search for. This filter uses the “equals” logic. Defaults to None.
*   `time_frame_minutes` (string, optional): A filter condition that specifies the timeframe in minutes to search for emails. Defaults to None.
*   `email_status` (List[Any], optional): A status of the email to search for. Defaults to None.
*   `move_to_trash` (boolean, optional): If selected, the action moves emails to Trash and doesn’t search through emails with the Trash label unless you configure the Labels Filter parameter to include the following label: Trash. If not selected, the action executes search across the whole mailbox and deletes emails forever. Selected by default. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
