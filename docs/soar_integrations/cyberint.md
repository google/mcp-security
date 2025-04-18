# Cyberint Integration

## Overview

This integration allows you to connect to the Cyberint Argos platform to update alert statuses and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cyberint details:

*   **API URL:** The base URL for the Cyberint API (e.g., `https://api.cyberint.com/`).
*   **API Key:** Your Cyberint API key for authentication.
*   **API Secret:** Your Cyberint API secret associated with the API key.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Update Alert

Update alert status in Cyberint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): Specify the ID of the alert that needs to have the status updated.
*   `status` (List[Any], optional): Specify the status for the event (e.g., `Open`, `Closed`, `In Progress`). Note: if "Closed" is selected, `closure_reason` is required.
*   `closure_reason` (List[Any], optional): Specify the closure reason if the status is set to "Closed".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the alert update operation.

### Ping

Test connectivity to the Cyberint with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the Cyberint integration is properly configured in the SOAR Marketplace tab with a valid API Key, API Secret, and API URL.
*   The API credentials require appropriate permissions within the Cyberint platform to update alerts.
