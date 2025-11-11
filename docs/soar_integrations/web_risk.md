# Google Web Risk Integration

This document describes the available tools for the Google Web Risk integration within the SecOps SOAR MCP Server. Web Risk allows applications to check URLs against Google's constantly updated lists of unsafe web resources.

## Configuration

Ensure the Web Risk integration is configured in the SOAR platform. This typically involves enabling the Web Risk API in your Google Cloud project and ensuring the SOAR service account has the necessary permissions.

## Available Tools

### web_risk_ping
- **Description:** Test connectivity to the Google Web Risk service using the configured project and credentials.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### web_risk_submit_entities
- **Description:** Submit URL entities to Web Risk for analysis to report potentially unsafe URLs. This action runs asynchronously.
- **Supported Entities:** URL
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `abuse_type` (List[str], optional): The type of abuse associated with the submission (e.g., ["MALWARE"], ["SOCIAL_ENGINEERING"]). See Web Risk API docs for `AbuseType`. Defaults to None.
    - `confidence_level` (List[str], optional): The confidence level of the submission (e.g., ["HIGH"], ["LOW"]). See Web Risk API docs for `ConfidenceLevel`. Defaults to None.
    - `justification` (List[str], optional): The justification for the submission (e.g., ["PHISHING_SITE"], ["MALWARE_SITE"]). See Web Risk API docs for `JustificationLabel`. Defaults to None.
    - `comment` (str, optional): A comment explaining the submission justification. Defaults to None.
    - `region_code` (str, optional): Comma-separated list of CLDR region codes associated with the submission. Defaults to None.
    - `platform` (List[str], optional): The platform type where the submission was detected (e.g., ["WINDOWS"], ["ANDROID"]). Defaults to None.
    - `skip_waiting` (bool, optional): If enabled, initiate the submission and don't wait for completion. Defaults to None (waits).
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the URL(s) to submit. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the submission initiation or completion.

### web_risk_enrich_entities
- **Description:** Enrich URL entities by checking them against Google Web Risk lists to determine if they are known threats.
- **Supported Entities:** URL
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Should contain the URL(s) to check. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the Web Risk analysis results for the submitted URLs, indicating threat types found (e.g., MALWARE, SOCIAL_ENGINEERING).
