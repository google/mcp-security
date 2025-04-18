# Google Chat

## Overview

This integration provides tools to interact with Google Chat for sending messages and listing spaces.

## Available Tools

### Ping

**Tool Name:** `google_chat_ping`

**Description:** Test connectivity to the Google Chat service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Send Advanced Message

**Tool Name:** `google_chat_send_advanced_message`

**Description:** Send an advanced message to a Google Chat space based on provided message JSON payload. Note that action is not working on Siemplify entities. See [Google Chat Card messages](https://developers.google.com/chat/api/guides/message-formats/cards) for examples of message payloads.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `space_name` (string, required): Specify a space name to send message to. Example space name: AAAAdaTsel0.
*   `message_json_payload` (Union[str, dict], required): Specify a JSON payload to send with message.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### List Spaces

**Tool Name:** `google_chat_list_spaces`

**Description:** List spaces that currently configured Google Chat bot was added to. Note: Action is not running on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter Google Chat spaces. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `include_user_memberships` (boolean, optional): If enabled, user memberships information will be added to the action Case Wall table and JSON result. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Send Message

**Tool Name:** `google_chat_send_message`

**Description:** Send a message to a Google Chat space that the Siemplify app was added to. Note that action is not working on Siemplify entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `space_name` (string, required): Specify a space name to send message to. Example space name: AAAAdaTsel0.
*   `message_text` (string, required): Specify a message text to send.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
