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
    # This function registers all tools (actions) for the GoogleCloudCompute integration.

    @mcp.tool()
    async def google_cloud_compute_remove_ip_from_firewall_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], type: Annotated[List[str], Field(..., description="Type of the IP range that will be removed.")], ip_ranges: Annotated[str, Field(..., description="List of IP ranges that needs to be removed from the Firewall Rule.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the firewall rule. Format: projects/{project_id}/global/firewalls/{firewall}. This parameter has higher priority over the combination of \"Project ID\", and \"Firewall Rule\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your firewall rule. If nothing is provided, the project will be extracted from integration configuration.")], firewall_rule: Annotated[str, Field(default=None, description="Specify firewall rule name to update.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Remove IP from firewall rule in Google Cloud Compute instance. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if firewall_rule is not None:
                script_params["Firewall Rule"] = firewall_rule
            script_params["Type"] = type
            script_params["IP Ranges"] = ip_ranges
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Remove IP From Firewall Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Remove IP From Firewall Rule",
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
                print(f"Error executing action GoogleCloudCompute_Remove IP From Firewall Rule for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_add_labels_to_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_labels: Annotated[str, Field(..., description="Specify instance lables to add to instance. Lables should be provided in the following format - label_key_name:label_value, for example: vm_label_key:label1. Parameter accepts multiple values as a comma separated string.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to add labels to. Instance id can be found with the \"List Instances\" action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add labels to the Google Cloud Compute Instance.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
            script_params["Instance Labels"] = instance_labels
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Add Labels To Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Add Labels To Instance",
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
                print(f"Error executing action GoogleCloudCompute_Add Labels To Instance for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_list_instances(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_name: Annotated[str, Field(default=None, description="Specify instance name to search for. Parameter accepts multiple values as a comma separated string.")], instance_status: Annotated[str, Field(default=None, description="Specify instance status to search for. Parameter accepts multiple values as a comma separated string.")], instance_labels: Annotated[str, Field(default=None, description="Specify instance labels to search for in the format label_key_name:label_value, for example vm_label_key:label1. Parameter accepts multiple values as a comma separated string.")], max_rows_to_return: Annotated[str, Field(default=None, description="Specify how many instances action should return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Google Cloud Compute instances based on the specified search criteria. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_name is not None:
                script_params["Instance Name"] = instance_name
            if instance_status is not None:
                script_params["Instance Status"] = instance_status
            if instance_labels is not None:
                script_params["Instance Labels"] = instance_labels
            if max_rows_to_return is not None:
                script_params["Max Rows to Return"] = max_rows_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_List Instances",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_List Instances",
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
                print(f"Error executing action GoogleCloudCompute_List Instances for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_delete_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to delete. Instance id can be found in \"List Instances\" action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Delete the specified Google Cloud Compute instance.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Delete Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Delete Instance",
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
                print(f"Error executing action GoogleCloudCompute_Delete Instance for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_start_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to start. Instance id can be found in \"List Instances\" action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Start a previously stopped Google Cloud Compute Instance. Note that it can take a few minutes for the instance to enter the running status.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Start Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Start Instance",
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
                print(f"Error executing action GoogleCloudCompute_Start Instance for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_execute_vm_patch_job(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], instance_filter_object: Annotated[str, Field(..., description="A JSON object to set an instance filter.")], name: Annotated[str, Field(..., description="The name for the patching job.")], patch_duration_timeout: Annotated[str, Field(..., description="The timeout value in minutes for a patching job.")], disruption_budget: Annotated[str, Field(..., description="The disruption budget for a patching job. You can use a specific number or a percentage like 10%.")], description: Annotated[str, Field(default=None, description="The description for the patching job.")], patching_config_object: Annotated[str, Field(default=None, description="A JSON object that specifies the steps for the patching job to execute. If you don\u2019t set a value, the action patches Compute Engine instances using the default value. To configure this parameter, use the following format: {\"key\": \"value\"}.")], rollout_strategy: Annotated[List[str], Field(default=None, description="The rollout strategy for a patching job.")], wait_for_completion: Annotated[bool, Field(default=None, description="If selected, the action waits for the patching job to complete.")], fail_if_completed_with_errors: Annotated[bool, Field(default=None, description="If selected and the patching job status is \u201cCompleted with errors\u201d or the action reaches a timeout, the action fails. If you didn\u2019t select the \u201cWait For Completion\u201d parameter, the action ignores this parameter.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Execute a VM patch job on Compute Engine instances. This action is asynchronous. Adjust the script timeout value in the Google SecOps IDE for the action as needed. This action requires you to enable the OS Config API.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            script_params["Instance Filter Object"] = instance_filter_object
            script_params["Name"] = name
            if description is not None:
                script_params["Description"] = description
            if patching_config_object is not None:
                script_params["Patching Config Object"] = patching_config_object
            script_params["Patch Duration Timeout"] = patch_duration_timeout
            if rollout_strategy is not None:
                script_params["Rollout Strategy"] = rollout_strategy
            script_params["Disruption Budget"] = disruption_budget
            if wait_for_completion is not None:
                script_params["Wait For Completion"] = wait_for_completion
            if fail_if_completed_with_errors is not None:
                script_params["Fail If Completed With Errors"] = fail_if_completed_with_errors
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Execute VM Patch Job",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Execute VM Patch Job",
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
                print(f"Error executing action GoogleCloudCompute_Execute VM Patch Job for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_add_network_tags(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], network_tags: Annotated[str, Field(..., description="A comma-separated list of network tags to add to the Compute Engine instance. This parameter only accepts tags that contain lowercase letters, numbers, and hyphens.")], resource_name: Annotated[str, Field(default=None, description="The full resource name for the Compute Engine instance, such as /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has a priority over the \u201cProject ID\u201d, \u201cInstance Zone\u201d, and \u201cInstance ID\u201d parameters.")], project_id: Annotated[str, Field(default=None, description="The project name of the Compute Engine instance. If you don\u2019t set a value,, the action retrieves the project name from the integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="The zone name of the Compute Engine instance. This parameter is required if you configure the Compute Engine instance using the \u201cInstance Zone\u201d and \u201cInstance ID\u201d parameters.")], instance_id: Annotated[str, Field(default=None, description="The Compute Engine instance ID. This parameter is required if you configure the Compute Engine instance using the \u201cInstance Zone\u201d and \u201cInstance ID\u201d parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add network tags to the Compute Engine instance. This action is asynchronous. Adjust the script timeout value in the Google SecOps IDE for the action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
            script_params["Network Tags"] = network_tags
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Add Network Tags",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Add Network Tags",
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
                print(f"Error executing action GoogleCloudCompute_Add Network Tags for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_get_instance_iam_policy(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to get policy for. Intsance id can be found in \"List Instances\" action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Gets the access control policy for the resource. Note that policy may be empty if no policy is assigned to the resource.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Get Instance IAM Policy",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Get Instance IAM Policy",
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
                print(f"Error executing action GoogleCloudCompute_Get Instance IAM Policy for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Google Cloud Compute service with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
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
                actionName="GoogleCloudCompute_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Ping",
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
                print(f"Error executing action GoogleCloudCompute_Ping for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_remove_external_ip_addresses(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: projects/{project_id}/zones/{zone_id}/instances/{instance_id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to modify. Instance id can be found in \"List Instances\" action.")], network_interfaces: Annotated[str, Field(default=None, description="Specify a comma-separated list of network interfaces to modify. If this parameter is left empty or  \u201c*\u201d is provided then all of the network interfaces will be updated.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Remove external IP addresses on a Google Cloud Compute instance. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
            if network_interfaces is not None:
                script_params["Network Interfaces"] = network_interfaces
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Remove External IP Addresses",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Remove External IP Addresses",
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
                print(f"Error executing action GoogleCloudCompute_Remove External IP Addresses for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_remove_network_tags(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], network_tags: Annotated[str, Field(..., description="A comma-separated list of network tags to remove from the Compute Engine instance. This parameter only accepts tags that contain lowercase letters, numbers, and hyphens.")], resource_name: Annotated[str, Field(default=None, description="The full resource name for the Compute Engine instance, such as /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has a priority over the \u201cProject ID\u201d, \u201cInstance Zone\u201d, and \u201cInstance ID\u201d parameters.")], project_id: Annotated[str, Field(default=None, description="The project name of your Compute Engine instance. If you don\u2019t set a value, the action retrieves the project name from the integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="The zone name of the Compute Engine instance. This parameter is required if you configure the Compute Engine instance using the \u201cInstance Zone\u201d and \u201cInstance ID\u201d parameters.")], instance_id: Annotated[str, Field(default=None, description="The Compute Engine instance ID. This parameter is required if you configure the Compute Engine instance using the \u201cInstance Zone\u201d and \u201cInstance ID\u201d parameters.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Remove network tags from the Compute Engine instance. This action is asynchronous. Adjust the sript timeout value in the Google SecOps IDE for the action as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
            script_params["Network Tags"] = network_tags
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Remove Network Tags",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Remove Network Tags",
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
                print(f"Error executing action GoogleCloudCompute_Remove Network Tags for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_set_instance_iam_policy(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], policy: Annotated[str, Field(..., description="Specify JSON policy document to set for instance.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to set policy for. Intsance id can be found in \"List Instances\" action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Sets the access control policy on the specified resource. Note that policy provided in action replaces any existing policy.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
            script_params["Policy"] = policy
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Set Instance IAM Policy",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Set Instance IAM Policy",
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
                print(f"Error executing action GoogleCloudCompute_Set Instance IAM Policy for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich Siemplify IP entities with instance information from Google Cloud Compute.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Enrich Entities",
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
                print(f"Error executing action GoogleCloudCompute_Enrich Entities for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_update_firewall_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the firewall rule. Format: projects/{project_id}/global/firewalls/{firewall}. This parameter has higher priority over the combination of \"Project ID\", and \"Firewall Rule\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your firewall rule. If nothing is provided, the project will be extracted from integration configuration.")], firewall_rule: Annotated[str, Field(default=None, description="Specify firewall rule name to update.")], source_ip_ranges: Annotated[str, Field(default=None, description="Specify a comma-separated list of source IP ranges. Parameter supports 'none' value. If \"none\" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value.")], source_tags: Annotated[str, Field(default=None, description="Specify a comma-separated list of source tags. Parameter supports 'none' value. If \"none\" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value.")], source_service_accounts: Annotated[str, Field(default=None, description="Specify a comma-separated list of source service accounts. Parameter supports 'none' value. If \"none\" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value.")], tcp_ports: Annotated[str, Field(default=None, description="Specify a comma-separated list of TCP ports. If specified, action will use it to update determine allow / deny lists. Parameter supports 'all' and 'none' values.")], udp_ports: Annotated[str, Field(default=None, description="Specify a comma-separated list of UDP ports. If specified, action will use it to update determine allow / deny lists. Parameter supports 'all' and 'none' values.")], other_protocols: Annotated[str, Field(default=None, description="Specify a comma-separated list of other protocols. Parameter supports 'none' value. If 'all' specified, the action will allow all protocols including tcp and udp.")], destination_ip_ranges: Annotated[str, Field(default=None, description="Specify a comma-separated list of destination IP ranges. Parameter supports 'none' value. If \"none\" value is provided, then the action will delete existing values for the firewall rule. If nothing is provided for the parameter, action will not update the existing value.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update a firewall rule with given parameters in Google Cloud Compute. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if firewall_rule is not None:
                script_params["Firewall Rule"] = firewall_rule
            if source_ip_ranges is not None:
                script_params["Source IP ranges"] = source_ip_ranges
            if source_tags is not None:
                script_params["Source Tags"] = source_tags
            if source_service_accounts is not None:
                script_params["Source Service Accounts"] = source_service_accounts
            if tcp_ports is not None:
                script_params["TCP Ports"] = tcp_ports
            if udp_ports is not None:
                script_params["UDP Ports"] = udp_ports
            if other_protocols is not None:
                script_params["Other Protocols"] = other_protocols
            if destination_ip_ranges is not None:
                script_params["Destination IP Ranges"] = destination_ip_ranges
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Update Firewall Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Update Firewall Rule",
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
                print(f"Error executing action GoogleCloudCompute_Update Firewall Rule for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_add_ip_to_firewall_rule(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], type: Annotated[List[str], Field(..., description="Type of the IP range that will be added.")], ip_ranges: Annotated[str, Field(..., description="List of IP ranges that needs to be added to the Firewall Rule.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the firewall rule. Format: projects/{project_id}/global/firewalls/{firewall}. This parameter has higher priority over the combination of \"Project ID\", and \"Firewall Rule\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your firewall rule. If nothing is provided, the project will be extracted from integration configuration.")], firewall_rule: Annotated[str, Field(default=None, description="Specify firewall rule name to update.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add IP range to firewall rule in Google Cloud Compute instance. Note: Action is running as async, please adjust script timeout value in Google SecOps IDE for action, as needed.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if firewall_rule is not None:
                script_params["Firewall Rule"] = firewall_rule
            script_params["Type"] = type
            script_params["IP Ranges"] = ip_ranges
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Add IP To Firewall Rule",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Add IP To Firewall Rule",
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
                print(f"Error executing action GoogleCloudCompute_Add IP To Firewall Rule for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_cloud_compute_stop_instance(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], resource_name: Annotated[str, Field(default=None, description="Specify the full resource name for the compute instance. Format: /projects/{project_id}/zones/{zone id}/instances/{instance id}. This parameter has higher priority over the combination of \"Project ID\", \"Instance Zone\" and \"Instance ID\".")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project of your compute instance. If nothing is provided, the project will be extracted from integration configuration.")], instance_zone: Annotated[str, Field(default=None, description="Specify instance zone name to search for instances in.")], instance_id: Annotated[str, Field(default=None, description="Specify instance id to stop. Instance id can be found in \"List Instances\" action.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Stops a running instance, shutting it down cleanly, and allows you to restart the instance at a later time. Stopped instances do not incur VM usage charges while they are stopped. However, resources that the VM is using, such as persistent disks and static IP addresses, will continue to be charged until they are deleted.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleCloudCompute")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleCloudCompute: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if resource_name is not None:
                script_params["Resource Name"] = resource_name
            if project_id is not None:
                script_params["Project ID"] = project_id
            if instance_zone is not None:
                script_params["Instance Zone"] = instance_zone
            if instance_id is not None:
                script_params["Instance ID"] = instance_id
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleCloudCompute_Stop Instance",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleCloudCompute_Stop Instance",
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
                print(f"Error executing action GoogleCloudCompute_Stop Instance for GoogleCloudCompute: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleCloudCompute")
            return {"Status": "Failed", "Message": "No active instance found."}
