# BMC Helix Remedyforce Integration

## Overview

This integration allows you to connect to BMC Helix Remedyforce (built on the Salesforce platform) to manage records (e.g., Incidents, Service Requests). Actions include creating, updating, deleting, and retrieving records, listing record types, executing SOQL queries, and handling OAuth authentication.

## Configuration

To configure this integration within the SOAR platform, you typically need the following BMC Helix Remedyforce / Salesforce details:

*   **Instance URL:** The URL of your Salesforce/Remedyforce instance (e.g., `https://yourinstance.salesforce.com` or `https://yourinstance.remedyforce.com`).
*   **Client ID:** The Consumer Key from your Salesforce Connected App setup for API integration.
*   **Client Secret:** The Consumer Secret from your Salesforce Connected App.
*   **Username:** The username of the Salesforce/Remedyforce integration user.
*   **Password:** The password for the integration user.
*   **Security Token:** The Salesforce security token for the integration user (often required for API logins unless IP restrictions are configured).
*   **(Optional) Refresh Token:** For OAuth authentication, a refresh token might be used. Use the `Get OAuth Refresh Token` action to generate this if needed.

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the Connected App and integration user have the necessary permissions to perform the desired actions within Remedyforce.)*

## Actions

### Update Record

Update record in BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record that needs to be updated (e.g., `Incident`, `ServiceRequest__c`). Use "List Record Types" action if unsure.
*   `record_id` (string, required): Specify the ID of the record that needs to be updated.
*   `fields_to_update` (string, required): Specify a JSON object containing the fields and values to update (e.g., `{"Status__c": "Closed", "Description": "Updated description"}`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the update operation.

### Get Record Details

Get detailed information about the record from BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record (e.g., `Incident`, `ServiceRequest__c`).
*   `record_i_ds` (string, required): Specify the comma-separated IDs of records for which you want to return details.
*   `fields_to_return` (string, optional): Specify what fields to return (comma-separated). If empty, returns all fields. If specified fields are not found, the action fails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details for the specified record(s).

### List Record Types

List available record types from BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `filter_value` (string, optional): Specify a value to filter record types by (e.g., "Incident").
*   `max_record_types_to_return` (string, optional): Specify how many record types to return. Default: 50.
*   `filter_logic` (List[Any], optional): Specify filter logic (Equals/Contains).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the list of available record types.

### Get OAuth Refresh Token

Generate the refresh token that is needed for the integration configuration. Authorization code can be generated using "Get OAuth Authorization Code". Please refer to the documentation portal for more information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `redirect_url` (string, required): Specify the redirect URL that was used when the "Connector App" was created.
*   `authorization_code` (string, required): Specify the authorization code from action "Get OAuth Authorization Code".
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the refresh token and related details.

### Ping

Test connectivity to the BMC Helix Remedyforce with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Execute Simple Query

Execute a SOQL query based on parameters in BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify what record type should be queried (e.g., `Incident`, `ServiceRequest__c`).
*   `where_filter` (string, optional): Specify the WHERE filter for the query (without the `WHERE` keyword).
*   `time_frame` (List[Any], optional): Specify a time frame (e.g., Last 7 Days, Custom). If "Custom", `start_time` is required.
*   `start_time` (string, optional): Start time (ISO 8601). Mandatory if `time_frame` is "Custom".
*   `end_time` (string, optional): End time (ISO 8601). Uses current time if `time_frame` is "Custom" and this is empty.
*   `fields_to_return` (string, optional): Specify fields to return (comma-separated). If empty, returns all fields.
*   `sort_field` (string, optional): Specify the field to sort by.
*   `max_results_to_return` (string, optional): Specify how many results to return. Default: 50. Maximum: 200.
*   `sort_order` (List[Any], optional): Specify the sort order (Ascending/Descending).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the query results.

### Delete Record

Delete a record in BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record to delete.
*   `record_id` (string, required): Specify the ID of the record to delete.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Create Record

Create a record in BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record to create (e.g., `Incident`, `ServiceRequest__c`).
*   `record_payload` (string, required): Specify a JSON object containing the fields and values for the new record.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the creation operation, likely including the new record ID.

### Wait For Fields Update

Wait for specific fields in a record to be updated to certain values in BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record.
*   `record_id` (string, required): Specify the ID of the record to monitor.
*   `fields_to_check` (string, required): Specify a JSON object containing the fields and their expected values (e.g., `{"Status__c": "Closed"}`).
*   `fail_if_timeout` (bool, required): If enabled, the action fails if the fields are not updated within the timeout period.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary indicating whether the fields were updated successfully within the timeout.

### Execute Custom Query

Execute a custom SOQL query in BMC Helix Remedyforce.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `soql_query` (string, required): Specify the full SOQL query to execute (e.g., `SELECT Id, Name FROM Incident WHERE Status__c = 'Open'`).
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the results of the custom SOQL query.

### Get OAuth Authorization Code

Generate an OAuth authorization code in BMC Helix Remedyforce. Please refer to the documentation portal for more information.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `redirect_url` (string, required): Specify the redirect URL that was used when the "Connector App" was created.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the authorization URL to initiate the OAuth flow.

## Notes

*   Ensure the BMC Helix Remedyforce integration is properly configured in the SOAR Marketplace tab with the correct Salesforce/Remedyforce instance URL and credentials (or OAuth details).
*   The integration user/Connected App needs appropriate permissions within Remedyforce for the desired actions (e.g., read/write access to Incident objects).
*   The `Get OAuth Authorization Code` and `Get OAuth Refresh Token` actions are typically used once during setup if using OAuth authentication.
*   SOQL query syntax should be used for the `Execute Custom Query` and `Execute Simple Query` actions.
