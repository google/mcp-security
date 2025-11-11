# SymantecEmailSecurityCloud SOAR Integration

## Overview
This document outlines the tools available in the Symantec Email Security.Cloud SOAR integration. These tools allow interaction with Symantec Email Security.Cloud for blocking entities and testing connectivity.

## Tools

### `symantec_email_security_cloud_block_entities`
Block entities in Symantec Email Security.Cloud. Supported entities: Hostname, IP address, URL, Filehash, Email Subject, Email Address (user entity that matches email regex). Note: only MD5 and SHA256 hashes are supported. All of the entities are treated as "sender IOCs" during blocking.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `description` (str, required): Specify a description that should be added to the blocked entities.
*   `remediation_action` (Optional[List[str]], optional, default=None): Specify the remediation action for the entities.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.

### `symantec_email_security_cloud_ping`
Test connectivity to the Symantec Email Security.Cloud with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**
*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default='All entities'): Defines the scope for the action.
