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
    # This function registers all tools (actions) for the Snowflake integration.

    @mcp.tool()
    async def snowflake_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Snowflake with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Snowflake")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Snowflake: {e}")
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
                actionName="Snowflake_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Snowflake_Ping",
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
                print(f"Error executing action Snowflake_Ping for Snowflake: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Snowflake")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def snowflake_execute_simple_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], database: Annotated[str, Field(..., description="Specify the name of the database in which you want to execute the query.")], table: Annotated[str, Field(..., description="Specify the name of the table in which you want to execute the query.")], schema: Annotated[str, Field(default=None, description="Specify the name of the schema in which you want to execute the query.")], where_filter: Annotated[str, Field(default=None, description="Specify the WHERE filter for the query  that needs to be executed. Note: you don't need to limit and sort. Also, you don\u2019t need to provide WHERE string in the payload. Only single quotes are supported in the query.")], fields_to_return: Annotated[str, Field(default=None, description="Specify what fields to return. If nothing is provided action will return all fields. Wildcard character is supported.")], sort_field: Annotated[str, Field(default=None, description="Specify what parameter should be used for sorting.")], sort_order: Annotated[List[str], Field(default=None, description="Specify the order of sorting.")], max_results_to_return: Annotated[str, Field(default=None, description="Specify how many results to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Execute a query based on parameters in Snowflake. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

Action Parameters: Database: Required. The name of the database to query., Table: Required. The name of the table to query., Schema: Optional. The name of the schema to query., Where Filter: Optional. The WHERE clause to filter the query results.Don't use the LIMIT or SORT keywords. Don't set the WHERE string in the payload.The query only supports single quotes., Fields To Return: Optional. A comma-separated list of fields to return.If you don't configure this parameter, the action returns all fields. The default value is *., Sort Field: Optional. The value to sort the results., Sort Order: Optional. The sorting order (ascending or descending). The possible values are as follows:ASC DESC The default value is ASC., Max Results To Return: Optional. The maximum number of results to return for every action run. The default value is 50.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Snowflake")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Snowflake: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Database"] = database
            script_params["Table"] = table
            if schema is not None:
                script_params["Schema"] = schema
            if where_filter is not None:
                script_params["Where Filter"] = where_filter
            if fields_to_return is not None:
                script_params["Fields To Return"] = fields_to_return
            if sort_field is not None:
                script_params["Sort Field"] = sort_field
            if sort_order is not None:
                script_params["Sort Order"] = sort_order
            if max_results_to_return is not None:
                script_params["Max Results To Return"] = max_results_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Snowflake_Execute Simple Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Snowflake_Execute Simple Query",
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
                print(f"Error executing action Snowflake_Execute Simple Query for Snowflake: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Snowflake")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def snowflake_execute_custom_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query that needs to be executed in Snowflake. Note: query shouldn't contain LIMIT keyword, because it\u2019s added automatically. Only single quotes are supported in the query.")], database: Annotated[str, Field(..., description="Specify the name of the database in which you want to execute the query.")], schema: Annotated[str, Field(default=None, description="Specify the name of the schema in which you want to execute the query.")], max_results_to_return: Annotated[str, Field(default=None, description="Specify how many results to return for the query. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Execute a custom query in Snowflake. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

Action Parameters: Query: Required. The SQL query to execute in Snowflake.The action automatically adds the LIMIT keyword to the query. Don't manually set the LIMIT keyword. The query only supports single quotes., Database: Required. The name of the Snowflake database to query., Schema: Optional. The name of the schema within the specified database to query., Max Results To Return: Optional. The maximum number of results to return from the query for every action run.The default value is 50.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Snowflake")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Snowflake: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            script_params["Database"] = database
            if schema is not None:
                script_params["Schema"] = schema
            if max_results_to_return is not None:
                script_params["Max Results To Return"] = max_results_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Snowflake_Execute Custom Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Snowflake_Execute Custom Query",
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
                print(f"Error executing action Snowflake_Execute Custom Query for Snowflake: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Snowflake")
            return {"Status": "Failed", "Message": "No active instance found."}
