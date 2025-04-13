# Check Point Threat Reputation Integration

## Overview

This integration allows you to connect to the Check Point ThreatCloud intelligence service to query the reputation of IP addresses, hostnames (domains), and file hashes.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Check Point details:

*   **API Key:** Your Check Point API key for ThreatCloud access (often obtained from the Check Point Infinity Portal or your management server).
*   **Client ID:** Your Check Point Client ID associated with the API key.
*   **Server URL:** The base URL for the Check Point Threat Reputation API (e.g., `https://threatcloud.checkpoint.com/ThreatCloud/API/v1/file/query`).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Get IP Reputation

Enrich Siemplify IP entity based on the information from the CheckPoint Threat Reputation service.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if the returned risk value for entity is above a given threshold (e.g., `Medium`, `High`, `Critical`).
*   `create_insight` (bool, optional): Specify whether the Siemplify Insight should be created based on the action result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation details (risk, classification, etc.) for the specified IP address(es).

### Get Host Reputation

Enrich the Siemplify Host entity based on the information from the CheckPoint Threat Reputation service.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if the returned risk value for entity is above a given threshold (e.g., `Medium`, `High`, `Critical`).
*   `create_insight` (bool, optional): Specify whether the Siemplify Insight should be created based on the action result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation details for the specified hostname(s)/domain(s).

### Ping

Test connectivity to the CheckPoint Threat Reputation service with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get File Hash Reputation

Enrich Siemplify File hash entity based on the information from the CheckPoint Threat Reputation service. Action accepts file hashes in md5, sha1 and sha256 formats.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if the returned risk value for entity is above a given threshold (e.g., `Medium`, `High`, `Critical`).
*   `create_insight` (bool, optional): Specify whether the Siemplify Insight should be created based on the action result.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities (MD5, SHA1, SHA256).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation details for the specified file hash(es).

## Notes

*   Ensure the Check Point Threat Reputation integration is properly configured in the SOAR Marketplace tab with a valid API Key, Client ID, and Server URL.
*   The API key requires permissions to access the ThreatCloud reputation services.
*   Specify a threshold for marking entities as suspicious based on the risk score returned by Check Point.
