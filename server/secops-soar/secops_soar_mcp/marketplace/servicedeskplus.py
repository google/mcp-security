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
    # This function registers all tools (actions) for the ServiceDeskPlus integration.

    @mcp.tool()
    async def service_desk_plus_create_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the request.")], requester: Annotated[str, Field(default=None, description="The requester of the request. If not specified, set to the user of the API key.")], description: Annotated[str, Field(default=None, description="The description of the request.")], status: Annotated[str, Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[str, Field(default=None, description="The priority of the request.")], urgency: Annotated[str, Field(default=None, description="The urgency of the request.")], category: Annotated[str, Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[str, Field(default=None, description="The type of the request. I.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[str, Field(default=None, description="The mode of the request.")], level: Annotated[str, Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="The site of the request.")], group: Annotated[str, Field(default=None, description="The group of the request.")], impact: Annotated[str, Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            if requester is not None:
                script_params["Requester"] = requester
            if description is not None:
                script_params["Description"] = description
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
                actionName="ServiceDeskPlus_Create Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Create Request",
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
                print(f"Error executing action ServiceDeskPlus_Create Request for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_create_alert_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="The subject of the request.")], requester: Annotated[str, Field(default=None, description="The requester of the request. If not specified, set to the user of the API key.")], status: Annotated[str, Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[str, Field(default=None, description="The priority of the request.")], urgency: Annotated[str, Field(default=None, description="The urgency of the request.")], category: Annotated[str, Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[str, Field(default=None, description="The type of the request. I.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[str, Field(default=None, description="The mode of the request.")], level: Annotated[str, Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="The site of the request.")], group: Annotated[str, Field(default=None, description="The group of the request.")], impact: Annotated[str, Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an request related to a Siemplify alert

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            if requester is not None:
                script_params["Requester"] = requester
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
                actionName="ServiceDeskPlus_Create Alert Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Create Alert Request",
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
                print(f"Error executing action ServiceDeskPlus_Create Alert Request for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_add_note_and_wait_for_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The requests' ID.")], note: Annotated[str, Field(..., description="The note's content.")], is_public: Annotated[bool, Field(..., description="Whether to make the note public or not.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a note and wait for new notes to be added to the given request.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Note"] = note
            script_params["Is Public"] = is_public
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlus_Add Note And Wait For Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Add Note And Wait For Reply",
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
                print(f"Error executing action ServiceDeskPlus_Add Note And Wait For Reply for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
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
                actionName="ServiceDeskPlus_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Ping",
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
                print(f"Error executing action ServiceDeskPlus_Ping for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_update_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The id of the request to update.")], requester: Annotated[str, Field(default=None, description="The requester of the request. If not specified, set to the user of the API key.")], description: Annotated[str, Field(default=None, description="The description of the request.")], status: Annotated[str, Field(default=None, description="The status of the request.")], technician: Annotated[str, Field(default=None, description="The name of the technician assigned to the request.")], priority: Annotated[str, Field(default=None, description="The priority of the request.")], urgency: Annotated[str, Field(default=None, description="The urgency of the request.")], category: Annotated[str, Field(default=None, description="The category of the request.")], request_template: Annotated[str, Field(default=None, description="The template of the request.")], request_type: Annotated[str, Field(default=None, description="The type of the request. I.e: Incident, Service Request, etc.")], due_by_time_ms: Annotated[str, Field(default=None, description="The due date of the request in milliseconds.")], mode: Annotated[str, Field(default=None, description="The mode of the request.")], level: Annotated[str, Field(default=None, description="The level of the request.")], site: Annotated[str, Field(default=None, description="The site of the request.")], group: Annotated[str, Field(default=None, description="The group of the request.")], impact: Annotated[str, Field(default=None, description="The impact of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a request

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            if requester is not None:
                script_params["Requester"] = requester
            if description is not None:
                script_params["Description"] = description
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
                actionName="ServiceDeskPlus_Update Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Update Request",
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
                print(f"Error executing action ServiceDeskPlus_Update Request for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_get_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about a request

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
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
                actionName="ServiceDeskPlus_Get Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Get Request",
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
                print(f"Error executing action ServiceDeskPlus_Get Request for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_close_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The request's ID.")], comment: Annotated[str, Field(..., description="Closing comment.")], resolution_acknowledged: Annotated[bool, Field(..., description="Whether the resolution of the request is acknowledged or not.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Comment"] = comment
            script_params["Resolution Acknowledged"] = resolution_acknowledged
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlus_Close Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Close Request",
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
                print(f"Error executing action ServiceDeskPlus_Close Request for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_wait_for_field_update(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request.")], field_name: Annotated[str, Field(..., description="The name of the field to be updated.")], values: Annotated[str, Field(..., description="Desired values for the given field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for a field of a request ot update to a desired value.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Field Name"] = field_name
            script_params["Values"] = values
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlus_Wait For Field Update",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Wait For Field Update",
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
                print(f"Error executing action ServiceDeskPlus_Wait For Field Update for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_add_note(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The requests' ID.")], note: Annotated[str, Field(..., description="The note's content.")], is_public: Annotated[bool, Field(..., description="Whether to make the note public or not.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Note"] = note
            script_params["Is Public"] = is_public
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlus_Add Note",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Add Note",
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
                print(f"Error executing action ServiceDeskPlus_Add Note for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def service_desk_plus_wait_for_status_update(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], request_id: Annotated[str, Field(..., description="The ID of the request.")], statuses: Annotated[str, Field(..., description="Desired request statuses, comma separated.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for the status of a request ot update to a desired status.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ServiceDeskPlus")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ServiceDeskPlus: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Request ID"] = request_id
            script_params["Statuses"] = statuses
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ServiceDeskPlus_Wait For Status Update",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ServiceDeskPlus_Wait For Status Update",
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
                print(f"Error executing action ServiceDeskPlus_Wait For Status Update for ServiceDeskPlus: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ServiceDeskPlus")
            return {"Status": "Failed", "Message": "No active instance found."}
