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
    # This function registers all tools (actions) for the Anomali integration.

    @mcp.tool()
    async def anomali_get_threat_info(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], limit: Annotated[str, Field(..., description="Specify how many records to return per entity.")], severity_threshold: Annotated[List[str], Field(default=None, description="Specify what should be the severity threshold for the entity, in order to mark it as suspicious. If multiple records are found for the same entity, action will take the highest severity out of all available records.")], confidence_threshold: Annotated[str, Field(default=None, description="Specify what should be the confidence threshold for the entity, in order to mark it as suspicious. Note: Maximum is 100. If multiple records are found for the entity, action will take the average. Active records have priority. Default: 50.")], ignore_false_positive_status: Annotated[bool, Field(default=None, description="If enabled, action will ignore the false positive status and mark the entity as suspicious based on the \"Severity Threshold\" and \"Confidence Threshold\". If disabled, action will never label false positive entities as suspicious, regardless, if they pass the \"Severity Threshold\" and \"Confidence Threshold\" conditions or not.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich entities using information from Anomali ThreatStream. Supported entities: IP, URL, Hash, Email Addresses (User entities that match email regex).

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Anomali")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Anomali: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Limit"] = limit
            if severity_threshold is not None:
                script_params["Severity Threshold"] = severity_threshold
            if confidence_threshold is not None:
                script_params["Confidence Threshold"] = confidence_threshold
            if ignore_false_positive_status is not None:
                script_params["Ignore False Positive Status"] = ignore_false_positive_status
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Anomali_GetThreatInfo",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Anomali_GetThreatInfo",
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
                print(f"Error executing action Anomali_GetThreatInfo for Anomali: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Anomali")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def anomali_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to Anomali ThreatStream

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Anomali")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Anomali: {e}")
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
                actionName="Anomali_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Anomali_Ping",
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
                print(f"Error executing action Anomali_Ping for Anomali: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Anomali")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def anomali_get_related_associations(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], return_campaigns: Annotated[bool, Field(default=None, description="If enabled, action will fetch related campaigns and details about them.")], return_threat_bulletins: Annotated[bool, Field(default=None, description="If enabled, action will fetch related threat bulletins and details about them.")], return_actors: Annotated[bool, Field(default=None, description="If enabled, action will fetch related actors and details about them.")], return_attack_patterns: Annotated[bool, Field(default=None, description="If enabled, action will fetch related attack patterns and details about them.")], return_courses_of_action: Annotated[bool, Field(default=None, description="If enabled, action will fetch related courses of action and details about them.")], return_identities: Annotated[bool, Field(default=None, description="If enabled, action will fetch related identities and details about them.")], return_incidents: Annotated[bool, Field(default=None, description="If enabled, action will fetch related incidents and details about them.")], return_infrastructure: Annotated[bool, Field(default=None, description="If enabled, action will fetch related infrastructure and details about them.")], return_intrusion_sets: Annotated[bool, Field(default=None, description="If enabled, action will fetch related intrusion sets and details about them.")], return_malware: Annotated[bool, Field(default=None, description="If enabled, action will fetch related malware and details about them.")], return_signatures: Annotated[bool, Field(default=None, description="If enabled, action will fetch related signatures and details about them.")], return_tools: Annotated[bool, Field(default=None, description="If enabled, action will fetch related tools and details about them.")], return_tt_ps: Annotated[bool, Field(default=None, description="If enabled, action will fetch related TTPs and details about them.")], return_vulnerabilities: Annotated[bool, Field(default=None, description="If enabled, action will fetch related vulnerabilities and details about them.")], create_campaign_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \"Campaign\" associations.")], create_actors_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \"Actor\" associations.")], create_signature_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \"Signature\" associations.")], create_vulnerability_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \"Vulnerability\" associations.")], max_associations_to_return: Annotated[str, Field(default=None, description="Specify how many associations to return per type. Default: 5")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related associations from Anomali ThreatStream.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Anomali")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Anomali: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if return_campaigns is not None:
                script_params["Return Campaigns"] = return_campaigns
            if return_threat_bulletins is not None:
                script_params["Return Threat Bulletins"] = return_threat_bulletins
            if return_actors is not None:
                script_params["Return Actors"] = return_actors
            if return_attack_patterns is not None:
                script_params["Return Attack Patterns"] = return_attack_patterns
            if return_courses_of_action is not None:
                script_params["Return Courses Of Action"] = return_courses_of_action
            if return_identities is not None:
                script_params["Return Identities"] = return_identities
            if return_incidents is not None:
                script_params["Return Incidents"] = return_incidents
            if return_infrastructure is not None:
                script_params["Return Infrastructure"] = return_infrastructure
            if return_intrusion_sets is not None:
                script_params["Return Intrusion Sets"] = return_intrusion_sets
            if return_malware is not None:
                script_params["Return Malware"] = return_malware
            if return_signatures is not None:
                script_params["Return Signatures"] = return_signatures
            if return_tools is not None:
                script_params["Return Tools"] = return_tools
            if return_tt_ps is not None:
                script_params["Return TTPs"] = return_tt_ps
            if return_vulnerabilities is not None:
                script_params["Return Vulnerabilities"] = return_vulnerabilities
            if create_campaign_entity is not None:
                script_params["Create Campaign Entity"] = create_campaign_entity
            if create_actors_entity is not None:
                script_params["Create Actors Entity"] = create_actors_entity
            if create_signature_entity is not None:
                script_params["Create Signature Entity"] = create_signature_entity
            if create_vulnerability_entity is not None:
                script_params["Create Vulnerability Entity"] = create_vulnerability_entity
            if max_associations_to_return is not None:
                script_params["Max Associations To Return"] = max_associations_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Anomali_Get Related Associations",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Anomali_Get Related Associations",
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
                print(f"Error executing action Anomali_Get Related Associations for Anomali: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Anomali")
            return {"Status": "Failed", "Message": "No active instance found."}
