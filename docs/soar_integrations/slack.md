# Slack SOAR Integration

## Overview

This integration provides tools for interacting with Slack from within the Chronicle SOAR platform. It allows sending messages (simple, advanced block kit, interactive), managing channels (create, list, rename), managing users (list, get details), uploading files, and waiting for replies or webhook interactions.

## Tools

### `slack_wait_for_reply`

Wait for a thread reply to a message previously sent with a 'Send Message' or 'Send Advanced Message' actions. Note: action is async, please adjust the timeout for action in Siemplify IDE. Action is not running on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `message_timestamp` (str, required): Specify the timestamp of the message to track. Timestamp can be found in the Send Message action json result as ts key.
*   `channel` (Optional[str], optional, default=None): Specify the channel name in which to track reply for the message. Note: if both Channel and Channel ID are specified, action will only work with ID.
*   `channel_id` (Optional[str], optional, default=None): Specify the id of the channel, in which to track reply for the message. Note: if both Channel and Channel ID are specified, action will only work with ID.
*   `wait_for_multiple_replies` (Optional[bool], optional, default=None): If enabled, action should wait for multiple responses  until action timeout. Otherwise, action finishes running after getting first reply to the message.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_create_channel`

Create a channel in Slack. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `channel_name` (str, required): Specify the name of the channel. Note: Channel names may only contain lowercase letters, numbers, hyphens, and underscores, and must be 80 characters or less.
*   `user_i_ds` (Optional[str], optional, default=None): Specify the ids of the users that should be invited to the newly created channel. Example: U014JDHLW87, U08544ABC85. Parameter accepts multiple values as a comma separated list. Note: if both “User IDs” and “User Emails” are specified, action will only work with IDs.
*   `is_private` (Optional[bool], optional, default=None): If enabled, action will create a private channel.
*   `user_emails` (Optional[str], optional, default=None): Specify the emails of users that should be invited to the newly created channel. Parameter accepts multiple values as a comma separated list. Note: if both “User IDs” and “User Emails” are specified, action will only work with IDs.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_list_channels`

Get a list of Slack channels based on the provided criteria. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_channels_to_return` (Optional[str], optional, default=None): Specify how many channels to return.
*   `type_filter` (Optional[str], optional, default=None): Specify what type of conversations to return. Example: public_channel,private_channel. Possible Values: public_channel, private_channel, mpim, im.
*   `filter_key` (Optional[List[str]], optional, default=None): Specify the key that needs to be used to filter channels.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If “Equal“ is selected, action will try to find the exact match among results and if “Contains“ is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the “Filter Key” parameter.
*   `filter_logic` (Optional[List[str]], optional, default=None): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the “Filter Key” parameter.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_get_channel_or_user_conversation_history`

Get conversation history for a user or a channel based on provided input criteria. Action works with either channel or user id, which could be searched with either 'List Channels' or 'List User' actions. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `channel_or_user_id` (str, required): Specify the channel or user id to fetch the conversation history for.
*   `time_frame` (Optional[List[str]], optional, default=None): Specify a time frame for the results. If Custom is selected, you also need to provide Start Time.
*   `start_time` (Optional[str], optional, default=None): Specify the start time for the results. This parameter is mandatory, if Custom is selected for the Time Frame parameter. 'Format: ISO 8601. Example: 2021-08-05T05:18:42Z'
*   `end_time` (Optional[str], optional, default=None): Specify the end time for the results. 'Format: ISO 8601. Example: 2021-08-05T05:18:42Z'. If nothing is provided and Custom is selected for the Time Frame parameter then this parameter will use current time.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many records to return. If nothing is provided, action will return 20 records.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_get_user_details_by_id`

Fetch Slack user account details. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `user_id` (str, required): Specify user account id to fetch details for. User ID can be found by running “List Users“ action.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_wait_for_reply_with_webhook`

Wait for a User reply to a message sent with a webhook - action periodically check the provided webhook to see if the User had provided any reply to it. Action can be used with the 'Send Advanced Message' action, if the block message with webhook was sent, to check if the user's response was provided to the webhook. Note: action is async, please adjust the timeout for action in Siemplify IDE. Action is not running on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `webhook_token_uuid` (str, required): Specify the Webhook token UUID to monitor for the user’s response.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_ping`

Test connectivity to the Slack instance with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_get_user_details`

Get Slack user details based on provided input criteria. Note: that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `search_by` (List[str], required): Specify the parameter to search user details by.
*   `user_value` (str, required): Specify the user value to search by.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_ask_question`

Ask question in Slack. Note: this action will be deprecated in the future integration's versions and replaced with actions providing enhanced functionality.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `channel` (str, required): Target channel.
*   `question` (str, required): Question content.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_send_advanced_message`

Send an advanced message to a Slack channel or user. Action provides an ability to send 'simple' text messages and 'rich' Slack block messages with buttons, advanced formatting and more. Please see https://api.slack.com/block-kit for the block messages reference. Note that action is not working on Siemplify entities. This action can be used together with the 'Wait for Reply With Webhook' action to first send a 'block' message with a webhook to a user, and when later with 'Wait for Reply With Webhook' action check for a user's response.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `recipient` (str, required): Specify the recipient to send a message to.
*   `recipient_type` (List[str], required): Specify channel or user name (full name) to send message to. Optionally channel or user id can be specified, or email address of a user.
*   `message` (str, required): Specify the message content to send.
*   `message_type` (List[str], required): Specify the message type to send.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_rename_channel`

Rename the specified Slack channel. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `new_name` (str, required): Specify what should be a new name for the channel. Note: Channel names may only contain lowercase letters, numbers, hyphens, and underscores, and must be 80 characters or less.
*   `channel_name` (Optional[str], optional, default=None): Specify the name of the channel, which you want to rename. Note: if both “Channel Name” and “Channel ID” are specified, action will only work with ID.
*   `channel_id` (Optional[str], optional, default=None): Specify the id of the channel, which you want to rename. Note: if both “Channel Name” and “Channel ID” are specified, action will only work with ID.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_upload_file`

Add files to Slack and share them with your teammates to help you collaborate. Uploaded files are stored, searchable, and shareable across your workspace. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_name` (str, required): Specify the name(title) that should be used to show in Slack for the uploaded file.
*   `file_path` (str, required): Specify the full file path on the Siemplify server for the file to upload.
*   `channel` (str, required): Specify the name of the Slack channel or the email address of the user to whom to send the message.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_send_interactive_message`

Send an interactive message to a channel or a user and when based on the provided Webhook UUID check a user's response. Action is similar to the 'Send Advanced Message' action, but it allows to send only 'block' content (not plain text messages) and also requires a webhook UUID to check a user's response to a webhook. Action is async, please adjust action timeout in IDE accordingly. Action is not working on Siemplify entities. Please configure the Slack app used in integration to allow interactive messages as described here - https://api.slack.com/legacy/interactive-messages#readying_app.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `recipient` (str, required): Specify the recipient to send a message to.
*   `recipient_type` (List[str], required): Specify channel or user name (full name) to send message to. Optionally channel or user id can be specified, or email address of a user.
*   `message` (str, required): Specify the message content to send.
*   `webhook_token_uuid` (str, required): Specify the Webhook token UUID to monitor for the user’s response.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_build_block`

Build a slack message block based on provided input criteria. Action creates a block with a webhook that can be later passed to the 'Send Interactive Message' to send a message with. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `question` (str, required): Specify the question text to add to the block.
*   `answers_buttons` (str, required): Specify the answer buttons to add to the block.
*   `siemplify_base_url` (str, required): Specify the Siemplify server base url to add to the block.
*   `webhook_token_uuid` (str, required): Specify the Webhook token UUID to monitor for the user’s response.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_send_message`

Send a message to a Slack channel or user. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `channel` (str, required): Specify the name of the Slack channel or the email address of the user to whom to send the message. Parameter accepts multiple values as a comma-separated string.
*   `message` (str, required): Specify the message content to send.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `slack_list_users`

Get a list of Slack users based on the provided criteria. Note that action is not working on Siemplify entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_records_to_return` (Optional[str], optional, default=None): Specify how many user accounts to return.
*   `filter_key` (Optional[List[str]], optional, default=None): Specify the key that needs to be used to filter user accounts.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If “Equal“ is selected, action will try to find the exact match among results and if “Contains“ is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the “Filter Key” parameter.
*   `filter_logic` (Optional[List[str]], optional, default=None): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the “Filter Key” parameter.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
