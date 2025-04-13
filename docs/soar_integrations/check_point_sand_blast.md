# Check Point SandBlast Integration

## Overview

This integration allows you to connect to Check Point SandBlast (Threat Emulation) to query file hash reputation and upload files for analysis.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Check Point details:

*   **API Key:** Your Check Point API key for authentication (often obtained from the Check Point Infinity Portal or your management server).
*   **Server URL:** The base URL for the SandBlast API endpoint (e.g., `https://te.checkpoint.com/tecloud/api/v1/file/`). The specific URL might vary depending on your deployment (cloud vs. on-premise).

*(Note: The exact parameter names and required details might vary depending on the specific SOAR platform configuration interface and your Check Point deployment.)*

## Actions

### Ping

Test connectivity to the Check Point SandBlast with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Query

Get threat reputation information about FILEHASH entities.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if severity is equal or above the given threshold (e.g., `Medium`, `High`, `Critical`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reputation details (severity, verdict, etc.) for the specified hash(es).

### Upload File

Upload files for analysis using specified SandBlast features.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): The full path of the file(s) to upload (comma-separated for multiple).
*   `enable_threat_emulation_feature` (bool, optional): If enabled, use Threat Emulation. Default if no features selected.
*   `enable_anti_virus_feature` (bool, optional): If enabled, use Anti-Virus.
*   `enable_threat_extraction_feature` (bool, optional): If enabled, use Threat Extraction (CDR).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the upload and analysis request, likely including report IDs or status.

## Notes

*   Ensure the Check Point SandBlast integration is properly configured in the SOAR Marketplace tab with a valid API Key and Server URL.
*   The API key requires appropriate permissions for file upload and query operations.
*   The `Query` action supports FileHash entities (MD5, SHA1, SHA256).
*   The `Upload File` action requires the full path to the file(s) accessible by the SOAR agent/server executing the action.
