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
  # This function registers all tools (actions) for the RSAArcher integration.

  @mcp.tool()
  async def rsa_archer_add_incident_journal_entry(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      destination_content_id: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a content id of the security incident to which you want to"
                  " add journal entry."
              ),
          ),
      ],
      text: Annotated[
          str, Field(..., description="Specify the text for the journal entry.")
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
    """Add a journal entry to the Security Incident in RSA Archer.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="RSAArcher")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for RSAArcher: {e}")
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
      script_params["Destination Content ID"] = destination_content_id
      script_params["Text"] = text

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="RSAArcher_Add Incident Journal Entry",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "RSAArcher_Add Incident Journal Entry"
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
            "Error executing action RSAArcher_Add Incident Journal Entry for"
            f" RSAArcher: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for RSAArcher")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def rsa_archer_update_incident(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      content_id: Annotated[
          str, Field(..., description="Content Id of the incident to update.")
      ],
      application_name: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify an application name for the incident. Default: Incidents."
              ),
          ),
      ],
      incident_summary: Annotated[
          Optional[str],
          Field(default=None, description="The new summary of the incident."),
      ],
      incident_details: Annotated[
          Optional[str],
          Field(
              default=None, description="The new details (decsription) of the incident."
          ),
      ],
      incident_owner: Annotated[
          Optional[str],
          Field(default=None, description="The new owner of the incident."),
      ],
      incident_status: Annotated[
          Optional[str],
          Field(default=None, description="The new status of the incident."),
      ],
      priority: Annotated[
          Optional[str],
          Field(default=None, description="The new priority of the incident."),
      ],
      category: Annotated[
          Optional[str],
          Field(default=None, description="The new category of the incident."),
      ],
      custom_fields: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a JSON object of fields that need to be updated. Example:"
                  " {\u201cCategory\u201d:\u201cMalware\u201d}."
              ),
          ),
      ],
      custom_mapping_file: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify an absolute path to the file that contains all of the"
                  " required mapping. If \u201cRemote File\u201c is enabled, then"
                  " provide a URL that contains the mapping file. Please refer to"
                  " action documentation for the additional information."
              ),
          ),
      ],
      remote_file: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will treat value provided in \u201cCustom Mapping"
                  " File\u201c as a URL and try to fetch a file from it."
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
    """Update an incident

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="RSAArcher")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for RSAArcher: {e}")
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
      script_params["Content ID"] = content_id
      if application_name is not None:
        script_params["Application Name"] = application_name
      if incident_summary is not None:
        script_params["Incident Summary"] = incident_summary
      if incident_details is not None:
        script_params["Incident Details"] = incident_details
      if incident_owner is not None:
        script_params["Incident Owner"] = incident_owner
      if incident_status is not None:
        script_params["Incident Status"] = incident_status
      if priority is not None:
        script_params["Priority"] = priority
      if category is not None:
        script_params["Category"] = category
      if custom_fields is not None:
        script_params["Custom Fields"] = custom_fields
      if custom_mapping_file is not None:
        script_params["Custom Mapping File"] = custom_mapping_file
      if remote_file is not None:
        script_params["Remote File"] = remote_file

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="RSAArcher_Update Incident",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "RSAArcher_Update Incident",  # Assuming same as actionName
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
        print(f"Error executing action RSAArcher_Update Incident for RSAArcher: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for RSAArcher")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def rsa_archer_ping(
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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="RSAArcher")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for RSAArcher: {e}")
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
          actionName="RSAArcher_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "RSAArcher_Ping",  # Assuming same as actionName
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
        print(f"Error executing action RSAArcher_Ping for RSAArcher: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for RSAArcher")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def rsa_archer_get_incident_details(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      content_id: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify ID of the content for which you want to retrieve details."
              ),
          ),
      ],
      application_name: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify an application name for the incident. Default: Incidents."
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
    """Retrieve information about the incident from RSA Archer.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="RSAArcher")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for RSAArcher: {e}")
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
      script_params["Content ID"] = content_id
      if application_name is not None:
        script_params["Application Name"] = application_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="RSAArcher_Get Incident Details",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "RSAArcher_Get Incident Details"
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
            f"Error executing action RSAArcher_Get Incident Details for RSAArcher: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for RSAArcher")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def rsa_archer_create_incident(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      incident_summary: Annotated[
          Optional[str],
          Field(default=None, description="The summary of the new incident."),
      ],
      application_name: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify an application name for the incident. Default: Incidents."
              ),
          ),
      ],
      incident_details: Annotated[
          Optional[str],
          Field(
              default=None, description="The details (description) of the new incident."
          ),
      ],
      incident_owner: Annotated[
          Optional[str],
          Field(default=None, description="The owner of the new incident."),
      ],
      incident_status: Annotated[
          Optional[str],
          Field(default=None, description="The status of the new incident."),
      ],
      priority: Annotated[
          Optional[str],
          Field(default=None, description="The priority of the new incident."),
      ],
      category: Annotated[
          Optional[str],
          Field(default=None, description="The category of the new incident."),
      ],
      custom_fields: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify a JSON object of fields that need to be used, when creating"
                  " an incident . Example: {\u201cCategory\u201d:\u201cMalware\u201d}."
              ),
          ),
      ],
      custom_mapping_file: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify an absolute path to the file that contains all of the"
                  " required mapping. If \u201cRemote File\u201c is enabled, then"
                  " provide a URL that contains the mapping file. Please refer to"
                  " action documentation for the additional information."
              ),
          ),
      ],
      remote_file: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will treat value provided in \u201cCustom Mapping"
                  " File\u201c as a URL and try to fetch a file from it."
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
    """Create a new incident

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="RSAArcher")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for RSAArcher: {e}")
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
      if incident_summary is not None:
        script_params["Incident Summary"] = incident_summary
      if application_name is not None:
        script_params["Application Name"] = application_name
      if incident_details is not None:
        script_params["Incident Details"] = incident_details
      if incident_owner is not None:
        script_params["Incident Owner"] = incident_owner
      if incident_status is not None:
        script_params["Incident Status"] = incident_status
      if priority is not None:
        script_params["Priority"] = priority
      if category is not None:
        script_params["Category"] = category
      if custom_fields is not None:
        script_params["Custom Fields"] = custom_fields
      if custom_mapping_file is not None:
        script_params["Custom Mapping File"] = custom_mapping_file
      if remote_file is not None:
        script_params["Remote File"] = remote_file

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="RSAArcher_Create Incident",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "RSAArcher_Create Incident",  # Assuming same as actionName
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
        print(f"Error executing action RSAArcher_Create Incident for RSAArcher: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for RSAArcher")
      return {"Status": "Failed", "Message": "No active instance found."}
