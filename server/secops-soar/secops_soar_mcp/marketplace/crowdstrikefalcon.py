# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
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
    # This function registers all tools (actions) for the CrowdStrikeFalcon integration.

    @mcp.tool()
    async def crowd_strike_falcon_add_comment_to_detection(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], detection_id: Annotated[str, Field(..., description="Specify the id of the detection to which you want to add a comment.")], comment: Annotated[str, Field(..., description="Specify the comment that needs to be added to the detection.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to the detection in Crowdstrike Falcon.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Detection ID"] = detection_id
            script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Add Comment to Detection",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Add Comment to Detection",
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
                print(f"Error executing action CrowdStrikeFalcon_Add Comment to Detection for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_submit_url(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ur_ls: Annotated[str, Field(..., description="Specify the URLs that need to be submitted.")], sandbox_environment: Annotated[List[str], Field(default=None, description="Specify the sandbox environment for the analysis.")], network_environment: Annotated[List[str], Field(default=None, description="Specify the network environment for the analysis.")], check_duplicate: Annotated[bool, Field(default=None, description="If enabled, the action checks if the file was already submitted previously and returns an available report. Note: during the validation \u201cNetwork Environment\u201d and \u201cSandbox Environment\u201d are not taken into consideration.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Submit urls to a sandbox in Crowdstrike. Note: This action requires a Falcon Sandbox license.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["URLs"] = ur_ls
            if sandbox_environment is not None:
                script_params["Sandbox Environment"] = sandbox_environment
            if network_environment is not None:
                script_params["Network Environment"] = network_environment
            if check_duplicate is not None:
                script_params["Check Duplicate"] = check_duplicate
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Submit URL",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Submit URL",
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
                print(f"Error executing action CrowdStrikeFalcon_Submit URL for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_update_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the ID of the incident that needs to be updated.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], status: Annotated[List[str], Field(default=None, description="Specify the status for the incident.")], assign_to: Annotated[str, Field(default=None, description="Specify the name or email of the analyst to whom the incident needs to be assigned. If \"Unassign\" is provided, action will remove assignment from the incident. Note: for name you need to provide first and last name of the analyst in the following format \"{first name} {last name}\"")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update incident in Crowdstrike.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            script_params["Incident ID"] = incident_id
            if status is not None:
                script_params["Status"] = status
            if assign_to is not None:
                script_params["Assign to"] = assign_to
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Update Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Update Incident",
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
                print(f"Error executing action CrowdStrikeFalcon_Update Incident for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_run_script(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], script_name: Annotated[str, Field(default=None, description="The name of the script file that needs to be executed. Note: either \u201cScript Name\u201d or \u201cRaw Script\u201d should be provided. If both \u201cScript Name\u201d and \u201cRaw Script\u201d are provided, then \u201cRaw Script\u201d will have the priority.")], raw_script: Annotated[str, Field(default=None, description="Raw powershell script payload that needs to be executed on the endpoints. Note: either \u201cScript Name\u201d or \u201cRaw Script\u201d should be provided. If both \u201cScript Name\u201d and \u201cRaw Script\u201d are provided, then \u201cRaw Script\u201d will have the priority.")], hostname: Annotated[str, Field(default=None, description="Comma-separated list of hostnames on which you want to execute the action. Note: action will run the action on both entities + this parameter values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute a powershell script on the endpoints in Crowdstrike. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for the action, as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            if script_name is not None:
                script_params["Script Name"] = script_name
            if raw_script is not None:
                script_params["Raw Script"] = raw_script
            if hostname is not None:
                script_params["Hostname"] = hostname
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Run Script",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Run Script",
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
                print(f"Error executing action CrowdStrikeFalcon_Run Script for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_execute_command(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], command: Annotated[str, Field(..., description="Specify what command to execute on the hosts.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], admin_command: Annotated[bool, Field(default=None, description="If enabled, action will execute commands with the admin level permissions. This is necessary for certain commands like \"put\".")], hostname: Annotated[str, Field(default=None, description="Comma-separated list of hostnames on which you want to execute the action. Note: action will run the action on both entities + this parameter values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute commands on the hosts in Crowdstrike Falcon. Supported entities: IP Address and Hostname.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            script_params["Command"] = command
            if admin_command is not None:
                script_params["Admin Command"] = admin_command
            if hostname is not None:
                script_params["Hostname"] = hostname
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Execute Command",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Execute Command",
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
                print(f"Error executing action CrowdStrikeFalcon_Execute Command for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_close_detection(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], detection_id: Annotated[str, Field(..., description="Specify the id of the detection that needs to be closed.")], hide_detection: Annotated[bool, Field(default=None, description="If enabled, action will hide the detection in the UI.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Close a Crowdstrike Falcon detection. Note: Action "Update Detection" is the best practice for this use case.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Detection ID"] = detection_id
            if hide_detection is not None:
                script_params["Hide Detection"] = hide_detection
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Close Detection",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Close Detection",
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
                print(f"Error executing action CrowdStrikeFalcon_Close Detection for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_add_incident_comment(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the ID of the incident that needs to be updated.")], comment: Annotated[str, Field(..., description="Specify the comment for the incident.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add comment to incident in Crowdstrike.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident ID"] = incident_id
            script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Add Incident Comment",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Add Incident Comment",
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
                print(f"Error executing action CrowdStrikeFalcon_Add Incident Comment for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_update_alert(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], alert_id: Annotated[str, Field(..., description="Specify the ID of the alert that needs to be updated.")], status: Annotated[List[str], Field(default=None, description="Specify the status for the alert.")], verdict: Annotated[List[str], Field(default=None, description="Specify the verdict for the alert.")], assign_to: Annotated[str, Field(default=None, description="Specify the name of the analyst to whom the alert needs to be assigned. If \"Unassign\" is provided, action will remove assignment from the alert. Note: API will accept any value that is provided, even if the underlying user doesn\u2019t exist.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update an alert in Crowdstrike.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Alert ID"] = alert_id
            if status is not None:
                script_params["Status"] = status
            if verdict is not None:
                script_params["Verdict"] = verdict
            if assign_to is not None:
                script_params["Assign To"] = assign_to
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Update Alert",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Update Alert",
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
                print(f"Error executing action CrowdStrikeFalcon_Update Alert for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_list_hosts(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what logic should be used, when searching for hosts.")], filter_value: Annotated[str, Field(default=None, description="Specify the value that should be used to filter hosts.")], max_hosts_to_return: Annotated[str, Field(default=None, description="Specify how many hosts to return. Default: 50. Maximum: 1000.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List available hosts in Crowdstrike Falcon.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            if filter_logic is not None:
                script_params["Filter Logic"] = filter_logic
            if filter_value is not None:
                script_params["Filter Value"] = filter_value
            if max_hosts_to_return is not None:
                script_params["Max Hosts To Return"] = max_hosts_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_List Hosts",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_List Hosts",
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
                print(f"Error executing action CrowdStrikeFalcon_List Hosts for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_add_identity_protection_detection_comment(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], detection_id: Annotated[str, Field(..., description="Specify the ID of the detection that needs to be updated.")], comment: Annotated[str, Field(..., description="Specify the comment for the detection.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to identity protection detection in Crowdstrike.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Detection ID"] = detection_id
            script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Add Identity Protection Detection Comment",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Add Identity Protection Detection Comment",
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
                print(f"Error executing action CrowdStrikeFalcon_Add Identity Protection Detection Comment for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_get_hosts_by_ioc(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """DEPRECATED. List hosts related to the IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash. Note: Hostname entities are treated as domain IOCs and action will extract domain part out of URLs. Only MD5 and SHA-256 hashes are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
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
                actionName="CrowdStrikeFalcon_Get Hosts by IOC",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Get Hosts by IOC",
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
                print(f"Error executing action CrowdStrikeFalcon_Get Hosts by IOC for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
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
                actionName="CrowdStrikeFalcon_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Ping",
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
                print(f"Error executing action CrowdStrikeFalcon_Ping for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_contain_endpoint(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], fail_if_timeout: Annotated[bool, Field(default=None, description="If enabled, action will be failed, if not all of the endpoints were contained.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Contain endpoint in Crowdstrike Falcon. Supported entities: Hostname and IP address.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            if fail_if_timeout is not None:
                script_params["Fail If Timeout"] = fail_if_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Contain Endpoint",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Contain Endpoint",
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
                print(f"Error executing action CrowdStrikeFalcon_Contain Endpoint for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_add_alert_comment(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], alert_id: Annotated[str, Field(..., description="Specify the ID of the alert that needs to be updated.")], comment: Annotated[str, Field(..., description="Specify the comment for the alert.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to alert in Crowdstrike. 

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Alert ID"] = alert_id
            script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Add Alert Comment",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Add Alert Comment",
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
                print(f"Error executing action CrowdStrikeFalcon_Add Alert Comment for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_update_ioc_information(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], description: Annotated[str, Field(default=None, description="Specify a new description for custom IOCs.")], source: Annotated[str, Field(default=None, description="Specify the source for custom IOCs.")], expiration_days: Annotated[str, Field(default=None, description="Specify the amount of days till expiration.")], detect_policy: Annotated[bool, Field(default=None, description="If enabled, IOCs that have been identifed, will send a notification. In other case, no action will be taken")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update information about custom IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash. Note: Hostname entities are treated as domain IOCs and action will extract domain part out of URLs. Only MD5 and SHA-256 hashes are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if description is not None:
                script_params["Description"] = description
            if source is not None:
                script_params["Source"] = source
            if expiration_days is not None:
                script_params["Expiration days"] = expiration_days
            if detect_policy is not None:
                script_params["Detect policy"] = detect_policy
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Update IOC Information",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Update IOC Information",
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
                print(f"Error executing action CrowdStrikeFalcon_Update IOC Information for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_download_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], download_folder_path: Annotated[str, Field(..., description="Specify the path to the folder, where you want to store the threat file.")], overwrite: Annotated[bool, Field(..., description="If enabled, action will overwrite the file with the same name.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Download files from the hosts in Crowdstrike Falcon. Supported entities: File Name, IP Address and Hostname. Note: action requires both File Name and IP Address/Hostname entity to be in the scope of the Siemplify alert. The downloaded file will be in password-protected zip. Password is "infected".

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
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
                actionName="CrowdStrikeFalcon_Download File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Download File",
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
                print(f"Error executing action CrowdStrikeFalcon_Download File for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_get_event_offset(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_events_to_process: Annotated[str, Field(..., description="Specify how many events the action needs to process starting from the offset from 30 days ago.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will retrieve the event offset that is used by the Event Streaming Connector. Note: action starts processing events from 30 days ago.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Max Events To Process"] = max_events_to_process
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Get Event Offset",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Get Event Offset",
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
                print(f"Error executing action CrowdStrikeFalcon_Get Event Offset for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_upload_io_cs(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], platform: Annotated[str, Field(..., description="Specify a comma-separated list of the platforms related to the IOC. Possible values: Windows, Linux, Mac.")], severity: Annotated[List[str], Field(..., description="Specify the severity for the IOC.")], comment: Annotated[str, Field(default=None, description="Specify a comment with more context related to IOC.")], host_group_name: Annotated[str, Field(default=None, description="Specify the name of the host group.")], action: Annotated[List[str], Field(default=None, description="Specify the action for the uploaded IOCs. Note: \"Block\" action can only be applied to hashes. Action will always apply \"Detect\" policy to all other IOC types.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add custom IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash. Note: Hostname entities are treated as domain IOCs and action will extract domain part out of URLs. Only MD5 and SHA-256 hashes are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Platform"] = platform
            script_params["Severity"] = severity
            if comment is not None:
                script_params["Comment"] = comment
            if host_group_name is not None:
                script_params["Host Group Name"] = host_group_name
            if action is not None:
                script_params["Action"] = action
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Upload IOCs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Upload IOCs",
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
                print(f"Error executing action CrowdStrikeFalcon_Upload IOCs for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_get_host_information(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create insights containing information regarding entities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about the hostname from Crowdstrike Falcon. Supported entities: Hostname, IP Address.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
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
                actionName="CrowdStrikeFalcon_Get Host Information",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Get Host Information",
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
                print(f"Error executing action CrowdStrikeFalcon_Get Host Information for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_on_demand_scan(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_paths_to_scan: Annotated[str, Field(..., description="Comma-separated list of paths to scan.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], file_paths_to_exclude_from_scan: Annotated[str, Field(default=None, description="Comma-separated list of paths to exclude from scanning.")], host_group_name: Annotated[str, Field(default=None, description="Comma-separated list of host group names to initiate scanning for. Note: Separate scanning process is created for each host group.")], scan_description: Annotated[str, Field(default=None, description="Description for the scan. If no value is provided, the action sets the description to the following: \"Scan initialized by Chronicle SecOps.\"")], cpu_priority: Annotated[List[str], Field(default=None, description="The amount of CPU to  use for the underlying host during scanning.")], sensor_anti_malware_detection_level: Annotated[List[str], Field(default=None, description="Specify the sensor anti-malware detection level. Note: Detection level must be equal to or higher than the Prevention level.")], sensor_anti_malware_prevention_level: Annotated[List[str], Field(default=None, description="Specify the sensor anti-malware prevention level. Note: Detection level must be equal to or higher than the Prevention level.")], cloud_anti_malware_detection_level: Annotated[List[str], Field(default=None, description="Specify the cloud anti-malware detection level. Note: Detection level must be equal to or higher than the Prevention level.")], cloud_anti_malware_prevention_level: Annotated[List[str], Field(default=None, description="Specify the cloud anti-malware prevention level. Note: Detection level must be equal to or higher than the Prevention level.")], quarantine_hosts: Annotated[bool, Field(default=None, description="If enabled, underlying hosts are quarantined as part of scanning.")], create_endpoint_notification: Annotated[bool, Field(default=None, description="If enabled, the scanning process creates an endpoint notification.")], max_scan_duration: Annotated[str, Field(default=None, description="Number of hours for a scan to run. If no value is provided, the scan runs continuously.")], hostname: Annotated[str, Field(default=None, description="Comma-separated list of hostnames on which you want to execute the action. Note: action will run the action on both entities + this parameter values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Scan the endpoint on demand in Crowdstrike. Note: only Windows hosts are supported. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Chronicle SecOps IDE for action, as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            script_params["File Paths To Scan"] = file_paths_to_scan
            if file_paths_to_exclude_from_scan is not None:
                script_params["File Paths To Exclude From Scan"] = file_paths_to_exclude_from_scan
            if host_group_name is not None:
                script_params["Host Group Name"] = host_group_name
            if scan_description is not None:
                script_params["Scan Description"] = scan_description
            if cpu_priority is not None:
                script_params["CPU Priority"] = cpu_priority
            if sensor_anti_malware_detection_level is not None:
                script_params["Sensor Anti-malware Detection Level"] = sensor_anti_malware_detection_level
            if sensor_anti_malware_prevention_level is not None:
                script_params["Sensor Anti-malware Prevention Level"] = sensor_anti_malware_prevention_level
            if cloud_anti_malware_detection_level is not None:
                script_params["Cloud Anti-malware Detection Level"] = cloud_anti_malware_detection_level
            if cloud_anti_malware_prevention_level is not None:
                script_params["Cloud Anti-malware Prevention Level"] = cloud_anti_malware_prevention_level
            if quarantine_hosts is not None:
                script_params["Quarantine Hosts"] = quarantine_hosts
            if create_endpoint_notification is not None:
                script_params["Create Endpoint Notification"] = create_endpoint_notification
            if max_scan_duration is not None:
                script_params["Max Scan Duration"] = max_scan_duration
            if hostname is not None:
                script_params["Hostname"] = hostname
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_On-Demand Scan",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_On-Demand Scan",
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
                print(f"Error executing action CrowdStrikeFalcon_On-Demand Scan for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_update_identity_protection_detection(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], detection_id: Annotated[str, Field(..., description="Specify the ID of the detection that needs to be updated.")], status: Annotated[List[str], Field(default=None, description="Specify the status for the detection.")], assign_to: Annotated[str, Field(default=None, description="Specify the name of the analyst to whom the detection needs to be assigned. If \"Unassign\" is provided, action will remove assignment from the detection. Note: API will accept any value that is provided, even if the underlying user doesn't exist.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update an identity protection detection in Crowdstrike. Note: this action requires an Identity Protection license.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Detection ID"] = detection_id
            if status is not None:
                script_params["Status"] = status
            if assign_to is not None:
                script_params["Assign To"] = assign_to
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Update Identity Protection Detection",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Update Identity Protection Detection",
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
                print(f"Error executing action CrowdStrikeFalcon_Update Identity Protection Detection for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_get_process_name_by_ioc(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], devices_names: Annotated[str, Field(..., description="Specify a comma-separated list of devices for which you want to retrieve processes related to entities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """DEPRECATED. Retrieve processes related to the IOCs and provided devices in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash. Note: Hostname entities are treated as domain IOCs and action will extract domain part out of URLs. Only MD5 and SHA-256 hashes are supported. IP address entities are treated as IOCs.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Devices Names"] = devices_names
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Get Process Name By IOC",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Get Process Name By IOC",
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
                print(f"Error executing action CrowdStrikeFalcon_Get Process Name By IOC for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_delete_ioc(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete custom IOCs in Crowdstrike Falcon. Supported entities: Hostname, URL, IP address and Hash. Note: Hostname entities are treated as domain IOCs and action will extract domain part out of URLs. Only MD5 and SHA-256 hashes are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
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
                actionName="CrowdStrikeFalcon_Delete IOC",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Delete IOC",
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
                print(f"Error executing action CrowdStrikeFalcon_Delete IOC for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_list_uploaded_io_cs(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ioc_type_filter: Annotated[str, Field(default=None, description="Specify a comma-separated list of IOC types that should be returned. If nothing is provided, action will return IOCs from all types. Possible values: ipv4,ipv6,md5,sha256,domain.")], value_filter_logic: Annotated[List[str], Field(default=None, description="Specify the value filter logic. If \"Equal\" is selected, action will try to find the exact match among IOCs and if \"Contains\" is selected, action will try to find IOCs that contain that substring.")], value_filter_string: Annotated[str, Field(default=None, description="Specify the string that should be searched among IOCs.")], max_io_cs_to_return: Annotated[str, Field(default=None, description="Specify how many IOCs to return. Default: 50. Maximum: 500.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List available custom IOCs in CrowdStrike Falcon.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if ioc_type_filter is not None:
                script_params["IOC Type Filter"] = ioc_type_filter
            if value_filter_logic is not None:
                script_params["Value Filter Logic"] = value_filter_logic
            if value_filter_string is not None:
                script_params["Value Filter String"] = value_filter_string
            if max_io_cs_to_return is not None:
                script_params["Max IOCs To Return"] = max_io_cs_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_List Uploaded IOCs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_List Uploaded IOCs",
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
                print(f"Error executing action CrowdStrikeFalcon_List Uploaded IOCs for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_submit_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_paths: Annotated[str, Field(..., description="Specify the file paths to the files that need to be submitted. Refer to the documentation portal for a list of the supported file formats.")], sandbox_environment: Annotated[List[str], Field(default=None, description="Specify the sandbox environment for the analysis.")], network_environment: Annotated[List[str], Field(default=None, description="Specify the network environment for the analysis.")], archive_password: Annotated[str, Field(default=None, description="Specify the password that would need to be used, when working with archive files.")], document_password: Annotated[str, Field(default=None, description="Specify the password that would need to be used, when working with Adobe or Office files. Maximum: 32 characters.")], check_duplicate: Annotated[bool, Field(default=None, description="If enabled, the action checks if the file was already submitted previously and returns the available report. Note: during the validation \u201cNetwork Environment\u201d and \u201cSandbox Environment\u201d are not taken into consideration.")], comment: Annotated[str, Field(default=None, description="Specify the comment for the submission.")], confidential_submission: Annotated[bool, Field(default=None, description="If enabled, the file is only shown to users within your customer account.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Submit files to a sandbox in Crowdstrike. Note: This action requires a Falcon Sandbox license. For the list of supported file formats, refer to the documentation portal.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["File Paths"] = file_paths
            if sandbox_environment is not None:
                script_params["Sandbox Environment"] = sandbox_environment
            if network_environment is not None:
                script_params["Network Environment"] = network_environment
            if archive_password is not None:
                script_params["Archive Password"] = archive_password
            if document_password is not None:
                script_params["Document Password"] = document_password
            if check_duplicate is not None:
                script_params["Check Duplicate"] = check_duplicate
            if comment is not None:
                script_params["Comment"] = comment
            if confidential_submission is not None:
                script_params["Confidential Submission"] = confidential_submission
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Submit File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Submit File",
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
                print(f"Error executing action CrowdStrikeFalcon_Submit File for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_update_detection(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], detection_id: Annotated[str, Field(..., description="Specify the ID of the detection that needs to be updated.")], status: Annotated[List[str], Field(..., description="Specify the new status for the detection.")], assign_detection_to: Annotated[str, Field(default=None, description="Specify the email address of the Crowdstrike Falcon user, who needs to be assigned to this detection")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update detection in Crowdstrike Falcon.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Detection ID"] = detection_id
            script_params["Status"] = status
            if assign_detection_to is not None:
                script_params["Assign Detection to"] = assign_detection_to
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Update Detection",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Update Detection",
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
                print(f"Error executing action CrowdStrikeFalcon_Update Detection for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_list_host_vulnerabilities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], severity_filter: Annotated[str, Field(default=None, description="Specify the comma-separated list of severities for vulnerabilities.If nothing is provided, action will ingest all related vulnerabilities. Possible values: Critical, High, Medium, Low, Unknown.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight per entity containing statistical information about related vulnerabilities.")], max_vulnerabilities_to_return: Annotated[str, Field(default=None, description="Specify how many vulnerabilities to return per host. If nothing is provided action will process all of the related vulnerabilities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List vulnerabilities found on the host in Crowdstrike Falcon. Supported entities: IP Address and Hostname. Note: requires Falcon Spotlight license and permissions. 

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            if severity_filter is not None:
                script_params["Severity Filter"] = severity_filter
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if max_vulnerabilities_to_return is not None:
                script_params["Max Vulnerabilities To Return"] = max_vulnerabilities_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_List Host Vulnerabilities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_List Host Vulnerabilities",
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
                print(f"Error executing action CrowdStrikeFalcon_List Host Vulnerabilities for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def crowd_strike_falcon_lift_contained_endpoint(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], customer_id: Annotated[str, Field(default=None, description="Specify the ID of the customer for which you want to execute the action.")], fail_if_timeout: Annotated[bool, Field(default=None, description="If enabled, action will be failed, if containment was not lifted on all endpoints.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Lift endpoint containment in Crowdstrike Falcon. Supported entities: Hostname and IP address.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CrowdStrikeFalcon")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CrowdStrikeFalcon: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if customer_id is not None:
                script_params["Customer ID"] = customer_id
            if fail_if_timeout is not None:
                script_params["Fail If Timeout"] = fail_if_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CrowdStrikeFalcon_Lift Contained Endpoint",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CrowdStrikeFalcon_Lift Contained Endpoint",
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
                print(f"Error executing action CrowdStrikeFalcon_Lift Contained Endpoint for CrowdStrikeFalcon: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CrowdStrikeFalcon")
            return {"Status": "Failed", "Message": "No active instance found."}
