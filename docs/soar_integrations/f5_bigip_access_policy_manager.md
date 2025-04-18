# F5 BIG-IP Access Policy Manager Integration

## Overview

This integration allows you to connect to F5 BIG-IP Access Policy Manager (APM) and perform actions such as listing active user sessions, disconnecting sessions based on various criteria, and testing connectivity.

## Configuration

The configuration for this integration (BIG-IP address, username, password) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Ping

Test connectivity to the F5 BIG-IP Access Policy Manager with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Active Sessions

The action will list all the currently active sessions in the F5 BIG-IP Access Policy Manager.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `limit` (string, optional): Specify the maximum number of entries you would like to get in the action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, including the list of active sessions.

### Disconnect Sessions

The action will disconnect the specified sessions from the F5 BIG-IP instance. Action can work using entities or using parameters, according to the Use Case Entities parameter’s value. Supported entities are Address and User Name. NOTE - Filters will be used with an OR logic, so that every session that even one of the parameters, or entities, will be matched in - will be disconnected.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `use_case_entities` (bool, optional): Specify whether the action should disconnect sessions using Address and Client IP entities found in the case, or work on the provided parameters only. NOTE - once checked, action will ignore all other parameters in the action.
*   `session_i_ds` (string, optional): Specify specific session IDs you would like to disconnect, in a comma separated list.
*   `logon_user_names` (string, optional): Specify Logon User Names you would like to disconnect sessions for, in a comma separated list, so only sessions for these Logon User Names will be disconnected.
*   `client_i_ps` (string, optional): Specify Client IPs you would like to disconnect the sessions for,in a comma separated list, so only sessions for these Client IPs will be disconnected.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on. Supports Address and User Name entities if `use_case_entities` is true.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution, indicating which sessions were disconnected.

## Notes

*   Ensure the F5 BIG-IP Access Policy Manager integration is properly configured in the SOAR Marketplace tab.
*   The `Disconnect Sessions` action uses OR logic for filtering when multiple criteria (Session IDs, User Names, Client IPs, or Entities) are provided.
