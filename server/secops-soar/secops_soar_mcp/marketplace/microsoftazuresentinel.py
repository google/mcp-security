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
from secops_soar_mcp import bindings
from mcp.server.fastmcp import FastMCP
from secops_soar_mcp.utils.consts import Endpoints
from secops_soar_mcp.utils.models import ApiManualActionDataModel, EmailContent, TargetEntity
import json
from typing import Optional, List, Dict, Union, Annotated
from pydantic import Field
from secops_soar_mcp.utils.pydantic_list_field import PydanticListField


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the MicrosoftAzureSentinel integration.

    @mcp.tool()
    async def microsoft_azure_sentinel_run_kql_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], kql_query: Annotated[str, Field(..., description="A KQL Query to execute in Azure Sentinel. For example, to get security alerts available in Sentinel, query will be \"SecurityAlert\". Use other action input parameters (time span, limit) to filter the query results. For the examples of KQL queries consider Sentinel \"Logs\" Web page")], time_span: Annotated[str, Field(default=None, description="Time span to look for, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute.")], query_timeout: Annotated[str, Field(default=None, description="Timeout value for the Azure Sentinel hunting rule API call. Note that Siemplify action python process timeout should be adjusted accordingly for this parameter, to not timeout action sooner than specified value because of the python process timeout.")], record_limit: Annotated[str, Field(default=None, description="How many records should be fetched. Optional parameter, if set, adds a \"| limit x\" to the kql query where x is the value set for the record limit. Can be removed if \"limit\" is already set in kql query or not needed.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Run Azure Sentinel KQL Query based on the provided action input parameters.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["KQL Query"] = kql_query
            if time_span is not None:
                script_params["Time Span"] = time_span
            if query_timeout is not None:
                script_params["Query Timeout"] = query_timeout
            if record_limit is not None:
                script_params["Record Limit"] = record_limit
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Run KQL Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Run KQL Query",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Run KQL Query for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_get_alert_rule_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], alert_rule_id: Annotated[str, Field(..., description="Alert Rule ID")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get Details of the Azure Sentinel Scheduled Alert Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Alert Rule ID"] = alert_rule_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Get Alert Rule Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Get Alert Rule Details",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Get Alert Rule Details for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_list_custom_hunting_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hunting_rule_names_to_return: Annotated[str, Field(default=None, description="Names for the hunting rules action should return. Comma-separated string")], fetch_specific_hunting_rule_tactics: Annotated[str, Field(default=None, description="What hunting rule tactics action should return. Comma-separated string")], max_rules_to_return: Annotated[str, Field(default=None, description="How many scheduled alert rules the action should return, for example, 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Custom Hunting Rules available in Sentinel

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if hunting_rule_names_to_return is not None:
                script_params["Hunting Rule Names to Return"] = hunting_rule_names_to_return
            if fetch_specific_hunting_rule_tactics is not None:
                script_params["Fetch Specific Hunting Rule Tactics"] = fetch_specific_hunting_rule_tactics
            if max_rules_to_return is not None:
                script_params["Max rules to return"] = max_rules_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_List Custom Hunting Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_List Custom Hunting Rules",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_List Custom Hunting Rules for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_get_incident_statistic(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], time_frame: Annotated[str, Field(default=None, description="Time frame in hours for which to fetch Incidents")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get Azure Sentinel Incident Statistics

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if time_frame is not None:
                script_params["Time Frame"] = time_frame
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Get Incident Statistic",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Get Incident Statistic",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Get Incident Statistic for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_create_alert_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], enable_alert_rule: Annotated[bool, Field(..., description="Enable or disable new alert rule")], name: Annotated[str, Field(..., description="Display name of the new alert rule")], severity: Annotated[List[str], Field(..., description="Severity of the new alert rule")], query: Annotated[str, Field(..., description="Query of the new alert rule")], frequency: Annotated[str, Field(..., description="How frequently to run the query, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. \nMinimum is 5 minutes, maximum is 14 days.")], period_of_lookup_data: Annotated[str, Field(..., description="Time of the last lookup data, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. \nMinimum is 5 minutes, maximum is 14 days.")], trigger_operator: Annotated[List[str], Field(..., description="Trigger operator for this alert rule.\nPossible values are: GreaterThan, LessThan, Equal, NotEqual")], trigger_threshold: Annotated[str, Field(..., description="Trigger threshold for this alert rule")], enable_suppression: Annotated[bool, Field(..., description="Whether you want to stop running query after alert is generated")], suppression_duration: Annotated[str, Field(..., description="How long you want to stop running query after alert is generated, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. \nMinimum is 5 minutes, maximum is 14 days.")], description: Annotated[str, Field(default=None, description="Description of the new alert rule")], tactics: Annotated[str, Field(default=None, description="Tactics of the new alert rule. Comma-separated values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create Azure Sentinel Scheduled Alert Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Enable Alert Rule"] = enable_alert_rule
            script_params["Name"] = name
            script_params["Severity"] = severity
            script_params["Query"] = query
            script_params["Frequency"] = frequency
            script_params["Period of Lookup Data"] = period_of_lookup_data
            script_params["Trigger Operator"] = trigger_operator
            script_params["Trigger Threshold"] = trigger_threshold
            script_params["Enable Suppression"] = enable_suppression
            script_params["Suppression Duration"] = suppression_duration
            if description is not None:
                script_params["Description"] = description
            if tactics is not None:
                script_params["Tactics"] = tactics
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Create Alert Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Create Alert Rule",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Create Alert Rule for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_update_alert_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], alert_rule_id: Annotated[str, Field(..., description="Alert Rule ID")], enable_alert_rule: Annotated[bool, Field(default=None, description="Enable or disable new alert rule")], name: Annotated[str, Field(default=None, description="Display name of the new alert rule")], severity: Annotated[List[str], Field(default=None, description="Severity of the new alert rule")], query: Annotated[str, Field(default=None, description="Query of the new alert rule")], frequency: Annotated[str, Field(default=None, description="How frequently to run the query, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. \nMinimum is 5 minutes, maximum is 14 days.")], period_of_lookup_data: Annotated[str, Field(default=None, description="Time of the last lookup data, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. \nMinimum is 5 minutes, maximum is 14 days.")], trigger_operator: Annotated[List[str], Field(default=None, description="Trigger operator for this alert rule.\nPossible values are: GreaterThan, LessThan, Equal, NotEqual")], trigger_threshold: Annotated[str, Field(default=None, description="Trigger threshold for this alert rule")], enable_suppression: Annotated[bool, Field(default=None, description="Whether you want to stop running query after alert is generated")], suppression_duration: Annotated[str, Field(default=None, description="How long you want to stop running query after alert is generated, use the following format: \nPT + number + (M, H), where M - minutes, H - hours. \nUse P + number + D to specify a number of days. \nCan be combined as P1DT1H1M - 1 day, 1 hour and 1 minute. \nMinimum is 5 minutes, maximum is 14 days.")], description: Annotated[str, Field(default=None, description="Description of the new alert rule")], tactics: Annotated[str, Field(default=None, description="Tactics of the new alert rule. Comma-separated values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update Azure Sentinel Scheduled Alert Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Alert Rule ID"] = alert_rule_id
            if enable_alert_rule is not None:
                script_params["Enable Alert Rule"] = enable_alert_rule
            if name is not None:
                script_params["Name"] = name
            if severity is not None:
                script_params["Severity"] = severity
            if query is not None:
                script_params["Query"] = query
            if frequency is not None:
                script_params["Frequency"] = frequency
            if period_of_lookup_data is not None:
                script_params["Period of Lookup Data"] = period_of_lookup_data
            if trigger_operator is not None:
                script_params["Trigger Operator"] = trigger_operator
            if trigger_threshold is not None:
                script_params["Trigger Threshold"] = trigger_threshold
            if enable_suppression is not None:
                script_params["Enable Suppression"] = enable_suppression
            if suppression_duration is not None:
                script_params["Suppression Duration"] = suppression_duration
            if description is not None:
                script_params["Description"] = description
            if tactics is not None:
                script_params["Tactics"] = tactics
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Update Alert Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Update Alert Rule",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Update Alert Rule for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_list_incidents(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], time_frame: Annotated[str, Field(default=None, description="Time frame in hours for which to fetch Incidents")], status: Annotated[str, Field(default=None, description="Statuses of the incidents to look for. Comma-separated string")], severity: Annotated[str, Field(default=None, description="Severities of the incidents to look for. Comma-separated string.")], how_many_incidents_to_fetch: Annotated[str, Field(default=None, description="How many incidents to fetch")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Microsoft Azure Sentinel Incidents based on the provided search criteria.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if time_frame is not None:
                script_params["Time Frame"] = time_frame
            if status is not None:
                script_params["Status"] = status
            if severity is not None:
                script_params["Severity"] = severity
            if how_many_incidents_to_fetch is not None:
                script_params["How Many Incidents to Fetch"] = how_many_incidents_to_fetch
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_List Incidents",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_List Incidents",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_List Incidents for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_add_comment_to_incident(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_number: Annotated[str, Field(..., description="Specify Incident number to add comment to.")], comment_to_add: Annotated[str, Field(..., description="Specify comment to add to Incident")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to Azure Sentinel Incident.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident Number"] = incident_number
            script_params["Comment to Add"] = comment_to_add
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Add Comment to Incident",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Add Comment to Incident",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Add Comment to Incident for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_update_incident_details_v2(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_case_number: Annotated[str, Field(..., description="Specify Azure Sentinel incident number to update.")], title: Annotated[str, Field(default=None, description="Specify new title for the Azure Sentinel incident.")], status: Annotated[List[str], Field(default=None, description="Specify new status for the Azure Sentinel incident.")], severity: Annotated[List[str], Field(default=None, description="Specify new severity for the Azure Sentinel incident.")], description: Annotated[str, Field(default=None, description="Specify new description for the Azure Sentinel incident.")], assigned_to: Annotated[str, Field(default=None, description="Specify the user to assign the incident to.")], closed_reason: Annotated[List[str], Field(default=None, description="If status of the incident is set to Closed, provide a Closed Reason for the incident.")], closing_comment: Annotated[str, Field(default=None, description="Optional closing comment to provide for the closed Azure Sentinel Incident.")], number_of_retries: Annotated[str, Field(default=None, description="Specify the number of retry attempts the action should make if the incident update was unsuccessful.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update Incident Details v2. Action is a Chronicle SOAR async action and can be configured for a retry for a longer period of time.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident Case Number"] = incident_case_number
            if title is not None:
                script_params["Title"] = title
            if status is not None:
                script_params["Status"] = status
            if severity is not None:
                script_params["Severity"] = severity
            if description is not None:
                script_params["Description"] = description
            if assigned_to is not None:
                script_params["Assigned To"] = assigned_to
            if closed_reason is not None:
                script_params["Closed Reason"] = closed_reason
            if closing_comment is not None:
                script_params["Closing Comment"] = closing_comment
            if number_of_retries is not None:
                script_params["Number of retries"] = number_of_retries
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Update Incident Details v2",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Update Incident Details v2",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Update Incident Details v2 for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to Microsoft Azure Sentinel

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Ping",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Ping for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_get_custom_hunting_rule_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hunting_rule_id: Annotated[str, Field(..., description="Hunting Rule ID")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get Details of the Azure Sentinel Custom Hunting Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Hunting Rule ID"] = hunting_rule_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Get Custom Hunting Rule Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Get Custom Hunting Rule Details",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Get Custom Hunting Rule Details for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_create_custom_hunting_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], display_name: Annotated[str, Field(..., description="Display name of the new custom hunting rule")], query: Annotated[str, Field(..., description="Query of the new custom hunting rule")], description: Annotated[str, Field(default=None, description="Description of the new custom hunting rule")], tactics: Annotated[str, Field(default=None, description="Tactics of the new custom hunting rule. Comma-separated values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create Azure Sentinel Custom Hunting Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Display Name"] = display_name
            script_params["Query"] = query
            if description is not None:
                script_params["Description"] = description
            if tactics is not None:
                script_params["Tactics"] = tactics
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Create Custom Hunting Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Create Custom Hunting Rule",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Create Custom Hunting Rule for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_delete_custom_hunting_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hunting_rule_id: Annotated[str, Field(..., description="Hunting Rule ID")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete Azure Sentinel Custom Hunting Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Hunting Rule ID"] = hunting_rule_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Delete Custom Hunting Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Delete Custom Hunting Rule",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Delete Custom Hunting Rule for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_update_incident_labels(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_case_number: Annotated[str, Field(..., description="Specify Azure Sentinel incident number to update with new labels.")], labels: Annotated[str, Field(..., description="Specify new labels that should be appended to the Incident. Parameter accepts multiple values as a comma-separated string.")], number_of_retries: Annotated[str, Field(default=None, description="Specify the number of retry attempts the action should make if the incident update was unsuccessful.")], retry_every: Annotated[str, Field(default=None, description="Specify what time period in seconds action should wait between incident update retries.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update Incident Labels. Please consider moving to the v2 version of the action, as it is implemented as a SOAR async action and provides more consistent results.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident Case Number"] = incident_case_number
            script_params["Labels"] = labels
            if number_of_retries is not None:
                script_params["Number of retries"] = number_of_retries
            if retry_every is not None:
                script_params["Retry Every"] = retry_every
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Update Incident Labels",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Update Incident Labels",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Update Incident Labels for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_update_incident_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_case_number: Annotated[str, Field(..., description="Specify Azure Sentinel incident number to update.")], title: Annotated[str, Field(default=None, description="Specify new title for the Azure Sentinel incident.")], status: Annotated[List[str], Field(default=None, description="Specify new status for the Azure Sentinel incident.")], severity: Annotated[List[str], Field(default=None, description="Specify new severity for the Azure Sentinel incident.")], description: Annotated[str, Field(default=None, description="Specify new description for the Azure Sentinel incident.")], assigned_to: Annotated[str, Field(default=None, description="Specify the user to assign the incident to.")], closed_reason: Annotated[List[str], Field(default=None, description="If status of the incident is set to Closed, provide a Closed Reason for the incident.")], closing_comment: Annotated[str, Field(default=None, description="Optional closing comment to provide for the closed Azure Sentinel Incident.")], number_of_retries: Annotated[str, Field(default=None, description="Specify the number of retry attempts the action should make if the incident update was unsuccessful.")], retry_every: Annotated[str, Field(default=None, description="Specify what time period action should wait between incident update retries.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update Incident Details. Please consider moving to the v2 version of the action, as it is implemented as a SOAR async action and provides more consistent results.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident Case Number"] = incident_case_number
            if title is not None:
                script_params["Title"] = title
            if status is not None:
                script_params["Status"] = status
            if severity is not None:
                script_params["Severity"] = severity
            if description is not None:
                script_params["Description"] = description
            if assigned_to is not None:
                script_params["Assigned To"] = assigned_to
            if closed_reason is not None:
                script_params["Closed Reason"] = closed_reason
            if closing_comment is not None:
                script_params["Closing Comment"] = closing_comment
            if number_of_retries is not None:
                script_params["Number of retries"] = number_of_retries
            if retry_every is not None:
                script_params["Retry Every"] = retry_every
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Update Incident Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Update Incident Details",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Update Incident Details for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_update_incident_labels_v2(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], incident_case_number: Annotated[str, Field(..., description="Specify Azure Sentinel incident number to update with new labels.")], labels: Annotated[str, Field(..., description="Specify new labels that should be appended to the Incident. Parameter accepts multiple values as a comma-separated string.")], number_of_retries: Annotated[str, Field(default=None, description="Specify the number of retry attempts the action should make if the incident update was unsuccessful.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update Incident Labels v2. Action is a Chronicle SOAR async action and can be configured for a retry for a longer period of time.

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Incident Case Number"] = incident_case_number
            script_params["Labels"] = labels
            if number_of_retries is not None:
                script_params["Number of retries"] = number_of_retries
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Update Incident Labels v2",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Update Incident Labels v2",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Update Incident Labels v2 for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_list_alert_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], alert_rule_severity: Annotated[str, Field(default=None, description="Severities of the alert rules to look for. Comma-separated string")], fetch_specific_alert_rule_types: Annotated[str, Field(default=None, description="What alert rule types action should return. Comma-separated string")], fetch_specific_alert_rule_tactics: Annotated[str, Field(default=None, description="What alert rule tactics action should return. Comma-separated string")], fetch_only_enabled_alert_rules: Annotated[bool, Field(default=None, description="If action should return only enabled alert rules")], max_rules_to_return: Annotated[str, Field(default=None, description="How many scheduled alert rules the action should return, for example, 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get Azure Sentinel Scheduled Rules list

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if alert_rule_severity is not None:
                script_params["Alert Rule Severity"] = alert_rule_severity
            if fetch_specific_alert_rule_types is not None:
                script_params["Fetch Specific Alert Rule Types"] = fetch_specific_alert_rule_types
            if fetch_specific_alert_rule_tactics is not None:
                script_params["Fetch Specific Alert Rule Tactics"] = fetch_specific_alert_rule_tactics
            if fetch_only_enabled_alert_rules is not None:
                script_params["Fetch only Enabled Alert Rules"] = fetch_only_enabled_alert_rules
            if max_rules_to_return is not None:
                script_params["Max rules to return"] = max_rules_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_List Alert Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_List Alert Rules",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_List Alert Rules for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_delete_alert_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], alert_rule_id: Annotated[str, Field(..., description="Alert Rule ID")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete Azure Sentinel Scheduled Alert Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Alert Rule ID"] = alert_rule_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Delete Alert Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Delete Alert Rule",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Delete Alert Rule for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_update_custom_hunting_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hunting_rule_id: Annotated[str, Field(..., description="Hunting Rule ID")], display_name: Annotated[str, Field(default=None, description="Display name of the new custom hunting rule")], query: Annotated[str, Field(default=None, description="Query of the new custom hunting rule")], description: Annotated[str, Field(default=None, description="Description of the new custom hunting rule")], tactics: Annotated[str, Field(default=None, description="Tactics of the new custom hunting rule. Comma-separated values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update Azure Sentinel Custom Hunting Rule

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Hunting Rule ID"] = hunting_rule_id
            if display_name is not None:
                script_params["Display Name"] = display_name
            if query is not None:
                script_params["Query"] = query
            if description is not None:
                script_params["Description"] = description
            if tactics is not None:
                script_params["Tactics"] = tactics
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Update Custom Hunting Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Update Custom Hunting Rule",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Update Custom Hunting Rule for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_azure_sentinel_run_custom_hunting_rule_query(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], hunting_rule_id: Annotated[str, Field(..., description="Hunting Rule ID")], timeout: Annotated[str, Field(default=None, description="Timeout value for the Azure Sentinel hunting rule API call")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Run Custom Hunting Rule Query

        Returns:
            dict: A dictionary containing the result of the action execution.
        """
        final_target_entities: Optional[List[TargetEntity]] = None
        final_scope: Optional[str] = None
        is_predefined_scope: Optional[bool] = None
    
        if target_entities:
            # Specific target entities provided, ignore scope parameter
            final_target_entities = target_entities
            final_scope = None
            is_predefined_scope = False
        else:
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
    
        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MicrosoftAzureSentinel")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftAzureSentinel: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Hunting Rule ID"] = hunting_rule_id
            if timeout is not None:
                script_params["Timeout"] = timeout
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftAzureSentinel_Run Custom Hunting Rule Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftAzureSentinel_Run Custom Hunting Rule Query",
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(f"Error executing action MicrosoftAzureSentinel_Run Custom Hunting Rule Query for MicrosoftAzureSentinel: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MicrosoftAzureSentinel")
            return {"Status": "Failed", "Message": "No active instance found."}
