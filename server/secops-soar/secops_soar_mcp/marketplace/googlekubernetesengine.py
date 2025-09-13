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
    # This function registers all tools (actions) for the GoogleGKE integration.

    @mcp.tool()
    async def google_gke_list_node_pools(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], cluster_name: Annotated[str, Field(..., description="Specify Google Kubernetes Engine cluster name.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied. Filtering logic is working based on the node pool name field.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter. If \"Equal\" is selected, action should will try to find the exact match among results and if \"Contains\" is selected, action will try to find results that contain the substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the node pool name field.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List node pools for the Google Kubernetes Engine cluster based on the specified search criteria. Note that action is not working on Siemplify entities. Additionally, filtering logic is working based on the node pool name field.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
            script_params["Cluster Name"] = cluster_name
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
                actionName="GoogleGKE_List Node Pools",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_List Node Pools",
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
                print(f"Error executing action GoogleGKE_List Node Pools for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_set_cluster_addons(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], cluster_name: Annotated[str, Field(..., description="Specify Google Kubernetes Engine cluster name.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], http_load_balancing: Annotated[List[str], Field(default=None, description="Specify the value for the HTTP Load Balancing addon configuration.")], horizontal_pod_autoscaling: Annotated[List[str], Field(default=None, description="Specify the value for the Horizontal Pod Autoscaling addon configuration.")], network_policy_config: Annotated[List[str], Field(default=None, description="Specify the value for the Network Policy Config addon configuration.")], cloud_run_config: Annotated[List[str], Field(default=None, description="Specify the value for the Cloud Run Config addon configuration.")], dns_cache_config: Annotated[List[str], Field(default=None, description="Specify the value for the DNS Cache Config addon configuration.")], config_connector_config: Annotated[List[str], Field(default=None, description="Specify the value for the Config Connector Config addon.")], gce_persistent_disk_csi_driver_config: Annotated[List[str], Field(default=None, description="Specify the value for the GCE Persistent Disk Csi Driver Config addon.")], wait_for_cluster_configuration_change_operation_to_finish: Annotated[bool, Field(default=None, description="If enabled, action will wait for the results of the cluster configuration change operation.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an operation to set addons for the Google Kubernetes Engine cluster. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
            script_params["Cluster Name"] = cluster_name
            if http_load_balancing is not None:
                script_params["HTTP Load Balancing"] = http_load_balancing
            if horizontal_pod_autoscaling is not None:
                script_params["Horizontal Pod Autoscaling"] = horizontal_pod_autoscaling
            if network_policy_config is not None:
                script_params["Network Policy Config"] = network_policy_config
            if cloud_run_config is not None:
                script_params["Cloud Run Config"] = cloud_run_config
            if dns_cache_config is not None:
                script_params["DNS Cache Config"] = dns_cache_config
            if config_connector_config is not None:
                script_params["Config Connector Config"] = config_connector_config
            if gce_persistent_disk_csi_driver_config is not None:
                script_params["GCE Persistent Disk Csi Driver Config"] = gce_persistent_disk_csi_driver_config
            if wait_for_cluster_configuration_change_operation_to_finish is not None:
                script_params["Wait for cluster configuration change operation to finish"] = wait_for_cluster_configuration_change_operation_to_finish
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleGKE_Set Cluster Addons",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Set Cluster Addons",
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
                print(f"Error executing action GoogleGKE_Set Cluster Addons for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_list_operations(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], location: Annotated[str, Field(..., description="Specify Google Compute Engine location for which to fetch the operations for. Example: europe-central2-a")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project for which to fetch the operations for. If nothing is provided, the project will be extracted from integration configuration.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter. If \"Equal\" is selected, action should will try to find the exact match among results and if \"Contains\" is selected, action will try to find results that contain the substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the operation name field.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return. Default: 50.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Google Kubernetes Engine operations for a location based on the specified search criteria. Note that action is not working on Siemplify entities. Additionally, filtering logic is working based on the operation name field.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Location"] = location
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
                actionName="GoogleGKE_List Operations",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_List Operations",
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
                print(f"Error executing action GoogleGKE_List Operations for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_set_node_pool_management(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], cluster_name: Annotated[str, Field(..., description="Specify Google Kubernetes Engine cluster name.")], node_pool_name: Annotated[str, Field(..., description="Specify node pool name for the Google Kubernetes Engine cluster.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], auto_upgrade: Annotated[List[str], Field(default=None, description="Specify the status of auto upgrade management feature.")], auto_repair: Annotated[List[str], Field(default=None, description="Specify the status of auto repair management feature.")], wait_for_cluster_configuration_change_operation_to_finish: Annotated[bool, Field(default=None, description="If enabled, action will wait for the results of the cluster configuration change operation.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an operation to set node pool management configuration for the Google Kubernetes Engine cluster. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
            script_params["Cluster Name"] = cluster_name
            script_params["Node Pool Name"] = node_pool_name
            if auto_upgrade is not None:
                script_params["Auto Upgrade"] = auto_upgrade
            if auto_repair is not None:
                script_params["Auto Repair"] = auto_repair
            if wait_for_cluster_configuration_change_operation_to_finish is not None:
                script_params["Wait for cluster configuration change operation to finish"] = wait_for_cluster_configuration_change_operation_to_finish
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleGKE_Set Node Pool Management",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Set Node Pool Management",
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
                print(f"Error executing action GoogleGKE_Set Node Pool Management for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Google Kubernetes Engine service with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
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
                actionName="GoogleGKE_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Ping",
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
                print(f"Error executing action GoogleGKE_Ping for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_set_cluster_labels(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], cluster_name: Annotated[str, Field(..., description="Specify Google Kubernetes Engine cluster name.")], cluster_labels: Annotated[str, Field(..., description="Specify a JSON object that contains labels to add to the cluster. Please consider default value for the format reference. Action appends new labels to any existing cluster labels.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], wait_for_cluster_configuration_change_operation_to_finish: Annotated[bool, Field(default=None, description="If enabled, action will wait for the results of the cluster configuration change operation.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an operation to set labels for the Google Kubernetes Engine cluster. Action is async. Action appends new labels to any existing cluster labels. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
            script_params["Cluster Name"] = cluster_name
            script_params["Cluster Labels"] = cluster_labels
            if wait_for_cluster_configuration_change_operation_to_finish is not None:
                script_params["Wait for cluster configuration change operation to finish"] = wait_for_cluster_configuration_change_operation_to_finish
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleGKE_Set Cluster Labels",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Set Cluster Labels",
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
                print(f"Error executing action GoogleGKE_Set Cluster Labels for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_get_operation_status(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], location: Annotated[str, Field(..., description="Specify Google Compute Engine location for which to fetch operation status for. Example: europe-central2-a")], operation_name: Annotated[str, Field(..., description="Specify Google Compute Engine operation to fetch.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project for which to fetch operation status for. If nothing is provided, the project will be extracted from integration configuration.")], wait_for_cluster_configuration_change_operation_to_finish: Annotated[bool, Field(default=None, description="If enabled, action will wait for the results of the cluster configuration change operation.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Get the Google Kubernetes Engine operation status. Action is async. Note that action is not working on Siemplify entities.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Location"] = location
            script_params["Operation Name"] = operation_name
            if wait_for_cluster_configuration_change_operation_to_finish is not None:
                script_params["Wait for cluster configuration change operation to finish"] = wait_for_cluster_configuration_change_operation_to_finish
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleGKE_Get Operation Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Get Operation Status",
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
                print(f"Error executing action GoogleGKE_Get Operation Status for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_list_clusters(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], filter_logic: Annotated[List[str], Field(default=None, description="Specify what filter logic should be applied. Filtering logic is working based on the cluster name field.")], filter_value: Annotated[str, Field(default=None, description="Specify what value should be used in the filter. If \"Equal\" is selected, action should will try to find the exact match among results and if \"Contains\" is selected, action will try to find results that contain the substring. If nothing is provided in this parameter, the filter will not be applied. Filtering logic is working based on the cluster name field.")], max_records_to_return: Annotated[str, Field(default=None, description="Specify how many records to return.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """List Google Kubernetes Engine clusters based on the specified search criteria. Note that action is not working on Siemplify entities. Additionally, filtering logic is working based on the cluster name field.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
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
                actionName="GoogleGKE_List Clusters",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_List Clusters",
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
                print(f"Error executing action GoogleGKE_List Clusters for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_set_node_autoscaling(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], cluster_name: Annotated[str, Field(..., description="Specify Google Kubernetes Engine cluster name.")], node_pool_name: Annotated[str, Field(..., description="Specify node pool name for the Google Kubernetes Engine cluster.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], autoscaling_mode: Annotated[List[str], Field(default=None, description="Specify autoscaling mode status for the node pool.")], minimum_node_count: Annotated[str, Field(default=None, description="Specify minimum node count for the node pool configuration.")], maximum_node_count: Annotated[str, Field(default=None, description="Specify maximum node count for the node pool configuration.")], wait_for_cluster_configuration_change_operation_to_finish: Annotated[bool, Field(default=None, description="If enabled, action will wait for the results of the cluster configuration change operation.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an operation to set node pool autoscaling configuration for the Google Kubernetes Engine cluster. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
            script_params["Cluster Name"] = cluster_name
            script_params["Node Pool Name"] = node_pool_name
            if autoscaling_mode is not None:
                script_params["Autoscaling Mode"] = autoscaling_mode
            if minimum_node_count is not None:
                script_params["Minimum Node Count"] = minimum_node_count
            if maximum_node_count is not None:
                script_params["Maximum Node Count"] = maximum_node_count
            if wait_for_cluster_configuration_change_operation_to_finish is not None:
                script_params["Wait for cluster configuration change operation to finish"] = wait_for_cluster_configuration_change_operation_to_finish
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleGKE_Set Node Autoscaling",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Set Node Autoscaling",
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
                print(f"Error executing action GoogleGKE_Set Node Autoscaling for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def google_gke_set_node_count(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], cluster_location: Annotated[str, Field(..., description="Specify Google Compute Engine location in which to search for clusters in. Example: europe-central2-a")], cluster_name: Annotated[str, Field(..., description="Specify Google Kubernetes Engine cluster name.")], node_pool_name: Annotated[str, Field(..., description="Specify node pool name for the Google Kubernetes Engine cluster.")], node_count: Annotated[str, Field(..., description="Specify node count for the Google Kubernetes Engine cluster node pool.")], project_id: Annotated[str, Field(default=None, description="Specify the name of the project in which to search for clusters in. If nothing is provided, the project will be extracted from integration configuration.")], wait_for_cluster_configuration_change_operation_to_finish: Annotated[bool, Field(default=None, description="If enabled, action will wait for the results of the cluster configuration change operation.")], target_entities: Annotated[List[TargetEntity], PydanticListField(TargetEntity, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Create an operation to set node count for the Google Kubernetes Engine cluster node pool. Action is async. Note that action is not working on Siemplify entities. Additionally, if the target cluster is already going under configuration change, new configuration changes will not be accepted until current configuration changes finish.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="GoogleGKE")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for GoogleGKE: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            script_params = {}
            if project_id is not None:
                script_params["Project ID"] = project_id
            script_params["Cluster Location"] = cluster_location
            script_params["Cluster Name"] = cluster_name
            script_params["Node Pool Name"] = node_pool_name
            script_params["Node Count"] = node_count
            if wait_for_cluster_configuration_change_operation_to_finish is not None:
                script_params["Wait for cluster configuration change operation to finish"] = wait_for_cluster_configuration_change_operation_to_finish
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="GoogleGKE_Set Node Count",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "GoogleGKE_Set Node Count",
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
                print(f"Error executing action GoogleGKE_Set Node Count for GoogleGKE: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for GoogleGKE")
            return {"Status": "Failed", "Message": "No active instance found."}
