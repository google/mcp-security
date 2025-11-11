# SiemplifyThreatFuse SOAR Integration

## Overview

This integration provides tools to interact with Siemplify ThreatFuse, allowing users to enrich entities, retrieve related indicators (IPs, domains, hashes, emails, URLs), manage observables, and check connectivity within the Chronicle SOAR platform.

## Tools

### `siemplify_threat_fuse_get_related_i_ps`

Retrieve entity related IP addresses based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold. Note: Maximum is 100.
*   `search_observables` (bool, required): If enabled, action will search among observables.
*   `search_threat_bulletins` (bool, required): If enabled, action will search among threat bulletins.
*   `search_actors` (bool, required): If enabled, action will search among actors.
*   `search_attack_patterns` (bool, required): If enabled, action will search among attack patterns.
*   `search_campaigns` (bool, required): If enabled, action will search among campaigns.
*   `search_courses_of_action` (bool, required): If enabled, action will search among courses of action.
*   `search_identities` (bool, required): If enabled, action will search among identities.
*   `search_incidents` (bool, required): If enabled, action will search among incidents.
*   `search_infrastructures` (bool, required): If enabled, action will search among infrastructures.
*   `search_intrusion_sets` (bool, required): If enabled, action will search among intrusion sets.
*   `search_malware` (bool, required): If enabled, action will search among malware.
*   `search_signatures` (bool, required): If enabled, action will search among signatures.
*   `search_tools` (bool, required): If enabled, action will search among tools.
*   `search_tt_ps` (bool, required): If enabled, action will search among TTPs.
*   `search_vulnerabilities` (bool, required): If enabled, action will search among vulnerabilities.
*   `max_i_ps_to_return` (Optional[str], optional, default=None): Specify how many IPs to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_get_related_domains`

Retrieve entity related domains based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold. Note: Maximum is 100.
*   `search_threat_bulletins` (bool, required): If enabled, action will search among threat bulletins.
*   `search_actors` (bool, required): If enabled, action will search among actors.
*   `search_attack_patterns` (bool, required): If enabled, action will search among attack patterns.
*   `search_campaigns` (bool, required): If enabled, action will search among campaigns.
*   `search_courses_of_action` (bool, required): If enabled, action will search among courses of action.
*   `search_identities` (bool, required): If enabled, action will search among identities.
*   `search_incidents` (bool, required): If enabled, action will search among incidents.
*   `search_infrastructures` (bool, required): If enabled, action will search among infrastructures.
*   `search_intrusion_sets` (bool, required): If enabled, action will search among intrusion sets.
*   `search_malware` (bool, required): If enabled, action will search among malware.
*   `search_signatures` (bool, required): If enabled, action will search among signatures.
*   `search_tools` (bool, required): If enabled, action will search among tools.
*   `search_tt_ps` (bool, required): If enabled, action will search among TTPs.
*   `search_vulnerabilities` (bool, required): If enabled, action will search among vulnerabilities.
*   `max_domains_to_return` (Optional[str], optional, default=None): Specify how many domains to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_ping`

Test connectivity to the Siemplify ThreatFuse with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_submit_observables`

Submit an observable to Siemplify ThreatFuse based on IP, URL, Hash or User entities with Email regexes from Siemplify ThreatFuse. Note: requires 'Org admin', 'Create Anomali Community Intel' and 'Approve Intel' permissions.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `classification` (List[str], required): Specify the classification of the observable.
*   `threat_type` (List[str], required): Specify the threat type of the observables.
*   `source` (Optional[str], optional, default=None): Specify the intelligence source for the observable.
*   `expiration_date` (Optional[str], optional, default=None): Specify the expiration date in days for the observable. If nothing is specified here, action will create an observable that will never expire.
*   `trusted_circle_i_ds` (Optional[str], optional, default=None): Specify the comma-separated list of trusted circle ids. Observables will be shared with those trusted circles.
*   `tlp` (Optional[List[str]], optional, default=None): Specify the TLP for your observables.
*   `confidence` (Optional[str], optional, default=None): Specify what should be the confidence for the observable. Note: this parameter will only work, if you create observables in your organization and requires 'Override System Confidence' to be enabled.
*   `override_system_confidence` (Optional[bool], optional, default=None): If enabled, created observables will have the confidence specified in the 'Confidence' parameter. Note: you can't share observables in trusted circles and publicly, when this parameter is enabled.
*   `anonymous_submission` (Optional[bool], optional, default=None): If enabled, action will make an anonymous submission.
*   `tags` (Optional[str], optional, default=None): Specify a comma-separated list of tags that you want to add to observable.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_get_related_associations`

Retrieve entity related associations from Siemplify ThreatFuse. Configure the parameters below: choose the association types to return, specify Max Associations To Return. You can also choose to add retrieved associations as entities to the case.

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

### `siemplify_threat_fuse_enrich_entities`

Retrieve information about IPs, URLs, hashes or User entities with Email regexes from Siemplify ThreatFuse. If multiple records are found for the same entity, action will enrich using the latest record.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `severity_threshold` (List[str], required): Specify what should be the severity threshold for the entity, in order to mark it as suspicious. If multiple records are found for the same entity, action will take the highest severity out of all available records.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold for the entity, in order to mark it as suspicious. Note: Maximum is 100. If multiple records are found for the entity, action will take the average. Active records have priority.
*   `ignore_false_positive_status` (Optional[bool], optional, default=None): If enabled, action will ignore the false positive status and mark the entity as suspicious based on the "Severity Threshold" and "Confidence Threshold". If disabled, action will never label false positive entities as suspicious, regardless, if they pass the "Severity Threshold" and "Confidence Threshold" conditions or not.
*   `add_threat_type_to_case` (Optional[bool], optional, default=None): If enabled, action will add threat types of the entity from all records as tags to the case. Example: apt
*   `create_insight` (Optional[bool], optional, default=None): If enabled, action will add an insight per processed entity.
*   `only_suspicious_entity_insight` (Optional[bool], optional, default=None): If enabled, action will create insight only for entities that exceeded the "Severity Threshold" and "Confidence Threshold".
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_get_related_hashes`

Retrieve entity related hashes based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold. Note: Maximum is 100.
*   `search_threat_bulletins` (bool, required): If enabled, action will search among threat bulletins.
*   `search_actors` (bool, required): If enabled, action will search among actors.
*   `search_attack_patterns` (bool, required): If enabled, action will search among attack patterns.
*   `search_campaigns` (bool, required): If enabled, action will search among campaigns.
*   `search_courses_of_action` (bool, required): If enabled, action will search among courses of action.
*   `search_identities` (bool, required): If enabled, action will search among identities.
*   `search_incidents` (bool, required): If enabled, action will search among incidents.
*   `search_infrastructures` (bool, required): If enabled, action will search among infrastructures.
*   `search_intrusion_sets` (bool, required): If enabled, action will search among intrusion sets.
*   `search_malware` (bool, required): If enabled, action will search among malware.
*   `search_signatures` (bool, required): If enabled, action will search among signatures.
*   `search_tools` (bool, required): If enabled, action will search among tools.
*   `search_tt_ps` (bool, required): If enabled, action will search among TTPs.
*   `search_vulnerabilities` (bool, required): If enabled, action will search among vulnerabilities.
*   `max_hashes_to_return` (Optional[str], optional, default=None): Specify how many hashes to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_get_related_email_addresses`

Retrieve entity related email addresses based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold. Note: Maximum is 100.
*   `search_observables` (bool, required): If enabled, action will search among observables.
*   `search_threat_bulletins` (bool, required): If enabled, action will search among threat bulletins.
*   `search_actors` (bool, required): If enabled, action will search among actors.
*   `search_attack_patterns` (bool, required): If enabled, action will search among attack patterns.
*   `search_campaigns` (bool, required): If enabled, action will search among campaigns.
*   `search_courses_of_action` (bool, required): If enabled, action will search among courses of action.
*   `search_identities` (bool, required): If enabled, action will search among identities.
*   `search_incidents` (bool, required): If enabled, action will search among incidents.
*   `search_infrastructures` (bool, required): If enabled, action will search among infrastructures.
*   `search_intrusion_sets` (bool, required): If enabled, action will search among intrusion sets.
*   `search_malware` (bool, required): If enabled, action will search among malware.
*   `search_signatures` (bool, required): If enabled, action will search among signatures.
*   `search_tools` (bool, required): If enabled, action will search among tools.
*   `search_tt_ps` (bool, required): If enabled, action will search among TTPs.
*   `search_vulnerabilities` (bool, required): If enabled, action will search among vulnerabilities.
*   `max_email_addresses_to_return` (Optional[str], optional, default=None): Specify how many email addresses to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `siemplify_threat_fuse_get_related_ur_ls`

Retrieve entity related urls based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `confidence_threshold` (str, required): Specify what should be the confidence threshold. Note: Maximum is 100.
*   `search_threat_bulletins` (bool, required): If enabled, action will search among threat bulletins.
*   `search_actors` (bool, required): If enabled, action will search among actors.
*   `search_attack_patterns` (bool, required): If enabled, action will search among attack patterns.
*   `search_campaigns` (bool, required): If enabled, action will search among campaigns.
*   `search_courses_of_action` (bool, required): If enabled, action will search among courses of action.
*   `search_identities` (bool, required): If enabled, action will search among identities.
*   `search_incidents` (bool, required): If enabled, action will search among incidents.
*   `search_infrastructures` (bool, required): If enabled, action will search among infrastructures.
*   `search_intrusion_sets` (bool, required): If enabled, action will search among intrusion sets.
*   `search_malware` (bool, required): If enabled, action will search among malware.
*   `search_signatures` (bool, required): If enabled, action will search among signatures.
*   `search_tools` (bool, required): If enabled, action will search among tools.
*   `search_tt_ps` (bool, required): If enabled, action will search among TTPs.
*   `search_vulnerabilities` (bool, required): If enabled, action will search among vulnerabilities.
*   `max_ur_ls_to_return` (Optional[str], optional, default=None): Specify how many hashes to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
