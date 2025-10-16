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
    # This function registers all tools (actions) for the VertexAI integration.

    @mcp.tool()
    async def vertex_ai_execute_prompt(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], text_prompt: Annotated[str, Field(..., description="The text instructions to include in the prompt.")], model_id: Annotated[str, Field(default=None, description="The ID of the model to use, such as gemini-1.5-flash-002.")], temperature: Annotated[str, Field(default=None, description="The value to control the degree of randomness in a token selection. This parameter accepts float data type values. For more information about temperature values, see \"Experiment with the parameter values\" (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#temperature).")], candidate_count: Annotated[str, Field(default=None, description="The number of response variations to return in every action run. For every request, the billing applies to an input token once and every output token of all generated candidates.")], response_mime_type: Annotated[List[str], Field(default=None, description="The media (MIME) type of the output response for the generated candidate text. The response media (MIME) type is available for the following models: gemini-1.5-pro, gemini-1.5-flash.")], response_schema: Annotated[str, Field(default=None, description="The schema for the generated candidate text to follow. To use this parameter, configure the \"Response mIME Type\" parameter. The response schema is available for the following models: gemini-1.5-pro, gemini-1.5-flash.")], max_input_tokens: Annotated[str, Field(default=None, description="The maximum number of input tokens to submit. One token consists of up to four characters. 100 tokens can correspond to 60-80 words. If you don\u2019t set a value, the action executes any prompt. If the number of tokens exceeds the configured maximum number, the action fails.")], max_output_tokens: Annotated[str, Field(default=None, description="The maximum number of output tokens to generate in every response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words. For more information, see \"Experiment with parameter values\" (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#max-output-tokens).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Execute Prompt action to execute individual text prompts using Vertex AI.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VertexAI")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VertexAI: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if model_id is not None:
                script_params["Model ID"] = model_id
            script_params["Text Prompt"] = text_prompt
            if temperature is not None:
                script_params["Temperature"] = temperature
            if candidate_count is not None:
                script_params["Candidate Count"] = candidate_count
            if response_mime_type is not None:
                script_params["Response MIME type"] = response_mime_type
            if response_schema is not None:
                script_params["Response Schema"] = response_schema
            if max_input_tokens is not None:
                script_params["Max Input Tokens"] = max_input_tokens
            if max_output_tokens is not None:
                script_params["Max Output Tokens"] = max_output_tokens
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VertexAI_Execute Prompt",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VertexAI_Execute Prompt",
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
                print(f"Error executing action VertexAI_Execute Prompt for VertexAI: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VertexAI")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def vertex_ai_describe_entity(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], refresh_after_days: Annotated[str, Field(..., description="The number of days for the action to wait before refreshing the entity summary. The action generates a hash value that is based on all inputs that are sent to Vertex AI excluding values from the \"Fields To Ignore\" parameter. If the hash value changed, the action refreshes the summary after the set number of days. If the hash value didn\u2019t change, the action doesn\u2019t refresh the summary even if the \"Refresh After (Days)\" parameter value is earlier than the latest summary generation time. The action validates the hash value of the latest actual generated summary and ignores the cached hash value.")], model_id: Annotated[str, Field(default=None, description="The ID of the model to use, such as gemini-1.5-flash-002.")], temperature: Annotated[str, Field(default=None, description="The value to control the degree of randomness in a token selection. This parameter accepts float data type values. For more information about temperature values, see \"Experiment with the parameter values\" (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#temperature).")], exclude_fields: Annotated[str, Field(default=None, description="A comma-separated list of the Google SecOps entity metadata fields to exclude during the entity summary generation.")], force_refresh: Annotated[bool, Field(default=None, description="If selected, the action ignores the \"Refresh After (Days)\" parameter and hash validation and regenerates the entity summary for every action run.")], max_output_tokens: Annotated[str, Field(default=None, description="The maximum number of output tokens to generate in every response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words. This limit applies to every individual entity. For more information, see \"Experiment with parameter values\" (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#max-output-tokens).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Preview. Use the Describe Entity action to summarize information about entities using Vertex AI. This action works with all entity types. and submits every entity individually.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VertexAI")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VertexAI: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if model_id is not None:
                script_params["Model ID"] = model_id
            if temperature is not None:
                script_params["Temperature"] = temperature
            if exclude_fields is not None:
                script_params["Exclude Fields"] = exclude_fields
            if force_refresh is not None:
                script_params["Force Refresh"] = force_refresh
            script_params["Refresh After (Days)"] = refresh_after_days
            if max_output_tokens is not None:
                script_params["Max Output Tokens"] = max_output_tokens
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VertexAI_Describe Entity",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VertexAI_Describe Entity",
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
                print(f"Error executing action VertexAI_Describe Entity for VertexAI: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VertexAI")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def vertex_ai_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Use the Ping action to test the connectivity to Vertex AI.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VertexAI")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VertexAI: {e}")
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
                actionName="VertexAI_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VertexAI_Ping",
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
                print(f"Error executing action VertexAI_Ping for VertexAI: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VertexAI")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def vertex_ai_analyze_eml(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], files_to_analyze: Annotated[str, Field(..., description="Comma-separated list of EML files to submit for analysis.")], model_id: Annotated[str, Field(default=None, description="The ID of the model to use, such as gemini-1.5-flash-002.")], temperature: Annotated[str, Field(default=None, description="The value to control the degree of randomness in a token selection. This parameter accepts float data type values. For more information about temperature values, see \u201cExperiment with the parameter values\u201d (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#temperature).")], max_output_tokens: Annotated[str, Field(default=None, description="The maximum number of output tokens to generate in every response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words. This limit applies to every individual entry. For more information, see \u201cExperiment with parameter values\u201d (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#max-output-tokens).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Preview. Use the Analyze EML action to analyze EML files using Vertex AI. The action submits every file individually.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VertexAI")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VertexAI: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if model_id is not None:
                script_params["Model ID"] = model_id
            if temperature is not None:
                script_params["Temperature"] = temperature
            script_params["Files To Analyze"] = files_to_analyze
            if max_output_tokens is not None:
                script_params["Max Output Tokens"] = max_output_tokens
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VertexAI_Analyze EML",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VertexAI_Analyze EML",
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
                print(f"Error executing action VertexAI_Analyze EML for VertexAI: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VertexAI")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def vertex_ai_transform_data(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], text_prompt: Annotated[str, Field(..., description="The text instructions to include in the prompt.")], json_object: Annotated[Union[str, dict], Field(..., description="The JSON object to use as an action input.")], max_output_tokens: Annotated[str, Field(..., description="The maximum number of output tokens to generate in every response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words. For more information, see \u201cExperiment with parameter values\u201d (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#max-output-tokens).")], model_id: Annotated[str, Field(default=None, description="The ID of the model to use, such as gemini-1.5-flash-002.")], temperature: Annotated[str, Field(default=None, description="The value to control the degree of randomness in a token selection. This parameter accepts float data type values. For more information about temperature values, see \u201cExperiment with the parameter values\u201d (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values#temperature).")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Preview. Use the Transform Data action to perform data transformations using Vertex AI.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VertexAI")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VertexAI: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if model_id is not None:
                script_params["Model ID"] = model_id
            script_params["Text Prompt"] = text_prompt
            if temperature is not None:
                script_params["Temperature"] = temperature
            script_params["JSON Object"] = json_object
            script_params["Max Output Tokens"] = max_output_tokens
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VertexAI_Transform Data",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VertexAI_Transform Data",
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
                print(f"Error executing action VertexAI_Transform Data for VertexAI: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VertexAI")
            return {"Status": "Failed", "Message": "No active instance found."}
