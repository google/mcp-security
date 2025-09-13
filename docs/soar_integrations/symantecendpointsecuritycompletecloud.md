# SymantecEndpointSecurityCompleteCloud SOAR Integration

## Overview
This document outlines the tools available in the Symantec Endpoint Security Complete Cloud (SymantecESCC) SOAR integration. These tools allow interaction with Symantec ESCC for retrieving related IOCs, testing connectivity, enriching entities, and listing device groups.

## Tools

### `symantec_escc_get_related_io_cs`
Get IOCs related to the entities from Symantec Endpoint Security Complete. Supported entities: Hash, URL and IP Address. Only SHA256 hashes are supported.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `source_filter` (Optional[str], optional, default=None): Specify the source filter. If nothing is provided, action will return related entities, based on all sources. Possible Values: byThreatActor, byProcessChain, bySignature, bySampleTraits, byNetworkingTrait, bySimilarIncidents.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `symantec_escc_ping`
Test connectivity to the  Symantec Endpoint Security Complete with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `symantec_escc_enrich_entities`
Enrich entities using information from Symantec Endpoint Security Complete. Supported entities: Hostname, Hash, URL and IP Address. Only SHA256 hashes are supported.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `device_group` (str, required): Specify the name of the device group that should be used to retrieve information about endpoints.
*   `create_endpoint_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight containing information about the endpoints.
*   `create_ioc_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight containing information about enriched IOCs.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `symantec_escc_list_device_groups`
List available device groups in Symantec Endpoint Security Complete.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_logic` (Optional[List[str]], optional, default=None): Specify what filter logic should be applied.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter.
*   `max_groups_to_return` (Optional[str], optional, default=None): Specify how many groups to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.
