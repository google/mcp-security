# Rapid7 InsightIDR Integration

The Rapid7 InsightIDR integration for Chronicle SOAR allows interaction with the InsightIDR cloud SIEM and XDR platform. This enables managing investigations and running log queries directly from SOAR workflows.

## Overview

Rapid7 InsightIDR combines SIEM, User and Entity Behavior Analytics (UEBA), and EDR capabilities into a single cloud platform. It collects data from various sources, detects threats, and provides tools for investigation and response.

This integration typically enables Chronicle SOAR to:

*   **Manage Investigations:** List, update status, disposition, and assignee for investigations within InsightIDR.
*   **Manage Saved Queries:** List, create, run, and delete saved Log Entry Query Language (LEQL) queries.
*   **Run Ad-Hoc Queries:** Execute LEQL queries directly (though this specific implementation focuses on saved queries).

## Key Actions

The following actions are available through the Rapid7 InsightIDR integration:

*   **Delete Saved Query (`rapid7_insight_idr_delete_saved_query`)**
    *   Description: Delete a specific saved query by its ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `saved_query_id` (string, required): ID of the saved query to delete (UUID format).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Update Investigation (`rapid7_insight_idr_update_investigation`)**
    *   Description: Update the status and/or disposition of an investigation. (Uses preview API endpoints).
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `investigation_id` (string, required): ID of the investigation to update.
        *   `status` (List[str], optional): New status (e.g., `["OPEN"]`, `["CLOSED"]`).
        *   `disposition` (List[str], optional): New disposition (e.g., `["BENIGN"]`, `["MALICIOUS"]`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Investigations (`rapid7_insight_idr_list_investigations`)**
    *   Description: List investigations based on time frame and status filters.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `time_frame` (string, optional): Time frame in hours to fetch investigations from.
        *   `record_limit` (string, optional): Maximum number of investigations to return.
        *   `include_closed_investigations` (bool, optional): Include closed investigations in the results.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Ping (`rapid7_insight_idr_ping`)**
    *   Description: Test connectivity to the Rapid7 InsightIDR API.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Set Investigation Status (`rapid7_insight_idr_set_investigation_status`)**
    *   Description: Set the status for a specific investigation.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `investigation_id` (string, required): ID of the investigation (UUID format).
        *   `status` (List[str], required): New status (e.g., `["OPEN"]`, `["CLOSED"]`).
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Run Saved Query (`rapid7_insight_idr_run_saved_query`)**
    *   Description: Execute a previously saved LEQL query by its ID.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `saved_query_id` (string, required): ID of the saved query to run.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **List Saved Queries (`rapid7_insight_idr_list_saved_queries`)**
    *   Description: List saved LEQL queries available in the InsightIDR account.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `record_limit` (string, optional): Maximum number of saved queries to return.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Set Investigation Assignee (`rapid7_insight_idr_set_investigation_assignee`)**
    *   Description: Assign an investigation to a specific user by their email address.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `investigation_id` (string, required): ID of the investigation (UUID format).
        *   `assignee_email` (string, required): Email address of the user to assign the investigation to.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

*   **Create Saved Query (`rapid7_insight_idr_create_saved_query`)**
    *   Description: Create a new saved LEQL query in InsightIDR.
    *   Parameters:
        *   `case_id` (string, required): The ID of the case.
        *   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
        *   `name` (string, required): Name for the new saved query.
        *   `statement` (string, required): The LEQL query statement (e.g., `where(foo=bar)`).
        *   `time_frame` (string, required): Time frame in hours for the query.
        *   `logs` (string, optional): Comma-separated list of log names to query against.
        *   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities.
        *   `scope` (string, optional, default="All entities"): Defines the scope for the action.

## Configuration

*(Details on configuring the integration, including the Rapid7 Insight Platform Region, API Key (Organization or User Key), and any specific SOAR platform settings, should be added here.)*
