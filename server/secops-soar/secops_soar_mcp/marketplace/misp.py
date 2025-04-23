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
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the MISP integration.

    @mcp.tool()
    async def misp_create_network_connection_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add network-connection objects.")], dst_port: Annotated[Optional[str], Field(default=None, description="Specify the destination port, which you want to add to the event.")], src_port: Annotated[Optional[str], Field(default=None, description="Specify the source port, which you want to add to the event.")], hostname_src: Annotated[Optional[str], Field(default=None, description="Specify the source hostname, which you want to add to the event.")], hostname_dst: Annotated[Optional[str], Field(default=None, description="Specify the source destination, which you want to add to the event.")], ip_src: Annotated[Optional[str], Field(default=None, description="Specify the source IP, which you want to add to the event.")], ip_dst: Annotated[Optional[str], Field(default=None, description="Specify the destination IP, which you want to add to the event.")], layer3_protocol: Annotated[Optional[str], Field(default=None, description="Specify the related layer 3 protocol, which you want to add to the event.")], layer4_protocol: Annotated[Optional[str], Field(default=None, description="Specify the related layer 4 protocol, which you want to add to the event.")], layer7_protocol: Annotated[Optional[str], Field(default=None, description="Specify the related layer 7 protocol, which you want to add to the event.")], use_entities: Annotated[Optional[bool], Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: IP Address. \u201cUse Entities\u201c has priority over other parameters.")], ip_type: Annotated[Optional[List[Any]], Field(default=None, description="Specify what attribute type should be used with IP entities.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a network-connection Object in MISP. Requires one of: Dst-port, Src-port, IP-Src, IP-Dst to be provided or “Use Entities“ parameter set to true.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if dst_port is not None:
                script_params["Dst-port"] = dst_port
            if src_port is not None:
                script_params["Src-port"] = src_port
            if hostname_src is not None:
                script_params["Hostname-src"] = hostname_src
            if hostname_dst is not None:
                script_params["Hostname-dst"] = hostname_dst
            if ip_src is not None:
                script_params["IP-Src"] = ip_src
            if ip_dst is not None:
                script_params["IP-Dst"] = ip_dst
            if layer3_protocol is not None:
                script_params["Layer3-protocol"] = layer3_protocol
            if layer4_protocol is not None:
                script_params["Layer4-protocol"] = layer4_protocol
            if layer7_protocol is not None:
                script_params["Layer7-protocol"] = layer7_protocol
            if use_entities is not None:
                script_params["Use Entities"] = use_entities
            if ip_type is not None:
                script_params["IP Type"] = ip_type
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Create network-connection Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create network-connection Misp Object", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Create network-connection Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_list_event_objects(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify a comma-separated list of IDs and UUIDs of the events, for which you want to retrieve details.")], max_objects_to_return: Annotated[Optional[str], Field(default=None, description="Specify how many objects to return.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about available objects in MISP event.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if max_objects_to_return is not None:
                script_params["Max Objects to Return"] = max_objects_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_List Event Objects",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_List Event Objects", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_List Event Objects for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_unpublish_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event that you want to unpublish.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """The action allows the user to unpublish an event. Unpublishing an event prevents it from being visible to the shared groups.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Unpublish Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Unpublish Event", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Unpublish Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_name: Annotated[str, Field(..., description="Specify the name for the new event.")], distribution: Annotated[Optional[str], Field(default=None, description="Specify the distribution of the event. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All. You can either provide a number or a string.")], threat_level: Annotated[Optional[str], Field(default=None, description="Specify the threat level of the event. Possible values: 1 - High, 2 - Medium, 3 - Low, 4 - Undefined. You can either provide a number or a string.")], analysis: Annotated[Optional[str], Field(default=None, description="Specify the analysis of the event. Possible values: 0 - Initial, 1 - Ongoing, 2 - Completed. You can either provide a number or a string.")], publish: Annotated[Optional[bool], Field(default=None, description="If enabled, action will publish the event to the community.")], comment: Annotated[Optional[str], Field(default=None, description="Specify additional comments related to the event.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a new event in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event Name"] = event_name
            if distribution is not None:
                script_params["Distribution"] = distribution
            if threat_level is not None:
                script_params["Threat Level"] = threat_level
            if analysis is not None:
                script_params["Analysis"] = analysis
            if publish is not None:
                script_params["Publish"] = publish
            if comment is not None:
                script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Create Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create Event", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Create Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_remove_tag_from_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to remove from attributes.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers from which you want to remove tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c or Object UUID is provided.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only remove tags from attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only remove tags from attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], object_uuid: Annotated[Optional[str], Field(default=None, description="Specify the UUID of the object that contains the desired attribute.")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs from which you want to remove new tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and remove tags from all attributes that match our criteria.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Remove tags from attributes in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            script_params["Tag Name"] = tag_name
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            if object_uuid is not None:
                script_params["Object UUID"] = object_uuid
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Remove Tag from an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Remove Tag from an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Remove Tag from an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Ping", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Ping for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_set_ids_flag_for_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers for which you want to set an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to seach for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only set IDS flag for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only set IDS flag for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and set IDS flag for all attributes that match our criteria.")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs for which you want to set an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Set IDS flag for attributes in MISP

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Set IDS Flag for an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Set IDS Flag for an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Set IDS Flag for an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_get_event_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify a comma-separated list of IDs or UUIDs of the events for which you want retrieve details.")], return_attributes_info: Annotated[Optional[bool], Field(default=None, description="If enabled, action will create a case wall table for all of the attributes that are a part of the event.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve details about events in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if return_attributes_info is not None:
                script_params["Return Attributes Info"] = return_attributes_info
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Get Event Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Get Event Details", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Get Event Details for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_tag_to_an_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event, for which you want to add tags.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to add to events.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add tags to event in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            script_params["Tag Name"] = tag_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Add Tag to an Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Tag to an Event", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Add Tag to an Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_remove_tag_from_an_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event, from which you want to remove tags.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to remove from events.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Remove tags from event in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            script_params["Tag Name"] = tag_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Remove Tag from an Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Remove Tag from an Event", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Remove Tag from an Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_delete_an_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event that you want to delete.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete event in MISP

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Delete an Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Delete an Event", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Delete an Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_ip_port_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add IP-Port objects.")], dst_port: Annotated[Optional[str], Field(default=None, description="Specify the destination port, which you want to add to the event.")], src_port: Annotated[Optional[str], Field(default=None, description="Specify the source port, which you want to add to the event.")], domain: Annotated[Optional[str], Field(default=None, description="Specify the domain, which you want to add to the event.")], hostname: Annotated[Optional[str], Field(default=None, description="Specify the hostname, which you want to add to the event.")], ip_src: Annotated[Optional[str], Field(default=None, description="Specify the source IP, which you want to add to the event.")], ip_dst: Annotated[Optional[str], Field(default=None, description="Specify the destination IP, which you want to add to the event.")], use_entities: Annotated[Optional[bool], Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: IP Address. \u201cUse Entities\u201c has priority over other parameters.")], ip_type: Annotated[Optional[List[Any]], Field(default=None, description="Specify what attribute type should be used with IP entities.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a IP-Port Object in MISP. Requires one of: Dst-port, Src-port, Domain, HOSTNAME, IP-Src, IP-Dst to be provided or “Use Entities“ parameter set to true.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if dst_port is not None:
                script_params["Dst-port"] = dst_port
            if src_port is not None:
                script_params["Src-port"] = src_port
            if domain is not None:
                script_params["Domain"] = domain
            if hostname is not None:
                script_params["HOSTNAME"] = hostname
            if ip_src is not None:
                script_params["IP-Src"] = ip_src
            if ip_dst is not None:
                script_params["IP-Dst"] = ip_dst
            if use_entities is not None:
                script_params["Use Entities"] = use_entities
            if ip_type is not None:
                script_params["IP Type"] = ip_type
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Create IP-Port Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create IP-Port Misp Object", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Create IP-Port Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_virustotal_report_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add URL objects.")], permalink: Annotated[str, Field(..., description="Specify the link to the VirusTotal report, which you want to add to the event.")], comment: Annotated[Optional[str], Field(default=None, description="Specify the comment, which you want to add to the event.")], detection_ratio: Annotated[Optional[str], Field(default=None, description="Specify the detection ration, which you want to add to the event.")], community_score: Annotated[Optional[str], Field(default=None, description="Specify the community score, which you want to add to the event.")], first_submission: Annotated[Optional[str], Field(default=None, description="Specify first submission of the event. Format: 2020-12-22T13:07:32Z")], last_submission: Annotated[Optional[str], Field(default=None, description="Specify last submission of the event. Format: 2020-12-22T13:07:32Z")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a Virustotal-Report Object in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            script_params["Permalink"] = permalink
            if comment is not None:
                script_params["Comment"] = comment
            if detection_ratio is not None:
                script_params["Detection Ratio"] = detection_ratio
            if community_score is not None:
                script_params["Community Score"] = community_score
            if first_submission is not None:
                script_params["First Submission"] = first_submission
            if last_submission is not None:
                script_params["Last Submission"] = last_submission
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Create Virustotal-Report Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create Virustotal-Report Object", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Create Virustotal-Report Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_sighting_to_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], sightings_type: Annotated[List[Any], Field(..., description="Specify the type of the Sighting.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers to which you want to add a new sighting. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only add sightings to attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only add sightings to attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], source: Annotated[Optional[str], Field(default=None, description="Specify the source for the sighting. Example: SIEM, SOAR, Siemplify.")], date_time: Annotated[Optional[str], Field(default=None, description="Specify the date time for the sighting. Format: 2020-02-10 11:00:00.")], object_uuid: Annotated[Optional[str], Field(default=None, description="Specify the uuid of the object that contains the desired attribute")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and add sighting for all attributes that match our criteria.")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs to which you want to add a new sighting. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a sighting to attributes in MISP

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            script_params["Sightings Type"] = sightings_type
            if source is not None:
                script_params["Source"] = source
            if date_time is not None:
                script_params["Date Time"] = date_time
            if object_uuid is not None:
                script_params["Object UUID"] = object_uuid
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Add Sighting to an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Sighting to an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Add Sighting to an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], number_of_attributes_to_return: Annotated[str, Field(..., description="Specify how many attributes to return for entities.")], filtering_condition: Annotated[List[Any], Field(..., description="Specify the filtering condition for the action. If \u201cLast\u201c is selected, action will use the oldest attribute for enrichment, if \u201cFirst\u201c is selected, action will use the newest attribute for enrichment.")], create_insights: Annotated[Optional[bool], Field(default=None, description="If enabled, action will generate an insight for every entity that was fully processed.")], threat_level_threshold: Annotated[Optional[List[Any]], Field(default=None, description="Specify what should be the threshold for the threat level of the event, where the entity was found. If related event exceeds or matches threshold, entity will be marked as suspicious.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich entities based on the attributes in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Number of attributes to return"] = number_of_attributes_to_return
            script_params["Filtering condition"] = filtering_condition
            if create_insights is not None:
                script_params["Create Insights"] = create_insights
            if threat_level_threshold is not None:
                script_params["Threat Level Threshold"] = threat_level_threshold
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Enrich Entities", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Enrich Entities for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_url_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add URL objects.")], url: Annotated[Optional[str], Field(default=None, description="Specify the URL, which you want to add to the event.")], port: Annotated[Optional[str], Field(default=None, description="Specify the port, which you want to add to the event.")], first_seen: Annotated[Optional[str], Field(default=None, description="Specify, when the URL was first seen. Format: 2020-12-22T13:07:32Z")], last_seen: Annotated[Optional[str], Field(default=None, description="Specify, when the URL was last seen. Format: 2020-12-22T13:07:32Z")], domain: Annotated[Optional[str], Field(default=None, description="Specify the domain, which you want to add to the event.")], text: Annotated[Optional[str], Field(default=None, description="Specify the additional text, which you want to add to the event.")], ip: Annotated[Optional[str], Field(default=None, description="Specify the IP, which you want to add to the event.")], host: Annotated[Optional[str], Field(default=None, description="Specify the Host, which you want to add to the event.")], use_entities: Annotated[Optional[bool], Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: URL. \u201cUse Entities\u201c has priority over other parameters.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a URL Object in MISP. Requires “URL” to be provided or “Use Entities“ parameter set to true.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if url is not None:
                script_params["URL"] = url
            if port is not None:
                script_params["Port"] = port
            if first_seen is not None:
                script_params["First seen"] = first_seen
            if last_seen is not None:
                script_params["Last seen"] = last_seen
            if domain is not None:
                script_params["Domain"] = domain
            if text is not None:
                script_params["Text"] = text
            if ip is not None:
                script_params["IP"] = ip
            if host is not None:
                script_params["Host"] = host
            if use_entities is not None:
                script_params["Use Entities"] = use_entities
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Create Url Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create Url Misp Object", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Create Url Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_download_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event from which you want to download files")], download_folder_path: Annotated[Optional[str], Field(default=None, description="Specify the absolute path to the folder, which should store files. If nothing is specified, action will create an attachment instead. Note: JSON result is only available, when you provide proper value for this parameter.")], overwrite: Annotated[Optional[bool], Field(default=None, description="If enabled, action will overwrite existing files.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Download files related to event in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if event_id is not None:
                script_params["Event ID"] = event_id
            if download_folder_path is not None:
                script_params["Download Folder Path"] = download_folder_path
            if overwrite is not None:
                script_params["Overwrite"] = overwrite
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Download File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Download File", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Download File for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_unset_ids_flag_for_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers for which you want to unset an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to seach for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only unset IDS flag for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only unset IDS flag for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and unset IDS flag for all attributes that match our criteria.")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs for which you want to unset an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Unset IDS flag for attributes in MISP

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Unset IDS Flag for an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Unset IDS Flag for an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Unset IDS Flag for an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_upload_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to upload this file.")], file_path: Annotated[str, Field(..., description="Specify a comma-separated list of absolute filepaths of the files that you want to upload to MISP.")], for_intrusion_detection_system: Annotated[bool, Field(..., description="If enabled, uploaded file will be used for intrusion detection systems.")], category: Annotated[Optional[str], Field(default=None, description="Specify the category for the uploaded file. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], distribution: Annotated[Optional[str], Field(default=None, description="Specify the distribution for the uploaded file. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All. You can either provide a number or a string.")], comment: Annotated[Optional[str], Field(default=None, description="Specify additional comments related to the uploaded file.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Upload a file to a MISP event.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            script_params["File Path"] = file_path
            if category is not None:
                script_params["Category"] = category
            if distribution is not None:
                script_params["Distribution"] = distribution
            script_params["For Intrusion Detection System"] = for_intrusion_detection_system
            if comment is not None:
                script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Upload File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Upload File", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Upload File for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="TheSpecify the ID or UUID of the event, for which you want to add attributes.")], for_intrusion_detection_system: Annotated[bool, Field(..., description="If enabled, attribute will be labeled as eligible to create an IDS signature out of it.")], category: Annotated[Optional[str], Field(default=None, description="Specify the category for attributes. Possible values: Targeting data, Payload delivery, Artifacts dropped, Payload installation, Persistence mechanism, Network activity, Attribution, External analysis, Social network.")], distribution: Annotated[Optional[str], Field(default=None, description="Specify the distribution of the attribute. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All, 5 - Inherit. You can either provide a number or a string.")], comment: Annotated[Optional[str], Field(default=None, description="Specify comment related to attribute.")], fallback_ip_type: Annotated[Optional[List[Any]], Field(default=None, description="Specify what should be the fallback attribute type for the IP address entity.")], fallback_email_type: Annotated[Optional[List[Any]], Field(default=None, description="Specify what should be the fallback attribute type for the email address entity.")], extract_domain: Annotated[Optional[bool], Field(default=None, description="If enabled, action will extract domain out of URL entity.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add attributes based on entities to the event in MISP. Supported hashes: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if category is not None:
                script_params["Category"] = category
            if distribution is not None:
                script_params["Distribution"] = distribution
            script_params["For Intrusion Detection System"] = for_intrusion_detection_system
            if comment is not None:
                script_params["Comment"] = comment
            if fallback_ip_type is not None:
                script_params["Fallback IP Type"] = fallback_ip_type
            if fallback_email_type is not None:
                script_params["Fallback Email Type"] = fallback_email_type
            if extract_domain is not None:
                script_params["Extract Domain"] = extract_domain
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Add Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Add Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_tag_to_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to add to attributes.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers to which you want to add tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c or Object UUID is provided.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only add tags to attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only add tags to attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], object_uuid: Annotated[Optional[str], Field(default=None, description="Specify the uuid of the object that contains the desired attribute.")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs to which you want to add new tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and add sighting for all attributes that match our criteria.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add tags to attributes in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            script_params["Tag Name"] = tag_name
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            if object_uuid is not None:
                script_params["Object UUID"] = object_uuid
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Add Tag to an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Tag to an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Add Tag to an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_file_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event for which you want to add file objects.")], filename: Annotated[Optional[str], Field(default=None, description="Specify the name of the file, which you want to add to the event.")], md5: Annotated[Optional[str], Field(default=None, description="Specify the md5 of the file, which you want to add to the event.")], sha1: Annotated[Optional[str], Field(default=None, description="Specify the sha1 of the file, which you want to add to the event.")], sha256: Annotated[Optional[str], Field(default=None, description="Specify the sha256 of the file, which you want to add to the event.")], ssdeep: Annotated[Optional[str], Field(default=None, description="Specify the ssdeep of the file, which you want to add to the event. Format: size:hash:hash")], use_entities: Annotated[Optional[bool], Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: File name and hash. \u201cUse Entities\u201c has priority over other parameters.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create a File Object in MISP. Requires one of: FILENAME, MD5, SHA1, SHA256, SSDEEP to be provided or “Use Entities“ parameter set to true.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
            if filename is not None:
                script_params["FILENAME"] = filename
            if md5 is not None:
                script_params["MD5"] = md5
            if sha1 is not None:
                script_params["SHA1"] = sha1
            if sha256 is not None:
                script_params["SHA256"] = sha256
            if ssdeep is not None:
                script_params["SSDEEP"] = ssdeep
            if use_entities is not None:
                script_params["Use Entities"] = use_entities
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Create File Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create File Misp Object", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Create File Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_get_related_events(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], events_limit: Annotated[Optional[str], Field(default=None, description="Specify max amount of events to fetch. If not specified, all events will be fetched.")], mark_as_suspicious: Annotated[Optional[bool], Field(default=None, description="If enabled, action will mark entity as suspicious, if there is at least one related event to it.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Retrieve information about events that are related to entities in MISP.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if events_limit is not None:
                script_params["Events Limit"] = events_limit
            if mark_as_suspicious is not None:
                script_params["Mark As Suspicious"] = mark_as_suspicious
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Get Related Events",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Get Related Events", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Get Related Events for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_publish_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event that you want to publish.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """The action allows the user to publish an event. Publishing an event shares it to the sharing group selected, making it visible to all members.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["Event ID"] = event_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Publish Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Publish Event", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Publish Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_list_sightings_of_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers for which you want to list sightings. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to seach for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only list sightings for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only list sightings for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and list sightings for all attributes that match our criteria.")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs for which you want to list sightings. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List available sightings for attributes in MISP

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_List Sightings of an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_List Sightings of an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_List Sightings of an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_delete_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute identifiers that you want to delete. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[Optional[str], Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c or Object UUID is provided.")], category: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only delete attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only delete attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], object_uuid: Annotated[Optional[str], Field(default=None, description="Specify the uuid of the object that contains the desired attribute")], attribute_uuid: Annotated[Optional[str], Field(default=None, description="Specify a comma-separated list of attribute UUIDs that you want to delete. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], attribute_search: Annotated[Optional[List[Any]], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and delete all attributes that match our criteria.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete attributes in MISP. Supported hashes: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.

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
            final_scope = None # Scope is ignored when specific entities are given
            is_predefined_scope = False
        else:
            # No specific target entities, use scope parameter
            # Check if the provided scope is valid
            if scope not in bindings.valid_scopes:
                allowed_values_str = ", ".join(sorted(list(bindings.valid_scopes)))
                return {
                    "Status": "Failed",
                    "Message": f"Invalid scope '{scope}'. Allowed values are: {allowed_values_str}",
                }
            # Scope is valid or validation is not configured
            final_target_entities = [] # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True
        # --- End scope/entity logic ---
    
        # Fetch integration instance identifier (assuming this pattern)
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            if attribute_name is not None:
                script_params["Attribute Name"] = attribute_name
            if event_id is not None:
                script_params["Event ID"] = event_id
            if category is not None:
                script_params["Category"] = category
            if type is not None:
                script_params["Type"] = type
            if object_uuid is not None:
                script_params["Object UUID"] = object_uuid
            if attribute_uuid is not None:
                script_params["Attribute UUID"] = attribute_uuid
            if attribute_search is not None:
                script_params["Attribute Search"] = attribute_search
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="MISP_Delete an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Delete an Attribute", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action MISP_Delete an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}
