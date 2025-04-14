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
  # This function registers all tools (actions) for the Anomali integration.

  @mcp.tool()
  async def anomali_get_threat_info(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      limit: Annotated[
          str, Field(..., description="Specify how many records to return per entity.")
      ],
      severity_threshold: Annotated[
          Optional[List[Any]],
          Field(
              default=None,
              description=(
                  "Specify what should be the severity threshold for the entity, in"
                  " order to mark it as suspicious. If multiple records are found for"
                  " the same entity, action will take the highest severity out of all"
                  " available records."
              ),
          ),
      ],
      confidence_threshold: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify what should be the confidence threshold for the entity, in"
                  " order to mark it as suspicious. Note: Maximum is 100. If multiple"
                  " records are found for the entity, action will take the average."
                  " Active records have priority. Default: 50."
              ),
          ),
      ],
      ignore_false_positive_status: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will ignore the false positive status and mark"
                  ' the entity as suspicious based on the "Severity Threshold" and'
                  ' "Confidence Threshold". If disabled, action will never label false'
                  " positive entities as suspicious, regardless, if they pass the"
                  ' "Severity Threshold" and "Confidence Threshold" conditions or not.'
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
    """Enrich entities using information from Anomali ThreatStream. Supported entities: IP, URL, Hash, Email Addresses (User entities that match email regex).

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Anomali")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Anomali: {e}")
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
      script_params["Limit"] = limit
      if severity_threshold is not None:
        script_params["Severity Threshold"] = severity_threshold
      if confidence_threshold is not None:
        script_params["Confidence Threshold"] = confidence_threshold
      if ignore_false_positive_status is not None:
        script_params["Ignore False Positive Status"] = ignore_false_positive_status

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Anomali_GetThreatInfo",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Anomali_GetThreatInfo",  # Assuming same as actionName
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
        print(f"Error executing action Anomali_GetThreatInfo for Anomali: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Anomali")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def anomali_ping(
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
    """Test connectivity to Anomali ThreatStream

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Anomali")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Anomali: {e}")
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
          actionName="Anomali_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "Anomali_Ping",  # Assuming same as actionName
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
        print(f"Error executing action Anomali_Ping for Anomali: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Anomali")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def anomali_get_related_associations(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      return_campaigns: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related campaigns and details about"
                  " them."
              ),
          ),
      ],
      return_threat_bulletins: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related threat bulletins and details"
                  " about them."
              ),
          ),
      ],
      return_actors: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related actors and details about them."
              ),
          ),
      ],
      return_attack_patterns: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related attack patterns and details"
                  " about them."
              ),
          ),
      ],
      return_courses_of_action: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related courses of action and details"
                  " about them."
              ),
          ),
      ],
      return_identities: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related identities and details about"
                  " them."
              ),
          ),
      ],
      return_incidents: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related incidents and details about"
                  " them."
              ),
          ),
      ],
      return_infrastructure: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related infrastructure and details"
                  " about them."
              ),
          ),
      ],
      return_intrusion_sets: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related intrusion sets and details"
                  " about them."
              ),
          ),
      ],
      return_malware: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related malware and details about"
                  " them."
              ),
          ),
      ],
      return_signatures: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related signatures and details about"
                  " them."
              ),
          ),
      ],
      return_tools: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related tools and details about them."
              ),
          ),
      ],
      return_tt_ps: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related TTPs and details about them."
              ),
          ),
      ],
      return_vulnerabilities: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will fetch related vulnerabilities and details"
                  " about them."
              ),
          ),
      ],
      create_campaign_entity: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  'If enabled, action will create an entity out of available "Campaign"'
                  " associations."
              ),
          ),
      ],
      create_actors_entity: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  'If enabled, action will create an entity out of available "Actor"'
                  " associations."
              ),
          ),
      ],
      create_signature_entity: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will create an entity out of available"
                  ' "Signature" associations.'
              ),
          ),
      ],
      create_vulnerability_entity: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will create an entity out of available"
                  ' "Vulnerability" associations.'
              ),
          ),
      ],
      max_associations_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many associations to return per type. Default: 5"
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
    """Retrieve entity related associations from Anomali ThreatStream.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Anomali")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for Anomali: {e}")
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
      if return_campaigns is not None:
        script_params["Return Campaigns"] = return_campaigns
      if return_threat_bulletins is not None:
        script_params["Return Threat Bulletins"] = return_threat_bulletins
      if return_actors is not None:
        script_params["Return Actors"] = return_actors
      if return_attack_patterns is not None:
        script_params["Return Attack Patterns"] = return_attack_patterns
      if return_courses_of_action is not None:
        script_params["Return Courses Of Action"] = return_courses_of_action
      if return_identities is not None:
        script_params["Return Identities"] = return_identities
      if return_incidents is not None:
        script_params["Return Incidents"] = return_incidents
      if return_infrastructure is not None:
        script_params["Return Infrastructure"] = return_infrastructure
      if return_intrusion_sets is not None:
        script_params["Return Intrusion Sets"] = return_intrusion_sets
      if return_malware is not None:
        script_params["Return Malware"] = return_malware
      if return_signatures is not None:
        script_params["Return Signatures"] = return_signatures
      if return_tools is not None:
        script_params["Return Tools"] = return_tools
      if return_tt_ps is not None:
        script_params["Return TTPs"] = return_tt_ps
      if return_vulnerabilities is not None:
        script_params["Return Vulnerabilities"] = return_vulnerabilities
      if create_campaign_entity is not None:
        script_params["Create Campaign Entity"] = create_campaign_entity
      if create_actors_entity is not None:
        script_params["Create Actors Entity"] = create_actors_entity
      if create_signature_entity is not None:
        script_params["Create Signature Entity"] = create_signature_entity
      if create_vulnerability_entity is not None:
        script_params["Create Vulnerability Entity"] = create_vulnerability_entity
      if max_associations_to_return is not None:
        script_params["Max Associations To Return"] = max_associations_to_return

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="Anomali_Get Related Associations",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "Anomali_Get Related Associations"
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
            f"Error executing action Anomali_Get Related Associations for Anomali: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for Anomali")
      return {"Status": "Failed", "Message": "No active instance found."}
