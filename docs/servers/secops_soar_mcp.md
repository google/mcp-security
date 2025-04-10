# SecOps SOAR MCP Server

This server provides tools for interacting with a Security Orchestration, Automation, and Response (SOAR) platform, likely Google SecOps SOAR (formerly Siemplify). It includes core case management functionalities and dynamically loads integration-specific tools.

## Core Tools (Case Management & Entities)

These tools are always available.

- **`list_cases()`**
    - **Description:** Lists available cases in the SOAR platform.
- **`post_case_comment(case_id, comment)`**
    - **Description:** Adds a textual comment to a specific case.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
        - `comment` (required): The comment text to add.
- **`list_alerts_by_case(case_id)`**
    - **Description:** Lists all alerts associated with a specific case ID.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
- **`list_alert_group_identifiers_by_case(case_id)`**
    - **Description:** Lists the unique group identifiers for alerts within a specific case.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
- **`list_events_by_alert(case_id, alert_id)`**
    - **Description:** Lists the events associated with a particular alert within a given case.
    - **Parameters:**
        - `case_id` (required): The ID of the case containing the alert.
        - `alert_id` (required): The ID of the specific alert.
- **`change_case_priority(case_id, case_priority)`**
    - **Description:** Modifies the priority level of a specific case.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
        - `case_priority` (required): The desired priority level (e.g., "PriorityLow", "PriorityMedium", "PriorityHigh", "PriorityCritical").
- **`get_entities_by_alert_group_identifiers(case_id, alert_group_identifiers)`**
    - **Description:** Retrieves entities (like IPs, users, hosts) involved in one or more alert groups within a case. Can also be used to get target entities for manual actions.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
        - `alert_group_identifiers` (required): A list of alert group identifiers.
- **`get_entity_details(entity_identifier, entity_type, entity_environment)`**
    - **Description:** Fetches detailed information about a specific entity identified by its identifier, type, and environment.
    - **Parameters:**
        - `entity_identifier` (required): The unique identifier of the entity.
        - `entity_type` (required): The type of the entity (e.g., "IP Address", "User").
        - `entity_environment` (required): The environment the entity belongs to.
- **`search_entity(term=None, type=None, is_suspicious=None, is_internal_asset=None, is_enriched=None, network_name=None, environment_name=None)`**
    - **Description:** Searches for entities within the SOAR platform based on various optional criteria.
    - **Parameters:** (All optional)
        - `term`: A search term (e.g., an IP address, username).
        - `type`: A list of entity types to filter by.
        - `is_suspicious`: Boolean filter for suspicious status.
        - `is_internal_asset`: Boolean filter for internal asset status.
        - `is_enriched`: Boolean filter for enrichment status.
        - `network_name`: List of network names to filter by.
        - `environment_name`: List of environment names to filter by.
- **`get_case_full_details(case_id)`**
    - **Description:** Retrieves comprehensive details for a single case, including its basic information, associated alerts, and comments.
    - **Parameters:**
        - `case_id` (required): The ID of the case.

## Dynamic Integration Tools (Marketplace)

This server can dynamically load additional tools based on integrations enabled via the `--integrations` command-line flag when the server is started. These tools correspond to modules found in the `marketplace/` directory (e.g., `--integrations CSV,Siemplify` would load tools from `marketplace/csv.py` and `marketplace/siemplify.py`).

Refer to the specific integration modules within the `marketplace/` directory or the SOAR platform's documentation for details on the tools provided by each integration.
