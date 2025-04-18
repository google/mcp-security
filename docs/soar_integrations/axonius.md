# Axonius Integration

## Overview

This integration allows you to connect to Axonius to enrich entities (devices and users), manage tags, add notes, and test connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Axonius details:

*   **API URL:** The URL of your Axonius instance (e.g., `https://your-company.axonius.com`).
*   **API Key:** An API key generated within your Axonius instance for authentication.
*   **API Secret:** The corresponding secret associated with the API Key.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Ping

Test connectivity to the Axonius with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Remove Tags

Remove tags from entities in Axonius. Supported entities: Hostname, IP, Mac Address, User, Email Addresses (User entities that match email regex).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tags` (string, required): Specify the comma-separated list of tags that need to be removed from the entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Enrich Entities

Enrich entities using information from Axonius. Supported entities: IP Address, Hostname, Mac Address, User, Email Addresses (User entities that match email regex).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_endpoint_insight` (bool, optional): If enabled, action will create an insight containing information about the endpoints.
*   `create_user_insight` (bool, optional): If enabled, action will create an insight containing information about the user.
*   `max_notes_to_return` (string, optional): Specify how many notes to show in the case wall table. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified entities.

### Add Tags

Add tags to entities in Axonius. Supported entities: Hostname, IP, Mac Address, User, Email Addresses (User entities that match email regex).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tags` (string, required): Specify the comma-separated list of tags that need to be added to the entities.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Note

Add a note to entities in Axonius. Supported entities: Hostname, IP, Mac Address, User, Email Addresses (User entities that match email regex).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `note` (string, required): Specify what note needs to be added.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Ensure the Axonius integration is properly configured in the SOAR Marketplace tab with the correct API URL, Key, and Secret.
*   Actions support various entity types for enrichment and management. Refer to individual action descriptions for supported types.
