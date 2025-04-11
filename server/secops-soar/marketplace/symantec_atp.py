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
import bindings
from mcp.server.fastmcp import FastMCP
from utils.consts import Endpoints
from utils.models import ApiManualActionDataModel, EmailContent, TargetEntity
import json
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the SymantecATP integration.

    @mcp.tool()
    async def symantec_atp_update_incident_resolution(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_uuid: Annotated[str, Field(..., description="Specify the UUID of the incident.")], resolution_status: Annotated[List[Any], Field(..., description="Specify what resolution status to set on the incident.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update resolution on the incident.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Incident UUID"] = incident_uuid
            script_params["Resolution Status"] = resolution_status

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Update Incident Resolution",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Update Incident Resolution", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Update Incident Resolution for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_get_sandbox_commands_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], commands_i_ds: Annotated[str, Field(..., description="Sandbox Command ID to fetch the status for.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get commands status by id.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Commands IDs"] = commands_i_ds

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Get Sandbox Commands Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Get Sandbox Commands Status", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Get Sandbox Commands Status for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_add_to_black_list(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a black list policy for an entity

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Add To Black list",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Add To Black list", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Add To Black list for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_get_events_for_entity(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], minutes_back_to_fetch: Annotated[str, Field(..., description="Fetch the event x minutes back. Limit is 7 days, or 10080 minutes. This is Symantec ATP limitation.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch all events for an entity since time

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Minutes Back To Fetch"] = minutes_back_to_fetch

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Get Events  For Entity",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Get Events  For Entity", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Get Events  For Entity for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_add_comment_to_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_uuid: Annotated[str, Field(..., description="Specify the UUID of the incident.")], comment: Annotated[str, Field(..., description="Specify the comment that you want to add to the incident. Limit is 512 characters. This is Symantec ATP limitation.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Attach comment to incident.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Incident UUID"] = incident_uuid
            script_params["Comment"] = comment

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Add Comment To Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Add Comment To Incident", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Add Comment To Incident for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_revoke_from_black_list(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete black list policy for a given entity

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Revoke From Black list",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Revoke From Black list", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Revoke From Black list for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_delete_allowlist_policy(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete Allowlist policy for entity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Delete Allowlist Policy",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Delete Allowlist Policy", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Delete Allowlist Policy for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_get_incident_comments(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_uuid: Annotated[str, Field(..., description="Specify the UUID of the incident.")], max_comments_to_return: Annotated[Optional[str], Field(default=None, description="Specify how many comments to return. Maximum is 1000 comments. This is a Symantec ATP limitation.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve comments related to the incident.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Incident UUID"] = incident_uuid
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Get Incident Comments",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Get Incident Comments", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Get Incident Comments for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_get_events_free_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Free query text.")], limit: Annotated[str, Field(..., description="Limit of query results. Note: Limit is 5000 events. This is Symantec ATP limitation.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch events by free query

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Query"] = query
            script_params["Limit"] = limit

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Get Events Free Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Get Events Free Query", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Get Events Free Query for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Ping", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Ping for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_add_to_allowlist(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create new allowlist policy. Note: MD5 hashes couldn’t be added to the allowlist, it's the Symantec ATP limitation.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Add To Allowlist",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Add To Allowlist", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Add To Allowlist for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_close_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_uuid: Annotated[str, Field(..., description="Specify the UUID of the incident")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Change incident status to closed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Incident UUID"] = incident_uuid

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Close Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Close Incident", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Close Incident for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_delete_black_list_policy(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete a black list policy for a Siemplify entity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Delete Black list Policy",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Delete Black list Policy", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Delete Black list Policy for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_enrich_file_hash(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich SHA2 hash using Symantec ATP information.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Enrich File Hash",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Enrich File Hash", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Enrich File Hash for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_delete_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_hash: Annotated[str, Field(..., description="File hash to delete.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete file from an endpoint

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["File Hash"] = file_hash

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Delete File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Delete File", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Delete File for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_rejoin_endpoint(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Rejoin endpoint in Symantec Endpoint Protection

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Rejoin Endpoint",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Rejoin Endpoint", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Rejoin Endpoint for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_isolate_endpoint(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Isolate an endpoint on Symantec Endpoint Protection

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Isolate Endpoint",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Isolate Endpoint", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Isolate Endpoint for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_submit_files_to_sandbox(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Submit file hashes to sandbox.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
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
                actionName="SymantecATP_Submit Files To Sandbox",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Submit Files To Sandbox", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Submit Files To Sandbox for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def symantec_atp_get_commands_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], commands_i_ds: Annotated[str, Field(..., description="Command ID to fetch the status for.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get status of a command

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SymantecATP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SymantecATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Commands IDs"] = commands_i_ds

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SymantecATP_Get Commands Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SymantecATP_Get Commands Status", # Assuming same as actionName
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
                print(f"Error executing action SymantecATP_Get Commands Status for SymantecATP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SymantecATP")
            return {"Status": "Failed", "Message": "No active instance found."}
