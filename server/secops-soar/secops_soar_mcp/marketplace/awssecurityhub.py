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
    # This function registers all tools (actions) for the AWSSecurityHub integration.

    @mcp.tool()
    async def aws_security_hub_get_insight_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], insight_arn: Annotated[str, Field(..., description="Specify the ARN of the insight.")], max_results_to_return: Annotated[str, Field(default=None, description="Specify how many results to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Return detailed information about an insight in AWS Security Hub.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSSecurityHub")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSSecurityHub: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Insight ARN"] = insight_arn
            if max_results_to_return is not None:
                script_params["Max Results to Return"] = max_results_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSSecurityHub_Get Insight Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSSecurityHub_Get Insight Details",
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
                print(f"Error executing action AWSSecurityHub_Get Insight Details for AWSSecurityHub: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSSecurityHub")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def aws_security_hub_create_insight(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], insight_name: Annotated[str, Field(..., description="Specify the name of the insight.")], group_by_attribute: Annotated[List[str], Field(..., description="Specify the name of the attribute by which findings should be grouped under one insight.")], filter_json_object: Annotated[Union[str, dict], Field(..., description="Specify a filter for the findings. Filter is represented as a JSON object, where you can specify different attributes and values. Please refer to action documentation for more details.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an insight in AWS Security Hub.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSSecurityHub")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSSecurityHub: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Insight Name"] = insight_name
            script_params["Group By Attribute"] = group_by_attribute
            script_params["Filter JSON Object"] = filter_json_object
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSSecurityHub_Create Insight",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSSecurityHub_Create Insight",
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
                print(f"Error executing action AWSSecurityHub_Create Insight for AWSSecurityHub: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSSecurityHub")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def aws_security_hub_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to AWS Security Hub with parameters provided at the integration configuration page on Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSSecurityHub")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSSecurityHub: {e}")
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
                actionName="AWSSecurityHub_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSSecurityHub_Ping",
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
                print(f"Error executing action AWSSecurityHub_Ping for AWSSecurityHub: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSSecurityHub")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def aws_security_hub_update_finding(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], id: Annotated[str, Field(..., description="Specify ID of the finding that you want to update.")], product_arn: Annotated[str, Field(..., description="Specify the product ARN of the finding that you want to update.")], note: Annotated[str, Field(default=None, description="Specify new text for the note on the finding. Note: If the \u201cNote\u201d parameter has a value, you should also fill out the \u201cNote Author\u201d parameter. This is an AWS Security Hub limitation.")], note_author: Annotated[str, Field(default=None, description="Specify the author of the note. Note: If the \u201cNote Author\u201d parameter has a value, you should also fill out the \u201cNote\u201d parameter. This is an AWS Security Hub limitation.")], severity: Annotated[List[str], Field(default=None, description="Specify new severity for the finding.")], verification_state: Annotated[List[str], Field(default=None, description="Specify a new verification state for the finding.")], confidence: Annotated[str, Field(default=None, description="Specify new confidence for the finding.")], criticality: Annotated[str, Field(default=None, description="Specify new criticality for the finding.")], types: Annotated[str, Field(default=None, description="Specify a comma-separated list of types for the finding. Example: type1,type2")], workflow_status: Annotated[List[str], Field(default=None, description="Specify new workflow status for the finding.")], custom_fields: Annotated[str, Field(default=None, description="Specify custom fields that should be updated in the finding. Format Custom_field_1:value,Custom_field_2:value")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update findings in AWS Security Hub.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSSecurityHub")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSSecurityHub: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["ID"] = id
            script_params["Product ARN"] = product_arn
            if note is not None:
                script_params["Note"] = note
            if note_author is not None:
                script_params["Note Author"] = note_author
            if severity is not None:
                script_params["Severity"] = severity
            if verification_state is not None:
                script_params["Verification State"] = verification_state
            if confidence is not None:
                script_params["Confidence"] = confidence
            if criticality is not None:
                script_params["Criticality"] = criticality
            if types is not None:
                script_params["Types"] = types
            if workflow_status is not None:
                script_params["Workflow Status"] = workflow_status
            if custom_fields is not None:
                script_params["Custom Fields"] = custom_fields
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSSecurityHub_Update Finding",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSSecurityHub_Update Finding",
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
                print(f"Error executing action AWSSecurityHub_Update Finding for AWSSecurityHub: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSSecurityHub")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def aws_security_hub_update_insight(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], insight_arn: Annotated[str, Field(..., description="Specify the ARN of the insight.")], insight_name: Annotated[str, Field(default=None, description="Specify the new name of the insight.")], group_by_attribute: Annotated[List[str], Field(default=None, description="Specify a new name of the attribute by which findings should be grouped under one insight.")], filter_json_object: Annotated[Union[str, dict], Field(default=None, description="Specify a new filter for the findings. Filter is represented as a JSON object, where you can specify different attributes and values. Please refer to action documentation for more details.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update an insight in AWS Security Hub.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSSecurityHub")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSSecurityHub: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Insight ARN"] = insight_arn
            if insight_name is not None:
                script_params["Insight Name"] = insight_name
            if group_by_attribute is not None:
                script_params["Group By Attribute"] = group_by_attribute
            if filter_json_object is not None:
                script_params["Filter JSON Object"] = filter_json_object
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSSecurityHub_Update Insight",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSSecurityHub_Update Insight",
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
                print(f"Error executing action AWSSecurityHub_Update Insight for AWSSecurityHub: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSSecurityHub")
            return {"Status": "Failed", "Message": "No active instance found."}
