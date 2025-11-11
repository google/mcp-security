# PhishRod Integration

The PhishRod integration for Chronicle SOAR connects the SOAR platform with the PhishRod Security Awareness and Anti-Phishing solution. This allows security teams to manage phishing incidents reported through PhishRod and potentially leverage PhishRod's capabilities within SOAR workflows.

## Overview

PhishRod offers a suite of tools for security awareness training, phishing simulation, and phishing incident response. Users can typically report suspected phishing emails using a PhishRod plugin, which then analyzes the email and creates an incident within the PhishRod platform.

This integration likely enables Chronicle SOAR to:

*   **Retrieve Reported Incidents:** Fetch details of phishing incidents reported and analyzed by PhishRod.
*   **Update Incident Status:** Modify the status or classification of incidents within PhishRod based on SOAR investigation findings (e.g., mark as malicious, benign, spam).
*   **Get Incident Details:** Pull specific information about a reported email, such as headers, body, attachments, and PhishRod's initial analysis verdict.
*   **Trigger Actions:** Potentially trigger actions within PhishRod, such as deleting emails from user inboxes (if supported by the PhishRod API and configured).

## Key Actions

The following actions are available through the PhishRod integration:

*   **Update Incident (`phishrod_update_incident`)**
    *   Description: Update an incident's status in PhishRod.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `incident_id` (string, required): Specify the ID of the incident that needs to be updated.
        *   `status` (List[str], optional): Specify the new status for the incident (e.g., `["Benign"]`, `["Malicious"]`, `["Spam"]`). The exact available values depend on the PhishRod configuration.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Mark Incident (`phishrod_mark_incident`)**
    *   Description: Mark an incident with a specific status and add a comment in PhishRod. (Note: The Python code description is empty, but the parameters suggest this functionality).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `incident_id` (string, required): Specify the ID of the incident that needs to be marked.
        *   `comment` (string, required): Specify the comment describing the reasons for marking the incident.
        *   `status` (List[str], optional): Specify how the incident needs to be marked (e.g., `["Benign"]`, `["Malicious"]`, `["Spam"]`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`phishrod_ping`)**
    *   Description: Test connectivity to the PhishRod API using the configured credentials.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Use Cases

*   **Streamlined Phishing Response:** Ingest reported phishing incidents from PhishRod into SOAR cases for consistent investigation and response alongside other alerts.
*   **Automated Triage:** Use SOAR playbooks to automatically query PhishRod for incident details, enrich indicators (URLs, attachments) using other threat intelligence tools, and update the incident status in PhishRod.
*   **Centralized Reporting:** Consolidate reporting and metrics for phishing incidents managed through both PhishRod and SOAR.

## Configuration

*(Details on configuring the integration, including obtaining PhishRod API credentials, specifying the PhishRod instance URL, and configuring settings within the SOAR platform, should be added here.)*
