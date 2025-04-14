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
  # This function registers all tools (actions) for the McAfeeESM integration.

  @mcp.tool()
  async def mc_afee_esm_send_advanced_query_to_esm(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      query_payload: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the JSON object that would need to be executed. Note: action"
                  " will at max return only 200 results."
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
    """Send an advanced query to ESM. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed. Please refer to the documentation portal for more information.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
      script_params["Query Payload"] = query_payload

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="McAfeeESM_Send Advanced Query To ESM",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "McAfeeESM_Send Advanced Query To ESM"
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
            "Error executing action McAfeeESM_Send Advanced Query To ESM for"
            f" McAfeeESM: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def mc_afee_esm_add_values_to_watchlist(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      watchlist_name: Annotated[
          str,
          Field(
              ...,
              description="Specify the name of the watchlist that needs to be updated.",
          ),
      ],
      values_to_add: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of values that need to be added to a"
                  " watchlist."
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
    """Add values to a watchlist in McAfee ESM. Note: McAfee ESM will allow values of the invalid type to be passed, for example, API will not raise error adding hash to the IP watchlist. Please pay attention to the input.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
      script_params["Watchlist Name"] = watchlist_name
      script_params["Values to Add"] = values_to_add

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="McAfeeESM_Add Values To Watchlist",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "McAfeeESM_Add Values To Watchlist"
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
            "Error executing action McAfeeESM_Add Values To Watchlist for"
            f" McAfeeESM: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def mc_afee_esm_send_query_to_esm(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      time_range: Annotated[
          List[Any],
          Field(
              ...,
              description=(
                  'Specify a time frame for the results. If "Custom" is selected, you'
                  ' also need to provide "Start Time".'
              ),
          ),
      ],
      filter_field_name: Annotated[
          str,
          Field(
              ..., description="Specify the field name that will be used for filtering."
          ),
      ],
      filter_operator: Annotated[
          List[Any],
          Field(
              ..., description="Specify the operator that should be used in the filter."
          ),
      ],
      filter_values: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of values that will be used in the"
                  " filter."
              ),
          ),
      ],
      start_time: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify the start time for the results. This parameter is mandatory,"
                  ' if "Custom" is selected for the "Time Frame" parameter. Format: ISO'
                  " 8601"
              ),
          ),
      ],
      end_time: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify the end time for the results. Format: ISO 8601. If nothing"
                  ' is provided and "Custom" is selected for the "Time Frame" parameter'
                  " then this parameter will use current time."
              ),
          ),
      ],
      fields_to_fetch: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a comma-separated list of fields that should be returned. If"
                  " nothing is provided, action will use the predefined fields."
              ),
          ),
      ],
      sort_field: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what parameter should be used for sorting. Note: this"
                  " parameter expects the field in the format {table}.{key name}. If"
                  " the parameter is provided in another format, action will skip it."
                  " Example: Alert.LastTime."
              ),
          ),
      ],
      sort_order: Annotated[
          Optional[List[Any]],
          Field(default=None, description="Specify the order of sorting."),
      ],
      query_type: Annotated[
          Optional[List[Any]],
          Field(default=None, description="Specify what needs to be queried."),
      ],
      max_results_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many results to return. Default: 50. Maximum: 200."
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
    """Send a query to ESM. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
      script_params["Time Range"] = time_range
      if start_time is not None:
        script_params["Start Time"] = start_time
      if end_time is not None:
        script_params["End Time"] = end_time
      script_params["Filter Field Name"] = filter_field_name
      script_params["Filter Operator"] = filter_operator
      script_params["Filter Values"] = filter_values
      if fields_to_fetch is not None:
        script_params["Fields To Fetch"] = fields_to_fetch
      if sort_field is not None:
        script_params["Sort Field"] = sort_field
      if sort_order is not None:
        script_params["Sort Order"] = sort_order
      if query_type is not None:
        script_params["Query Type"] = query_type
      if max_results_to_return is not None:
        script_params["Max Results To Return"] = max_results_to_return

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="McAfeeESM_Send Query To ESM",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "McAfeeESM_Send Query To ESM"
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
        print(f"Error executing action McAfeeESM_Send Query To ESM for McAfeeESM: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def mc_afee_esm_remove_values_from_watchlist(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      watchlist_name: Annotated[
          str,
          Field(
              ...,
              description="Specify the name of the watchlist that needs to be updated.",
          ),
      ],
      values_to_remove: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of values that need to be removed"
                  " from a watchlist."
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
    """Remove values from a watchlist in McAfee ESM.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
      script_params["Watchlist Name"] = watchlist_name
      script_params["Values to Remove"] = values_to_remove

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="McAfeeESM_Remove Values From Watchlist",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "McAfeeESM_Remove Values From Watchlist"
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
            "Error executing action McAfeeESM_Remove Values From Watchlist for"
            f" McAfeeESM: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def mc_afee_esm_send_entity_query_to_esm(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      ip_address_entity_key: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the key that will be used with the IP Address entity during"
                  " filtering. Note: if invalid key is provided, the action will still"
                  " return results, but they will be unexpected."
              ),
          ),
      ],
      hostname_entity_key: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the key that will be used with the Hostname entity during"
                  " filtering. Note: if invalid key is provided, the action will still"
                  " return results, but they will be unexpected."
              ),
          ),
      ],
      time_range: Annotated[
          List[Any],
          Field(
              ...,
              description=(
                  'Specify a time frame for the results. If "Custom" is selected, you'
                  ' also need to provide "Start Time".'
              ),
          ),
      ],
      filter_field_name: Annotated[
          str,
          Field(
              ..., description="Specify the field name that will be used for filtering."
          ),
      ],
      filter_operator: Annotated[
          List[Any],
          Field(
              ..., description="Specify the operator that should be used in the filter."
          ),
      ],
      filter_values: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of values that will be used in the"
                  " filter."
              ),
          ),
      ],
      start_time: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify the start time for the results. This parameter is mandatory,"
                  ' if "Custom" is selected for the "Time Frame" parameter. Format: ISO'
                  " 8601"
              ),
          ),
      ],
      end_time: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify the end time for the results. Format: ISO 8601. If nothing"
                  ' is provided and "Custom" is selected for the "Time Frame" parameter'
                  " then this parameter will use current time."
              ),
          ),
      ],
      fields_to_fetch: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a comma-separated list of fields that should be returned. If"
                  " nothing is provided, action will use the predefined fields."
              ),
          ),
      ],
      sort_field: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what parameter should be used for sorting. Note: this"
                  " parameter expects the field in the format {table}.{key name}. If"
                  " the parameter is provided in another format, action will skip it."
                  " Example: Alert.LastTime."
              ),
          ),
      ],
      sort_order: Annotated[
          Optional[List[Any]],
          Field(default=None, description="Specify the order of sorting."),
      ],
      max_results_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many results to return. Default: 50. Maximum: 200."
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
    """Send a query to ESM based on entities. Supported entities: IP Address, Hostname. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
      script_params["IP Address Entity Key"] = ip_address_entity_key
      script_params["Hostname Entity Key"] = hostname_entity_key
      script_params["Time Range"] = time_range
      if start_time is not None:
        script_params["Start Time"] = start_time
      if end_time is not None:
        script_params["End Time"] = end_time
      script_params["Filter Field Name"] = filter_field_name
      script_params["Filter Operator"] = filter_operator
      script_params["Filter Values"] = filter_values
      if fields_to_fetch is not None:
        script_params["Fields To Fetch"] = fields_to_fetch
      if sort_field is not None:
        script_params["Sort Field"] = sort_field
      if sort_order is not None:
        script_params["Sort Order"] = sort_order
      if max_results_to_return is not None:
        script_params["Max Results To Return"] = max_results_to_return

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="McAfeeESM_Send Entity Query To ESM",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "McAfeeESM_Send Entity Query To ESM"
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
            "Error executing action McAfeeESM_Send Entity Query To ESM for"
            f" McAfeeESM: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def mc_afee_esm_ping(
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
    """Test connectivity to McAfee ESM with parameters provided at the integration configuration page on the Marketplace tab.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
          actionName="McAfeeESM_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "McAfeeESM_Ping",  # Assuming same as actionName
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
        print(f"Error executing action McAfeeESM_Ping for McAfeeESM: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def mc_afee_esm_get_similar_events(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      hours_back: Annotated[
          str, Field(..., description="Specify how many hours backwards to search.")
      ],
      ips_id: Annotated[
          Optional[str],
          Field(default=None, description="Specify the IP SID for the search."),
      ],
      result_limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify how many results to return. Max: 200 per entity.",
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
    """Get events related to the entities in McAfee ESM. Supported entities: Hostname, IP Address, User. Note: Action is running as async, please adjust script timeout value in Chronicle SOAR IDE for action as needed.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="McAfeeESM")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for McAfeeESM: {e}")
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
      script_params["Hours Back"] = hours_back
      if ips_id is not None:
        script_params["IPS ID"] = ips_id
      if result_limit is not None:
        script_params["Result Limit"] = result_limit

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="McAfeeESM_Get Similar Events",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "McAfeeESM_Get Similar Events"
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
        print(f"Error executing action McAfeeESM_Get Similar Events for McAfeeESM: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for McAfeeESM")
      return {"Status": "Failed", "Message": "No active instance found."}
