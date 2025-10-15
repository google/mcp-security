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
    # This function registers all tools (actions) for the CSV integration.

    @mcp.tool()
    async def csv_csv_search_by_entity(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], csv_path: Annotated[str, Field(..., description="Specify the file path to the CSV file or a folder path that contains all of the CSV files. If folder is provide, action will iterate over all CSV files in the folder.")], file_encoding_types: Annotated[str, Field(..., description="A comma separated list CSV encoding types used for decoding your CSV files, e.g. utf-8, latin-1, iso-8859-1, utf-16... Order in which the encoding types are given sets the order in which they are used for decoding files, e.g.(from example above) the utf-8 has the highest priority and will be used primarily for decoding all the files, if there is a CSV file that uses some other encoding then the next in the order: latin-1 encoding will be used, and so on, until the last encoding is used.")], csv_column: Annotated[str, Field(default=None, description="Specify a comma-separated list of columns that can contain entity information. If nothing is provided, action will search in all of the columns.")], days_back: Annotated[str, Field(default=None, description="Specify how many days backwards to process the CSV files.")], mark_as_suspicious: Annotated[bool, Field(default=None, description="If enabled, action will mark entity as suspicious, if it was found in file.")], return_the_first_row_only: Annotated[bool, Field(default=None, description="If enabled, action will only return 1 row in the first file that matched the entity.")], enrich_entities: Annotated[bool, Field(default=None, description="If enabled, action will add information from CSV file and add it to the enrichment table of entity.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight, if entity was found in the file.")], fields_to_return: Annotated[str, Field(default=None, description="Specify a comma-separated list of values that need to be returned.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search for entities in CSV files and enrich them.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CSV")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CSV: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["CSV Path"] = csv_path
            if csv_column is not None:
                script_params["CSV Column"] = csv_column
            if days_back is not None:
                script_params["Days Back"] = days_back
            if mark_as_suspicious is not None:
                script_params["Mark As Suspicious"] = mark_as_suspicious
            if return_the_first_row_only is not None:
                script_params["Return the first row only"] = return_the_first_row_only
            script_params["File Encoding Types"] = file_encoding_types
            if enrich_entities is not None:
                script_params["Enrich Entities"] = enrich_entities
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if fields_to_return is not None:
                script_params["Fields To Return"] = fields_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CSV_CSV Search by Entity",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CSV_CSV Search by Entity",
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
                print(f"Error executing action CSV_CSV Search by Entity for CSV: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CSV")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def csv_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CSV")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CSV: {e}")
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
                actionName="CSV_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CSV_Ping",
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
                print(f"Error executing action CSV_Ping for CSV: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CSV")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def csv_save_json_to_csv(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], json_object: Annotated[Union[str, dict], Field(..., description="Specify the JSON object that needs to be saved as CSV.")], file_path: Annotated[str, Field(..., description="Specify the absolute file path for the newly created CSV file. If only the file name is provided, action will store the file in /tmp/ folder.")], overwrite: Annotated[bool, Field(default=None, description="If enabled, action will overwrite existing file.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Save JSON object  to CSV.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CSV")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CSV: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["JSON Object"] = json_object
            if overwrite is not None:
                script_params["Overwrite"] = overwrite
            script_params["File Path"] = file_path
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CSV_Save Json To CSV",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CSV_Save Json To CSV",
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
                print(f"Error executing action CSV_Save Json To CSV for CSV: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CSV")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def csv_csv_search_by_string(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], csv_path: Annotated[str, Field(..., description="Specify the file path to the CSV file or a folder path that contains all of the CSV files. If folder is provide, action will iterate over all CSV files in the folder.")], search_value: Annotated[str, Field(..., description="Specify a string that needs to be searched. If 'Search Multiple Strings' is enabled, this parameter is treated as a comma-separated list of strings that need to be searched.")], file_encoding_types: Annotated[str, Field(..., description="A comma separated list CSV encoding types used for decoding your CSV files, e.g. utf-8, latin-1, iso-8859-1, utf-16... Order in which the encoding types are given sets the order in which they are used for decoding files, e.g.(from example above) the utf-8 has the highest priority and will be used primarily for decoding all the files, if there is a CSV file that uses some other encoding then the next in the order: latin-1 encoding will be used, and so on, until the last encoding is used.")], csv_column: Annotated[str, Field(default=None, description="Specify a comma-separated list of columns that can contain entity information. If nothing is provided, action will search in all of the columns.")], days_back: Annotated[str, Field(default=None, description="Specify how many days backwards to process the CSV files.")], return_the_first_row_only: Annotated[bool, Field(default=None, description="If enabled, action will only return 1 row in the first file that matched the entity.")], fields_to_return: Annotated[str, Field(default=None, description="Specify a comma-separated list of values that need to be returned.")], search_multiple_strings: Annotated[bool, Field(default=None, description="If enabled, 'Search Value' will work as a comma-separated list of values, instead of a single string.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search for strings in CSV files.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CSV")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for CSV: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["CSV Path"] = csv_path
            if csv_column is not None:
                script_params["CSV Column"] = csv_column
            if days_back is not None:
                script_params["Days Back"] = days_back
            script_params["Search Value"] = search_value
            if return_the_first_row_only is not None:
                script_params["Return the first row only"] = return_the_first_row_only
            script_params["File Encoding Types"] = file_encoding_types
            if fields_to_return is not None:
                script_params["Fields To Return"] = fields_to_return
            if search_multiple_strings is not None:
                script_params["Search Multiple Strings"] = search_multiple_strings
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="CSV_CSV Search by String",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "CSV_CSV Search by String",
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
                print(f"Error executing action CSV_CSV Search by String for CSV: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for CSV")
            return {"Status": "Failed", "Message": "No active instance found."}
