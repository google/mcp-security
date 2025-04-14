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
  # This function registers all tools (actions) for the Splunk integration.

  @mcp.tool()
  async def splunk_splunk_csv_viewer(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      results: Annotated[str, Field(..., description="Raw results.")],
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
    """Deprecated. This action creates a CSV table based on the raw results.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
      script_params["Results"] = results

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Splunk_SplunkCsvViewer",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Splunk_SplunkCsvViewer",  # Assuming same as actionName
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
        print(f"Error executing action Splunk_SplunkCsvViewer for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def splunk_get_host_events(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      event_per_host_limit: Annotated[
          str, Field(..., description="Specify how many events to return per host.")
      ],
      results_from: Annotated[
          str, Field(..., description="Specify the start time for the events.")
      ],
      results_to: Annotated[
          str, Field(..., description="Specify the end time for the events.")
      ],
      result_fields: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a comma-separated list of fields that need to be returned."
              ),
          ),
      ],
      index: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what index should be used, when searching for events related"
                  " to the host. If nothing is provided, action will not use index."
              ),
          ),
      ],
      host_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used to get information about host"
                  " events. Default: host."
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
    """Get events related to hosts in Splunk.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
      script_params["Event Per Host Limit"] = event_per_host_limit
      script_params["Results From"] = results_from
      script_params["Results To"] = results_to
      if result_fields is not None:
        script_params["Result fields"] = result_fields
      if index is not None:
        script_params["Index"] = index
      if host_key is not None:
        script_params["Host Key"] = host_key

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Splunk_Get Host Events",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Splunk_Get Host Events",  # Assuming same as actionName
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
        print(f"Error executing action Splunk_Get Host Events for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def splunk_update_notable_events(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      notable_event_i_ds: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify IDs of notable events."
                  " Example:1A082D7B-D5A1-4A2B-BB94-41C439BE3EB7@@notable@@cb87390ae72763679d3f6f8f097ebe2b,1D234D5B-1531-2D2B-BB94-41C439BE12B7@@notable@@cb87390ae72763679d3f6f8f097ebe2b"
              ),
          ),
      ],
      status: Annotated[
          Optional[List[Any]],
          Field(default=None, description="Specify the new status for notable events."),
      ],
      urgency: Annotated[
          Optional[List[Any]],
          Field(
              default=None, description="Specify the new urgency for the notable event."
          ),
      ],
      new_owner: Annotated[
          Optional[str],
          Field(
              default=None, description="Specify the new owner of the notable event."
          ),
      ],
      comment: Annotated[
          Optional[str],
          Field(default=None, description="Specify comment for the notable event."),
      ],
      disposition: Annotated[
          Optional[List[Any]],
          Field(
              default=None, description="Specify the disposition for the notable event."
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
    """Update notable events in Splunk ES. Note: This action is only supported for Splunk ES.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
      script_params["Notable Event IDs"] = notable_event_i_ds
      if status is not None:
        script_params["Status"] = status
      if urgency is not None:
        script_params["Urgency"] = urgency
      if new_owner is not None:
        script_params["New Owner"] = new_owner
      if comment is not None:
        script_params["Comment"] = comment
      if disposition is not None:
        script_params["Disposition"] = disposition

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Splunk_Update Notable Events",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "Splunk_Update Notable Events"
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
        print(f"Error executing action Splunk_Update Notable Events for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def splunk_ping(
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
    """Test connectivity to the Splunk with parameters provided at the integration configuration page on the Marketplace tab.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
          actionName="Splunk_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Splunk_Ping",  # Assuming same as actionName
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
        print(f"Error executing action Splunk_Ping for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def splunk_splunk_query(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      query: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the query that needs to be executed. Example:"
                  ' index="_internal". You can provide multiple queries in the same'
                  " action. The format is [\u201cquery 1\u201d, \u201cquery 2\u201d]."
              ),
          ),
      ],
      search_mode: Annotated[
          Optional[List[Any]],
          Field(default=None, description="Specify the mode for search execution."),
      ],
      results_count_limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many results to return. Note: this parameter appends the"
                  " \u201chead\u201d key word to the provided query. Default is 100."
              ),
          ),
      ],
      results_from: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the start time for the query. Default: -24h",
          ),
      ],
      results_to: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the end time for the query. Default: now.",
          ),
      ],
      result_fields: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a comma-separated list of fields that need to be returned."
                  ' Note: this parameter appends "fields" key word to the provided'
                  " query."
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
    """Execute a query in Splunk. Note: Please exclude any quotes that are part of the query string.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
      if search_mode is not None:
        script_params["Search Mode"] = search_mode
      script_params["Query"] = query
      if results_count_limit is not None:
        script_params["Results count limit"] = results_count_limit
      if results_from is not None:
        script_params["Results From"] = results_from
      if results_to is not None:
        script_params["Results To"] = results_to
      if result_fields is not None:
        script_params["Result fields"] = result_fields

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Splunk_SplunkQuery",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Splunk_SplunkQuery",  # Assuming same as actionName
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
        print(f"Error executing action Splunk_SplunkQuery for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def splunk_execute_entity_query(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      query: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the query that needs to be executed without the"
                  ' \u201cWhere\u201d clause.  Example: index="_internal"'
              ),
          ),
      ],
      cross_entity_operator: Annotated[
          List[Any],
          Field(
              ...,
              description=(
                  "Specify what should be the logical operator used between different"
                  " entity types."
              ),
          ),
      ],
      search_mode: Annotated[
          Optional[List[Any]],
          Field(default=None, description="Specify the mode for search execution."),
      ],
      results_count_limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many results to return. Note: this parameter appends the"
                  ' "head" key word to the provided query. Default is 100.'
              ),
          ),
      ],
      results_from: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the start time for the query. Default: -24h",
          ),
      ],
      results_to: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the end time for the query. Default: now.",
          ),
      ],
      result_fields: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a comma-separated list of fields that need to be returned."
                  ' Note: this parameter appends "fields" key word to the provided'
                  " query."
              ),
          ),
      ],
      ip_entity_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used with IP entities. Please refer to"
                  " the action documentation for details."
              ),
          ),
      ],
      hostname_entity_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used with Hostname entities, when"
                  " preparing the. Please refer to the action documentation for"
                  " details."
              ),
          ),
      ],
      file_hash_entity_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used with File Hash entities. Please"
                  " refer to the action documentation for details."
              ),
          ),
      ],
      user_entity_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used with User entities. Please refer to"
                  " the action documentation for details."
              ),
          ),
      ],
      url_entity_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used with URL entities. Please refer to"
                  " the action documentation for details."
              ),
          ),
      ],
      email_address_entity_key: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what key should be used with Email Address entities. Please"
                  " refer to the action documentation for details."
              ),
          ),
      ],
      stop_if_not_enough_entities: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will not start execution, unless all of the"
                  ' entity types are available for the specified ".. Entity Keys".'
                  ' Example: if "IP Entity Key" and "File Hash Entity Key" are'
                  " specified, but in the scope there are no file hashes then if this"
                  " parameter is enabled, action will not execute the query."
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
    """Execute an entity query in Splunk. Note: this action prepares the “Where” clause based on the entities. Check documentation for additional information.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
      if search_mode is not None:
        script_params["Search Mode"] = search_mode
      script_params["Query"] = query
      if results_count_limit is not None:
        script_params["Results count limit"] = results_count_limit
      if results_from is not None:
        script_params["Results from"] = results_from
      if results_to is not None:
        script_params["Results To"] = results_to
      if result_fields is not None:
        script_params["Result fields"] = result_fields
      if ip_entity_key is not None:
        script_params["IP Entity Key"] = ip_entity_key
      if hostname_entity_key is not None:
        script_params["Hostname Entity Key"] = hostname_entity_key
      if file_hash_entity_key is not None:
        script_params["File Hash Entity Key"] = file_hash_entity_key
      if user_entity_key is not None:
        script_params["User Entity Key"] = user_entity_key
      if url_entity_key is not None:
        script_params["URL Entity Key"] = url_entity_key
      if email_address_entity_key is not None:
        script_params["Email Address Entity Key"] = email_address_entity_key
      if stop_if_not_enough_entities is not None:
        script_params["Stop If Not Enough Entities"] = stop_if_not_enough_entities
      script_params["Cross Entity Operator"] = cross_entity_operator

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Splunk_Execute Entity Query",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "Splunk_Execute Entity Query"
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
        print(f"Error executing action Splunk_Execute Entity Query for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def splunk_submit_event(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      index: Annotated[
          str,
          Field(
              ..., description="Specify the index, where the event should be created."
          ),
      ],
      event: Annotated[
          str,
          Field(..., description="Specify the raw event that needs to be submitted."),
      ],
      host: Annotated[
          Optional[str],
          Field(
              default=None, description="Specify the host that is related to the event."
          ),
      ],
      source: Annotated[
          Optional[str],
          Field(
              default=None, description="Specify the source of the event. Example: www."
          ),
      ],
      sourcetype: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the source type of the event. Example: web_event",
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
    """Submit event to Splunk

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Splunk")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Splunk: {e}")
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
      script_params["Index"] = index
      script_params["Event"] = event
      if host is not None:
        script_params["Host"] = host
      if source is not None:
        script_params["Source"] = source
      if sourcetype is not None:
        script_params["Sourcetype"] = sourcetype

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Splunk_Submit Event",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Splunk_Submit Event",  # Assuming same as actionName
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
        print(f"Error executing action Splunk_Submit Event for Splunk: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Splunk")
      return {"Status": "Failed", "Message": "No active instance found."}
