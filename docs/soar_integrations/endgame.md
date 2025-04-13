# Endgame Integration

## Overview

This integration allows you to connect to Endgame and perform actions such as collecting autoruns, isolating/unisolating hosts, hunting for users, processes, files, IPs, and registry keys, managing host isolation configurations, surveying system details, killing processes, downloading/deleting files, and listing investigations and endpoints.

## Configuration

The configuration for this integration (API endpoint, credentials, etc.) is managed within the SOAR platform's Marketplace tab. The actions utilize these pre-configured settings.

## Actions

### Collect Autoruns

Collect Autoruns from Endgame endpoints (Windows only).

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many autoruns to return.
*   `category_all` (bool, optional): If enabled, search for all autorun categories.
*   `category_network_provider` (bool, optional): If enabled, search for "Network Provider" autorun category.
*   `category_office` (bool, optional): If enabled, search for "Office" autorun category.
*   `category_driver` (bool, optional): If enabled, search for "Driver" autorun category.
*   `category_app_init` (bool, optional): If enabled, search for "App Init" autorun category.
*   `category_winlogon` (bool, optional): If enabled, search for "Winlogon" autorun category.
*   `category_print_monitor` (bool, optional): If enabled, search for "Print Monitor" autorun category.
*   `category_ease_of_access` (bool, optional): If enabled, search for "Ease of Access" autorun category.
*   `category_wmi` (bool, optional): If enabled, search for "WMI" autorun category.
*   `category_lsa_provider` (bool, optional): If enabled, search for "LSA Provider" autorun category.
*   `category_service` (bool, optional): If enabled, search for "Service" autorun category.
*   `category_bits` (bool, optional): If enabled, search for "Bits" autorun category.
*   `category_known_dll` (bool, optional): If enabled, search for "Known dll" autorun category.
*   `category_print_provider` (bool, optional): If enabled, search for "Print Provider" autorun category.
*   `category_image_hijack` (bool, optional): If enabled, search for "Image Hijack" autorun category.
*   `category_startup_folder` (bool, optional): If enabled, search for "Startup Folder" autorun category.
*   `category_internet_explorer` (bool, optional): If enabled, search for "Internet Explorer" autorun category.
*   `category_codec` (bool, optional): If enabled, search for "Codec" autorun category.
*   `category_logon` (bool, optional): If enabled, search for "Logon" autorun category.
*   `category_search_order_hijack` (bool, optional): If enabled, search for "Search Order Hijack" autorun category.
*   `category_winsock_provider` (bool, optional): If enabled, search for "Winsock Provider" autorun category.
*   `category_boot_execute` (bool, optional): If enabled, search for "Boot Execute" autorun category.
*   `category_phantom_dll` (bool, optional): If enabled, search for "Phantom dll" autorun category.
*   `category_com_hijack` (bool, optional): If enabled, search for "Com Hijack" autorun category.
*   `category_explorer` (bool, optional): If enabled, search for "Explorer" autorun category.
*   `category_scheduled_task` (bool, optional): If enabled, search for "Scheduled Task" autorun category.
*   `include_all_metadata` (bool, optional): If enabled, provides all available data.
*   `include_malware_classification_metadata` (bool, optional): If enabled, provides information about MalwareScore.
*   `include_authenticode_metadata` (bool, optional): If enabled, provides Signer Information.
*   `include_md5_hash` (bool, optional): If enabled, provides MD5 hash in the response.
*   `include_sha_1_hash` (bool, optional): If enabled, provides SHA-1 hash in the response.
*   `include_sha_256_hash` (bool, optional): If enabled, provides SHA-256 hash in the response.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Isolate Host

Initiate Endgame endpoint isolation. This action supports only Windows and MacOS endpoints.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (bool, optional): If enabled, creates Insight after successful execution of this action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Hunt User

Searches the network for logged in users.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `endpoints_core_os` (string, optional): Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.
*   `find_username` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter username(s), separate multiple entries with a semicolon.
*   `domain_name` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter Domain Name.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Add IP Subnet to Host Isolation Config

Add IP subnet to Host Isolation Config defined in the Endgame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ip_subnet` (string, required): Enter the IPv4 Subnet that you want to add to Host Isolation Config.
*   `description` (string, optional): Enter the description to the IP Subnet.
*   `create_insight` (bool, optional): If enabled, creates Insight after successful execution of this action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Investigation Details

Get information on a specific Endgame Investigation.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `investigation_id` (string, required): Specify Endgame Investigation ID to search for.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Remove IP Subnet from Host Isolation Config

Remove IP subnet from Host Isolation Config defined in the Endgame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `ip_subnet` (string, required): Enter the IPv4 Subnet that you want to remove from Host Isolation Config.
*   `create_insight` (bool, optional): If enabled, creates Insight after successful execution of this action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### System Survey

Get system information on a single endgame endpoint, such as memory use, dns, and OS.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `include_security_product_information_windows_only` (bool, optional): Specify to get information about the security products installed on the endpoint (Windows only).
*   `include_patch_information_windows_only` (bool, optional): Specify to get information about patches (Windows only).
*   `include_disk_information` (bool, optional): Specify to get information about Disks.
*   `include_network_interface_information` (bool, optional): Specify to get information about network interfaces.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Hunt Process

Searches for running processes.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `endpoints_core_os` (string, optional): Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.
*   `md5_hashes` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter MD5 Hashes, separated by comma.
*   `sha1_hashes` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter SHA1 Hashes, separated by comma.
*   `sha256_hashes` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter SHA256 Hashes, separated by comma.
*   `process_name` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter Process Name ex. iss.exe.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Firewall Survey (Windows only)

Get information about the firewall rules on a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Unisolate Host

Initiate Endgame endpoint unisolation. This action supports only Windows and MacOS endpoints.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `create_insight` (bool, optional): If enabled, creates Insight after successful execution of this action.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### List Investigations

List Endgame Investigations.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `os` (string, optional): Specify for which OS you want to list investigations. Parameter can take multiple values as a comma separated string.
*   `fetch_investigations_for_the_last_x_hours` (string, optional): Return investigations created for the specified time frame in hours.
*   `max_investigation_to_return` (string, optional): Specify how many investigation you want to query.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Ping

Test connectivity to the Endgame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Host Isolation Config

Get Host Isolation Config defined in the Endgame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Get Endpoints

List all endpoints.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Process Survey

Get information about running processes on a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `detect_fileless_attacks_windows_only` (bool, optional): Specify to detect fileless attacks. Windows Only.
*   `detect_malware_with_malware_score_windows_only` (bool, optional): Specify to detect malware processes with MalwareScore. Windows Only.
*   `collect_process_threads` (bool, optional): Specify to include information about the amount of process threads in the response.
*   `return_only_suspicious_processes` (bool, optional): Specify to return only suspicious processes from the endpoint. By the Endgame definition: Suspicious processes are unbacked executable processes.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Drivers Survey (Windows only)

Get the information on drivers from a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Kill Process

Kill a process in a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `process_name` (string, required): Enter the process name.
*   `pid` (string, optional): Enter ID of the process.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### User Sessions Survey

Get information about an active user sessions on a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Network Survey

Get information about connections, DNS cache, Net Bios, ARP, and Route tables from a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `include_route_entries_information` (bool, optional): Specify to get information about the Route Entries.
*   `include_net_bios_information` (bool, optional): Specify to get information about Net Bios.
*   `include_dns_cache_information` (bool, optional): Specify to get information about the DNS Cache.
*   `include_arp_table_information` (bool, optional): Specify to get information about the ARP table.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Hunt IP

Searches for network connections.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `endpoints_core_os` (string, optional): Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.
*   `remote_ip_address` (string, optional): remote IP address - separated by comma.
*   `local_ip_address` (string, optional): separated by comma.
*   `state` (string, optional): Enter state to return. Ex. ANY.
*   `protocol` (string, optional): Ex. ANY, UDP, TCP.
*   `network_port` (string, optional): Network port.
*   `network_remote` (string, optional): Network Remote or Local.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Hunt Registry

Searches for a registry key or value name.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `hive` (string, optional): One of the following: HKEY_CLASSES_ROOT, HKEY_CURRENT_CONFIG, HKEY_USERS, HKEY_LOCAL_MACHINE, ALL.
*   `keys` (string, optional): Registry Key or Value Name.
*   `min_size` (string, optional): Min byte size.
*   `max_size` (string, optional): Max byte size.
*   `endpoints_core_os` (string, optional): Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Enrich Entities

Enrich Siemplify Host and IP entities based on the information from the Endgame.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Hunt File

Searches for running files.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `endpoints_core_os` (string, optional): Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.
*   `md5_hashes` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter MD5 Hashes, separated by comma.
*   `sha1_hashes` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter SHA1 Hashes, separated by comma.
*   `sha256_hashes` (string, optional): ADVANCED CONFIGURATION for this hunt. Enter SHA256 Hashes, separated by comma.
*   `directory` (string, optional): The starting directory path e.g. C:\\windows\\system32.
*   `find_file` (string, optional): Enter the filename(s) to search. TIP: Enter a regex to narrow search results.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Download File

Download a file from a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `full_file_path` (string, required): Enter the path to the file.
*   `full_download_folder_path` (string, required): Enter the path to the folder, where you want to store this file.
*   `expected_sha_256_hash` (string, optional): Enter the expected SHA-256 hash.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Delete File

Delete a file from Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `file_path` (string, required): Enter the path to the file.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Removable Media Survey (Windows only)

Get information about removable media from a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

### Software Survey (Windows only)

Get information about an installed software on a specific Endgame endpoint.

**Arguments:**

*   `case_id` (string, required): The ID of the case.
*   `alert_group_identifiers` (List[string], required): Identifiers for the alert groups.
*   `max_items_to_return` (string, optional): Specify how many items to return.
*   `target_entities` (List[TargetEntity], optional): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (string, optional): Defines the scope for the action. Defaults to "All entities".

**Returns:**

*   `dict`: A dictionary containing the result of the action execution.

## Notes

*   Some actions are specific to certain operating systems (e.g., Windows only) as indicated in their names or descriptions.
*   Actions rely on the Endgame integration being properly configured in the SOAR Marketplace.
*   The `Hunt` actions may have advanced configuration options specified in their argument descriptions.
