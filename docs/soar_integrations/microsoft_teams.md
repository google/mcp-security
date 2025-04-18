# Microsoft Teams Integration

## Overview

This integration allows you to interact with Microsoft Teams to manage chats, channels, teams, users, and messages via the Microsoft Graph API.

## Configuration

The configuration for this integration (Tenant ID, Client ID, Client Secret, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings. Depending on the actions used, either delegated or application permissions might be required.

## Actions

### List Chats

List available chats in Teams based on specified filters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `chat_type` (List[Any], optional): Specify what type of chat should be returned.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter chats.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied (e.g., Equals, Contains).
*   `filter_value` (string, optional): Specify what value should be used in the filter.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of chats matching the criteria.

### Create Chat

Create a user chat in Microsoft Teams. Supported entities: Username, Email Address (username that matches email regex). Note: chat will be created for each user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ID of the created chat.

### Wait For Reply

Action waits for the reply to a specified message in a channel. Note: You need to be a part of the desired team and channel. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): Specify name of the team.
*   `channel_name` (string, required): Specify name of the channel.
*   `message_id` (string, required): Specify ID of the message that is expected to have a reply.
*   `expected_reply` (string, optional): Specify text of the expected reply. If not provided, action stops on any reply.
*   `wait_method` (List[Any], optional): Specify wait method ("Check First Reply" or "Wait Till Timeout").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reply message details if received within the timeout/conditions.

### Create Channel

Create a channel in Microsoft Teams.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): Specify the name of the team in which you need to create the channel.
*   `channel_name` (string, required): Specify a unique name of the channel.
*   `channel_type` (List[Any], required): Specify the type of the channel (Standard or Private).
*   `description` (string, optional): Specify a description for the channel.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, likely including the ID of the created channel.

### List Channels

Get all channels details that exist in specific team.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): The name of the team.
*   `max_channels_to_return` (string, optional): Specify how many channels to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of channels in the specified team.

### Send User Message

Send a chat message to the user in Microsoft Teams. Supported entities: Username, Email Address. Note: Action is running as async if “Wait For Reply” is enabled.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `text` (string, required): Specify the content of the message.
*   `user_identifiers` (string, optional): Comma-separated list of user identifiers to send the message to.
*   `wait_for_reply` (bool, optional): If enabled, action will wait until replies from all entities are available.
*   `content_type` (List[Any], optional): Specify the content type for the message (e.g., text, html).
*   `user_selection` (List[Any], optional): Specify user selection method ("From Entities & User Identifiers", "From Entities", "From User Identifiers").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove Users From Channel

Remove users from the private channel in Microsoft Teams. Supported entities: Username, Email Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): Specify the name of the team.
*   `channel_name` (string, required): Specify a name of the private channel.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Message Reply

Send a reply to the channel message in Microsoft Teams.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): Specify the team name.
*   `channel_name` (string, required): Specify the channel name.
*   `message_id` (string, required): Specify the ID of the message to reply to.
*   `text` (string, required): Specify the content of the reply message.
*   `content_type` (List[Any], optional): Specify the content type for the message.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Generate Token

Get an access token using the authorization url received in the previous step (Get Authorization). Used for delegated permissions setup.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `authorization_url` (string, required): Use the authorization URL received in the Get Authorization action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the access token details.

### Add Users To Channel

Add users to the private channel in Microsoft Teams. Supported entities: Username, Email Address. Note: only users that are a part of the same team can be added.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): Specify the name of the team.
*   `channel_name` (string, required): Specify the name of the private channel.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username and Email Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test Connectivity to Microsoft Teams.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get User Details

Retrieve the properties and relationships of specific user.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `username` (string, required): The username (UPN or ID) of the user.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Username entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the user details.

### Delete Channel

Delete a channel in Microsoft Teams.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): Specify the name of the team.
*   `channel_name` (string, required): Specify a name of the channel that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Teams

Retrieve details of all teams the user/application has access to.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_teams_to_return` (string, optional): Specify how many teams to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of teams.

### Get Team Details

Retrieve the properties of specific team.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): The name of the team.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified team.

### Get Authorization

Run the action and browse to the received URL TO grant the permissions your app needs at the Azure portal. Used for delegated permissions setup.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the authorization URL.

### Send Chat Message

Send a chat message in Microsoft Teams. Note: Action is running as async if “Wait For Reply” is enabled.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `chat_id` (string, required): Specify the ID of the chat to send the message to.
*   `text` (string, required): Specify the content of the message.
*   `wait_for_reply` (bool, optional): If enabled, action will wait until reply.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Send Message

Send Message to specific Channel.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `team_name` (string, required): The name of the team.
*   `channel_name` (string, required): The name of the channel.
*   `message` (string, required): The message content.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Users

Get all users details.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_users_to_return` (string, optional): Specify how many users to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of users.

## Notes

*   Ensure the Microsoft Teams integration is properly configured in the SOAR Marketplace tab with the necessary permissions (delegated or application depending on use case) and credentials.
*   Some actions are asynchronous and may require adjusting script timeouts in the SOAR IDE.
*   Actions involving users typically support Username or Email Address entities.
*   The `Get Authorization` and `Generate Token` actions are used for setting up delegated permissions.
