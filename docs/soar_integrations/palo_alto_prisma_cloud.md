# Palo Alto Prisma Cloud Integration

## Overview

This integration allows you to connect to Palo Alto Networks Prisma Cloud to enrich asset information, respond to alerts, and test connectivity.

## Configuration

The configuration for this integration (Prisma Cloud API URL, Access Key ID, Secret Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Enrich Assets

Enrich information about a resource using Palo Alto Prisma Cloud based on asset identifiers.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `asset_identifiers` (string, required): Comma-separated list of asset identifiers (Asset ID or Asset RRN) for which you want to fetch details.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment details for the specified assets.

### Respond To Alert

Respond to an alert in Palo Alto Prisma Cloud by changing its status (Dismiss, Snooze, Reopen, Remediate).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_id` (string, required): ID of the alert to respond to.
*   `response_type` (List[Any], optional): Alert status to set (Dismiss, Snooze, Reopen, Remediate).
*   `snooze_time` (string, optional): Snooze time in hours (required if `response_type` is Snooze).
*   `dismiss_note` (string, optional): Note for a dismissal.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the alert response operation.

### Ping

Test connectivity to the Palo Alto Prisma Cloud with parameters provided at the integration configuration page in the Chronicle Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

## Notes

*   Ensure the Palo Alto Prisma Cloud integration is properly configured in the SOAR Marketplace tab with the correct API credentials.
*   Asset identifiers can be either the Asset ID or the Asset Resource Name (RRN).
*   When responding to an alert with `Snooze`, the `snooze_time` parameter is required.
