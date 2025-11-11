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
    # This function registers all tools (actions) for the TruSTAR integration.

    @mcp.tool()
    async def tru_star_get_related_io_cs(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_io_cs_to_return: Annotated[str, Field(default=None, description="Specify how many IOCs to return. Default: 50. Maximum: 1000.")], enclave_filter: Annotated[str, Field(default=None, description="Specify a comma-separated list of enclave names that should be used during the enrichment.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about IOCs that are related to the provided entities. Supported entities: All.

Action Parameters: Max IOCs To Return: Specify how many IOCs to return. Default: 50. Maximum: 1000., Enclave Filter: Specify a comma-separated list of enclave names that should be used during the enrichment.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TruSTAR")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for TruSTAR: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_io_cs_to_return is not None:
                script_params["Max IOCs To Return"] = max_io_cs_to_return
            if enclave_filter is not None:
                script_params["Enclave Filter"] = enclave_filter
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="TruSTAR_Get Related IOCs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "TruSTAR_Get Related IOCs",
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
                print(f"Error executing action TruSTAR_Get Related IOCs for TruSTAR: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for TruSTAR")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def tru_star_get_related_reports(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about reports related to the entities.")], include_report_body_in_insight: Annotated[bool, Field(default=None, description="If enabled, insight will contain information about the report body. Note: report body can be very big in size.")], enclave_filter: Annotated[str, Field(default=None, description="Specify a comma-separated list of enclave names that should be used during the enrichment.")], max_reports_to_return: Annotated[str, Field(default=None, description="Specify how many reports to return. Default: 10. Maximum: 25.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Get information about reports related to the entities. Supported entities: All.

Action Parameters: Create Insight: If enabled, action will create an insight containing information about reports related to the entities., Include Report Body In Insight: If enabled, insight will contain information about the report body. Note: report body can be very big in size., Enclave Filter: Specify a comma-separated list of enclave names that should be used during the enrichment., Max Reports To Return: Specify how many reports to return. Default: 10. Maximum: 25.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TruSTAR")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for TruSTAR: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if include_report_body_in_insight is not None:
                script_params["Include Report Body In Insight"] = include_report_body_in_insight
            if enclave_filter is not None:
                script_params["Enclave Filter"] = enclave_filter
            if max_reports_to_return is not None:
                script_params["Max Reports To Return"] = max_reports_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="TruSTAR_Get Related Reports",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "TruSTAR_Get Related Reports",
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
                print(f"Error executing action TruSTAR_Get Related Reports for TruSTAR: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for TruSTAR")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def tru_star_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the TruSTAR with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TruSTAR")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for TruSTAR: {e}")
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
                actionName="TruSTAR_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "TruSTAR_Ping",
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
                print(f"Error executing action TruSTAR_Ping for TruSTAR: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for TruSTAR")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def tru_star_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], security_level_threshold: Annotated[List[str], Field(..., description="Specify what should be the lowest security level for the entity to be marked as suspicious.")], enclave_filter: Annotated[str, Field(default=None, description="Specify a comma-separated list of enclave names that should be used during the enrichment.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich entities using information from TruSTAR. Supported entities: All.

Action Parameters: Security Level Threshold: Specify what should be the lowest security level for the entity to be marked as suspicious., Enclave Filter: Specify a comma-separated list of enclave names that should be used during the enrichment.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TruSTAR")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for TruSTAR: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Security Level Threshold"] = security_level_threshold
            if enclave_filter is not None:
                script_params["Enclave Filter"] = enclave_filter
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="TruSTAR_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "TruSTAR_Enrich Entities",
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
                print(f"Error executing action TruSTAR_Enrich Entities for TruSTAR: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for TruSTAR")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def tru_star_list_enclaves(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter.")], max_enclaves_to_return: Annotated[str, Field(default=None, description="Specify how many enclaves to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List available enclaves in TruSTAR.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TruSTAR")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for TruSTAR: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if filter_logic is not None:
                script_params["Filter Logic"] = filter_logic
            if filter_value is not None:
                script_params["Filter Value"] = filter_value
            if max_enclaves_to_return is not None:
                script_params["Max Enclaves To Return"] = max_enclaves_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="TruSTAR_List Enclaves",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "TruSTAR_List Enclaves",
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
                print(f"Error executing action TruSTAR_List Enclaves for TruSTAR: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for TruSTAR")
            return {"Status": "Failed", "Message": "No active instance found."}
