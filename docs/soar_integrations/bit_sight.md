# BitSight Integration

## Overview

This integration allows you to connect to BitSight Security Ratings platform to retrieve company details, security highlights, and vulnerability information.

## Configuration

To configure this integration within the SOAR platform, you typically need the following BitSight details:

*   **API Token:** Your BitSight API token for authentication. You can usually generate this within your BitSight account settings.
*   **(Optional) API URL:** The base URL for the BitSight API, if different from the default (`https://api.bitsighttech.com`).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### List Company Highlights

List highlights (significant security events or rating changes) related to the specified company in BitSight within a given time frame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `company_name` (string, required): Specify the name of the company for which you want to return highlights.
*   `time_frame` (List[Any], optional): Specify a time frame for the results (e.g., Last 7 Days, Last 30 Days, Custom). If "Custom" is selected, `start_time` is required.
*   `start_time` (string, optional): Specify the start time for the results (Format: ISO 8601). Mandatory if `time_frame` is "Custom".
*   `end_time` (string, optional): Specify the end time for the results (Format: ISO 8601). Uses current time if `time_frame` is "Custom" and this is empty.
*   `max_highlights_to_return` (string, optional): Specify the number of highlights you want to return. Default: 20.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of company highlights matching the criteria.

### Get Company Details

Get information about a company in BitSight, including their security rating and other profile details.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `company_name` (string, required): Specify the name of the company for which you want to return details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified company.

### Ping

Test connectivity to the BitSight with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### List Company Vulnerabilities

List vulnerabilities related to the specified company in BitSight.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `company_name` (string, required): Specify the name of the company for which you want to return vulnerabilities.
*   `only_high_confidence` (bool, optional): If enabled, action will only return vulnerabilities with high confidence.
*   `max_vulnerabilities_to_return` (string, optional): Specify how many vulnerabilities you want to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of vulnerabilities for the specified company.

## Notes

*   Ensure the BitSight integration is properly configured in the SOAR Marketplace tab with a valid API Token.
*   Time frame parameters accept ISO 8601 format for custom ranges.
