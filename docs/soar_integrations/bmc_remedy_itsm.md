# BMC Remedy ITSM Integration

## Overview

This integration allows you to connect to BMC Remedy ITSM to manage records, primarily Incidents. Actions include creating, updating, deleting, and retrieving incident and other record details, adding work notes, and waiting for field updates.

## Configuration

To configure this integration within the SOAR platform, you typically need the following BMC Remedy ITSM details:

*   **Server Address:** The hostname or IP address of your BMC Remedy AR System server.
*   **Username:** The username for the integration account.
*   **Password:** The password for the integration account.
*   **(Optional) Port:** The port number if your AR System server uses a non-standard port (often defaults are used).
*   **(Optional) Authentication:** Specific authentication details if required by your server configuration (e.g., AR-JWT token details, specific authentication string).

*(Note: The exact parameter names might vary slightly depending on the specific SOAR platform configuration interface. Ensure the integration user has the necessary permissions within Remedy ITSM to perform the desired actions, such as creating or updating incidents.)*

## Actions

### Update Incident

Update an incident in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the id of the incident that needs to be updated.
*   `status` (List[Any], optional): Specify the status for the incident. Note: if status is "Pending" or "Resolved", then you also need to provide "Status Reason" value.
*   `status_reason` (string, optional): Specify the status reason for the incident.
*   `impact` (List[Any], optional): Specify the impact for the incident.
*   `urgency` (List[Any], optional): Specify the urgency for the incident.
*   `description` (string, optional): Specify the description of the incident.
*   `incident_type` (List[Any], optional): Specify the incident type for the incident.
*   `assigned_group` (string, optional): Specify the assigned group for the incident.
*   `assignee` (string, optional): Specify the assignee for the incident.
*   `resolution` (string, optional): Specify the resolution for the incident.
*   `resolution_category_tier_1` (string, optional): Specify the resolution category tier 1 for the incident.
*   `resolution_category_tier_2` (string, optional): Specify the resolution category tier 2 for the incident.
*   `resolution_category_tier_3` (string, optional): Specify the resolution category tier 3 for the incident.
*   `resolution_product_category_tier_1` (string, optional): Specify the resolution product category tier 1 for the incident.
*   `resolution_product_category_tier_2` (string, optional): Specify the resolution product category tier 2 for the incident.
*   `resolution_product_category_tier_3` (string, optional): Specify the resolution product category tier 3 for the incident.
*   `reported_source` (List[Any], optional): Specify the reported source.
*   `custom_fields` (string, optional): Specify a JSON object containing all of the needed fields and values that need to be updated. Note: this parameter will overwrite other provided parameters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the incident update operation.

### Update Record

Update a record in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record that needs to be updated.
*   `record_id` (string, required): Specify the id of the record that needs to be updated.
*   `record_payload` (string, required): Specify a JSON object containing all of the needed fields and values that need to be updated.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the record update operation.

### Get Record Details

Get detailed information about the record from BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record for which you want to retrieve details.
*   `record_i_ds` (string, required): Specify the comma-separated IDs of records for which you want to return details.
*   `fields_to_return` (string, optional): Specify what fields to return (comma-separated). If empty, returns all fields. If invalid fields are provided, the action fails.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details for the specified record(s).

### Add Work Note To Incident

Add a work note to incidents in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the id of the incident to which you want to add a work note.
*   `work_note_text` (string, required): Specify the text for the work note.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Wait For Record Fields Update

Wait for specific fields in a record to be updated to certain values in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record for which you are waiting an update.
*   `record_id` (string, required): Specify the ID of the record that needs to be updated.
*   `fields_to_check` (string, required): Specify a JSON object containing all of the needed fields and values (e.g., `{"Status": "Closed"}`).
*   `fail_if_timeout` (bool, required): If enabled, action will be failed, if not all of the fields were updated within the timeout period.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary indicating whether the fields were updated successfully within the timeout.

### Delete Incident

Delete an incident in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the id of the incident that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Ping

Test connectivity to the BMC Remedy ITSM with parameters provided at the integration configuration page on the Marketplace tab.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the ping action.

### Delete Record

Delete a record in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record that needs to be deleted.
*   `record_id` (string, required): Specify the id of the record that needs to be deleted.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the deletion operation.

### Get Incident Details

Get detailed information about the incidents from BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_i_ds` (string, required): Specify the comma-separated IDs of incidents for which you want to return details.
*   `fields_to_return` (string, optional): Specify what fields to return (comma-separated). If empty, returns all fields. If invalid fields are provided, the action fails.
*   `fetch_work_notes` (bool, optional): If enabled, action will return work notes related to the incident.
*   `max_work_notes_to_return` (string, optional): Specify how many Work Notes to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the details for the specified incident(s), potentially including work notes.

### Create Record

Create a record in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `record_type` (string, required): Specify the type of the record that needs to be created.
*   `record_payload` (string, required): Specify a JSON object containing all of the needed fields and values.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the creation operation, likely including the new record ID.

### Create Incident

Create an incident in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `status` (List[Any], optional): Specify the status for the incident.
*   `impact` (List[Any], optional): Specify the impact for the incident.
*   `urgency` (List[Any], optional): Specify the urgency for the incident.
*   `description` (string, optional): Specify the description of the incident.
*   `company` (string, optional): Specify the company for the incident.
*   `customer` (string, optional): Specify the customer for the incident. Note: Customer needs to be provided in the format "{Last Name} {First Name}". Example: Allbrook Allen.
*   `template_name` (string, optional): Specify the name of the template for the incident. Note: action will try to find the ID of the template. For better precision provide the template ID via Custom Fields.
*   `incident_type` (List[Any], optional): Specify the incident type for the incident.
*   `assigned_group` (string, optional): Specify the assigned group for the incident.
*   `assignee` (string, optional): Specify the assignee for the incident.
*   `resolution` (string, optional): Specify the resolution for the incident.
*   `resolution_category_tier_1` (string, optional): Specify the resolution category tier 1.
*   `resolution_category_tier_2` (string, optional): Specify the resolution category tier 2.
*   `resolution_category_tier_3` (string, optional): Specify the resolution category tier 3.
*   `resolution_product_category_tier_1` (string, optional): Specify the resolution product category tier 1.
*   `resolution_product_category_tier_2` (string, optional): Specify the resolution product category tier 2.
*   `resolution_product_category_tier_3` (string, optional): Specify the resolution product category tier 3.
*   `reported_source` (List[Any], optional): Specify the reported source.
*   `custom_fields` (string, optional): Specify a JSON object containing additional fields and values. Note: this parameter will overwrite other provided parameters.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the incident creation, likely including the new incident ID.

### Wait For Incident Fields Update

Wait for incident fields update in BMC Remedy ITSM.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `incident_id` (string, required): Specify the ID of the incident that needs to be updated.
*   `fail_if_timeout` (bool, required): If enabled, action will be failed, if not all of the fields were updated within the timeout period.
*   `status` (List[Any], optional): Specify the expected status for the incident.
*   `fields_to_check` (string, optional): Specify a JSON object containing the fields and their expected values (e.g., `{"Status": "Closed"}`). Note: this parameter has priority over the "Status" field.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary indicating whether the fields were updated successfully within the timeout.

## Notes

*   Ensure the BMC Remedy ITSM integration is properly configured in the SOAR Marketplace tab with the correct server details and credentials.
*   The integration user requires appropriate permissions within Remedy ITSM to perform actions like creating, updating, or deleting records.
*   When updating incidents, providing a `Status Reason` might be required depending on the chosen `Status`.
*   The `Custom Fields` parameter in `Create Incident` and `Update Incident` allows setting values for fields not explicitly listed as parameters, but it overwrites other provided parameters if there are overlaps.
*   The `Wait For...` actions are asynchronous and depend on the SOAR platform's timeout settings.
