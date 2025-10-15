# VirusTotalV3 SOAR Integration

## Overview

This document outlines the tools available in the VirusTotalV3 SOAR integration.

## Tools

### `virus_total_v3_add_comment_to_entity`

Add a comment to entities in VirusTotal. Supported entities: File Hash, URL, Hostname, Domain, IP Address. Note: only MD5, SHA-1 and SHA-256 Hash types are supported Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `comment` (str, required): Specify the comment that should be added to entities.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_search_io_cs`

Search for IOCs in the VirusTotal's dataset, using the same query syntax that you would use in the VirusTotal Intelligence user interface. This action requires a VT Enterprise token. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query according to the VirusTotal query search syntax.
*   `order_by` (List[str], required): Specify the order by the selected field, in which results are returned. Default: Use Default Order. Note: Entity types might have different ordering fields. Refer to the VT Intelligence corpus https://docs.virustotal.com/reference/intelligence-search for more information.
*   `create_entities` (bool, optional, default=None): If enabled, action will create entities for the returned IOCs. Note: this action does not enrich entities.
*   `sort_order` (List[str], optional, default=None): Specify the direction in which the results should be returned. If “Use Default Order” is chosen for “Order By” field, this parameter will be ignored.
*   `max_io_cs_to_return` (str, optional, default=None): Specify how many IOCs to return. Max IOCs to return is 300. Default: 10.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_enrich_hash`

Enrich Hash using information from VirusTotal. Supported entities: Filehash. Note: only MD5, SHA-1 and SHA-256 are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `engine_threshold` (str, optional, default=None): Specify how many engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.
*   `engine_percentage_threshold` (str, optional, default=None): Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.
*   `engine_whitelist` (str, optional, default=None): Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it’s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".
*   `resubmit_hash` (bool, optional, default=None): If enabled, action will resubmit hashes for analysis instead of using the latest information.
*   `resubmit_after_days` (str, optional, default=None): Specify how many days since the last submission should pass for the entity to be submitted again. Note: parameter \"Resubmit Hash\" needs to be enabled.
*   `retrieve_comments` (bool, optional, default=None): If enabled, action will retrieve comments about the entity.
*   `retrieve_sigma_analysis` (bool, optional, default=None): If enabled, action will retrieve sigma analysis for the hash.
*   `sandbox` (str, optional, default=None): Specify a comma-separated list of sandbox names that should be used for behavior analysis. If nothing is provided, action will only use the \"VirusTotal Jujubox\" sandbox. Make sure that the spelling is correct. Examples of sandboxes: VirusTotal Jujubox, VirusTotal ZenBox, Microsoft Sysinternals, Tencent HABO.
*   `retrieve_sandbox_analysis` (bool, optional, default=None): If enabled, action will fetch sandbox analysis for the entity. For each sandbox, action will create a separate section in the JSON result. Action will only return data for the sandboxes that are provided in the parameter \"Sandbox\".
*   `create_insight` (bool, optional, default=None): If enabled, action will create an insight containing information about the entities.
*   `only_suspicious_entity_insight` (bool, optional, default=None): If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.
*   `max_comments_to_return` (str, optional, default=None): Specify how many comments to return. Default: 10.
*   `widget_theme` (List[str], optional, default=None): Specify the theme for the widget.
*   `fetch_widget` (bool, optional, default=None): If enabled, action will fetch augmented widget related to the entity.
*   `fetch_mitre_details` (bool, optional, default=None): If enabled, action will return information about related MITRE techniques and tactics.
*   `lowest_mitre_technique_severity` (List[str], optional, default=None): Specify the lowest signature severity related to MITRE technique for technique to be returned. \"Unknown\" severity is treated as \"Info\".
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_get_related_i_ps`

Get related IPs to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `results` (List[str], optional, default=None): Specify how the JSON result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.
*   `max_i_ps_to_return` (str, optional, default=None): Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_get_related_domains`

Get related domains to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: IP, URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `results` (List[str], optional, default=None): Specify how the JSON result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.
*   `max_domains_to_return` (str, optional, default=None): Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_enrich_ip`

Enrich IP using information from VirusTotal. Supported entities: IP address. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `engine_threshold` (str, optional, default=None): Specify how many engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.
*   `engine_percentage_threshold` (str, optional, default=None): Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.
*   `engine_whitelist` (str, optional, default=None): Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it’s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".
*   `retrieve_comments` (bool, optional, default=None): If enabled, action will retrieve comments about the entity.
*   `create_insight` (bool, optional, default=None): If enabled, action will create an insight containing information about the entities.
*   `only_suspicious_entity_insight` (bool, optional, default=None): If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.
*   `max_comments_to_return` (str, optional, default=None): Specify how many comments to return. Default: 10
*   `widget_theme` (List[str], optional, default=None): Specify the theme for the widget.
*   `fetch_widget` (bool, optional, default=None): If enabled, action will fetch augmented widget related to the entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_ping`

Test connectivity to the VirusTotal with parameters provided at the integration configuration page on the Marketplace tab. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_get_domain_details`

Get detailed information about the domain using information from VirusTotal. Supported entities: URL (entity extracts domain part), Hostname, Domain. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `engine_threshold` (str, optional, default=None): Specify how many engines should mark the domain as malicious or suspicious, for Siemplify to label it as risky. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.
*   `engine_percentage_threshold` (str, optional, default=None): Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.
*   `engine_whitelist` (str, optional, default=None): Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it’s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".
*   `retrieve_comments` (bool, optional, default=None): If enabled, action will retrieve comments about the entity.
*   `create_insight` (bool, optional, default=None): If enabled, action will create an insight containing information about the entities.
*   `only_suspicious_entity_insight` (bool, optional, default=None): If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.
*   `max_comments_to_return` (str, optional, default=None): Specify how many comments to return. Default: 10.
*   `widget_theme` (List[str], optional, default=None): Specify the theme for the widget.
*   `fetch_widget` (bool, optional, default=None): If enabled, action will fetch augmented widget related to the entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_search_graphs`

Search graphs based on custom filters in VirusTotal. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `query` (str, required): Specify the query filter for the graph. Please refer to the documentation portal for more details.
*   `sort_field` (List[str], optional, default=None): Specify what should be the sort field.
*   `max_graphs_to_return` (str, optional, default=None): Specify how many graphs to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_search_entity_graphs`

Search graphs based on the entities in VirusTotal. Supported entities: IP, URL, Filehash, Hostname, Domain, Threat Actor, User. Note: only MD5, SHA-1 and SHA-256 are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `sort_field` (List[str], optional, default=None): Specify what should be the sort field.
*   `max_graphs_to_return` (str, optional, default=None): Specify how many graphs to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_enrich_ioc`

Enrich IOCs using information from VirusTotal. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `io_cs` (str, required): Specify a comma-separated list of IOCs for which you want to ingest data.
*   `ioc_type` (List[str], optional, default=None): Specify the type of the IOC.
*   `widget_theme` (List[str], optional, default=None): Specify the theme for the widget.
*   `fetch_widget` (bool, optional, default=None): If enabled, action will fetch augmented widget related to the entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_download_file`

Download file from VirusTotal. Supported entities: Filehash. Note: this action requires a VT Enterprise token. Only MD5, SHA-1, SHA-256 hashes are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `download_folder_path` (str, required): Specify the path to the folder, where you want to store the files.
*   `overwrite` (bool, optional, default=None): If enabled, action will overwrite the file with the same name.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_get_related_hashes`

Get related hashes to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: IP, URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `results` (List[str], optional, default=None): Specify how the JSON result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.
*   `max_hashes_to_return` (str, optional, default=None): Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_add_vote_to_entity`

Add a vote to entities in VirusTotal. Supported entities: File Hash, URL, Hostname, Domain, IP Address. Note: only MD5, SHA-1 and SHA-256 Hash types are supported Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `vote` (List[str], required): Specify the vote that should be added to entities.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_get_graph_details`

Get detailed information about graphs in VirusTotal. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `graph_id` (str, required): Specify a comma-separated list of graph ids for which you want to retrieve detailed information.
*   `max_links_to_return` (str, optional, default=None): Specify how many links to return.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_enrich_url`

Enrich URL using information from VirusTotal. Supported entities: URL. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `engine_threshold` (str, optional, default=None): Specify how many engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.
*   `engine_percentage_threshold` (str, optional, default=None): Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.
*   `engine_whitelist` (str, optional, default=None): Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it’s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".
*   `resubmit_url` (bool, optional, default=None): If enabled, action will resubmit urls for analysis instead of using the latest information.
*   `retrieve_comments` (bool, optional, default=None): If enabled, action will retrieve comments about the entity.
*   `only_suspicious_entity_insight` (bool, optional, default=None): If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.
*   `create_insight` (bool, optional, default=None): If enabled, action will create an insight containing information about the entities.
*   `max_comments_to_return` (str, optional, default=None): Specify how many comments to return. Default: 10.
*   `resubmit_after_days` (str, optional, default=None): Specify how many days since the last submission should pass for the entity to be submitted again. Note: parameter \"Resubmit URL\" needs to be enabled. Default: 30.
*   `widget_theme` (List[str], optional, default=None): Specify the theme for the widget.
*   `fetch_widget` (bool, optional, default=None): If enabled, action will fetch augmented widget related to the entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_submit_file`

Submit a file and return results from VirusTotal. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_paths` (str, required): Specify a comma-separated list of absolute file paths. Note: if \"Linux Server Address\" is specified, action will try to fetch file from remote server.
*   `engine_threshold` (str, optional, default=None): Specify how many engines should mark the file as malicious or suspicious, for Siemplify to label it as risky. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.
*   `engine_percentage_threshold` (str, optional, default=None): Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.
*   `engine_whitelist` (str, optional, default=None): Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it’s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".
*   `retrieve_comments` (bool, optional, default=None): If enabled, action will retrieve comments about the entity.
*   `max_comments_to_return` (str, optional, default=None): Specify how many comments to return.
*   `linux_server_address` (str, optional, default=None): Specify the IP address of the remote linux server, where the file is located.
*   `linux_username` (str, optional, default=None): Specify the username of the remote linux server, where the file is located.
*   `linux_password` (str, optional, default=None): Specify the password of the remote linux server, where the file is located.
*   `private_submission` (bool, optional, default=None): If enabled, action will submit the file privately. Note: this functionality requires premium VT access.
*   `fetch_mitre_details` (bool, optional, default=None): If enabled, action will return information about related MITRE techniques and tactics.
*   `lowest_mitre_technique_severity` (List[str], optional, default=None): Specify the lowest signature severity related to MITRE technique for technique to be returned. \"Unknown\" severity is treated as \"Info\".
*   `retrieve_ai_summary` (bool, optional, default=None): Experimental. If enabled, action will retrieve an AI Summary for the submitted file. AI Summary is only available for private submissions.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `virus_total_v3_get_related_ur_ls`

Get related urls to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: IP, URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported. Returns: dict: A dictionary containing the result of the action execution.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `results` (List[str], optional, default=None): Specify how the JSON  result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.
*   `max_ur_ls_to_return` (str, optional, default=None): Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
