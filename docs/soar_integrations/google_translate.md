# Google Translate

## Overview

This integration provides tools to interact with the Google Translate API for listing supported languages and translating text.

## Available Tools

### List Languages

**Tool Name:** `google_translate_list_languages`

**Description:** List available languages in Google Translate.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key that needs to be used to filter languages. Defaults to None.
*   `filter_logic` (List[Any], optional): Specify what filter logic should be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `filter_value` (string, optional): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among results and if "Contains" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the "Filter Key" parameter. Defaults to None.
*   `max_records_to_return` (string, optional): Specify how many records to return. If nothing is provided, action will return 50 records. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `google_translate_ping`

**Description:** Test connectivity to the Google Translate with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Translate Text

**Tool Name:** `google_translate_translate_text`

**Description:** Translate text using Google Translate.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_language` (string, required): Specify the desired language.
*   `text` (string, required): Specify the text that needs to be translated.
*   `source_language` (string, optional): Specify the source language of the text. If nothing is provided, action will detect the language automatically. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
