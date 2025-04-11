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
import bindings
from mcp.server.fastmcp import FastMCP
from utils.consts import Endpoints
from utils.models import ApiManualActionDataModel, EmailContent, TargetEntity
import json
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the Zendesk integration.

    @mcp.tool()
    async def zendesk_create_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], subject: Annotated[str, Field(..., description="")], description: Annotated[str, Field(..., description="")], assigned_user: Annotated[Optional[str], Field(default=None, description="User full name.")], assignment_group: Annotated[Optional[str], Field(default=None, description="Group name.")], priority: Annotated[Optional[str], Field(default=None, description="Priority will be one of the following: urgent, high, normal or low.")], ticket_type: Annotated[Optional[str], Field(default=None, description="The ticket type will be one of the following: problem, incident, question or task.")], tag: Annotated[Optional[str], Field(default=None, description="")], internal_note: Annotated[Optional[bool], Field(default=None, description="Specify whether the comment should be public, or internal. Unchecked means it will be public, checked means it will be private.")], email_c_cs: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of email addresses, which should also receive the notification of the ticket creation. Note: at max 48 email CCs can be added. This is Zendesk limitation.")], validate_email_c_cs: Annotated[Optional[bool], Field(default=None, description="If enabled, action will try to check that users with emails provided in \u201cEmail CCs\u201c parameter exist. If at least one user doesn\u2019t exist, action will fail. If this parameter is disabled, action will not perform this check.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a ticket with specific properties

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Subject"] = subject
            script_params["Description"] = description
            if assigned_user is not None:
                script_params["Assigned User"] = assigned_user
            if assignment_group is not None:
                script_params["Assignment Group"] = assignment_group
            if priority is not None:
                script_params["Priority"] = priority
            if ticket_type is not None:
                script_params["Ticket Type"] = ticket_type
            if tag is not None:
                script_params["Tag"] = tag
            if internal_note is not None:
                script_params["Internal Note"] = internal_note
            if email_c_cs is not None:
                script_params["Email CCs"] = email_c_cs
            if validate_email_c_cs is not None:
                script_params["Validate Email CCs"] = validate_email_c_cs

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Create Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Create Ticket", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Create Ticket for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zendesk_get_ticket_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="The ID f the ticket.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get ticket details, comments, and attachments by ticket id

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Ticket ID"] = ticket_id

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Get Ticket Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Get Ticket Details", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Get Ticket Details for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zendesk_add_comment_to_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Specify the Zendesk Ticket ID for which you would like to add a comment.")], comment_body: Annotated[str, Field(..., description="Provide the text you would like to be contained in the comment body")], internal_note: Annotated[bool, Field(..., description="Specify whether the comment should be public, or internal. Unchecked means it will be public, checked means it will be private.")], author_name: Annotated[Optional[str], Field(default=None, description="Specify the name of the author, please make sure this name exists on Zendesk")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to an existing ticket

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Comment Body"] = comment_body
            if author_name is not None:
                script_params["Author Name"] = author_name
            script_params["Internal Note"] = internal_note

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Add Comment To Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Add Comment To Ticket", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Add Comment To Ticket for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zendesk_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Ping", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Ping for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zendesk_apply_macros_on_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Ticket number.")], macro_title: Annotated[str, Field(..., description="")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Apply macro to a ticket

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            script_params["Macro Title"] = macro_title

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Apply Macros On Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Apply Macros On Ticket", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Apply Macros On Ticket for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zendesk_update_ticket(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], ticket_id: Annotated[str, Field(..., description="Ticket number.")], subject: Annotated[Optional[str], Field(default=None, description="The subject of the ticket.")], assigned_user: Annotated[Optional[str], Field(default=None, description="User full name.")], assignment_group: Annotated[Optional[str], Field(default=None, description="Group name.")], priority: Annotated[Optional[str], Field(default=None, description="Priority will be one of the following: urgent, high, normal or low.")], ticket_type: Annotated[Optional[str], Field(default=None, description="The ticket type will be one of the following: problem, incident, question or task.")], tag: Annotated[Optional[str], Field(default=None, description="Tag to add to the ticket.")], status: Annotated[Optional[str], Field(default=None, description="The status will be one of the following: new, open, pending, hold, solved or closed.")], internal_note: Annotated[Optional[bool], Field(default=None, description="Specify whether the comment should be public, or internal. Unchecked means it will be public, checked means it will be private.")], additional_comment: Annotated[Optional[str], Field(default=None, description="If you want to add a comment to the ticket, specify the text you would like to add as a comment here.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update existing ticket details

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Ticket ID"] = ticket_id
            if subject is not None:
                script_params["Subject"] = subject
            if assigned_user is not None:
                script_params["Assigned User"] = assigned_user
            if assignment_group is not None:
                script_params["Assignment Group"] = assignment_group
            if priority is not None:
                script_params["Priority"] = priority
            if ticket_type is not None:
                script_params["Ticket Type"] = ticket_type
            if tag is not None:
                script_params["Tag"] = tag
            if status is not None:
                script_params["Status"] = status
            if internal_note is not None:
                script_params["Internal Note"] = internal_note
            if additional_comment is not None:
                script_params["Additional Comment"] = additional_comment

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Update Ticket",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Update Ticket", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Update Ticket for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def zendesk_search_tickets(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], search_query: Annotated[str, Field(..., description="Query content(e.g: type:ticket status:pending).")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search tickets by keyword

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        # --- Determine scope and target entities for API call ---
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None

        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---

        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Zendesk")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for Zendesk: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}

            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Search Query"] = search_query

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="Zendesk_Search Tickets",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Zendesk_Search Tickets", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )

            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action Zendesk_Search Tickets for Zendesk: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Zendesk")
            return {"Status": "Failed", "Message": "No active instance found."}
