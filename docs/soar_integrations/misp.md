# MISP Integration

## Overview

This integration allows you to connect to MISP (Malware Information Sharing Platform) to manage events, attributes, objects, sightings, and tags.

## Configuration

The configuration for this integration (MISP URL, API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Create network-connection Misp Object

Create a network-connection Object in MISP. Requires one of: Dst-port, Src-port, IP-Src, IP-Dst to be provided or “Use Entities“ parameter set to true.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to which you want to add network-connection objects.
*   `dst_port` (string, optional): Specify the destination port.
*   `src_port` (string, optional): Specify the source port.
*   `hostname_src` (string, optional): Specify the source hostname.
*   `hostname_dst` (string, optional): Specify the destination hostname.
*   `ip_src` (string, optional): Specify the source IP.
*   `ip_dst` (string, optional): Specify the destination IP.
*   `layer3_protocol` (string, optional): Specify the related layer 3 protocol.
*   `layer4_protocol` (string, optional): Specify the related layer 4 protocol.
*   `layer7_protocol` (string, optional): Specify the related layer 7 protocol.
*   `use_entities` (bool, optional): If enabled, uses IP Address entities to populate IP-Src/IP-Dst. Has priority over other parameters.
*   `ip_type` (List[Any], optional): Specify attribute type for IP entities (IP-Src or IP-Dst).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the object creation.

### List Event Objects

Retrieve information about available objects in MISP event.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify a comma-separated list of IDs and UUIDs of the events.
*   `max_objects_to_return` (string, optional): Specify how many objects to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of objects for the specified event(s).

### Unpublish Event

Unpublish an event, preventing it from being visible to shared groups.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to unpublish.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unpublish operation.

### Create Event

Create a new event in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_name` (string, required): Specify the name for the new event.
*   `distribution` (string, optional): Specify the distribution (0-Organisation, 1-Community, 2-Connected, 3-All).
*   `threat_level` (string, optional): Specify the threat level (1-High, 2-Medium, 3-Low, 4-Undefined).
*   `analysis` (string, optional): Specify the analysis status (0-Initial, 1-Ongoing, 2-Completed).
*   `publish` (bool, optional): If enabled, publish the event to the community.
*   `comment` (string, optional): Specify additional comments related to the event.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the event creation, likely including the new event ID.

### Remove Tag from an Attribute

Remove tags from attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tag_name` (string, required): Comma-separated list of tags to remove.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event" or Object UUID is provided).
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `object_uuid` (string, optional): UUID of the object containing the attribute.
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the tag removal operation.

### Ping

Test Connectivity to MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Set IDS Flag for an Attribute

Set IDS flag for attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event").
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the flag setting operation.

### Get Event Details

Retrieve details about events in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Comma-separated list of IDs or UUIDs of the events.
*   `return_attributes_info` (bool, optional): If enabled, creates a case wall table for all event attributes.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details of the specified event(s).

### Add Tag to an Event

Add tags to event in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event.
*   `tag_name` (string, required): Comma-separated list of tags to add.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the tag addition operation.

### Remove Tag from an Event

Remove tags from event in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event.
*   `tag_name` (string, required): Comma-separated list of tags to remove.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the tag removal operation.

### Delete an Event

Delete event in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Create IP-Port Misp Object

Create an IP-Port Object in MISP. Requires one of: Dst-port, Src-port, Domain, HOSTNAME, IP-Src, IP-Dst to be provided or “Use Entities“ parameter set to true.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to add the object to.
*   `dst_port` (string, optional): Specify the destination port.
*   `src_port` (string, optional): Specify the source port.
*   `domain` (string, optional): Specify the domain.
*   `hostname` (string, optional): Specify the hostname.
*   `ip_src` (string, optional): Specify the source IP.
*   `ip_dst` (string, optional): Specify the destination IP.
*   `use_entities` (bool, optional): If enabled, uses IP Address entities. Has priority over other parameters.
*   `ip_type` (List[Any], optional): Specify attribute type for IP entities (IP-Src or IP-Dst).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the object creation.

### Create Virustotal-Report Object

Create a Virustotal-Report Object in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to add the object to.
*   `permalink` (string, required): Specify the link to the VirusTotal report.
*   `comment` (string, optional): Specify the comment.
*   `detection_ratio` (string, optional): Specify the detection ratio.
*   `community_score` (string, optional): Specify the community score.
*   `first_submission` (string, optional): Specify first submission date (Format: YYYY-MM-DDTHH:MM:SSZ).
*   `last_submission` (string, optional): Specify last submission date (Format: YYYY-MM-DDTHH:MM:SSZ).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the object creation.

### Add Sighting to an Attribute

Add a sighting to attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `sightings_type` (List[Any], required): Specify the type of the Sighting.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event").
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `source` (string, optional): Specify the source for the sighting (e.g., SIEM, SOAR).
*   `date_time` (string, optional): Specify the date time for the sighting (Format: YYYY-MM-DD HH:MM:SS).
*   `object_uuid` (string, optional): UUID of the object containing the attribute.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the sighting addition.

### Enrich Entities

Enrich entities based on the attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `number_of_attributes_to_return` (string, required): Specify how many attributes to return for entities.
*   `filtering_condition` (List[Any], required): Specify filtering condition ("First" or "Last").
*   `create_insights` (bool, optional): If enabled, generates an insight for every fully processed entity.
*   `threat_level_threshold` (List[Any], optional): Specify threat level threshold. Marks entity as suspicious if related event matches or exceeds threshold.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment information for the specified entities.

### Create Url Misp Object

Create a URL Object in MISP. Requires “URL” to be provided or “Use Entities“ parameter set to true.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to add URL objects to.
*   `url` (string, optional): Specify the URL.
*   `port` (string, optional): Specify the port.
*   `first_seen` (string, optional): Specify when the URL was first seen (Format: YYYY-MM-DDTHH:MM:SSZ).
*   `last_seen` (string, optional): Specify when the URL was last seen (Format: YYYY-MM-DDTHH:MM:SSZ).
*   `domain` (string, optional): Specify the domain.
*   `text` (string, optional): Specify additional text.
*   `ip` (string, optional): Specify the IP address.
*   `host` (string, optional): Specify the Host.
*   `use_entities` (bool, optional): If enabled, uses URL entities. Has priority over other parameters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the object creation.

### Download File

Download files related to event in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, optional): Specify the ID or UUID of the event to download files from.
*   `download_folder_path` (string, optional): Absolute path to the folder to store files. If empty, creates attachments instead. JSON result only available if path provided.
*   `overwrite` (bool, optional): If enabled, overwrites existing files.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports FileHash entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download operation, potentially including file paths or attachment info.

### Unset IDS Flag for an Attribute

Unset IDS flag for attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event").
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the flag unset operation.

### Upload File

Upload a file to a MISP event.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to upload the file to.
*   `file_path` (string, required): Comma-separated list of absolute filepaths to upload.
*   `for_intrusion_detection_system` (bool, required): If enabled, uploaded file will be used for IDS.
*   `category` (string, optional): Specify the category for the uploaded file.
*   `distribution` (string, optional): Specify the distribution (0-Organisation, 1-Community, 2-Connected, 3-All, 5-Inherit).
*   `comment` (string, optional): Specify additional comments.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the upload operation.

### Add Attribute

Add attributes based on entities to the event in MISP. Supported hashes: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to add attributes to.
*   `for_intrusion_detection_system` (bool, required): If enabled, attribute will be labeled eligible for IDS signature creation.
*   `category` (string, optional): Specify the category for attributes.
*   `distribution` (string, optional): Specify the distribution (0-Organisation, 1-Community, 2-Connected, 3-All, 5-Inherit).
*   `comment` (string, optional): Specify comment related to attribute.
*   `fallback_ip_type` (List[Any], optional): Specify fallback attribute type for IP address entity.
*   `fallback_email_type` (List[Any], optional): Specify fallback attribute type for email address entity.
*   `extract_domain` (bool, optional): If enabled, extracts domain out of URL entity.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports various entity types (IP, Hash, URL, Email, Domain).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the attribute addition.

### Add Tag to an Attribute

Add tags to attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `tag_name` (string, required): Comma-separated list of tags to add.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event" or Object UUID is provided).
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `object_uuid` (string, optional): UUID of the object containing the attribute.
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the tag addition operation.

### Create File Misp Object

Create a File Object in MISP. Requires one of: FILENAME, MD5, SHA1, SHA256, SSDEEP to be provided or “Use Entities“ parameter set to true.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to add file objects to.
*   `filename` (string, optional): Specify the name of the file.
*   `md5` (string, optional): Specify the MD5 hash.
*   `sha1` (string, optional): Specify the SHA1 hash.
*   `sha256` (string, optional): Specify the SHA256 hash.
*   `ssdeep` (string, optional): Specify the ssdeep hash (Format: size:hash:hash).
*   `use_entities` (bool, optional): If enabled, uses File name and Hash entities. Has priority over other parameters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the object creation.

### Get Related Events

Retrieve information about events that are related to entities in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `events_limit` (string, optional): Specify max amount of events to fetch. If empty, fetches all.
*   `mark_as_suspicious` (bool, optional): If enabled, marks entity as suspicious if at least one related event exists.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports various entity types.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing related event information for the entities.

### Publish Event

Publish an event, making it visible to the selected sharing group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `event_id` (string, required): Specify the ID or UUID of the event to publish.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the publish operation.

### List Sightings of an Attribute

List available sightings for attributes in MISP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event").
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of sightings for the specified attributes.

### Delete an Attribute

Delete attributes in MISP. Supported hashes: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `attribute_name` (string, optional): Comma-separated list of attribute identifiers (values).
*   `event_id` (string, optional): Event ID/UUID to search within (required if Attribute Search is "Provided Event" or Object UUID is provided).
*   `category` (string, optional): Comma-separated list of categories to filter attributes.
*   `type` (string, optional): Comma-separated list of attribute types to filter attributes.
*   `object_uuid` (string, optional): UUID of the object containing the attribute.
*   `attribute_uuid` (string, optional): Comma-separated list of attribute UUIDs. Takes priority over Attribute Name.
*   `attribute_search` (List[Any], optional): Where to search for attributes ("Provided Event" or "All Events").
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

## Notes

*   Ensure the MISP integration is properly configured in the SOAR Marketplace tab.
*   Many actions allow specifying targets via Event ID, Attribute Name/UUID, or Object UUID. Pay attention to parameter priorities (UUID usually takes precedence over Name/Value).
*   Attribute search scope can be limited to a specific event or encompass all events.
*   Date/Time parameters generally expect ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) or YYYY-MM-DD HH:MM:SS depending on the action.
*   Supported hash types for attribute addition include MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.
