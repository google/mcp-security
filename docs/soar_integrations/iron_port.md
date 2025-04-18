# IronPort

## Overview

This integration provides tools to interact with the Cisco IronPort Email Security Appliance, allowing you to fetch reports and track email activity.

## Available Tools

### Get Report

**Tool Name:** `iron_port_get_report`

**Description:** Fetch specific Ironport report information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `report_type` (List[Any], required): The type of the report to fetch. Note: mail_sender_ip_hostname_detail and mail_incoming_ip_hostname_detail reports work based on Siemplify IP or Host entities; mail_users_detail works on Siemplify User entity (with email address). Other reports are working without Siemplify entities.
*   `search_reports_data_for_last_x_days` (string, required): Specify a time frame in days for which to search for reports data. By default is set to last 7 days.
*   `max_records_to_return` (string, required): Specify a time frame in days for which to search for reports data. By default is set to last 7 days.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Ping

**Tool Name:** `iron_port_ping`

**Description:** Test Connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get All Recipients By Sender

**Tool Name:** `iron_port_get_all_recipients_by_sender`

**Description:** Get a list of recipients who received emails from a given sender. Note: for action to work, please make sure that message tracking is enabled in IronPort, along with AsyncOS API.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `sender` (string, required): The sender email address to filter by.
*   `search_emails_for_last_x` (string, required): Specify a time frame for which to search for emails. Note that this value should be set accordingly to the amount of emails processed by Ironport, if big enough value will be provided action can time out.
*   `set_search_email_period_in` (List[Any], required): Specify if search emails should be done with the period of days or hours.
*   `max_recipients_to_return` (Optional[str], optional): Specify how many recipients action should return. Defaults to None.
*   `page_size` (Optional[str], optional): Specify the page size for the action to use when searching for emails. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

---

### Get All Recipients By Subject

**Tool Name:** `iron_port_get_all_recipients_by_subject`

**Description:** Get a list of all recipients that received an email with the same subject. Note: for action to work, please make sure that message tracking is enabled in IronPort, along with AsyncOS API.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `subject` (string, required): The subject to filter by.
*   `search_emails_for_last_x` (string, required): Specify a time frame for which to search for emails. Note that this value should be set accordingly to the amount of emails processed by Ironport, if big enough value will be provided action can time out.
*   `set_search_email_period_in` (List[Any], required): Specify if search emails should be done with the period of days or hours.
*   `max_recipients_to_return` (Optional[str], optional): Specify how many recipients action should return. Defaults to None.
*   `page_size` (Optional[str], optional): Specify the page size for the action to use when searching for emails. Defaults to None.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.
