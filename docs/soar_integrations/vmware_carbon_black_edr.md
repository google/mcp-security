# VMware Carbon Black EDR Integration

The VMware Carbon Black EDR (formerly Carbon Black Response or CB Response) integration for Chronicle SOAR allows interaction with the on-premises Carbon Black EDR platform. This enables deep investigation of endpoint activity, threat hunting, and live response actions directly from SOAR workflows.

## Overview

VMware Carbon Black EDR is an on-premises solution providing advanced threat hunting and incident response capabilities. It continuously records endpoint activity, allowing security teams to visualize attack chains, hunt for threats, and respond by isolating endpoints or terminating processes.

This integration typically enables Chronicle SOAR to:

*   **Search Process Activity:** Query for specific processes based on hash, name, command line, parent process, network connections, file modifications, registry modifications, etc.
*   **Retrieve Endpoint Details:** Get information about sensors (endpoints) managed by CB EDR.
*   **Isolate/Unisolate Endpoints:** Isolate compromised endpoints from the network or remove them from isolation.
*   **Manage Watchlists/Feeds:** Interact with CB EDR watchlists or threat intelligence feeds.
*   **Live Response (Potentially):** Initiate live response sessions or execute specific commands on endpoints (depending on API capabilities and integration implementation).
*   **Manage Bans:** Ban specific binary hashes from executing.

## Key Actions

The following actions are available through the VMware Carbon Black EDR integration:

*   **Enrich Hash (`cb_enterprise_edr_enrich_hash`)**
    *   Description: Enrich a FileHash entity (SHA-256 only) with information from Carbon Black EDR.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash entities (SHA-256).
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Process Search (`cb_enterprise_edr_process_search`)**
    *   Description: Search for process activity on hosts with CB sensors based on search parameters and Host entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `record_limit` (string, required): Maximum number of process records to return.
        *   `query` (string, optional): Query string for process search (e.g., `process_name:svchost.exe`, `process_hash:<hash>`).
        *   `time_frame` (string, optional): Time frame in hours to search within.
        *   `sort_by` (string, optional): Parameter to sort results by.
        *   `sort_order` (List[str], optional): Sort order (e.g., `["ASC"]`, `["DESC"]`).
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname entities to search on.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`cb_enterprise_edr_ping`)**
    *   Description: Test connectivity to the VMware Carbon Black Enterprise EDR server.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Events Associated With Process by Process Guid (`cb_enterprise_edr_get_events_associated_with_process_by_process_guid`)**
    *   Description: Get detailed events (e.g., network connections, file mods) associated with a specific process GUID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `process_guid` (string, required): The specific process GUID to query events for.
        *   `query` (string, required): Query string to filter events (e.g., `netconn_action:ACTION_CONNECTION_CREATE`).
        *   `record_limit` (string, required): Maximum number of event records to return.
        *   `search_criteria` (string, optional): Additional search criteria (e.g., comma-separated `event_type` values like `netconn`).
        *   `time_frame` (string, optional): Time frame in hours to search within.
        *   `sort_by` (string, optional): Parameter to sort results by.
        *   `sort_order` (List[str], optional): Sort order (e.g., `["ASC"]`, `["DESC"]`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (typically Process entity with GUID).
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Use Cases

*   **Deep Dive Investigation:** Following an alert from SIEM or another tool, use the CB EDR integration to search for the associated process hash or command line across all endpoints to understand its prevalence and behavior.
*   **Threat Hunting:** Proactively hunt for specific TTPs or indicators by querying the CB EDR process data via SOAR playbooks.
*   **Rapid Containment:** Isolate endpoints confirmed to be compromised directly from the SOAR case.
*   **Malware Blocking:** Ban the hash of confirmed malware across the environment using the CB EDR integration.

## Configuration

*(Details on configuring the integration, including the CB EDR server URL, API Token (often generated per-user within CB EDR), and any specific SOAR platform settings, should be added here.)*
