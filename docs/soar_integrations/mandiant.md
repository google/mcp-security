# Mandiant Integration

## Overview

This integration allows you to connect to Mandiant Threat Intelligence and perform actions like enriching IOCs and entities, retrieving related entities, getting malware details, and testing connectivity.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Enrich IOCs

Get information about Indicators of Compromise (IOCs) from Mandiant.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ioc_identifiers` (string, required): Specify a comma-separated list of IOCs that need to be enriched.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including enrichment data for the IOCs.

### Ping

Test connectivity to the Mandiant service using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Related Entities

Get information about IOCs related to entities using information from Mandiant. Supported entities: Hostname, IP Address, URL, File Hash, Threat Actor.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `lowest_severity_score` (string, required): Specify the lowest severity score that will be used to return related indicators. Maximum: 100.
*   `max_io_cs_to_return` (string, optional): Specify how many indicators action needs to process per entity. Default: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including related IOCs.

### Enrich Entities

Enrich entities using information from Mandiant. Supported entities: Hostname, IP Address, URL, File Hash, Threat Actor, Vulnerability. Note: only MD5, SHA-1 and SHA-256 are supported.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `severity_score_threshold` (string, required): Specify the lowest severity score that will be used to mark the entity as suspicious. Note: only indicators (hostname, IP address, file hash, url) can be marked as suspicious. Maximum: 100.
*   `create_insight` (bool, optional): If enabled, action will create an insight containing all of the retrieved information about the entity.
*   `only_suspicious_entity_insight` (bool, optional): If enabled, action will only create an insight for suspicious entities. Note: parameter "Create Insight" should be enabled. Insights for "Threat Actor" and "Vulnerability" entities will also be created even though they are not marked as suspicious.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including enrichment data for the entities.

### Get Malware Details

Get information about malware from Mandiant.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `malware_names` (string, required): Specify a comma-separated list of malware names that need to be enriched.
*   `create_insight` (bool, optional): If enabled, action will create an insight containing information about the malware.
*   `fetch_related_io_cs` (bool, optional): If enabled, action will fetch indicators that are related to the provided malware.
*   `max_related_io_cs_to_return` (string, optional): Specify how many indicators action needs to process per malware. Default: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including details about the specified malware.

## Notes

*   Ensure the Mandiant integration is properly configured in the SOAR Marketplace tab.
*   This integration appears functionally identical to the "Mandiant Threat Intelligence" integration.
*   Some actions support specific entity types as input. Refer to the action descriptions for details.
*   Hash enrichment supports MD5, SHA-1, and SHA-256.
