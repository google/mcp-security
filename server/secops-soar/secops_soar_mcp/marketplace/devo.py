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
    # This function registers all tools (actions) for the Devo integration.

    @mcp.tool()
    async def devo_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Devo instance with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Devo")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Devo: {e}")
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
                actionName="Devo_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Devo_Ping",
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
                print(f"Error executing action Devo_Ping for Devo: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Devo")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def devo_advanced_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify a query to execute against Devo instance. Example format: 'from siem.logtrust.alert.info'.")], time_frame: Annotated[List[str], Field(default=None, description="Specify a time frame for the results. If 'Custom' is selected, you also need to provide 'Start Time'.")], start_time: Annotated[str, Field(default=None, description="Specify a time frame for the results. If 'Custom' is selected, you also need to provide 'Start Time'.")], end_time: Annotated[str, Field(default=None, description="Specify the start time for the query. This parameter is mandatory, if 'Custom' is selected for the 'Time Frame' parameter. Format: ISO 8601. Example: 2021-08-05T05:18:42Z")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify max number of rows the action should return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Execute an advanced query based on the provided parameters. Note that action is not working on Siemplify entities. If its planned to query table other than siem.logtrust.alert.info, please create an additional token for that table following the documentation at https://docs.devo.com/confluence/ndt/latest/domain-administration/security-credentials/authentication-tokens and specify it on the integration configuration page.

Action Parameters: Query: Specify a query to execute against Devo instance.Example: "from siem.logtrust.alert.info"., Time Frame: Specify a time frame for the results.If "Custom" is selected, you also need to provide the "Start Time" parameter., Start Time: Specify the start time for the query.This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter.Format: ISO 8601Example: 2021-08-05T05:18:42Z, End Time: Specify the end time for the query.If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter uses current time.Format: ISO 8601Example: 2021-08-05T05:18:42Z, Max Rows to Return: Specify the maximum number of rows the action should return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Devo")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Devo: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            if time_frame is not None:
                script_params["Time Frame"] = time_frame
            if start_time is not None:
                script_params["Start Time"] = start_time
            if end_time is not None:
                script_params["End Time"] = end_time
            if max_rows_to_return is not None:
                script_params["Max rows to return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Devo_Advanced Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Devo_Advanced Query",
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
                print(f"Error executing action Devo_Advanced Query for Devo: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Devo")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def devo_simple_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], table_name: Annotated[str, Field(..., description="Specify what table should be queried.")], fields_to_return: Annotated[str, Field(default=None, description="Specify what fields to return. If nothing is provided, action will return all fields.")], where_filter: Annotated[str, Field(default=None, description="Specify the WHERE filter for the query  that needs to be executed.")], time_frame: Annotated[List[str], Field(default=None, description="Specify a time frame for the results. If 'Custom' is selected, you also need to provide 'Start Time'.")], start_time: Annotated[str, Field(default=None, description="Specify a time frame for the results. If 'Custom' is selected, you also need to provide 'Start Time'.")], end_time: Annotated[str, Field(default=None, description="Specify the start time for the query. This parameter is mandatory, if 'Custom' is selected for the 'Time Frame' parameter. Format: ISO 8601. Example: 2021-08-05T05:18:42Z")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify max number of rows the action should return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Execute a simple query based on the provided parameters. Note that action is not working on Siemplify entities. If its planned to query table other than siem.logtrust.alert.info, please create an additional token for that table following the documentation at https://docs.devo.com/confluence/ndt/latest/domain-administration/security-credentials/authentication-tokens and specify it on the integration configuration page.

Action Parameters: Table Name: Specify the table that should be queried., Fields To Return: Specify the fields to return.If nothing is provided, the action returns all fields., Where Filter: Specify the Where filter for the query that needs to be executed., Time Frame: Specify a time frame for the results.If "Custom" is selected, you also need to provide the "Start Time" parameter., Start Time: Specify the start time for the query.This parameter is mandatory, if "Custom" is selected for the "Time Frame" parameter.Format: ISO 8601Example: 2021-08-05T05:18:42Z, End Time: Specify the end time for the query.If nothing is provided and "Custom" is selected for the "Time Frame" parameter then this parameter uses current time.Format: ISO 8601 Example: 2021-08-05T05:18:42Z, Max Rows to Return: Specify the maximum number of rows the action should return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Devo")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Devo: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Table Name"] = table_name
            if fields_to_return is not None:
                script_params["Fields To Return"] = fields_to_return
            if where_filter is not None:
                script_params["Where Filter"] = where_filter
            if time_frame is not None:
                script_params["Time Frame"] = time_frame
            if start_time is not None:
                script_params["Start Time"] = start_time
            if end_time is not None:
                script_params["End Time"] = end_time
            if max_rows_to_return is not None:
                script_params["Max rows to return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Devo_Simple Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Devo_Simple Query",
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
                print(f"Error executing action Devo_Simple Query for Devo: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Devo")
            return {"Status": "Failed", "Message": "No active instance found."}
