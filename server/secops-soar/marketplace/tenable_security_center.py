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
  # This function registers all tools (actions) for the TenableSecurityCenter integration.

  @mcp.tool()
  async def tenable_security_center_get_report(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      report_id: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Report ID number.Can be found at the report URL.",
          ),
      ],
      report_name: Annotated[
          Optional[str],
          Field(
              default=None,
              description="The name of the report, as mentioned at the GUI.",
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
    """Get report content by ID or name.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      if report_id is not None:
        script_params["Report ID"] = report_id
      if report_name is not None:
        script_params["Report Name"] = report_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Get Report",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Get Report"
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
            "Error executing action TenableSecurityCenter_Get Report for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_get_related_assets(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      repository_name: Annotated[str, Field(..., description="The repository name.")],
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
    """Get assets that are related to an IP address

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Repository Name"] = repository_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Get Related Assets",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Get Related Assets"
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
            "Error executing action TenableSecurityCenter_Get Related Assets for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_get_scan_results(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      scan_result_id: Annotated[str, Field(..., description="The scan results ID.")],
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
    """Wait for scan to complete and get results of the scan

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Scan Result ID"] = scan_result_id

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Get Scan Results",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Get Scan Results"
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
            "Error executing action TenableSecurityCenter_Get Scan Results for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_get_vulnerabilities_for_ip(
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
    """Get vulnerabilities and severity summary for an IP address

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
          actionName="TenableSecurityCenter_Get Vulnerabilities for IP",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Get Vulnerabilities for IP"
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
            "Error executing action TenableSecurityCenter_Get Vulnerabilities for IP"
            f" for TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_create_ip_list_asset(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      name: Annotated[
          str, Field(..., description="Specify the name for the IP list asset.")
      ],
      description: Annotated[
          Optional[str],
          Field(
              default=None, description="Specify the description of the IP list asset."
          ),
      ],
      tag: Annotated[
          Optional[str],
          Field(default=None, description="Specify the tag of the IP list asset."),
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
    """Create an IP list asset in Tenable.sc. Requires at least 1 IP entity for successful execution.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Name"] = name
      if description is not None:
        script_params["Description"] = description
      if tag is not None:
        script_params["Tag"] = tag

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Create IP List Asset",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Create IP List Asset"
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
            "Error executing action TenableSecurityCenter_Create IP List Asset for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_enrich_ip(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      repository_name: Annotated[str, Field(..., description="The repository name.")],
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
    """Get information about IP addresses and enrich them

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Repository Name"] = repository_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Enrich IP",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Enrich IP"
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
            "Error executing action TenableSecurityCenter_Enrich IP for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_ping(
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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
          actionName="TenableSecurityCenter_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "TenableSecurityCenter_Ping",  # Assuming same as actionName
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
            "Error executing action TenableSecurityCenter_Ping for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_run_asset_scan(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      scan_name: Annotated[
          str, Field(..., description="Specify the name for the scan.")
      ],
      asset_name: Annotated[
          str,
          Field(
              ..., description="Specify the name of the asset that should be scanned."
          ),
      ],
      policy_id: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the id of the policy that should be used in the scan."
              ),
          ),
      ],
      repository_id: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the id of the repository that should be used in the scan."
              ),
          ),
      ],
      description: Annotated[
          Optional[str],
          Field(default=None, description="Specify the description for the scan."),
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
    """Execute Asset Scan in Tenable.sc.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Scan Name"] = scan_name
      script_params["Asset Name"] = asset_name
      script_params["Policy ID"] = policy_id
      script_params["Repository ID"] = repository_id
      if description is not None:
        script_params["Description"] = description

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Run Asset Scan",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Run Asset Scan"
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
            "Error executing action TenableSecurityCenter_Run Asset Scan for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_scan_ips(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      scan_name: Annotated[
          str, Field(..., description="The name of the scan to create.")
      ],
      policy_name: Annotated[str, Field(..., description="The name of the policy.")],
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
    """Initiate a scan of IP addresses

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Scan Name"] = scan_name
      script_params["Policy Name"] = policy_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Scan Ips",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Scan Ips"
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
            "Error executing action TenableSecurityCenter_Scan Ips for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def tenable_security_center_add_ip_to_ip_list_asset(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      asset_name: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the name of the IP list asset to which you want to add new"
                  " IPs."
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
    """Add an IP to IP list asset in Tenable.sc.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(
              INTEGRATION_NAME="TenableSecurityCenter"
          )
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for TenableSecurityCenter: {e}")
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
      script_params["Asset Name"] = asset_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="TenableSecurityCenter_Add IP To IP List Asset",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "TenableSecurityCenter_Add IP To IP List Asset"
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
            "Error executing action TenableSecurityCenter_Add IP To IP List Asset for"
            f" TenableSecurityCenter: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for TenableSecurityCenter")
      return {"Status": "Failed", "Message": "No active instance found."}
