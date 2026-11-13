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
from typing import Annotated
from pydantic import Field
from secops_soar_mcp.utils.pydantic_list_field import PydanticListField
from logger_utils import get_logger

logger = get_logger(__name__)


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the ThreatQ integration.

    @mcp.tool()
    async def threat_q_enrich_email(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], score_threshold: Annotated[str | None, Field(default=None, description="Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.")], show_sources: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related sources.")], show_comments: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related comments.")], show_attributes: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related attributes.")], mark_whitelisted_entities_as_suspicious: Annotated[bool | None, Field(default=None, description="If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich an email address using ThreatQ information.

Action Parameters: Score Threshold: Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, the entity will be marked as suspicious., Show Sources: If enabled, action will return an additional table with related sources., Show Comments: If enabled, action will return an additional table with related comments., Show Attributes: If enabled, action will return an additional table with related attributes., Mark Whitelisted Entities As Suspicious: If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if score_threshold is not None:
                script_params["Score Threshold"] = score_threshold
            if show_sources is not None:
                script_params["Show Sources"] = show_sources
            if show_comments is not None:
                script_params["Show Comments"] = show_comments
            if show_attributes is not None:
                script_params["Show Attributes"] = show_attributes
            if mark_whitelisted_entities_as_suspicious is not None:
                script_params["Mark Whitelisted Entities As Suspicious"] = mark_whitelisted_entities_as_suspicious
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Enrich Email",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Enrich Email",
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
                logger.error("Error executing action ThreatQ_Enrich Email for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_add_source(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], object_type: Annotated[list[str], Field(..., description="Specify to which object type source should be added.")], object_identifier: Annotated[str, Field(..., description="Specify identifier of the object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.")], source_name: Annotated[str, Field(..., description="Specify the name of the source.")], indicator_type: Annotated[list[str] | None, Field(default=None, description="Specify the type of the indicator. This parameter is only used, if Source Object Type is Indicator.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action adds a source to the object.

Action Parameters: Object Type: Specify to which object type source should be added., Object Identifier: Specify the identifier of the object. For example, it can be an MD5 hash, title of the event, name of the adversary, etc., Indicator Type: Specify the type of indicator. This parameter is only used if Object Type is "Indicator"., Source Name: Specify the name of the source.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Object Type"] = object_type
            script_params["Object Identifier"] = object_identifier
            if indicator_type is not None:
                script_params["Indicator Type"] = indicator_type
            script_params["Source Name"] = source_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Add Source",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Add Source",
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
                logger.error("Error executing action ThreatQ_Add Source for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_enrich_hash(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], score_threshold: Annotated[str | None, Field(default=None, description="Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.")], show_sources: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related sources.")], show_comments: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related comments.")], show_attributes: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related attributes.")], mark_whitelisted_entities_as_suspicious: Annotated[bool | None, Field(default=None, description="If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich a Hash using ThreatQ information.

Action Parameters: Score Threshold: Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, the entity will be marked as suspicious., Show Sources: If enabled, action will return an additional table with related sources., Show Comments: If enabled, action will return an additional table with related comments., Show Attributes: If enabled, action will return an additional table with related attributes., Mark Whitelisted Entities As Suspicious: If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if score_threshold is not None:
                script_params["Score Threshold"] = score_threshold
            if show_sources is not None:
                script_params["Show Sources"] = show_sources
            if show_comments is not None:
                script_params["Show Comments"] = show_comments
            if show_attributes is not None:
                script_params["Show Attributes"] = show_attributes
            if mark_whitelisted_entities_as_suspicious is not None:
                script_params["Mark Whitelisted Entities As Suspicious"] = mark_whitelisted_entities_as_suspicious
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Enrich Hash",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Enrich Hash",
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
                logger.error("Error executing action ThreatQ_Enrich Hash for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_get_indicator_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search for entities in ThreatQ and get detailed information.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
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
                actionName="ThreatQ_Get Indicator Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Get Indicator Details",
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
                logger.error("Error executing action ThreatQ_Get Indicator Details for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_enrich_cve(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], score_threshold: Annotated[str | None, Field(default=None, description="Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.")], show_sources: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related sources.")], show_comments: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related comments.")], show_attributes: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related attributes.")], mark_whitelisted_entities_as_suspicious: Annotated[bool | None, Field(default=None, description="If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich a CVE using ThreatQ information.

Action Parameters: Score Threshold: Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, the entity will be marked as suspicious., Show Sources: If enabled, action will return an additional table with related sources., Show Comments: If enabled, action will return an additional table with related comments., Show Attributes: If enabled, action will return an additional table with related attributes., Mark Whitelisted Entities As Suspicious: If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if score_threshold is not None:
                script_params["Score Threshold"] = score_threshold
            if show_sources is not None:
                script_params["Show Sources"] = show_sources
            if show_comments is not None:
                script_params["Show Comments"] = show_comments
            if show_attributes is not None:
                script_params["Show Attributes"] = show_attributes
            if mark_whitelisted_entities_as_suspicious is not None:
                script_params["Mark Whitelisted Entities As Suspicious"] = mark_whitelisted_entities_as_suspicious
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Enrich CVE",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Enrich CVE",
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
                logger.error("Error executing action ThreatQ_Enrich CVE for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_update_indicator_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], status: Annotated[list[str], Field(..., description="Specify the new status of the indicator.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action updates indicator status in ThreatQ.

Action Parameters: Status: Specify the new status of the indicator.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Status"] = status
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Update Indicator Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Update Indicator Status",
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
                logger.error("Error executing action ThreatQ_Update Indicator Status for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_create_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], event_type: Annotated[list[str], Field(..., description="Specify the type of the event.")], title: Annotated[str, Field(..., description="Specify the title of the event.")], happened_at: Annotated[str | None, Field(default=None, description="Specify when the event happened. If nothing is entered in this field, action will use current time. Format: YYYY-MM-DD hh:mm:ss")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create an event in ThreatQ.

Action Parameters: Title: Specify the title of the event., Event Type: Specify the type of the event., Happened At: Specify when the event happened. If nothing is entered in this field, action will use current time. Format: YYYY-MM-DD hh:mm:ss

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Event Type"] = event_type
            script_params["Title"] = title
            if happened_at is not None:
                script_params["Happened At"] = happened_at
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Create Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Create Event",
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
                logger.error("Error executing action ThreatQ_Create Event for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_link_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action links all of the entities in ThreatQ.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
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
                actionName="ThreatQ_Link Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Link Entities",
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
                logger.error("Error executing action ThreatQ_Link Entities for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_list_related_objects(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], source_object_type: Annotated[list[str], Field(..., description="Specify the type of the source object.")], source_object_identifier: Annotated[str, Field(..., description="Specify identifier of the source object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.")], related_object_type: Annotated[list[str], Field(..., description="Specify the type of the related object that needs to be returned.")], source_indicator_type: Annotated[list[str] | None, Field(default=None, description="Specify the type of the source indicator. This parameter is only used, if Source Object Type is Indicator.")], max_related_objects_to_return: Annotated[str | None, Field(default=None, description="Specify how many related objects to return.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action lists related objects in ThreatQ.

Action Parameters: Source Object Type: Specify the type of the source object., Source Object Identifier: Specify the identifier of the source object. For example, it can be an MD5 hash, title of the event, name of the adversary, etc., Source Indicator Type: Specify the type of the source indicator. This parameter is only used, if Source Object Type is "Indicator"., Related Object Type: Specify the type of the related object that needs to be returned., Max Related Objects To Return: Specify how many related objects to return.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Source Object Type"] = source_object_type
            script_params["Source Object Identifier"] = source_object_identifier
            if source_indicator_type is not None:
                script_params["Source Indicator Type"] = source_indicator_type
            script_params["Related Object Type"] = related_object_type
            if max_related_objects_to_return is not None:
                script_params["Max Related Objects To Return"] = max_related_objects_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_List Related Objects",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_List Related Objects",
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
                logger.error("Error executing action ThreatQ_List Related Objects for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_list_entity_related_objects(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], related_object_type: Annotated[list[str], Field(..., description="Specify the type of the related object that needs to be returned.")], max_related_objects_to_return: Annotated[str | None, Field(default=None, description="Specify how many related objects to return. Maximum is 1000. This is a ThreatQ limitation.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action lists related objects for entities in ThreatQ.

Action Parameters: Related Object Type: Specify the type of related object that needs to be returned., Max Related Objects To Return: Specify how many related objects to return. Maximum is 1000. This is a ThreatQ limitation.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Related Object Type"] = related_object_type
            if max_related_objects_to_return is not None:
                script_params["Max Related Objects To Return"] = max_related_objects_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_List Entity Related Objects",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_List Entity Related Objects",
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
                logger.error("Error executing action ThreatQ_List Entity Related Objects for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_enrich_ip(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], score_threshold: Annotated[str | None, Field(default=None, description="Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.")], show_sources: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related sources.")], show_comments: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related comments.")], show_attributes: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related attributes.")], mark_whitelisted_entities_as_suspicious: Annotated[bool | None, Field(default=None, description="If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich an IP using ThreatQ information.

Action Parameters: Score Threshold: Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, the entity will be marked as suspicious., Show Sources: If enabled, action will return an additional table with related sources., Show Comments: If enabled, action will return an additional table with related comments., Show Attributes: If enabled, action will return an additional table with related attributes., Mark Whitelisted Entities As Suspicious: If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if score_threshold is not None:
                script_params["Score Threshold"] = score_threshold
            if show_sources is not None:
                script_params["Show Sources"] = show_sources
            if show_comments is not None:
                script_params["Show Comments"] = show_comments
            if show_attributes is not None:
                script_params["Show Attributes"] = show_attributes
            if mark_whitelisted_entities_as_suspicious is not None:
                script_params["Mark Whitelisted Entities As Suspicious"] = mark_whitelisted_entities_as_suspicious
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Enrich IP",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Enrich IP",
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
                logger.error("Error executing action ThreatQ_Enrich IP for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_create_adversary(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an adversary in ThreatQ.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
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
                actionName="ThreatQ_Create Adversary",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Create Adversary",
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
                logger.error("Error executing action ThreatQ_Create Adversary for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
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
                actionName="ThreatQ_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Ping",
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
                logger.error("Error executing action ThreatQ_Ping for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_list_events(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], additional_fields: Annotated[str | None, Field(default=None, description="Specify what additional fields should be included in the response. Possible values: adversaries, attachments, attributes, comments, events, indicators, signatures, sources, spearphish, tags, type, watchlist.")], sort_field: Annotated[list[str] | None, Field(default=None, description="Specify what field should be used for sorting events.")], sort_direction: Annotated[list[str] | None, Field(default=None, description="Specify the sorting direction.")], max_events_to_return: Annotated[str | None, Field(default=None, description="Specify how many events to return.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
List events from ThreatQ.

Action Parameters: Additional Fields: Specify what additional fields should be included in the response. Possible values: adversaries, attachments, attributes, comments, events, indicators, signatures, sources, spearphish, tags, type, watchlist., Sort Field: Specify what field should be used for sorting events., Sort Direction: Specify the sorting direction., Max Events to Return: Specify how many events to return.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if additional_fields is not None:
                script_params["Additional Fields"] = additional_fields
            if sort_field is not None:
                script_params["Sort Field"] = sort_field
            if sort_direction is not None:
                script_params["Sort Direction"] = sort_direction
            if max_events_to_return is not None:
                script_params["Max Events To Return"] = max_events_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_List Events",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_List Events",
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
                logger.error("Error executing action ThreatQ_List Events for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_update_indicator_score(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], score: Annotated[list[str], Field(..., description="Specify the new score of the indicator.")], score_validation: Annotated[list[str], Field(..., description="Specify what kind of score validation should be used. If \u201c Highest Score\u201d is specified, action will compare current values and update the indicator\u2019s score only, if the specified score is higher than current generated and manual score. If \u201cForce Update\u201d is specified, action will update the indicator's score without comparing current values.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action updates indicator score in ThreatQ

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Score"] = score
            script_params["Score Validation"] = score_validation
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Update Indicator Score",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Update Indicator Score",
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
                logger.error("Error executing action ThreatQ_Update Indicator Score for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_link_entities_to_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], object_type: Annotated[list[str], Field(..., description="Specify the type of the object to which you want to link entities.")], object_identifier: Annotated[str, Field(..., description="Specify identifier of the object to which you want to link entities. For example, it can be an MD5 hash, title of the event, name of the adversary etc.")], indicator_type: Annotated[list[str] | None, Field(default=None, description="Specify the type of the  indicator to which you want to link entities. This parameter is only used, if Source Object Type is \u201cIndicator\u201d.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action links all of the entities in ThreatQ.

Action Parameters: Object Type: Specify the type of the object to which you want to link entities., Object Identifier: Specify identifier of the object to which you want to link entities. For example, it can be an MD5 hash, title of the event, name of the adversary etc., Indicator Type: Specify the type of the indicator to which you want to link entities. This parameter is only used, if Source Object Type is "Indicator".

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Object Type"] = object_type
            script_params["Object Identifier"] = object_identifier
            if indicator_type is not None:
                script_params["Indicator Type"] = indicator_type
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Link Entities To Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Link Entities To Object",
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
                logger.error("Error executing action ThreatQ_Link Entities To Object for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_add_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], object_type: Annotated[list[str], Field(..., description="Specify to which object type attribute should be added.")], object_identifier: Annotated[str, Field(..., description="Specify identifier of the object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.")], attribute_name: Annotated[str, Field(..., description="Specify the name of the attribute.")], attribute_value: Annotated[str, Field(..., description="Specify the value of the attribute.")], indicator_type: Annotated[list[str] | None, Field(default=None, description="Specify the type of the indicator. This parameter is only used, if Source Object Type is Indicator.")], attribute_source: Annotated[str | None, Field(default=None, description="Specify the source of the attribute.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action adds an attribute to the object.

Action Parameters: Object Type: Specify to which object type attribute should be added., Object Identifier: Specify the identifier of the object. For example, it can be an MD5 hash, title of the event, name of the adversary, etc., Indicator Type: Specify the type of the indicator. This parameter is only used if Object Type is "Indicator", Attribute Name: Specify the name of the attribute., Attribute Value: Specify the value of the attribute, Attribute Source: Specify the source of the attribute.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Object Type"] = object_type
            script_params["Object Identifier"] = object_identifier
            if indicator_type is not None:
                script_params["Indicator Type"] = indicator_type
            script_params["Attribute Name"] = attribute_name
            script_params["Attribute Value"] = attribute_value
            if attribute_source is not None:
                script_params["Attribute Source"] = attribute_source
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Add Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Add Attribute",
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
                logger.error("Error executing action ThreatQ_Add Attribute for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_create_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], object_type: Annotated[list[str], Field(..., description="Specify to which object type attribute should be added.")], value: Annotated[str, Field(..., description="Specify the value of the new object.")], description: Annotated[str | None, Field(default=None, description="Specify description of the new object.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create an object in ThreatQ.

Action Parameters: Object Type: Specify the type of the object., Value: Specify the value of the new object., Description: Specify description to the new object.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Object Type"] = object_type
            script_params["Value"] = value
            if description is not None:
                script_params["Description"] = description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Create Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Create Object",
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
                logger.error("Error executing action ThreatQ_Create Object for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_get_malware_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], additional_information: Annotated[str | None, Field(default=None, description="Specify what additional fields should be included in the response. Possible values: adversaries, attackPattern, campaign, courseOfAction, attachments, attributes, comments, events, indicators, signatures, sources, status, tags, type, watchlist, exploitTarget, identity, incident, intrusionSet, malware, report, tool, ttp, vulnerability, tasks")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action returns information about malware based on entities from ThreatQ.

Action Parameters: Additional Information: Specify what additional fields should be included in the response. Possible values: adversaries, attackPattern, campaign, courseOfAction, attachments, attributes, comments, events, indicators, signatures, sources, status, tags, type, watchlist, exploitTarget, identity, incident, intrusionSet, malware, report, tool, ttp, vulnerability, tasks

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if additional_information is not None:
                script_params["Additional Information"] = additional_information
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Get Malware Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Get Malware Details",
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
                logger.error("Error executing action ThreatQ_Get Malware Details for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_create_indicator(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], indicator_type: Annotated[list[str], Field(..., description="Specify the type of the new indicator.")], status: Annotated[list[str], Field(..., description="Specify the status of the new indicator.")], description: Annotated[str | None, Field(default=None, description="Specify description of the new indicator.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create an indicator in ThreatQ.

Action Parameters: Indicator Type: Specify the type of the new indicator., Status: Specify the status of the new indicator., Description: Specify description of the new indicator.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Indicator Type"] = indicator_type
            script_params["Status"] = status
            if description is not None:
                script_params["Description"] = description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Create Indicator",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Create Indicator",
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
                logger.error("Error executing action ThreatQ_Create Indicator for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_link_objects(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], source_object_type: Annotated[list[str], Field(..., description="Specify the type of the source object.")], source_object_identifier: Annotated[str, Field(..., description="Specify identifier of the source object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.")], destination_object_type: Annotated[list[str], Field(..., description="Specify the type of the destination object.")], destination_object_identifier: Annotated[str, Field(..., description="Specify identifier of the destination object. For example, it can be an MD5 hash, title of the event, name of the adversary etc.")], source_indicator_type: Annotated[list[str] | None, Field(default=None, description="Specify the type of the source indicator. This parameter is only used, if Source Object Type is Indicator.")], destination_indicator_type: Annotated[list[str] | None, Field(default=None, description="Specify the type of the destination indicator. This parameter is only used, if Destination Object Type is Indicator.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Action links two objects in ThreatQ.

Action Parameters: Source Object Type: Specify the type of the source object., Source Object Identifier: Specify identifier of the source object. For example, it can be an MD5 hash, title of the event, name of the adversary etc., Source Indicator Type: Specify the type of the source indicator. This parameter is only used, if Source Object Type is "Indicator"., Destination Object Type: Specify the type of the destination object., Destination Object Identifier: Specify the identifier of the destination object. For example, it can be an MD5 hash, title of the event, name of the adversary, etc., Destination Indicator Type: Specify the type of the destination indicator. This parameter is only used if Destination Object Type is "Indicator".

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Source Object Type"] = source_object_type
            script_params["Source Object Identifier"] = source_object_identifier
            if source_indicator_type is not None:
                script_params["Source Indicator Type"] = source_indicator_type
            script_params["Destination Object Type"] = destination_object_type
            script_params["Destination Object Identifier"] = destination_object_identifier
            if destination_indicator_type is not None:
                script_params["Destination Indicator Type"] = destination_indicator_type
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Link Objects",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Link Objects",
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
                logger.error("Error executing action ThreatQ_Link Objects for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def threat_q_enrich_url(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[list[str], Field(..., description="Identifiers for the alert groups.")], score_threshold: Annotated[str | None, Field(default=None, description="Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, entity will be marked as suspicious.")], show_sources: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related sources.")], show_comments: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related comments.")], show_attributes: Annotated[bool | None, Field(default=None, description="If enabled, action will return an additional table with related attributes.")], mark_whitelisted_entities_as_suspicious: Annotated[bool | None, Field(default=None, description="If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.")], target_entities: Annotated[list[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich an URL using ThreatQ information.

Action Parameters: Score Threshold: Set the acceptable score threshold for the entity. If the score exceeds the specified threshold, the entity will be marked as suspicious., Show Sources: If enabled, action will return an additional table with related sources., Show Comments: If enabled, action will return an additional table with related comments., Show Attributes: If enabled, action will return an additional table with related attributes., Mark Whitelisted Entities As Suspicious: If enabled, action will mark entities as suspicious if they passed the allowed threshold, even if the entity is whitelisted in ThreatQ.

Returns:
dict: A dictionary containing the result of the action execution.
"""
        final_target_entities: list[TargetEntity] | None = None
        final_scope: str | None = None
        is_predefined_scope: bool | None = None
    
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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ThreatQ")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            logger.error("Error fetching instance for ThreatQ: %s", e)
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if score_threshold is not None:
                script_params["Score Threshold"] = score_threshold
            if show_sources is not None:
                script_params["Show Sources"] = show_sources
            if show_comments is not None:
                script_params["Show Comments"] = show_comments
            if show_attributes is not None:
                script_params["Show Attributes"] = show_attributes
            if mark_whitelisted_entities_as_suspicious is not None:
                script_params["Mark Whitelisted Entities As Suspicious"] = mark_whitelisted_entities_as_suspicious
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ThreatQ_Enrich URL",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ThreatQ_Enrich URL",
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
                logger.error("Error executing action ThreatQ_Enrich URL for ThreatQ: %s", e)
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            logger.warning("Warning: No active integration instance found for ThreatQ")
            return {"Status": "Failed", "Message": "No active instance found."}
