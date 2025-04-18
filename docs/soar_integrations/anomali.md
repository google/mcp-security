# Anomali SOAR Integration

This document details the tools provided by the Anomali SOAR integration.

## Tools

### `anomali_get_threat_info`

Enrich entities using information from Anomali ThreatStream. Supported entities: IP, URL, Hash, Email Addresses (User entities that match email regex).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `limit` (str, required): Specify how many records to return per entity.
*   `severity_threshold` (Optional[List[Any]], optional, default=None): Specify what should be the severity threshold for the entity, in order to mark it as suspicious. If multiple records are found for the same entity, action will take the highest severity out of all available records.
*   `confidence_threshold` (Optional[str], optional, default=None): Specify what should be the confidence threshold for the entity, in order to mark it as suspicious. Note: Maximum is 100. If multiple records are found for the entity, action will take the average. Active records have priority. Default: 50.
*   `ignore_false_positive_status` (Optional[bool], optional, default=None): If enabled, action will ignore the false positive status and mark the entity as suspicious based on the "Severity Threshold" and "Confidence Threshold". If disabled, action will never label false positive entities as suspicious, regardless, if they pass the "Severity Threshold" and "Confidence Threshold" conditions or not.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_ping`

Test connectivity to Anomali ThreatStream

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_get_related_associations`

Retrieve entity related associations from Anomali ThreatStream.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `return_campaigns` (Optional[bool], optional, default=None): If enabled, action will fetch related campaigns and details about them.
*   `return_threat_bulletins` (Optional[bool], optional, default=None): If enabled, action will fetch related threat bulletins and details about them.
*   `return_actors` (Optional[bool], optional, default=None): If enabled, action will fetch related actors and details about them.
*   `return_attack_patterns` (Optional[bool], optional, default=None): If enabled, action will fetch related attack patterns and details about them.
*   `return_courses_of_action` (Optional[bool], optional, default=None): If enabled, action will fetch related courses of action and details about them.
*   `return_identities` (Optional[bool], optional, default=None): If enabled, action will fetch related identities and details about them.
*   `return_incidents` (Optional[bool], optional, default=None): If enabled, action will fetch related incidents and details about them.
*   `return_infrastructure` (Optional[bool], optional, default=None): If enabled, action will fetch related infrastructure and details about them.
*   `return_intrusion_sets` (Optional[bool], optional, default=None): If enabled, action will fetch related intrusion sets and details about them.
*   `return_malware` (Optional[bool], optional, default=None): If enabled, action will fetch related malware and details about them.
*   `return_signatures` (Optional[bool], optional, default=None): If enabled, action will fetch related signatures and details about them.
*   `return_tools` (Optional[bool], optional, default=None): If enabled, action will fetch related tools and details about them.
*   `return_tt_ps` (Optional[bool], optional, default=None): If enabled, action will fetch related TTPs and details about them.
*   `return_vulnerabilities` (Optional[bool], optional, default=None): If enabled, action will fetch related vulnerabilities and details about them.
*   `create_campaign_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available "Campaign" associations.
*   `create_actors_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available "Actor" associations.
*   `create_signature_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available "Signature" associations.
*   `create_vulnerability_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available "Vulnerability" associations.
*   `max_associations_to_return` (Optional[str], optional, default=None): Specify how many associations to return per type. Default: 5
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
