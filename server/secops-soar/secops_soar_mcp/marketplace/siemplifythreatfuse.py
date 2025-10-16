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
    # This function registers all tools (actions) for the SiemplifyThreatFuse integration.

    @mcp.tool()
    async def siemplify_threat_fuse_get_related_i_ps(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], confidence_threshold: Annotated[str, Field(..., description="Specify what should be the confidence threshold. Note: Maximum is 100.")], search_observables: Annotated[bool, Field(..., description="If enabled, action will search among observables.")], search_threat_bulletins: Annotated[bool, Field(..., description="If enabled, action will search among threat bulletins.")], search_actors: Annotated[bool, Field(..., description="If enabled, action will search among actors.")], search_attack_patterns: Annotated[bool, Field(..., description="If enabled, action will search among attack patterns.")], search_campaigns: Annotated[bool, Field(..., description="If enabled, action will search among campaigns.")], search_courses_of_action: Annotated[bool, Field(..., description="If enabled, action will search among courses of action.")], search_identities: Annotated[bool, Field(..., description="If enabled, action will search among identities.")], search_incidents: Annotated[bool, Field(..., description="If enabled, action will search among incidents.")], search_infrastructures: Annotated[bool, Field(..., description="If enabled, action will search among infrastructures.")], search_intrusion_sets: Annotated[bool, Field(..., description="If enabled, action will search among intrusion sets.")], search_malware: Annotated[bool, Field(..., description="If enabled, action will search among malware.")], search_signatures: Annotated[bool, Field(..., description="If enabled, action will search among signatures.")], search_tools: Annotated[bool, Field(..., description="If enabled, action will search among tools.")], search_tt_ps: Annotated[bool, Field(..., description="If enabled, action will search among TTPs.")], search_vulnerabilities: Annotated[bool, Field(..., description="If enabled, action will search among vulnerabilities.")], max_i_ps_to_return: Annotated[str, Field(default=None, description="Specify how many IPs to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related IP addresses based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Confidence Threshold"] = confidence_threshold
            script_params["Search Observables"] = search_observables
            script_params["Search Threat Bulletins"] = search_threat_bulletins
            script_params["Search Actors"] = search_actors
            script_params["Search Attack Patterns"] = search_attack_patterns
            script_params["Search Campaigns"] = search_campaigns
            script_params["Search Courses Of Action"] = search_courses_of_action
            script_params["Search Identities"] = search_identities
            script_params["Search Incidents"] = search_incidents
            script_params["Search Infrastructures"] = search_infrastructures
            script_params["Search Intrusion Sets"] = search_intrusion_sets
            script_params["Search Malware"] = search_malware
            script_params["Search Signatures"] = search_signatures
            script_params["Search Tools"] = search_tools
            script_params["Search TTPs"] = search_tt_ps
            script_params["Search Vulnerabilities"] = search_vulnerabilities
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
                actionName="SiemplifyThreatFuse_Get Related IPs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Get Related IPs",
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
                print(f"Error executing action SiemplifyThreatFuse_Get Related IPs for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_get_related_domains(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], confidence_threshold: Annotated[str, Field(..., description="Specify what should be the confidence threshold. Note: Maximum is 100.")], search_threat_bulletins: Annotated[bool, Field(..., description="If enabled, action will search among threat bulletins.")], search_actors: Annotated[bool, Field(..., description="If enabled, action will search among actors.")], search_attack_patterns: Annotated[bool, Field(..., description="If enabled, action will search among attack patterns.")], search_campaigns: Annotated[bool, Field(..., description="If enabled, action will search among campaigns.")], search_courses_of_action: Annotated[bool, Field(..., description="If enabled, action will search among courses of action.")], search_identities: Annotated[bool, Field(..., description="If enabled, action will search among identities.")], search_incidents: Annotated[bool, Field(..., description="If enabled, action will search among incidents.")], search_infrastructures: Annotated[bool, Field(..., description="If enabled, action will search among infrastructures.")], search_intrusion_sets: Annotated[bool, Field(..., description="If enabled, action will search among intrusion sets.")], search_malware: Annotated[bool, Field(..., description="If enabled, action will search among malware.")], search_signatures: Annotated[bool, Field(..., description="If enabled, action will search among signatures.")], search_tools: Annotated[bool, Field(..., description="If enabled, action will search among tools.")], search_tt_ps: Annotated[bool, Field(..., description="If enabled, action will search among TTPs.")], search_vulnerabilities: Annotated[bool, Field(..., description="If enabled, action will search among vulnerabilities.")], max_domains_to_return: Annotated[str, Field(default=None, description="Specify how many domains to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related domains based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Confidence Threshold"] = confidence_threshold
            script_params["Search Threat Bulletins"] = search_threat_bulletins
            script_params["Search Actors"] = search_actors
            script_params["Search Attack Patterns"] = search_attack_patterns
            script_params["Search Campaigns"] = search_campaigns
            script_params["Search Courses Of Action"] = search_courses_of_action
            script_params["Search Identities"] = search_identities
            script_params["Search Incidents"] = search_incidents
            script_params["Search Infrastructures"] = search_infrastructures
            script_params["Search Intrusion Sets"] = search_intrusion_sets
            script_params["Search Malware"] = search_malware
            script_params["Search Signatures"] = search_signatures
            script_params["Search Tools"] = search_tools
            script_params["Search TTPs"] = search_tt_ps
            script_params["Search Vulnerabilities"] = search_vulnerabilities
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
                actionName="SiemplifyThreatFuse_Get Related Domains",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Get Related Domains",
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
                print(f"Error executing action SiemplifyThreatFuse_Get Related Domains for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Siemplify ThreatFuse with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
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
                actionName="SiemplifyThreatFuse_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Ping",
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
                print(f"Error executing action SiemplifyThreatFuse_Ping for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_submit_observables(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], classification: Annotated[List[str], Field(..., description="Specify the classification of the observable.")], threat_type: Annotated[List[str], Field(..., description="Specify the threat type of the observables.")], source: Annotated[str, Field(default=None, description="Specify the intelligence source for the observable.")], expiration_date: Annotated[str, Field(default=None, description="Specify the expiration date in days for the observable. If nothing is specified here, action will create an observable that will never expire.")], trusted_circle_i_ds: Annotated[str, Field(default=None, description="Specify the comma-separated list of trusted circle ids. Observables will be shared with those trusted circles.")], tlp: Annotated[List[str], Field(default=None, description="Specify the TLP for your observables.")], confidence: Annotated[str, Field(default=None, description="Specify what should be the confidence for the observable. Note: this parameter will only work, if you create observables in your organization and requires 'Override System Confidence' to be enabled.")], override_system_confidence: Annotated[bool, Field(default=None, description="If enabled, created observables will have the confidence specified in the 'Confidence' parameter. Note: you can't share observables in trusted circles and publicly, when this parameter is enabled.")], anonymous_submission: Annotated[bool, Field(default=None, description="If enabled, action will make an anonymous submission.")], tags: Annotated[str, Field(default=None, description="Specify a comma-separated list of tags that you want to add to observable.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Submit an observable to Siemplify ThreatFuse based on IP, URL, Hash or User entities with Email regexes from Siemplify ThreatFuse. Note: requires 'Org admin', 'Create Anomali Community Intel' and 'Approve Intel' permissions.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Classification"] = classification
            script_params["Threat Type"] = threat_type
            if source is not None:
                script_params["Source"] = source
            if expiration_date is not None:
                script_params["Expiration Date"] = expiration_date
            if trusted_circle_i_ds is not None:
                script_params["Trusted Circle IDs"] = trusted_circle_i_ds
            if tlp is not None:
                script_params["TLP"] = tlp
            if confidence is not None:
                script_params["Confidence"] = confidence
            if override_system_confidence is not None:
                script_params["Override System Confidence"] = override_system_confidence
            if anonymous_submission is not None:
                script_params["Anonymous Submission"] = anonymous_submission
            if tags is not None:
                script_params["Tags"] = tags
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SiemplifyThreatFuse_Submit Observables",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Submit Observables",
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
                print(f"Error executing action SiemplifyThreatFuse_Submit Observables for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_get_related_associations(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], return_campaigns: Annotated[bool, Field(default=None, description="If enabled, action will fetch related campaigns and details about them.")], return_threat_bulletins: Annotated[bool, Field(default=None, description="If enabled, action will fetch related threat bulletins and details about them.")], return_actors: Annotated[bool, Field(default=None, description="If enabled, action will fetch related actors and details about them.")], return_attack_patterns: Annotated[bool, Field(default=None, description="If enabled, action will fetch related attack patterns and details about them.")], return_courses_of_action: Annotated[bool, Field(default=None, description="If enabled, action will fetch related courses of action and details about them.")], return_identities: Annotated[bool, Field(default=None, description="If enabled, action will fetch related identities and details about them.")], return_incidents: Annotated[bool, Field(default=None, description="If enabled, action will fetch related incidents and details about them.")], return_infrastructure: Annotated[bool, Field(default=None, description="If enabled, action will fetch related infrastructure and details about them.")], return_intrusion_sets: Annotated[bool, Field(default=None, description="If enabled, action will fetch related intrusion sets and details about them.")], return_malware: Annotated[bool, Field(default=None, description="If enabled, action will fetch related malware and details about them.")], return_signatures: Annotated[bool, Field(default=None, description="If enabled, action will fetch related signatures and details about them.")], return_tools: Annotated[bool, Field(default=None, description="If enabled, action will fetch related tools and details about them.")], return_tt_ps: Annotated[bool, Field(default=None, description="If enabled, action will fetch related TTPs and details about them.")], return_vulnerabilities: Annotated[bool, Field(default=None, description="If enabled, action will fetch related vulnerabilities and details about them.")], create_campaign_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \u201cCampaign\u201d associations.")], create_actors_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \u201cActor\u201d associations.")], create_signature_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \u201cSignature\u201d associations.")], create_vulnerability_entity: Annotated[bool, Field(default=None, description="If enabled, action will create an entity out of available \u201cVulnerability\u201d associations.")], create_case_tag: Annotated[bool, Field(default=None, description="If enabled, action will create case tags based on the results.")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will create an insight base on the results.")], max_associations_to_return: Annotated[str, Field(default=None, description="Specify how many associations to return per type. Default: 5")], max_statistics_to_return: Annotated[str, Field(default=None, description="Specify how many top statistics results regarding IOCs to return. Note: action will at max process 1000 IOCs related to the association. If you provide \"0\", action will not try to fetch statistics information.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related associations from Siemplify ThreatFuse. Configure the parameters below: choose the association types to return, specify Max Associations To Return. You can also choose to add retrieved associations as entities to the case.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
            if create_case_tag is not None:
                script_params["Create Case Tag"] = create_case_tag
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if max_associations_to_return is not None:
                script_params["Max Associations To Return"] = max_associations_to_return
            if max_statistics_to_return is not None:
                script_params["Max Statistics To Return"] = max_statistics_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SiemplifyThreatFuse_Get Related Associations",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Get Related Associations",
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
                print(f"Error executing action SiemplifyThreatFuse_Get Related Associations for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], severity_threshold: Annotated[List[str], Field(..., description="Specify what should be the severity threshold for the entity, in order to mark it as suspicious. If multiple records are found for the same entity, action will take the highest severity out of all available records.")], confidence_threshold: Annotated[str, Field(..., description="Specify what should be the confidence threshold for the entity, in order to mark it as suspicious. Note: Maximum is 100. If multiple records are found for the entity, action will take the average. Active records have priority.")], ignore_false_positive_status: Annotated[bool, Field(default=None, description="If enabled, action will ignore the false positive status and mark the entity as suspicious based on the \"Severity Threshold\" and \"Confidence Threshold\". If disabled, action will never label false positive entities as suspicious, regardless, if they pass the \"Severity Threshold\" and \"Confidence Threshold\" conditions or not.")], add_threat_type_to_case: Annotated[bool, Field(default=None, description="If enabled, action will add threat types of the entity from all records as tags to the case. Example: apt")], create_insight: Annotated[bool, Field(default=None, description="If enabled, action will add an insight per processed entity.")], only_suspicious_entity_insight: Annotated[bool, Field(default=None, description="If enabled, action will create insight only for entities that exceeded the \"Severity Threshold\" and \"Confidence Threshold\".")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about IPs, URLs, hashes or User entities with Email regexes from Siemplify ThreatFuse. If multiple records are found for the same entity, action will enrich using the latest record.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Severity Threshold"] = severity_threshold
            script_params["Confidence Threshold"] = confidence_threshold
            if ignore_false_positive_status is not None:
                script_params["Ignore False Positive Status"] = ignore_false_positive_status
            if add_threat_type_to_case is not None:
                script_params["Add Threat Type To Case"] = add_threat_type_to_case
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
            if only_suspicious_entity_insight is not None:
                script_params["Only Suspicious Entity Insight"] = only_suspicious_entity_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SiemplifyThreatFuse_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Enrich Entities",
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
                print(f"Error executing action SiemplifyThreatFuse_Enrich Entities for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_get_related_hashes(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], confidence_threshold: Annotated[str, Field(..., description="Specify what should be the confidence threshold. Note: Maximum is 100.")], search_threat_bulletins: Annotated[bool, Field(..., description="If enabled, action will search among threat bulletins.")], search_actors: Annotated[bool, Field(..., description="If enabled, action will search among actors.")], search_attack_patterns: Annotated[bool, Field(..., description="If enabled, action will search among attack patterns.")], search_campaigns: Annotated[bool, Field(..., description="If enabled, action will search among campaigns.")], search_courses_of_action: Annotated[bool, Field(..., description="If enabled, action will search among courses of action.")], search_identities: Annotated[bool, Field(..., description="If enabled, action will search among identities.")], search_incidents: Annotated[bool, Field(..., description="If enabled, action will search among incidents.")], search_infrastructures: Annotated[bool, Field(..., description="If enabled, action will search among infrastructures.")], search_intrusion_sets: Annotated[bool, Field(..., description="If enabled, action will search among intrusion sets.")], search_malware: Annotated[bool, Field(..., description="If enabled, action will search among malware.")], search_signatures: Annotated[bool, Field(..., description="If enabled, action will search among signatures.")], search_tools: Annotated[bool, Field(..., description="If enabled, action will search among tools.")], search_tt_ps: Annotated[bool, Field(..., description="If enabled, action will search among TTPs.")], search_vulnerabilities: Annotated[bool, Field(..., description="If enabled, action will search among vulnerabilities.")], max_hashes_to_return: Annotated[str, Field(default=None, description="Specify how many hashes to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related hashes based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Confidence Threshold"] = confidence_threshold
            script_params["Search Threat Bulletins"] = search_threat_bulletins
            script_params["Search Actors"] = search_actors
            script_params["Search Attack Patterns"] = search_attack_patterns
            script_params["Search Campaigns"] = search_campaigns
            script_params["Search Courses Of Action"] = search_courses_of_action
            script_params["Search Identities"] = search_identities
            script_params["Search Incidents"] = search_incidents
            script_params["Search Infrastructures"] = search_infrastructures
            script_params["Search Intrusion Sets"] = search_intrusion_sets
            script_params["Search Malware"] = search_malware
            script_params["Search Signatures"] = search_signatures
            script_params["Search Tools"] = search_tools
            script_params["Search TTPs"] = search_tt_ps
            script_params["Search Vulnerabilities"] = search_vulnerabilities
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
                actionName="SiemplifyThreatFuse_Get Related Hashes",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Get Related Hashes",
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
                print(f"Error executing action SiemplifyThreatFuse_Get Related Hashes for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_get_related_email_addresses(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], confidence_threshold: Annotated[str, Field(..., description="Specify what should be the confidence threshold. Note: Maximum is 100.")], search_observables: Annotated[bool, Field(..., description="If enabled, action will search among observables.")], search_threat_bulletins: Annotated[bool, Field(..., description="If enabled, action will search among threat bulletins.")], search_actors: Annotated[bool, Field(..., description="If enabled, action will search among actors.")], search_attack_patterns: Annotated[bool, Field(..., description="If enabled, action will search among attack patterns.")], search_campaigns: Annotated[bool, Field(..., description="If enabled, action will search among campaigns.")], search_courses_of_action: Annotated[bool, Field(..., description="If enabled, action will search among courses of action.")], search_identities: Annotated[bool, Field(..., description="If enabled, action will search among identities.")], search_incidents: Annotated[bool, Field(..., description="If enabled, action will search among incidents.")], search_infrastructures: Annotated[bool, Field(..., description="If enabled, action will search among infrastructures.")], search_intrusion_sets: Annotated[bool, Field(..., description="If enabled, action will search among intrusion sets.")], search_malware: Annotated[bool, Field(..., description="If enabled, action will search among malware.")], search_signatures: Annotated[bool, Field(..., description="If enabled, action will search among signatures.")], search_tools: Annotated[bool, Field(..., description="If enabled, action will search among tools.")], search_tt_ps: Annotated[bool, Field(..., description="If enabled, action will search among TTPs.")], search_vulnerabilities: Annotated[bool, Field(..., description="If enabled, action will search among vulnerabilities.")], max_email_addresses_to_return: Annotated[str, Field(default=None, description="Specify how many email addresses to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related email addresses based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Confidence Threshold"] = confidence_threshold
            script_params["Search Observables"] = search_observables
            script_params["Search Threat Bulletins"] = search_threat_bulletins
            script_params["Search Actors"] = search_actors
            script_params["Search Attack Patterns"] = search_attack_patterns
            script_params["Search Campaigns"] = search_campaigns
            script_params["Search Courses Of Action"] = search_courses_of_action
            script_params["Search Identities"] = search_identities
            script_params["Search Incidents"] = search_incidents
            script_params["Search Infrastructures"] = search_infrastructures
            script_params["Search Intrusion Sets"] = search_intrusion_sets
            script_params["Search Malware"] = search_malware
            script_params["Search Signatures"] = search_signatures
            script_params["Search Tools"] = search_tools
            script_params["Search TTPs"] = search_tt_ps
            script_params["Search Vulnerabilities"] = search_vulnerabilities
            if max_email_addresses_to_return is not None:
                script_params["Max Email Addresses To Return"] = max_email_addresses_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="SiemplifyThreatFuse_Get Related Email Addresses",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Get Related Email Addresses",
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
                print(f"Error executing action SiemplifyThreatFuse_Get Related Email Addresses for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def siemplify_threat_fuse_get_related_ur_ls(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], confidence_threshold: Annotated[str, Field(..., description="Specify what should be the confidence threshold. Note: Maximum is 100.")], search_threat_bulletins: Annotated[bool, Field(..., description="If enabled, action will search among threat bulletins.")], search_actors: Annotated[bool, Field(..., description="If enabled, action will search among actors.")], search_attack_patterns: Annotated[bool, Field(..., description="If enabled, action will search among attack patterns.")], search_campaigns: Annotated[bool, Field(..., description="If enabled, action will search among campaigns.")], search_courses_of_action: Annotated[bool, Field(..., description="If enabled, action will search among courses of action.")], search_identities: Annotated[bool, Field(..., description="If enabled, action will search among identities.")], search_incidents: Annotated[bool, Field(..., description="If enabled, action will search among incidents.")], search_infrastructures: Annotated[bool, Field(..., description="If enabled, action will search among infrastructures.")], search_intrusion_sets: Annotated[bool, Field(..., description="If enabled, action will search among intrusion sets.")], search_malware: Annotated[bool, Field(..., description="If enabled, action will search among malware.")], search_signatures: Annotated[bool, Field(..., description="If enabled, action will search among signatures.")], search_tools: Annotated[bool, Field(..., description="If enabled, action will search among tools.")], search_tt_ps: Annotated[bool, Field(..., description="If enabled, action will search among TTPs.")], search_vulnerabilities: Annotated[bool, Field(..., description="If enabled, action will search among vulnerabilities.")], max_ur_ls_to_return: Annotated[str, Field(default=None, description="Specify how many hashes to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve entity related urls based on the associations in Siemplify ThreatFuse. Supported entities: Hash, URL, IP Address, Email Address (user entity that matches email regex), Threat Actor, CVE.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SiemplifyThreatFuse")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for SiemplifyThreatFuse: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Confidence Threshold"] = confidence_threshold
            script_params["Search Threat Bulletins"] = search_threat_bulletins
            script_params["Search Actors"] = search_actors
            script_params["Search Attack Patterns"] = search_attack_patterns
            script_params["Search Campaigns"] = search_campaigns
            script_params["Search Courses Of Action"] = search_courses_of_action
            script_params["Search Identities"] = search_identities
            script_params["Search Incidents"] = search_incidents
            script_params["Search Infrastructures"] = search_infrastructures
            script_params["Search Intrusion Sets"] = search_intrusion_sets
            script_params["Search Malware"] = search_malware
            script_params["Search Signatures"] = search_signatures
            script_params["Search Tools"] = search_tools
            script_params["Search TTPs"] = search_tt_ps
            script_params["Search Vulnerabilities"] = search_vulnerabilities
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
                actionName="SiemplifyThreatFuse_Get Related URLs",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SiemplifyThreatFuse_Get Related URLs",
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
                print(f"Error executing action SiemplifyThreatFuse_Get Related URLs for SiemplifyThreatFuse: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SiemplifyThreatFuse")
            return {"Status": "Failed", "Message": "No active instance found."}
