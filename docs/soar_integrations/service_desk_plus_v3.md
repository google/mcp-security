# ServiceDeskPlusV3 SOAR Integration

## Overview

The ServiceDesk Plus V3 integration for Chronicle SOAR allows users to interact with ServiceDesk Plus requests directly from the SOAR platform. This includes creating new requests (general or linked to alerts), updating existing requests, retrieving request details, adding notes, closing requests, and testing connectivity to the ServiceDesk Plus instance. It also provides tools to wait for specific field or status updates on requests.

## Tools

### `service_desk_plus_v3_create_request`

Create a new request

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `subject` (str, required): The subject of the request.
*   `requester` (str, required): The requester of the request. If not specified, set to the user of the API key.
*   `description` (Optional[str], optional, default=None): The description of the request.
*   `assets` (Optional[str], optional, default=None): Names of Assets to be associated with the request
*   `status` (Optional[str], optional, default=None): The status of the request.
*   `technician` (Optional[str], optional, default=None): The name of the technician assigned to the request.
*   `priority` (Optional[str], optional, default=None): The priority of the request.
*   `urgency` (Optional[str], optional, default=None): The urgency of the request.
*   `category` (Optional[str], optional, default=None): The category of the request.
*   `request_template` (Optional[str], optional, default=None): The template of the request.
*   `request_type` (Optional[str], optional, default=None): The type of the request. i.e: Incident, Service Request, etc.
*   `due_by_time_ms` (Optional[str], optional, default=None): The due date of the request in milliseconds.
*   `mode` (Optional[str], optional, default=None): The mode in which this request is created.Example : E-mail
*   `level` (Optional[str], optional, default=None): The level of the request.
*   `site` (Optional[str], optional, default=None): Denotes the site to which this request belongs
*   `group` (Optional[str], optional, default=None): Group to which this request belongs
*   `impact` (Optional[str], optional, default=None): The impact of the request.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_create_alert_request`

Create a request related to a Siemplify alert

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `subject` (str, required): The subject of the request.
*   `requester` (str, required): The requester of the request. If not specified, set to the user of the API key.
*   `assets` (Optional[str], optional, default=None): Names of Assets to be associated with the request
*   `status` (Optional[str], optional, default=None): The status of the request.
*   `technician` (Optional[str], optional, default=None): The name of the technician assigned to the request.
*   `priority` (Optional[str], optional, default=None): The priority of the request.
*   `urgency` (Optional[str], optional, default=None): The urgency of the request.
*   `category` (Optional[str], optional, default=None): The category of the request.
*   `request_template` (Optional[str], optional, default=None): The template of the request.
*   `request_type` (Optional[str], optional, default=None): The type of the request. i.e: Incident, Service Request, etc.
*   `due_by_time_ms` (Optional[str], optional, default=None): The due date of the request in milliseconds.
*   `mode` (Optional[str], optional, default=None): The mode in which this request is created.Example : E-mail
*   `level` (Optional[str], optional, default=None): The level of the request.
*   `site` (Optional[str], optional, default=None): Denotes the site to which this request belongs
*   `group` (Optional[str], optional, default=None): Group to which this request belongs
*   `impact` (Optional[str], optional, default=None): The impact of the request.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_create_request_dropdown_lists`

Create a new request

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `subject` (str, required): The subject of the request.
*   `requester` (str, required): The requester of the request. If not specified, set to the user of the API key.
*   `description` (Optional[str], optional, default=None): The description of the request.
*   `assets` (Optional[str], optional, default=None): Names of Assets to be associated with the request
*   `status` (Optional[List[str]], optional, default=None): The status of the request.
*   `technician` (Optional[str], optional, default=None): The name of the technician assigned to the request.
*   `priority` (Optional[List[str]], optional, default=None): The priority of the request.
*   `urgency` (Optional[List[str]], optional, default=None): The urgency of the request.
*   `category` (Optional[List[str]], optional, default=None): The category of the request.
*   `request_template` (Optional[str], optional, default=None): The template of the request.
*   `request_type` (Optional[List[str]], optional, default=None): The type of the request. i.e: Incident, Service Request, etc.
*   `due_by_time_ms` (Optional[str], optional, default=None): The due date of the request in milliseconds.
*   `mode` (Optional[List[str]], optional, default=None): The mode in which this request is created.Example : E-mail
*   `level` (Optional[List[str]], optional, default=None): The level of the request.
*   `site` (Optional[str], optional, default=None): Denotes the site to which this request belongs
*   `group` (Optional[str], optional, default=None): Group to which this request belongs
*   `impact` (Optional[List[str]], optional, default=None): The impact of the request.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_add_note_and_wait_for_reply`

Add a note to a request. Note: Please update the actual time you would like the action to run in the IDE timeout section for this action.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The requests' ID.
*   `note` (str, required): The note's content.
*   `show_to_requester` (Optional[bool], optional, default=None): Specify whether the note should be shown to the requester or not.
*   `notify_technician` (Optional[bool], optional, default=None): Specify whether the note should be shown to the requester or not
*   `mark_first_response` (Optional[bool], optional, default=None): Specify whether this note should be marked as first response
*   `add_to_linked_requests` (Optional[bool], optional, default=None): Specify whether this note should be added to the linked requests
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_ping`

Test connectivity to ServiceDesk Plus instance.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_update_request`

Update a ServiceDesk Plus request via it’s ID

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The ID of the request to update.
*   `subject` (Optional[str], optional, default=None): The subject of the request.
*   `requester` (Optional[str], optional, default=None): The requester of the request. If not specified, set to the user of the API key.
*   `description` (Optional[str], optional, default=None): The description of the request.
*   `assets` (Optional[str], optional, default=None): Names of Assets to be associated with the request
*   `status` (Optional[str], optional, default=None): The status of the request.
*   `technician` (Optional[str], optional, default=None): The name of the technician assigned to the request.
*   `priority` (Optional[str], optional, default=None): The priority of the request.
*   `urgency` (Optional[str], optional, default=None): The urgency of the request.
*   `category` (Optional[str], optional, default=None): The category of the request.
*   `request_template` (Optional[str], optional, default=None): The template of the request.
*   `request_type` (Optional[str], optional, default=None): The type of the request. i.e: Incident, Service Request, etc.
*   `due_by_time_ms` (Optional[str], optional, default=None): The due date of the request in milliseconds.
*   `mode` (Optional[str], optional, default=None): The mode in which this request is created.Example : E-mail
*   `level` (Optional[str], optional, default=None): The level of the request.
*   `site` (Optional[str], optional, default=None): Denotes the site to which this request belongs
*   `group` (Optional[str], optional, default=None): Group to which this request belongs
*   `impact` (Optional[str], optional, default=None): The impact of the request.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_get_request`

Retrieve information about a request In Service Desk Plus.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The ID of the request.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_close_request`

Close a request

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The requests' ID.
*   `comment` (str, required): Closing comment.
*   `resolution_acknowledged` (Optional[bool], optional, default=None): Whether the resolution of the request is acknowledged or not.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_wait_for_field_update`

Wait for a field of a request ot update to a desired value. Note: Please update the actual time you would like the action to run in the IDE timeout section for this action.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The ID of the request.
*   `values` (str, required): Desired values for the given field.
*   `field_name` (str, required): The name of the field to be updated.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_add_note`

Add a note to a request

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The requests' ID.
*   `note` (str, required): The note's content.
*   `show_to_requester` (Optional[bool], optional, default=None): Specify whether the note should be shown to the requester or not.
*   `notify_technician` (Optional[bool], optional, default=None): Specify whether the note should be shown to the requester or not
*   `mark_first_response` (Optional[bool], optional, default=None): Specify whether this note should be marked as first response
*   `add_to_linked_requests` (Optional[bool], optional, default=None): Specify whether this note should be added to the linked requests
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `service_desk_plus_v3_wait_for_status_update`

Wait for the status of a request ot update to a desired status. Note: Please update the actual time you would like the action to run in the IDE timeout section for this action.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): The ID of the request.
*   `values` (str, required): Desired values for the given field.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
