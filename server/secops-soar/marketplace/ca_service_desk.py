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
import json
from typing import Annotated
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import bindings
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from utils.consts import Endpoints
from utils.models import ApiManualActionDataModel
from utils.models import EmailContent
from utils.models import TargetEntity


def register_tools(mcp: FastMCP):
  # This function registers all tools (actions) for the CaServiceDesk integration.

  @mcp.tool()
  async def ca_service_desk_create_ticket(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      summary: Annotated[str, Field(..., description="Incident's summary text")],
      description: Annotated[
          str, Field(..., description="Incident's description text")
      ],
      category_name: Annotated[
          str, Field(..., description="Incident's area name. e.g. Software")
      ],
      group_name: Annotated[str, Field(..., description="Group name. e.g. Test")],
      username: Annotated[str, Field(..., description="User name")],
      custom_fields: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a JSON object containing all of the needed fields and"
                  " values. The structure is the following:"
                  ' {"field\u201d:\u201dvalue"}. If the same field is provided in the'
                  " \u201cCustom Fields\u201c parameter and other parameters, the"
                  " \u201cCustom Fields\u201c  parameter value has priority."
              ),
          ),
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Create new ticket in CA ServiceDesk.

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Summary"] = summary
      script_params["Description"] = description
      script_params["Category Name"] = category_name
      script_params["Group Name"] = group_name
      script_params["Username"] = username
      if custom_fields is not None:
        script_params["Custom Fields"] = custom_fields

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Create Ticket",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Create Ticket"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            f"Error executing action CaServiceDesk_Create Ticket for CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_wait_for_status_change(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ticket_id: Annotated[str, Field(..., description="Target ticket ID.")],
      expected_ticket_status_name: Annotated[
          str, Field(..., description="Expected status.")
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Waiting until ticket status is changed.

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Ticket ID"] = ticket_id
      script_params["Expected Ticket Status Name"] = expected_ticket_status_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Wait For Status Change",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Wait For Status Change"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            "Error executing action CaServiceDesk_Wait For Status Change for"
            f" CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_sync_ticket_history(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      comment_type_field: Annotated[
          Optional[str], Field(default=None, description="Ticket type. e.g. type.sym")
      ],
      analyst_name_field: Annotated[
          Optional[str],
          Field(default=None, description="Analyst Name. e.g. analyst.combo_name"),
      ],
      time_stamp_field: Annotated[
          Optional[str], Field(default=None, description="Time field e.g. time_stamap.")
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Fetch and attach the entire ticket history to an alert

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      if comment_type_field is not None:
        script_params["Comment Type Field"] = comment_type_field
      if analyst_name_field is not None:
        script_params["Analyst Name Field"] = analyst_name_field
      if time_stamp_field is not None:
        script_params["TimeStamp Field"] = time_stamp_field

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Sync Ticket History",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Sync Ticket History"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            "Error executing action CaServiceDesk_Sync Ticket History for"
            f" CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_change_ticket_status(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ticket_id: Annotated[str, Field(..., description="Incident number")],
      status: Annotated[
          str, Field(..., description="Incident status to change. e.g. Closed")
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Change CA Desk Manager ticket status

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Ticket ID"] = ticket_id
      script_params["Status"] = status

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Change Ticket Status",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Change Ticket Status"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            "Error executing action CaServiceDesk_Change Ticket Status for"
            f" CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_ping(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "CaServiceDesk_Ping",  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(f"Error executing action CaServiceDesk_Ping for CaServiceDesk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_add_comment(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ticket_id: Annotated[str, Field(..., description="Incident's ref num. e.g. 338")],
      comment: Annotated[str, Field(..., description="Comment to add to an incident")],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Add comment to a CA ServiceDesk incident

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Ticket ID"] = ticket_id
      script_params["Comment"] = comment

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Add Comment",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "CaServiceDesk_Add Comment",  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            f"Error executing action CaServiceDesk_Add Comment for CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_close_ticket(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ticket_id: Annotated[str, Field(..., description="Incident number")],
      close_reason: Annotated[
          str,
          Field(
              ...,
              description="description which can be used in the Close activity log.",
          ),
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Close incident in CA ServiceDesk manager

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Ticket ID"] = ticket_id
      script_params["Close Reason"] = close_reason

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Close Ticket",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "CaServiceDesk_Close Ticket",  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            f"Error executing action CaServiceDesk_Close Ticket for CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_assign_to_group(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ticket_id: Annotated[str, Field(..., description="Incident number")],
      group: Annotated[str, Field(..., description="Group to assign the incident to")],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Assign an incident to a particular group

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Ticket ID"] = ticket_id
      script_params["Group"] = group

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Assign To Group",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Assign To Group"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            "Error executing action CaServiceDesk_Assign To Group for"
            f" CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_search_tickets(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      incident_id: Annotated[
          Optional[str], Field(default=None, description="Incident ID to filter by")
      ],
      summary: Annotated[
          Optional[str], Field(default=None, description="Summary content to filter by")
      ],
      description: Annotated[
          Optional[str],
          Field(default=None, description="Description content to filter by"),
      ],
      status: Annotated[
          Optional[str], Field(default=None, description="Filter by status. e.g. Open")
      ],
      days_backwards: Annotated[
          Optional[str],
          Field(
              default=None, description="Get results from 'x' days backwards. e.g. 5'"
          ),
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Search tickets in CA Desk Manager by field

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      if incident_id is not None:
        script_params["Incident ID"] = incident_id
      if summary is not None:
        script_params["Summary"] = summary
      if description is not None:
        script_params["Description"] = description
      if status is not None:
        script_params["Status"] = status
      if days_backwards is not None:
        script_params["Days Backwards"] = days_backwards

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Search Tickets",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Search Tickets"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            "Error executing action CaServiceDesk_Search Tickets for"
            f" CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def ca_service_desk_assign_incident_to_user(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ticket_id: Annotated[str, Field(..., description="Incident number")],
      username: Annotated[
          str, Field(..., description="Username to assign the incident to.")
      ],
      target_entities: Annotated[
          List[TargetEntity],
          Field(
              default_factory=list,
              description=(
                  "Optional list of specific target entities (Identifier, EntityType)"
                  " to run the action on."
              ),
          ),
      ],
      scope: Annotated[
          str,
          Field(
              default="All entities", description="Defines the scope for the action."
          ),
      ],
  ) -> dict:
    """Assign an incident to a specific user

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
      final_scope = None  # Scope is ignored when specific entities are given
      is_predefined_scope = False
    else:
      # No specific target entities, use scope parameter
      # Check if the provided scope is valid
      if scope not in bindings.valid_scopes:
        allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
        return {
            "Status": "Failed",
            "Message": (
                f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}"
            ),
        }
      # Scope is valid or validation is not configured
      final_target_entities = []  # Pass empty list for entities when using scope
      final_scope = scope
      is_predefined_scope = True
    # --- End scope/entity logic ---

    # Fetch integration instance identifier (assuming this pattern)
    try:
      instance_response = await bindings.http_client.get(
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="CaServiceDesk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for CaServiceDesk: {e}")
      return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

    if instances:
      instance_identifier = instances[0].get("identifier")
      if not instance_identifier:
        # Log error or handle missing identifier
        return {
            "Status": "Failed",
            "Message": "Instance found but identifier is missing.",
        }

      # Construct parameters dictionary for the API call
      script_params = {}
      script_params["Ticket ID"] = ticket_id
      script_params["Username"] = username

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="CaServiceDesk_Assign Incident To User",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "CaServiceDesk_Assign Incident To User"
              ),  # Assuming same as actionName
              "ScriptParametersEntityFields": json.dumps(script_params),
          },
      )

      # Execute the action via HTTP POST
      try:
        execution_response = await bindings.http_client.post(
            Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
        )
        return execution_response
      except Exception as e:
        # Log error appropriately
        print(
            "Error executing action CaServiceDesk_Assign Incident To User for"
            f" CaServiceDesk: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for CaServiceDesk")
      return {"Status": "Failed", "Message": "No active instance found."}
