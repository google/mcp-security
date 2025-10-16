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
    # This function registers all tools (actions) for the ZohoDesk integration.

    @mcp.tool()
    async def zoho_desk_create_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], title: Annotated[str, Field(..., description="Specify the title for the ticket.")], description: Annotated[str, Field(..., description="Specify the description of the ticket.")], department_name: Annotated[str, Field(..., description="Specify the name of the department in which you want to create a ticket.")], contact: Annotated[str, Field(..., description="Specify the email of the contact for the ticket.")], assignee_type: Annotated[List[str], Field(default=None, description="Specify the type of the assignee. If \"Agent\" or \"Team\" is selected \"Assignee Name\" is required.")], assignee_name: Annotated[str, Field(default=None, description="Specify the name of the assignee for the ticket. For the agent type you can provide an email address or display name.")], priority: Annotated[List[str], Field(default=None, description="Specify the priority for the ticket.")], classification: Annotated[List[str], Field(default=None, description="Specify the classification type for the ticket.")], channel: Annotated[List[str], Field(default=None, description="Specify the channel for the ticket.")], category: Annotated[str, Field(default=None, description="Specify the category for the ticket.")], sub_category: Annotated[str, Field(default=None, description="Specify the subcategory for the ticket.")], due_date: Annotated[str, Field(default=None, description="Specify the due date for the ticket. Format: ISO 8601. Example: 2022-07-06T07:05:43Z.")], custom_fields: Annotated[str, Field(default=None, description="Specify a json object containing the custom fields that need to be added. Note: you need to provide the API names of the keys.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a ticket in Zoho Desk.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Title"] = title
            script_params["Description"] = description
            script_params["Department Name"] = department_name
            script_params["Contact"] = contact
            if assignee_type is not None:
                script_params["Assignee Type"] = assignee_type
            if assignee_name is not None:
                script_params["Assignee Name"] = assignee_name
            if priority is not None:
                script_params["Priority"] = priority
            if classification is not None:
                script_params["Classification"] = classification
            if channel is not None:
                script_params["Channel"] = channel
            if category is not None:
                script_params["Category"] = category
            if sub_category is not None:
                script_params["Sub Category"] = sub_category
            if due_date is not None:
                script_params["Due Date"] = due_date
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
                actionName="ZohoDesk_Create Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Create Ticket",
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
                print(f"Error executing action ZohoDesk_Create Ticket for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zoho_desk_get_ticket_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_i_ds: Annotated[str, Field(..., description="Specify a comma-separated list of ids for which you want to return details.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about tickets.")], additional_fields_to_return: Annotated[str, Field(default=None, description="Specify what additional fields to return. Possible values: contacts, products, assignee, departments, contract, isRead, team, skills.")], fetch_comments: Annotated[bool, Field(default=None, description="If enabled, action will fetch comments related to the tickets.")], max_comments_to_return: Annotated[str, Field(default=None, description="Specify how many comments to return per ticket. Default: 50. Maximum: 100.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get detailed information about the ticket from Zoho Desk.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket IDs"] = ticket_i_ds
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if additional_fields_to_return is not None:
                script_params["Additional Fields To Return"] = additional_fields_to_return
            if fetch_comments is not None:
                script_params["Fetch Comments"] = fetch_comments
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ZohoDesk_Get Ticket Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Get Ticket Details",
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
                print(f"Error executing action ZohoDesk_Get Ticket Details for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zoho_desk_add_comment_to_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify an id of the ticket to which you want to add a comment.")], text: Annotated[str, Field(..., description="Specify the content of the comment.")], visibility: Annotated[List[str], Field(default=None, description="Specify if the comment should be public or private.")], type: Annotated[List[str], Field(default=None, description="Specify what should be the type of the comment.")], wait_for_reply: Annotated[bool, Field(default=None, description="If enabled, action will wait for reply.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to a ticket in Zoho Desk. Note: Action is running as async if "Wait For Reply" is enabled, please adjust script timeout value in Siemplify IDE for action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if visibility is not None:
                script_params["Visibility"] = visibility
            if type is not None:
                script_params["Type"] = type
            script_params["Text"] = text
            if wait_for_reply is not None:
                script_params["Wait For Reply"] = wait_for_reply
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ZohoDesk_Add Comment To Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Add Comment To Ticket",
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
                print(f"Error executing action ZohoDesk_Add Comment To Ticket for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zoho_desk_mark_ticket_as_spam(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify an id of the ticket that needs to be marked as spam.")], mark_contact: Annotated[bool, Field(default=None, description="If enabled, the contact that created the ticket will be marked as spammer.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Mark ticket as spam in Zoho Desk.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if mark_contact is not None:
                script_params["Mark Contact"] = mark_contact
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ZohoDesk_Mark Ticket As Spam",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Mark Ticket As Spam",
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
                print(f"Error executing action ZohoDesk_Mark Ticket As Spam for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zoho_desk_get_refresh_token(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], authorization_link: Annotated[str, Field(..., description="Specify the authorization link for the integration.")], authorization_code: Annotated[str, Field(..., description="Specify the authorization code that was generated in the dev console of Zoho.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get a refresh token for the configuration.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Authorization Link"] = authorization_link
            script_params["Authorization Code"] = authorization_code
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ZohoDesk_Get Refresh Token",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Get Refresh Token",
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
                print(f"Error executing action ZohoDesk_Get Refresh Token for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zoho_desk_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Zoho Desk with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
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
                actionName="ZohoDesk_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Ping",
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
                print(f"Error executing action ZohoDesk_Ping for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zoho_desk_update_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify an id of the ticket that needs to be updated.")], title: Annotated[str, Field(default=None, description="Specify the title that should be set for the ticket.")], description: Annotated[str, Field(default=None, description="Specify the description for the ticket.")], department_name: Annotated[str, Field(default=None, description="Specify the name of the department that should be set for the ticket.")], contact: Annotated[str, Field(default=None, description="Specify the email of the contact for the ticket.")], assignee_type: Annotated[List[str], Field(default=None, description="Specify the type of the assignee. If \u201cAgent\u201d or \u201cTeam\u201d is selected \u201cAssignee Name\u201d is required.")], assignee_name: Annotated[str, Field(default=None, description="Specify the name of the assignee for the ticket. For the agent type you can provide an email address or display name.")], resolution: Annotated[str, Field(default=None, description="Specify the resolution for the ticket.")], priority: Annotated[List[str], Field(default=None, description="Specify the priority for the ticket.")], status: Annotated[List[str], Field(default=None, description="Specify the status for the ticket.")], mark_state: Annotated[List[str], Field(default=None, description="Specify the mark state for the ticket.")], classification: Annotated[List[str], Field(default=None, description="Specify the classification type for the ticket.")], channel: Annotated[List[str], Field(default=None, description="Specify the channel for the ticket.")], category: Annotated[str, Field(default=None, description="Specify the category for the ticket.")], sub_category: Annotated[str, Field(default=None, description="Specify the subcategory for the ticket.")], due_date: Annotated[str, Field(default=None, description="Specify the due date for the ticket. Format: ISO 8601. Example: 2022-07-06T07:05:43Z. Note: this parameter doesn\u2019t have an impact, when status is \u201cOn Hold\u201d.")], custom_fields: Annotated[str, Field(default=None, description="Specify a json object containing the custom fields that need to be added. Note: you need to provide the API names of the keys.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a ticket in Zoho Desk.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ZohoDesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ZohoDesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if title is not None:
                script_params["Title"] = title
            if description is not None:
                script_params["Description"] = description
            if department_name is not None:
                script_params["Department Name"] = department_name
            if contact is not None:
                script_params["Contact"] = contact
            if assignee_type is not None:
                script_params["Assignee Type"] = assignee_type
            if assignee_name is not None:
                script_params["Assignee Name"] = assignee_name
            if resolution is not None:
                script_params["Resolution"] = resolution
            if priority is not None:
                script_params["Priority"] = priority
            if status is not None:
                script_params["Status"] = status
            if mark_state is not None:
                script_params["Mark State"] = mark_state
            if classification is not None:
                script_params["Classification"] = classification
            if channel is not None:
                script_params["Channel"] = channel
            if category is not None:
                script_params["Category"] = category
            if sub_category is not None:
                script_params["Sub Category"] = sub_category
            if due_date is not None:
                script_params["Due Date"] = due_date
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
                actionName="ZohoDesk_Update Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ZohoDesk_Update Ticket",
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
                print(f"Error executing action ZohoDesk_Update Ticket for ZohoDesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ZohoDesk")
            return {"Status": "Failed", "Message": "No active instance found."}
