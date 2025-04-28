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
    # This function registers all tools (actions) for the Okta integration.

    @mcp.tool()
    async def okta_list_providers(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[Optional[str], Field(default=None, description="Search the name property for a match")], type: Annotated[Optional[str], Field(default=None, description="Filter by type")], limit: Annotated[Optional[str], Field(default=None, description="Max amount of results to return")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List identity providers (IdPs) in your organization

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if query is not None:
                script_params["Query"] = query
            if type is not None:
                script_params["Type"] = type
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
                actionName="Okta_List Providers",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_List Providers",
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
                print(f"Error executing action Okta_List Providers for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_assign_role(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], role_types: Annotated[str, Field(..., description="The type of role to assign to the users")], user_i_ds: Annotated[Optional[str], Field(default=None, description="Ids of users in Okta")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Assign a role to a user

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds is not None:
                script_params["User IDs"] = user_i_ds
            script_params["Role Types"] = role_types
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Assign Role",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Assign Role",
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
                print(f"Error executing action Okta_Assign Role for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_unassign_role(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], role_i_ds_or_names: Annotated[str, Field(..., description="Ids or names of roles in Okta")], user_i_ds: Annotated[Optional[str], Field(default=None, description="Ids of users in Okta")], is_id: Annotated[Optional[bool], Field(default=None, description="Whether the values are ids or names")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Unassign a role from a user

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds is not None:
                script_params["User IDs"] = user_i_ds
            script_params["Role IDs Or Names"] = role_i_ds_or_names
            if is_id is not None:
                script_params["Is Id"] = is_id
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Unassign Role",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Unassign Role",
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
                print(f"Error executing action Okta_Unassign Role for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_disable_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], user_i_ds_or_logins: Annotated[Optional[str], Field(default=None, description="Ids of users in Okta")], is_deactivate: Annotated[Optional[bool], Field(default=None, description="Whether to dactivate or only suspend the user")], send_email_if_deactivate: Annotated[Optional[bool], Field(default=None, description="Whether to send an email after deactivating or not")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Disables the specified user

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds_or_logins is not None:
                script_params["User IDs Or Logins"] = user_i_ds_or_logins
            if is_deactivate is not None:
                script_params["Is Deactivate"] = is_deactivate
            if send_email_if_deactivate is not None:
                script_params["Send Email If Deactivate"] = send_email_if_deactivate
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Disable User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Disable User",
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
                print(f"Error executing action Okta_Disable User for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_get_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], user_ids_or_logins: Annotated[Optional[str], Field(default=None, description="Ids or logins (email or short email name) of a user in Okta, e.g. test@gmail.com or simply 'test'")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get information about a user

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_ids_or_logins is not None:
                script_params["User Ids Or Logins"] = user_ids_or_logins
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Get User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Get User",
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
                print(f"Error executing action Okta_Get User for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connection With Okta

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
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
                actionName="Okta_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Ping",
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
                print(f"Error executing action Okta_Ping for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_list_user_groups(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], user_i_ds_or_logins: Annotated[Optional[str], Field(default=None, description="Ids or logins of users in Okta")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get the groups that the user is a member of

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds_or_logins is not None:
                script_params["User IDs Or Logins"] = user_i_ds_or_logins
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_List User Groups",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_List User Groups",
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
                print(f"Error executing action Okta_List User Groups for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_get_group(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], group_ids_or_names: Annotated[str, Field(..., description="Ids or names of groups in Okta")], is_id: Annotated[Optional[bool], Field(default=None, description="Whether the value is an id or a name")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get information about a group

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Group Ids Or Names"] = group_ids_or_names
            if is_id is not None:
                script_params["Is Id"] = is_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Get Group",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Get Group",
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
                print(f"Error executing action Okta_Get Group for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_add_group(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], group_name: Annotated[str, Field(..., description="The name of the group in Okta")], group_description: Annotated[Optional[str], Field(default=None, description="The description for the group")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a group

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Group Name"] = group_name
            if group_description is not None:
                script_params["Group Description"] = group_description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Add Group",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Add Group",
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
                print(f"Error executing action Okta_Add Group for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_reset_password(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], user_i_ds_or_logins: Annotated[Optional[str], Field(default=None, description="Ids or logins of users in Okta")], send_email: Annotated[Optional[bool], Field(default=None, description="Whether to send an email for the password reset or return the token for every user")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Generate a one-time token that can be used to reset a user's password

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds_or_logins is not None:
                script_params["User IDs Or Logins"] = user_i_ds_or_logins
            if send_email is not None:
                script_params["Send Email"] = send_email
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Reset Password",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Reset Password",
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
                print(f"Error executing action Okta_Reset Password for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_list_roles(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], user_i_ds: Annotated[Optional[str], Field(default=None, description="Ids of users in Okta")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Lists all roles assigned to a user

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds is not None:
                script_params["User IDs"] = user_i_ds
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_List Roles",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_List Roles",
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
                print(f"Error executing action Okta_List Roles for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_enable_user(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], user_i_ds_or_logins: Annotated[Optional[str], Field(default=None, description="Ids or logins of users in Okta")], is_activate: Annotated[Optional[bool], Field(default=None, description="Whether to activate the user or just unsuspend")], send_email_if_activate: Annotated[Optional[bool], Field(default=None, description="Whether to send an email after activating or not")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enables the specified user

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds_or_logins is not None:
                script_params["User IDs Or Logins"] = user_i_ds_or_logins
            if is_activate is not None:
                script_params["Is Activate"] = is_activate
            if send_email_if_activate is not None:
                script_params["Send Email If Activate"] = send_email_if_activate
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Enable User",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Enable User",
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
                print(f"Error executing action Okta_Enable User for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_set_password(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], new_password: Annotated[str, Field(..., description="The new password")], user_i_ds_or_logins: Annotated[Optional[str], Field(default=None, description="Ids or logins of users in Okta")], add_10_random_chars: Annotated[Optional[bool], Field(default=None, description="Whether to add extra characters to every user password or not")], also_run_on_scope: Annotated[Optional[bool], Field(default=None, description="Whether to run on entities as well as the input")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Set the password of a user without validating existing credentials

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if user_i_ds_or_logins is not None:
                script_params["User IDs Or Logins"] = user_i_ds_or_logins
            script_params["New Password"] = new_password
            if add_10_random_chars is not None:
                script_params["Add 10 Random Chars"] = add_10_random_chars
            if also_run_on_scope is not None:
                script_params["Also Run On Scope"] = also_run_on_scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Okta_Set Password",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_Set Password",
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
                print(f"Error executing action Okta_Set Password for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def okta_list_users(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[Optional[str], Field(default=None, description="Search for a match in the firstname, lastname or in the email")], filter: Annotated[Optional[str], Field(default=None, description="Custom search query for a subset of properties")], search: Annotated[Optional[str], Field(default=None, description="Custom search query for most properties")], limit: Annotated[Optional[str], Field(default=None, description="Max amount of results to return")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get the list of users

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Okta")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Okta: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if query is not None:
                script_params["Query"] = query
            if filter is not None:
                script_params["Filter"] = filter
            if search is not None:
                script_params["Search"] = search
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
                actionName="Okta_List Users",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Okta_List Users",
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
                print(f"Error executing action Okta_List Users for Okta: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Okta")
            return {"Status": "Failed", "Message": "No active instance found."}
