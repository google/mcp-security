# AlgoSec SOAR Integration

This document details the tools provided by the AlgoSec SOAR integration.

## Tools

### `algo_sec_list_templates`

List available templates in AlgoSec.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `filter_logic` (Optional[List[Any]], optional, default=None): Specify what filter logic should be applied.
*   `filter_value` (Optional[str], optional, default=None): Specify what value should be used in the filter. If "Equal" is selected, action will try to find the exact match among record types and if "Contains" is selected, action will try to find items that contain that substring. If nothing is provided in this parameter, the filter will not be applied.
*   `max_templates_to_return` (Optional[str], optional, default=None): Specify how many templates to return. Default: 50.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `algo_sec_wait_for_change_request_status_update`

Wait for change request status update in AlgoSec. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. Only traffic change requests are supported.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `request_id` (str, required): Specify the id of the request for which action needs to check the status.
*   `status` (str, required): Specify a comma-separated list of change request statuses for which action should wait. Possible values: resolved, reconcile, open, check, implementation plan, implement, validate.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `algo_sec_ping`

Test connectivity to the AlgoSec with parameters provided at the integration configuration page on the Marketplace tab.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `algo_sec_allow_ip`

Allow IPs in AlgoSec. Supported entities: IP address. Note: IP address entities are treated as destinations in the change request. This action creates a traffic change request to allow traffic to IP entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `template` (str, required): Specify the template for the change request.
*   `source` (str, required): Specify a comma-separated list of sources for the allow rule. It can be an IP address, IP Set or special keyword like (all).
*   `service` (str, required): Specify a comma-separated list of services that needs to be allowed. Values can have a look of {TCP/UDP}/{port} (tcp/80) or special reserved keyword (all).
*   `subject` (Optional[str], optional, default=None): Specify the subject for the change request. If nothing is provided action will put "Siemplify Allow IP request" in the subject.
*   `owner` (Optional[str], optional, default=None): Specify who should be the owner of the change request. If nothing is provided, the user that created the ticket will be the owner.
*   `due_date` (Optional[str], optional, default=None): Specify the due date for the change request. Format: ISO 8601. Example: 2021-08-13T08:16:10Z.
*   `expiration_date` (Optional[str], optional, default=None): Specify the expiration date for the change request. Format: ISO 8601. Example: 2021-08-13T08:16:10Z.
*   `custom_fields` (Optional[str], optional, default=None): Specify a JSON object containing information about all of the fields that need to be added to the change request. Note: this parameter has a priority over other fields
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `algo_sec_block_ip`

Block IPs in AlgoSec. Supported entities: IP address. Note: IP address entities are treated as destinations in the change request. This action creates a traffic change request to block traffic to IP entities.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `template` (str, required): Specify the template for the change request.
*   `source` (str, required): Specify a comma-separated list of sources for the block rule. It can be an IP address, IP Set or special keyword like (all).
*   `service` (str, required): Specify a comma-separated list of services that needs to be blocked. Values can have a look of {TCP/UDP}/{port} (tcp/80) or special reserved keyword (all).
*   `subject` (Optional[str], optional, default=None): Specify the subject for the change request. If nothing is provided action will put “Siemplify Block IP request” in the subject.
*   `owner` (Optional[str], optional, default=None): Specify who should be the owner of the change request. If nothing is provided, the user that created the ticket will be the owner.
*   `due_date` (Optional[str], optional, default=None): Specify the due date for the change request. Format: ISO 8601. Example: 2021-08-13T08:16:10Z.
*   `expiration_date` (Optional[str], optional, default=None): Specify the expiration date for the change request. Format: ISO 8601. Example: 2021-08-13T08:16:10Z.
*   `custom_fields` (Optional[str], optional, default=None): Specify a JSON object containing information about all of the fields that need to be added to the change request. Note: this parameter has a priority over other fields
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
