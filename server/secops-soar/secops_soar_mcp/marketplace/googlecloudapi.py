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
    # This function registers all tools (actions) for the GoogleCloudApi integration.

    @mcp.tool()
    async def google_cloud_api_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudApi")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudApi: {e}")
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
                actionName="GoogleCloudApi_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudApi_Ping",
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
                print(f"Error executing action GoogleCloudApi_Ping for GoogleCloudApi: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudApi")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_api_execute_http_request(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], method: Annotated[List[str], Field(..., description="Specify the method for the request.")], url_path: Annotated[str, Field(..., description="Specify the URL that needs to be executed.")], fields_to_return: Annotated[str, Field(..., description="Specify what fields to return. Possible values: response_data, redirects, response_code,response_cookies,response_headers,apparent_encoding")], request_timeout: Annotated[str, Field(..., description="How long to wait for the server to send data before giving up")], url_params: Annotated[str, Field(default=None, description="Specify the parameters for the URL. Any value provided in this parameter will be used alongside the values that are directly provided in the URL path parameters.")], headers: Annotated[str, Field(default=None, description="Specify headers for the HTTP request.")], cookie: Annotated[str, Field(default=None, description="Specify the parameters that should be constructed into the \"Cookie\" header. This parameter will overwrite the cookie provided in the \"Headers\" parameter.")], body_payload: Annotated[str, Field(default=None, description="Specify body for the HTTP request.")], expected_response_values: Annotated[str, Field(default=None, description="Specify the expected response values. If this parameter is not empty, then action will work in ASYNC mode and action will execute until the expected values will be seen or until timeout.")], follow_redirects: Annotated[bool, Field(default=None, description="If enabled, action will follow the redirects.")], fail_on_4xx_5xx: Annotated[bool, Field(default=None, description="If enabled, action will fail, if the status code of the response is 4xx or 5xx.")], base64_output: Annotated[bool, Field(default=None, description="If enabled, action will convert the response to base64. This is useful when downloading files. Note: JSON result can't be bigger than 15 mb.")], save_to_case_wall: Annotated[bool, Field(default=None, description="If enabled, action will save the file and attach it to the case wall. Note: the file will be archived with \".zip\" extension. This zip will not be password protected.")], password_protect_zip: Annotated[bool, Field(default=None, description="If enabled, action will add an \"infected\" password to the zip created with \"Save To Case Wall\" parameter. Use this, when you are dealing with suspicious files.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute HTTP request.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudApi")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudApi: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Method"] = method
            script_params["URL Path"] = url_path
            if url_params is not None:
                script_params["URL Params"] = url_params
            if headers is not None:
                script_params["Headers"] = headers
            if cookie is not None:
                script_params["Cookie"] = cookie
            if body_payload is not None:
                script_params["Body Payload"] = body_payload
            if expected_response_values is not None:
                script_params["Expected Response Values"] = expected_response_values
            if follow_redirects is not None:
                script_params["Follow Redirects"] = follow_redirects
            if fail_on_4xx_5xx is not None:
                script_params["Fail on 4xx/5xx"] = fail_on_4xx_5xx
            if base64_output is not None:
                script_params["Base64 Output"] = base64_output
            script_params["Fields To Return"] = fields_to_return
            script_params["Request Timeout"] = request_timeout
            if save_to_case_wall is not None:
                script_params["Save To Case Wall"] = save_to_case_wall
            if password_protect_zip is not None:
                script_params["Password Protect Zip"] = password_protect_zip
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudApi_Execute HTTP Request",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudApi_Execute HTTP Request",
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
                print(f"Error executing action GoogleCloudApi_Execute HTTP Request for GoogleCloudApi: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudApi")
            return {"Status": "Failed", "Message": "No active instance found."}
