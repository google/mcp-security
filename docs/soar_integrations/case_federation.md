# Case Federation Integration

## Overview

This integration facilitates testing connectivity between federated SOAR instances. It currently provides a Ping action to verify the connection setup. Case Federation allows linking cases between different SOAR environments (e.g., Parent/Child, MSSP/Customer).

## Configuration

To configure this integration within the SOAR platform, you typically need the following details for the remote SOAR instance you are federating with:

*   **Remote SOAR URL:** The URL of the target SOAR instance (e.g., `https://remote-soar.example.com`).
*   **API Key / Token:** An API key or token generated on the remote SOAR instance for authentication.
*   **(Optional) Username/Password:** Some federation setups might use username/password credentials instead of or in addition to an API key.
*   **(Optional) Instance Identifier:** A unique name or identifier for the remote instance connection.

*(Note: The exact parameter names and authentication methods might vary depending on the specific SOAR platform versions and federation configuration.)*

## Actions

### Ping

Test Connectivity to the remote federated SOAR instance.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action, indicating success or failure of the connection test.

## Notes

*   Ensure the Case Federation integration is properly configured in the SOAR Marketplace tab with the correct URL and credentials for the remote instance.
*   This integration primarily serves to test the connection for case federation features configured elsewhere in the platform.
