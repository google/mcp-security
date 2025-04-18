# Anomali Staxx SOAR Integration

This document details the tools provided by the Anomali Staxx SOAR integration.

## Tools

### `anomali_staxx_ping`

Test connectivity to the Anomali Staxx with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
