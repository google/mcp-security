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
    # This function registers all tools (actions) for the MicrosoftIntune integration.

    @mcp.tool()
    async def microsoft_intune_remote_lock_managed_device(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], host_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of host names to run the action on. Host name is case insensitive. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], host_id: Annotated[str, Field(default=None, description="Specify a comma-separated list of host ids to run the action on. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Remote lock managed device. The action starts the task, to check the current task status, run "Get Managed Device" action and see "deviceActionResults" section for task status.  The host name to run the action on can be provided either as a Siemplify entity or as an action input parameter. If the host name is passed to action both as an entity and input parameter - action will be executed on the input parameter. Host name is case insensitive. Action also can be provided with the host id to run on. If both host id and hostname are provided, action will run on the host id as a priority.  Please refer to our doc portal for more details.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if host_name is not None:
                script_params["Host Name"] = host_name
            if host_id is not None:
                script_params["Host Id"] = host_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_Remote Lock Managed Device",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Remote Lock Managed Device",
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
                print(f"Error executing action MicrosoftIntune_Remote Lock Managed Device for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_list_managed_devices(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], filter_key: Annotated[List[str], Field(default=None, description="Specify the key that needs to be used to filter managed devices.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied. Filtering logic is working based on the value  provided in the \u201cFilter Key\u201d parameter.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter. If \u201cEqual\u201c is selected, action will try to find the exact match among results and if \u201cContains\u201c is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value  provided in the \u201cFilter Key\u201d parameter.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return. If nothing is provided, action will return 50 records. Maximum: 100.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List managed devices available in the Microsoft Intune instance based on provided criteria. Note: This action doesn't run on Chronicle SOAR entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if filter_key is not None:
                script_params["Filter Key"] = filter_key
            if filter_logic is not None:
                script_params["Filter Logic"] = filter_logic
            if filter_value is not None:
                script_params["Filter Value"] = filter_value
            if max_records_to_return is not None:
                script_params["Max Records To Return"] = max_records_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_List Managed Devices",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_List Managed Devices",
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
                print(f"Error executing action MicrosoftIntune_List Managed Devices for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_sync_managed_device(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], host_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of host names to run the action on. Host name is case insensitive. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], host_id: Annotated[str, Field(default=None, description="Specify a comma-separated list of host ids to run the action on. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Sync managed device with the Microsoft Intune service. The host name to run the action on can be provided either as a Siemplify entity or as an action input parameter. If the host name is passed to action both as an entity and input parameter - action will be executed on the input parameter. Host name is case insensitive. Action also can be provided with the host id to run on. If both host id and hostname are provided, action will run on the host id as a priority. Please refer to our doc portal for more details.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if host_name is not None:
                script_params["Host Name"] = host_name
            if host_id is not None:
                script_params["Host Id"] = host_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_Sync Managed Device",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Sync Managed Device",
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
                print(f"Error executing action MicrosoftIntune_Sync Managed Device for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Microsoft Intune service with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
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
                actionName="MicrosoftIntune_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Ping",
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
                print(f"Error executing action MicrosoftIntune_Ping for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_locate_managed_device(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], host_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of host names to run the action on. Host name is case insensitive. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], host_id: Annotated[str, Field(default=None, description="Specify a comma-separated list of host ids to run the action on. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Locate managed device with the Microsoft Intune service. The action starts the task, to check the current task status, run "Get Managed Device" action and see "deviceActionResults" section for task status.  The host name to run the action on can be provided either as a Siemplify entity or as an action input parameter. If the host name is passed to action both as an entity and input parameter - action will be executed on the input parameter. Host name is case insensitive. Action also can be provided with the host id to run on. If both host id and hostname are provided, action will run on the host id as a priority.  Please refer to our doc portal for more details.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if host_name is not None:
                script_params["Host Name"] = host_name
            if host_id is not None:
                script_params["Host Id"] = host_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_Locate Managed Device",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Locate Managed Device",
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
                print(f"Error executing action MicrosoftIntune_Locate Managed Device for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_wipe_managed_device(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], host_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of host names to run the action on. Host name is case insensitive. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], host_id: Annotated[str, Field(default=None, description="Specify a comma-separated list of host ids to run the action on. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], keep_enrollment_data: Annotated[bool, Field(default=None, description="If enabled, keep enrollment data on the device.")], keep_user_data: Annotated[bool, Field(default=None, description="If enabled, keep user data on the device.")], persist_esim_data_plan: Annotated[bool, Field(default=None, description="If enabled, persist esim data plan for the device.")], mac_os_unlock_code: Annotated[str, Field(default=None, description="Specify if applicable Mac OS unlock code.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wipe managed device with the Microsoft Intune service. The host name to run the action on can be provided either as a Siemplify entity or as an action input parameter. If the host name is passed to action both as an entity and input parameter - action will be executed on the input parameter. Host name is case insensitive. Action also can be provided with the host id to run on. If both host id and hostname are provided, action will run on the host id as a priority. Please refer to our doc portal for more details.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if host_name is not None:
                script_params["Host Name"] = host_name
            if host_id is not None:
                script_params["Host Id"] = host_id
            if keep_enrollment_data is not None:
                script_params["Keep Enrollment Data"] = keep_enrollment_data
            if keep_user_data is not None:
                script_params["Keep User Data"] = keep_user_data
            if persist_esim_data_plan is not None:
                script_params["Persist Esim Data Plan"] = persist_esim_data_plan
            if mac_os_unlock_code is not None:
                script_params["Mac OS Unlock Code"] = mac_os_unlock_code
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_Wipe Managed Device",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Wipe Managed Device",
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
                print(f"Error executing action MicrosoftIntune_Wipe Managed Device for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_get_managed_device(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], host_name: Annotated[str, Field(default=None, description="Specify the host name to run the action on. Host name is case insensitive. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Multiple values can be as a comma-separated string.")], host_id: Annotated[str, Field(default=None, description="Specify the host id to run the action on. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Multiple values can be as a comma-separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get managed device information from the Microsoft Intune service, including information on specific actions, for example locate device ("deviceActionResults" section of the json result). The host name to run the action on can be provided either as a Siemplify entity or as an action input parameter. If the host name is passed to action both as an entity and input parameter - action will be executed on the input parameter. Host name is case insensitive. Action also can be provided with the host id to run on. If both host id and hostname are provided, action will run on the host id as a priority.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if host_name is not None:
                script_params["Host Name"] = host_name
            if host_id is not None:
                script_params["Host Id"] = host_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_Get Managed Device",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Get Managed Device",
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
                print(f"Error executing action MicrosoftIntune_Get Managed Device for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_intune_reset_managed_device_passcode(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], host_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of host names to run the action on. Host name is case insensitive. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], host_id: Annotated[str, Field(default=None, description="Specify a comma-separated list of host ids to run the action on. If the action does not run on a hostname entity, it can run either on Host Name or Host ID. Note: if both \"Host Name\" and \"Host Id\" are provided, then \"Host Id\" value will have priority. Multiple values can be as a comma-separated string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Reset managed device passcode. The action starts the task, to check the current task status, run "Get Managed Device" action and see "deviceActionResults" section for task status.  The host name to run the action on can be provided either as a Siemplify entity or as an action input parameter. If the host name is passed to action both as an entity and input parameter - action will be executed on the input parameter. Host name is case insensitive. Action also can be provided with the host id to run on. If both host id and hostname are provided, action will run on the host id as a priority.  Please refer to our doc portal for more details.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftIntune")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftIntune: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if host_name is not None:
                script_params["Host Name"] = host_name
            if host_id is not None:
                script_params["Host Id"] = host_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftIntune_Reset Managed Device Passcode",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftIntune_Reset Managed Device Passcode",
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
                print(f"Error executing action MicrosoftIntune_Reset Managed Device Passcode for MicrosoftIntune: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftIntune")
            return {"Status": "Failed", "Message": "No active instance found."}
