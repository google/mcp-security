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
  # This function registers all tools (actions) for the TrendMicroDDAN integration.

  @mcp.tool()
  async def trend_micro_ddan_submit_file_url(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      file_ur_ls: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of the URLs that point to the file"
                  " that needs to be analyzed."
              ),
          ),
      ],
      fetch_event_log: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch event logs related to the files."
              ),
          ),
      ],
      fetch_suspicious_objects: Annotated[
          Optional[bool],
          Field(
              default=None,
              description="If enabled, action will fetch suspicious objects.",
          ),
      ],
      fetch_sandbox_screenshot: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will try to fetch a sandbox screenshot related to"
                  " the files."
              ),
          ),
      ],
      resubmit_file: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will not check if there was a submission for this"
                  " file previously."
              ),
          ),
      ],
      max_event_logs_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many event logs to return. Default: 50. Max: 200."
              ),
          ),
      ],
      max_suspicious_objects_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many suspicious objects to return. Default: 50. Max:"
                  " 200."
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
    """Submit a file via URLs in Trend Micro DDAN. Note: Action is running as async, adjust the script timeout value in Chronicle SOAR IDE for action as needed.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TrendMicroDDAN")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TrendMicroDDAN: {e}")
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
      script_params["File URLs"] = file_ur_ls
      if fetch_event_log is not None:
        script_params["Fetch Event Log"] = fetch_event_log
      if fetch_suspicious_objects is not None:
        script_params["Fetch Suspicious Objects"] = fetch_suspicious_objects
      if fetch_sandbox_screenshot is not None:
        script_params["Fetch Sandbox Screenshot"] = fetch_sandbox_screenshot
      if resubmit_file is not None:
        script_params["Resubmit File"] = resubmit_file
      if max_event_logs_to_return is not None:
        script_params["Max Event Logs To Return"] = max_event_logs_to_return
      if max_suspicious_objects_to_return is not None:
        script_params["Max Suspicious Objects To Return"] = (
            max_suspicious_objects_to_return
        )

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TrendMicroDDAN_Submit File URL",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TrendMicroDDAN_Submit File URL"
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
            "Error executing action TrendMicroDDAN_Submit File URL for"
            f" TrendMicroDDAN: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TrendMicroDDAN")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def trend_micro_ddan_ping(
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
    """Test connectivity to Trend Micro DDAN with parameters provided at the integration configuration page on the Marketplace tab.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TrendMicroDDAN")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TrendMicroDDAN: {e}")
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
          actionName="TrendMicroDDAN_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "TrendMicroDDAN_Ping",  # Assuming same as actionName
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
        print(f"Error executing action TrendMicroDDAN_Ping for TrendMicroDDAN: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TrendMicroDDAN")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def trend_micro_ddan_submit_file(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      file_paths: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of the absolute file paths that point"
                  " to the file that needs to be analyzed."
              ),
          ),
      ],
      fetch_event_log: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch event logs related to the files."
              ),
          ),
      ],
      fetch_suspicious_objects: Annotated[
          Optional[bool],
          Field(
              default=None,
              description="If enabled, action will fetch suspicious objects.",
          ),
      ],
      fetch_sandbox_screenshot: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will try to fetch a sandbox screenshot related to"
                  " the files."
              ),
          ),
      ],
      resubmit_file: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will not check if there was a submission for this"
                  " file previously."
              ),
          ),
      ],
      max_event_logs_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many event logs to return. Default: 50. Max: 200."
              ),
          ),
      ],
      max_suspicious_objects_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many suspicious objects to return. Default: 50. Max:"
                  " 200."
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
    """Submit files in Trend Micro DDAN. Note: Action is running as async, adjust the script timeout value in Chronicle SOAR IDE for action as needed.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="TrendMicroDDAN")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TrendMicroDDAN: {e}")
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
      script_params["File Paths"] = file_paths
      if fetch_event_log is not None:
        script_params["Fetch Event Log"] = fetch_event_log
      if fetch_suspicious_objects is not None:
        script_params["Fetch Suspicious Objects"] = fetch_suspicious_objects
      if fetch_sandbox_screenshot is not None:
        script_params["Fetch Sandbox Screenshot"] = fetch_sandbox_screenshot
      if resubmit_file is not None:
        script_params["Resubmit File"] = resubmit_file
      if max_event_logs_to_return is not None:
        script_params["Max Event Logs To Return"] = max_event_logs_to_return
      if max_suspicious_objects_to_return is not None:
        script_params["Max Suspicious Objects To Return"] = (
            max_suspicious_objects_to_return
        )

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TrendMicroDDAN_Submit File",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "TrendMicroDDAN_Submit File",  # Assuming same as actionName
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
            f"Error executing action TrendMicroDDAN_Submit File for TrendMicroDDAN: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TrendMicroDDAN")
      return {"Status": "Failed", "Message": "No active instance found."}
