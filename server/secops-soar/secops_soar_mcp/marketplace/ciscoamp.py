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
    # This function registers all tools (actions) for the CiscoAMP integration.

    @mcp.tool()
    async def cisco_amp_get_computers_by_network_activity_url(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch a list of computers that have connected to the given hostname or URL

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Computers By Network Activity (URL)",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Computers By Network Activity (URL)",
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
                print(f"Error executing action CiscoAMP_Get Computers By Network Activity (URL) for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_computers_by_network_activity_ip(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch a list of computers that have connected to the given IP address

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Computers By Network Activity (Ip)",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Computers By Network Activity (Ip)",
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
                print(f"Error executing action CiscoAMP_Get Computers By Network Activity (Ip) for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_add_file_to_file_list(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_list_name: Annotated[str, Field(..., description="File Blacklist")], description: Annotated[str, Field(..., description="Description of the file")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a SHA-256 for a specific file list

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["File List Name"] = file_list_name
            script_params["Description"] = description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CiscoAMP_Add File To File List",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Add File To File List",
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
                print(f"Error executing action CiscoAMP_Add File To File List for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_unisolate_machine(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Stop isolation of Machine by connector guid.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Unisolate Machine",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Unisolate Machine",
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
                print(f"Error executing action CiscoAMP_Unisolate Machine for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_groups(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get group details

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Groups",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Groups",
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
                print(f"Error executing action CiscoAMP_Get Groups for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_computers_by_file_hash(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch a list of computers that have observed files with the given SHA-256 value

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Computers By File Hash",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Computers By File Hash",
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
                print(f"Error executing action CiscoAMP_Get Computers By File Hash for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_file_lists_by_policy(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], policy_name: Annotated[str, Field(..., description="The name of the policy e.g. Triage")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get the file lists that are assigned in a policy

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Policy Name"] = policy_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CiscoAMP_Get File Lists By Policy",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get File Lists By Policy",
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
                print(f"Error executing action CiscoAMP_Get File Lists By Policy for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_create_group(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], group_name: Annotated[str, Field(..., description="The name of the new group")], group_description: Annotated[str, Field(..., description="The description of the new group")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a new group

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Group Name"] = group_name
            script_params["Group Description"] = group_description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CiscoAMP_Create Group",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Create Group",
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
                print(f"Error executing action CiscoAMP_Create Group for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_computers_by_file_name(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch a list of computers that have observed files with the given file name

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Computers By File Name",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Computers By File Name",
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
                print(f"Error executing action CiscoAMP_Get Computers By File Name for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to Cisco AMP.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Ping",
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
                print(f"Error executing action CiscoAMP_Ping for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_file_list_items(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_list_name: Annotated[str, Field(..., description="e.g. File Blacklist")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get the items listed in a given file list

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["File List Name"] = file_list_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CiscoAMP_Get File List Items",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get File List Items",
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
                print(f"Error executing action CiscoAMP_Get File List Items for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_policies(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get policy details

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Policies",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Policies",
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
                print(f"Error executing action CiscoAMP_Get Policies for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_get_computer_info(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get details about a computer

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Get Computer Info",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Get Computer Info",
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
                print(f"Error executing action CiscoAMP_Get Computer Info for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cisco_amp_isolate_machine(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Isolate Machine by connector guid.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CiscoAMP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CiscoAMP: {e}")
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
                actionName="CiscoAMP_Isolate Machine",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CiscoAMP_Isolate Machine",
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
                print(f"Error executing action CiscoAMP_Isolate Machine for CiscoAMP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CiscoAMP")
            return {"Status": "Failed", "Message": "No active instance found."}
