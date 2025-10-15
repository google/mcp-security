# ThreatQ SOAR Integration

## Overview
This document outlines the tools available in the ThreatQ integration for Chronicle SOAR.

## Tools

### `threat_q_enrich_email`
Enrich an email address using ThreatQ information.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `score_threshold` (Optional[str], optional, default=None): Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.
*   `show_sources` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related sources.
*   `show_comments` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related comments.
*   `show_attributes` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related attributes.
*   `mark_whitelisted_entities_as_suspicious` (Optional[bool], optional, default=None): If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_add_source`
Action adds a source to the object.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `object_type` (List[str], required): Specify to which object type source should be added.
*   `object_identifier` (str, required): Specify identifier of the object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.
*   `source_name` (str, required): Specify the name of the source.
*   `indicator_type` (Optional[List[str]], optional, default=None): Specify the type of the indicator. This parameter is only used, if Source Object Type is Indicator.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_enrich_hash`
Enrich a Hash using ThreatQ information.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `score_threshold` (Optional[str], optional, default=None): Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.
*   `show_sources` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related sources.
*   `show_comments` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related comments.
*   `show_attributes` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related attributes.
*   `mark_whitelisted_entities_as_suspicious` (Optional[bool], optional, default=None): If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_get_indicator_details`
Search for entities in ThreatQ and get detailed information.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_enrich_cve`
Enrich a CVE using ThreatQ information.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `score_threshold` (Optional[str], optional, default=None): Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.
*   `show_sources` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related sources.
*   `show_comments` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related comments.
*   `show_attributes` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related attributes.
*   `mark_whitelisted_entities_as_suspicious` (Optional[bool], optional, default=None): If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_update_indicator_status`
Action updates indicator status in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `status` (List[str], required): Specify the new status of the indicator.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_create_event`
Create an event in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `event_type` (List[str], required): Specify the type of the event.
*   `title` (str, required): Specify the title of the event.
*   `happened_at` (Optional[str], optional, default=None): Specify when the event happened. If nothing is entered in this field, action will use current time. Format: YYYY-MM-DD hh:mm:ss
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_link_entities`
Action links all of the entities in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_list_related_objects`
Action lists related objects in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `source_object_type` (List[str], required): Specify the type of the source object.
*   `source_object_identifier` (str, required): Specify identifier of the source object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.
*   `related_object_type` (List[str], required): Specify the type of the related object that needs to be returned.
*   `source_indicator_type` (Optional[List[str]], optional, default=None): Specify the type of the source indicator. This parameter is only used, if Source Object Type is Indicator.
*   `max_related_objects_to_return` (Optional[str], optional, default=None): Specify how many related objects to return.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_list_entity_related_objects`
Action lists related objects for entities in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `related_object_type` (List[str], required): Specify the type of the related object that needs to be returned.
*   `max_related_objects_to_return` (Optional[str], optional, default=None): Specify how many related objects to return. Maximum is 1000. This is a ThreatQ limitation.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_enrich_ip`
Enrich an IP using ThreatQ information.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `score_threshold` (Optional[str], optional, default=None): Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.
*   `show_sources` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related sources.
*   `show_comments` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related comments.
*   `show_attributes` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related attributes.
*   `mark_whitelisted_entities_as_suspicious` (Optional[bool], optional, default=None): If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_create_adversary`
Create an adversary in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_ping`
Test Connectivity.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_list_events`
List events from ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `additional_fields` (Optional[str], optional, default=None): Specify what additional fields should be included in the response. Possible values: adversaries, attachments, attributes, comments, events, indicators, signatures, sources, spearphish, tags, type, watchlist.
*   `sort_field` (Optional[List[str]], optional, default=None): Specify what field should be used for sorting events.
*   `sort_direction` (Optional[List[str]], optional, default=None): Specify the sorting direction.
*   `max_events_to_return` (Optional[str], optional, default=None): Specify how many events to return.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_update_indicator_score`
Action updates indicator score in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `score` (List[str], required): Specify the new score of the indicator.
*   `score_validation` (List[str], required): Specify what kind of score validation should be used. If “ Highest Score” is specified, action will compare current values and update the indicator’s score only, if the specified score is higher than current generated and manual score. If “Force Update” is specified, action will update the indicator's score without comparing current values.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_link_entities_to_object`
Action links entities to a specific object in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `object_type` (List[str], required): Specify the type of the object to which you want to link entities.
*   `object_identifier` (str, required): Specify identifier of the object to which you want to link entities. For example, it can be an MD5 hash, title of the event, name of the adversary etc.
*   `indicator_type` (Optional[List[str]], optional, default=None): Specify the type of the indicator to which you want to link entities. This parameter is only used, if Source Object Type is “Indicator”.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_add_attribute`
Action adds an attribute to the object.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `object_type` (List[str], required): Specify to which object type attribute should be added.
*   `object_identifier` (str, required): Specify identifier of the object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.
*   `attribute_name` (str, required): Specify the name of the attribute.
*   `attribute_value` (str, required): Specify the value of the attribute.
*   `indicator_type` (Optional[List[str]], optional, default=None): Specify the type of the indicator. This parameter is only used, if Source Object Type is Indicator.
*   `attribute_source` (Optional[str], optional, default=None): Specify the source of the attribute.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_create_object`
Create an object in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `object_type` (List[str], required): Specify the type of the object to create.
*   `value` (str, required): Specify the value of the new object.
*   `description` (Optional[str], optional, default=None): Specify description of the new object.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_get_malware_details`
Action returns information about malware based on entities from ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `additional_information` (Optional[str], optional, default=None): Specify what additional fields should be included in the response. Possible values: adversaries, attackPattern, campaign, courseOfAction, attachments, attributes, comments, events, indicators, signatures, sources, status, tags, type, watchlist, exploitTarget, identity, incident, intrusionSet, malware, report, tool, ttp, vulnerability, tasks
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_create_indicator`
Create an indicator in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `indicator_type` (List[str], required): Specify the type of the new indicator.
*   `status` (List[str], required): Specify the status of the new indicator.
*   `description` (Optional[str], optional, default=None): Specify description of the new indicator.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_link_objects`
Action links two objects in ThreatQ.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `source_object_type` (List[str], required): Specify the type of the source object.
*   `source_object_identifier` (str, required): Specify identifier of the source object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.
*   `destination_object_type` (List[str], required): Specify the type of the destination object.
*   `destination_object_identifier` (str, required): Specify identifier of the destination object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.
*   `source_indicator_type` (Optional[List[str]], optional, default=None): Specify the type of the source indicator. This parameter is only used, if Source Object Type is Indicator.
*   `destination_indicator_type` (Optional[List[str]], optional, default=None): Specify the type of the destination indicator. This parameter is only used, if Destination Object Type is Indicator.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `threat_q_enrich_url`
Enrich an URL using ThreatQ information.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `score_threshold` (Optional[str], optional, default=None): Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.
*   `show_sources` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related sources.
*   `show_comments` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related comments.
*   `show_attributes` (Optional[bool], optional, default=None): If enabled, action will return an additional table with related attributes.
*   `mark_whitelisted_entities_as_suspicious` (Optional[bool], optional, default=None): If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.
*   `target_entities` (List[TargetEntity], optional, default=factory): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
