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
  # This function registers all tools (actions) for the VMRay integration.

  @mcp.tool()
  async def vm_ray_scan_hash(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      threat_indicator_score_threshold: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the lowest score that will be used to return threat"
                  " indicators. Maximum: 5."
              ),
          ),
      ],
      ioc_type_filter: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of IOC types that need to be"
                  " returned. Possible values: domains, emails, files, ips, mutexes,"
                  " processes, registry, urls."
              ),
          ),
      ],
      ioc_verdict_filter: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of IOC verdicts that will be used"
                  " during the ingestion of IOCs. Possible values: Malicious,"
                  " Suspicious, Clean, None."
              ),
          ),
      ],
      max_io_cs_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many IOCs to return per entity per IOC type."
                  " Default: 10."
              ),
          ),
      ],
      max_threat_indicators_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many threat indicators to return per entity."
                  " Default: 10."
              ),
          ),
      ],
      create_insight: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will create an insight containing information"
                  " about entities."
              ),
          ),
      ],
      only_suspicious_insight: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will only create insight for suspicious entities."
                  ' Note: "Create Insight" parameter needs to be enabled.'
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
    """Get details about a specific hash.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VMRay")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for VMRay: {e}")
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
      script_params["Threat Indicator Score Threshold"] = (
          threat_indicator_score_threshold
      )
      script_params["IOC Type Filter"] = ioc_type_filter
      script_params["IOC Verdict Filter"] = ioc_verdict_filter
      if max_io_cs_to_return is not None:
        script_params["Max IOCs To Return"] = max_io_cs_to_return
      if max_threat_indicators_to_return is not None:
        script_params["Max Threat Indicators To Return"] = (
            max_threat_indicators_to_return
        )
      if create_insight is not None:
        script_params["Create Insight"] = create_insight
      if only_suspicious_insight is not None:
        script_params["Only Suspicious Insight"] = only_suspicious_insight

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="VMRay_Scan Hash",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "VMRay_Scan Hash",  # Assuming same as actionName
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
        print(f"Error executing action VMRay_Scan Hash for VMRay: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for VMRay")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def vm_ray_upload_file_and_get_report(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      sample_file_path: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of absolute file paths for"
                  " submission."
              ),
          ),
      ],
      tag_names: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the tags that you want to add to the submission.",
          ),
      ],
      comment: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the comment that you want to add to the submission.",
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
    """Submit files for analysis in VMRay. Note: Action is running as async, please adjust script timeout value in Siemplify IDE for action as needed.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VMRay")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for VMRay: {e}")
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
      script_params["Sample File Path"] = sample_file_path
      if tag_names is not None:
        script_params["Tag Names"] = tag_names
      if comment is not None:
        script_params["Comment"] = comment

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="VMRay_Upload File And Get Report",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "VMRay_Upload File And Get Report"
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
        print(f"Error executing action VMRay_Upload File And Get Report for VMRay: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for VMRay")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def vm_ray_add_tag_to_submission(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      submission_id: Annotated[
          str, Field(..., description="The ID of the Submission.")
      ],
      tag_name: Annotated[
          str, Field(..., description="The tag Name that need to be added.")
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
    """Add Tag to Submission using Submission ID.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VMRay")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for VMRay: {e}")
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
      script_params["Submission ID"] = submission_id
      script_params["Tag Name"] = tag_name

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="VMRay_Add Tag to Submission",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "VMRay_Add Tag to Submission"
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
        print(f"Error executing action VMRay_Add Tag to Submission for VMRay: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for VMRay")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def vm_ray_ping(
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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VMRay")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for VMRay: {e}")
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
          actionName="VMRay_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "VMRay_Ping",  # Assuming same as actionName
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
        print(f"Error executing action VMRay_Ping for VMRay: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for VMRay")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def vm_ray_scan_url(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      threat_indicator_score_threshold: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify the lowest score that will be used to return threat"
                  " indicators. Maximum: 5."
              ),
          ),
      ],
      ioc_type_filter: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of IOC types that need to be"
                  " returned. Possible values: ips, urls, domains."
              ),
          ),
      ],
      ioc_verdict_filter: Annotated[
          str,
          Field(
              ...,
              description=(
                  "Specify a comma-separated list of IOC verdicts that will be used"
                  " during the ingestion of IOCs. Possible values: Malicious,"
                  " Suspicious, Clean, None."
              ),
          ),
      ],
      max_io_cs_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many IOCs to return per entity per IOC type."
                  " Default: 10."
              ),
          ),
      ],
      max_threat_indicators_to_return: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Specify how many threat indicators to return per entity."
                  " Default: 10."
              ),
          ),
      ],
      create_insight: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will create an insight containing information"
                  " about entities."
              ),
          ),
      ],
      only_suspicious_insight: Annotated[
          Optional[bool],
          Field(
              default=None,
              description=(
                  "If enabled, action will only create insight for suspicious entities."
                  ' Note: "Create Insight" parameter needs to be enabled.'
              ),
          ),
      ],
      tag_names: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the tags that you want to add to the submission.",
          ),
      ],
      comment: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Specify the comment that you want to add to the submission.",
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
    """Submit a URL and receive related information.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VMRay")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for VMRay: {e}")
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
      script_params["Threat Indicator Score Threshold"] = (
          threat_indicator_score_threshold
      )
      script_params["IOC Type Filter"] = ioc_type_filter
      script_params["IOC Verdict Filter"] = ioc_verdict_filter
      if max_io_cs_to_return is not None:
        script_params["Max IOCs To Return"] = max_io_cs_to_return
      if max_threat_indicators_to_return is not None:
        script_params["Max Threat Indicators To Return"] = (
            max_threat_indicators_to_return
        )
      if create_insight is not None:
        script_params["Create Insight"] = create_insight
      if only_suspicious_insight is not None:
        script_params["Only Suspicious Insight"] = only_suspicious_insight
      if tag_names is not None:
        script_params["Tag Names"] = tag_names
      if comment is not None:
        script_params["Comment"] = comment

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="VMRay_Scan URL",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "VMRay_Scan URL",  # Assuming same as actionName
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
        print(f"Error executing action VMRay_Scan URL for VMRay: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for VMRay")
      return {"Status": "Failed", "Message": "No active instance found."}
