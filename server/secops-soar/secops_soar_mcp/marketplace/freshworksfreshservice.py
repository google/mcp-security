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
    # This function registers all tools (actions) for the FreshworksFreshservice integration.

    @mcp.tool()
    async def freshworks_freshservice_list_tickets(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_type: Annotated[List[str], Field(default=None, description="Specify ticket type to return.")], requester: Annotated[str, Field(default=None, description="Specify the requester email of tickets to return.")], include_stats: Annotated[bool, Field(default=None, description="If enabled, action will return additional stats on the tickets.")], search_for_last_x_hours: Annotated[str, Field(default=None, description="Specify the timeframe to search tickets for.")], rows_per_page: Annotated[str, Field(default=None, description="Specify how many tickets should be returned per page for Freshservice pagination.")], start_at_page: Annotated[str, Field(default=None, description="Specify starting from which page tickets should be returned with Freshservice pagination.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many tickets action should return in total.")], workspace_id: Annotated[str, Field(default=None, description="Specify the ID of the workspace that should be used to list tickets. If nothing is provided, the action will list tickets only from the primary workspace. To list tickets from all workspaces provide \u201c0\u201d in the parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Freshservice tickets base on the specified search criteria. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if ticket_type is not None:
                script_params["Ticket Type"] = ticket_type
            if requester is not None:
                script_params["Requester"] = requester
            if include_stats is not None:
                script_params["Include Stats"] = include_stats
            if search_for_last_x_hours is not None:
                script_params["Search for Last X hours"] = search_for_last_x_hours
            if rows_per_page is not None:
                script_params["Rows per Page"] = rows_per_page
            if start_at_page is not None:
                script_params["Start at Page"] = start_at_page
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
            if workspace_id is not None:
                script_params["Workspace ID"] = workspace_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_List Tickets",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_List Tickets",
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
                print(f"Error executing action FreshworksFreshservice_List Tickets for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_list_requesters(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], requester_email: Annotated[str, Field(default=None, description="Specify the email address to return requester records for.")], rows_per_page: Annotated[str, Field(default=None, description="Specify how many requester records should be returned per page for Freshservice pagination.")], start_at_page: Annotated[str, Field(default=None, description="Specify starting from which page requester records should be returned with Freshservice pagination.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many requester records action should return in total.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List requesters registered in Freshservice based on the specified search criteria. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if requester_email is not None:
                script_params["Requester Email"] = requester_email
            if rows_per_page is not None:
                script_params["Rows per Page"] = rows_per_page
            if start_at_page is not None:
                script_params["Start at Page"] = start_at_page
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_List Requesters",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_List Requesters",
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
                print(f"Error executing action FreshworksFreshservice_List Requesters for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_create_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="Specify subject field for created ticket.")], description: Annotated[str, Field(..., description="Specify description field for created ticket.")], requester_email: Annotated[str, Field(..., description="Specify requester email for created ticket.")], priority: Annotated[List[str], Field(..., description="Specify priority to assign to the ticket.")], agent_assign_to: Annotated[str, Field(default=None, description="Specify the agent email to assign the ticket to.")], group_assign_to: Annotated[str, Field(default=None, description="Specify the group name to assign the ticket to.")], urgency: Annotated[List[str], Field(default=None, description="Specify urgency to assign to the ticket.")], impact: Annotated[List[str], Field(default=None, description="Specify impact to assign to the ticket.")], tags: Annotated[str, Field(default=None, description="Specify tags to assign to the ticket. Parameter accepts multiple values as a comma separated string.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the ticket. Action appends new custom fields to any existing for a ticket. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], file_attachments_to_add: Annotated[str, Field(default=None, description="Specify the full path for the file to be uploaded with the ticket. Parameter accepts multiple values as a comma separated string. The total size of the attachments must not exceed 15MB")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a Freshservice ticket. Note: as of now, Freshservice API supports only creation of tickets with the type "Incident" and the ticket's priority is dynamically calculated according to the "Urgency" and "Impact" values, same as in FreshService's UI. Additionally, if file attachments to add are provided, the total size of the attachments must not exceed 15MB.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Subject"] = subject
            script_params["Description"] = description
            script_params["Requester Email"] = requester_email
            if agent_assign_to is not None:
                script_params["Agent Assign To"] = agent_assign_to
            if group_assign_to is not None:
                script_params["Group Assign To"] = group_assign_to
            script_params["Priority"] = priority
            if urgency is not None:
                script_params["Urgency"] = urgency
            if impact is not None:
                script_params["Impact"] = impact
            if tags is not None:
                script_params["Tags"] = tags
            if custom_fields is not None:
                script_params["Custom Fields"] = custom_fields
            if file_attachments_to_add is not None:
                script_params["File Attachments to Add"] = file_attachments_to_add
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Create Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Create Ticket",
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
                print(f"Error executing action FreshworksFreshservice_Create Ticket for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_add_a_ticket_reply(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to return conversations for.")], reply_text: Annotated[str, Field(..., description="Specify reply text to add to ticket.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a reply to a Freshservice ticket. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Reply Text"] = reply_text
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Add a Ticket Reply",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Add a Ticket Reply",
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
                print(f"Error executing action FreshworksFreshservice_Add a Ticket Reply for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_deactivate_agent(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], agent_id: Annotated[str, Field(..., description="Specify agent id to deactivate.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Deactivate Freshservice agent. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Agent ID"] = agent_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Deactivate Agent",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Deactivate Agent",
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
                print(f"Error executing action FreshworksFreshservice_Deactivate Agent for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_delete_ticket_time_entry(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to delete a time entry for.")], time_entry_id: Annotated[str, Field(..., description="Specify time entry ID to delete.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete a time entry for a Freshservice ticket. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Time Entry ID"] = time_entry_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Delete Ticket Time Entry",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Delete Ticket Time Entry",
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
                print(f"Error executing action FreshworksFreshservice_Delete Ticket Time Entry for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_create_agent(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], email: Annotated[str, Field(..., description="Specify the email of the agent to create.")], first_name: Annotated[str, Field(..., description="Specify the first name of the agent to create.")], roles: Annotated[str, Field(..., description="Specify roles to add to agent. Parameter accepts multiple values as a comma separated string. Example: {'role_id':17000023338,'assignment_scope': 'entire_helpdesk'}")], last_name: Annotated[str, Field(default=None, description="Specify the last name of the agent to create.")], is_occasional: Annotated[bool, Field(default=None, description="If enabled, agent will be created as an occasional agent, otherwise full-time agent will be created.")], can_see_all_tickets_from_associated_departments: Annotated[bool, Field(default=None, description="If enabled, agent will be able to see all tickets from Associated departments.")], departments: Annotated[str, Field(default=None, description="Specify department names associated with the agent. Parameter accepts multiple values as a comma separated string.")], location: Annotated[str, Field(default=None, description="Specify location name associated with the agent.")], group_memberships: Annotated[str, Field(default=None, description="Specify group names agent should be a member of.")], job_title: Annotated[str, Field(default=None, description="Specify agent job title.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the agent. Action appends new custom fields to any existing for an agent. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a new Freshservice Agent. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Email"] = email
            script_params["First Name"] = first_name
            if last_name is not None:
                script_params["Last Name"] = last_name
            if is_occasional is not None:
                script_params["Is occasional"] = is_occasional
            if can_see_all_tickets_from_associated_departments is not None:
                script_params["Can See All Tickets From Associated Departments"] = can_see_all_tickets_from_associated_departments
            if departments is not None:
                script_params["Departments"] = departments
            if location is not None:
                script_params["Location"] = location
            if group_memberships is not None:
                script_params["Group Memberships"] = group_memberships
            script_params["Roles"] = roles
            if job_title is not None:
                script_params["Job Title"] = job_title
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
                actionName="FreshworksFreshservice_Create Agent",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Create Agent",
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
                print(f"Error executing action FreshworksFreshservice_Create Agent for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_list_agents(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], agent_email: Annotated[str, Field(default=None, description="Specify the email address to return agent records for.")], agent_state: Annotated[List[str], Field(default=None, description="Specify agent states to return.")], include_not_active_agents: Annotated[bool, Field(default=None, description="If enabled, results will include not active agent records.")], rows_per_page: Annotated[str, Field(default=None, description="Specify how many agent records should be returned per page for Freshservice pagination.")], start_at_page: Annotated[str, Field(default=None, description="Specify starting from which page agent records should be returned with Freshservice pagination")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many agent records action should return in total.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Freshservice agents based on the specified search criteria. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if agent_email is not None:
                script_params["Agent Email"] = agent_email
            if agent_state is not None:
                script_params["Agent State"] = agent_state
            if include_not_active_agents is not None:
                script_params["Include not Active Agents"] = include_not_active_agents
            if rows_per_page is not None:
                script_params["Rows per Page"] = rows_per_page
            if start_at_page is not None:
                script_params["Start at Page"] = start_at_page
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_List Agents",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_List Agents",
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
                print(f"Error executing action FreshworksFreshservice_List Agents for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_list_ticket_time_entries(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to return time entries for.")], agent_email: Annotated[str, Field(..., description="Specify agent email to list ticket time entries for.")], rows_per_page: Annotated[str, Field(default=None, description="Specify how many ticket time entries should be returned per page for Freshservice pagination.")], start_at_page: Annotated[str, Field(default=None, description="Specify starting from which page ticket time entries should be returned with Freshservice pagination.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many ticket time entries action should return in total.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Freshservice tickets time entries based on the specified search criteria. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Agent Email"] = agent_email
            if rows_per_page is not None:
                script_params["Rows per Page"] = rows_per_page
            if start_at_page is not None:
                script_params["Start at Page"] = start_at_page
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_List Ticket Time Entries",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_List Ticket Time Entries",
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
                print(f"Error executing action FreshworksFreshservice_List Ticket Time Entries for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_add_ticket_time_entry(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to add a time entry for.")], agent_email: Annotated[str, Field(..., description="Specify agent email for whom to add a ticket time entry.")], time_spent: Annotated[str, Field(..., description="Specify time spent for ticket time entry. Format: {hh:mm}")], note: Annotated[str, Field(default=None, description="Specify a note to add to the ticket time entry.")], billable: Annotated[bool, Field(default=None, description="If enabled, ticket time entry will be marked as billable.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the ticket time entry. Action appends new custom fields to any existing for ticket time entry. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a time entry to a Freshservice ticket. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Agent Email"] = agent_email
            if note is not None:
                script_params["Note"] = note
            script_params["Time Spent"] = time_spent
            if billable is not None:
                script_params["Billable"] = billable
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
                actionName="FreshworksFreshservice_Add Ticket Time Entry",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Add Ticket Time Entry",
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
                print(f"Error executing action FreshworksFreshservice_Add Ticket Time Entry for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_list_ticket_conversations(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to return conversations for.")], rows_per_page: Annotated[str, Field(default=None, description="Specify how many ticket conversations should be returned per page for Freshservice pagination.")], start_at_page: Annotated[str, Field(default=None, description="Specify starting from which page ticket conversations should be returned with Freshservice pagination.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many ticket conversations action should return in total.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Freshservice ticket conversations based on the specified search criteria. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if rows_per_page is not None:
                script_params["Rows per Page"] = rows_per_page
            if start_at_page is not None:
                script_params["Start at Page"] = start_at_page
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_List Ticket Conversations",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_List Ticket Conversations",
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
                print(f"Error executing action FreshworksFreshservice_List Ticket Conversations for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_update_ticket_time_entry(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to update a time entry for.")], time_entry_id: Annotated[str, Field(..., description="Specify time entry ID to update.")], agent_email: Annotated[str, Field(default=None, description="Specify agent email for whom to change a ticket time entry.")], note: Annotated[str, Field(default=None, description="Specify a note for the ticket time entry.")], time_spent: Annotated[str, Field(default=None, description="Specify time spent for ticket time entry. Format: {hh:mm}")], billable: Annotated[bool, Field(default=None, description="If enabled, ticket time entry will be marked as billable.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the ticket time entry. Action appends new custom fields to any existing for ticket time entry. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a time entry for a Freshservice ticket. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Time Entry ID"] = time_entry_id
            if agent_email is not None:
                script_params["Agent Email"] = agent_email
            if note is not None:
                script_params["Note"] = note
            if time_spent is not None:
                script_params["Time Spent"] = time_spent
            if billable is not None:
                script_params["Billable"] = billable
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
                actionName="FreshworksFreshservice_Update Ticket Time Entry",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Update Ticket Time Entry",
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
                print(f"Error executing action FreshworksFreshservice_Update Ticket Time Entry for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_update_agent(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], agent_id: Annotated[str, Field(..., description="Specify agent id to update.")], email: Annotated[str, Field(default=None, description="Specify the email of the agent to update.")], first_name: Annotated[str, Field(default=None, description="Specify the first name of the agent to update.")], last_name: Annotated[str, Field(default=None, description="Specify the last name of the agent to update.")], is_occasional: Annotated[bool, Field(default=None, description="If enabled, agent will be updated as an occasional agent, otherwise it will be a full-time agent.")], can_see_all_tickets_from_associated_departments: Annotated[bool, Field(default=None, description="If enabled, agent will be able to see all tickets from Associated departments.")], departments: Annotated[str, Field(default=None, description="Specify department names associated with the agent. Parameter accepts multiple values as a comma separated string.")], location: Annotated[str, Field(default=None, description="Specify location name associated with the agent.")], group_memberships: Annotated[str, Field(default=None, description="Specify group names agent should be a member of.")], roles: Annotated[str, Field(default=None, description="Specify roles to add to agent. Parameter accepts multiple values as a comma separated string. Example: {'role_id':170000XXXXX,'assignment_scope': 'entire_helpdesk'}")], job_title: Annotated[str, Field(default=None, description="Specify agent job title.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the agent. Action appends new custom fields to any existing for an agent. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update existing Freshservice Agent. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Agent ID"] = agent_id
            if email is not None:
                script_params["Email"] = email
            if first_name is not None:
                script_params["First Name"] = first_name
            if last_name is not None:
                script_params["Last Name"] = last_name
            if is_occasional is not None:
                script_params["Is occasional"] = is_occasional
            if can_see_all_tickets_from_associated_departments is not None:
                script_params["Can See All Tickets From Associated Departments"] = can_see_all_tickets_from_associated_departments
            if departments is not None:
                script_params["Departments"] = departments
            if location is not None:
                script_params["Location"] = location
            if group_memberships is not None:
                script_params["Group Memberships"] = group_memberships
            if roles is not None:
                script_params["Roles"] = roles
            if job_title is not None:
                script_params["Job Title"] = job_title
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
                actionName="FreshworksFreshservice_Update Agent",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Update Agent",
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
                print(f"Error executing action FreshworksFreshservice_Update Agent for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Freshservice instance with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
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
                actionName="FreshworksFreshservice_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Ping",
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
                print(f"Error executing action FreshworksFreshservice_Ping for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_create_requester(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], email: Annotated[str, Field(..., description="Specify the email of the requester to create.")], first_name: Annotated[str, Field(..., description="Specify the first name of the requester to create.")], last_name: Annotated[str, Field(default=None, description="Specify the last name of the requester to create.")], can_see_all_tickets_from_associated_departments: Annotated[bool, Field(default=None, description="If enabled, requester will be able to see all tickets from associated departments.")], departments: Annotated[str, Field(default=None, description="Specify department names associated with the requester. Parameter accepts multiple values as a comma separated string.")], location: Annotated[str, Field(default=None, description="Specify location name associated with the requester.")], job_title: Annotated[str, Field(default=None, description="Specify requester job title.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the requester. Action appends new custom fields to any existing for requester. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a new Freshservice requester. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Email"] = email
            script_params["First Name"] = first_name
            if last_name is not None:
                script_params["Last Name"] = last_name
            if can_see_all_tickets_from_associated_departments is not None:
                script_params["Can See All Tickets From Associated Departments"] = can_see_all_tickets_from_associated_departments
            if departments is not None:
                script_params["Departments"] = departments
            if location is not None:
                script_params["Location"] = location
            if job_title is not None:
                script_params["Job Title"] = job_title
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
                actionName="FreshworksFreshservice_Create Requester",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Create Requester",
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
                print(f"Error executing action FreshworksFreshservice_Create Requester for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_deactivate_requester(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], requester_id: Annotated[str, Field(..., description="Specify requester id to deactivate.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Deactivate Freshservice requester. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Requester ID"] = requester_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Deactivate Requester",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Deactivate Requester",
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
                print(f"Error executing action FreshworksFreshservice_Deactivate Requester for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_update_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket id to update.")], status: Annotated[List[str], Field(default=None, description="Specify new status for the ticket.")], subject: Annotated[str, Field(default=None, description="Specify subject field to update.")], description: Annotated[str, Field(default=None, description="Specify description field to update.")], requester_email: Annotated[str, Field(default=None, description="Specify requester email to update.")], agent_assign_to: Annotated[str, Field(default=None, description="Specify the agent email to update.")], group_assign_to: Annotated[str, Field(default=None, description="Specify the group name to update.")], priority: Annotated[List[str], Field(default=None, description="Specify priority to update.")], urgency: Annotated[List[str], Field(default=None, description="Specify urgency to update.")], impact: Annotated[List[str], Field(default=None, description="Specify impact to update.")], tags: Annotated[str, Field(default=None, description="Specify tags to replace in the ticket. Parameter accepts multiple values as a comma separated string. Note that due to the Freshservice API limitations action replaces existing tags in the ticket, not appending new ones to existing.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the ticket. Action appends new custom fields to any existing for a ticket. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], file_attachments_to_add: Annotated[str, Field(default=None, description="Specify the full path for the file to be uploaded with the ticket. Parameter accepts multiple values as a comma separated string. The total size of the attachments must not exceed 15MB")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a Freshservice ticket based on provided action input parameters. Note that if new tags for the ticket are provided, due to the Freshservice API limitations action replaces existing tags in the ticket, not appending new ones to existing. Additionally, if file attachments to add are provided, the total size of the attachments must not exceed 15MB

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if status is not None:
                script_params["Status"] = status
            if subject is not None:
                script_params["Subject"] = subject
            if description is not None:
                script_params["Description"] = description
            if requester_email is not None:
                script_params["Requester Email"] = requester_email
            if agent_assign_to is not None:
                script_params["Agent Assign To"] = agent_assign_to
            if group_assign_to is not None:
                script_params["Group Assign To"] = group_assign_to
            if priority is not None:
                script_params["Priority"] = priority
            if urgency is not None:
                script_params["Urgency"] = urgency
            if impact is not None:
                script_params["Impact"] = impact
            if tags is not None:
                script_params["Tags"] = tags
            if custom_fields is not None:
                script_params["Custom Fields"] = custom_fields
            if file_attachments_to_add is not None:
                script_params["File Attachments to Add"] = file_attachments_to_add
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Update Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Update Ticket",
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
                print(f"Error executing action FreshworksFreshservice_Update Ticket for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_update_requester(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], requester_id: Annotated[str, Field(..., description="Specify requester id to update.")], email: Annotated[str, Field(default=None, description="Specify the email of the requester to update.")], first_name: Annotated[str, Field(default=None, description="Specify the first name of the requester to update.")], last_name: Annotated[str, Field(default=None, description="Specify the last name of the requester to update.")], can_see_all_tickets_from_associated_departments: Annotated[bool, Field(default=None, description="If enabled, requester will be able to see all tickets from associated departments.")], departments: Annotated[str, Field(default=None, description="Specify department names associated with the requester. Parameter accepts multiple values as a comma separated string.")], location: Annotated[str, Field(default=None, description="Specify location name associated with the requester.")], job_title: Annotated[str, Field(default=None, description="Specify requester job title.")], custom_fields: Annotated[str, Field(default=None, description="Specify a JSON object that contains custom fields to add to the requester. Action appends new custom fields to any existing for requester. Example format: {\"key1\":\"value1\",\"key2\":\"value2\"}")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update existing Freshservice Requester. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Requester ID"] = requester_id
            if email is not None:
                script_params["Email"] = email
            if first_name is not None:
                script_params["First Name"] = first_name
            if last_name is not None:
                script_params["Last Name"] = last_name
            if can_see_all_tickets_from_associated_departments is not None:
                script_params["Can See All Tickets From Associated Departments"] = can_see_all_tickets_from_associated_departments
            if departments is not None:
                script_params["Departments"] = departments
            if location is not None:
                script_params["Location"] = location
            if job_title is not None:
                script_params["Job Title"] = job_title
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
                actionName="FreshworksFreshservice_Update Requester",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Update Requester",
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
                print(f"Error executing action FreshworksFreshservice_Update Requester for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def freshworks_freshservice_add_a_ticket_note(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify ticket ID to return conversations for.")], note_text: Annotated[str, Field(..., description="Specify note text to add to ticket.")], note_type: Annotated[List[str], Field(default=None, description="Specify the type of note action should add to the ticket.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a note to a Freshservice ticket. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="FreshworksFreshservice")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for FreshworksFreshservice: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if note_type is not None:
                script_params["Note Type"] = note_type
            script_params["Note Text"] = note_text
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="FreshworksFreshservice_Add a Ticket Note",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "FreshworksFreshservice_Add a Ticket Note",
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
                print(f"Error executing action FreshworksFreshservice_Add a Ticket Note for FreshworksFreshservice: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for FreshworksFreshservice")
            return {"Status": "Failed", "Message": "No active instance found."}
