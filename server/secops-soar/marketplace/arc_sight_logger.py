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
  # This function registers all tools (actions) for the ArcSightLogger integration.

  @mcp.tool()
  async def arc_sight_logger_send_query(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      query: Annotated[
          str,
          Field(
              ...,
              description="Specify the query to send to ArcSight Logger event search.",
          ),
      ],
      max_events_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify the amount of events to return. Limit is 10000. This is"
                  " ArcSight Logger limitation."
              ),
          ),
      ],
      time_frame: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify the time frame which will be used to fetch events."
                  " \nPossible values:\n1m - 1 minute ago\n1h - 1 hour ago\n1d - 1 day"
                  " ago\nNote: You can\u2019t combine different values, like 1d2h30m."
              ),
          ),
      ],
      fields_to_fetch: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what fields to fetch from ArcSight Logger. If nothing is"
                  " specified, then all of the available fields will be returned."
              ),
          ),
      ],
      include_raw_event_data: Annotated[
          Optional[bool],
          Field(
              default=None,
              description="If enabled, raw event data is included in the response.",
          ),
      ],
      local_search_only: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "Indicates that ArcSight Logger event search is local only, and does"
                  " not include ArcSight Logger peers. Set to false if you want to"
                  " include peers in the event search."
              ),
          ),
      ],
      discover_fields: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "Indicates that the ArcSight Logger search should try to discover"
                  " fields in the events found."
              ),
          ),
      ],
      sort: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what sorting method to use.\nPossible"
                  " values:\nascending\ndescending"
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
    """Send a query to get information about related events from ArcSight Logger event log manager.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ArcSightLogger")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for ArcSightLogger: {e}")
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
      script_params["Query"] = query
      if max_events_to_return is not None:
        script_params["Max Events to Return"] = max_events_to_return
      if time_frame is not None:
        script_params["Time Frame"] = time_frame
      if fields_to_fetch is not None:
        script_params["Fields to Fetch"] = fields_to_fetch
      if include_raw_event_data is not None:
        script_params["Include Raw Event Data"] = include_raw_event_data
      if local_search_only is not None:
        script_params["Local Search Only"] = local_search_only
      if discover_fields is not None:
        script_params["Discover Fields"] = discover_fields
      if sort is not None:
        script_params["Sort"] = sort

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="ArcSightLogger_Send Query",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "ArcSightLogger_Send Query",  # Assuming same as actionName
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
            f"Error executing action ArcSightLogger_Send Query for ArcSightLogger: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for ArcSightLogger")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def arc_sight_logger_ping(
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
    """Test connectivity to ArcSight Logger with parameters provided at the integration configuration page on Marketplace tab.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ArcSightLogger")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for ArcSightLogger: {e}")
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
          actionName="ArcSightLogger_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "ArcSightLogger_Ping",  # Assuming same as actionName
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
        print(f"Error executing action ArcSightLogger_Ping for ArcSightLogger: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for ArcSightLogger")
      return {"Status": "Failed", "Message": "No active instance found."}
