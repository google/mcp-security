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
    # This function registers all tools (actions) for the MISP integration.

    @mcp.tool()
    async def misp_create_network_connection_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add network-connection objects.")], dst_port: Annotated[str, Field(default=None, description="Specify the destination port, which you want to add to the event.")], src_port: Annotated[str, Field(default=None, description="Specify the source port, which you want to add to the event.")], hostname_src: Annotated[str, Field(default=None, description="Specify the source hostname, which you want to add to the event.")], hostname_dst: Annotated[str, Field(default=None, description="Specify the source destination, which you want to add to the event.")], ip_src: Annotated[str, Field(default=None, description="Specify the source IP, which you want to add to the event.")], ip_dst: Annotated[str, Field(default=None, description="Specify the destination IP, which you want to add to the event.")], layer3_protocol: Annotated[str, Field(default=None, description="Specify the related layer 3 protocol, which you want to add to the event.")], layer4_protocol: Annotated[str, Field(default=None, description="Specify the related layer 4 protocol, which you want to add to the event.")], layer7_protocol: Annotated[str, Field(default=None, description="Specify the related layer 7 protocol, which you want to add to the event.")], use_entities: Annotated[bool, Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: IP Address. \u201cUse Entities\u201c has priority over other parameters.")], ip_type: Annotated[List[str], Field(default=None, description="Specify what attribute type should be used with IP entities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a network-connection Object in MISP. Requires one of: Dst-port, Src-port, IP-Src, IP-Dst to be provided or “Use Entities“ parameter set to true.

Action Parameters: Event ID: Specify the ID or UUID of the event to which you want to add network-connection objects., Dst-port: Specify the destination port, which you want to add to the event., Src-port: Specify the source port, which you want to add to the event., Hostname-dst: Specify the source destination, which you want to add to the event., Hostname-src: Specify the source hostname, which you want to add to the event., IP-Src: Specify the source IP, which you want to add to the event., IP-Dst: Specify the destination IP, which you want to add to the event., Layer3-protocol: Specify the related layer 3 protocol, which you want to add to the event., Layer4-protocol: Specify the related layer 4 protocol, which you want to add to the event., Layer7-protocol: Specify the related layer 7 protocol, which you want to add to the event., Use Entities: If enabled, action will use entities in order to create objects. Supported entities: IP Address. "Use Entities" has priority over other parameters., IP Type: Specify what attribute type should be used with IP entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Create network-connection Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create network-connection Misp Object",
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
                print(f"Error executing action MISP_Create network-connection Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_list_event_objects(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify a comma-separated list of IDs and UUIDs of the events, for which you want to retrieve details.")], max_objects_to_return: Annotated[str, Field(default=None, description="Specify how many objects to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve information about available objects in MISP event.

Action Parameters: Event ID: Specify a comma-separated list of IDs and UUIDs of the events, for which you want to retrieve details., Max Objects to Return: Specify how many objects to return.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_List Event Objects",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_List Event Objects",
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
                print(f"Error executing action MISP_List Event Objects for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_unpublish_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event that you want to unpublish.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
The action allows the user to unpublish an event. Unpublishing an event prevents it from being visible to the shared groups.

Action Parameters: Event ID: Specify the ID or UUID of the event that you want to unpublish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Event ID"] = event_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Unpublish Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Unpublish Event",
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
                print(f"Error executing action MISP_Unpublish Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_name: Annotated[str, Field(..., description="Specify the name for the new event.")], distribution: Annotated[str, Field(default=None, description="Specify the distribution of the event. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All. You can either provide a number or a string.")], threat_level: Annotated[str, Field(default=None, description="Specify the threat level of the event. Possible values: 1 - High, 2 - Medium, 3 - Low, 4 - Undefined. You can either provide a number or a string.")], analysis: Annotated[str, Field(default=None, description="Specify the analysis of the event. Possible values: 0 - Initial, 1 - Ongoing, 2 - Completed. You can either provide a number or a string.")], publish: Annotated[bool, Field(default=None, description="If enabled, action will publish the event to the community.")], comment: Annotated[str, Field(default=None, description="Specify additional comments related to the event.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a new event in MISP.

Action Parameters: Event Name: The name of the event., Threat Level: The threat level of the event. Default: 0., Distribution: The distribution of the attribute. Default: 1., Analysis: The analysis level of the event [0-2]: Default: 0., Publish: Whether to publish the event or not., Comment: The comment of the event.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Create Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create Event",
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
                print(f"Error executing action MISP_Create Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_remove_tag_from_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to remove from attributes.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers from which you want to remove tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c or Object UUID is provided.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only remove tags from attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only remove tags from attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], object_uuid: Annotated[str, Field(default=None, description="Specify the UUID of the object that contains the desired attribute.")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs from which you want to remove new tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and remove tags from all attributes that match our criteria.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Remove tags from attributes in MISP.

Action Parameters: Event ID: Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if "Attribute Search" is set to "Provided Event"., Tag Name: Specify a comma-separated list of tags that you want to remove from attributes., Attribute Name: Specify a comma-separated list of attribute identifiers from which you want to remove tags. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values., Category: Specify a comma-separated list of categories. If specified, action will only remove tags from attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation., Type: Specify a comma-separated list of attribute types. If specified, action will only remove tags from attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst, Object UUID: Specify the UUID of the object that contains the desired attribute., Attribute Search: Specify, where action should search for attributes. If "Provided Event" is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in "Event ID" parameter. If "All Events", action will search for attributes among all events and remove tags from all attributes that match our criteria., Attribute UUID: Specify a comma-separated list of attribute UUIDs from which you want to remove new tags. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Remove Tag from an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Remove Tag from an Attribute",
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
                print(f"Error executing action MISP_Remove Tag from an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test Connectivity

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
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
                actionName="MISP_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Ping",
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
                print(f"Error executing action MISP_Ping for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_set_ids_flag_for_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers for which you want to set an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to seach for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only set IDS flag for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only set IDS flag for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and set IDS flag for all attributes that match our criteria.")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs for which you want to set an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Set IDS flag for attributes in MISP

Action Parameters: Attribute Name: Specify a comma-separated list of attribute identifiers for which you want to set an IDS flag. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values., Event ID: Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if "Attribute Search" is set to "Provided Event"., Category: Specify a comma-separated list of categories. If specified, action will only set IDS flag for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation., Type: Specify a comma-separated list of attribute types. If specified, action will only set IDS flag for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst, Attribute Search: Specify, where action should search for attributes. If "Provided Event" is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in "Event ID" parameter. If "All Events", action will search for attributes among all events and set IDS flag for all attributes that match our criteria., Attribute UUID: Specify a comma-separated list of attribute UUIDs for which you want to set an IDS flag. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Set IDS Flag for an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Set IDS Flag for an Attribute",
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
                print(f"Error executing action MISP_Set IDS Flag for an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_get_event_details(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify a comma-separated list of IDs or UUIDs of the events for which you want retrieve details.")], return_attributes_info: Annotated[bool, Field(default=None, description="If enabled, action will create a case wall table for all of the attributes that are a part of the event.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve details about events in MISP.

Action Parameters: Event ID: Specify a comma-separated list of IDs or UUIDs of the events for which you want retrieve details., Return Attributes Info: If enabled, action will create a case wall table for all of the attributes that are a part of the event.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Get Event Details",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Get Event Details",
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
                print(f"Error executing action MISP_Get Event Details for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_tag_to_an_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event, for which you want to add tags.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to add to events.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add tags to event in MISP.

Action Parameters: Event ID: The unique identifier specifying the event to add tag to., Tag Name: The name of the tag to add to an event.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Event ID"] = event_id
            script_params["Tag Name"] = tag_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Add Tag to an Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Tag to an Event",
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
                print(f"Error executing action MISP_Add Tag to an Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_remove_tag_from_an_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event, from which you want to remove tags.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to remove from events.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Remove tags from event in MISP.

Action Parameters: Event ID: Specify the ID or UUID of the event, from which you want to remove tags., Tag Name: Specify a comma-separated list of tags that you want to remove from events.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Event ID"] = event_id
            script_params["Tag Name"] = tag_name
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Remove Tag from an Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Remove Tag from an Event",
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
                print(f"Error executing action MISP_Remove Tag from an Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_delete_an_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event that you want to delete.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Delete event in MISP

Action Parameters: Event ID: Specify the ID or UUID of the event that you want to delete.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Event ID"] = event_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Delete an Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Delete an Event",
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
                print(f"Error executing action MISP_Delete an Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_ip_port_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add IP-Port objects.")], dst_port: Annotated[str, Field(default=None, description="Specify the destination port, which you want to add to the event.")], src_port: Annotated[str, Field(default=None, description="Specify the source port, which you want to add to the event.")], domain: Annotated[str, Field(default=None, description="Specify the domain, which you want to add to the event.")], hostname: Annotated[str, Field(default=None, description="Specify the hostname, which you want to add to the event.")], ip_src: Annotated[str, Field(default=None, description="Specify the source IP, which you want to add to the event.")], ip_dst: Annotated[str, Field(default=None, description="Specify the destination IP, which you want to add to the event.")], use_entities: Annotated[bool, Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: IP Address. \u201cUse Entities\u201c has priority over other parameters.")], ip_type: Annotated[List[str], Field(default=None, description="Specify what attribute type should be used with IP entities.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a IP-Port Object in MISP. Requires one of: Dst-port, Src-port, Domain, HOSTNAME, IP-Src, IP-Dst to be provided or “Use Entities“ parameter set to true.

Action Parameters: Event ID: The unique identifier of the event to add the object. Example: 1, Dst-port: Destination port., Src-port: Source port., Domain: Domain., Hostname: Hostname., IP-Src: Source IP Address., IP-Dst: Destination IP Address.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Create IP-Port Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create IP-Port Misp Object",
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
                print(f"Error executing action MISP_Create IP-Port Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_virustotal_report_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add URL objects.")], permalink: Annotated[str, Field(..., description="Specify the link to the VirusTotal report, which you want to add to the event.")], comment: Annotated[str, Field(default=None, description="Specify the comment, which you want to add to the event.")], detection_ratio: Annotated[str, Field(default=None, description="Specify the detection ration, which you want to add to the event.")], community_score: Annotated[str, Field(default=None, description="Specify the community score, which you want to add to the event.")], first_submission: Annotated[str, Field(default=None, description="Specify first submission of the event. Format: 2020-12-22T13:07:32Z")], last_submission: Annotated[str, Field(default=None, description="Specify last submission of the event. Format: 2020-12-22T13:07:32Z")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a Virustotal-Report Object in MISP.

Action Parameters: Event ID: Specify the ID or UUID of the event to which you want to add URL objects., Permalink: Specify the link to the VirusTotal report, which you want to add to the event., Comment: Specify the comment, which you want to add to the event., Detection Ratio: Specify the detection ration, which you want to add to the event., Community Score: Specify the community score, which you want to add to the event., First Submission: Specify first submission of the event. Format: 2020-12-22T13:07:32Z, Last Submission: Specify last submission of the event. Format: 2020-12-22T13:07:32Z

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Create Virustotal-Report Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create Virustotal-Report Object",
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
                print(f"Error executing action MISP_Create Virustotal-Report Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_sighting_to_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], sightings_type: Annotated[List[str], Field(..., description="Specify the type of the Sighting.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers to which you want to add a new sighting. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only add sightings to attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only add sightings to attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], source: Annotated[str, Field(default=None, description="Specify the source for the sighting. Example: SIEM, SOAR, Siemplify.")], date_time: Annotated[str, Field(default=None, description="Specify the date time for the sighting. Format: 2020-02-10 11:00:00.")], object_uuid: Annotated[str, Field(default=None, description="Specify the uuid of the object that contains the desired attribute")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and add sighting for all attributes that match our criteria.")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs to which you want to add a new sighting. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a sighting to attributes in MISP

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Add Sighting to an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Sighting to an Attribute",
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
                print(f"Error executing action MISP_Add Sighting to an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], number_of_attributes_to_return: Annotated[str, Field(..., description="Specify how many attributes to return for entities.")], filtering_condition: Annotated[List[str], Field(..., description="Specify the filtering condition for the action. If \u201cLast\u201c is selected, action will use the oldest attribute for enrichment, if \u201cFirst\u201c is selected, action will use the newest attribute for enrichment.")], create_insights: Annotated[bool, Field(default=None, description="If enabled, action will generate an insight for every entity that was fully processed.")], threat_level_threshold: Annotated[List[str], Field(default=None, description="Specify what should be the threshold for the threat level of the event, where the entity was found. If related event exceeds or matches threshold, entity will be marked as suspicious.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Enrich entities based on the attributes in MISP.

Action Parameters: Number of attributes to return: Specify how many attributes to return for entities., Filtering condition: Specify the filtering condition for the action. If "Last" is selected, action will use the oldest attribute for enrichment, if "First" is selected, action will use the newest attribute for enrichment., Threat Level Threshold: Specify what should be the threshold for the threat level of the event, where the entity was found. If related event exceeds or matches threshold, entity will be marked as suspicious., Attribute Search Limit: Specify how many attributes to search for per entity. This parameter has an impact on which attribute will be selected for enrichment. Default: 50.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Enrich Entities",
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
                print(f"Error executing action MISP_Enrich Entities for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_url_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to add URL objects.")], url: Annotated[str, Field(default=None, description="Specify the URL, which you want to add to the event.")], port: Annotated[str, Field(default=None, description="Specify the port, which you want to add to the event.")], first_seen: Annotated[str, Field(default=None, description="Specify, when the URL was first seen. Format: 2020-12-22T13:07:32Z")], last_seen: Annotated[str, Field(default=None, description="Specify, when the URL was last seen. Format: 2020-12-22T13:07:32Z")], domain: Annotated[str, Field(default=None, description="Specify the domain, which you want to add to the event.")], text: Annotated[str, Field(default=None, description="Specify the additional text, which you want to add to the event.")], ip: Annotated[str, Field(default=None, description="Specify the IP, which you want to add to the event.")], host: Annotated[str, Field(default=None, description="Specify the Host, which you want to add to the event.")], use_entities: Annotated[bool, Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: URL. \u201cUse Entities\u201c has priority over other parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a URL Object in MISP. Requires “URL” to be provided or “Use Entities“ parameter set to true.

Action Parameters: Event ID: Specify the ID or UUID of the event to which you want to add URL objects., URL: Specify the URL, which you want to add to the event., Port: Specify the port, which you want to add to the event., First seen: Specify, when the URL was first seen. Format: 2020-12-22T13:07:32Z, Last seen: Specify, when the URL was last seen. Format: 2020-12-22T13:07:32Z, Domain: Specify the domain, which you want to add to the event., Text: Specify the additional text, which you want to add to the event., IP: Specify the IP, which you want to add to the event., Host: Specify the Host, which you want to add to the event., Use Entities: If enabled, action will use entities in order to create objects. Supported entities: URL. "Use Entities" has priority over other parameters.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Create Url Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create Url Misp Object",
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
                print(f"Error executing action MISP_Create Url Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_download_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event from which you want to download files")], download_folder_path: Annotated[str, Field(default=None, description="Specify the absolute path to the folder, which should store files. If nothing is specified, action will create an attachment instead. Note: JSON result is only available, when you provide proper value for this parameter.")], overwrite: Annotated[bool, Field(default=None, description="If enabled, action will overwrite existing files.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Download files related to event in MISP.

Action Parameters: Event ID: Specify the ID or UUID of the event from which you want to download files, Download Folder Path: Specify the absolute path to the folder, which should store files. If nothing is specified, action will create an attachment instead. Note: JSON result is only available, when you provide proper value for this parameter., Overwrite: If enabled, action will overwrite existing files.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Download File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Download File",
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
                print(f"Error executing action MISP_Download File for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_unset_ids_flag_for_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers for which you want to unset an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to seach for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only unset IDS flag for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only unset IDS flag for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and unset IDS flag for all attributes that match our criteria.")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs for which you want to unset an IDS flag. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Unset IDS flag for attributes in MISP

Action Parameters: Attribute Name: Specify a comma-separated list of attribute identifiers for which you want to unset an IDS flag. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values., Event ID: Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if "Attribute Search" is set to "Provided Event"., Category: Specify a comma-separated list of categories. If specified, action will only unset IDS flag for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation., Type: Specify a comma-separated list of attribute types. If specified, action will only unset IDS flag for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst, Attribute Search: Specify, where action should search for attributes. If "Provided Event" is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in "Event ID" parameter. If "All Events", action will search for attributes among all events and unset IDS flag for all attributes that match our criteria., Attribute UUID: Specify a comma-separated list of attribute UUIDs for which you want to unset an IDS flag. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Unset IDS Flag for an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Unset IDS Flag for an Attribute",
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
                print(f"Error executing action MISP_Unset IDS Flag for an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_upload_file(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event to which you want to upload this file.")], file_path: Annotated[str, Field(..., description="Specify a comma-separated list of absolute filepaths of the files that you want to upload to MISP.")], for_intrusion_detection_system: Annotated[bool, Field(..., description="If enabled, uploaded file will be used for intrusion detection systems.")], category: Annotated[str, Field(default=None, description="Specify the category for the uploaded file. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], distribution: Annotated[str, Field(default=None, description="Specify the distribution for the uploaded file. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All. You can either provide a number or a string.")], comment: Annotated[str, Field(default=None, description="Specify additional comments related to the uploaded file.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Upload a file to a MISP event.

Action Parameters: Event ID: Specify the ID or UUID of the event to which you want to upload this file., File Path: Specify a comma-separated list of absolute filepaths of the files that you want to upload to MISP., Category: Specify the category for the uploaded file. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation., Distribution: Specify the distribution for the uploaded file. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All. You can either provide a number or a string., Threat Level: Specify the threat level for the uploaded file. Possible values: 1 - High, 2 - Medium, 3 - Low, 4 - Undefined. You can either provide a number or a string., Analysis: Specify the analysis of the event.Possible values: 0 - Initial, 1 - Ongoing, 2 - Completed. You can either provide a number or a string., Info: Specify additional info for the uploaded file., For Intrusion Detection System: If enabled, uploaded file will be used for intrusion detection systems., Comment: Specify additional comments related to the uploaded file.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Upload File",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Upload File",
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
                print(f"Error executing action MISP_Upload File for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="TheSpecify the ID or UUID of the event, for which you want to add attributes.")], for_intrusion_detection_system: Annotated[bool, Field(..., description="If enabled, attribute will be labeled as eligible to create an IDS signature out of it.")], category: Annotated[str, Field(default=None, description="Specify the category for attributes. Possible values: Targeting data, Payload delivery, Artifacts dropped, Payload installation, Persistence mechanism, Network activity, Attribution, External analysis, Social network.")], distribution: Annotated[str, Field(default=None, description="Specify the distribution of the attribute. Possible values: 0 - Organisation, 1 - Community, 2 - Connected, 3 - All, 5 - Inherit. You can either provide a number or a string.")], comment: Annotated[str, Field(default=None, description="Specify comment related to attribute.")], fallback_ip_type: Annotated[List[str], Field(default=None, description="Specify what should be the fallback attribute type for the IP address entity.")], fallback_email_type: Annotated[List[str], Field(default=None, description="Specify what should be the fallback attribute type for the email address entity.")], extract_domain: Annotated[bool, Field(default=None, description="If enabled, action will extract domain out of URL entity.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add attributes based on entities to the event in MISP. Supported hashes: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.

Action Parameters: Event ID: The ID of the event., Category: The category of the attribute. Default: External analysis., Distribution: The distribution of the attribute. Default: 1., For Intrusion Detection System: Whether the attribute is used for Intrusion Detection System. Default: false., Comment: The comment to add to the attribute.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Add Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Attribute",
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
                print(f"Error executing action MISP_Add Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_add_tag_to_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], tag_name: Annotated[str, Field(..., description="Specify a comma-separated list of tags that you want to add to attributes.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers to which you want to add tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c or Object UUID is provided.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only add tags to attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only add tags to attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], object_uuid: Annotated[str, Field(default=None, description="Specify the uuid of the object that contains the desired attribute.")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs to which you want to add new tags. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and add sighting for all attributes that match our criteria.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Add tags to attributes in MISP.

Action Parameters: Event ID: The identifier of the event that the attribute is associated with. Example: 1., Tag Name: The name of the tag to add to an attribute., Attribute Name: The name identifier of the attribute to tag., Category: The category which the attribute belongs to. e.g. Payload Delivery., Type: The type of the attribute. e.g. filename., Object UUID: The unique identifier for an object in the event.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Add Tag to an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Add Tag to an Attribute",
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
                print(f"Error executing action MISP_Add Tag to an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_create_file_misp_object(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event for which you want to add file objects.")], filename: Annotated[str, Field(default=None, description="Specify the name of the file, which you want to add to the event.")], md5: Annotated[str, Field(default=None, description="Specify the md5 of the file, which you want to add to the event.")], sha1: Annotated[str, Field(default=None, description="Specify the sha1 of the file, which you want to add to the event.")], sha256: Annotated[str, Field(default=None, description="Specify the sha256 of the file, which you want to add to the event.")], ssdeep: Annotated[str, Field(default=None, description="Specify the ssdeep of the file, which you want to add to the event. Format: size:hash:hash")], use_entities: Annotated[bool, Field(default=None, description="If enabled, action will use entities in order to create objects. Supported entities: File name and hash. \u201cUse Entities\u201c has priority over other parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Create a File Object in MISP. Requires one of: FILENAME, MD5, SHA1, SHA256, SSDEEP to be provided or “Use Entities“ parameter set to true.

Action Parameters: Event ID: The unique identifier of the event to add the object. Example: 1, Filename: The filename of the file., MD5: The md5 hash value of the file., SHA1: The sha1 hash value of the file., SHA256: The sha256 hash value of the file., SSDEEP: The ssdeep value of the file Example: 96:p5aAS1tN0M3t9AnTNuG6TNOt5PR1TNZdkljOXTNSnKTF3X7KsTFW+kLtW6K8i7bI:p5mb4rgQhRp7GljCbF3LKqFjkwxtU, Imphash: The MD5 hash value calculated from the imported table.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Create File Misp Object",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Create File Misp Object",
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
                print(f"Error executing action MISP_Create File Misp Object for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_get_related_events(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], events_limit: Annotated[str, Field(default=None, description="Specify max amount of events to fetch. If not specified, all events will be fetched.")], mark_as_suspicious: Annotated[bool, Field(default=None, description="If enabled, action will mark entity as suspicious, if there is at least one related event to it.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Retrieve information about events that are related to entities in MISP.

Action Parameters: Mark As Suspicious: If enabled, action will mark entity as suspicious, if there is at least one related event to it.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Get Related Events",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Get Related Events",
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
                print(f"Error executing action MISP_Get Related Events for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_publish_event(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], event_id: Annotated[str, Field(..., description="Specify the ID or UUID of the event that you want to publish.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
The action allows the user to publish an event. Publishing an event shares it to the sharing group selected, making it visible to all members.

Action Parameters: Event ID: Specify the ID or UUID of the event that you want to publish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Event ID"] = event_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Publish Event",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Publish Event",
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
                print(f"Error executing action MISP_Publish Event for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_list_sightings_of_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers for which you want to list sightings. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to seach for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only list sightings for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only list sightings for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and list sightings for all attributes that match our criteria.")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs for which you want to list sightings. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
List available sightings for attributes in MISP

Action Parameters: Attribute Name: Specify a comma-separated list of attribute identifiers for which you want to list sightings. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values., Event ID: Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if "Attribute Search" is set to "Provided Event"., Category: Specify a comma-separated list of categories. If specified, action will only list sightings for attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation., Type: Specify a comma-separated list of attribute types. If specified, action will only list sightings for attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst, Attribute Search: Specify, where action should search for attributes. If "Provided Event" is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in "Event ID" parameter. If "All Events", action will search for attributes among all events and list sightings for all attributes that match our criteria., Attribute UUID: Specify a comma-separated list of attribute UUIDs for which you want to list sightings. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_List Sightings of an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_List Sightings of an Attribute",
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
                print(f"Error executing action MISP_List Sightings of an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def misp_delete_an_attribute(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], attribute_name: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute identifiers that you want to delete. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], event_id: Annotated[str, Field(default=None, description="Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if \u201cAttribute Search\u201c is set to \u201cProvided Event\u201c or Object UUID is provided.")], category: Annotated[str, Field(default=None, description="Specify a comma-separated list of categories. If specified, action will only delete attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation.")], type: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute types. If specified, action will only delete attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst")], object_uuid: Annotated[str, Field(default=None, description="Specify the uuid of the object that contains the desired attribute")], attribute_uuid: Annotated[str, Field(default=None, description="Specify a comma-separated list of attribute UUIDs that you want to delete. Note: If both \u201cAttribute Name\u201c and \u201cAttribute UUID\u201c are specified, action will work with \u201cAttribute UUID\u201c values.")], attribute_search: Annotated[List[str], Field(default=None, description="Specify, where action should search for attributes. If \u201cProvided Event\u201c is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in \u201cEvent ID\u201c parameter. If \u201cAll Events\u201c, action will search for attributes among all events and delete all attributes that match our criteria.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """
Delete attributes in MISP. Supported hashes: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, SSDeep.

Action Parameters: Event ID: Specify the ID or UUID of the event, where to search for attributes. This parameter is required, if "Attribute Search" is set to "Provided Event"., Attribute Name: Specify a comma-separated list of attribute identifiers that you want to delete. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values., Category: Specify a comma-separated list of categories. If specified, action will only delete attributes that have matching category. If nothing is specified, action will ignore categories in attributes. Possible values: External Analysis, Payload Delivery, Artifacts Dropped, Payload Installation., Type: Specify a comma-separated list of attribute types. If specified, action will only delete attributes that have matching attribute type. If nothing is specified, action will ignore types in attributes. Example values: md5, sha1, ip-src, ip-dst, Object UUID: The unique identifier for an object in the event., Attribute Search: Specify, where action should search for attributes. If "Provided Event" is selected, action will only search for attributes or attribute UUIDs in event with ID/UUID provided in "Event ID" parameter. If "All Events", action will search for attributes among all events and delete all attributes that match our criteria., Attribute UUID: Specify a comma-separated list of attribute UUIDs that you want to delete. Note: If both "Attribute Name" and "Attribute UUID" are specified, action will work with "Attribute UUID" values.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="MISP")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MISP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
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
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MISP_Delete an Attribute",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MISP_Delete an Attribute",
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
                print(f"Error executing action MISP_Delete an Attribute for MISP: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for MISP")
            return {"Status": "Failed", "Message": "No active instance found."}
