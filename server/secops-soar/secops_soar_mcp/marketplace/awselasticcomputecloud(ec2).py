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
    # This function registers all tools (actions) for the AWSEC2 integration.

    @mcp.tool()
    async def awsec2_terminate_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_i_ds: Annotated[str, Field(..., description="One or more instance IDs. Separated by comma.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """When you've decided that you no longer need an instance, you can terminate it. Terminated instances cannot be started. Notice that you can only terminate instance store-backed instances.  For more information about instance store-backed instances, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Instance IDs"] = instance_i_ds
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Terminate Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Terminate Instance",
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
                print(f"Error executing action AWSEC2_Terminate Instance for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_list_instances(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_i_ds: Annotated[str, Field(default=None, description="One or more instance IDs. specify instance IDs, the output includes information for only the specified instances. Please note that the parameter \u2018Instance IDs\u2019 cannot be used with the parameter \u2018Max Results\u2019. \u2018Instance IDs\u2019 has priority over the \u2018Max Result\u2019 parameter.")], tag_filters: Annotated[str, Field(default=None, description="The key/value combination of a tag assigned to the resource. For example, to find all resources that have a tag with the key Owner and the value TeamA , specify Owner:TeamA. Comma separated tag filters. E.g. Name:Name1,Owner:TeamA. Returned instances will be fit to all filters.")], max_results: Annotated[str, Field(default=None, description="Specify how many instances to return. Default is 50. Maximum is 1000. Please note that the parameter \u2018Instance IDs\u2019 cannot be used with the parameter \u2018Max Results\u2019. \u2018Instance IDs\u2019 has priority over the \u2018Max Result\u2019 parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Describes the specified instances or all instances.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if instance_i_ds is not None:
                script_params["Instance IDs"] = instance_i_ds
            if tag_filters is not None:
                script_params["Tag Filters"] = tag_filters
            if max_results is not None:
                script_params["Max Results"] = max_results
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_List Instances",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_List Instances",
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
                print(f"Error executing action AWSEC2_List Instances for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_take_snapshot(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_id: Annotated[str, Field(..., description="Instance ID. Specify the instance ID")], description: Annotated[str, Field(default=None, description="Specify the description of the snapshot")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Take snapshot of the instance

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Instance ID"] = instance_id
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
                actionName="AWSEC2_Take Snapshot",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Take Snapshot",
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
                print(f"Error executing action AWSEC2_Take Snapshot for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_revoke_security_group_egress(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], security_group_i_ds: Annotated[str, Field(..., description="One or more security group IDs. Separated by comma.")], ip_protocol: Annotated[List[str], Field(default=None, description="The IP protocol name. Use \"all\" to specify all protocols. Specifying \"all\" allows traffic on all ports, regardless of any port range you specify.")], from_port: Annotated[str, Field(default=None, description="The start of port range for the TCP and UDP protocols, or an ICMP type number.")], to_port: Annotated[str, Field(default=None, description="The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.")], ip_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv4 address in  CIDR format. To specify a single IPv4 address, use the /32 prefix length.")], i_pv6_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv6 CIDR range.  To specify a single IPv6 address, use the /128 prefix length.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Removes the specified egress rules (outbound rules) from a security group for EC2-VPC. This action does not apply to security groups for use in EC2-Classic. To remove a rule, the values that you specify (for example, ports) must match the existing rule's values exactly. Rule changes are propagated to instances within the security group as quickly as possible. However, a small delay might occur.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Security Group IDs"] = security_group_i_ds
            if ip_protocol is not None:
                script_params["IP Protocol"] = ip_protocol
            if from_port is not None:
                script_params["From Port"] = from_port
            if to_port is not None:
                script_params["To Port"] = to_port
            if ip_ranges_cidr_ip is not None:
                script_params["IP Ranges - CidrIP"] = ip_ranges_cidr_ip
            if i_pv6_ranges_cidr_ip is not None:
                script_params["IPv6 Ranges - CidrIP"] = i_pv6_ranges_cidr_ip
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Revoke Security Group Egress",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Revoke Security Group Egress",
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
                print(f"Error executing action AWSEC2_Revoke Security Group Egress for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_start_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_i_ds: Annotated[str, Field(..., description="One or more instance IDs. Separated by comma.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Starts an Amazon EBS-backed instance that you have previously stopped. It can take a few minutes for the instance to enter the running state. Notice that you can't start an instance store-backed instance.  For more information about instance store-backed instances, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Instance IDs"] = instance_i_ds
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Start Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Start Instance",
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
                print(f"Error executing action AWSEC2_Start Instance for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_create_tags(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_i_ds: Annotated[str, Field(..., description="One or more resource IDs. Separated by comma.")], tags: Annotated[str, Field(..., description="The key/value combination of a tag to be assigned to the resource. For example, to add to all specified resources a tag with the key Owner and the value TeamA , specify Owner:TeamA. You can specify multiple key/value combinations by comma separation. You can add or overwrite the specified tags. Please note: tag keys must be unique per resource.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """A tag is a label that you assign to an AWS resource. Each tag consists of a key and an optional value. You can use tags to search and filter your resources or track your AWS costs. Adds or overwrites only the specified tags for the specified Amazon EC2 resource or resources. When you specify an existing tag key, the value is overwritten with the new value. Each resource can have a maximum of 50 tags. Tag keys must be unique per resource. For more information about tags, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html in the Amazon Elastic Compute Cloud User Guide .

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Resource IDs"] = resource_i_ds
            script_params["Tags"] = tags
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Create Tags",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Create Tags",
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
                print(f"Error executing action AWSEC2_Create Tags for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to AWS EC2 with parameters provided at the integration configuration page on Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
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
                actionName="AWSEC2_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Ping",
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
                print(f"Error executing action AWSEC2_Ping for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_list_security_groups(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], security_group_names: Annotated[str, Field(default=None, description="One or more security group Names [EC2-Classic and default VPC only]. Separated by comma. If you specify security group Names, the output includes information for only the specified names.")], security_group_i_ds: Annotated[str, Field(default=None, description="One or more security group IDs. Separated by comma. If you specify security group IDs, the output includes information for only the specified ids. Required for security groups in a non-default VPC.")], tag_filters: Annotated[str, Field(default=None, description="The key/value combination of a tag assigned to the security group. For example, to find all groups that have a tag with the key Owner and the value TeamA , specify Owner:TeamA. Comma separated tag filters. E.g. Name:Name1,Owner:TeamA. Returned groups will be fit to all filters.")], max_results: Annotated[str, Field(default=None, description="Specify how many security groups to return. Default is 50. Maximum is 1000. Please note that the parameters \u2018Security Group IDs\u2019 and \u2018Security Group Names\u2019 cannot be used with the parameter \u2018Max Results\u2019")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Describes the specified security groups or all of your security groups. A security group is for use with instances either in the EC2-Classic platform or in a specific VPC. For more information, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if security_group_names is not None:
                script_params["Security Group Names"] = security_group_names
            if security_group_i_ds is not None:
                script_params["Security Group IDs"] = security_group_i_ds
            if tag_filters is not None:
                script_params["Tag Filters"] = tag_filters
            if max_results is not None:
                script_params["Max Results"] = max_results
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_List Security Groups",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_List Security Groups",
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
                print(f"Error executing action AWSEC2_List Security Groups for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_authorize_security_group_egress(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], security_group_i_ds: Annotated[str, Field(..., description="One or more security group IDs. Separated by comma.")], ip_protocol: Annotated[List[str], Field(default=None, description="The IP protocol name. Use \u2019all\u2019 to specify all protocols. Specifying \u2018all\u2019 allows traffic on all ports, regardless of any port range you specify.")], from_port: Annotated[str, Field(default=None, description="The start of port range for the TCP and UDP protocols, or an ICMP type number.")], to_port: Annotated[str, Field(default=None, description="The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.")], ip_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv4 CIDR range. To specify a single IPv4 address, use the /32 prefix length.")], i_pv6_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv6 CIDR range. To specify a single IPv6 address, use the /128 prefix length.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Adds the specified egress rule to a security group for use with a VPC. An outbound rule permits instances to send traffic to the specified IPv4 or IPv6 CIDR address ranges. Rule changes are propagated to affected instances as quickly as possible. However, a small delay might occur. For more information about VPC security group limits, see https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Security Group IDs"] = security_group_i_ds
            if ip_protocol is not None:
                script_params["IP Protocol"] = ip_protocol
            if from_port is not None:
                script_params["From Port"] = from_port
            if to_port is not None:
                script_params["To Port"] = to_port
            if ip_ranges_cidr_ip is not None:
                script_params["IP Ranges - CidrIP"] = ip_ranges_cidr_ip
            if i_pv6_ranges_cidr_ip is not None:
                script_params["IPv6 Ranges - CidrIP"] = i_pv6_ranges_cidr_ip
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Authorize Security Group Egress",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Authorize Security Group Egress",
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
                print(f"Error executing action AWSEC2_Authorize Security Group Egress for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_authorize_security_group_ingress(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], security_group_i_ds: Annotated[str, Field(..., description="One or more security group IDs. Separated by comma.")], ip_protocol: Annotated[List[str], Field(default=None, description="The IP protocol name. Use \"all\" to specify all protocols. Specifying \"all\" allows traffic on all ports, regardless of any port range you specify.")], from_port: Annotated[str, Field(default=None, description="The start of port range for the TCP and UDP protocols, or an ICMP type number.")], to_port: Annotated[str, Field(default=None, description="The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.")], ip_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv4 CIDR range. To specify a single IPv4 address, use the /32 prefix length.")], i_pv6_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv6 CIDR range. To specify a single IPv6 address, use the /128 prefix length.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Adds the specified ingress rule to a security group. An inbound rule permits instances to receive traffic from the specified IPv4 or IPv6 CIDR address ranges. Rule changes are propagated to affected instances as quickly as possible. However, a small delay might occur. For more information about VPC security group limits, see https://docs.aws.amazon.com/vpc/latest/userguide/amazon-vpc-limits.html

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Security Group IDs"] = security_group_i_ds
            if ip_protocol is not None:
                script_params["IP Protocol"] = ip_protocol
            if from_port is not None:
                script_params["From Port"] = from_port
            if to_port is not None:
                script_params["To Port"] = to_port
            if ip_ranges_cidr_ip is not None:
                script_params["IP Ranges - CidrIP"] = ip_ranges_cidr_ip
            if i_pv6_ranges_cidr_ip is not None:
                script_params["IPv6 Ranges - CidrIP"] = i_pv6_ranges_cidr_ip
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Authorize Security Group Ingress",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Authorize Security Group Ingress",
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
                print(f"Error executing action AWSEC2_Authorize Security Group Ingress for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_revoke_security_group_ingress(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], security_group_i_ds: Annotated[str, Field(..., description="One or more security group IDs. Separated by comma.")], ip_protocol: Annotated[List[str], Field(default=None, description="The IP protocol name. Use \"all\" to specify all protocols. Specifying \"all\" allowes traffic on all ports, regardless of any port range you specify.")], from_port: Annotated[str, Field(default=None, description="The start of port range for the TCP and UDP protocols, or an ICMP type number.")], to_port: Annotated[str, Field(default=None, description="The end of port range for the TCP and UDP protocols allows traffic on all ports, regardless of any port range you specify.")], ip_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv4 address in  CIDR format. To specify a single IPv4 address, use the /32 prefix length.")], i_pv6_ranges_cidr_ip: Annotated[str, Field(default=None, description="The IPv6 CIDR range.  To specify a single IPv6 address, use the /128 prefix length.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Removes the specified ingress rules (inbound rules) from a security group. To remove a rule, the values that you specify (for example, ports) must match the existing rule's values exactly. Rule changes are propagated to instances within the security group as quickly as possible. However, a small delay might occur.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Security Group IDs"] = security_group_i_ds
            if ip_protocol is not None:
                script_params["IP Protocol"] = ip_protocol
            if from_port is not None:
                script_params["From Port"] = from_port
            if to_port is not None:
                script_params["To Port"] = to_port
            if ip_ranges_cidr_ip is not None:
                script_params["IP Ranges - CidrIP"] = ip_ranges_cidr_ip
            if i_pv6_ranges_cidr_ip is not None:
                script_params["IPv6 Ranges - CidrIP"] = i_pv6_ranges_cidr_ip
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Revoke Security Group Ingress",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Revoke Security Group Ingress",
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
                print(f"Error executing action AWSEC2_Revoke Security Group Ingress for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def awsec2_stop_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_i_ds: Annotated[str, Field(..., description="One or more instance IDs. Separated by comma.")], force: Annotated[bool, Field(default=None, description="Forces the instances to stop. The instances do not have an opportunity to flush file system caches or file system metadata. If you use this option, you must perform file system check and repair procedures. This option is not recommended for Windows instances.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Stop an Amazon EBS-backed instance. When you stop an instance, we attempt to shut it down forcibly after a short while. It can take a few minutes for the instance to stop. The instance can be started at any time. Notice that you can't stop an instance store-backed instance.  For more information about instance store-backed instances, see https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="AWSEC2")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for AWSEC2: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Instance IDs"] = instance_i_ds
            if force is not None:
                script_params["Force"] = force
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="AWSEC2_Stop Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "AWSEC2_Stop Instance",
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
                print(f"Error executing action AWSEC2_Stop Instance for AWSEC2: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for AWSEC2")
            return {"Status": "Failed", "Message": "No active instance found."}
