# McAfee TIE DXL Integration

## Overview

This integration allows you to connect to McAfee Threat Intelligence Exchange (TIE) via Data Exchange Layer (DXL) to get and set file reputations, retrieve file references, and test connectivity.

## Configuration

The configuration for this integration (DXL broker details, certificates, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Get File Reputation

Get file reputation information from McAfee TIE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `enrich_with_all_services` (bool, optional): If checked, enrich with all results from all returned services. Else, store only the worst reputation as enrichment.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including file reputation details.

### Set File Reputation

Set a file's enterprise reputation in McAfee TIE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `trust_level` (string, required): The trust level to set to the file's reputation.
*   `file_name` (string, optional): The name of the file.
*   `comment` (string, optional): The comment to add to the file's reputation.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the McAfee TIE DXL service.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get File References

Get references for a file (the agent on which the file was used) from McAfee TIE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including agent references for the file.

## Notes

*   Ensure the McAfee TIE DXL integration is properly configured in the SOAR Marketplace tab, including DXL broker details and necessary certificates.
*   Actions primarily operate on FileHash entities within the specified scope.
