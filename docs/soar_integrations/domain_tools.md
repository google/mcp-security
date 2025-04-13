# DomainTools Integration

## Overview

This integration allows interaction with the DomainTools API to perform various domain intelligence tasks, including WHOIS lookups, hosting history retrieval, domain risk assessment, reverse IP/email lookups, and searching for recently registered domains.

## Configuration

To configure this integration within the SOAR platform, you typically need the following DomainTools API details:

*   **API Username:** Your DomainTools API username.
*   **API Key:** Your DomainTools API key.
*   **API URL:** The base URL for the DomainTools API (usually `https://api.domaintools.com/`).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface.)*

## Actions

### Recent Domains

Search for new domains containing a particular word.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `string_query` (string, required): Search for new domains containing this particular word.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of recently registered domains matching the query.

### Get Hosting History

Get domain hosting history information, enrich and add CSV table.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the hosting history for the specified domain(s), often including a CSV attachment.

### Get Domain Risk

Enrich external domain entity with the domain risk score given by DomainTools data.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `threshold` (string, required): Mark entity as suspicious if the domain risk score passes the given threshold (e.g., `70`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the domain risk score and related information for the specified domain(s).

### Ping

Test Connectivity to DomainTools API.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Reverse Domain

Find IPs that point to a particular domain (Reverse DNS lookup).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the IP addresses associated with the specified domain(s).

### Get Domain Profile

Enrich external domain entity with DomainTools threat Intelligence data and return CSV output. Provides comprehensive profile information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and Hostname entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the domain profile information, often including a CSV attachment.

### Reverse Email

Find domains with an email address in their WhoIs record.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Email entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of domains associated with the specified email address(es).

### Reverse IP

Find domain names that share a particular IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of domains hosted on the specified IP address(es).

## Notes

*   Ensure the DomainTools integration is properly configured in the SOAR Marketplace tab with a valid API Username and API Key.
*   The API credentials require appropriate permissions and subscription level within DomainTools for the desired actions (e.g., Risk Score, Hosting History, Reverse Lookups).
*   Actions typically target Domain, Hostname, IP Address, or Email entities.
