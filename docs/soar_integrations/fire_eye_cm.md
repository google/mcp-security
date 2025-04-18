# FireEye CM Integration

## Overview

This integration allows you to connect to FireEye Central Management (CM) and perform actions related to alerts, IOC feeds, quarantined emails (requires FireEye EX), and custom rules.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Delete IOC Feed

Deletes an existing Indicator of Compromise (IOC) feed from FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `feed_name` (string, required): The name of the IOC feed to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Release Quarantined Email

Releases a specific email from quarantine. This action requires a FireEye EX appliance connected to the FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `queue_id` (string, required): The queue ID of the email to release.
*   `sensor_name` (string, optional): The name of the sensor (FireEye EX appliance) where the email is quarantined. If not specified, the action attempts to find the sensor automatically.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Acknowledge Alert

Acknowledges a specific alert in FireEye CM, typically indicating it has been reviewed.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_uuid` (string, required): The UUID of the alert to acknowledge.
*   `annotation` (string, required): An explanation or comment for acknowledging the alert.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Tests connectivity to the configured FireEye CM appliance using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Delete Quarantined Email

Deletes a specific email from quarantine. This action requires a FireEye EX appliance connected to the FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `queue_id` (string, required): The queue ID of the email to delete.
*   `sensor_name` (string, optional): The name of the sensor (FireEye EX appliance) where the email is quarantined. If not specified, the action attempts to find the sensor automatically.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add Rule To Custom Rules File

Adds a new rule definition to an existing custom rules file on a specified sensor (or automatically detected sensor).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `rule` (string, required): The rule definition to add.
*   `sensor_name` (string, optional): The name of the sensor where the custom rules file resides. If not specified, the action attempts to find the sensor automatically.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add IOC Feed

Creates a new IOC feed in FireEye CM based on provided entities (Hashes, Domains, IPs, URLs).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `action` (List[Any], required): The action to associate with the IOC feed (e.g., "alert", "block").
*   `extract_domain` (boolean, required): If enabled, extracts the domain from URL entities to create domain IOCs.
*   `comment` (string, optional): An optional comment for the IOC feed.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Entities provide the IOC values.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Download Alert Artifacts

Downloads artifacts associated with a specific alert from FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_uuid` (string, required): The UUID of the alert whose artifacts should be downloaded.
*   `download_folder_path` (string, required): The absolute path on the SOAR server where the artifacts should be saved.
*   `overwrite` (boolean, required): If enabled, overwrites existing files with the same name in the download path.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download action, potentially including paths to the downloaded files.

### List IOC Feeds

Lists the available IOC feeds configured in FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_ioc_feeds_to_return` (string, optional): The maximum number of IOC feeds to return. Defaults to 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing a list of IOC feeds and their details.

### Download Custom Rules File

Downloads the custom rules file from a specified sensor (or automatically detected sensor).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `download_folder_path` (string, required): The absolute path on the SOAR server where the rules file should be saved.
*   `overwrite` (boolean, required): If enabled, overwrites an existing file with the same name in the download path.
*   `sensor_name` (string, optional): The name of the sensor from which to download the rules file. If not specified, the action attempts to find the sensor automatically.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download action, potentially including the path to the downloaded file.

### Download Quarantined Email

Downloads a specific quarantined email. This action requires a FireEye EX appliance connected to the FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `queue_id` (string, required): The queue ID of the email to download.
*   `download_folder_path` (string, required): The absolute path on the SOAR server where the email file should be saved.
*   `overwrite` (boolean, required): If enabled, overwrites an existing file with the same name in the download path.
*   `sensor_name` (string, optional): The name of the sensor (FireEye EX appliance) where the email is quarantined. If not specified, the action attempts to find the sensor automatically.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download action, potentially including the path to the downloaded email file.

### List Quarantined Emails

Lists emails currently held in quarantine, based on specified filters. Requires FireEye EX connected to FireEye CM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `start_time` (string, optional): Filters emails created after this time (Format: YYYY-MM-DD'T'HH:MM:SS.SSS-HHMM). Defaults to 24 hours ago if no time range is specified.
*   `end_time` (string, optional): Filters emails created before this time (Format: YYYY-MM-DD'T'HH:MM:SS.SSS-HHMM). Defaults to now if no time range is specified.
*   `sender_filter` (string, optional): Filters emails by sender address.
*   `subject_filter` (string, optional): Filters emails by subject line.
*   `max_emails_to_return` (string, optional): The maximum number of emails to return (Limit: 10000).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing a list of quarantined emails matching the criteria.

## Notes

*   Actions involving quarantined emails (`Release Quarantined Email`, `Delete Quarantined Email`, `Download Quarantined Email`, `List Quarantined Emails`) require a FireEye EX appliance to be connected and managed by the FireEye CM instance.
*   Ensure the FireEye CM integration is properly configured in the SOAR Marketplace tab.
*   Some actions rely on underlying scripts executed by the SOAR platform.
