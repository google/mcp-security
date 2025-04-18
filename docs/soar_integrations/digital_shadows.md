# Digital Shadows Integration

## Overview

This integration allows interaction with the ReliaQuest GreyMatter Digital Risk Protection platform (formerly Digital Shadows SearchLight) to enrich various types of indicators.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Digital Shadows details:

*   **API Key:** Your Digital Shadows API Key ID.
*   **API Secret:** Your Digital Shadows API Secret Key.
*   **API URL:** The base URL for the Digital Shadows API (e.g., `https://api.searchlight.app/`).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Enrich URL

Enrich a Url using Digital Shadows information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified URL(s).

### Enrich Hash (Deprecated)

Deprecated: Enrich a Hash using Digital Shadows information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified hash(es). *(Note: This action is deprecated and may not function as expected).*

### Ping

Test Connectivity to Digital Shadows.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Enrich CVE

Enrich a CVE using Digital Shadows information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports CVE entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified CVE(s).

### Enrich IP (Deprecated)

Deprecated: Enrich an Ip using Digital Shadows information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified IP address(es). *(Note: This action is deprecated and may not function as expected).*

## Notes

*   Ensure the Digital Shadows integration is properly configured in the SOAR Marketplace tab with a valid API Key, API Secret, and API URL.
*   The API credentials require appropriate permissions within the Digital Shadows platform.
*   The `Enrich Hash` and `Enrich IP` actions are marked as deprecated and might be removed or replaced in future versions. Prefer using other available enrichment integrations if possible.
