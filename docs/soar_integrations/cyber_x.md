# Microsoft Defender for IoT (CyberX) Integration

## Overview

This integration allows interaction with Microsoft Defender for IoT (formerly CyberX) to retrieve information about OT/ICS assets, connections, events, alerts, and vulnerabilities.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Microsoft Defender for IoT details:

*   **API URL:** The URL of your Defender for IoT management console API (e.g., `https://your-defender-iot.example.com/api/v1/`).
*   **API Token:** An API token generated within Defender for IoT for authentication.
*   **(Optional) Verify SSL:** Whether to verify the server's SSL certificate.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the API token has the necessary permissions for the desired read operations.)*

## Actions

### Enrich Endpoints

Fetch endpoint (device) information from Defender for IoT.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified endpoint(s).

### Get Connections for Endpoint

Get list of connections for each device (endpoint).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of connections for the specified endpoint(s).

### Get Events

Fetch list of events reported to the event log.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of events retrieved from Defender for IoT.

### Ping

Test CyberX (Defender for IoT) connectivity.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Device Vulnerability Report

Fetch vulnerability report for each endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing vulnerability information for the specified endpoint(s).

### Get Alerts

Fetch list of all alerts detected by XSense (Defender for IoT Sensor).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of alerts retrieved from Defender for IoT.

## Notes

*   Ensure the Microsoft Defender for IoT (CyberX) integration is properly configured in the SOAR Marketplace tab with the correct API URL and API Token.
*   The API token requires appropriate read permissions within Defender for IoT.
*   Actions typically target endpoints identified by IP Address or Hostname entities.
