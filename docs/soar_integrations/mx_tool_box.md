# MXToolBox Integration

## Overview

This integration allows you to connect to MXToolBox to perform various DNS and network lookups, including A record, reverse DNS, TCP port status, HTTPS/SSL checks, SPF records, MX records, blacklist checks, and external pings.

## Configuration

The configuration for this integration (API Key, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### A Record Lookup

A record lookup returns the IP address for a specific domain name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the A record lookup results, including IP addresses associated with the domain.

### Reverse DNS Lookup

Reverse DNS lookup returns domain name associated with specific IP.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the reverse DNS lookup results, including domain names associated with the IP.

### TCP Port Status

Check if specific TCP port is open for a given IP address or domain.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `port_number` (string, required): The port number to check.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the status of the specified TCP port (open/closed).

### Ping

Test Connectivity to MXToolBox.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### HTTPS Information Lookup

The HTTPS Lookup and SSL Certificate Checker will query a website URL and tell you if it responds securely with SSL encryption.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports URL entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing HTTPS and SSL certificate details for the URL.

### SPF Lookup

Sender Policy Framework (SPF) records allow domain owners to publish a list of IP addresses or subnets that are authorized to send email on their behalf. This action checks the SPF record for a given domain.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ip_address` (string, required): The IP address to look for (Note: This seems incorrect based on the description, likely should be Domain Name).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the SPF record details for the domain.

### MX Record Lookup

MX record lookup returns the mail server address for a specific Domain.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the MX record lookup results, including mail server addresses.

### Blacklist Check

Blacklist check returns if Domain or IP were blacklisted based on a threshold.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `blacklist_threshold` (string, required): The threshold of the blacklist count to determine whether a domain or IP is considered blacklisted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Domain and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing blacklist check results, indicating if the entity is blacklisted based on the threshold.

### Ping External IP

Ping external IP or Domain using ICMP protocol.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and Domain entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the ICMP ping results.

## Notes

*   Ensure the MXToolBox integration is properly configured in the SOAR Marketplace tab with a valid API Key.
*   Actions support different entity types (Domain, IP Address, URL). Refer to individual action descriptions.
*   The `SPF Lookup` action description mentions looking up by IP address, but SPF records are associated with domains. Clarification might be needed on its exact functionality or the parameter might be mislabeled.
