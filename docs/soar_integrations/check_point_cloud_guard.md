# Check Point CloudGuard Integration

## Overview

This integration allows you to connect to Check Point CloudGuard Dome9 platform. Currently, it primarily provides a connectivity test action.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Check Point CloudGuard details:

*   **API Key:** Your CloudGuard API Key ID.
*   **API Secret:** Your CloudGuard API Secret Key.
*   **Server URL:** The base URL for the CloudGuard API (e.g., `https://api.dome9.com/v2/`).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Ping

Test connectivity to the Check Point Cloud Guard with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action, indicating success or failure of the connection test.

## Notes

*   Ensure the Check Point CloudGuard integration is properly configured in the SOAR Marketplace tab with a valid API Key, Secret, and Server URL.
*   This integration currently focuses on connectivity testing. Future updates might include actions for managing CloudGuard entities or policies.
