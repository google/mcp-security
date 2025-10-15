# Security Command Center (SCC) Enterprise Integration

Connects Chronicle SOAR to Google Cloud Security Command Center (SCC) Enterprise tier, focusing on managing cloud security posture findings and integrating with ITSM tools like ServiceNow and Jira.

## Configuration

*(Details on setting up the SCC Enterprise integration, including necessary GCP service accounts, API enablement (Security Command Center API, Cloud Asset API), and potentially ITSM credentials, would go here.)*

## Key Actions (Tools)

The following actions are available through the SCC Enterprise integration:

### `scc_enterprise_lock_playbook`

*   **Description:** This action will enforce only one playbook being executed for given Posture case.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_create_scc_enterprise_cloud_posture_ticket_type_snow`

*   **Description:** This action will create a new ticket type called "SCC Enterprise Cloud Posture Ticket" in ServiceNow. It’s a mandatory requirement for the "Sync SCC-ServiceNow Tickets" job and "Posture Findings with SNOW" playbook to work.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `api_root` (str, required): API root of the ServiceNow instance.
    *   `username` (str, required): Username of the ServiceNow account.
    *   `password` (str, required): Password of the ServiceNow account.
    *   `verify_ssl` (Optional[bool], optional, default: None): If enabled, verify the SSL certificate for the connection to the ServiceNow is valid.
    *   `table_role` (Optional[str], optional, default: None): Specify the role that should be set to access the newly created table. If nothing is provided, action will create a new role "u_scc_enterprise_cloud_posture_ticket_user".
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_set_scc_findings_state_context_value`

*   **Description:** Set "SCC-FINDINGS-STATE" context value that is used by the "Sync SCC Data" job, action "Prepare Description" and ITSM jobs.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_cloud_entity_parser`

*   **Description:** Parse GCP related Entities from am existing alert's events data, and adds them to the alert.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_ping`

*   **Description:** Test Connectivity
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_create_scc_enterprise_cloud_posture_ticket_type_jira`

*   **Description:** This action will create a new ticket type called SCC Enterprise Cloud Posture Ticket” in Jira. It’s a mandatory requirement for the “Sync SCC-Jira Tickets” job and “Posture Findings with Jira” playbook to work. Note: as a part of the process, action will create a new project SCC Enterprise Project” dedicated to SCC Enterprise.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `api_root` (str, required): API root of the Jira instance.
    *   `username` (str, required): Username of the Jira account.
    *   `api_token` (str, required): Password of the Jira account.
    *   `verify_ssl` (Optional[bool], optional, default: None): If enabled, verify the SSL certificate for the connection to Jira is valid.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_add_scce_tags`

*   **Description:** Add all of the SCCE metadata tags to the case.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `scc_enterprise_prepare_description`

*   **Description:** Prepare description for ITSM ticket.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `output` (Optional[List[str]], optional, default: None):
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

## Use Cases

*   Parsing GCP entities from SCC findings within SOAR alerts.
*   Adding SCC-specific metadata tags to SOAR cases.
*   Preparing finding details for synchronization with ITSM tools (ServiceNow, Jira).
*   Setting up required ticket types and configurations in ServiceNow or Jira for SCC integration.
*   Managing playbook execution flow for SCC posture cases.
