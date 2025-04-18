# Any.Run SOAR Integration

This document details the tools provided by the Any.Run SOAR integration.

## Tools

### `any_run_get_report`

Get Any.Run report from previous analysis based on the provided Siemplify FileHash, Filename or URL entity. Note: Action supports filehash entity in md-5, sha-1 and sha-256 formats.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `threshold` (str, required): Mark entity as suspicious if the score value for the entity is above the specified threshold.
*   `search_in_last_x_scans` (str, required): Search for report in last x analysises executed in Any.Run.
*   `create_insight` (Optional[bool], optional, default=None): Specify whether to create insight based on the report data.
*   `fetch_latest_report` (Optional[bool], optional, default=None): Specify whether to return latest analysis report or all found reports for the provided entity.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `any_run_analyze_file`

Create Any.Run file analysis task. Note: Action is not working with Siemplify entities, full path to file to analyze should be provided as action input parameter.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `file_path` (str, required): Specify full path to file to analyze.
*   `try_to_create_submission_for_x_times` (str, required): How many attempts action should make to check if the API concurrency limit is not exceeded and try to create a new submission. Check is made every 2 seconds.
*   `wait_for_the_report` (Optional[bool], optional, default=None): Specify whether action should wait for the report creation. Report also can be obtained later with Get report action once scan is completed.
*   `os_version` (Optional[List[Any]], optional, default=None): OS version to run analysis on.
*   `operation_system_bitness` (Optional[List[Any]], optional, default=None): Bitness of Operation System
*   `os_environment_type` (Optional[List[Any]], optional, default=None): Environment type to run analysis on.
*   `network_connection_status` (Optional[List[Any]], optional, default=None): Network connection state for analysis.
*   `fake_net_feature_status` (Optional[List[Any]], optional, default=None): FakeNet feature state for analysis.
*   `use_tor` (Optional[List[Any]], optional, default=None): Use TOR or not while running analysis.
*   `opt_network_mitm` (Optional[List[Any]], optional, default=None): HTTPS MITM proxy option.
*   `opt_network_geo` (Optional[List[Any]], optional, default=None): Geo location option.
*   `opt_kernel_heavyevasion` (Optional[List[Any]], optional, default=None): Heavy evasion option.
*   `opt_privacy_type` (Optional[List[Any]], optional, default=None): Privacy settings for analysis.
*   `obj_ext_startfolder` (Optional[List[Any]], optional, default=None): Start location for analysis.
*   `opt_timeout` (Optional[str], optional, default=None): Timeout period for analysis in range from 10 to 9999 seconds.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `any_run_ping`

Test Connectivity

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `any_run_analyze_file_url`

Create Any.Run file analysis task. Note: Action is not working with Siemplify entities, URL to file to analyze should be provided as action input parameter.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `url_to_file` (str, required): Specify URL to file to download and analyze.
*   `try_to_create_submission_for_x_times` (str, required): How many attempts action should make to check if the API concurrency limit is not exceeded and try to create a new submission. Check is made every 2 seconds.
*   `wait_for_the_report` (Optional[bool], optional, default=None): Specify whether action should wait for the report creation. Report also can be obtained later with Get report action once scan is completed.
*   `os_version` (Optional[List[Any]], optional, default=None): OS version to run analysis on.
*   `operation_system_bitness` (Optional[List[Any]], optional, default=None): Bitness of Operation System
*   `os_environment_type` (Optional[List[Any]], optional, default=None): Environment type to run analysis on.
*   `network_connection_status` (Optional[List[Any]], optional, default=None): Network connection state for analysis.
*   `fake_net_feature_status` (Optional[List[Any]], optional, default=None): FakeNet feature state for analysis.
*   `use_tor` (Optional[List[Any]], optional, default=None): Use TOR or not while running analysis.
*   `opt_network_mitm` (Optional[List[Any]], optional, default=None): HTTPS MITM proxy option.
*   `opt_network_geo` (Optional[List[Any]], optional, default=None): Geo location option.
*   `opt_kernel_heavyevasion` (Optional[List[Any]], optional, default=None): Heavy evasion option.
*   `opt_privacy_type` (Optional[List[Any]], optional, default=None): Privacy settings for analysis.
*   `obj_ext_startfolder` (Optional[List[Any]], optional, default=None): Start location for analysis.
*   `opt_timeout` (Optional[str], optional, default=None): Timeout period for analysis in range from 10 to 9999 seconds.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `any_run_search_report_history`

Search Any.Run scans history. Note: Action is not working with Siemplify entities, only action input parameters are used.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `search_in_last_x_scans` (str, required): Search for report in last x analyses executed in Any.Run.
*   `submission_name` (Optional[str], optional, default=None): Specific submission name to search for.
*   `skip_first_x_scans` (Optional[str], optional, default=None): Skip first x scans returned by Any.Run API.
*   `get_team_history` (Optional[bool], optional, default=None): Specify whether to get team history or not.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.

### `any_run_analyze_url`

Create Any.Run analysis task for the provided URL. Note: URL can be provided either as a Siemplify URL entity (artifact) or as an action input parameter. If the URL is provided both as an entity and input parameter - action will be executed on the input parameter.

**Parameters:**

*   `case_id` (str, required): The ID of the case.
*   `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
*   `url_for_analysis` (str, required): Specify URL to analyze. If URL is provided in both as entity and as this input parameter - action will be executed on input parameter.
*   `try_to_create_submission_for_x_times` (str, required): How many attempts action should make to check if the API concurrency limit is not exceeded and try to create a new submission. Check is made every 2 seconds.
*   `wait_for_the_report` (Optional[bool], optional, default=None): Specify whether action should wait for the report creation. Report also can be obtained later with Get report action once scan is completed.
*   `os_version` (Optional[List[Any]], optional, default=None): OS version to run analysis on.
*   `operation_system_bitness` (Optional[List[Any]], optional, default=None): Bitness of Operation System
*   `os_environment_type` (Optional[List[Any]], optional, default=None): Environment type to run analysis on.
*   `network_connection_status` (Optional[List[Any]], optional, default=None): Network connection state for analysis.
*   `fake_net_feature_status` (Optional[List[Any]], optional, default=None): FakeNet feature state for analysis.
*   `use_tor` (Optional[List[Any]], optional, default=None): Use TOR or not while running analysis.
*   `opt_network_mitm` (Optional[List[Any]], optional, default=None): HTTPS MITM proxy option.
*   `opt_network_geo` (Optional[List[Any]], optional, default=None): Geo location option.
*   `opt_kernel_heavyevasion` (Optional[List[Any]], optional, default=None): Heavy evasion option.
*   `opt_privacy_type` (Optional[List[Any]], optional, default=None): Privacy settings for analysis.
*   `obj_ext_startfolder` (Optional[List[Any]], optional, default=None): Start location for analysis.
*   `opt_timeout` (Optional[str], optional, default=None): Timeout period for analysis in range from 10 to 9999 seconds.
*   `target_entities` (List[TargetEntity], optional, default=[]): Optional list of specific target entities (Identifier, EntityType) to run the action on.
*   `scope` (str, optional, default="All entities"): Defines the scope for the action.
