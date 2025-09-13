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
    # This function registers all tools (actions) for the FileOperation integration.

    @mcp.tool()
    async def file_operation_transfer_file_linux_to_windows(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_linux_file_path: Annotated[str, Field(..., description="The remote server folder with the relevant files. Full path")], source_linux_ip: Annotated[str, Field(..., description="x.x.x.x")], source_linux_username: Annotated[str, Field(..., description="")], source_linux_password: Annotated[str, Field(..., description="")], dest_win_path: Annotated[str, Field(..., description="The server folder to put the files into")], keep_file: Annotated[bool, Field(..., description="Indicates weather to keep the file in source or remove it")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Transfer file from windows share to remote Linux host

Action Parameters: source_linux_file_path: The remote server folder with the relevant files. Full path., source_linux_ip: x.x.x.x, source_linux_username: , source_linux_password: , dest_win_path: The server folder to put the files into., keep_file: Indicates weather to keep the file in source or remove it.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["source_linux_file_path"] = source_linux_file_path
            script_params["source_linux_ip"] = source_linux_ip
            script_params["source_linux_username"] = source_linux_username
            script_params["source_linux_password"] = source_linux_password
            script_params["dest_win_path"] = dest_win_path
            script_params["keep_file"] = keep_file
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Transfer File Linux To Windows",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Transfer File Linux To Windows",
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
                print(f"Error executing action FileOperation_Transfer File Linux To Windows for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_transfer_file_linux_to_linux(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_linux_file_path: Annotated[str, Field(..., description="The remote server folder with the relevant files. Full path")], source_linux_ip: Annotated[str, Field(..., description="x.x.x.x")], source_linux_username: Annotated[str, Field(..., description="")], source_linux_password: Annotated[str, Field(..., description="")], dest_linux_path: Annotated[str, Field(..., description="The remote server folder to put the files into")], dest_linux_ip: Annotated[str, Field(..., description="x.x.x.x")], dest_linux_username: Annotated[str, Field(..., description="")], dest_linux_password: Annotated[str, Field(..., description="")], keep_file: Annotated[bool, Field(..., description="Indicates weather to keep the file in source or remove it")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Transfer file from remote linux host to another remote linux host

Action Parameters: source_linux_file_path: The remote server folder with the relevant files. Full path., source_linux_ip: x.x.x.x, source_linux_username: , source_linux_password: , dest_linux_path: The remote server folder to put the files into., dest_linux_ip: x.x.x.x, dest_linux_username: , dest_linux_password: , keep_file: Indicates weather to keep the file in source or remove it.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["source_linux_file_path"] = source_linux_file_path
            script_params["source_linux_ip"] = source_linux_ip
            script_params["source_linux_username"] = source_linux_username
            script_params["source_linux_password"] = source_linux_password
            script_params["dest_linux_path"] = dest_linux_path
            script_params["dest_linux_ip"] = dest_linux_ip
            script_params["dest_linux_username"] = dest_linux_username
            script_params["dest_linux_password"] = dest_linux_password
            script_params["keep_file"] = keep_file
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Transfer File Linux To Linux",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Transfer File Linux To Linux",
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
                print(f"Error executing action FileOperation_Transfer File Linux To Linux for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_transfer_file_windows_to_linux(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_win_file_path: Annotated[str, Field(..., description="The server folder with the relevant files. Full path")], dest_linux_path: Annotated[str, Field(..., description="The remote server folder to put the files into")], dest_linux_ip: Annotated[str, Field(..., description="x.x.x.x")], dest_linux_username: Annotated[str, Field(..., description="")], dest_linux_password: Annotated[str, Field(..., description="")], keep_file: Annotated[bool, Field(..., description="Indicates weather to keep the file in source or remove it")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Transfer file from windows share to a remote Linux host

Action Parameters: source_win_file_path: The server folder with the relevant files. Full path., dest_linux_path: The remote server folder to put the files into., dest_linux_ip: x.x.x.x, dest_linux_username: , dest_linux_password: , keep_file: Indicates weather to keep the file in source or remove it.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["source_win_file_path"] = source_win_file_path
            script_params["dest_linux_path"] = dest_linux_path
            script_params["dest_linux_ip"] = dest_linux_ip
            script_params["dest_linux_username"] = dest_linux_username
            script_params["dest_linux_password"] = dest_linux_password
            script_params["keep_file"] = keep_file
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Transfer File Windows To Linux",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Transfer File Windows To Linux",
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
                print(f"Error executing action FileOperation_Transfer File Windows To Linux for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_zip_files_linux(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], server_ip: Annotated[str, Field(..., description="x.x.x.x")], username: Annotated[str, Field(..., description="")], password: Annotated[str, Field(..., description="")], source_folder: Annotated[str, Field(..., description="The remote server folder with the relevant files")], file_filter: Annotated[str, Field(..., description="files extension to include in zip file {ex: *.txt}")], output_folder: Annotated[str, Field(..., description="The remote server folder to put the zip file into")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a zip file from source folder files in a remote Linux host

Action Parameters: server_ip: x.x.x.x, username: , password: , source_folder: The remote server folder with the relevant files., file_filter: Files extension to include in zip file {ex: *.txt}., output_folder: The remote server folder to put the zip file into.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["server_ip"] = server_ip
            script_params["username"] = username
            script_params["password"] = password
            script_params["source_folder"] = source_folder
            script_params["file_filter"] = file_filter
            script_params["output_folder"] = output_folder
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Zip Files Linux",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Zip Files Linux",
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
                print(f"Error executing action FileOperation_Zip Files Linux for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_tarzip_files_windows(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_folder: Annotated[str, Field(default=None, description="The full path to the folder with the relevant files")], file_filter: Annotated[str, Field(default=None, description="iles extension to include in targzip file {ex: *.txt}")], output_folder: Annotated[str, Field(default=None, description="The path to the folder to put the zip file into")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Compress a tarzip file on windows share

Action Parameters: source_folder: The full path to the folder with the relevant files., file_filter: Files extension to include in targzip file {Example: *.txt}., output_folder: The path to the folder to put the zip file into.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if source_folder is not None:
                script_params["source_folder"] = source_folder
            if file_filter is not None:
                script_params["file_filter"] = file_filter
            if output_folder is not None:
                script_params["output_folder"] = output_folder
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Tarzip Files Windows",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Tarzip Files Windows",
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
                print(f"Error executing action FileOperation_Tarzip Files Windows for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_tarzip_files_linux(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], server_ip: Annotated[str, Field(..., description="x.x.x.x")], username: Annotated[str, Field(..., description="")], password: Annotated[str, Field(..., description="")], source_folder: Annotated[str, Field(..., description="The remote server folder with the relevant files. Full path")], file_filter: Annotated[str, Field(..., description="files extension to include in zip file {ex: *.txt}")], output_folder: Annotated[str, Field(..., description="The remote server folder to put the zip file into")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create zip file on a remote Linux host

Action Parameters: server_ip: x.x.x.x, username: , password: , source_folder: The remote server folder with the relevant files. Full path., file_filter: files extension to include in zip file {Example: *.txt}., output_folder: The remote server folder to put the zip file into.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["server_ip"] = server_ip
            script_params["username"] = username
            script_params["password"] = password
            script_params["source_folder"] = source_folder
            script_params["file_filter"] = file_filter
            script_params["output_folder"] = output_folder
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Tarzip Files Linux",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Tarzip Files Linux",
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
                print(f"Error executing action FileOperation_Tarzip Files Linux for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_transfer_file_windows_to_windows(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_win_file_path: Annotated[str, Field(..., description="The folder with the relevant files. Full path")], dest_win_path: Annotated[str, Field(..., description="The folder to put the files into")], keep_file: Annotated[str, Field(..., description="Indicates weather to keep the file in source or remove it")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Transfer file between two windows shares

Action Parameters: source_win_file_path: The folder with the relevant files. Full path., dest_win_path: The folder to put the files into., keep_file: Indicates weather to keep the file in source or remove it.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["source_win_file_path"] = source_win_file_path
            script_params["dest_win_path"] = dest_win_path
            script_params["keep_file"] = keep_file
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Transfer File Windows To Windows",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Transfer File Windows To Windows",
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
                print(f"Error executing action FileOperation_Transfer File Windows To Windows for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
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
                actionName="FileOperation_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Ping",
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
                print(f"Error executing action FileOperation_Ping for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def file_operation_zip_files_windows(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], source_folder: Annotated[str, Field(..., description="The folder with the relevant files")], file_filter: Annotated[str, Field(..., description="files extension to include in zip file {ex: *.txt}")], output_folder: Annotated[str, Field(..., description="The folder to put the zip file into")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a zip file from source windows share files

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FileOperation")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FileOperation: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["source_folder"] = source_folder
            script_params["file_filter"] = file_filter
            script_params["output_folder"] = output_folder
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FileOperation_Zip Files Windows",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FileOperation_Zip Files Windows",
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
                print(f"Error executing action FileOperation_Zip Files Windows for FileOperation: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FileOperation")
            return {"Status": "Failed", "Message": "No active instance found."}
