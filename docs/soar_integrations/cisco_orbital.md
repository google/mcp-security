# Cisco Orbital Integration

## Overview

This integration allows you to connect to Cisco Orbital to execute Osquery queries on endpoints and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cisco Orbital / SecureX details:

*   **API URL:** The regional API endpoint for Cisco Orbital (e.g., `orbital.amp.cisco.com`, `orbital.apjc.amp.cisco.com`, `orbital.eu.amp.cisco.com`).
*   **Client ID:** Your SecureX API Client ID.
*   **Client Password:** Your SecureX API Client Password.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API credentials have the necessary permissions for Orbital query execution.)*

## Actions

### Execute Query

Execute queries on endpoints based on IP and Hostname entities in Cisco Orbital. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. Maximum timeout is 24 hours.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `query` (string, required): Specify the Osquery query that needs to be executed.
*   `name` (string, optional): Specify the name for the query job. If empty, defaults to `Siemplify-{guid}`.
*   `custom_context_fields` (string, optional): Specify additional custom context fields (key-value pairs) to add to the job. Format: `key_1:value_1,key_2:value_1`.
*   `max_results_to_return` (string, optional): Specify how many results should be returned.
*   `hide_case_wall_table` (bool, optional): If enabled, action will not prepare a case wall table with results.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the query execution, including job status and potentially results if the query completes within the timeout.

### Ping

Test connectivity to the Cisco Orbital with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the Cisco Orbital integration is properly configured in the SOAR Marketplace tab with the correct API URL, Client ID, and Client Password.
*   The API credentials require permissions to execute Orbital queries.
*   The `Execute Query` action runs asynchronously. Adjust playbook timeouts accordingly. Results might need to be retrieved in a subsequent step or checked via the Orbital console if the query takes longer than the action timeout.
*   Familiarity with Osquery syntax is required for the `Execute Query` action.
