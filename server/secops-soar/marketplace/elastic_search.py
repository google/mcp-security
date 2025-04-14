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
  # This function registers all tools (actions) for the ElasticSearch integration.

  @mcp.tool()
  async def elastic_search_simple_es_search(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      index: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Search pattern for a elastic index.\r\nIn elastic, index is like a"
                  " DatabaseName, and data is stored across various indexes.\r\nThis"
                  " param defines in what index(es) to search. It can be an exact name"
                  ' ie: "smp_playbooks-2019.06.13"\r\nor you can use a (*) wildcard to'
                  ' search by a pattern. e: "smp_playbooks-2019.06*" or "smp*".\r\nTo'
                  " learn more about elastic indexes visit"
                  " https://www.elastic.co/blog/what-is-an-elasticsearch-index"
              ),
          ),
      ],
      query: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  'The search query to perform. It is in Lucene syntax.\r\nIE1: "*"'
                  " (this is a wildcard that will return all record)\r\nIE1:"
                  ' "level:error"\r\nIE2: "level:information"\r\nIE3: "level:error OR'
                  ' level:warning"\r\nTo learn more about lucene syntax,'
                  " visit\r\nhttps://www.elastic.co/guide/en/kibana/current/lucene-query.html#lucene-query\r\nhttps://www.elastic.co/guide/en/elasticsearch/reference/7.1/query-dsl-query-string-query.html#query-string-syntax"
              ),
          ),
      ],
      limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Limits the document return count, ie: 10.\r\n0 = No limit",
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
    """Searches through everything in Elastic Search and returns back results in a dictionary format. This action supports only queries without time range, if you want to use time range in your query use Advanced ES Search action.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ElasticSearch")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for ElasticSearch: {e}")
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
      if index is not None:
        script_params["Index"] = index
      if query is not None:
        script_params["Query"] = query
      if limit is not None:
        script_params["Limit"] = limit

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="ElasticSearch_Simple ES Search",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "ElasticSearch_Simple ES Search"
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
            "Error executing action ElasticSearch_Simple ES Search for"
            f" ElasticSearch: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for ElasticSearch")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def elastic_search_advanced_es_search(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      index: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Search pattern for a elastic index.\r\nIn elastic, index is like a"
                  " DatabaseName, and data is stored across various indexes.\r\nThis"
                  " param defines in what index(es) to search. It can be an exact name"
                  ' ie: "smp_playbooks-2019.06.13"\r\nor you can use a (*) wildcard to'
                  ' search by a pattern. e: "smp_playbooks-2019.06*" or "smp*".\r\nTo'
                  " learn more about elastic indexes visit"
                  " https://www.elastic.co/blog/what-is-an-elasticsearch-index"
              ),
          ),
      ],
      query: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  'The search query to perform. It is in Lucene syntax.\r\nIE1: "*"'
                  " (this is a wildcard that will return all record)\r\nIE1:"
                  ' "level:error"\r\nIE2: "level:information"\r\nIE3: "level:error OR'
                  ' level:warning"\r\nTo learn more about lucene syntax,'
                  " visit\r\nhttps://www.elastic.co/guide/en/kibana/current/lucene-query.html#lucene-query\r\nhttps://www.elastic.co/guide/en/elasticsearch/reference/7.1/query-dsl-query-string-query.html#query-string-syntax"
              ),
          ),
      ],
      limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Limits the document return count, ie: 10.\r\n0 = No limit",
          ),
      ],
      display_field: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  'Limits the returned fields. Default "*" = Return all fields.\r\nYou'
                  ' can state a single field. ie: "level"'
              ),
          ),
      ],
      search_field: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Search field for free text queries (When query doesn't specify a"
                  ' field name).\r\nDefault is "_all", which means all fields are'
                  ' searched. It is best to use proper lucene syntanx on "_all" fields,'
                  " or textual search on a specific field.\r\nie1: Search Field ="
                  ' "_all". Query = "level:error" Query will return all records where'
                  ' "level" field, equals "error".\r\nie2: Search Field = "Message",'
                  ' query = "*Login Alarm*". Query will return all records, which their'
                  ' "Message" field, contains the text "Login Alarm"'
              ),
          ),
      ],
      timestamp_field: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "The name of the field to run time-based filtering against. Default"
                  " is @timestamp. If both Earliest Date and Oldest Date are empty, no"
                  " time-based filtering will occur."
              ),
          ),
      ],
      oldest_date: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Start date of the search. Search will return only records equal or"
                  " after this point in time.\r\nInput may be in exact"
                  " UTC:\r\n\tFormat: YYYY-MM-DDTHH:MM:SSZ\r\n\tie:"
                  " 2019-06-04T10:00:00Z\r\nInput may also be in relative form (using"
                  ' date-math):\r\n\tie: "now", "now-1d", "now-1d/d",'
                  ' "now-2h/h"\r\n\tto learn more about date-math visit'
                  " https://www.elastic.co/guide/en/elasticsearch/reference/7.1/common-options.html#date-math"
              ),
          ),
      ],
      earliest_date: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "End date of the search. Search will return only records equal or"
                  " before this point in time.\r\nInput may be in exact"
                  " UTC:\r\n\tFormat: YYYY-MM-DDTHH:MM:SSZ\r\n\tie:"
                  " 2019-06-04T10:00:00Z\r\nInput may also be in relative form (using"
                  ' date-math):\r\n\tie: "now", "now-1d", "now-1d/d",'
                  ' "now-2h/h"\r\n\tto learn more about date-math visit'
                  " https://www.elastic.co/guide/en/elasticsearch/reference/7.1/common-options.html#date-math"
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
    """Premade structured Elastic search query, returns a dict of dictionaries. This action should be used when you want to use time range in the query. If you don’t want to use the time range, use Simple ES Search action.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ElasticSearch")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for ElasticSearch: {e}")
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
      if index is not None:
        script_params["Index"] = index
      if query is not None:
        script_params["Query"] = query
      if limit is not None:
        script_params["Limit"] = limit
      if display_field is not None:
        script_params["Display Field"] = display_field
      if search_field is not None:
        script_params["Search Field"] = search_field
      if timestamp_field is not None:
        script_params["Timestamp Field"] = timestamp_field
      if oldest_date is not None:
        script_params["Oldest Date"] = oldest_date
      if earliest_date is not None:
        script_params["Earliest Date"] = earliest_date

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="ElasticSearch_Advanced ES Search",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": (
                  "ElasticSearch_Advanced ES Search"
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
            "Error executing action ElasticSearch_Advanced ES Search for"
            f" ElasticSearch: {e}"
        )
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for ElasticSearch")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def elastic_search_ping(
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
    """Verifies connectivity to Elastic Search server

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ElasticSearch")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for ElasticSearch: {e}")
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
          actionName="ElasticSearch_Ping",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "ElasticSearch_Ping",  # Assuming same as actionName
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
        print(f"Error executing action ElasticSearch_Ping for ElasticSearch: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for ElasticSearch")
      return {"Status": "Failed", "Message": "No active instance found."}

  @mcp.tool()
  async def elastic_search_dsl_search(
      case_id: Annotated[str, Field(..., description="The ID of the case.")],
      alert_group_identifiers: Annotated[
          List[str], Field(..., description="Identifiers for the alert groups.")
      ],
      index: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "Search pattern for a elastic index.\r\nIn elastic, index is like a"
                  " DatabaseName, and data is stored across various indexes.\r\nThis"
                  " param defines in what index(es) to search. It can be an exact name"
                  ' ie: "smp_playbooks-2019.06.13"\r\nor you can use a (*) wildcard to'
                  ' search by a pattern. e: "smp_playbooks-2019.06*" or "smp*".\r\nTo'
                  " learn more about elastic indexes visit"
                  " https://www.elastic.co/blog/what-is-an-elasticsearch-index"
              ),
          ),
      ],
      query: Annotated[
          Optional[str],
          Field(
              default=None,
              description=(
                  "The DSL query to perform. The query must be a valid JSON, or *. For"
                  " more information, please refer to"
                  " https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html."
              ),
          ),
      ],
      limit: Annotated[
          Optional[str],
          Field(
              default=None,
              description="Limits the document return count, ie: 10.\r\n0 = No limit",
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
    """Execute a DSL query in the ElasticSearch. This action fetches data from ES for past 24 hours.

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
          Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ElasticSearch")
      )
      instances = instance_response.get("integration_instances", [])
    except Exception as e:
      # Log error appropriately in real code
      print(f"Error fetching instance for ElasticSearch: {e}")
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
      if index is not None:
        script_params["Index"] = index
      if query is not None:
        script_params["Query"] = query
      if limit is not None:
        script_params["Limit"] = limit

      # Prepare data model for the API request
      action_data = ApiManualActionDataModel(
          alertGroupIdentifiers=alert_group_identifiers,
          caseId=case_id,
          targetEntities=final_target_entities,
          scope=final_scope,
          isPredefinedScope=is_predefined_scope,  # Pass the is_predefined_scope parameter
          actionProvider="Scripts",  # Assuming constant based on example
          actionName="ElasticSearch_DSL Search",
          properties={
              "IntegrationInstance": instance_identifier,
              "ScriptName": "ElasticSearch_DSL Search",  # Assuming same as actionName
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
        print(f"Error executing action ElasticSearch_DSL Search for ElasticSearch: {e}")
        return {"Status": "Failed", "Message": f"Error executing action: {e}"}
    else:
      print(f"Warning: No active integration instance found for ElasticSearch")
      return {"Status": "Failed", "Message": "No active instance found."}
