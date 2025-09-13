# RSA NetWitness Platform Integration

Connects Chronicle SOAR to the broader RSA NetWitness Platform, encompassing network, logs, and endpoint data for comprehensive threat detection and response.

## Configuration

*(Details on setting up the RSA NetWitness Platform integration, including API credentials, endpoint URLs, specific component configurations (Respond, Endpoint Server), and necessary permissions, would go here.)*

## Key Actions (Tools)

The following actions are available through the RSA NetWitness Platform integration:

### `rsa_net_witness_platform_update_incident`

*   **Description:** Update Incident in RSA Netwitness. Requires RSA Netwitness Respond license, configured Web Username and Web Password in the integration configuration.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `incident_id` (str, required): Specify ID of the incident that needs to be updated.
    *   `status` (Optional[List[str]], optional, default: None): Specify new status for the incident.
    *   `assignee` (Optional[str], optional, default: None): Specify new assignee for the incident.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_query_net_witness_for_events_around_ip`

*   **Description:** Run a query on RSA NetWitness to retreive all events for a specific query (conditions) for a given IP address in the alert.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `max_hours_backwards` (Optional[str], optional, default: None): Specify how many hours backwards to fetch events. Default is 1 hour.
    *   `max_events_to_return` (Optional[str], optional, default: None): Specify how many events to return. If nothing is specified, action will return 50 events.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_query_net_witness_for_events_around_host`

*   **Description:** Retrieve the latest events related to the hostnames in RSA Netwitness. Requires configuration of Broker API or Concentrator API.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `max_hours_backwards` (Optional[str], optional, default: None): Specify how many hours backwards to fetch events. Default is 1 hour.
    *   `max_events_to_return` (Optional[str], optional, default: None): Specify how many events to return. If nothing is specified, action will return 50 events.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_run_general_query`

*   **Description:** Run free query and receive event and a PCAP file.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `query` (str, required): Custom query string.
    *   `max_hours_backwards` (Optional[str], optional, default: None): Specify how many hours backwards to fetch events. Default is 1 hour.
    *   `max_events_to_return` (Optional[str], optional, default: None): Specify how many events to return. If nothing is specified, action will return 50 events.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_enrich_endpoint`

*   **Description:** Fetch endpoint's system information by its hostname or IP address. Requires RSA Netwitness Respond license, endpoint server service running in the background, configured Web Username and Web Password in the integration configuration.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `risk_score_threshold` (Optional[str], optional, default: None): Specify risk threshold for the endpoint. If the endpoint exceeds the threshold, the related entity will be marked as suspicious. If nothing is specified, action won’t check the risk score.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_ping`

*   **Description:** Test Connectivity
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_add_note_to_incident`

*   **Description:** Add Note to Incident in RSA Netwitness. Requires RSA Netwitness Respond license, configured Web Username and Web Password in the integration configuration.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `incident_id` (str, required): Specify ID of the incident that needs to be updated.
    *   `note` (str, required): Specify which note should be added to.
    *   `author` (str, required): Specify the author of the note.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_query_net_witness_for_events_around_user`

*   **Description:** Run a query on RSA NetWitness to retreive all events for a specific query (conditions) for a given username in the alert.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `max_hours_backwards` (Optional[str], optional, default: None): Specify how many hours backwards to fetch events. Default is 1 hour.
    *   `max_events_to_return` (Optional[str], optional, default: None): Specify how many events to return. If nothing is specified, action will return 50 events.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_isolate_endpoint`

*   **Description:** Request endpoint isolation in RSA Netwitness. Requires RSA Netwitness Respond license, endpoint server service running in the background, configured Web Username and Web Password in the integration configuration.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `comment` (str, required): Add comment, which describes the reason behind the isolation request.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_enrich_file`

*   **Description:** Fetch information about the file using hashes or file names. Only MD5 and SHA256 are supported. Requires RSA Netwitness Respond license, endpoint server service running in the background, configured Web Username and Web Password in the integration configuration.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `risk_score_threshold` (Optional[str], optional, default: None): Specify risk threshold for the file. If the file exceeds the threshold, the related entity will be marked as suspicious. If nothing is specified, action won’t check the risk score.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

### `rsa_net_witness_platform_unisolate_endpoint`

*   **Description:** Request endpoint unisolation in RSA Netwitness. Requires RSA Netwitness Respond license, endpoint server service running in the background, configured Web Username and Web Password in the integration configuration.
*   **Parameters:**
    *   `case_id` (str, required): The ID of the case.
    *   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    *   `comment` (str, required): Add comment, which describes the reason behind the unisolation request.
    *   `target_entities` (List[TargetEntity], optional, default: []): Optional list of specific target entities (Identifier, EntityType) to run the action on.
    *   `scope` (str, optional, default: "All entities"): Defines the scope for the action.

## Use Cases

*   Performing comprehensive event queries across network, logs, and endpoints based on SOAR entities (IPs, hosts, users, files).
*   Enriching SOAR entities (endpoints, files) with risk scores and system details from NetWitness.
*   Managing NetWitness incidents (updating status, assignee, adding notes) from SOAR.
*   Initiating endpoint response actions like isolation/unisolation directly from SOAR playbooks.
*   Retrieving PCAP data for network forensic analysis.
