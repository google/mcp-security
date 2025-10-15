# UrlScanIo SOAR Integration

## Overview

This document outlines the tools available for the urlscan.io integration within the SOAR platform. These tools allow interaction with the urlscan.io API for submitting URLs for scanning, searching existing scans, and retrieving scan details.

## Tools

### `url_scan_io_search_for_scans`

Search for urlscan.io existing scans by attributes such as domains, IPs, Autonomous System (AS) numbers, hashes, etc. The action will find public scans performed by anyone as well as unlisted and private scans performed by you or your teams.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `max_scans` (str, optional, default=None): Number of scans to return per entity. Default: 100, Max: 10000 (depending on subscription).
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `url_scan_io_url_check`

Submit a URL to be scanned and get the scan details.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `visibility` (List[str], optional, default=None): Scans on urlscan.io have one of three visibility levels, make sure to use the appropriate level for your submission.
*   `threshold` (str, optional, default=None): Mark entity as suspicious if the score of verdicts is equal or above the given threshold. Default is 0, in this case, we consider every scanned url as suspicious.
*   `create_insight` (bool, optional, default=None): If enabled, action will create an insight containing information about entities.
*   `only_suspicious_insight` (bool, optional, default=None): If enabled, action will only create insight for suspicious entities. Note: "Create Insight" parameter needs to be enabled.
*   `add_screenshot_to_insight` (bool, optional, default=None): If enabled, action will add a screenshot of the website to the insight, if it’s available.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `url_scan_io_ping`

Test Connectivity.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `url_scan_io_get_scan_full_details`

Get Scan Full Details by scan ID.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `scan_id` (str, required): Get scan report using the scan ID. Comma separated values.
*   `target_entities` (List[TargetEntity], optional, default=None): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
