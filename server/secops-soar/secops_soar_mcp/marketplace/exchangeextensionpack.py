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
    # This function registers all tools (actions) for the ExchangeExtensionPack integration.

    @mcp.tool()
    async def exchange_extension_pack_add_senders_to_exchange_siemplify_mail_flow_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_add_senders_to: Annotated[List[str], Field(..., description="Specify the rule to add the sender to. If the rule doesn't exist - action will create it where it's missing.")], email_addresses: Annotated[str, Field(default=None, description="Specify the email addresses you would like to add to the rule, in a comma separated list. If no parameter will be provided, action will work with User entities.")], should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well: Annotated[bool, Field(default=None, description="Specify whether the action should automatically take the domains of the provided email addresses and add them as well to the corresponding domain rules (same rule action for domains)")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Email Addresses, or will work on User entities with Email regexes (if parameters are not provided), and will be able to create a new rule,filtering the senders from your Exchange Server. Actions can be modified in the parameters using the rule parameter. Note - to use this action, please make sure you have Organization Management permissions, as stated here: https://docs.microsoft.com/en-us/exchange/permissions-exo/feature-permissions

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if email_addresses is not None:
                script_params["Email Addresses"] = email_addresses
            script_params["Rule to add senders to"] = rule_to_add_senders_to
            if should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well is not None:
                script_params["Should add senders' domain to the corresponding Domains List rule as well?"] = should_add_senders_domain_to_the_corresponding_domains_list_rule_as_well
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Add Senders to Exchange-Siemplify Mail Flow Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Add Senders to Exchange-Siemplify Mail Flow Rule",
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
                print(f"Error executing action ExchangeExtensionPack_Add Senders to Exchange-Siemplify Mail Flow Rule for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_fetch_compliance_search_results(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], compliance_search_name: Annotated[str, Field(..., description="Name for the Compliance Search. Note that name shouldn't contain special characters.")], max_emails_to_return: Annotated[str, Field(default=None, description="Specify how many emails action can return.")], remove_compliance_search_once_action_completes: Annotated[bool, Field(default=None, description="Specify whether action should remove from Exchange server the search action and any related fetch or purge tasks once the action completes.")], create_case_wall_output_table: Annotated[bool, Field(default=None, description="Specify if action should create case wall output table. If Max Emails To Return is set to a bigger number, its recommended to uncheck this to increase action performance.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Fetch results for the completed Compliance Search. Note: Action is not working on Siemplify entities. Note2: Maximum of 200 elements will be displayed, but actual search can have more findings that are shown.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Compliance Search Name"] = compliance_search_name
            if max_emails_to_return is not None:
                script_params["Max Emails To Return"] = max_emails_to_return
            if remove_compliance_search_once_action_completes is not None:
                script_params["Remove Compliance Search Once Action Completes?"] = remove_compliance_search_once_action_completes
            if create_case_wall_output_table is not None:
                script_params["Create Case Wall Output Table?"] = create_case_wall_output_table
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Fetch Compliance Search Results",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Fetch Compliance Search Results",
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
                print(f"Error executing action ExchangeExtensionPack_Fetch Compliance Search Results for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_remove_domains_from_exchange_siemplify_mail_flow_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_remove_domains_from: Annotated[List[str], Field(..., description="Specify the rule to remove the Domains from. If the rule doesn't exist - action will do nothing.")], domains: Annotated[str, Field(default=None, description="Specify the Domains you would like to remove from the rule, in a comma separated list.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Domains, and will be able to remove the provided domains from the existing rules. Note - to use this action, please make sure you have Organization Management permissions, as stated here: https://docs.microsoft.com/en-us/exchange/permissions-exo/feature-permissions

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if domains is not None:
                script_params["Domains"] = domains
            script_params["Rule to remove Domains from"] = rule_to_remove_domains_from
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Remove Domains from Exchange-Siemplify Mail Flow Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Remove Domains from Exchange-Siemplify Mail Flow Rules",
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
                print(f"Error executing action ExchangeExtensionPack_Remove Domains from Exchange-Siemplify Mail Flow Rules for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_delete_compliance_search(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], compliance_search_name: Annotated[str, Field(..., description="Name for the Compliance Search. Note that name shouldn't contain special characters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete Compliance Search and any associated with it fetch results or purge emails tasks. Note: Action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Compliance Search Name"] = compliance_search_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Delete Compliance Search",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Delete Compliance Search",
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
                print(f"Error executing action ExchangeExtensionPack_Delete Compliance Search for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_purge_compliance_search_results(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], compliance_search_name: Annotated[str, Field(..., description="Name for the Compliance Search. Note that name shouldn't contain special characters.")], perform_a_hard_delete_for_deleted_emails: Annotated[bool, Field(default=None, description="Specify whether HardDelete should be performed. This option is applies only to O365 and mark emails for permanent removal from the mailbox.")], remove_compliance_search_once_action_completes: Annotated[bool, Field(default=None, description="Specify whether action should remove from Exchange server the search action and any related fetch or purge tasks once the action completes.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Purge emails found by the completed Compliance Search. Note: Action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Compliance Search Name"] = compliance_search_name
            if perform_a_hard_delete_for_deleted_emails is not None:
                script_params["Perform a HardDelete for deleted emails?"] = perform_a_hard_delete_for_deleted_emails
            if remove_compliance_search_once_action_completes is not None:
                script_params["Remove Compliance Search Once Action Completes?"] = remove_compliance_search_once_action_completes
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Purge Compliance Search Results",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Purge Compliance Search Results",
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
                print(f"Error executing action ExchangeExtensionPack_Purge Compliance Search Results for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_add_domains_to_exchange_siemplify_mail_flow_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_add_domains_to: Annotated[List[str], Field(..., description="Specify the rule to add the Domains to. If the rule doesn't exist - action will create it where it's missing.")], domains: Annotated[str, Field(default=None, description="Specify the Domains you would like to add to the rule, in a comma separated list.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Domains, and will be able to create a new rule, filtering the domains from your Exchange Server. Actions to take can be modified in the parameters using rule parameters. Note - to use this action, please make sure you have Organization Management permissions, as stated here: https://docs.microsoft.com/en-us/exchange/permissions-exo/feature-permissions

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if domains is not None:
                script_params["Domains"] = domains
            script_params["Rule to add Domains to"] = rule_to_add_domains_to
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Add Domains to Exchange-Siemplify Mail Flow Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Add Domains to Exchange-Siemplify Mail Flow Rules",
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
                print(f"Error executing action ExchangeExtensionPack_Add Domains to Exchange-Siemplify Mail Flow Rules for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_remove_senders_from_exchange_siemplify_mail_flow_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_to_remove_senders_from: Annotated[List[str], Field(..., description="Specify the rule to remove the Senders from. If the rule doesn't exist - action will do nothing.")], email_addresses: Annotated[str, Field(default=None, description="Specify the email addresses you would like to remove from the rule, in a comma separated list. If no parameter will be provided, action will work with entities.")], should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well: Annotated[bool, Field(default=None, description="Specify whether the action should automatically take the domains of the provided email addresses and remove them as well from the corresponding domain rules (same rule action for domains)")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a list of Senders, or will work on User entities (if parameters are not provided), and will be able to remove the provided Senders from the existing rules. Note - to use this action, please make sure you have Organization Management permissions, as stated here: https://docs.microsoft.com/en-us/exchange/permissions-exo/feature-permissions

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if email_addresses is not None:
                script_params["Email Addresses"] = email_addresses
            script_params["Rule to remove Senders from"] = rule_to_remove_senders_from
            if should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well is not None:
                script_params["Should remove senders' domains from the corresponding Domains List rule as well?"] = should_remove_senders_domains_from_the_corresponding_domains_list_rule_as_well
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Remove Senders from Exchange-Siemplify Mail Flow Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Remove Senders from Exchange-Siemplify Mail Flow Rules",
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
                print(f"Error executing action ExchangeExtensionPack_Remove Senders from Exchange-Siemplify Mail Flow Rules for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Exchange or O365 server with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
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
                actionName="ExchangeExtensionPack_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Ping",
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
                print(f"Error executing action ExchangeExtensionPack_Ping for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_run_compliance_search(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], compliance_search_name: Annotated[str, Field(..., description="Name for the Compliance Search. Note that name shouldn't contain special characters.")], location_to_search_emails_in: Annotated[str, Field(..., description="Location to search emails in, can be one of the following: Comma separate list of mailboxes. A distribution group or mail-enabled security group All - for all mailboxes in organization.")], subject_filter: Annotated[str, Field(default=None, description="Filter condition, specify what subject to search for emails")], sender_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the sender of needed emails")], recipient_filter: Annotated[str, Field(default=None, description="Filter condition, specify who should be the recipient of needed emails")], operator: Annotated[List[str], Field(default=None, description="Operator to use to construct query from conditions above.")], time_frame_hours: Annotated[str, Field(default=None, description="Time frame interval in hours to search for emails.")], fetch_compliance_search_results: Annotated[bool, Field(default=None, description="Specify whether the action should immediately fetch the compliance search results. Note that maximum of 200 elements will be displayed, but actual search can have more findings that are shown.")], max_emails_to_return: Annotated[str, Field(default=None, description="Specify how many emails action can return.")], create_case_wall_output_table: Annotated[bool, Field(default=None, description="Specify if action should create case wall output table. If Max Emails To Return is set to a bigger number, its recommended to uncheck this to increase action performance.")], advanced_query: Annotated[str, Field(default=None, description="Instead of subject, sender or recipient filters, provide a query you want to run compliance search on. Consider https://docs.microsoft.com/en-us/sharepoint/dev/general-development/keyword-query-language-kql-syntax-reference and https://docs.microsoft.com/en-us/exchange/message-properties-indexed-by-exchange-search-exchange-2013-help?redirectedfrom=MSDN for reference on query syntax.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Run Exchange Compliance Search based on the provided search conditions. If the fetch compliance search results checkbox is set, action returns the search results similarly to the fetch compliance search results action. Exchange Compliance Search provides a fast mechanism to search in multiple mailboxes that will be most useful for large Organizations with 1000+ mailboxes. Note: Action is not working on Siemplify entities.  Note2: If "Fetch Compliance Search Results?" checkbox is checked, maximum of 200 elements will be displayed, but actual search can have more findings that are shown.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Compliance Search Name"] = compliance_search_name
            if subject_filter is not None:
                script_params["Subject Filter"] = subject_filter
            if sender_filter is not None:
                script_params["Sender Filter"] = sender_filter
            if recipient_filter is not None:
                script_params["Recipient Filter"] = recipient_filter
            if operator is not None:
                script_params["Operator"] = operator
            if time_frame_hours is not None:
                script_params["Time Frame (hours)"] = time_frame_hours
            script_params["Location to Search Emails In"] = location_to_search_emails_in
            if fetch_compliance_search_results is not None:
                script_params["Fetch Compliance Search Results?"] = fetch_compliance_search_results
            if max_emails_to_return is not None:
                script_params["Max Emails To Return"] = max_emails_to_return
            if create_case_wall_output_table is not None:
                script_params["Create Case Wall Output Table?"] = create_case_wall_output_table
            if advanced_query is not None:
                script_params["Advanced Query"] = advanced_query
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Run Compliance Search",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Run Compliance Search",
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
                print(f"Error executing action ExchangeExtensionPack_Run Compliance Search for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_list_exchange_siemplify_mail_flow_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name_to_list: Annotated[List[str], Field(..., description="Specify the Rule name you would like to list")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a rule name and will list it. Note - to use this action, please make sure you have Organization Management permissions, as stated here: https://docs.microsoft.com/en-us/exchange/permissions-exo/feature-permissions

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name To List"] = rule_name_to_list
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_List Exchange-Siemplify Mail Flow Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_List Exchange-Siemplify Mail Flow Rules",
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
                print(f"Error executing action ExchangeExtensionPack_List Exchange-Siemplify Mail Flow Rules for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def exchange_extension_pack_delete_exchange_siemplify_mail_flow_rules(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], rule_name_to_delete: Annotated[List[str], Field(..., description="Specify the Rule name you would like to completely delete")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Action will get as a parameter a rule name and will delete it. Note - to use this action, please make sure you have Organization Management permissions, as stated here: https://docs.microsoft.com/en-us/exchange/permissions-exo/feature-permissions

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="ExchangeExtensionPack")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for ExchangeExtensionPack: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Rule Name To Delete"] = rule_name_to_delete
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="ExchangeExtensionPack_Delete Exchange-Siemplify Mail Flow Rules",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "ExchangeExtensionPack_Delete Exchange-Siemplify Mail Flow Rules",
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
                print(f"Error executing action ExchangeExtensionPack_Delete Exchange-Siemplify Mail Flow Rules for ExchangeExtensionPack: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for ExchangeExtensionPack")
            return {"Status": "Failed", "Message": "No active instance found."}
