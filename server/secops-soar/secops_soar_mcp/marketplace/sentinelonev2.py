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
    # This function registers all tools (actions) for the SentinelOneV2 integration.

    @mcp.tool()
    async def sentinel_one_v2_add_threat_note(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threat_id: Annotated[str, Field(..., description="Specify the id of the threat for which you want to add a note.")], note: Annotated[str, Field(..., description="Specify the note that needs to be added to the threat.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add a note to the threat in SentinelOne.

Action Parameters: Threat ID: Required.The ID of the threat to add a note., Note: Required.A note to add to the threat.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threat ID"] = threat_id
            script_params["Note"] = note
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Add Threat Note",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Add Threat Note",
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
                print(f"Error executing action SentinelOneV2_Add Threat Note for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_resolve_threat(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threat_i_ds: Annotated[str, Field(..., description="Specify a comma-separated list of threat IDs that need to be resolved.")], annotation: Annotated[str, Field(default=None, description="Specify an annotation describing, why the threat can be resolved.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Resolve threats in SentinelOne.

Action Parameters: Threat IDs: Required.A comma-separated list of threat IDs to resolve., Annotation: Optional.A justification for resolving the threat.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threat IDs"] = threat_i_ds
            if annotation is not None:
                script_params["Annotation"] = annotation
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Resolve Threat",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Resolve Threat",
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
                print(f"Error executing action SentinelOneV2_Resolve Threat for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_blacklist(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hash: Annotated[str, Field(default=None, description="Specify a comma-separated list of hashes that need to be checked in blacklist. Only hashes that were found will be returned. If nothing is specified here action will return all hashes. Note: if \"Hash\" parameter is provided then \"Limit\" parameter is ignored.")], site_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of site ids, which should be used to return blacklist items.")], group_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of group ids, which should be used to return blacklist items.")], account_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of account ids, which should be used to return blacklist items.")], limit: Annotated[str, Field(default=None, description="Specify how many blacklist items should be returned. Note: if \"Hash\" parameter has values, then this parameter is ignored. Maximum is 1000.")], query: Annotated[str, Field(default=None, description="Specify the query that needs to be used in order to filter the results.")], use_global_blacklist: Annotated[bool, Field(default=None, description="If enabled, action will also return hashes from the global blacklist.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get a list of all the items available in the blacklist in SentinelOne.

Action Parameters: Hash: Optional.A comma-separated list of hashes to check in the blocklist.The action only returns hashes that were found.If you set the Hash, the action ignores the Limit parameter., Site IDs: Optional.A comma-separated list of site IDs to return blocklist items., Group IDs: Optional.A comma-separated list of group IDs to return blocklist items., Account Ids: Optional.A comma-separated list of account IDs to return blocklist items., Limit: Optional.A number of blocklist items to return.If you set the Hash parameter, the action ignores this parameter. The maximum value is 1000.The default value is 50., Query: Optional.A query to filter results., Use Global Blacklist: Optional.If selected, the action returns hashes from a global blocklist.Not selected by default.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if hash is not None:
                script_params["Hash"] = hash
            if site_i_ds is not None:
                script_params["Site IDs"] = site_i_ds
            if group_i_ds is not None:
                script_params["Group IDs"] = group_i_ds
            if account_i_ds is not None:
                script_params["Account IDs"] = account_i_ds
            if limit is not None:
                script_params["Limit"] = limit
            if query is not None:
                script_params["Query"] = query
            if use_global_blacklist is not None:
                script_params["Use Global Blacklist"] = use_global_blacklist
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Blacklist",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Blacklist",
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
                print(f"Error executing action SentinelOneV2_Get Blacklist for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_create_hash_exclusion_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], operation_system: Annotated[str, Field(..., description="Specify the OS for the hash. Possible values: windows, windows_legacy, macos, linux.")], site_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of site ids, where hash needs to be sent to the exclusion list.")], group_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of group ids, where hash needs to be sent to the exclusion list.")], account_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of account ids, where hash needs to be sent to the exclusion list.")], description: Annotated[str, Field(default=None, description="Specify additional information related to the hash.")], add_to_global_exclusion_list: Annotated[bool, Field(default=None, description="If enabled, action will add the hash to the global exclusion list. Note: when this parameter is enabled, parameters \u201cSite IDs\u201c, \u201cGroup IDs\u201c and \u201cAccount IDs\u201c are ignored.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add hash to the exclusion list in SentinelOne. Note: Only SHA1 hashes are supported.

Action Parameters: Operation System: Required.An operation system (OS) for the hash. The possible values are as follows: windowswindows_legacy macoslinuxThe default value is windows., Site IDs: Optional. A comma-separated list of site IDs to send the hash to the exclusion list.The action requires at least one valid value., Group IDs: Optional.A comma-separated list of group ID to send the hash to the exclusion list.The action requires at least one valid value., Account IDs: Optional.A comma-separated list of account IDs to send the hash to the exclusion list., Description: Optional. Additional information related to the hash., Add to global exclusion list: Optional. If selected, the action adds a hash to the global exclusion list. If you select this parameter, the action ignores the Site IDs, Group IDs, and Account IDs parameters.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Operation System"] = operation_system
            if site_i_ds is not None:
                script_params["Site IDs"] = site_i_ds
            if group_i_ds is not None:
                script_params["Group IDs"] = group_i_ds
            if account_i_ds is not None:
                script_params["Account IDs"] = account_i_ds
            if description is not None:
                script_params["Description"] = description
            if add_to_global_exclusion_list is not None:
                script_params["Add to global exclusion list"] = add_to_global_exclusion_list
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Create Hash Exclusion Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Create Hash Exclusion Record",
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
                print(f"Error executing action SentinelOneV2_Create Hash Exclusion Record for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_system_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Fetch system status.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Get System Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get System Status",
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
                print(f"Error executing action SentinelOneV2_Get System Status for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_disconnect_agent_from_network(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Disconnect agent from network by it's host name or IP address.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Disconnect Agent From Network",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Disconnect Agent From Network",
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
                print(f"Error executing action SentinelOneV2_Disconnect Agent From Network for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_events_for_endpoint_hours_back(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hours_back: Annotated[str, Field(..., description="Specify how many hours backwards to fetch events.")], events_amount_limit: Annotated[str, Field(default=None, description="Specify how many events to return per event type. Default: 50.")], include_file_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about file events.")], include_indicator_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about indicator events.")], include_dns_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about DNS events.")], include_network_actions_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about \u201cnetwork actions\u201d events.")], include_url_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about URL events.")], include_registry_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about registry events.")], include_scheduled_task_events_information: Annotated[bool, Field(default=None, description="If enabled, action will also query information about scheduled task events.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve information about the latest events on the endpoint. Works with IP and Hostname entities.Note: this action uses an endpoint that has rate limiting. Only one endpoint can be processed per minute․

Action Parameters: Hours Back: Required.The number of hours prior to now to fetch events., Events Amount Limit: Optional.The maximum number of events to return for every event type.The default value is 50., Include File Events Information: Optional.If selected, the action queries information about file events., Include Indicator Events Information: Optional.If selected, the action queries information about indicator events., Include DNS Events Information: Optional.If selected, the action queries information about DNS events., Include Network Actions Events Information: Optional.If selected, the action queries information about the network actions events., Include URL Events Information: Optional.If selected, the action queries information about URL events., Include Registry Events Information: Optional.If selected, the action queries information about registry events., Include Scheduled Task Events Information: Optional.If selected, the action queries information about scheduled task events.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Hours Back"] = hours_back
            if events_amount_limit is not None:
                script_params["Events Amount Limit"] = events_amount_limit
            if include_file_events_information is not None:
                script_params["Include File Events Information"] = include_file_events_information
            if include_indicator_events_information is not None:
                script_params["Include Indicator Events Information"] = include_indicator_events_information
            if include_dns_events_information is not None:
                script_params["Include DNS Events Information"] = include_dns_events_information
            if include_network_actions_events_information is not None:
                script_params["Include Network Actions Events Information"] = include_network_actions_events_information
            if include_url_events_information is not None:
                script_params["Include URL Events Information"] = include_url_events_information
            if include_registry_events_information is not None:
                script_params["Include Registry Events Information"] = include_registry_events_information
            if include_scheduled_task_events_information is not None:
                script_params["Include Scheduled Task Events Information"] = include_scheduled_task_events_information
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Events For Endpoint Hours Back",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Events For Endpoint Hours Back",
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
                print(f"Error executing action SentinelOneV2_Get Events For Endpoint Hours Back for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_create_path_exclusion_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], path: Annotated[str, Field(..., description="Specify the path that needs to be added to the exclusion list.")], operation_system: Annotated[str, Field(..., description="Specify the OS for the path. Possible values: windows, windows_legacy, macos, linux.")], site_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of site ids, where path needs to be sent to the exclusion list.")], group_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of group ids, where path needs to be sent to the exclusion list.")], account_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of account ids, where path needs to be sent to the exclusion list.")], description: Annotated[str, Field(default=None, description="Specify additional information related to the path.")], add_to_global_exclusion_list: Annotated[bool, Field(default=None, description="If enabled, action will add the path to the global exclusion list. Note: when this parameter is enabled, parameters \u201cSite IDs\u201c, \u201cGroup IDs\u201c and \u201cAccount IDs\u201c are ignored.")], include_subfolders: Annotated[bool, Field(default=None, description="If enabled, action will include subfolders for the provided path. This feature only works, if user provides folder path and not file path.")], mode: Annotated[List[str], Field(default=None, description="Specify what mode should be used for the excluded path.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add path to the exclusion list in SentinelOne.

Action Parameters: Path: Required. A path to add to the exclusion list., Operation System: Required.An operation system (OS) for the hash. The possible values are as follows: windowswindows_legacy macoslinuxThe default value is windows., Site IDs: Optional. A comma-separated list of site IDs to send the hash to the exclusion list.The action requires at least one valid value., Group IDs: Optional.A comma-separated list of group ID to send the hash to the exclusion list.The action requires at least one valid value., Account IDs: Optional.A comma-separated list of account IDs to send the hash to the exclusion list., Description: Optional. Additional information related to the hash., Add to global exclusion list: Optional. If selected, the action adds a hash to the global exclusion list. If you select this parameter, the action ignores the Site IDs, Group IDs, and Account IDs parameters., Include Subfolders: Optional. If selected, the action includes subfolders for the provided path. This parameter only applies if you configure a folder path in the Path parameter., Mode: Optional. A mode to use for the excluded path.The possible values are as follows:Suppress Alerts Interoperability Interoperability - Extended Performance Focus Performance Focus - Extended

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Path"] = path
            script_params["Operation System"] = operation_system
            if site_i_ds is not None:
                script_params["Site IDs"] = site_i_ds
            if group_i_ds is not None:
                script_params["Group IDs"] = group_i_ds
            if account_i_ds is not None:
                script_params["Account IDs"] = account_i_ds
            if description is not None:
                script_params["Description"] = description
            if add_to_global_exclusion_list is not None:
                script_params["Add to global exclusion list"] = add_to_global_exclusion_list
            if include_subfolders is not None:
                script_params["Include Subfolders"] = include_subfolders
            if mode is not None:
                script_params["Mode"] = mode
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Create Path Exclusion Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Create Path Exclusion Record",
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
                print(f"Error executing action SentinelOneV2_Create Path Exclusion Record for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_deep_visibility_query_result(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query_id: Annotated[str, Field(..., description="Specify the ID of the query for which you want to return results. This ID is available in the JSON result of the action \u201cInitiate Deep Visibility Query\u201c as \u201cquery_id\u201c parameter.")], limit: Annotated[str, Field(default=None, description="Specify how many events to return. Default: 50. Maximum is 100.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about deep visibility query results. Note: this action should be used in combination with “Initiate Deep Visibility Query“.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query ID"] = query_id
            if limit is not None:
                script_params["Limit"] = limit
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Deep Visibility Query Result",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Deep Visibility Query Result",
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
                print(f"Error executing action SentinelOneV2_Get Deep Visibility Query Result for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_initiate_deep_visibility_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query for the search.")], start_date: Annotated[str, Field(default=None, description="Specify the start date for the search. If nothing is specified, action will fetch events from 30 days ago.")], end_date: Annotated[str, Field(default=None, description="Specify the end date for the search. If nothing is specified, action will use current time.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Initiate a Deep Visibility Query search. Returns query id, which should be used in the action "Get Deep Visibility Query Result".

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            if start_date is not None:
                script_params["Start Date"] = start_date
            if end_date is not None:
                script_params["End Date"] = end_date
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Initiate Deep Visibility Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Initiate Deep Visibility Query",
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
                print(f"Error executing action SentinelOneV2_Initiate Deep Visibility Query for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_threats(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mitigation_status: Annotated[str, Field(default=None, description="Specify the comma-separated list of threat statuses. Only threats that match the statuses will be returned. Possible values: mitigated, active, blocked, suspicious, suspicious_resolved")], created_until: Annotated[str, Field(default=None, description="Specify the end time for the threats. Example: 2020-03-02T21:30:13.014874Z")], created_from: Annotated[str, Field(default=None, description="Specify the start time for the threats. Example: 2020-03-02T21:30:13.014874Z")], resolved_threats: Annotated[bool, Field(default=None, description="If enabled, action will only return resolved threats.")], threat_display_name: Annotated[str, Field(default=None, description="Specify a display name of the threat that you want to return. Partial name will also work.")], limit: Annotated[str, Field(default=None, description="Specify how many threats to return. Default: 10.")], api_version: Annotated[List[str], Field(default=None, description="Specify what version of API to use in the action. If nothing is provided connector will use version 2.1. Note: JSON result structure is different between API versions. It is recommended to use the latest one.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve information about threats in SentinelOne.

Action Parameters: Mitigation Status: Optional.A comma-separated list of threat statuses. The action only returns threats that match the configured statuses. The possible values are as follows:mitigated activeblocked suspicioussuspicious_resolved, Created until: Optional. The end time for the threats, such as 2020-03-02T21:30:13.014874Z., Created from: Optional. The start time for the threats, such as 2020-03-02T21:30:13.014874Z., Resolved Threats: Optional.If selected, the action only returns resolved threats., Threat Display Name: Optional.A display name of the threat to return., Limit: Optional.A number of threats to return.The default value is 10., API Version: Optional. A version of API to use in the action. If you don't set a value, the action uses the 2.1 version. API version impacts the JSON result structure. We recommend to set the latest API version.The possible values are as follows: 2.02.1The default value is 2.0.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if mitigation_status is not None:
                script_params["Mitigation Status"] = mitigation_status
            if created_until is not None:
                script_params["Created until"] = created_until
            if created_from is not None:
                script_params["Created from"] = created_from
            if resolved_threats is not None:
                script_params["Resolved Threats"] = resolved_threats
            if threat_display_name is not None:
                script_params["Threat Display Name"] = threat_display_name
            if limit is not None:
                script_params["Limit"] = limit
            if api_version is not None:
                script_params["API Version"] = api_version
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Threats",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Threats",
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
                print(f"Error executing action SentinelOneV2_Get Threats for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_enrich_endpoint(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight with information about endpoints.")], only_infected_endpoints_insights: Annotated[bool, Field(default=None, description="If enabled, action will only create insights for the infected endpoints.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich information about the endpoint by IP address or Hostname.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if only_infected_endpoints_insights is not None:
                script_params["Only Infected Endpoints Insights"] = only_infected_endpoints_insights
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Enrich Endpoint",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Enrich Endpoint",
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
                print(f"Error executing action SentinelOneV2_Enrich Endpoint for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_initiate_full_scan(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Initiate a full disk scan on the endpoint in SentinelOne.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Initiate Full Scan",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Initiate Full Scan",
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
                print(f"Error executing action SentinelOneV2_Initiate Full Scan for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_mark_as_threat(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threat_i_ds: Annotated[str, Field(..., description="Specify a comma-separated list of threat IDs that should be marked.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Marks suspicious threats as a true positive threat in SentinelOne.

Action Parameters: Threat IDs: Required. A comma-separated list of detection IDs to mark as threats.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threat IDs"] = threat_i_ds
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Mark as Threat",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Mark as Threat",
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
                print(f"Error executing action SentinelOneV2_Mark as Threat for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Test integration connectivity.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Ping",
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
                print(f"Error executing action SentinelOneV2_Ping for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_delete_hash_blacklist_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], site_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of site ids, from where the hash needs to be removed.")], group_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of group ids, from where the hash needs to be removed.")], account_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of account ids, from where the hash needs to be removed.")], remove_from_global_black_list: Annotated[bool, Field(default=None, description="If enabled, action will remove the hash from the global black list. Note: when this parameter is enabled, parameters \"Site IDs\", \"Group IDs\" and \"Account IDs\" are ignored.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Delete hashes from a blacklist in SentinelOne. Note: Only SHA1 hashes are supported.

Action Parameters: Site IDs: Optional.A comma-separated list of site IDs to remove the hash., Group IDs: Optional.A comma-separated list of group IDs to remove the hash., Account IDs: Optional.A comma-separated list of account IDs to remove the hash., Remove from global black list: Optional.If selected, the action removes the hash from the global blocklist.If you select this parameter, the action ignores the Site IDs, Group IDs, and Account IDs parameters.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if site_i_ds is not None:
                script_params["Site IDs"] = site_i_ds
            if group_i_ds is not None:
                script_params["Group IDs"] = group_i_ds
            if account_i_ds is not None:
                script_params["Account IDs"] = account_i_ds
            if remove_from_global_black_list is not None:
                script_params["Remove from global black list"] = remove_from_global_black_list
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Delete Hash Blacklist Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Delete Hash Blacklist Record",
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
                print(f"Error executing action SentinelOneV2_Delete Hash Blacklist Record for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_system_version(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Fetch system version.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Get System Version",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get System Version",
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
                print(f"Error executing action SentinelOneV2_Get System Version for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_update_incident_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threat_id: Annotated[str, Field(..., description="Specify a comma-separated list of threat ids for which you want to update the incident status.")], status: Annotated[List[str], Field(..., description="Specify the incident status.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Update threat incident status in SentinelOne.

Action Parameters: Threat ID: Required.A comma-separated list of threat IDs to update the incident status., Status: Required.An incident status.The possible values are as follows:UnresolvedIn Progress ResolvedThe default value is Resolved.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threat ID"] = threat_id
            script_params["Status"] = status
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Update Incident Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Update Incident Status",
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
                print(f"Error executing action SentinelOneV2_Update Incident Status for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_mitigate_threat(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], mitigation_action: Annotated[List[str], Field(..., description="Specify the mitigation actions for the provided threats.")], threat_i_ds: Annotated[str, Field(..., description="Specify a comma-separated list of threat IDs that should be mitigated.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Executes mitigation actions on the threats in SentinelOne.

Action Parameters: Mitigation action: Required.A mitigation action for the detected threats. The possible values are as follows: quarantinekill un-quarantineremediate rollback-remediateThe default value is quarantine., Threat IDs: Required.A comma-separated list of threat IDs to mitigate.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Mitigation action"] = mitigation_action
            script_params["Threat IDs"] = threat_i_ds
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Mitigate Threat",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Mitigate Threat",
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
                print(f"Error executing action SentinelOneV2_Mitigate Threat for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_download_threat_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threat_id: Annotated[str, Field(..., description="Specify the id of the threat for which you want to download the file.")], password: Annotated[str, Field(..., description="Specify the password for the zip that contains the threat file. Password requirements: At least 10 characters. Three of these: uppercase, lowercase, digits, special symbols. Maximum length is 256 characters.")], download_folder_path: Annotated[str, Field(..., description="Specify the path to the folder, where you want to store the threat file.")], overwrite: Annotated[bool, Field(..., description="If enabled, action will overwrite the file with the same name.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Download file related to threat in SentinelOne. Note: Your user role must have permissions to Fetch Threat File - Admin, IR Team, SOC.

Action Parameters: Threat ID: Required.The ID of the threat to download a file., Password: Required.A password for the zipped folder that contains the threat file.The password requirements are as follows:Is at least 10 characters long.Includes uppercase letters, lowercase letters, digits, and special symbols.The maximum length for the password is 256 characters., Download Folder Path: Required.A path to a folder to store the threat file., Overwrite: Required.If selected, the action overwrites a file with the identical name.Not selected by default.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threat ID"] = threat_id
            script_params["Password"] = password
            script_params["Download Folder Path"] = download_folder_path
            script_params["Overwrite"] = overwrite
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Download Threat File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Download Threat File",
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
                print(f"Error executing action SentinelOneV2_Download Threat File for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_agent_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve information about the status of the agents on the endpoints based on the IP or Hostname entity.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Get Agent Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Agent Status",
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
                print(f"Error executing action SentinelOneV2_Get Agent Status for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_list_sites(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], filter_key: Annotated[List[str], Field(default=None, description="Specify the key that needs to be used to filter sites.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied. Filtering logic is working based on the value provided in the \"Filter Key\" parameter.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter. If \"Equal\" is selected, action will try to find the exact match among results and if \"Contains\" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value  provided in the \"Filter Key\" parameter.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
List available sites in SentinelOne.

Action Parameters: Filter Key: Optional.The key to filter sites.The possible values are as follows:Select OneName IDThe default value is Select One., Filter Logic: Optional.The filter logic to apply.The filter logic uses the value set in the Filter Key parameter.The possible values are as follows:Not Specified EqualContainsThe default value is Not Specified., Filter Value: Optional.The value to use in the filter.The filter logic uses the value set in the Filter Key parameter.If you select Equal in the Filter Logic parameter, the action searches for the exact match among results.If you select Contains in the Filter Logic parameter, the action searches for results that contain the specified substring.If you don't set a value, the action ignores the filter., Max Records To Return: Optional.The number of records to return.The default value is 50.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_List Sites",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_List Sites",
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
                print(f"Error executing action SentinelOneV2_List Sites for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_create_hash_blacklist_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], operating_system: Annotated[str, Field(..., description="Specify the OS for the hash. Possible values: windows, windows_legacy, macos, linux.")], add_to_global_black_list: Annotated[bool, Field(..., description="If enabled, action will add the hash to the global blacklist. Note: when this parameter is enabled, parameters \u201cSite IDs\u201c, \u201cGroup IDs\u201c and \u201cAccount IDs\u201c are ignored.")], site_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of site ids, where hash needs to be sent to the blacklist.")], group_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of group ids, where hash needs to be sent to the blacklist.")], account_i_ds: Annotated[str, Field(default=None, description="Specify a comma-separated list of account ids, where hash needs to be sent to the blacklist.")], description: Annotated[str, Field(default=None, description="Specify additional information related to the hash.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add hashes to a blacklist in SentinelOne. Note: Only SHA1 hashes are supported.

Action Parameters: Operating System: Required.An operating system for the hash.The possible values are as follows:windows windows_legacymacos linuxThe default value is windows., Site IDs: Optional.A comma-separated list of site IDs to send to the blocklist., Group IDs: Optional.A comma-separated list of group IDs to send to the blocklist., Account IDs: Optional.A comma-separated list of account IDs to send to the blocklist., Description: Optional.Additional information related to a hash.The default value is ""., Add to global blocklist: Required.If selected, the action adds a hash to a global blocklist.If you select this parameter, the action ignores the Site IDs, Group IDs, and Account IDs parameters.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Operating System"] = operating_system
            if site_i_ds is not None:
                script_params["Site IDs"] = site_i_ds
            if group_i_ds is not None:
                script_params["Group IDs"] = group_i_ds
            if account_i_ds is not None:
                script_params["Account IDs"] = account_i_ds
            if description is not None:
                script_params["Description"] = description
            script_params["Add to global black list"] = add_to_global_black_list
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Create Hash Blacklist Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Create Hash Blacklist Record",
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
                print(f"Error executing action SentinelOneV2_Create Hash Blacklist Record for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_reconnect_agent_to_the_network(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Reconnect disconnected endpoint to the network. Works with Hostname and IP entities.

Action Parameters: None.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
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
                actionName="SentinelOneV2_Reconnect Agent To The Network",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Reconnect Agent To The Network",
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
                print(f"Error executing action SentinelOneV2_Reconnect Agent To The Network for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_application_list_for_endpoint(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_applications_to_return: Annotated[str, Field(default=None, description="Specify how many applications to return. If nothing is specified action will return all of the applications.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about available applications on the endpoint by IP or Hostname.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_applications_to_return is not None:
                script_params["Max Applications To Return"] = max_applications_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Application List For Endpoint",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Application List For Endpoint",
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
                print(f"Error executing action SentinelOneV2_Get Application List For Endpoint for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_hash_reputation(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], reputation_threshold: Annotated[str, Field(default=None, description="Specify what should be the reputation threshold in order it to be marked as suspicious. If nothing is provided, action will not mark entites as suspicious. Maximum: 10.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about the reputation.")], only_suspicious_hashes_insight: Annotated[bool, Field(default=None, description="If enabled, action will only create insight for hashes that have higher or equal reputation to \u201cReputation Threshold\u201c value.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve information about the hashes from SentinelOne.

Action Parameters: Reputation Threshold: Optional.A reputation threshold to mark entity as suspicious.If you don't set a value, the action doesn't mark any entity as suspicious.The maximum value is 10.The default value is 5., Create Insight: Optional.If selected, the action creates an insight that contains information about the reputation., Only Suspicious Hashes Insight: Optional.If selected, the action only creates an insight for hashes with the reputation exceeding or equal to the Reputation Threshold value.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if reputation_threshold is not None:
                script_params["Reputation Threshold"] = reputation_threshold
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if only_suspicious_hashes_insight is not None:
                script_params["Only Suspicious Hashes Insight"] = only_suspicious_hashes_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Hash Reputation",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Hash Reputation",
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
                print(f"Error executing action SentinelOneV2_Get Hash Reputation for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_get_group_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], group_names: Annotated[str, Field(..., description="Specify a comma-separated list of group names for which you want to retrieve details.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve detailed information about the provided groups.

Action Parameters: Group Names: Required.Group names to retrieve details. This parameter accepts multiple values as a comma-separated list.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Group Names"] = group_names
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Get Group Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Get Group Details",
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
                print(f"Error executing action SentinelOneV2_Get Group Details for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_update_analyst_verdict(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], threat_id: Annotated[str, Field(..., description="Specify a comma-separated list of threat ids for which you want to update the analyst verdict.")], analyst_verdict: Annotated[List[str], Field(..., description="Specify the analyst verdict.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Update analyst verdict of the threat in SentinelOne.

Action Parameters: Threat ID: Required.A comma-separated list of threat IDs to update the analyst verdict., Analyst Verdict: Required.An analyst verdict.The possible values are as follows:True Positive False PositiveSuspicious UndefinedThe default value is Undefined.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Threat ID"] = threat_id
            script_params["Analyst Verdict"] = analyst_verdict
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Update Analyst Verdict",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Update Analyst Verdict",
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
                print(f"Error executing action SentinelOneV2_Update Analyst Verdict for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sentinel_one_v2_move_agents(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], group_id: Annotated[str, Field(default=None, description="Specify the ID of the group, where to move the agents.")], group_name: Annotated[str, Field(default=None, description="Specify the name of the group, where to move the agents. Note: if both Group ID and Group Name are provided, action will put \u201cGroup ID\u201c in the priority.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Move agents to the provided group. This action works with Hostname and IP address entities. Note: the group should be from the same site.

Action Parameters: Group ID: Optional.The ID of the group to move agents., Group Name: Optional.The name of the group to move agents.If you configure both the Group ID parameter and the Group Name parameters, the action prioritizes the Group ID parameter.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SentinelOneV2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SentinelOneV2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if group_id is not None:
                script_params["Group ID"] = group_id
            if group_name is not None:
                script_params["Group Name"] = group_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SentinelOneV2_Move Agents",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SentinelOneV2_Move Agents",
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
                print(f"Error executing action SentinelOneV2_Move Agents for SentinelOneV2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SentinelOneV2")
            return {"Status": "Failed", "Message": "No active instance found."}
