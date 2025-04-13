# IntSights

## Overview

This integration provides tools to interact with the IntSights Threat Intelligence platform for managing alerts, searching IOCs, and retrieving alert-related information.

## Available Tools

### Ask An Analyst

**Tool Name:** `intsights_ask_an_analyst`

**Description:** Ask an analyst regarding the alert in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert where you want to ask the analyst.
*   `comment` (string, required): Specify the comment for the analyst.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Search IOCs

**Tool Name:** `intsights_search_io_cs`

**Description:** Search IOCs.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Typically runs on IOC entities like IP Address, URL, Filehash, Domain. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the search results for the provided IOCs.

---

### Close Alert

**Tool Name:** `intsights_close_alert`

**Description:** Close alert in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert which you want to close.
*   `reason` (List[Any], required): Specify the reason why the alert needs to be closed.
*   `additional_info` (string, optional): Specify additional information explaining why the alert should be closed. Defaults to None.
*   `rate` (string, optional): Specify the rating of the alert. Maximum is 5. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Assign Alert

**Tool Name:** `intsights_assign_alert`

**Description:** Assign alert to an analyst in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert on which you want to change the assignment.
*   `assignee_id` (string, optional): Specify the ID of the analyst that should be assigned to the alert. Note: If both Assignee ID and Assignee Email Address are specified, action will prioritize Assignee ID. Defaults to None.
*   `assignee_email_address` (string, optional): Specify the email address of the analyst that should be assigned to the alert. Note: If both Assignee ID and Assignee Email Address are specified, action will prioritize Assignee ID. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `intsights_ping`

**Description:** Check connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Download Alert CSV

**Tool Name:** `intsights_download_alert_csv`

**Description:** Download CSV file containing information related to alert in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert for which you want to download CSV.
*   `download_folder_path` (string, required): Specify the path to the folder, where you want to store the CSV file.
*   `overwrite` (boolean, optional): If enabled, action will overwrite the file with the same name. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the path to the downloaded file.

---

### Reopen Alert

**Tool Name:** `intsights_reopen_alert`

**Description:** Reopen alert in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert which you want to reopen.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get Alert Image

**Tool Name:** `intsights_get_alert_image`

**Description:** Retrieve information about alert images in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_image_i_ds` (string, required): Specify the comma-separated list of alert image IDs. Example: id1,id2.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including image data or links.

---

### Add Note

**Tool Name:** `intsights_add_note`

**Description:** Add a note to the alert in IntSights.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert to which you want to add a note.
*   `note` (string, required): Specify the note for the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
