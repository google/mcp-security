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
    # This function registers all tools (actions) for the VirusTotalV3 integration.

    @mcp.tool()
    async def virus_total_v3_add_comment_to_entity(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], comment: Annotated[str, Field(..., description="Specify the comment that should be added to entities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to entities in VirusTotal. Supported entities: File Hash, URL, Hostname, Domain, IP Address. Note: only MD5, SHA-1 and SHA-256 Hash types are supported

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Add Comment To Entity",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Add Comment To Entity",
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
                print(f"Error executing action VirusTotalV3_Add Comment To Entity for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_search_io_cs(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query according to the VirusTotal query search syntax.")], order_by: Annotated[List[str], Field(..., description="Specify the order by the selected field, in which results are returned. Default: Use Default Order. Note: Entity types might have different ordering fields. Refer to the VT Intelligence corpus https://docs.virustotal.com/reference/intelligence-search for more information.")], create_entities: Annotated[bool, Field(default=None, description="If enabled, action will create entities for the returned IOCs. Note: this action does not enrich entities.")], sort_order: Annotated[List[str], Field(default=None, description="Specify the direction in which the results should be returned. If \u201cUse Default Order\u201d is chosen for \u201cOrder By\u201d field, this parameter will be ignored.")], max_io_cs_to_return: Annotated[str, Field(default=None, description="Specify how many IOCs to return. Max IOCs to return is 300. Default: 10.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search for IOCs in the VirusTotal's dataset, using the same query syntax that you would use in the VirusTotal Intelligence user interface. This action requires a VT Enterprise token.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            if create_entities is not None:
                script_params["Create Entities"] = create_entities
            script_params["Order By"] = order_by
            if sort_order is not None:
                script_params["Sort Order"] = sort_order
            if max_io_cs_to_return is not None:
                script_params["Max IOCs To Return"] = max_io_cs_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Search IOCs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Search IOCs",
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
                print(f"Error executing action VirusTotalV3_Search IOCs for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_enrich_hash(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], engine_threshold: Annotated[str, Field(default=None, description="Specify how many engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.")], engine_percentage_threshold: Annotated[str, Field(default=None, description="Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.")], engine_whitelist: Annotated[str, Field(default=None, description="Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it\u2019s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".")], resubmit_hash: Annotated[bool, Field(default=None, description="If enabled, action will resubmit hashes for analysis instead of using the latest information.")], resubmit_after_days: Annotated[str, Field(default=None, description="Specify how many days since the last submission should pass for the entity to be submitted again. Note: parameter \"Resubmit Hash\" needs to be enabled.")], retrieve_comments: Annotated[bool, Field(default=None, description="If enabled, action will retrieve comments about the entity.")], retrieve_sigma_analysis: Annotated[bool, Field(default=None, description="If enabled, action will retrieve sigma analysis for the hash.")], sandbox: Annotated[str, Field(default=None, description="Specify a comma-separated list of sandbox names that should be used for behavior analysis. If nothing is provided, action will only use the \"VirusTotal Jujubox\" sandbox. Make sure that the spelling is correct. Examples of sandboxes: VirusTotal Jujubox, VirusTotal ZenBox, Microsoft Sysinternals, Tencent HABO.")], retrieve_sandbox_analysis: Annotated[bool, Field(default=None, description="If enabled, action will fetch sandbox analysis for the entity. For each sandbox, action will create a separate section in the JSON result. Action will only return data for the sandboxes that are provided in the parameter \"Sandbox\".")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about the entities.")], only_suspicious_entity_insight: Annotated[bool, Field(default=None, description="If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.")], max_comments_to_return: Annotated[str, Field(default=None, description="Specify how many comments to return. Default: 10.")], widget_theme: Annotated[List[str], Field(default=None, description="Specify the theme for the widget.")], fetch_widget: Annotated[bool, Field(default=None, description="If enabled, action will fetch augmented widget related to the entity.")], fetch_mitre_details: Annotated[bool, Field(default=None, description="If enabled, action will return information about related MITRE techniques and tactics.")], lowest_mitre_technique_severity: Annotated[List[str], Field(default=None, description="Specify the lowest signature severity related to MITRE technique for technique to be returned. \"Unknown\" severity is treated as \"Info\".")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich Hash using information from VirusTotal. Supported entities: Filehash. Note: only MD5, SHA-1 and SHA-256 are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if engine_threshold is not None:
                script_params["Engine Threshold"] = engine_threshold
            if engine_percentage_threshold is not None:
                script_params["Engine Percentage Threshold"] = engine_percentage_threshold
            if engine_whitelist is not None:
                script_params["Engine Whitelist"] = engine_whitelist
            if resubmit_hash is not None:
                script_params["Resubmit Hash"] = resubmit_hash
            if resubmit_after_days is not None:
                script_params["Resubmit After (Days)"] = resubmit_after_days
            if retrieve_comments is not None:
                script_params["Retrieve Comments"] = retrieve_comments
            if retrieve_sigma_analysis is not None:
                script_params["Retrieve Sigma Analysis"] = retrieve_sigma_analysis
            if sandbox is not None:
                script_params["Sandbox"] = sandbox
            if retrieve_sandbox_analysis is not None:
                script_params["Retrieve Sandbox Analysis"] = retrieve_sandbox_analysis
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if only_suspicious_entity_insight is not None:
                script_params["Only Suspicious Entity Insight"] = only_suspicious_entity_insight
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return
            if widget_theme is not None:
                script_params["Widget Theme"] = widget_theme
            if fetch_widget is not None:
                script_params["Fetch Widget"] = fetch_widget
            if fetch_mitre_details is not None:
                script_params["Fetch MITRE Details"] = fetch_mitre_details
            if lowest_mitre_technique_severity is not None:
                script_params["Lowest MITRE Technique Severity"] = lowest_mitre_technique_severity
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Enrich Hash",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Enrich Hash",
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
                print(f"Error executing action VirusTotalV3_Enrich Hash for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_get_related_i_ps(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], results: Annotated[List[str], Field(default=None, description="Specify how the JSON result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.")], max_i_ps_to_return: Annotated[str, Field(default=None, description="Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get related IPs to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if results is not None:
                script_params["Results"] = results
            if max_i_ps_to_return is not None:
                script_params["Max IPs To Return"] = max_i_ps_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Get Related IPs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Get Related IPs",
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
                print(f"Error executing action VirusTotalV3_Get Related IPs for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_get_related_domains(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], results: Annotated[List[str], Field(default=None, description="Specify how the JSON result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.")], max_domains_to_return: Annotated[str, Field(default=None, description="Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get related domains to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: IP, URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if results is not None:
                script_params["Results"] = results
            if max_domains_to_return is not None:
                script_params["Max Domains To Return"] = max_domains_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Get Related Domains",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Get Related Domains",
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
                print(f"Error executing action VirusTotalV3_Get Related Domains for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_enrich_ip(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], engine_threshold: Annotated[str, Field(default=None, description="Specify how many engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.")], engine_percentage_threshold: Annotated[str, Field(default=None, description="Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.")], engine_whitelist: Annotated[str, Field(default=None, description="Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it\u2019s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".")], retrieve_comments: Annotated[bool, Field(default=None, description="If enabled, action will retrieve comments about the entity.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about the entities.")], only_suspicious_entity_insight: Annotated[bool, Field(default=None, description="If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.")], max_comments_to_return: Annotated[str, Field(default=None, description="Specify how many comments to return. Default: 10")], widget_theme: Annotated[List[str], Field(default=None, description="Specify the theme for the widget.")], fetch_widget: Annotated[bool, Field(default=None, description="If enabled, action will fetch augmented widget related to the entity.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich IP using information from VirusTotal. Supported entities: IP address.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if engine_threshold is not None:
                script_params["Engine Threshold"] = engine_threshold
            if engine_percentage_threshold is not None:
                script_params["Engine Percentage Threshold"] = engine_percentage_threshold
            if engine_whitelist is not None:
                script_params["Engine Whitelist"] = engine_whitelist
            if retrieve_comments is not None:
                script_params["Retrieve Comments"] = retrieve_comments
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if only_suspicious_entity_insight is not None:
                script_params["Only Suspicious Entity Insight"] = only_suspicious_entity_insight
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return
            if widget_theme is not None:
                script_params["Widget Theme"] = widget_theme
            if fetch_widget is not None:
                script_params["Fetch Widget"] = fetch_widget
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Enrich IP",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Enrich IP",
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
                print(f"Error executing action VirusTotalV3_Enrich IP for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the VirusTotal with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
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
                actionName="VirusTotalV3_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Ping",
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
                print(f"Error executing action VirusTotalV3_Ping for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_get_domain_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], engine_threshold: Annotated[str, Field(default=None, description="Specify how many engines should mark the domain as malicious or suspicious, for Siemplify to label it as risky. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.")], engine_percentage_threshold: Annotated[str, Field(default=None, description="Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.")], engine_whitelist: Annotated[str, Field(default=None, description="Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it\u2019s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".")], retrieve_comments: Annotated[bool, Field(default=None, description="If enabled, action will retrieve comments about the entity.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about the entities.")], only_suspicious_entity_insight: Annotated[bool, Field(default=None, description="If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.")], max_comments_to_return: Annotated[str, Field(default=None, description="Specify how many comments to return. Default: 10.")], widget_theme: Annotated[List[str], Field(default=None, description="Specify the theme for the widget.")], fetch_widget: Annotated[bool, Field(default=None, description="If enabled, action will fetch augmented widget related to the entity.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get detailed information about the domain using information from VirusTotal. Supported entities: URL (entity extracts domain part), Hostname, Domain.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if engine_threshold is not None:
                script_params["Engine Threshold"] = engine_threshold
            if engine_percentage_threshold is not None:
                script_params["Engine Percentage Threshold"] = engine_percentage_threshold
            if engine_whitelist is not None:
                script_params["Engine Whitelist"] = engine_whitelist
            if retrieve_comments is not None:
                script_params["Retrieve Comments"] = retrieve_comments
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if only_suspicious_entity_insight is not None:
                script_params["Only Suspicious Entity Insight"] = only_suspicious_entity_insight
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return
            if widget_theme is not None:
                script_params["Widget Theme"] = widget_theme
            if fetch_widget is not None:
                script_params["Fetch Widget"] = fetch_widget
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Get Domain Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Get Domain Details",
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
                print(f"Error executing action VirusTotalV3_Get Domain Details for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_search_graphs(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], query: Annotated[str, Field(..., description="Specify the query filter for the graph. Please refer to the documentation portal for more details.")], sort_field: Annotated[List[str], Field(default=None, description="Specify what should be the sort field.")], max_graphs_to_return: Annotated[str, Field(default=None, description="Specify how many graphs to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search graphs based on custom filters in VirusTotal.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Query"] = query
            if sort_field is not None:
                script_params["Sort Field"] = sort_field
            if max_graphs_to_return is not None:
                script_params["Max Graphs To Return"] = max_graphs_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Search Graphs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Search Graphs",
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
                print(f"Error executing action VirusTotalV3_Search Graphs for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_search_entity_graphs(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], sort_field: Annotated[List[str], Field(default=None, description="Specify what should be the sort field.")], max_graphs_to_return: Annotated[str, Field(default=None, description="Specify how many graphs to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search graphs based on the entities in VirusTotal. Supported entities: IP, URL, Filehash, Hostname, Domain, Threat Actor, User. Note: only MD5, SHA-1 and SHA-256 are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if sort_field is not None:
                script_params["Sort Field"] = sort_field
            if max_graphs_to_return is not None:
                script_params["Max Graphs To Return"] = max_graphs_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Search Entity Graphs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Search Entity Graphs",
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
                print(f"Error executing action VirusTotalV3_Search Entity Graphs for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_enrich_ioc(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], io_cs: Annotated[str, Field(..., description="Specify a comma-separated list of IOCs for which you want to ingest data.")], ioc_type: Annotated[List[str], Field(default=None, description="Specify the type of the IOC.")], widget_theme: Annotated[List[str], Field(default=None, description="Specify the theme for the widget.")], fetch_widget: Annotated[bool, Field(default=None, description="If enabled, action will fetch augmented widget related to the entity.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich IOCs using information from VirusTotal.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if ioc_type is not None:
                script_params["IOC Type"] = ioc_type
            script_params["IOCs"] = io_cs
            if widget_theme is not None:
                script_params["Widget Theme"] = widget_theme
            if fetch_widget is not None:
                script_params["Fetch Widget"] = fetch_widget
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Enrich IOC",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Enrich IOC",
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
                print(f"Error executing action VirusTotalV3_Enrich IOC for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_download_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], download_folder_path: Annotated[str, Field(..., description="Specify the path to the folder, where you want to store the files.")], overwrite: Annotated[bool, Field(default=None, description="If enabled, action will overwrite the file with the same name.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Download file from VirusTotal. Supported entities: Filehash. Note: this action requires a VT Enterprise token. Only MD5, SHA-1, SHA-256 hashes are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Download Folder Path"] = download_folder_path
            if overwrite is not None:
                script_params["Overwrite"] = overwrite
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Download File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Download File",
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
                print(f"Error executing action VirusTotalV3_Download File for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_get_related_hashes(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], results: Annotated[List[str], Field(default=None, description="Specify how the JSON result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.")], max_hashes_to_return: Annotated[str, Field(default=None, description="Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get related hashes to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: IP, URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if results is not None:
                script_params["Results"] = results
            if max_hashes_to_return is not None:
                script_params["Max Hashes To Return"] = max_hashes_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Get Related Hashes",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Get Related Hashes",
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
                print(f"Error executing action VirusTotalV3_Get Related Hashes for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_add_vote_to_entity(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], vote: Annotated[List[str], Field(..., description="Specify the vote that should be added to entities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a vote to entities in VirusTotal. Supported entities: File Hash, URL, Hostname, Domain, IP Address. Note: only MD5, SHA-1 and SHA-256 Hash types are supported

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Vote"] = vote
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Add Vote To Entity",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Add Vote To Entity",
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
                print(f"Error executing action VirusTotalV3_Add Vote To Entity for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_get_graph_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], graph_id: Annotated[str, Field(..., description="Specify a comma-separated list of graph ids for which you want to retrieve detailed information.")], max_links_to_return: Annotated[str, Field(default=None, description="Specify how many links to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get detailed information about graphs in VirusTotal.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Graph ID"] = graph_id
            if max_links_to_return is not None:
                script_params["Max Links To Return"] = max_links_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Get Graph Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Get Graph Details",
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
                print(f"Error executing action VirusTotalV3_Get Graph Details for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_enrich_url(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], engine_threshold: Annotated[str, Field(default=None, description="Specify how many engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.")], engine_percentage_threshold: Annotated[str, Field(default=None, description="Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.")], engine_whitelist: Annotated[str, Field(default=None, description="Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it\u2019s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".")], resubmit_url: Annotated[bool, Field(default=None, description="If enabled, action will resubmit urls for analysis instead of using the latest information.")], retrieve_comments: Annotated[bool, Field(default=None, description="If enabled, action will retrieve comments about the entity.")], only_suspicious_entity_insight: Annotated[bool, Field(default=None, description="If enabled, action will only create an insight for suspicious entities. Note: parameter \"Create Insight\" should be enabled.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight containing information about the entities.")], max_comments_to_return: Annotated[str, Field(default=None, description="Specify how many comments to return. Default: 10.")], resubmit_after_days: Annotated[str, Field(default=None, description="Specify how many days since the last submission should pass for the entity to be submitted again. Note: parameter \"Resubmit URL\" needs to be enabled. Default: 30.")], widget_theme: Annotated[List[str], Field(default=None, description="Specify the theme for the widget.")], fetch_widget: Annotated[bool, Field(default=None, description="If enabled, action will fetch augmented widget related to the entity.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich URL using information from VirusTotal. Supported entities: URL.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if engine_threshold is not None:
                script_params["Engine Threshold"] = engine_threshold
            if engine_percentage_threshold is not None:
                script_params["Engine Percentage Threshold"] = engine_percentage_threshold
            if engine_whitelist is not None:
                script_params["Engine Whitelist"] = engine_whitelist
            if resubmit_url is not None:
                script_params["Resubmit URL"] = resubmit_url
            if retrieve_comments is not None:
                script_params["Retrieve Comments"] = retrieve_comments
            if only_suspicious_entity_insight is not None:
                script_params["Only Suspicious Entity Insight"] = only_suspicious_entity_insight
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return
            if resubmit_after_days is not None:
                script_params["Resubmit After (Days)"] = resubmit_after_days
            if widget_theme is not None:
                script_params["Widget Theme"] = widget_theme
            if fetch_widget is not None:
                script_params["Fetch Widget"] = fetch_widget
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Enrich URL",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Enrich URL",
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
                print(f"Error executing action VirusTotalV3_Enrich URL for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_submit_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], file_paths: Annotated[str, Field(..., description="Specify a comma-separated list of absolute file paths. Note: if \"Linux Server Address\" is specified, action will try to fetch file from remote server.")], engine_threshold: Annotated[str, Field(default=None, description="Specify how many engines should mark the file as malicious or suspicious, for Siemplify to label it as risky. Note: if \"Engine Whitelist\" contains values, action will only count results from those engines.")], engine_percentage_threshold: Annotated[str, Field(default=None, description="Specify the percentage of engines should mark the entity as malicious or suspicious, for Siemplify to label it as suspicious. Note: if \"Engine Whitelist\" contains values, action will only count the percentage from those engines. If both \"Engine Threshold\" and \"Engine Percentage Threshold\" are provided, \"Engine Threshold\" will be used. Maximum value: 100. Minimum: 0.")], engine_whitelist: Annotated[str, Field(default=None, description="Specify a comma-separated list of engines that should be used to retrieve information, whether an entity is malicious or not. Example: AlienVault,Kaspersky. Note: if nothing is specified in this parameter, action will take results from every available engine. If the engine didn't return any information about the entity it\u2019s not going to be counted for the parameters \"Engine Threshold\" and \"Engine Percentage Threshold\".")], retrieve_comments: Annotated[bool, Field(default=None, description="If enabled, action will retrieve comments about the entity.")], max_comments_to_return: Annotated[str, Field(default=None, description="Specify how many comments to return.")], linux_server_address: Annotated[str, Field(default=None, description="Specify the IP address of the remote linux server, where the file is located.")], linux_username: Annotated[str, Field(default=None, description="Specify the username of the remote linux server, where the file is located.")], linux_password: Annotated[str, Field(default=None, description="Specify the password of the remote linux server, where the file is located.")], private_submission: Annotated[bool, Field(default=None, description="If enabled, action will submit the file privately. Note: this functionality requires premium VT access.")], fetch_mitre_details: Annotated[bool, Field(default=None, description="If enabled, action will return information about related MITRE techniques and tactics.")], lowest_mitre_technique_severity: Annotated[List[str], Field(default=None, description="Specify the lowest signature severity related to MITRE technique for technique to be returned. \"Unknown\" severity is treated as \"Info\".")], retrieve_ai_summary: Annotated[bool, Field(default=None, description="Experimental. If enabled, action will retrieve an AI Summary for the submitted file. AI Summary is only available for private submissions.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Submit a file and return results from VirusTotal.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["File Paths"] = file_paths
            if engine_threshold is not None:
                script_params["Engine Threshold"] = engine_threshold
            if engine_percentage_threshold is not None:
                script_params["Engine Percentage Threshold"] = engine_percentage_threshold
            if engine_whitelist is not None:
                script_params["Engine Whitelist"] = engine_whitelist
            if retrieve_comments is not None:
                script_params["Retrieve Comments"] = retrieve_comments
            if max_comments_to_return is not None:
                script_params["Max Comments To Return"] = max_comments_to_return
            if linux_server_address is not None:
                script_params["Linux Server Address"] = linux_server_address
            if linux_username is not None:
                script_params["Linux Username"] = linux_username
            if linux_password is not None:
                script_params["Linux Password"] = linux_password
            if private_submission is not None:
                script_params["Private Submission"] = private_submission
            if fetch_mitre_details is not None:
                script_params["Fetch MITRE Details"] = fetch_mitre_details
            if lowest_mitre_technique_severity is not None:
                script_params["Lowest MITRE Technique Severity"] = lowest_mitre_technique_severity
            if retrieve_ai_summary is not None:
                script_params["Retrieve AI Summary"] = retrieve_ai_summary
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Submit File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Submit File",
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
                print(f"Error executing action VirusTotalV3_Submit File for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def virus_total_v3_get_related_ur_ls(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], results: Annotated[List[str], Field(default=None, description="Specify how the JSON  result should look like. If \"Combined\" is selected then action will return all of the unique results that were found among the provided entities. If \"Per Entity\" is selected, then action will return all of the unique items per entity.")], max_ur_ls_to_return: Annotated[str, Field(default=None, description="Specify how many URLs to return. Depending on the parameter \"Results\", this parameter will behave differently. For \"Combined\" the limit will define how many results to return from ALL entities. For \"Per Entity\" this parameter dictates how many results to return per entity. Default: 40.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get related urls to the provided entities from VirusTotal. Note: this action requires a VT Enterprise token. Supported entities: IP, URL, Filehash, Hostname, Domain. Note: only MD5, SHA-1 and SHA-256 are supported.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="VirusTotalV3")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for VirusTotalV3: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if results is not None:
                script_params["Results"] = results
            if max_ur_ls_to_return is not None:
                script_params["Max URLs To Return"] = max_ur_ls_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="VirusTotalV3_Get Related URLs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "VirusTotalV3_Get Related URLs",
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
                print(f"Error executing action VirusTotalV3_Get Related URLs for VirusTotalV3: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for VirusTotalV3")
            return {"Status": "Failed", "Message": "No active instance found."}
