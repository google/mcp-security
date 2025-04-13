# MITRE ATT&CK Integration

## Overview

This integration allows you to interact with the MITRE ATT&CK framework data to retrieve details about techniques, associated intrusions (groups/software), and mitigations.

## Configuration

This integration typically uses a local or cached version of the MITRE ATT&CK data and does not require external configuration like API keys within the SOAR platform's Marketplace tab.

## Actions

### Get Associated Intrusions

Retrieve information about intrusions (groups/software) that are associated with a MITRE ATT&CK technique.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `technique_id` (string, required): Specify the identifier (Name, ID, or External ID) that will be used to find the associated intrusions.
*   `identifier_type` (List[Any], required): Specify what identifier type to use (Attack Name, Attack ID, External Attack ID).
*   `max_intrusions_to_return` (string, optional): Specify how many intrusions to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of associated intrusions (groups and software).

### Get Technique Details

Retrieve detailed information about MITRE ATT&CK technique(s).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `technique_identifier` (string, required): Specify the comma-separated list of identifiers (Name, ID, or External ID) that will be used to find the detailed information about techniques.
*   `identifier_type` (List[Any], required): Specify what identifier type to use (Name, ID, External ID).
*   `create_insights` (bool, optional): If enabled, action will create a separate insight for every processed technique.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified technique(s).

### Get Techniques Details

Retrieve detailed information about MITRE ATT&CK techniques. (Note: This action seems functionally identical to "Get Technique Details" but might handle multiple identifiers differently internally).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `technique_identifier` (string, required): Specify the identifier (Name, ID, or External ID) that will be used to find the detailed information about technique. Comma-separated values.
*   `identifier_type` (List[Any], required): Specify what identifier type to use (Attack Name, Attack ID, External Attack ID).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified technique(s).

### Ping

Test Connectivity (typically checks if the MITRE ATT&CK data source is accessible).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Mitigations

Retrieve information about mitigations that are associated with a MITRE ATT&CK technique.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `technique_id` (string, required): Specify the identifier (Name, ID, or External ID) that will be used to find the mitigations related to the attack technique.
*   `identifier_type` (List[Any], required): Specify what identifier type to use (Attack Name, Attack ID, External Attack ID).
*   `max_mitigations_to_return` (string, optional): Specify how many mitigations to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of associated mitigations.

### Get Techniques Mitigations

Retrieve information about mitigations that are associated with MITRE ATT&CK techniques. (Note: This action seems functionally identical to "Get Mitigations" but might handle multiple identifiers differently internally).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `technique_id` (string, required): Specify the identifier (Name, ID, or External ID) that will be used to find the mitigations related to attack technique. Comma-separated values.
*   `identifier_type` (List[Any], required): Specify what identifier type to use (Attack Name, Attack ID, External Attack ID).
*   `max_mitigations_to_return` (string, optional): Specify how many mitigations to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of associated mitigations for the specified technique(s).

## Notes

*   This integration relies on the MITRE ATT&CK dataset. Ensure the data source is up-to-date if using a local copy.
*   Techniques can be identified by Name (e.g., "Access Token Manipulation"), ID (e.g., "attack-pattern--478aa214-2ca7-4ec0-9978-18798e514790"), or External ID (e.g., "T1050").
