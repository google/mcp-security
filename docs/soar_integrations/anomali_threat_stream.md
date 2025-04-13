# Anomali ThreatStream SOAR Integration

This document details the tools provided by the Anomali ThreatStream SOAR integration.

## Tools

### `anomali_threat_stream_add_tags_to_entities`

Add tags to entities in Anomali ThreatStream. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `tags` (str, required): Specify a comma-separated list of tags that need to be added to entities in Anomali ThreatStream.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_ping`

Test connectivity to the Anomali ThreatStream with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_get_related_entities`

Retrieve related entities based on the associations in Anomali ThreatStream. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold. Note: Maximum is 100.
*   `search_threat_bulletins` (Optional[bool], optional, default=None): If enabled, action will search among threat bulletins.
*   `search_actors` (Optional[bool], optional, default=None): If enabled, action will search among actors.
*   `search_attack_patterns` (Optional[bool], optional, default=None): If enabled, action will search among attack patterns.
*   `search_campaigns` (Optional[bool], optional, default=None): If enabled, action will search among campaigns.
*   `search_courses_of_action` (Optional[bool], optional, default=None): If enabled, action will search among courses of action.
*   `search_identities` (Optional[bool], optional, default=None): If enabled, action will search among identities.
*   `search_incidents` (Optional[bool], optional, default=None): If enabled, action will search among incidents.
*   `search_infrastructures` (Optional[bool], optional, default=None): If enabled, action will search among infrastructures.
*   `search_intrusion_sets` (Optional[bool], optional, default=None): If enabled, action will search among intrusion sets.
*   `search_malware` (Optional[bool], optional, default=None): If enabled, action will search among malware.
*   `search_signatures` (Optional[bool], optional, default=None): If enabled, action will search among signatures.
*   `search_tools` (Optional[bool], optional, default=None): If enabled, action will search among tools.
*   `search_tt_ps` (Optional[bool], optional, default=None): If enabled, action will search among TTPs.
*   `search_vulnerabilities` (Optional[bool], optional, default=None): If enabled, action will search among vulnerabilities.
*   `max_entities_to_return` (Optional[str], optional, default=None): Specify how many entities to return per entity type. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_report_as_false_positive`

Report entities in Anomali ThreatStream as false positive. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `reason` (str, required): Specify the reason why you want to mark entities as false positives.
*   `comment` (str, required): Specify additional information related to your decision regarding marking the entity as false positive.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_submit_observables`

Submit an observable to Anomali ThreatStream based on IP, URL, Hash, Email entities. Note: requires "Org admin", "Create Anomali Community Intel" and "Approve Intel" permissions. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `classification` (List[Any], required): Specify the classification of the observable.
*   `threat_type` (List[Any], required): Specify the threat type of the observables.
*   `source` (Optional[str], optional, default=None): Specify the intelligence source for the observable.
*   `expiration_date` (Optional[str], optional, default=None): Specify the expiration date in days for the observable. If nothing is specified here, action will create an observable that will never expire.
*   `trusted_circle_i_ds` (Optional[str], optional, default=None): Specify the comma-separated list of trusted circle ids. Observables will be shared with those trusted circles.
*   `tlp` (Optional[List[Any]], optional, default=None): Specify the TLP for your observables.
*   `confidence` (Optional[str], optional, default=None): Specify what should be the confidence for the observable. Note: this parameter will only work, if you create observables in your organization and requires 'Override System Confidence' to be enabled.
*   `override_system_confidence` (Optional[bool], optional, default=None): If enabled, created observables will have the confidence specified in the 'Confidence' parameter. Note: you can't share observables in trusted circles and publicly, when this parameter is enabled.
*   `anonymous_submission` (Optional[bool], optional, default=None): If enabled, action will make an anonymous submission.
*   `tags` (Optional[str], optional, default=None): Specify a comma-separated list of tags that you want to add to observable.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_get_related_associations`

Retrieve entity related associations from Anomali ThreatStream. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex).

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
*   `create_campaign_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available “Campaign” associations.
*   `create_actors_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available “Actor” associations.
*   `create_signature_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available “Signature” associations.
*   `create_vulnerability_entity` (Optional[bool], optional, default=None): If enabled, action will create an entity out of available “Vulnerability” associations.
*   `create_case_tag` (Optional[bool], optional, default=None): If enabled, action will create case tags based on the results.
*   `create_insight` (Optional[bool], optional, default=None): If enabled, action will create an insight base on the results.
*   `max_associations_to_return` (Optional[str], optional, default=None): Specify how many associations to return per type. Default: 5
*   `max_statistics_to_return` (Optional[str], optional, default=None): Specify how many top statistics results regarding IOCs to return. Note: action will at max process 1000 IOCs related to the association. If you provide "0", action will not try to fetch statistics information.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_remove_tags_from_entities`

Remove tags from entities in Anomali ThreatStream. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex).

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `tags` (str, required): Specify a comma-separated list of tags that need to be removed from entities in Anomali ThreatStream.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `anomali_threat_stream_enrich_entities`

Retrieve information about entities from Anomali ThreatStream. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Hostname, Domain.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `severity_threshold` (List[Any], required): Specify what should be the severity threshold for the entity, in order to mark it as suspicious. If multiple records are found for the same entity, action will take the highest severity out of all available records.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold for the entity, in order to mark it as suspicious. Note: Maximum is 100. If multiple records are found for the entity, action will take the average. Active records have priority.
*   `create_insight` (bool, required): If enabled, action will add an insight per processed entity.
*   `only_suspicious_entity_insight` (bool, required): If enabled, action will create insight only for entities that exceeded the "Severity Threshold" and "Confidence Threshold".
*   `ignore_false_positive_status` (Optional[bool], optional, default=None): If enabled, action will ignore the false positive status and mark the entity as suspicious based on the "Severity Threshold" and "Confidence Threshold". If disabled, action will never label false positive entities as suspicious, regardless, if they pass the "Severity Threshold" and "Confidence Threshold" conditions or not.
*   `add_threat_type_to_case` (Optional[bool], optional, default=None): If enabled, action will add threat types of the entity from all records as tags to the case. Example: apt
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
