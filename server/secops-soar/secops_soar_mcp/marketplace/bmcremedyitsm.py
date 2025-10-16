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
    # This function registers all tools (actions) for the BMCRemedyITSM integration.

    @mcp.tool()
    async def bmc_remedy_itsm_update_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the id of the  incident that needs to be updated.")], status: Annotated[List[str], Field(default=None, description="Specify the status for the incident. Note: if status is \"Pending\" or \"Resolved\", then you also need to provide \"Status Reason\" value.")], status_reason: Annotated[str, Field(default=None, description="Specify the status reason for the incident.")], impact: Annotated[List[str], Field(default=None, description="Specify the impact for the incident.")], urgency: Annotated[List[str], Field(default=None, description="Specify the urgency for the incident.")], description: Annotated[str, Field(default=None, description="Specify the description of the incident")], incident_type: Annotated[List[str], Field(default=None, description="Specify the incident type for the incident.")], assigned_group: Annotated[str, Field(default=None, description="Specify the assigned group for the incident")], assignee: Annotated[str, Field(default=None, description="Specify the assignee for the incident")], resolution: Annotated[str, Field(default=None, description="Specify the resolution for the incident.")], resolution_category_tier_1: Annotated[str, Field(default=None, description="Specify the resolution category tier 1 for the incident.")], resolution_category_tier_2: Annotated[str, Field(default=None, description="Specify the resolution category tier 2 for the incident.")], resolution_category_tier_3: Annotated[str, Field(default=None, description="Specify the resolution category tier 3 for the incident.")], resolution_product_category_tier_1: Annotated[str, Field(default=None, description="Specify the resolution category tier 1 for the incident.")], resolution_product_category_tier_2: Annotated[str, Field(default=None, description="Specify the resolution category tier 2 for the incident.")], resolution_product_category_tier_3: Annotated[str, Field(default=None, description="Specify the resolution category tier 3 for the incident.")], reported_source: Annotated[List[str], Field(default=None, description="Specify the reported source.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object containing all of the needed fields and  values that need to be updated. Note: this parameter will overwrite other provided parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update an incident in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident ID"] = incident_id
            if status is not None:
                script_params["Status"] = status
            if status_reason is not None:
                script_params["Status Reason"] = status_reason
            if impact is not None:
                script_params["Impact"] = impact
            if urgency is not None:
                script_params["Urgency"] = urgency
            if description is not None:
                script_params["Description"] = description
            if incident_type is not None:
                script_params["Incident Type"] = incident_type
            if assigned_group is not None:
                script_params["Assigned Group"] = assigned_group
            if assignee is not None:
                script_params["Assignee"] = assignee
            if resolution is not None:
                script_params["Resolution"] = resolution
            if resolution_category_tier_1 is not None:
                script_params["Resolution Category Tier 1"] = resolution_category_tier_1
            if resolution_category_tier_2 is not None:
                script_params["Resolution Category Tier 2"] = resolution_category_tier_2
            if resolution_category_tier_3 is not None:
                script_params["Resolution Category Tier 3"] = resolution_category_tier_3
            if resolution_product_category_tier_1 is not None:
                script_params["Resolution Product Category Tier 1"] = resolution_product_category_tier_1
            if resolution_product_category_tier_2 is not None:
                script_params["Resolution Product Category Tier 2"] = resolution_product_category_tier_2
            if resolution_product_category_tier_3 is not None:
                script_params["Resolution Product Category Tier 3"] = resolution_product_category_tier_3
            if reported_source is not None:
                script_params["Reported Source"] = reported_source
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
                actionName="BMCRemedyITSM_Update Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Update Incident",
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
                print(f"Error executing action BMCRemedyITSM_Update Incident for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_update_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], record_type: Annotated[str, Field(..., description="Specify the type of the record that needs to be updated.")], record_id: Annotated[str, Field(..., description="Specify the id of the  record that needs to be updated.")], record_payload: Annotated[str, Field(..., description="Specify a JSON object containing all of the needed fields and values that need to be updated.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a record in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Record Type"] = record_type
            script_params["Record ID"] = record_id
            script_params["Record Payload"] = record_payload
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Update Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Update Record",
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
                print(f"Error executing action BMCRemedyITSM_Update Record for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_get_record_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], record_type: Annotated[str, Field(..., description="Specify the type of the record for which you want to retrieve details.")], record_i_ds: Annotated[str, Field(..., description="Specify the ids of records for which you want to return details.")], fields_to_return: Annotated[str, Field(default=None, description="Specify what fields to return. If invalid fields are provided, action will fail. If nothing is provided, action will return all fields.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get detailed information about the record from BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Record Type"] = record_type
            script_params["Record IDs"] = record_i_ds
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
                actionName="BMCRemedyITSM_Get Record Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Get Record Details",
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
                print(f"Error executing action BMCRemedyITSM_Get Record Details for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_add_work_note_to_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the id of the incident to which you want to add a work note.")], work_note_text: Annotated[str, Field(..., description="Specify the text for the work note.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a work note to incidents in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident ID"] = incident_id
            script_params["Work Note Text"] = work_note_text
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Add Work Note To Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Add Work Note To Incident",
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
                print(f"Error executing action BMCRemedyITSM_Add Work Note To Incident for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_wait_for_record_fields_update(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], record_type: Annotated[str, Field(..., description="Specify the type of the record for which you are waiting an update.")], record_id: Annotated[str, Field(..., description="Specify the ID of the record that needs to be updated.")], fields_to_check: Annotated[str, Field(..., description="Specify a JSON object containing all of the needed fields and values.")], fail_if_timeout: Annotated[bool, Field(..., description="If enabled, action will be failed, if not all of the fields were updated.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for record fields update in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Record Type"] = record_type
            script_params["Record ID"] = record_id
            script_params["Fields To Check"] = fields_to_check
            script_params["Fail If Timeout"] = fail_if_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Wait For Record Fields Update",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Wait For Record Fields Update",
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
                print(f"Error executing action BMCRemedyITSM_Wait For Record Fields Update for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_delete_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the id of the incident that needs to be deleted.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete an incident in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident ID"] = incident_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Delete Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Delete Incident",
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
                print(f"Error executing action BMCRemedyITSM_Delete Incident for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the BMC Remedy ITSM with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
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
                actionName="BMCRemedyITSM_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Ping",
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
                print(f"Error executing action BMCRemedyITSM_Ping for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_delete_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], record_type: Annotated[str, Field(..., description="Specify the type of the record that needs to be deleted.")], record_id: Annotated[str, Field(..., description="Specify the id of the record that needs to be deleted.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete a record in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Record Type"] = record_type
            script_params["Record ID"] = record_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Delete Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Delete Record",
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
                print(f"Error executing action BMCRemedyITSM_Delete Record for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_get_incident_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_i_ds: Annotated[str, Field(..., description="Specify the ids of incidents for which you want to return details.")], fields_to_return: Annotated[str, Field(default=None, description="Specify what fields to return. If invalid fields are provided, action will fail. If nothing is provided, action will return all fields.")], fetch_work_notes: Annotated[bool, Field(default=None, description="If enabled, action will return work notes related to the incident.")], max_work_notes_to_return: Annotated[str, Field(default=None, description="Specify how many Work Notes to return. If nothing is provided, action will return 50 Work Notes.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get detailed information about the incidents from BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident IDs"] = incident_i_ds
            if fields_to_return is not None:
                script_params["Fields To Return"] = fields_to_return
            if fetch_work_notes is not None:
                script_params["Fetch Work Notes"] = fetch_work_notes
            if max_work_notes_to_return is not None:
                script_params["Max Work Notes To Return"] = max_work_notes_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Get Incident Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Get Incident Details",
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
                print(f"Error executing action BMCRemedyITSM_Get Incident Details for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_create_record(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], record_type: Annotated[str, Field(..., description="Specify the type of the record that needs to be created.")], record_payload: Annotated[str, Field(..., description="Specify a JSON object containing all of the needed fields and  values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a record in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Record Type"] = record_type
            script_params["Record Payload"] = record_payload
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Create Record",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Create Record",
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
                print(f"Error executing action BMCRemedyITSM_Create Record for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_create_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], status: Annotated[List[str], Field(default=None, description="Specify the status for the incident.")], impact: Annotated[List[str], Field(default=None, description="Specify the impact for the incident.")], urgency: Annotated[List[str], Field(default=None, description="Specify the urgency for the incident.")], description: Annotated[str, Field(default=None, description="Specify the description of the incident")], company: Annotated[str, Field(default=None, description="Specify the company for the incident")], customer: Annotated[str, Field(default=None, description="Specify the customer for the incident. Note: Customer needs to be provide in the format \"{Last Name} {First Name}\". Example: Allbrook Allen.")], template_name: Annotated[str, Field(default=None, description="Specify the name of the template for the incident. Note: action will try to find the ID of the template in the background. For better precision you can provide the template ID directly via Custom Fields.")], incident_type: Annotated[List[str], Field(default=None, description="Specify the incident type for the incident.")], assigned_group: Annotated[str, Field(default=None, description="Specify the assigned group for the incident")], assignee: Annotated[str, Field(default=None, description="Specify the assignee for the incident")], resolution: Annotated[str, Field(default=None, description="Specify the resolution for the incident.")], resolution_category_tier_1: Annotated[str, Field(default=None, description="Specify the resolution category tier 1 for the incident.")], resolution_category_tier_2: Annotated[str, Field(default=None, description="Specify the resolution category tier 2 for the incident.")], resolution_category_tier_3: Annotated[str, Field(default=None, description="Specify the resolution category tier 3 for the incident.")], resolution_product_category_tier_1: Annotated[str, Field(default=None, description="Specify the resolution category tier 1 for the incident.")], resolution_product_category_tier_2: Annotated[str, Field(default=None, description="Specify the resolution category tier 2 for the incident.")], resolution_product_category_tier_3: Annotated[str, Field(default=None, description="Specify the resolution category tier 3 for the incident.")], reported_source: Annotated[List[str], Field(default=None, description="Specify the reported source")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object containing all of the needed fields and  values that need to be used during the creation. Note: this parameter will overwrite other provided parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an incident in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if status is not None:
                script_params["Status"] = status
            if impact is not None:
                script_params["Impact"] = impact
            if urgency is not None:
                script_params["Urgency"] = urgency
            if description is not None:
                script_params["Description"] = description
            if company is not None:
                script_params["Company"] = company
            if customer is not None:
                script_params["Customer"] = customer
            if template_name is not None:
                script_params["Template Name"] = template_name
            if incident_type is not None:
                script_params["Incident Type"] = incident_type
            if assigned_group is not None:
                script_params["Assigned Group"] = assigned_group
            if assignee is not None:
                script_params["Assignee"] = assignee
            if resolution is not None:
                script_params["Resolution"] = resolution
            if resolution_category_tier_1 is not None:
                script_params["Resolution Category Tier 1"] = resolution_category_tier_1
            if resolution_category_tier_2 is not None:
                script_params["Resolution Category Tier 2"] = resolution_category_tier_2
            if resolution_category_tier_3 is not None:
                script_params["Resolution Category Tier 3"] = resolution_category_tier_3
            if resolution_product_category_tier_1 is not None:
                script_params["Resolution Product Category Tier 1"] = resolution_product_category_tier_1
            if resolution_product_category_tier_2 is not None:
                script_params["Resolution Product Category Tier 2"] = resolution_product_category_tier_2
            if resolution_product_category_tier_3 is not None:
                script_params["Resolution Product Category Tier 3"] = resolution_product_category_tier_3
            if reported_source is not None:
                script_params["Reported Source"] = reported_source
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
                actionName="BMCRemedyITSM_Create Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Create Incident",
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
                print(f"Error executing action BMCRemedyITSM_Create Incident for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def bmc_remedy_itsm_wait_for_incident_fields_update(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_id: Annotated[str, Field(..., description="Specify the ID of the incident that needs to be updated.")], fail_if_timeout: Annotated[bool, Field(..., description="If enabled, action will be failed, if not all of the fields were updated.")], status: Annotated[List[str], Field(default=None, description="Specify what is the expected status for the incident.")], fields_to_check: Annotated[str, Field(default=None, description="Specify a JSON object containing all of the needed fields and values. Note: this parameter has priority over \"Status\" field.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Wait for incident fields update in BMC Remedy ITSM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="BMCRemedyITSM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for BMCRemedyITSM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident ID"] = incident_id
            if status is not None:
                script_params["Status"] = status
            if fields_to_check is not None:
                script_params["Fields To Check"] = fields_to_check
            script_params["Fail If Timeout"] = fail_if_timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="BMCRemedyITSM_Wait For Incident Fields Update",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "BMCRemedyITSM_Wait For Incident Fields Update",
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
                print(f"Error executing action BMCRemedyITSM_Wait For Incident Fields Update for BMCRemedyITSM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for BMCRemedyITSM")
            return {"Status": "Failed", "Message": "No active instance found."}
