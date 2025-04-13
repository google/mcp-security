# FireEye EX Integration

## Overview

This integration allows you to connect to FireEye Email Security (EX) and perform actions related to quarantined emails and alert artifacts.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Release Quarantined Email

Releases a specific email from quarantine in FireEye EX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `queue_id` (string, required): The queue ID of the email to release.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Tests connectivity to the configured FireEye EX appliance using the parameters provided in the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Delete Quarantined Email

Deletes a specific email from quarantine in FireEye EX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `queue_id` (string, required): The queue ID of the email to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Download Alert Artifacts

Downloads artifacts associated with a specific alert from FireEye EX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `alert_uuid` (string, required): The UUID of the alert whose artifacts should be downloaded.
*   `download_path` (string, required): The absolute path on the SOAR server where the artifacts should be saved. If not specified, the file will not be saved to disk.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download action, potentially including paths to the downloaded files.

### Download Quarantined Email

Downloads a specific quarantined email from FireEye EX.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `queue_id` (string, required): The queue ID of the email to download.
*   `download_path` (string, required): The absolute path on the SOAR server where the email file should be saved. If not specified, the file will not be saved to disk.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the download action, potentially including the path to the downloaded email file.

### List Quarantined Emails

Lists emails currently held in quarantine in FireEye EX, based on specified filters.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `start_time` (string, optional): Filters emails created after this time (Format: YYYY-MM-DD'T'HH:MM:SS.SSS-HHMM). Defaults to the last 24 hours if no time range is specified.
*   `end_time` (string, optional): Filters emails created before this time (Format: YYYY-MM-DD'T'HH:MM:SS.SSS-HHMM). Defaults to now if no time range is specified.
*   `sender_filter` (string, optional): Filters emails by sender address.
*   `subject_filter` (string, optional): Filters emails by subject line.
*   `max_email_to_return` (string, optional): The maximum number of emails to return (Limit: 10000).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing a list of quarantined emails matching the criteria.

## Notes

*   Ensure the FireEye EX integration is properly configured in the SOAR Marketplace tab with valid credentials and appliance details.
*   Some actions rely on underlying scripts executed by the SOAR platform.
