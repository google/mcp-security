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
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the CiscoOrbital integration.

    @mcp.tool()
    async def cisco_orbital_execute_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query that needs to be executed.")], name: Annotated[Optional[str], Field(default=None, description="Specify the name for the query job. If nothing is specified, action will use a name in the following format: Siemplify-{guid}")], custom_context_fields: Annotated[Optional[str], Field(default=None, description="Specify additional custom context fields that should be added to the job. Format: key_1:value_1,key_2:value_1.")], max_results_to_return: Annotated[Optional[str], Field(default=None, description="Specify how many results should be returned.")], hide_case_wall_table: Annotated[Optional[bool], Field(default=None, description="If enabled, action will not prepare a case wall table.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute queries on endpoints based on IP and Hostname entities in Cisco Orbital. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed. Maximum timeout is 24 hours.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoOrbital")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for CiscoOrbital: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Query"] = query
            if name is not None:
                script_params["Name"] = name
            if custom_context_fields is not None:
                script_params["Custom Context Fields"] = custom_context_fields
            if max_results_to_return is not None:
                script_params["Max Results To Return"] = max_results_to_return
            if hide_case_wall_table is not None:
                script_params["Hide Case Wall Table"] = hide_case_wall_table
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="CiscoOrbital_Execute Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoOrbital_Execute Query", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action CiscoOrbital_Execute Query for CiscoOrbital: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoOrbital")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_orbital_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Cisco Orbital with parameters provided at the integration configuration page on the Marketplace tab.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoOrbital")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for CiscoOrbital: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="CiscoOrbital_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoOrbital_Ping", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action CiscoOrbital_Ping for CiscoOrbital: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoOrbital")
            return {"Status": "Failed", "Message": "No active instance found."}
