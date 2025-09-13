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
    # This function registers all tools (actions) for the Endgame integration.

    @mcp.tool()
    async def endgame_collect_autoruns(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many autoruns to return.")], category_all: Annotated[bool, Field(default=None, description="If enabled, search for all autorun categories")], category_network_provider: Annotated[bool, Field(default=None, description="If enabled, search for \"Network Provider\" autorun category")], category_office: Annotated[bool, Field(default=None, description="If enabled, search for \"Office\" autorun category")], category_driver: Annotated[bool, Field(default=None, description="If enabled, search for \"Driver\" autorun category")], category_app_init: Annotated[bool, Field(default=None, description="If enabled, search for \"App Init\" autorun category")], category_winlogon: Annotated[bool, Field(default=None, description="If enabled, search for \"Winlogon\" autorun category")], category_print_monitor: Annotated[bool, Field(default=None, description="If enabled, search for \"Print Monitor\" autorun category")], category_ease_of_access: Annotated[bool, Field(default=None, description="If enabled, search for \"Ease of Access\" autorun category")], category_wmi: Annotated[bool, Field(default=None, description="If enabled, search for \"WMI\" autorun category")], category_lsa_provider: Annotated[bool, Field(default=None, description="If enabled, search for \"LSA Provider\" autorun category")], category_service: Annotated[bool, Field(default=None, description="If enabled, search for \"Service\" autorun category")], category_bits: Annotated[bool, Field(default=None, description="If enabled, search for \"Bits\" autorun category")], category_known_dll: Annotated[bool, Field(default=None, description="If enabled, search for \"Known dll\" autorun category")], category_print_provider: Annotated[bool, Field(default=None, description="If enabled, search for \"Print Provider\" autorun category")], category_image_hijack: Annotated[bool, Field(default=None, description="If enabled, search for \"Image Hijack\" autorun category")], category_startup_folder: Annotated[bool, Field(default=None, description="If enabled, search for \"Startup Folder\" autorun category")], category_internet_explorer: Annotated[bool, Field(default=None, description="If enabled, search for \"Internet Explorer\" autorun category")], category_codec: Annotated[bool, Field(default=None, description="If enabled, search for \"Codec\" autorun category")], category_logon: Annotated[bool, Field(default=None, description="If enabled, search for \"Logon\" autorun category")], category_search_order_hijack: Annotated[bool, Field(default=None, description="If enabled, search for \"Search Order Hijack\" autorun category")], category_winsock_provider: Annotated[bool, Field(default=None, description="If enabled, search for \"Winsock Provider\" autorun category")], category_boot_execute: Annotated[bool, Field(default=None, description="If enabled, search for \"Boot Execute\" autorun category")], category_phantom_dll: Annotated[bool, Field(default=None, description="If enabled, search for \"Phantom dll\" autorun category")], category_com_hijack: Annotated[bool, Field(default=None, description="If enabled, search for \"Com Hijack\" autorun category")], category_explorer: Annotated[bool, Field(default=None, description="If enabled, search for \"Explorer\" autorun category")], category_scheduled_task: Annotated[bool, Field(default=None, description="If enabled, search for \"Scheduled Task\" autorun category")], include_all_metadata: Annotated[bool, Field(default=None, description="If enabled, provides all available data")], include_malware_classification_metadata: Annotated[bool, Field(default=None, description="If enabled, provides information about MalwareScore")], include_authenticode_metadata: Annotated[bool, Field(default=None, description="If enabled, provides Signer Information")], include_md5_hash: Annotated[bool, Field(default=None, description="If enabled, provides MD5 hash in the response")], include_sha_1_hash: Annotated[bool, Field(default=None, description="If enabled, provides SHA-1 hash in the response")], include_sha_256_hash: Annotated[bool, Field(default=None, description="If enabled, provides SHA-256 hash in the response")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Collect Autoruns from Endgame endpoints (Windows only).

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
            if category_all is not None:
                script_params['Category "All"'] = category_all
            if category_network_provider is not None:
                script_params['Category "Network Provider"'] = category_network_provider
            if category_office is not None:
                script_params['Category "Office"'] = category_office
            if category_driver is not None:
                script_params['Category "Driver"'] = category_driver
            if category_app_init is not None:
                script_params['Category "App Init"'] = category_app_init
            if category_winlogon is not None:
                script_params['Category "Winlogon"'] = category_winlogon
            if category_print_monitor is not None:
                script_params['Category "Print Monitor"'] = category_print_monitor
            if category_ease_of_access is not None:
                script_params['Category "Ease of Access"'] = category_ease_of_access
            if category_wmi is not None:
                script_params['Category "WMI"'] = category_wmi
            if category_lsa_provider is not None:
                script_params['Category "LSA Provider"'] = category_lsa_provider
            if category_service is not None:
                script_params['Category "Service"'] = category_service
            if category_bits is not None:
                script_params['Category "Bits"'] = category_bits
            if category_known_dll is not None:
                script_params['Category "Known dll"'] = category_known_dll
            if category_print_provider is not None:
                script_params['Category "Print Provider"'] = category_print_provider
            if category_image_hijack is not None:
                script_params['Category "Image Hijack"'] = category_image_hijack
            if category_startup_folder is not None:
                script_params['Category "Startup Folder"'] = category_startup_folder
            if category_internet_explorer is not None:
                script_params['Category "Internet Explorer"'] = category_internet_explorer
            if category_codec is not None:
                script_params['Category "Codec"'] = category_codec
            if category_logon is not None:
                script_params['Category "Logon"'] = category_logon
            if category_search_order_hijack is not None:
                script_params['Category "Search Order Hijack"'] = category_search_order_hijack
            if category_winsock_provider is not None:
                script_params['Category "Winsock Provider"'] = category_winsock_provider
            if category_boot_execute is not None:
                script_params['Category "Boot Execute"'] = category_boot_execute
            if category_phantom_dll is not None:
                script_params['Category "Phantom dll"'] = category_phantom_dll
            if category_com_hijack is not None:
                script_params['Category "Com Hijack"'] = category_com_hijack
            if category_explorer is not None:
                script_params['Category "Explorer"'] = category_explorer
            if category_scheduled_task is not None:
                script_params['Category "Scheduled Task"'] = category_scheduled_task
            if include_all_metadata is not None:
                script_params["Include All Metadata"] = include_all_metadata
            if include_malware_classification_metadata is not None:
                script_params["Include Malware Classification Metadata"] = include_malware_classification_metadata
            if include_authenticode_metadata is not None:
                script_params["Include Authenticode Metadata"] = include_authenticode_metadata
            if include_md5_hash is not None:
                script_params["Include MD5 Hash"] = include_md5_hash
            if include_sha_1_hash is not None:
                script_params["Include SHA-1 Hash"] = include_sha_1_hash
            if include_sha_256_hash is not None:
                script_params["Include SHA-256 Hash"] = include_sha_256_hash
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Collect Autoruns",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Collect Autoruns",
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
                print(f"Error executing action Endgame_Collect Autoruns for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_isolate_host(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, creates Insight after successful execution of this action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Initiate Endgame endpoint isolation. This action supports only Windows and MacOS endpoints.

Action Parameters: Create Insight: If enabled, creates an Insight after successful execution of this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Isolate Host",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Isolate Host",
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
                print(f"Error executing action Endgame_Isolate Host for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_hunt_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], endpoints_core_os: Annotated[str, Field(default=None, description="Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.")], find_username: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter username(s), separate multiple entries with a semicolon.")], domain_name: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter Domain Name")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Searches the network for logged in users.

Action Parameters: Endpoints Core OS: Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system., Find Username: ADVANCED CONFIGURATION for this hunt. Enter username(s), separate multiple entries with a semicolon., Domain Name: ADVANCED CONFIGURATION for this hunt. Enter Domain Name.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if endpoints_core_os is not None:
                script_params["Endpoints Core OS"] = endpoints_core_os
            if find_username is not None:
                script_params["Find Username"] = find_username
            if domain_name is not None:
                script_params["Domain Name"] = domain_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Hunt User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Hunt User",
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
                print(f"Error executing action Endgame_Hunt User for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_add_ip_subnet_to_host_isolation_config(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ip_subnet: Annotated[str, Field(..., description="Enter the IPv4 Subnet that you want to add to Host Isolation Config.")], description: Annotated[str, Field(default=None, description="Enter the description to the IP Subnet.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, creates Insight after successful execution of this action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add IP subnet to Host Isolation Config defined in the Endgame.

Action Parameters: IP Subnet: Enter the IPv4 Subnet that you want to add to Host Isolation Config., Description: Enter the description to the IP Subnet., Create Insight: If enabled, creates Insight after successful execution of this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["IP Subnet"] = ip_subnet
            if description is not None:
                script_params["Description"] = description
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Add IP Subnet to Host Isolation Config",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Add IP Subnet to Host Isolation Config",
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
                print(f"Error executing action Endgame_Add IP Subnet to Host Isolation Config for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_get_investigation_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], investigation_id: Annotated[str, Field(..., description="Specify Endgame Investigation ID to search for.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information on a specific Endgame Investigation.

Action Parameters: Investigation ID: Specify Endgame investigation ID to search for.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Investigation ID"] = investigation_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Get Investigation Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Get Investigation Details",
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
                print(f"Error executing action Endgame_Get Investigation Details for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_remove_ip_subnet_from_host_isolation_config(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ip_subnet: Annotated[str, Field(..., description="Enter the IPv4 Subnet that you want to remove from Host Isolation Config.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, creates Insight after successful execution of this action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Remove IP subnet from Host Isolation Config defined in the Endgame.

Action Parameters: IP Subnet: Enter the IPv4 Subnet that you want to add to Host Isolation Config., Create Insight: If enabled, creates Insight after successful execution of this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["IP Subnet"] = ip_subnet
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Remove IP Subnet from Host Isolation Config",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Remove IP Subnet from Host Isolation Config",
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
                print(f"Error executing action Endgame_Remove IP Subnet from Host Isolation Config for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_system_survey(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], include_security_product_information_windows_only: Annotated[bool, Field(default=None, description="Specify to get information about the security products installed on the endpoint (Windows only).")], include_patch_information_windows_only: Annotated[bool, Field(default=None, description="Specify to get information about patches (Windows only).")], include_disk_information: Annotated[bool, Field(default=None, description="Specify to get information about Disks.")], include_network_interface_information: Annotated[bool, Field(default=None, description="Specify to get information about network interfaces.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get system information on a single endgame endpoint, such as memory use, dns, and OS.

Action Parameters: Max Items to Return: Specify how many items to return., Include Security Product Information (Windows only): Specify to get information about the security products installed on the endpoint (Windows only)., Include Patch Information (Windows only): Specify to get information about patches (Windows only)., Include Disk Information: Specify to get information about Disks., Include Network Interface Information: Specify to get information about network interfaces.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
            if include_security_product_information_windows_only is not None:
                script_params["Include Security Product Information (Windows only)"] = include_security_product_information_windows_only
            if include_patch_information_windows_only is not None:
                script_params["Include Patch Information (Windows only)"] = include_patch_information_windows_only
            if include_disk_information is not None:
                script_params["Include Disk Information"] = include_disk_information
            if include_network_interface_information is not None:
                script_params["Include Network Interface Information"] = include_network_interface_information
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_System Survey",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_System Survey",
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
                print(f"Error executing action Endgame_System Survey for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_hunt_process(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], endpoints_core_os: Annotated[str, Field(default=None, description="Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.")], md5_hashes: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter MD5 Hashes, separated by comma")], sha1_hashes: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter SHA1 Hashes, separated by comma")], sha256_hashes: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter SHA256 Hashes, separated by comma")], process_name: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter Process Name ex. iss.exe")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Searches for running processes.

Action Parameters: Endpoints Core OS: Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system., MD5 Hashes: ADVANCED CONFIGURATION for this hunt. Enter MD5 Hashes, separated by comma., SHA1 Hashes: ADVANCED CONFIGURATION for this hunt. Enter SHA-1 Hashes, separated by comma., SHA256 Hashes: ADVANCED CONFIGURATION for this hunt. Enter SHA256 Hashes, separated by comma., Process Name: ADVANCED CONFIGURATION for this hunt. Enter Process Name ex. iss.exe*

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if endpoints_core_os is not None:
                script_params["Endpoints Core OS"] = endpoints_core_os
            if md5_hashes is not None:
                script_params["MD5 Hashes"] = md5_hashes
            if sha1_hashes is not None:
                script_params["SHA1 Hashes"] = sha1_hashes
            if sha256_hashes is not None:
                script_params["SHA256 Hashes"] = sha256_hashes
            if process_name is not None:
                script_params["Process Name"] = process_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Hunt Process",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Hunt Process",
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
                print(f"Error executing action Endgame_Hunt Process for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_firewall_survey_windows_only(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about the firewall rules on a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many items to return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Firewall Survey (Windows only)",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Firewall Survey (Windows only)",
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
                print(f"Error executing action Endgame_Firewall Survey (Windows only) for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_unisolate_host(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, creates Insight after successful execution of this action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Initiate Endgame endpoint unisolation. This action supports only Windows and MacOS endpoints.

Action Parameters: Create Insight: If enabled, creates an Insight after successful execution of this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Unisolate Host",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Unisolate Host",
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
                print(f"Error executing action Endgame_Unisolate Host for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_list_investigations(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], os: Annotated[str, Field(default=None, description="Specify for which OS you want to list investigations. Parameter can take multiple values as a comma separated string.")], fetch_investigations_for_the_last_x_hours: Annotated[str, Field(default=None, description="Return investigations created for the specified time frame in hours.")], max_investigation_to_return: Annotated[str, Field(default=None, description="Specify how many investigation you want to query.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
List Endgame Investigations.

Action Parameters: OS: Specify for which OS you want to list investigations. Parameter can take multiple values as a comma-separated string., Fetch investigations for the last X hours: Return investigations created for the specified timeframe in hours., Max Investigation to Return: Specify how many investigation you want to query.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if os is not None:
                script_params["OS"] = os
            if fetch_investigations_for_the_last_x_hours is not None:
                script_params["Fetch investigations for the last X hours"] = fetch_investigations_for_the_last_x_hours
            if max_investigation_to_return is not None:
                script_params["Max Investigation to Return"] = max_investigation_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_List Investigations",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_List Investigations",
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
                print(f"Error executing action Endgame_List Investigations for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Endgame

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
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
                actionName="Endgame_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Ping",
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
                print(f"Error executing action Endgame_Ping for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_get_host_isolation_config(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get Host Isolation Config defined in the Endgame.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
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
                actionName="Endgame_Get Host Isolation Config",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Get Host Isolation Config",
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
                print(f"Error executing action Endgame_Get Host Isolation Config for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_get_endpoints(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List all endpoints.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
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
                actionName="Endgame_Get Endpoints",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Get Endpoints",
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
                print(f"Error executing action Endgame_Get Endpoints for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_process_survey(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], detect_fileless_attacks_windows_only: Annotated[bool, Field(default=None, description="Specify to detect fileless attacks. Windows Only.")], detect_malware_with_malware_score_windows_only: Annotated[bool, Field(default=None, description="Specify to detect malware processes with MalwareScore. Windows Only.")], collect_process_threads: Annotated[bool, Field(default=None, description="Specify to include information about the amount of process threads in the response.")], return_only_suspicious_processes: Annotated[bool, Field(default=None, description="Specify to return only suspicious processes from the endpoint. By the Endgame definition: Suspicious processes are unbacked executable processes.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about running processes on a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many items to return., Detect Fileless Attacks (Windows Only): Specify to detect fileless attacks. Windows Only., Detect Malware With MalwareScore (Windows Only): Specify to detect malware processes with MalwareScore. Windows Only., Collect Process Threads: Specify to include information about the amount of process threads in the response., Return Only Suspicious Processes: Specify to return only suspicious processes from the endpoint. By the Endgame definition: Suspicious processes are unbacked executable processes.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
            if detect_fileless_attacks_windows_only is not None:
                script_params["Detect Fileless Attacks (Windows Only)"] = detect_fileless_attacks_windows_only
            if detect_malware_with_malware_score_windows_only is not None:
                script_params["Detect Malware With MalwareScore (Windows Only)"] = detect_malware_with_malware_score_windows_only
            if collect_process_threads is not None:
                script_params["Collect Process Threads"] = collect_process_threads
            if return_only_suspicious_processes is not None:
                script_params["Return Only Suspicious Processes"] = return_only_suspicious_processes
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Process Survey",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Process Survey",
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
                print(f"Error executing action Endgame_Process Survey for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_drivers_survey_windows_only(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get the information on drivers from a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many items to return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Drivers Survey (Windows only)",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Drivers Survey (Windows only)",
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
                print(f"Error executing action Endgame_Drivers Survey (Windows only) for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_kill_process(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], process_name: Annotated[str, Field(..., description="Enter the process name.")], pid: Annotated[str, Field(default=None, description="Enter ID of the process.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Kill a process in a specific Endgame endpoint.

Action Parameters: Process Name: Enter the process name, PID: Enter ID of the process.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Process Name"] = process_name
            if pid is not None:
                script_params["PID"] = pid
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Kill Process",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Kill Process",
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
                print(f"Error executing action Endgame_Kill Process for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_user_sessions_survey(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about an active user sessions on a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many items to return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_User Sessions Survey",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_User Sessions Survey",
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
                print(f"Error executing action Endgame_User Sessions Survey for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_network_survey(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], include_route_entries_information: Annotated[bool, Field(default=None, description="Specify to get information about the Route Entries.")], include_net_bios_information: Annotated[bool, Field(default=None, description="Specify to get information about Net Bios.")], include_dns_cache_information: Annotated[bool, Field(default=None, description="Specify to get information about the DNS Cache.")], include_arp_table_information: Annotated[bool, Field(default=None, description="Specify to get information about the ARP table.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about connections, DNS cache, Net Bios, ARP, and Route tables from a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many autoruns to return., Include Route Entries Information: Specify to get information about the Route Entries., Include Net Bios Information: Specify to get information about Net Bios., Include DNS Cache Information: Specify to get information about the DNS Cache., Include ARP Table Information: Specify to get information about the ARP table.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
            if include_route_entries_information is not None:
                script_params["Include Route Entries Information"] = include_route_entries_information
            if include_net_bios_information is not None:
                script_params["Include Net Bios Information"] = include_net_bios_information
            if include_dns_cache_information is not None:
                script_params["Include DNS Cache Information"] = include_dns_cache_information
            if include_arp_table_information is not None:
                script_params["Include ARP Table Information"] = include_arp_table_information
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Network Survey",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Network Survey",
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
                print(f"Error executing action Endgame_Network Survey for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_hunt_ip(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], endpoints_core_os: Annotated[str, Field(default=None, description="Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.")], remote_ip_address: Annotated[str, Field(default=None, description="remote IP address - separated by comma")], local_ip_address: Annotated[str, Field(default=None, description="separated by comma")], state: Annotated[str, Field(default=None, description="Enter state to return. Ex. ANY")], protocol: Annotated[str, Field(default=None, description="Ex. ANY, UDP, TCP")], network_port: Annotated[str, Field(default=None, description="ul")], network_remote: Annotated[str, Field(default=None, description="Network Remote or Local")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Searches for network connections.

Action Parameters: Endpoints Core OS: Select an operating system (for example, Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system., Remote IP Address: remote IP address - separated by comma, Local IP Address: separated by comma, State: Enter state to return. Example: ANY, Protocol: Example: ANY, UDP, TCP, Network Port: , Network Remote: Network Remote or Local.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if endpoints_core_os is not None:
                script_params["Endpoints Core OS"] = endpoints_core_os
            if remote_ip_address is not None:
                script_params["Remote IP Address"] = remote_ip_address
            if local_ip_address is not None:
                script_params["Local IP Address"] = local_ip_address
            if state is not None:
                script_params["State"] = state
            if protocol is not None:
                script_params["Protocol"] = protocol
            if network_port is not None:
                script_params["Network Port"] = network_port
            if network_remote is not None:
                script_params["Network Remote"] = network_remote
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Hunt IP",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Hunt IP",
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
                print(f"Error executing action Endgame_Hunt IP for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_hunt_registry(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hive: Annotated[str, Field(default=None, description="One of the following: HKEY_CLASSES_ROOT, HKEY_CURRENT_CONFIG, HKEY_USERS, HKEY_LOCAL_MACHINE, ALL")], keys: Annotated[str, Field(default=None, description="Registry Key or Value Name")], min_size: Annotated[str, Field(default=None, description="Min byte size")], max_size: Annotated[str, Field(default=None, description="Max byte size")], endpoints_core_os: Annotated[str, Field(default=None, description="Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Searches for a registry key or value name.

Action Parameters: Hive: One of the following: HKEY_CLASSES_ROOT, HKEY_CURRENT_CONFIG, HKEY_USERS, HKEY_LOCAL_MACHINE, ALL., Keys: Registry Key or Value Name., Min Size: Min byte size., Max Size: Max byte size., Endpoints Core OS: Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if hive is not None:
                script_params["Hive"] = hive
            if keys is not None:
                script_params["Keys"] = keys
            if min_size is not None:
                script_params["Min Size"] = min_size
            if max_size is not None:
                script_params["Max Size"] = max_size
            if endpoints_core_os is not None:
                script_params["Endpoints Core OS"] = endpoints_core_os
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Hunt Registry",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Hunt Registry",
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
                print(f"Error executing action Endgame_Hunt Registry for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich Siemplify Host and IP entities based on the information from the Endgame.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
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
                actionName="Endgame_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Enrich Entities",
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
                print(f"Error executing action Endgame_Enrich Entities for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_hunt_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], endpoints_core_os: Annotated[str, Field(default=None, description="Select an operating system (i.e., Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system.")], md5_hashes: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter MD5 Hashes, separated by comma")], sha1_hashes: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter SHA1 Hashes, separated by comma")], sha256_hashes: Annotated[str, Field(default=None, description="ADVANCED CONFIGURATION for this hunt. Enter SHA256 Hashes, separated by comma")], directory: Annotated[str, Field(default=None, description="The starting directory path e.g. C:\\windows\\system32")], find_file: Annotated[str, Field(default=None, description="Enter the filename(s) to search. TIP: Enter a regex to narrow search results.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Searches for running files.

Action Parameters: Endpoints Core OS: Select an operating system (for example, Windows, Linux, or Mac) to filter the Endpoints list. Note: You can only create a single investigation for endpoints that run on the same operating system., MD5 Hashes: ADVANCED CONFIGURATION for this hunt. Enter MD5 Hashes, separated by comma., SHA1 Hashes: ADVANCED CONFIGURATION for this hunt. Enter SHA-1 Hashes, separated by comma., SHA256 Hashes: ADVANCED CONFIGURATION for this hunt. Enter SHA256 Hashes, separated by comma., Directory: The starting directory path Example C:\windows\system32, Find File: Enter the filename(s) to search. Enter a regular expression to narrow search results.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if endpoints_core_os is not None:
                script_params["Endpoints Core OS"] = endpoints_core_os
            if md5_hashes is not None:
                script_params["MD5 Hashes"] = md5_hashes
            if sha1_hashes is not None:
                script_params["SHA1 Hashes"] = sha1_hashes
            if sha256_hashes is not None:
                script_params["SHA256 Hashes"] = sha256_hashes
            if directory is not None:
                script_params["Directory"] = directory
            if find_file is not None:
                script_params["Find File"] = find_file
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Hunt File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Hunt File",
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
                print(f"Error executing action Endgame_Hunt File for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_download_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], full_file_path: Annotated[str, Field(..., description="Enter the path to the file")], full_download_folder_path: Annotated[str, Field(..., description="Enter the path to the folder, where you want to store this file.")], expected_sha_256_hash: Annotated[str, Field(default=None, description="Enter the expected SHA-256 hash")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Download a file from a specific Endgame endpoint.

Action Parameters: Full File Path: If enabled, creates an Insight after successful execution of this action., Full Download Folder Path: Enter the path to the folder, where you want to store this file., Expected SHA-256 Hash: Enter the expected SHA-256 hash.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Full File Path"] = full_file_path
            script_params["Full Download Folder Path"] = full_download_folder_path
            if expected_sha_256_hash is not None:
                script_params["Expected SHA-256 Hash"] = expected_sha_256_hash
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Download File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Download File",
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
                print(f"Error executing action Endgame_Download File for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_delete_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_path: Annotated[str, Field(..., description="Enter the path to the file")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Delete a file from Endgame endpoint.

Action Parameters: File Path: Enter the path to the file.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["File Path"] = file_path
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Delete File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Delete File",
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
                print(f"Error executing action Endgame_Delete File for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_removable_media_survey_windows_only(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about removable media from a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many items to return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Removable Media Survey (Windows only)",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Removable Media Survey (Windows only)",
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
                print(f"Error executing action Endgame_Removable Media Survey (Windows only) for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def endgame_software_survey_windows_only(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_items_to_return: Annotated[str, Field(default=None, description="Specify how many items to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about an installed software on a specific Endgame endpoint.

Action Parameters: Max Items to Return: Specify how many items to return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Endgame")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Endgame: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_items_to_return is not None:
                script_params["Max Items to Return"] = max_items_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Endgame_Software Survey (Windows only)",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Endgame_Software Survey (Windows only)",
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
                print(f"Error executing action Endgame_Software Survey (Windows only) for Endgame: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Endgame")
            return {"Status": "Failed", "Message": "No active instance found."}
