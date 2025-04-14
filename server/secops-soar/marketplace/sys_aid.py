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
  # This function registers all tools (actions) for the SysAid integration.

  @mcp.tool()
  async def sys_aid_list_service_requests(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      service_request_type: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "The type of the service request to filter by. Valid values:"
                  " incident, request, problem, change, all."
              ),
          ),
      ],
      status: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The status of the request service to filter by.",
          ),
      ],
      priority: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The priority of the request service to filter by.",
          ),
      ],
      assignee: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The assignee of the request service to filter by.",
          ),
      ],
      urgency: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The urgency of the request service to filter by.",
          ),
      ],
      request_user: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The request user of the request service to filter by.",
          ),
      ],
      category: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The category of the request service to filter by.",
          ),
      ],
      subcategory: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The subcategory of the request service to filter by.",
          ),
      ],
      third_category: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The third category of the request service to filter by.",
          ),
      ],
      assigned_group: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The assigned group of the request service to filter by.",
          ),
      ],
      get_archived: Annotated[
          Optional[bool],
          Field(
              default=None,
              description="Whether to get archived request services or not.",
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
    """List service requests.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
      if service_request_type is not None:
        script_params["Service Request Type"] = service_request_type
      if status is not None:
        script_params["Status"] = status
      if priority is not None:
        script_params["Priority"] = priority
      if assignee is not None:
        script_params["Assignee"] = assignee
      if urgency is not None:
        script_params["Urgency"] = urgency
      if request_user is not None:
        script_params["Request User"] = request_user
      if category is not None:
        script_params["Category"] = category
      if subcategory is not None:
        script_params["Subcategory"] = subcategory
      if third_category is not None:
        script_params["Third Category"] = third_category
      if assigned_group is not None:
        script_params["Assigned Group"] = assigned_group
      if get_archived is not None:
        script_params["Get Archived"] = get_archived

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="SysAid_List Service Requests",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "SysAid_List Service Requests"
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
        print(f"Error executing action SysAid_List Service Requests for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_delete_service_request(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      service_request_id: Annotated[
          str, Field(..., description="The ID of the service request to delete.")
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
    """Delete a service request.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
      script_params["Service Request ID"] = service_request_id

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="SysAid_Delete Service Request",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "SysAid_Delete Service Request"
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
        print(f"Error executing action SysAid_Delete Service Request for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_get_service_request(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      service_request_id: Annotated[
          str,
          Field(..., description="The ID of the service request to get info about."),
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
    """Get a service request.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
      script_params["Service Request ID"] = service_request_id

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="SysAid_Get Service Request",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "SysAid_Get Service Request",  # Assuming same as actionName
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
        print(f"Error executing action SysAid_Get Service Request for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_ping(
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
    """Test SysAid connectivity.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
          actionName="SysAid_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "SysAid_Ping",  # Assuming same as actionName
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
        print(f"Error executing action SysAid_Ping for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_update_service_request(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      service_request_id: Annotated[
          str, Field(..., description="The id of the service request to update.")
      ],
      status: Annotated[
          Optional[str],
          Field(default=None, description="The new status of the request service."),
      ],
      priority: Annotated[
          Optional[str],
          Field(default=None, description="The new priority of the request service."),
      ],
      assignee: Annotated[
          Optional[str],
          Field(default=None, description="The new assignee of the request service."),
      ],
      urgency: Annotated[
          Optional[str],
          Field(default=None, description="The new urgency of the request service."),
      ],
      request_user: Annotated[
          Optional[str],
          Field(
              default=None, description="The new request user of the request service."
          ),
      ],
      category: Annotated[
          Optional[str],
          Field(default=None, description="The new category of the request service."),
      ],
      subcategory: Annotated[
          Optional[str],
          Field(
              default=None, description="The new subcategory of the request service."
          ),
      ],
      third_category: Annotated[
          Optional[str],
          Field(
              default=None, description="The new third category of the request service."
          ),
      ],
      assigned_group: Annotated[
          Optional[str],
          Field(
              default=None, description="The new assigned group of the request service."
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
    """Update a service request.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
      script_params["Service Request ID"] = service_request_id
      if status is not None:
        script_params["Status"] = status
      if priority is not None:
        script_params["Priority"] = priority
      if assignee is not None:
        script_params["Assignee"] = assignee
      if urgency is not None:
        script_params["Urgency"] = urgency
      if request_user is not None:
        script_params["Request User"] = request_user
      if category is not None:
        script_params["Category"] = category
      if subcategory is not None:
        script_params["Subcategory"] = subcategory
      if third_category is not None:
        script_params["Third Category"] = third_category
      if assigned_group is not None:
        script_params["Assigned Group"] = assigned_group

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="SysAid_Update Service Request",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "SysAid_Update Service Request"
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
        print(f"Error executing action SysAid_Update Service Request for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_close_service_request(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      service_request_id: Annotated[
          str, Field(..., description="The ID of the service request to delete.")
      ],
      solution: Annotated[
          str, Field(..., description="The solution of the request service.")
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
    """Close a service request.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
      script_params["Service Request ID"] = service_request_id
      script_params["Solution"] = solution

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="SysAid_Close Service Request",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "SysAid_Close Service Request"
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
        print(f"Error executing action SysAid_Close Service Request for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_create_service_request(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      title: Annotated[
          str, Field(..., description="The title of the service request.")
      ],
      description: Annotated[
          str, Field(..., description="The description of the service request.")
      ],
      status: Annotated[
          str, Field(..., description="The status of the request service.")
      ],
      priority: Annotated[
          str, Field(..., description="The priority of the request service.")
      ],
      assignee: Annotated[
          str, Field(..., description="The assignee of the request service.")
      ],
      urgency: Annotated[
          str, Field(..., description="The urgency of the request service.")
      ],
      service_request_type: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "The type of the service request. Valid values: incident, request,"
                  " problem, change, all."
              ),
          ),
      ],
      request_user: Annotated[
          Optional[str],
          Field(default=None, description="The request user of the request service."),
      ],
      category: Annotated[
          Optional[str],
          Field(default=None, description="The category of the request service."),
      ],
      subcategory: Annotated[
          Optional[str],
          Field(default=None, description="The subcategory of the request service."),
      ],
      third_category: Annotated[
          Optional[str],
          Field(default=None, description="The third category of the request service."),
      ],
      assigned_group: Annotated[
          Optional[str],
          Field(default=None, description="The assigned group of the request service."),
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
    """Create a service request.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
      script_params["Title"] = title
      script_params["Description"] = description
      if service_request_type is not None:
        script_params["Service Request Type"] = service_request_type
      script_params["Status"] = status
      script_params["Priority"] = priority
      script_params["Assignee"] = assignee
      script_params["Urgency"] = urgency
      if request_user is not None:
        script_params["Request User"] = request_user
      if category is not None:
        script_params["Category"] = category
      if subcategory is not None:
        script_params["Subcategory"] = subcategory
      if third_category is not None:
        script_params["Third Category"] = third_category
      if assigned_group is not None:
        script_params["Assigned Group"] = assigned_group

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="SysAid_Create Service Request",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "SysAid_Create Service Request"
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
        print(f"Error executing action SysAid_Create Service Request for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def sys_aid_list_users(
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
    """List SysAid users.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SysAid")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for SysAid: {e}")
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
          actionName="SysAid_List Users",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "SysAid_List Users",  # Assuming same as actionName
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
        print(f"Error executing action SysAid_List Users for SysAid: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for SysAid")
      return {"Status": "Failed", "Message": "No active instance found."}
