# RSA NetWitness EDR Integration

Connects Chronicle SOAR to RSA NetWitness Endpoint Detection and Response (EDR) for endpoint investigation and response actions.

## Configuration

*(Details on setting up the RSA NetWitness EDR integration, including API credentials, endpoint URLs, and necessary permissions, would go here.)*

## Key Actions (Tools)

The following actions are available through the RSA NetWitness EDR integration:

### `rsa_net_witness_edr_add_url_to_blacklist`

*   **Description:** Add URL To Blacklist in RSA Netwitness EDR.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_edr_enrich_endpoint`

*   **Description:** Fetch endpoint's system information by its hostname or IP address.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `iioc_score_threshold` (Optional[str], optional, default: None): Specify IIOC score threshold for the endpoint. If the endpoint exceeds the threshold, the related entity will be marked as suspicious. If nothing is specified, action won’t check the IIOC score.
    *   `include_ioc_information` (Optional[bool], optional, default: None): If enabled, action will fetch information about the IOCs that are associated with the endpoint
    *   `max_io_cs_to_return` (Optional[str], optional, default: None): Specify how many IOCs to return. Maximum is 50. This is RSA Netwitness EDR limitation.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_edr_ping`

*   **Description:** Test Connectivity
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_edr_get_ioc_details`

*   **Description:** Enrich Siemplify Entities with information about IOCs from RSA Netwitness EDR.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `ioc_level_threshold` (List[str], required): Specify IOC level threshold for the entity. If the entity exceeds the threshold, the related entity will be marked as suspicious.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_edr_add_ip_to_blacklist`

*   **Description:** Add IP To Blacklist in RSA Netwitness EDR.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

## Use Cases

*   Enriching endpoint entities (hosts, IPs) in SOAR with system information and IOC details from NetWitness EDR.
*   Adding malicious IPs or URLs identified during an investigation to the NetWitness EDR blacklist.
*   Assessing endpoint risk based on IIOC scores.
