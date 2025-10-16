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
    # This function registers all tools (actions) for the Cloudflare integration.

    @mcp.tool()
    async def cloudflare_list_firewall_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], zone_name: Annotated[str, Field(..., description="Specify the name of the zone, which will contain the firewall rule.")], filter_key: Annotated[List[str], Field(default=None, description="Specify the key that needs to be used to filter results.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied. Filtering logic is working based on the value  provided in the \"Filter Key\" parameter.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter. If \"Equal\" is selected, action will try to find the exact match among results and if \"Contains\" is selected, action will try to find results that contain that substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the value provided in the \"Filter Key\" parameter.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return. If nothing is provided, action will return 50 records.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
List available firewall rules in Cloudflare.

Action Parameters: Zone Name: Specify the name of the zone, which will contain the firewall rule., Filter Key: Specify the key that needs to be used to filter {item type}., Filter Logic: Specify the filter logic that should be applied. The filtering logic is based on the value provided in the "Filter Key" parameter., Filter Value: Specify the value that should be used in the filter.If "Equal" is selected, the action tries to find the exact match among results.If "Contains" is selected, the action tries to find results that contain that substring.If nothing is provided in this parameter, the filter is not applied. The filtering logic is based on the value provided in the "Filter Key" parameter., Max Records To Return: Specify the number of records to return.If nothing is provided, the action returns 50 records.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Zone Name"] = zone_name
            if filter_key is not None:
                script_params["Filter Key"] = filter_key
            if filter_logic is not None:
                script_params["Filter Logic"] = filter_logic
            if filter_value is not None:
                script_params["Filter Value"] = filter_value
            if max_records_to_return is not None:
                script_params["Max Records To Return"] = max_records_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Cloudflare_List Firewall Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_List Firewall Rules",
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
                print(f"Error executing action Cloudflare_List Firewall Rules for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cloudflare_add_ip_to_rule_list(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name: Annotated[str, Field(..., description="Specify the name of the rule list to which you want to add rule list items.")], description: Annotated[str, Field(default=None, description="Specify a description for the newly added rule list items.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add IP addresses to the rule list in Cloudflare. Supported Entities: IP Address.

Action Parameters: Rule Name: Specify the name of the rule list to which you want to add rule list items., Description: Specify a description for the newly added rule list items.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name"] = rule_name
            if description is not None:
                script_params["Description"] = description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Cloudflare_Add IP To Rule List",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_Add IP To Rule List",
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
                print(f"Error executing action Cloudflare_Add IP To Rule List for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cloudflare_add_url_to_rule_list(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name: Annotated[str, Field(..., description="Specify the name of the rule list to which you want to add rule list items.")], target_url: Annotated[str, Field(..., description="Specify the target URL for the rule list item.")], description: Annotated[str, Field(default=None, description="Specify a description for the newly added rule list item.")], status_code: Annotated[List[str], Field(default=None, description="Specify the status for the rule list item.")], preserve_query_string: Annotated[bool, Field(default=None, description="If enabled, the rule list item will preserve the query string.")], include_subdomains: Annotated[bool, Field(default=None, description="If enabled, the rule list item will include subdomains.")], subpath_matching: Annotated[bool, Field(default=None, description="If enabled, the rule list item will match the subpath.")], preserve_path_suffix: Annotated[bool, Field(default=None, description="If enabled, the rule list item will preserve the path suffix.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add URLs to the rule list in Cloudflare. Supported Entities: URL. Note: URL entities are treated as "Source URLs".

Action Parameters: Rule Name: Specify the name of the rule list to which you want to add rule list items., Source URL: Specify the source URL for the rule list item., Description: Specify a description for the newly added rule list items., Status Code: Specify the status for the rule list item., Preserve Query String: If enabled, the rule list item preserves the query string., Include Subdomains: If enabled, the rule list item includes subdomains., Subpath Matching: If enabled, the rule list item matches the subpath., Preserve Path Suffix: If enabled, the rule list item preserves the path suffix.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name"] = rule_name
            script_params["Target URL"] = target_url
            if description is not None:
                script_params["Description"] = description
            if status_code is not None:
                script_params["Status Code"] = status_code
            if preserve_query_string is not None:
                script_params["Preserve Query String"] = preserve_query_string
            if include_subdomains is not None:
                script_params["Include Subdomains"] = include_subdomains
            if subpath_matching is not None:
                script_params["Subpath Matching"] = subpath_matching
            if preserve_path_suffix is not None:
                script_params["Preserve Path Suffix"] = preserve_path_suffix
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Cloudflare_Add URL To Rule List",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_Add URL To Rule List",
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
                print(f"Error executing action Cloudflare_Add URL To Rule List for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cloudflare_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Cloudflare with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
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
                actionName="Cloudflare_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_Ping",
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
                print(f"Error executing action Cloudflare_Ping for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cloudflare_update_firewall_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name: Annotated[str, Field(..., description="Specify the name of the rule that needs to be updated.")], zone_name: Annotated[str, Field(..., description="Specify the name of the zone, which will contain the firewall rule.")], action: Annotated[List[str], Field(default=None, description="Specify the action for the firewall rule. If \"Bypass\" is selected, you need to provide values in the \"Products\" parameter.")], expression: Annotated[str, Field(default=None, description="Specify the expression for the firewall rule.")], products: Annotated[str, Field(default=None, description="Specify a comma-separated list of products for the firewall rule. Note: this parameter is only mandatory, if \"Bypass\" is selected for \"Action\" parameter. Possible values: zoneLockdown, uaBlock, bic, hot, securityLevel, rateLimit, waf.")], priority: Annotated[str, Field(default=None, description="Specify the priority for the firewall rule.")], reference_tag: Annotated[str, Field(default=None, description="Specify a reference tag for the firewall rule. Note: it can only be up to 50 characters long.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a firewall rule in Cloudflare.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name"] = rule_name
            script_params["Zone Name"] = zone_name
            if action is not None:
                script_params["Action"] = action
            if expression is not None:
                script_params["Expression"] = expression
            if products is not None:
                script_params["Products"] = products
            if priority is not None:
                script_params["Priority"] = priority
            if reference_tag is not None:
                script_params["Reference Tag"] = reference_tag
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Cloudflare_Update Firewall Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_Update Firewall Rule",
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
                print(f"Error executing action Cloudflare_Update Firewall Rule for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cloudflare_create_rule_list(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], name: Annotated[str, Field(..., description="Specify the name for the rule list.")], type: Annotated[List[str], Field(default=None, description="Specify the type for the rule list.")], description: Annotated[str, Field(default=None, description="Specify the description for the rule list.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a rule list in Cloudflare.

Action Parameters: Name: Specify the name for the rule list., Type: Specify the type for the rule list., Description: Specify the description for the rule list.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Name"] = name
            if type is not None:
                script_params["Type"] = type
            if description is not None:
                script_params["Description"] = description
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Cloudflare_Create Rule List",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_Create Rule List",
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
                print(f"Error executing action Cloudflare_Create Rule List for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def cloudflare_create_firewall_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], zone_name: Annotated[str, Field(..., description="Specify the name of the zone, which will contain the firewall rule.")], expression: Annotated[str, Field(..., description="Specify the expression for the firewall rule.")], name: Annotated[str, Field(default=None, description="Specify the name for the firewall rule.")], action: Annotated[List[str], Field(default=None, description="Specify the action for the firewall rule. If \"Bypass\" is selected, you need to provide values in the \"Products\" parameter.")], products: Annotated[str, Field(default=None, description="Specify a comma-separated list of products for the firewall rule. Note: this parameter is only mandatory, if \"Bypass\" is selected for \"Action\" parameter. Possible values: zoneLockdown, uaBlock, bic, hot, securityLevel, rateLimit, waf.")], priority: Annotated[str, Field(default=None, description="Specify the priority for the firewall rule.")], reference_tag: Annotated[str, Field(default=None, description="Specify a reference tag for the firewall rule. Note: it can only be up to 50 characters long.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a firewall rule in Cloudflare.

Action Parameters: Zone Name: Specify the name of the zone, which contains the firewall rule., Name: Specify the name for the firewall rule., Action: Specify the action for the firewall rule.If "Block" is selected, you need to provide values in the "Products" parameter., Expression: Specify the expression for the firewall rule., Products: Specify a comma-separated list of products for the firewall rule.Note: This parameter is only mandatory, if "Bypass" is selected for the "Action" parameter.Possible values: zoneLockdown, uaBlock, bic, hot, securityLevel, rateLimit, waf, Priority: Specify the priority for the firewall rule., Reference Tag: Specify a reference tag for the firewall rule.Note: It can only be up to 50 characters long.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Cloudflare")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for Cloudflare: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Zone Name"] = zone_name
            if name is not None:
                script_params["Name"] = name
            if action is not None:
                script_params["Action"] = action
            script_params["Expression"] = expression
            if products is not None:
                script_params["Products"] = products
            if priority is not None:
                script_params["Priority"] = priority
            if reference_tag is not None:
                script_params["Reference Tag"] = reference_tag
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="Cloudflare_Create Firewall Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "Cloudflare_Create Firewall Rule",
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
                print(f"Error executing action Cloudflare_Create Firewall Rule for Cloudflare: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for Cloudflare")
            return {"Status": "Failed", "Message": "No active instance found."}
