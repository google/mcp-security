# Trend Micro Cloud App Security Integration

This document describes the available tools for the Trend Micro Cloud App Security integration within the SecOps SOAR MCP Server. This integration allows interaction with Trend Micro Cloud App Security for email security, account mitigation, and threat enrichment.

## Configuration

Ensure the Trend Micro Cloud App Security integration is configured in the SOAR platform with the necessary API credentials and instance details.

## Available Tools

### trend_micro_cloud_app_security_add_entities_to_blocklist
- **Description:** Add entities (URL, Filehash - SHA-1 only, Email Address) to a blocklist in Trend Micro Cloud App Security.
- **Supported Entities:** URL, Filehash (SHA-1), Email Address (User entity matching email pattern)
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the entities to block. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the blocklist action.

### trend_micro_cloud_app_security_mitigate_accounts
- **Description:** Perform mitigation actions (e.g., disable sign-in, reset password) on user accounts via Trend Micro Cloud App Security.
- **Note:** Only Exchange accounts are supported.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `mitigation_action` (List[str], required): Specify the mitigation action(s) to apply (refer to Trend Micro documentation for valid actions).
    - `email_addresses` (str, required): Specify a comma-separated list of email addresses to mitigate.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the mitigation action.

### trend_micro_cloud_app_security_ping
- **Description:** Test connectivity to the Trend Micro Cloud App Security instance configured in the SOAR platform.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### trend_micro_cloud_app_security_mitigate_emails
- **Description:** Delete or quarantine emails using Trend Micro Cloud App Security based on message IDs.
- **Notes:**
    - For Gmail, only deletion is supported.
    - This action only initiates mitigation; it does not check the final status.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `mitigation_action` (List[str], required): Specify the mitigation action ("delete" or "quarantine").
    - `service` (List[str], required): Specify the email service ("gmail" or "exchange").
    - `message_i_ds` (str, required): Specify a comma-separated list of message IDs to mitigate.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the mitigation initiation.

### trend_micro_cloud_app_security_enrich_entities
- **Description:** Enrich entities (URL, Filehash, Email Address) with information from Trend Micro Cloud App Security.
- **Note:** For URLs, the action uses the domain part for enrichment.
- **Supported Entities:** URL, Filehash, Email Address (User entity matching email pattern)
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the entities to enrich. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the enrichment results.

### trend_micro_cloud_app_security_entity_email_search
- **Description:** Search emails based on entities (URL, Hash, Email, Subject, Filename, IP) in Trend Micro Cloud App Security.
- **Note:** Only SHA-1 and SHA-256 hashes are supported.
- **Supported Entities:** URL, Filehash (SHA1, SHA256), Email Address, Email Subject, File Name, IP Address
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `max_days_backwards` (str, optional): Max days backwards to search (Max 90, Default: 30). Defaults to None.
    - `max_emails_to_return` (str, optional): Max emails to return (Default: 100). Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the entities to search by. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the search results (emails found).
