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
    # This function registers all tools (actions) for the CBLiveResponse integration.

    @mcp.tool()
    async def cb_live_response_create_memdump(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], file_name: Annotated[str, Field(default=None, description="Specify the file name for memdump creation. File name is case insensitive. File Name can be specified as a \"full path\" having both path and a file name, in that case Remote Directory Path parameter will not be used.")], remote_directory_path: Annotated[str, Field(default=None, description="Specify the directory file path to store the memdump. Example: C:\\TMP\\")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create memdump on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity. Note: The File name for the memdump to create can be provided either as a Siemplify File entity (artifact) or as an action input parameter. If the File name is passed to action both as an entity and input parameter - action will be executed on the input parameter. File name is case insensitive. File name will be appended to Remote Directory Path to get the resulting file paths that CB Cloud API accepts. Additionally, note that VMware CB API does not provide an error message if an unvalid Remote Directory Path is provided for the created memory dump.  File Name also can be specified as a "full path" having both path and a file name, or having file name and file path as separate parameters

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if file_name is not None:
                script_params["File Name"] = file_name
            if remote_directory_path is not None:
                script_params["Remote Directory Path"] = remote_directory_path
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Create Memdump",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Create Memdump",
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
                print(f"Error executing action CBLiveResponse_Create Memdump for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the VMware Carbon Black Endpoint Standard Live Response with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
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
                actionName="CBLiveResponse_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Ping",
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
                print(f"Error executing action CBLiveResponse_Ping for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_execute_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], file_name: Annotated[str, Field(default=None, description="Specify the file name to execute. File name is case insensitive. File Name can be specified as a \"full path\" having both path and a file name, in that case Remote Directory Path parameter will not be used.")], remote_directory_path: Annotated[str, Field(default=None, description="Specify the remote directory path for the file to execute. Example: C:\\TMP\\")], output_log_file_on_remote_host: Annotated[str, Field(default=None, description="Specify the output log file action should save the redirected output to. Example: C:\\TMP\\cmdoutput.log")], command_arguments_to_pass_to_file: Annotated[str, Field(default=None, description="Specify the command arguments to pass for executing the file. Example, here we specify \"/C whoami\" to execute whoami command with cmd: C:\\Windows\\system32\\cmd.exe /C whoami")], wait_for_the_result: Annotated[bool, Field(default=None, description="If enabled, action will wait for the command to complete.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute file on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity. Note: The File name can be provided either as a Siemplify File entity (artifact) or as an action input parameter. If the File name is passed to action both as an entity and input parameter - action will be executed on the input parameter. File name is case insensitive. File name will be appended to Remote Directory Path to get the resulting file paths that CB Cloud API accepts. File Name also can be specified as a "full path" having both path and a file name, or having file name and file path as separate parameters

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if file_name is not None:
                script_params["File Name"] = file_name
            if remote_directory_path is not None:
                script_params["Remote Directory Path"] = remote_directory_path
            if output_log_file_on_remote_host is not None:
                script_params["Output Log File on Remote Host"] = output_log_file_on_remote_host
            if command_arguments_to_pass_to_file is not None:
                script_params["Command Arguments to Pass to File"] = command_arguments_to_pass_to_file
            if wait_for_the_result is not None:
                script_params["Wait for the Result"] = wait_for_the_result
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Execute File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Execute File",
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
                print(f"Error executing action CBLiveResponse_Execute File for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_list_processes(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], process_name: Annotated[str, Field(default=None, description="Process name to search for on the host.")], how_many_records_to_return: Annotated[str, Field(default=None, description="How many records per entity action should return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List processes running on endpoint based on the provided Siemplify Host or IP entity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if process_name is not None:
                script_params["Process Name"] = process_name
            if how_many_records_to_return is not None:
                script_params["How Many Records To Return"] = how_many_records_to_return
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_List Processes",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_List Processes",
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
                print(f"Error executing action CBLiveResponse_List Processes for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_kill_process(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], process_name: Annotated[str, Field(default=None, description="Process name to search PID for.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Kill process on a host based on the Siemplify Host or IP entity. Note: The Process name can be provided either as a Siemplify entity (artifact) or as an action input parameter. If the Process name is passed to action both as an entity (process) and input parameter - action will be executed on the input parameter.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if process_name is not None:
                script_params["Process Name"] = process_name
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Kill Process",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Kill Process",
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
                print(f"Error executing action CBLiveResponse_Kill Process for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_list_files(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], remote_directory_path: Annotated[str, Field(..., description="Specify the target directory path action should list. Example: C:\\TMP\\ or /tmp/")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many rows action should return.")], start_from_row: Annotated[str, Field(default=None, description="Specify from which row action should start to return data.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List files on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Remote Directory Path"] = remote_directory_path
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
            if start_from_row is not None:
                script_params["Start from Row"] = start_from_row
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_List Files",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_List Files",
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
                print(f"Error executing action CBLiveResponse_List Files for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_download_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], local_directory_path: Annotated[str, Field(..., description="Specify the local directory path action should save the file to. Example: /tmp/")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], file_name: Annotated[str, Field(default=None, description="Specify the file name to download. File name is case insensitive. File Name can be specified as a \"full path\" having both path and a file name, in that case Remote Directory Path parameter will not be used.")], remote_directory_path: Annotated[str, Field(default=None, description="Specify the remote directory path action should take to download the file. Example: C:\\TMP\\")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Download a file from a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity. Note: The File name can be provided either as a Siemplify File entity (artifact) or as an action input parameter. If the File name is passed to action both as an entity and input parameter - action will be executed on the input parameter. File name is case insensitive. File name will be appended to both Local Directory Path and Remote Directory Path to get the resulting file paths that CB Cloud API accepts. If action is executed against multiple Host or IP entities, to not overwrite the file downloaded from multiple entities, the downloaded file name is appended with Hostname or IP address, example format: hostname_filename. File Name also can be specified as a "full path" having both path and a file name, or having file name and file path as separate parameters

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if file_name is not None:
                script_params["File Name"] = file_name
            if remote_directory_path is not None:
                script_params["Remote Directory Path"] = remote_directory_path
            script_params["Local Directory Path"] = local_directory_path
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Download File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Download File",
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
                print(f"Error executing action CBLiveResponse_Download File for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_list_files_in_cloud_storage(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many rows action should return.")], start_from_row: Annotated[str, Field(default=None, description="Specify from which row action should start to return data.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List files in the VMware Carbon Black Cloud file storage for an existing live response session based on the Siemplify Host or IP entity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
            if start_from_row is not None:
                script_params["Start from Row"] = start_from_row
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_List Files in Cloud Storage",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_List Files in Cloud Storage",
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
                print(f"Error executing action CBLiveResponse_List Files in Cloud Storage for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_put_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], destination_directory_path: Annotated[str, Field(..., description="Specify the target directory path action should upload the file to. Example: C:\\TMP\\")], file_name: Annotated[str, Field(default=None, description="Specify the file name to upload. File name is case insensitive. File Name can be specified as a \"full path\" having both path and a file name, in that case Source Directory Path parameter will not be used.")], source_directory_path: Annotated[str, Field(default=None, description="Specify the source directory path action should take to get the file to upload. Example: /tmp/")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Put a file on a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity. Note: The File name can be provided either as a Siemplify File entity (artifact) or as an action input parameter. If the File name is passed to action both as an entity and input parameter - action will be executed on the input parameter. File name is case insensitive. File name will be appended to both Source Directory Path and Destination Directory Path to get the resulting file paths that CB Cloud API accepts. File Name also can be specified as a "full path" having both path and a file name, or having file name and file path as separate parameters

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if file_name is not None:
                script_params["File Name"] = file_name
            script_params["Check for active session x times"] = check_for_active_session_x_times
            if source_directory_path is not None:
                script_params["Source Directory Path"] = source_directory_path
            script_params["Destination Directory Path"] = destination_directory_path
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Put File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Put File",
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
                print(f"Error executing action CBLiveResponse_Put File for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_delete_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], remote_directory_path: Annotated[str, Field(default=None, description="Specify the remote directory path to file to delete. Example: C:\\TMP\\")], file_name: Annotated[str, Field(default=None, description="Specify the file name to delete. File name is case insensitive. File Name can be specified as a \"full path\" having both path and a file name, in that case Remote Directory Path parameter will not be used.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete a file from a host running VMware CB Cloud Agent based on the Siemplify Host or IP entity. Note: The File name can be provided either as a Siemplify File entity (artifact) or as an action input parameter. If the File name is passed to action both as an entity and input parameter - action will be executed on the input parameter. File name is case insensitive. File name will be appended to Remote Directory Path to get the resulting file paths that CB Cloud API accepts. File Name also can be specified as a "full path" having both path and a file name, or having file name and file path as separate parameters

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if remote_directory_path is not None:
                script_params["Remote Directory Path"] = remote_directory_path
            if file_name is not None:
                script_params["File Name"] = file_name
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Delete File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Delete File",
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
                print(f"Error executing action CBLiveResponse_Delete File for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cb_live_response_delete_file_from_cloud_storage(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], check_for_active_session_x_times: Annotated[str, Field(..., description="How many attempts action should make to get active session for the entity. Check is made every 2 seconds.")], file_name: Annotated[str, Field(default=None, description="Specify the file name to delete. File name is case insensitive.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete a file from the VMware Carbon Black Cloud file storage for an existing live response session based on the Siemplify Host or IP entity. Note: This action is not supported in Carbon Black Live Response API v3, API v6 should be used to run this action. The File name can be provided either as a Siemplify File entity (artifact) or as an action input parameter. If the File name is passed to action both as an entity and input parameter - action will be executed on the input parameter. File name is case insensitive.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CBLiveResponse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CBLiveResponse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if file_name is not None:
                script_params["File Name"] = file_name
            script_params["Check for active session x times"] = check_for_active_session_x_times
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CBLiveResponse_Delete File from Cloud Storage",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CBLiveResponse_Delete File from Cloud Storage",
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
                print(f"Error executing action CBLiveResponse_Delete File from Cloud Storage for CBLiveResponse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CBLiveResponse")
            return {"Status": "Failed", "Message": "No active instance found."}
