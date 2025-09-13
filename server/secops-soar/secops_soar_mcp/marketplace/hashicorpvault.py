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
    # This function registers all tools (actions) for the HashiCorpVault integration.

    @mcp.tool()
    async def hashi_corp_vault_generate_aws_credentials(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], aws_role_name: Annotated[str, Field(..., description="Specify the role name to generate credentials for.")], aws_secret_engine_path: Annotated[str, Field(default=None, description="Specify the path used for the aws secret storage. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/aws/roles/")], aws_role_arn: Annotated[str, Field(default=None, description="Specify the ARN of the role to assume if credential_type on the Vault role is assumed_role. Must match one of the allowed role ARNs in the Vault role.")], aws_role_session_name: Annotated[str, Field(default=None, description="Specify the role session name to attach to the assumed role ARN. If not provided it will be generated dynamically by default.")], ttl_seconds: Annotated[str, Field(default=None, description="Specifies the TTL in seconds for the use of the STS token. This is specified as a string with a duration suffix. Valid only when AWS role credential_type in Vault is assumed_role or federation_token. When not specified, the default_sts_ttl set for the role will be used. If that is also not set, then the default value of 3600 seconds will be used.")], json_expression_builder: Annotated[Union[str, dict], Field(default=None, description="Specify a JSON Expression Builder expression to filter a specific subset of data from secret, for example:  | \u201cdata\u201d | \u201cdata\u201d | \u201ckey0\u201d")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Generate credentials based on AWS role stored in HashiCorp Vault. Note: This action doesn’t run on Chronicle SOAR entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="HashiCorpVault")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for HashiCorpVault: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if aws_secret_engine_path is not None:
                script_params["AWS Secret Engine Path"] = aws_secret_engine_path
            script_params["AWS Role Name"] = aws_role_name
            if aws_role_arn is not None:
                script_params["AWS Role ARN"] = aws_role_arn
            if aws_role_session_name is not None:
                script_params["AWS Role Session Name"] = aws_role_session_name
            if ttl_seconds is not None:
                script_params["TTL (seconds)"] = ttl_seconds
            if json_expression_builder is not None:
                script_params["JSON Expression Builder"] = json_expression_builder
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="HashiCorpVault_Generate AWS Credentials",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "HashiCorpVault_Generate AWS Credentials",
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
                print(f"Error executing action HashiCorpVault_Generate AWS Credentials for HashiCorpVault: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for HashiCorpVault")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def hashi_corp_vault_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the HashiCorp Vault installation with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="HashiCorpVault")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for HashiCorpVault: {e}")
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
                actionName="HashiCorpVault_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "HashiCorpVault_Ping",
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
                print(f"Error executing action HashiCorpVault_Ping for HashiCorpVault: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for HashiCorpVault")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def hashi_corp_vault_list_key_value_secret_keys(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], key_value_secret_engine_path: Annotated[str, Field(default=None, description="Specify the path used for the key-value secret storage. Currently only version 2 is supported. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/secret/data/<secret to fetch from kv store>")], secret_path: Annotated[str, Field(default=None, description="Specify secret path to fetch, action accept folder names, example secret path folder name is my-secret, key-value store path is secret, so full path to fetch would be \"https://x.x.x.x:8200/v1/secret/data/my-secret\". If not provided, action will return all secret keys stored in the secret engine.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return. If nothing is provided, action will return 50 records.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List secrets keys available in the HashiCorp Vault based on provided criteria. Action returns key names stored in secret path without values. Folder names should be specified for secret path, action does not work if secret key is provided. Note: This action doesn't run on Chronicle SOAR entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="HashiCorpVault")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for HashiCorpVault: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if key_value_secret_engine_path is not None:
                script_params["Key-Value Secret Engine Path"] = key_value_secret_engine_path
            if secret_path is not None:
                script_params["Secret Path"] = secret_path
            if max_records_to_return is not None:
                script_params["Max Records To Return"] = max_records_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="HashiCorpVault_List Key-Value Secret Keys",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "HashiCorpVault_List Key-Value Secret Keys",
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
                print(f"Error executing action HashiCorpVault_List Key-Value Secret Keys for HashiCorpVault: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for HashiCorpVault")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def hashi_corp_vault_list_aws_roles(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], aws_secret_engine_path: Annotated[str, Field(default=None, description="Specify the path used for the aws secret storage. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/aws/roles/")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return. If nothing is provided, action will return 50 records.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List AWS roles available in the HashiCorp Vault based on provided criteria. Note: This action doesn’t run on Chronicle SOAR entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="HashiCorpVault")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for HashiCorpVault: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if aws_secret_engine_path is not None:
                script_params["AWS Secret Engine Path"] = aws_secret_engine_path
            if max_records_to_return is not None:
                script_params["Max Records To Return"] = max_records_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="HashiCorpVault_List AWS Roles",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "HashiCorpVault_List AWS Roles",
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
                print(f"Error executing action HashiCorpVault_List AWS Roles for HashiCorpVault: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for HashiCorpVault")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def hashi_corp_vault_read_key_value_secret(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], secret_path: Annotated[str, Field(..., description="Specify secret path to fetch, example secret path is my-secret, key-value store path is secret, so full path to fetch would be \"https://x.x.x.x:8200/v1/secret/data/my-secret\".")], key_value_secret_engine_path: Annotated[str, Field(default=None, description="Specify the path used for the key-value secret storage. Currently only version 2 is supported. Parameter is used to interact with secrets stored in storage, it is used to construct the urls like https://x.x.x.x:8200/v1/secret/data/<secret to fetch from kv store>")], secret_version: Annotated[str, Field(default=None, description="Specify a secret version to fetch.")], json_expression_builder: Annotated[Union[str, dict], Field(default=None, description="Specify a JSON Expression Builder expression to filter a specific subset of data from secret, for example: data | data | key0")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Read Key-Value secret stored in HashiCorp Vault based on provided criteria. Note: This action doesn't run on Chronicle SOAR entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="HashiCorpVault")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for HashiCorpVault: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if key_value_secret_engine_path is not None:
                script_params["Key-Value Secret Engine Path"] = key_value_secret_engine_path
            script_params["Secret Path"] = secret_path
            if secret_version is not None:
                script_params["Secret Version"] = secret_version
            if json_expression_builder is not None:
                script_params["JSON Expression Builder"] = json_expression_builder
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="HashiCorpVault_Read Key-Value Secret",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "HashiCorpVault_Read Key-Value Secret",
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
                print(f"Error executing action HashiCorpVault_Read Key-Value Secret for HashiCorpVault: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for HashiCorpVault")
            return {"Status": "Failed", "Message": "No active instance found."}
