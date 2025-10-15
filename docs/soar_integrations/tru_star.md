# TruSTAR SOAR Integration

## Overview

This document outlines the tools available for the TruSTAR integration within the SOAR platform. These tools allow interaction with the TruSTAR API for enriching entities, retrieving related IOCs and reports, and managing enclaves.

## Tools

### `tru_star_get_related_io_cs`

Get information about IOCs that are related to the provided entities. Supported entities: All.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_io_cs_to_return` (str, optional, default=None): Specify how many IOCs to return. Default: 50. Maximum: 1000.
*   `enclave_filter` (str, optional, default=None): Specify a comma-separated list of enclave names that should be used during the enrichment.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tru_star_get_related_reports`

Get information about reports related to the entities. Supported entities: All.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `create_insight` (bool, optional, default=None): If enabled, action will create an insight containing information about reports related to the entities.
*   `include_report_body_in_insight` (bool, optional, default=None): If enabled, insight will contain information about the report body. Note: report body can be very big in size.
*   `enclave_filter` (str, optional, default=None): Specify a comma-separated list of enclave names that should be used during the enrichment.
*   `max_reports_to_return` (str, optional, default=None): Specify how many reports to return. Default: 10. Maximum: 25.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tru_star_ping`

Test connectivity to the TruSTAR with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tru_star_enrich_entities`

Enrich entities using information from TruSTAR. Supported entities: All.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `security_level_threshold` (List[str], required): Specify what should be the lowest security level for the entity to be marked as suspicious.
*   `enclave_filter` (str, optional, default=None): Specify a comma-separated list of enclave names that should be used during the enrichment.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `tru_star_list_enclaves`

List available enclaves in TruSTAR.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_logic` (List[str], optional, default=None): Specify what filter logic should be applied.
*   `filter_value` (str, optional, default=None): Specify what value should be used in the filter.
*   `max_enclaves_to_return` (str, optional, default=None): Specify how many enclaves to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
