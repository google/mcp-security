# Broadcom DeepSight Integration

## Overview

This integration allows interaction with the Broadcom DeepSight Intelligence platform to query the reputation of various indicators, including IP addresses, domains, URLs, file hashes, and email addresses.

## Configuration

To configure this integration within the SOAR platform, you typically need the following DeepSight details:

*   **API Key:** Your DeepSight API key for authentication.
*   **API URL:** The base URL for the DeepSight API (e.g., `https://deepsightapi.symantec.com`).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Scan Hash

DeepSight scan hash. Retrieves reputation information for a given file hash.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation details (e.g., score, classification, first seen) for the specified hash(es).

### Scan Email

DeepSight scan email. Retrieves reputation information for a given email address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Email entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation details for the specified email address(es).

### Ping

Test Connectivity to DeepSight.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Scan URL

DeepSight scan URL. Retrieves reputation information for a given URL.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation details for the specified URL(s).

### Scan File Name

DeepSight scan file name. Retrieves reputation information associated with a given file name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports File entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation details associated with the specified file name(s).

### Scan Domain

DeepSight scan domain. Retrieves reputation information for a given domain.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation details for the specified domain(s).

### Scan IP

DeepSight scan IP address. Retrieves reputation information for a given IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing reputation details for the specified IP address(es).

## Notes

*   Ensure the DeepSight integration is properly configured in the SOAR Marketplace tab with a valid API Key and API URL.
*   The API key requires appropriate permissions within the DeepSight platform.
*   Each "Scan" action targets a specific entity type (IP, Domain, URL, Hash, Email, File Name).
