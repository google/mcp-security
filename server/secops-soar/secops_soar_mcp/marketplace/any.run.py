# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from secops_soar_mcp import bindings
from mcp.server.fastmcp import FastMCP
from secops_soar_mcp.utils.consts import Endpoints
from secops_soar_mcp.utils.models import ApiManualActionDataModel, EmailContent, TargetEntity
import json
from typing import Optional, List, Dict, Union, Annotated
from pydantic import Field
from secops_soar_mcp.utils.pydantic_list_field import PydanticListField


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the AnyRun integration.

    @mcp.tool()
    async def any_run_get_report(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threshold: Annotated[str, Field(..., description="Mark entity as suspicious if the score value for the entity is above the specified threshold.")], search_in_last_x_scans: Annotated[str, Field(..., description="Search for report in last x analysises executed in Any.Run.")], create_insight: Annotated[bool, Field(default=None, description="Specify whether to create insight based on the report data.")], fetch_latest_report: Annotated[bool, Field(default=None, description="Specify whether to return latest analysis report or all found reports for the provided entity.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get Any.Run report from previous analysis based on the provided Siemplify FileHash, Filename or URL entity. Note: Action supports filehash entity in md-5, sha-1 and sha-256 formats.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AnyRun")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AnyRun: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threshold"] = threshold
            script_params["Search in last x scans"] = search_in_last_x_scans
            if create_insight is not None:
                script_params["Create Insight?"] = create_insight
            if fetch_latest_report is not None:
                script_params["Fetch latest report?"] = fetch_latest_report
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AnyRun_Get Report",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AnyRun_Get Report",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action AnyRun_Get Report for AnyRun: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AnyRun")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def any_run_analyze_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_path: Annotated[str, Field(..., description="Specify full path to file to analyze.")], try_to_create_submission_for_x_times: Annotated[str, Field(..., description="How many attempts action should make to check if the API concurrency limit is not exceeded and try to create a new submission. Check is made every 2 seconds.")], wait_for_the_report: Annotated[bool, Field(default=None, description="Specify whether action should wait for the report creation. Report also can be obtained later with Get report action once scan is completed.")], os_version: Annotated[List[str], Field(default=None, description="OS version to run analysis on.")], operation_system_bitness: Annotated[List[str], Field(default=None, description="Bitness of Operation System")], os_environment_type: Annotated[List[str], Field(default=None, description="Environment type to run analysis on.")], network_connection_status: Annotated[List[str], Field(default=None, description="Network connection state for analysis.")], fake_net_feature_status: Annotated[List[str], Field(default=None, description="FakeNet feature state for analysis.")], use_tor: Annotated[List[str], Field(default=None, description="Use TOR or not while running analysis.")], opt_network_mitm: Annotated[List[str], Field(default=None, description="HTTPS MITM proxy option.")], opt_network_geo: Annotated[List[str], Field(default=None, description="Geo location option.")], opt_kernel_heavyevasion: Annotated[List[str], Field(default=None, description="Heavy evasion option.")], opt_privacy_type: Annotated[List[str], Field(default=None, description="Privacy settings for analysis.")], obj_ext_startfolder: Annotated[List[str], Field(default=None, description="Start location for analysis.")], opt_timeout: Annotated[str, Field(default=None, description="Timeout period for analysis in range from 10 to 9999 seconds.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create Any.Run file analysis task. Note: Action is not working with Siemplify entities, full path to file to analyze should be provided as action input parameter.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AnyRun")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AnyRun: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["File Path"] = file_path
            if wait_for_the_report is not None:
                script_params["Wait for the report?"] = wait_for_the_report
            script_params["Try to create submission for x times"] = try_to_create_submission_for_x_times
            if os_version is not None:
                script_params["OS Version"] = os_version
            if operation_system_bitness is not None:
                script_params["Operation System Bitness"] = operation_system_bitness
            if os_environment_type is not None:
                script_params["OS Environment Type"] = os_environment_type
            if network_connection_status is not None:
                script_params["Network Connection Status"] = network_connection_status
            if fake_net_feature_status is not None:
                script_params["FakeNet Feature Status"] = fake_net_feature_status
            if use_tor is not None:
                script_params["Use TOR"] = use_tor
            if opt_network_mitm is not None:
                script_params["opt_network_mitm"] = opt_network_mitm
            if opt_network_geo is not None:
                script_params["opt_network_geo"] = opt_network_geo
            if opt_kernel_heavyevasion is not None:
                script_params["opt_kernel_heavyevasion"] = opt_kernel_heavyevasion
            if opt_privacy_type is not None:
                script_params["opt_privacy_type"] = opt_privacy_type
            if obj_ext_startfolder is not None:
                script_params["obj_ext_startfolder"] = obj_ext_startfolder
            if opt_timeout is not None:
                script_params["opt_timeout"] = opt_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AnyRun_AnalyzeFile",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AnyRun_AnalyzeFile",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action AnyRun_AnalyzeFile for AnyRun: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AnyRun")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def any_run_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AnyRun")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AnyRun: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AnyRun_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AnyRun_Ping",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action AnyRun_Ping for AnyRun: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AnyRun")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def any_run_analyze_file_url(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], url_to_file: Annotated[str, Field(..., description="Specify URL to file to download and analyze.")], try_to_create_submission_for_x_times: Annotated[str, Field(..., description="How many attempts action should make to check if the API concurrency limit is not exceeded and try to create a new submission. Check is made every 2 seconds.")], wait_for_the_report: Annotated[bool, Field(default=None, description="Specify whether action should wait for the report creation. Report also can be obtained later with Get report action once scan is completed.")], os_version: Annotated[List[str], Field(default=None, description="OS version to run analysis on.")], operation_system_bitness: Annotated[List[str], Field(default=None, description="Bitness of Operation System")], os_environment_type: Annotated[List[str], Field(default=None, description="Environment type to run analysis on.")], network_connection_status: Annotated[List[str], Field(default=None, description="Network connection state for analysis.")], fake_net_feature_status: Annotated[List[str], Field(default=None, description="FakeNet feature state for analysis.")], use_tor: Annotated[List[str], Field(default=None, description="Use TOR or not while running analysis.")], opt_network_mitm: Annotated[List[str], Field(default=None, description="HTTPS MITM proxy option.")], opt_network_geo: Annotated[List[str], Field(default=None, description="Geo location option.")], opt_kernel_heavyevasion: Annotated[List[str], Field(default=None, description="Heavy evasion option.")], opt_privacy_type: Annotated[List[str], Field(default=None, description="Privacy settings for analysis.")], obj_ext_startfolder: Annotated[List[str], Field(default=None, description="Start location for analysis.")], opt_timeout: Annotated[str, Field(default=None, description="Timeout period for analysis in range from 10 to 9999 seconds.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create Any.Run file analysis task. Note: Action is not working with Siemplify entities, URL to file to analyze should be provided as action input parameter.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AnyRun")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AnyRun: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["URL to File"] = url_to_file
            if wait_for_the_report is not None:
                script_params["Wait for the report?"] = wait_for_the_report
            script_params["Try to create submission for x times"] = try_to_create_submission_for_x_times
            if os_version is not None:
                script_params["OS Version"] = os_version
            if operation_system_bitness is not None:
                script_params["Operation System Bitness"] = operation_system_bitness
            if os_environment_type is not None:
                script_params["OS Environment Type"] = os_environment_type
            if network_connection_status is not None:
                script_params["Network Connection Status"] = network_connection_status
            if fake_net_feature_status is not None:
                script_params["FakeNet Feature Status"] = fake_net_feature_status
            if use_tor is not None:
                script_params["Use TOR"] = use_tor
            if opt_network_mitm is not None:
                script_params["opt_network_mitm"] = opt_network_mitm
            if opt_network_geo is not None:
                script_params["opt_network_geo"] = opt_network_geo
            if opt_kernel_heavyevasion is not None:
                script_params["opt_kernel_heavyevasion"] = opt_kernel_heavyevasion
            if opt_privacy_type is not None:
                script_params["opt_privacy_type"] = opt_privacy_type
            if obj_ext_startfolder is not None:
                script_params["obj_ext_startfolder"] = obj_ext_startfolder
            if opt_timeout is not None:
                script_params["opt_timeout"] = opt_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AnyRun_AnalyzeFileURL",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AnyRun_AnalyzeFileURL",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action AnyRun_AnalyzeFileURL for AnyRun: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AnyRun")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def any_run_search_report_history(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_in_last_x_scans: Annotated[str, Field(..., description="Search for report in last x analyses executed in Any.Run.")], submission_name: Annotated[str, Field(default=None, description="Specific submission name to search for.")], skip_first_x_scans: Annotated[str, Field(default=None, description="Skip first x scans returned by Any.Run API.")], get_team_history: Annotated[bool, Field(default=None, description="Specify whether to get team history or not.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search Any.Run scans history. Note: Action is not working with Siemplify entities, only action input parameters are used.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AnyRun")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AnyRun: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if submission_name is not None:
                script_params["Submission Name"] = submission_name
            script_params["Search in last x scans"] = search_in_last_x_scans
            if skip_first_x_scans is not None:
                script_params["Skip first x scans"] = skip_first_x_scans
            if get_team_history is not None:
                script_params["Get team history?"] = get_team_history
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AnyRun_Search Report History",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AnyRun_Search Report History",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action AnyRun_Search Report History for AnyRun: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AnyRun")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def any_run_analyze_url(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], url_for_analysis: Annotated[str, Field(..., description="Specify URL to analyze. If URL is provided in both as entity and as this input parameter - action will be executed on input parameter.")], try_to_create_submission_for_x_times: Annotated[str, Field(..., description="How many attempts action should make to check if the API concurrency limit is not exceeded and try to create a new submission. Check is made every 2 seconds.")], wait_for_the_report: Annotated[bool, Field(default=None, description="Specify whether action should wait for the report creation. Report also can be obtained later with Get report action once scan is completed.")], os_version: Annotated[List[str], Field(default=None, description="OS version to run analysis on.")], operation_system_bitness: Annotated[List[str], Field(default=None, description="Bitness of Operation System")], os_environment_type: Annotated[List[str], Field(default=None, description="Environment type to run analysis on.")], network_connection_status: Annotated[List[str], Field(default=None, description="Network connection state for analysis.")], fake_net_feature_status: Annotated[List[str], Field(default=None, description="FakeNet feature state for analysis.")], use_tor: Annotated[List[str], Field(default=None, description="Use TOR or not while running analysis.")], opt_network_mitm: Annotated[List[str], Field(default=None, description="HTTPS MITM proxy option.")], opt_network_geo: Annotated[List[str], Field(default=None, description="Geo location option.")], opt_kernel_heavyevasion: Annotated[List[str], Field(default=None, description="Heavy evasion option.")], opt_privacy_type: Annotated[List[str], Field(default=None, description="Privacy settings for analysis.")], obj_ext_startfolder: Annotated[List[str], Field(default=None, description="Start location for analysis.")], opt_timeout: Annotated[str, Field(default=None, description="Timeout period for analysis in range from 10 to 9999 seconds.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create Any.Run analysis task for the provided URL. Note: URL can be provided either as a Siemplify URL entity (artifact) or as an action input parameter. If the URL is provided both as an entity and input parameter - action will be executed on the input parameter.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AnyRun")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AnyRun: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["URL For Analysis"] = url_for_analysis
            if wait_for_the_report is not None:
                script_params["Wait for the report?"] = wait_for_the_report
            script_params["Try to create submission for x times"] = try_to_create_submission_for_x_times
            if os_version is not None:
                script_params["OS Version"] = os_version
            if operation_system_bitness is not None:
                script_params["Operation System Bitness"] = operation_system_bitness
            if os_environment_type is not None:
                script_params["OS Environment Type"] = os_environment_type
            if network_connection_status is not None:
                script_params["Network Connection Status"] = network_connection_status
            if fake_net_feature_status is not None:
                script_params["FakeNet Feature Status"] = fake_net_feature_status
            if use_tor is not None:
                script_params["Use TOR"] = use_tor
            if opt_network_mitm is not None:
                script_params["opt_network_mitm"] = opt_network_mitm
            if opt_network_geo is not None:
                script_params["opt_network_geo"] = opt_network_geo
            if opt_kernel_heavyevasion is not None:
                script_params["opt_kernel_heavyevasion"] = opt_kernel_heavyevasion
            if opt_privacy_type is not None:
                script_params["opt_privacy_type"] = opt_privacy_type
            if obj_ext_startfolder is not None:
                script_params["obj_ext_startfolder"] = obj_ext_startfolder
            if opt_timeout is not None:
                script_params["opt_timeout"] = opt_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AnyRun_AnalyzeURL",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AnyRun_AnalyzeURL",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action AnyRun_AnalyzeURL for AnyRun: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AnyRun")
            return {"Status": "Failed", "Message": "No active instance found."}
