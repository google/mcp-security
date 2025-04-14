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
  # This function registers all tools (actions) for the NozomiNetworks integration.

  @mcp.tool()
  async def nozomi_networks_run_a_cli_command(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      cli_command: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a CLI Command to execute on Nozomi Networks device.  Note:"
                  " Nozomi API doesnt provide a validation for executed CLI commands,"
                  " its up to the User to make sure that the provided CLI command is"
                  " correct."
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
    """Run a CLI command on Nozomi Networks device. Note: Nozomi API doesnt provide a validation for executed CLI commands, its up to the User to make sure that the provided CLI command is correct. Note2: Action is not working with Siemplify Entities.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="NozomiNetworks")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for NozomiNetworks: {e}")
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
      script_params["CLI Command"] = cli_command

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="NozomiNetworks_Run a CLI Command",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "NozomiNetworks_Run a CLI Command"
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
            "Error executing action NozomiNetworks_Run a CLI Command for"
            f" NozomiNetworks: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for NozomiNetworks")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def nozomi_networks_run_a_query(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      query: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a query to execute on Nozomi Networks device, for example:"
                  " alerts | head 10"
              ),
          ),
      ],
      record_limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Can be used to specify how many records can be returned by the"
                  " action. If default value of 10 is set, parameter adds \u201c| head"
                  " 10\u201d to the final query to limit the number of returned"
                  " records. If nothing is provided for the parameter - all query"
                  " results are returned. Negative values are ignored."
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
    """Run a query on Nozomi Networks device. Note: Action is not working with Siemplify Entities.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="NozomiNetworks")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for NozomiNetworks: {e}")
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
      if record_limit is not None:
        script_params["Record Limit"] = record_limit

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="NozomiNetworks_Run a Query",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "NozomiNetworks_Run a Query",  # Assuming same as actionName
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
            f"Error executing action NozomiNetworks_Run a Query for NozomiNetworks: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for NozomiNetworks")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def nozomi_networks_list_vulnerabilities(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      record_limit: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Can be used to specify how many records can be returned by the"
                  " action."
              ),
          ),
      ],
      ip_address: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "List vulnerabilities for the provided ip address. Parameter accepts"
                  " multiple values as a comma separated string."
              ),
          ),
      ],
      cve_score: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Minimum CVE score vulnerability should have to be listed, score can"
                  " be a number from 0 to 10."
              ),
          ),
      ],
      vulnerability_name_contains: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a string that vulnerability name should contain to be"
                  " listed."
              ),
          ),
      ],
      cve_id: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "If you know specific CVE to look for, provide the related id in this"
                  " field, for example, CVE-2020-1207. Parameter accepts multiple"
                  " values as a comma separated string."
              ),
          ),
      ],
      include_vulnerabilities_that_marked_as_resolved: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "Specify whether action should also return vulnerabilities that are"
                  " marked as resolved."
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
    """List vulnerabilities discovered by Nozomi device based on the provided action input parameters.  Note: Action is not working with Siemplify entities, only with action input parameters.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="NozomiNetworks")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for NozomiNetworks: {e}")
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
      if ip_address is not None:
        script_params["IP Address"] = ip_address
      if cve_score is not None:
        script_params["CVE Score"] = cve_score
      if vulnerability_name_contains is not None:
        script_params["Vulnerability Name Contains"] = vulnerability_name_contains
      if cve_id is not None:
        script_params["CVE ID"] = cve_id
      script_params["Record Limit"] = record_limit
      if include_vulnerabilities_that_marked_as_resolved is not None:
        script_params["Include vulnerabilities that marked as resolved?"] = (
            include_vulnerabilities_that_marked_as_resolved
        )

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="NozomiNetworks_List Vulnerabilities",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "NozomiNetworks_List Vulnerabilities"
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
            "Error executing action NozomiNetworks_List Vulnerabilities for"
            f" NozomiNetworks: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for NozomiNetworks")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def nozomi_networks_ping(
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
    """Test connectivity to the Nozomi Networks instance with parameters provided at the integration configuration page on the Marketplace tab.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="NozomiNetworks")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for NozomiNetworks: {e}")
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
          actionName="NozomiNetworks_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "NozomiNetworks_Ping",  # Assuming same as actionName
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
        print(f"Error executing action NozomiNetworks_Ping for NozomiNetworks: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for NozomiNetworks")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def nozomi_networks_enrich_entities(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      additional_fields_to_add_to_enrichment: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Comma separated list of fields that should be additionally taken"
                  " from Nodes query to add to fields that are used for enrichment by"
                  " default."
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
    """Enrich Siemplify Host or IP entities based on the information from the Nozomi Networks device.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="NozomiNetworks")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for NozomiNetworks: {e}")
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
      if additional_fields_to_add_to_enrichment is not None:
        script_params["Additional fields to add to enrichment"] = (
            additional_fields_to_add_to_enrichment
        )

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="NozomiNetworks_Enrich Entities",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "NozomiNetworks_Enrich Entities"
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
            "Error executing action NozomiNetworks_Enrich Entities for"
            f" NozomiNetworks: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for NozomiNetworks")
      return {"Status": "Failed", "Message": "No active instance found."}
