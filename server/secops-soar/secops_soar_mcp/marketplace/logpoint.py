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
    # This function registers all tools (actions) for the LogPoint integration.

    @mcp.tool()
    async def log_point_list_repos(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], max_repos_to_return: Annotated[str, Field(default=None, description="Specify how many reports should be returned.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
List available repos in Logpoint.

Action Parameters: Max Repos To Return: Specify how many reports should be returned.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="LogPoint")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for LogPoint: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if max_repos_to_return is not None:
                script_params["Max Repos To Return"] = max_repos_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="LogPoint_List Repos",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "LogPoint_List Repos",
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
                print(f"Error executing action LogPoint_List Repos for LogPoint: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for LogPoint")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def log_point_execute_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query that needs to be executed in Logpoint.")], time_frame: Annotated[List[str], Field(..., description="Specify the time frame for the query. If \u201cCustom\u201d is selected, you need to also provide start time and end time.")], start_time: Annotated[str, Field(default=None, description="Specify the start time for the query. Format: YYYY-MM-DDThh:mm:ssZ or timestamp.")], end_time: Annotated[str, Field(default=None, description="Specify the end time for the query.Format: YYYY-MM-DDThh:mm:ssZ or timestamp. If nothing is provided action will use current time as end time.")], repos: Annotated[str, Field(default=None, description="Specify a comma-separated list of names of the repos. If nothing is provided, action will search in all repos.")], max_results_to_return: Annotated[str, Field(default=None, description="Specify how many results should be returned.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Execute search query in Logpoint.

Action Parameters: Query: Specify the query that needs to be executed in Logpoint., Time Frame: Specify the time frame for the query. If "Custom" is selected, you need to also provide start time and end time., Start Time: Specify the start time for the query. Format:YYYY-MM-DDThh:mm:ssZ or timestamp., End Time: Specify the end time for the query.Format:YYYY-MM-DDThh:mm:ssZ or timestamp. If nothing is provided action will use current time as end time., Repos: Specify a comma-separated list of names of the repos. If nothing is provided, action will search in all repos., Max Results To Return: Specify how many results should be returned.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="LogPoint")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for LogPoint: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            script_params["Time Frame"] = time_frame
            if start_time is not None:
                script_params["Start Time"] = start_time
            if end_time is not None:
                script_params["End Time"] = end_time
            if repos is not None:
                script_params["Repos"] = repos
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
                actionName="LogPoint_Execute Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "LogPoint_Execute Query",
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
                print(f"Error executing action LogPoint_Execute Query for LogPoint: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for LogPoint")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def log_point_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Logpoint with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="LogPoint")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for LogPoint: {e}")
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
                actionName="LogPoint_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "LogPoint_Ping",
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
                print(f"Error executing action LogPoint_Ping for LogPoint: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for LogPoint")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def log_point_update_incident_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the id of the incident, which you want to update.")], action: Annotated[List[str], Field(..., description="Specify the action for the incident.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Update incident status in Logpoint.

Action Parameters: Incident ID: Specify the id of the incident, which you want to update., Action: Specify the action for the incident.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="LogPoint")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for LogPoint: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident ID"] = incident_id
            script_params["Action"] = action
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="LogPoint_Update Incident Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "LogPoint_Update Incident Status",
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
                print(f"Error executing action LogPoint_Update Incident Status for LogPoint: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for LogPoint")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def log_point_execute_entity_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query that needs to be executed. Please refer to the action documentation for details.")], time_frame: Annotated[List[str], Field(..., description="Specify the time frame for the query. If \"Custom\" is selected, you need also provide start time, end time by default will be current time.")], stop_if_not_enough_entities: Annotated[bool, Field(..., description="If enabled, action will not start execution, unless all of the entity types are available for the specified \".. Entity Keys\". Example: if \"IP Entity Key\" and \"File Hash Entity Keys\" are specified, but in the scope there are no file hashes then if this parameter is enabled, action will not execute the query.")], cross_entity_operator: Annotated[List[str], Field(..., description="Specify what should be the logical operator used between different entity types.")], start_time: Annotated[str, Field(default=None, description="Specify the start time for the query. Format: YYYY-MM-DDThh:mm:ssZ or timestamp.")], end_time: Annotated[str, Field(default=None, description="Specify the end time for the query. Format: YYYY-MM-DDThh:mm:ssZ or timestamp. If nothing is provided action will use current time as end time.")], repos: Annotated[str, Field(default=None, description="Specify a comma-separated list of names of the repos. If nothing is provided, action will search in all repos.")], ip_entity_key: Annotated[str, Field(default=None, description="Specify what key should be used with IP entities. Please refer to the action documentation for details.")], hostname_entity_key: Annotated[str, Field(default=None, description="Specify what key should be used with Hostname entities, when preparing the filter. Please refer to the action documentation for details.")], file_hash_entity_key: Annotated[str, Field(default=None, description="Specify what key should be used with File Hash entities. Please refer to the action documentation for details.")], user_entity_key: Annotated[str, Field(default=None, description="Specify what key should be used with User entities. Please refer to the action documentation for details.")], url_entity_key: Annotated[str, Field(default=None, description="Specify what key should be used with URL entities. Please refer to the action documentation for details.")], email_address_entity_key: Annotated[str, Field(default=None, description="Specify what key should be used with Email Address entities. Please refer to the action documentation for details.")], max_results_to_return: Annotated[str, Field(default=None, description="Specify how many results should be returned.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Execute query in Logpoint based on entities. Currently supported entity types: User, IP, Email Address, URL, File Hash, Hostname. Note: Email Address is a User entity that matches the format of email address.

Action Parameters: Query: Specify the query that needs to be executed. Please refer to the action documentation for details., Time Frame: Specify the time frame for the query. If "Custom" is selected, you need to also provide start time, end time by default will use current time., Start Time: Specify the start time for the query. Format:YYYY-MM-DDThh:mm:ssZ or timestamp., End Time: Specify the end time for the query.Format:YYYY-MM-DDThh:mm:ssZ or timestamp. If nothing is provided action will use current time as end time., Repos: Specify a comma-separated list of names of the repos. If nothing is provided, action will search in all repos., IP Entity Key: Specify what key should be used with IP entities. Please refer to the action documentation for details., Hostname Entity Key: Specify what key should be used with Hostname entities, when preparing the . Please refer to the action documentation for details., File Hash Entity Key: Specify what key should be used with File Hash entities. Please refer to the action documentation for details., User Entity Key: Specify what key should be used with User entities. Please refer to the action documentation for details., URL Entity Key: Specify what key should be used with URL entities. Please refer to the action documentation for details., Email Address Entity Key: Specify what key should be used with Email Address entities. Please refer to the action documentation for details., Stop If Not Enough Entities: If enabled, action will not start execution, unless all of the entity types are available for the specified ".. Entity Keys". Example: if "IP Entity Key" and "File Hash Entity Key" are specified, but in the scope there are no file hashes then if this parameter is enabled, action will not execute the query., Cross Entity Operator: Specify what should be the logical operator used between different entity types., Max Results To Return: Specify how many results should be returned.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="LogPoint")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for LogPoint: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            script_params["Time Frame"] = time_frame
            if start_time is not None:
                script_params["Start Time"] = start_time
            if end_time is not None:
                script_params["End Time"] = end_time
            if repos is not None:
                script_params["Repos"] = repos
            if ip_entity_key is not None:
                script_params["IP Entity Key"] = ip_entity_key
            if hostname_entity_key is not None:
                script_params["Hostname Entity Key"] = hostname_entity_key
            if file_hash_entity_key is not None:
                script_params["File Hash Entity Key"] = file_hash_entity_key
            if user_entity_key is not None:
                script_params["User Entity Key"] = user_entity_key
            if url_entity_key is not None:
                script_params["URL Entity Key"] = url_entity_key
            if email_address_entity_key is not None:
                script_params["Email Address Entity Key"] = email_address_entity_key
            script_params["Stop if Not Enough Entities"] = stop_if_not_enough_entities
            script_params["Cross Entity Operator"] = cross_entity_operator
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
                actionName="LogPoint_Execute Entity Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "LogPoint_Execute Entity Query",
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
                print(f"Error executing action LogPoint_Execute Entity Query for LogPoint: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for LogPoint")
            return {"Status": "Failed", "Message": "No active instance found."}
