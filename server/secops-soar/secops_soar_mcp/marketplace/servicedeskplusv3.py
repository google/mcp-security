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
    # This function registers all tools (actions) for the ServiceDeskPlusV3 integration.

    @mcp.tool()
    async def service_desk_plus_v3_create_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the request.")], requester: Annotated[str, Field(..., description="The requester of the request. If not specified, set to the user of the API key.")], description: Annotated[str, Field(default=None, description="The description of the request.")], assets: Annotated[str, Field(default=None, description="Names of Assets to be associated with the request")], status: Annotated[str, Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[str, Field(default=None, description="The priority of the request.")], urgency: Annotated[str, Field(default=None, description="The urgency of the request.")], category: Annotated[str, Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[str, Field(default=None, description="The type of the request. i.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[str, Field(default=None, description="The mode in which this request is created.Example : E-mail")], level: Annotated[str, Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="Denotes the site to which this request belongs")], group: Annotated[str, Field(default=None, description="Group to which this request belongs")], impact: Annotated[str, Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a new request

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Requester"] = requester
            if description is not None:
                script_params["Description"] = description
            if assets is not None:
                script_params["Assets"] = assets
            if status is not None:
                script_params["Status"] = status
            if technician is not None:
                script_params["Technician"] = technician
            if priority is not None:
                script_params["Priority"] = priority
            if urgency is not None:
                script_params["Urgency"] = urgency
            if category is not None:
                script_params["Category"] = category
            if request_template is not None:
                script_params["Request Template"] = request_template
            if request_type is not None:
                script_params["Request Type"] = request_type
            if due_by_time_ms is not None:
                script_params["Due By Time (ms)"] = due_by_time_ms
            if mode is not None:
                script_params["Mode"] = mode
            if level is not None:
                script_params["Level"] = level
            if site is not None:
                script_params["Site"] = site
            if group is not None:
                script_params["Group"] = group
            if impact is not None:
                script_params["Impact"] = impact
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Create Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Create Request",
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
                print(f"Error executing action ServiceDeskPlusV3_Create Request for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_create_alert_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the request.")], requester: Annotated[str, Field(..., description="The requester of the request. If not specified, set to the user of the API key.")], assets: Annotated[str, Field(default=None, description="Names of Assets to be associated with the request")], status: Annotated[str, Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[str, Field(default=None, description="The priority of the request.")], urgency: Annotated[str, Field(default=None, description="The urgency of the request.")], category: Annotated[str, Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[str, Field(default=None, description="The type of the request. i.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[str, Field(default=None, description="The mode in which this request is created.Example : E-mail")], level: Annotated[str, Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="Denotes the site to which this request belongs")], group: Annotated[str, Field(default=None, description="Group to which this request belongs")], impact: Annotated[str, Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a request related to a Siemplify alert

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Requester"] = requester
            if assets is not None:
                script_params["Assets"] = assets
            if status is not None:
                script_params["Status"] = status
            if technician is not None:
                script_params["Technician"] = technician
            if priority is not None:
                script_params["Priority"] = priority
            if urgency is not None:
                script_params["Urgency"] = urgency
            if category is not None:
                script_params["Category"] = category
            if request_template is not None:
                script_params["Request Template"] = request_template
            if request_type is not None:
                script_params["Request Type"] = request_type
            if due_by_time_ms is not None:
                script_params["Due By Time (ms)"] = due_by_time_ms
            if mode is not None:
                script_params["Mode"] = mode
            if level is not None:
                script_params["Level"] = level
            if site is not None:
                script_params["Site"] = site
            if group is not None:
                script_params["Group"] = group
            if impact is not None:
                script_params["Impact"] = impact
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Create Alert Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Create Alert Request",
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
                print(f"Error executing action ServiceDeskPlusV3_Create Alert Request for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_create_request_dropdown_lists(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the request.")], requester: Annotated[str, Field(..., description="The requester of the request. If not specified, set to the user of the API key.")], description: Annotated[str, Field(default=None, description="The description of the request.")], assets: Annotated[str, Field(default=None, description="Names of Assets to be associated with the request")], status: Annotated[List[str], Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[List[str], Field(default=None, description="The priority of the request.")], urgency: Annotated[List[str], Field(default=None, description="The urgency of the request.")], category: Annotated[List[str], Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[List[str], Field(default=None, description="The type of the request. i.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[List[str], Field(default=None, description="The mode in which this request is created.Example : E-mail")], level: Annotated[List[str], Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="Denotes the site to which this request belongs")], group: Annotated[str, Field(default=None, description="Group to which this request belongs")], impact: Annotated[List[str], Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a new request

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Requester"] = requester
            if description is not None:
                script_params["Description"] = description
            if assets is not None:
                script_params["Assets"] = assets
            if status is not None:
                script_params["Status"] = status
            if technician is not None:
                script_params["Technician"] = technician
            if priority is not None:
                script_params["Priority"] = priority
            if urgency is not None:
                script_params["Urgency"] = urgency
            if category is not None:
                script_params["Category"] = category
            if request_template is not None:
                script_params["Request Template"] = request_template
            if request_type is not None:
                script_params["Request Type"] = request_type
            if due_by_time_ms is not None:
                script_params["Due By Time (ms)"] = due_by_time_ms
            if mode is not None:
                script_params["Mode"] = mode
            if level is not None:
                script_params["Level"] = level
            if site is not None:
                script_params["Site"] = site
            if group is not None:
                script_params["Group"] = group
            if impact is not None:
                script_params["Impact"] = impact
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Create Request - Dropdown Lists",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Create Request - Dropdown Lists",
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
                print(f"Error executing action ServiceDeskPlusV3_Create Request - Dropdown Lists for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_add_note_and_wait_for_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The requests' ID.")], note: Annotated[str, Field(..., description="The note's content.")], show_to_requester: Annotated[bool, Field(default=None, description="Specify whether the note should be shown to the requester or not.")], notify_technician: Annotated[bool, Field(default=None, description="Specify whether the note should be shown to the requester or not")], mark_first_response: Annotated[bool, Field(default=None, description="Specify whether this note should be marked as first response")], add_to_linked_requests: Annotated[bool, Field(default=None, description="Specify whether this note should be added to the linked requests")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a note to a request. Note: Please update the actual time you would like the action to run in the IDE timeout section for this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Note"] = note
            if show_to_requester is not None:
                script_params["Show To Requester"] = show_to_requester
            if notify_technician is not None:
                script_params["Notify Technician"] = notify_technician
            if mark_first_response is not None:
                script_params["Mark First Response"] = mark_first_response
            if add_to_linked_requests is not None:
                script_params["Add To Linked Requests"] = add_to_linked_requests
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Add Note And Wait For Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Add Note And Wait For Reply",
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
                print(f"Error executing action ServiceDeskPlusV3_Add Note And Wait For Reply for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to ServiceDesk Plus instance.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
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
                actionName="ServiceDeskPlusV3_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Ping",
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
                print(f"Error executing action ServiceDeskPlusV3_Ping for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_update_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request to update.")], subject: Annotated[str, Field(default=None, description="The subject of the request.")], requester: Annotated[str, Field(default=None, description="The requester of the request. If not specified, set to the user of the API key.")], description: Annotated[str, Field(default=None, description="The description of the request.")], assets: Annotated[str, Field(default=None, description="Names of Assets to be associated with the request")], status: Annotated[str, Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[str, Field(default=None, description="The priority of the request.")], urgency: Annotated[str, Field(default=None, description="The urgency of the request.")], category: Annotated[str, Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[str, Field(default=None, description="The type of the request. i.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[str, Field(default=None, description="The mode in which this request is created.Example : E-mail")], level: Annotated[str, Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="Denotes the site to which this request belongs")], group: Annotated[str, Field(default=None, description="Group to which this request belongs")], impact: Annotated[str, Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a ServiceDesk Plus request via it’s ID

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            if subject is not None:
                script_params["Subject"] = subject
            if requester is not None:
                script_params["Requester"] = requester
            if description is not None:
                script_params["Description"] = description
            if assets is not None:
                script_params["Assets"] = assets
            if status is not None:
                script_params["Status"] = status
            if technician is not None:
                script_params["Technician"] = technician
            if priority is not None:
                script_params["Priority"] = priority
            if urgency is not None:
                script_params["Urgency"] = urgency
            if category is not None:
                script_params["Category"] = category
            if request_template is not None:
                script_params["Request Template"] = request_template
            if request_type is not None:
                script_params["Request Type"] = request_type
            if due_by_time_ms is not None:
                script_params["Due By Time (ms)"] = due_by_time_ms
            if mode is not None:
                script_params["Mode"] = mode
            if level is not None:
                script_params["Level"] = level
            if site is not None:
                script_params["Site"] = site
            if group is not None:
                script_params["Group"] = group
            if impact is not None:
                script_params["Impact"] = impact
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Update Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Update Request",
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
                print(f"Error executing action ServiceDeskPlusV3_Update Request for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_get_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about a request In Service Desk Plus.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Get Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Get Request",
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
                print(f"Error executing action ServiceDeskPlusV3_Get Request for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_close_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The requests' ID.")], comment: Annotated[str, Field(..., description="Closing comment.")], resolution_acknowledged: Annotated[bool, Field(default=None, description="Whether the resolution of the request is acknowledged or not.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Close a request

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Comment"] = comment
            if resolution_acknowledged is not None:
                script_params["Resolution Acknowledged"] = resolution_acknowledged
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Close Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Close Request",
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
                print(f"Error executing action ServiceDeskPlusV3_Close Request for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_wait_for_field_update(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request.")], values: Annotated[str, Field(..., description="Desired values for the given field.")], field_name: Annotated[str, Field(..., description="The name of the field to be updated.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for a field of a request ot update to a desired value. Note: Please update the actual time you would like the action to run in the IDE timeout section for this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Values"] = values
            script_params["Field Name"] = field_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Wait For Field Update",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Wait For Field Update",
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
                print(f"Error executing action ServiceDeskPlusV3_Wait For Field Update for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_add_note(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The requests' ID.")], note: Annotated[str, Field(..., description="The note's content.")], show_to_requester: Annotated[bool, Field(default=None, description="Specify whether the note should be shown to the requester or not.")], notify_technician: Annotated[bool, Field(default=None, description="Specify whether the note should be shown to the requester or not")], mark_first_response: Annotated[bool, Field(default=None, description="Specify whether this note should be marked as first response")], add_to_linked_requests: Annotated[bool, Field(default=None, description="Specify whether this note should be added to the linked requests")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a note to a request

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Note"] = note
            if show_to_requester is not None:
                script_params["Show To Requester"] = show_to_requester
            if notify_technician is not None:
                script_params["Notify Technician"] = notify_technician
            if mark_first_response is not None:
                script_params["Mark First Response"] = mark_first_response
            if add_to_linked_requests is not None:
                script_params["Add To Linked Requests"] = add_to_linked_requests
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Add Note",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Add Note",
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
                print(f"Error executing action ServiceDeskPlusV3_Add Note for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_v3_wait_for_status_update(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request.")], values: Annotated[str, Field(..., description="Desired values for the given field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for the status of a request ot update to a desired status. Note: Please update the actual time you would like the action to run in the IDE timeout section for this action.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlusV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlusV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Values"] = values
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlusV3_Wait For Status Update",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlusV3_Wait For Status Update",
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
                print(f"Error executing action ServiceDeskPlusV3_Wait For Status Update for ServiceDeskPlusV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlusV3")
            return {"Status": "Failed", "Message": "No active instance found."}
