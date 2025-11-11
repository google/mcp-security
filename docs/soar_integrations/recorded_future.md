# Recorded Future Integration

The Recorded Future integration for Chronicle SOAR allows interaction with the Recorded Future Security Intelligence Platform. This enables enriching various indicators (IPs, hashes, domains, URLs, CVEs) with threat intelligence, managing Recorded Future alerts, and adding analyst notes.

## Overview

Recorded Future provides real-time threat intelligence powered by machine learning, aggregating and analyzing data from open, closed, and technical sources. It offers context on indicators, vulnerabilities, threat actors, and attack trends.

This integration typically enables Chronicle SOAR to:

*   **Enrich Indicators:** Query Recorded Future for risk scores, related entities, threat context, and evidence for IPs, domains/hostnames, file hashes, URLs, and CVEs.
*   **Manage Alerts:** Retrieve details for specific Recorded Future alerts and update their status or assignment.
*   **Add Analyst Notes:** Add notes to entities within Recorded Future directly from SOAR.

## Key Actions

The following actions are available through the Recorded Future integration:

*   **Get Host Related Entities (`recorded_future_get_host_related_entities`)**
    *   Description: Query Recorded Future to get related entities (e.g., IPs, malware) for a Hostname entity.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich Hash (`recorded_future_enrich_hash`)**
    *   Description: Enrich a FileHash entity with Recorded Future intelligence, including risk score and optionally related entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `risk_score_threshold` (string, required): Minimum risk score (0-89) to mark as suspicious.
        *   `include_related_entities` (bool, optional): Include related entities in the enrichment data.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Hash Related Entities (`recorded_future_get_hash_related_entities`)**
    *   Description: Query Recorded Future to get related entities for a FileHash entity.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific FileHash entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Add Analyst Note (`recorded_future_add_analyst_note`)**
    *   Description: Add an analyst note to entities (previously enriched with RF ID) within Recorded Future.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `note_title` (string, required): Title for the note.
        *   `note_text` (string, required): Text content of the note.
        *   `note_source` (string, required): Recorded Future ID for the note source (e.g., `VWKdVr` for analyst notes).
        *   `enrich_entity` (bool, required): Whether to enrich the entity first if RF ID is missing.
        *   `topic` (List[str], optional): Relevant note topic.
        *   `target_entities` (List[TargetEntity], optional): Entities (IP, Hash, Domain, URL, CVE) to add the note to.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Update Alert (`recorded_future_update_alert`)**
    *   Description: Update the status or assignee of a Recorded Future alert.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `alert_id` (string, required): The ID of the Recorded Future alert to update.
        *   `status` (List[str], required): New status for the alert (e.g., `["Dismissed"]`, `["Open"]`).
        *   `assign_to` (string, optional): User ID, username, hash, or email to assign the alert to.
        *   `note` (string, optional): Note to add to the alert update.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich CVE (`recorded_future_enrich_cve`)**
    *   Description: Enrich a CVE entity with Recorded Future intelligence, including risk score and optionally related entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `risk_score_threshold` (string, required): Minimum risk score (0-99) to mark as suspicious.
        *   `include_related_entities` (bool, optional): Include related entities in the enrichment data.
        *   `target_entities` (List[TargetEntity], optional): Specific CVE entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich IP (`recorded_future_enrich_ip`)**
    *   Description: Enrich an IP Address entity with Recorded Future intelligence, including risk score and optionally related entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `risk_score_threshold` (string, required): Minimum risk score (0-99) to mark as suspicious.
        *   `include_related_entities` (bool, optional): Include related entities in the enrichment data.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`recorded_future_ping`)**
    *   Description: Test connectivity to the Recorded Future API.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get Alert Details (`recorded_future_get_alert_details`)**
    *   Description: Fetch detailed information (documents, related entities, evidence) for a specific Recorded Future alert ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `alert_id` (string, required): The ID of the Recorded Future alert.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get IP Related Entities (`recorded_future_get_ip_related_entities`)**
    *   Description: Query Recorded Future to get related entities (e.g., domains, hashes) for an IP Address entity.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific IP Address entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich IOC (`recorded_future_enrich_ioc`)**
    *   Description: Enrich multiple IOC entities (IP, Hash, Domain, URL, CVE) simultaneously. Recommended as the first enrichment step.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `risk_score_threshold` (string, required): Minimum risk score to mark entities as suspicious (applies appropriate scale per entity type).
        *   `target_entities` (List[TargetEntity], optional): Entities to enrich.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich Host (`recorded_future_enrich_host`)**
    *   Description: Enrich a Hostname/Domain entity with Recorded Future intelligence, including risk score and optionally related entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `risk_score_threshold` (string, required): Minimum risk score (0-99) to mark as suspicious.
        *   `include_related_entities` (bool, optional): Include related entities in the enrichment data.
        *   `target_entities` (List[TargetEntity], optional): Specific Hostname/Domain entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Get CVE Related Entities (`recorded_future_get_cve_related_entities`)**
    *   Description: Query Recorded Future to get related entities for a CVE entity.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Specific CVE entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Enrich URL (`recorded_future_enrich_url`)**
    *   Description: Enrich a URL entity with Recorded Future intelligence, including risk score and optionally related entities.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `risk_score_threshold` (string, required): Minimum risk score (0-99) to mark as suspicious.
        *   `include_related_entities` (bool, optional): Include related entities in the enrichment data.
        *   `target_entities` (List[TargetEntity], optional): Specific URL entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Configuration

*(Details on configuring the integration, including the Recorded Future API URL, API Token, and any specific SOAR platform settings, should be added here.)*
