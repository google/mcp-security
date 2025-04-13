# Cisco ISE Integration

## Overview

This integration allows you to connect to Cisco Identity Services Engine (ISE) to manage endpoints and sessions. Actions include quarantining/unquarantining endpoints by MAC address, terminating sessions, updating endpoint details, listing endpoint identity groups, enriching endpoints, and testing connectivity.

## Configuration

To configure this integration within the SOAR platform, you typically need the following Cisco ISE details:

*   **Server Address:** The IP address or hostname of your Cisco ISE Primary Administration Node (PAN).
*   **ERS Username:** The username for an ERS (External RESTful Services) enabled administrator account.
*   **ERS Password:** The password for the ERS administrator account.
*   **MnT Username:** The username for a Monitoring (MnT) API enabled administrator account (can be the same as ERS user).
*   **MnT Password:** The password for the MnT administrator account.
*   **(Optional) Verify SSL:** Whether to verify the ISE server's SSL certificate.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the user accounts have the necessary permissions for ERS and MnT API operations.)*

## Actions

### Unquarantine Address

Unquarantine endpoint by MAC address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports MAC Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the unquarantine operation.

### Terminate Session

Session disconnect via an API call.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `node_server_name` (string, required): ISE node server name (e.g., `ciscoISE`).
*   `calling_station_id` (string, required): The ID value of the calling station (often the MAC address, e.g., `1`).
*   `terminate_type` (string, optional): Terminate Type value (integer 0-2). 0=DYNAMIC_AUTHZ_PORT_DEFAULT, 1=DYNAMIC_AUTHZ_PORT_BOUNCE, 2=DYNAMIC_AUTHZ_PORT_SHUTDOWN.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the session termination attempt.

### Update Endpoint

Update endpoint object attributes.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `description` (string, optional): Endpoint's description.
*   `group_id` (string, optional): Endpoint's Identity Group ID to update.
*   `portal_user` (string, optional): Endpoint's property to update.
*   `identity_store` (string, optional): Endpoint's property to update.
*   `identity_store_id` (string, optional): Endpoint's property to update.
*   `custom_attributes` (string, optional): JSON object for custom attributes `{'param':'val'}`.
*   `mdm_server_name` (string, optional): MDM Server Name.
*   `mdm_reachable` (string, optional): MDM Reachable status (e.g., `true` or `false`).
*   `mdm_enrolled` (string, optional): MDM Enrolled status (e.g., `true` or `false`).
*   `mdm_compliance_status` (string, optional): MDM Compliance Status (e.g., `true` or `false`).
*   `mdm_os` (string, optional): MDM OS.
*   `mdm_manufacturer` (string, optional): MDM Manufacturer.
*   `mdm_model` (string, optional): MDM Model.
*   `mdm_encrypted` (string, optional): MDM Encrypted status (e.g., `true` or `false`).
*   `mdm_pinlock` (string, optional): MDM Pinlock status (e.g., `true` or `false`).
*   `mdm_jail_broken` (string, optional): MDM Jail Broken status (e.g., `true` or `false`).
*   `mdm_imei` (string, optional): MDM IMEI.
*   `mdm_phone_number` (string, optional): MDM Phone Number.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Requires endpoint identifier (e.g., MAC Address).
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the endpoint update operation.

### List Endpoint Identity Group

List available endpoint identity groups in Cisco ISE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_key` (List[Any], optional): Specify the key to filter groups by (e.g., `name`, `description`).
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains).
*   `filter_value` (string, optional): Specify the value to filter by.
*   `max_records_to_return` (string, optional): Specify how many records to return. Default: 100. Maximum: 100.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of endpoint identity groups matching the criteria.

### Quarantine Address

Quarantine endpoint by MAC address by assigning it to a specific policy/group.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `policy_name` (string, required): Policy name (or Endpoint Identity Group name) to assign the endpoint to for quarantine.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports MAC Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the quarantine operation.

### Enrich Endpoint

Enrich endpoint by data from Cisco ISE based on MAC address or IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports MAC Address and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing enrichment data for the specified endpoint(s).

### Ping

Check connectivity to Cisco ISE.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Get Endpoints

Get requested endpoint data from endpoints monitored by Cisco ISE based on MAC address or IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports MAC Address and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing detailed information about the specified endpoint(s).

### Add Endpoint To Endpoint Identity Group

Add endpoint to endpoint identity group in Cisco ISE. Supported entity types: IP Address, MAC Address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `endpoint_identity_group_name` (string, required): Specify the name of the endpoint identity group to which you want to add the endpoint.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports IP Address and MAC Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Sessions

Get a list of active sessions based on endpoint MAC address or IP address.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports MAC Address and IP Address entities.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of active sessions for the specified endpoint(s).

## Notes

*   Ensure the Cisco ISE integration is properly configured in the SOAR Marketplace tab with the correct Server Address and credentials for both ERS and MnT APIs.
*   The user accounts used require appropriate permissions within Cisco ISE.
*   Actions targeting endpoints often use the MAC address as the primary identifier.
*   Session termination requires the `calling_station_id` (often the MAC address) and the name of the ISE node that handled the session.
