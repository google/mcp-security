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
from secops_soar_mcp.utils.models import (
    ApiManualActionDataModel,
    EmailContent,
    TargetEntity,
)
import json
from typing import Optional, List, Dict, Union, Annotated
from pydantic import Field
from secops_soar_mcp.utils.pydantic_list_field import PydanticListField


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the MicrosoftDefenderATP integration.

    @mcp.tool()
    async def microsoft_defender_atp_run_advanced_hunting_query(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        query: Annotated[
            str, Field(..., description="Advanced hunting query to execute")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Run Advanced Hunting Query

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Query"] = query

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Run Advanced Hunting Query",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Run Advanced Hunting Query",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Run Advanced Hunting Query for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_get_machine_related_alerts(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        status: Annotated[
            str,
            Field(
                default=None,
                description="Statuses of the alert to look for. Comma-separated string",
            ),
        ],
        severity: Annotated[
            str,
            Field(
                default=None,
                description="Severities of the alert to look for. Comma-separated string.",
            ),
        ],
        category: Annotated[
            str,
            Field(
                default=None,
                description="Categories of the alert to look for. Comma-separated string.",
            ),
        ],
        incident_id: Annotated[
            str,
            Field(
                default=None,
                description="Microsoft Defender Incident ID for which you want to find related alerts.",
            ),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get Machine Related Alerts

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            if status is not None:
                script_params["Status"] = status
            if severity is not None:
                script_params["Severity"] = severity
            if category is not None:
                script_params["Category"] = category
            if incident_id is not None:
                script_params["Incident ID"] = incident_id

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Get Machine Related Alerts",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Get Machine Related Alerts",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Get Machine Related Alerts for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_wait_task_status(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        task_i_ds: Annotated[
            str, Field(..., description="Task IDs list. Comma-separated string")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Wait for Task Status

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Task IDs"] = task_i_ds

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Wait Task Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Wait Task Status",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Wait Task Status for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_get_file_related_machines(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        machine_name: Annotated[
            str, Field(default=None, description="Full Machine Name to look for")
        ],
        machine_ip_address: Annotated[
            str, Field(default=None, description="Machine IP Address to look for")
        ],
        machine_risk_score: Annotated[
            str,
            Field(
                default=None,
                description="Machine risk score to look for. Comma-separated string.",
            ),
        ],
        machine_health_status: Annotated[
            str,
            Field(
                default=None,
                description="Machine health status to look for. Comma-separated string",
            ),
        ],
        machine_os_platform: Annotated[
            str, Field(default=None, description="Machine OS platform to look for.")
        ],
        rbac_group_id: Annotated[
            str, Field(default=None, description="RBAC Group ID to look for.")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get File Related Machines. Note: For this action only SHA1 is supported

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            if machine_name is not None:
                script_params["Machine Name"] = machine_name
            if machine_ip_address is not None:
                script_params["Machine IP Address"] = machine_ip_address
            if machine_risk_score is not None:
                script_params["Machine Risk Score"] = machine_risk_score
            if machine_health_status is not None:
                script_params["Machine Health Status"] = machine_health_status
            if machine_os_platform is not None:
                script_params["Machine OS Platform"] = machine_os_platform
            if rbac_group_id is not None:
                script_params["RBAC Group ID"] = rbac_group_id

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Get File Related Machines",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Get File Related Machines",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Get File Related Machines for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_get_current_task_status(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        task_i_ds: Annotated[
            str, Field(..., description="Task IDs list. Comma-separated string")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get Current Task Status

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Task IDs"] = task_i_ds

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Get Current Task Status",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Get Current Task Status",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Get Current Task Status for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_create_stop_and_quarantine_file_specific_machine_task(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        sha1_file_hash_to_quarantine: Annotated[
            str, Field(..., description="SHA1 File Hash to Quarantine")
        ],
        comment: Annotated[
            str, Field(..., description="Comment to associate with the action")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Create Stop and Quarantine a File on Specific Machine Task

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["SHA1 File Hash to Quarantine"] = sha1_file_hash_to_quarantine
            script_params["Comment"] = comment

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Create Stop And Quarantine File Specific Machine Task",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Create Stop And Quarantine File Specific Machine Task",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Create Stop And Quarantine File Specific Machine Task for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_create_isolate_machine_task(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        isolation_type: Annotated[str, Field(..., description="Isolation type")],
        comment: Annotated[
            str, Field(..., description="Comment why the machine needs to be isolated")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Create Isolate Machine Task

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Isolation Type"] = isolation_type
            script_params["Comment"] = comment

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Create Isolate Machine Task",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Create Isolate Machine Task",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Create Isolate Machine Task for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_update_alert(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        alert_id: Annotated[
            str, Field(..., description="Microsoft Defender ATP Alert ID to update.")
        ],
        status: Annotated[
            List[str], Field(default=None, description="Status of the alert")
        ],
        assigned_to: Annotated[
            str, Field(default=None, description="User who is assigned to this alert")
        ],
        classification: Annotated[
            List[str],
            Field(default=None, description="Classification to update alert with"),
        ],
        determination: Annotated[
            List[str],
            Field(default=None, description="Determination to update alert with"),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Update Alerts

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Alert ID"] = alert_id
            if status is not None:
                script_params["Status"] = status
            if assigned_to is not None:
                script_params["Assigned To"] = assigned_to
            if classification is not None:
                script_params["Classification"] = classification
            if determination is not None:
                script_params["Determination"] = determination

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Update Alert",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Update Alert",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Update Alert for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_list_alerts(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        time_frame: Annotated[
            str,
            Field(
                default=None,
                description="Time frame in hours for which to fetch Alerts",
            ),
        ],
        status: Annotated[
            str,
            Field(
                default=None,
                description="Statuses of the alert to look for. Comma-separated string",
            ),
        ],
        severity: Annotated[
            str,
            Field(
                default=None,
                description="Severities of the alert to look for. Comma-separated string.",
            ),
        ],
        category: Annotated[
            str,
            Field(
                default=None,
                description="Categories of the alert to look for. Comma-separated string.",
            ),
        ],
        incident_id: Annotated[
            str,
            Field(
                default=None,
                description="Microsoft Defender Incident ID for which you want to find related alerts.",
            ),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get Alerts

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            if time_frame is not None:
                script_params["Time Frame"] = time_frame
            if status is not None:
                script_params["Status"] = status
            if severity is not None:
                script_params["Severity"] = severity
            if category is not None:
                script_params["Category"] = category
            if incident_id is not None:
                script_params["Incident ID"] = incident_id

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_List Alerts",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_List Alerts",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_List Alerts for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_ping(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Ping",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Ping for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_get_machine_logon_users(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get Machine Log on users

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Get Machine Logon Users",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Get Machine Logon Users",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Get Machine Logon Users for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_list_machines(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        last_seen_time_frame: Annotated[
            str,
            Field(
                default=None,
                description="Time frame in hours for which to fetch Machines",
            ),
        ],
        machine_name: Annotated[
            str, Field(default=None, description="Full Machine Name to look for")
        ],
        machine_ip_address: Annotated[
            str, Field(default=None, description="Machine IP Address to look for")
        ],
        machine_risk_score: Annotated[
            str,
            Field(
                default=None,
                description="Machine risk score to look for. Comma-separated string.",
            ),
        ],
        machine_health_status: Annotated[
            str,
            Field(
                default=None,
                description="Machine health status to look for. Comma-separated string",
            ),
        ],
        machine_os_platform: Annotated[
            str, Field(default=None, description="Machine OS platform to look for.")
        ],
        rbac_group_id: Annotated[
            str, Field(default=None, description="RBAC Group ID to look for.")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get Machines

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            if last_seen_time_frame is not None:
                script_params["Last Seen Time Frame"] = last_seen_time_frame
            if machine_name is not None:
                script_params["Machine Name"] = machine_name
            if machine_ip_address is not None:
                script_params["Machine IP Address"] = machine_ip_address
            if machine_risk_score is not None:
                script_params["Machine Risk Score"] = machine_risk_score
            if machine_health_status is not None:
                script_params["Machine Health Status"] = machine_health_status
            if machine_os_platform is not None:
                script_params["Machine OS Platform"] = machine_os_platform
            if rbac_group_id is not None:
                script_params["RBAC Group ID"] = rbac_group_id

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_List Machines",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_List Machines",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_List Machines for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_list_indicators(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        indicators: Annotated[
            str,
            Field(
                default=None,
                description="Specify a comma-separated list of indicators that you would like to retrieve.",
            ),
        ],
        indicator_types: Annotated[
            str,
            Field(
                default=None,
                description="Specify a comma-separated list of indicator types that you want to retrieve. Possible values: FileSha1, FileSha256, FileMd5, CertificateThumbprint, IpAddress, DomainName, Url.",
            ),
        ],
        actions: Annotated[
            str,
            Field(
                default=None,
                description="Specify a comma-separated list of indicator actions that you want to use for filtering. Possible values: Warn,Block,Audit,Alert,AlertAndBlock,BlockAndRemediate,Allowed.",
            ),
        ],
        severity: Annotated[
            str,
            Field(
                default=None,
                description="Specify a comma-separated list of severities that you want to use for filtering. Possible values: Informational,Low,Medium,High.",
            ),
        ],
        max_results_to_return: Annotated[
            str,
            Field(
                default=None,
                description="Specify how many indicators to return. Default: 50.",
            ),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """List indicators in Microsoft Defender ATP.

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            if indicators is not None:
                script_params["Indicators"] = indicators
            if indicator_types is not None:
                script_params["Indicator Types"] = indicator_types
            if actions is not None:
                script_params["Actions"] = actions
            if severity is not None:
                script_params["Severity"] = severity
            if max_results_to_return is not None:
                script_params["Max Results To Return"] = max_results_to_return

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_List Indicators",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_List Indicators",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_List Indicators for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_submit_entity_indicators(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        action: Annotated[
            List[str],
            Field(
                ...,
                description='Specify the action that needs to be applied to the entities. Note: "Block And Remediate" is supported only for filehash entities.',
            ),
        ],
        severity: Annotated[
            List[str],
            Field(..., description="Specify the severity for the found entities."),
        ],
        indicator_alert_title: Annotated[
            str,
            Field(
                ...,
                description="Specify what should be the title for the alert, if they are identified in the environment.",
            ),
        ],
        description: Annotated[
            str, Field(..., description="Specify the description for the entities.")
        ],
        application: Annotated[
            str,
            Field(
                default=None,
                description="Specify an application that is related to the entities.",
            ),
        ],
        recommended_action: Annotated[
            str,
            Field(
                default=None,
                description="Specify what should be the recommended actions for the handling of the entities.",
            ),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Submit entities as indicators in Microsoft Defender ATP. Supported entities: Filehash, URL, IP Address. Note: only MD5, SHA1 and SHA256 hashes are supported.

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Action"] = action
            script_params["Severity"] = severity
            if application is not None:
                script_params["Application"] = application
            script_params["Indicator Alert Title"] = indicator_alert_title
            script_params["Description"] = description
            if recommended_action is not None:
                script_params["Recommended Action"] = recommended_action

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Submit Entity Indicators",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Submit Entity Indicators",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Submit Entity Indicators for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_get_file_related_alerts(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        status: Annotated[
            str,
            Field(
                default=None,
                description="Statuses of the alert to look for. Comma-separated string",
            ),
        ],
        severity: Annotated[
            str,
            Field(
                default=None,
                description="Severities of the alert to look for. Comma-separated string.",
            ),
        ],
        category: Annotated[
            str,
            Field(
                default=None,
                description="Categories of the alert to look for. Comma-separated string.",
            ),
        ],
        incident_id: Annotated[
            str,
            Field(
                default=None,
                description="Microsoft Defender Incident ID for which you want to find related alerts.",
            ),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Get File Related Alerts. Note: For this action only SHA1 is supported

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            if status is not None:
                script_params["Status"] = status
            if severity is not None:
                script_params["Severity"] = severity
            if category is not None:
                script_params["Category"] = category
            if incident_id is not None:
                script_params["Incident ID"] = incident_id

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Get File Related Alerts",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Get File Related Alerts",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Get File Related Alerts for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_enrich_entities(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """This action allows a user to enrich Microsoft Defender ATP hosts, ips and file hashes. Note: File hash can be in sha1 or sha256 format.

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Enrich Entities",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Enrich Entities for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_create_run_antivirus_scan_task(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        antivirus_scan_type: Annotated[
            List[str], Field(..., description="Antivirus Scan Type")
        ],
        comment: Annotated[
            str,
            Field(
                ...,
                description="Comment why an antivirus scan needs to be executed on the machine",
            ),
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Create Run AV Scan Task

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}
            script_params["Antivirus Scan Type"] = antivirus_scan_type
            script_params["Comment"] = comment

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Create Run Antivirus Scan Task",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Create Run Antivirus Scan Task",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Create Run Antivirus Scan Task for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_create_unisolate_machine_task(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        comment: Annotated[
            str, Field(..., description="Comment why the machine needs to be isolated")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Create Unisolate Machine Task

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

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
                actionName="MicrosoftDefenderATP_Create Unisolate Machine Task",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Create Unisolate Machine Task",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Create Unisolate Machine Task for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def microsoft_defender_atp_delete_entity_indicators(
        case_id: Annotated[str, Field(..., description="The ID of the case.")],
        alert_group_identifiers: Annotated[
            List[str], Field(..., description="Identifiers for the alert groups.")
        ],
        target_entities: Annotated[
            List[TargetEntity],
            Field(
                default_factory=list,
                description="Optional list of specific target entities (Identifier, EntityType) to run the action on.",
            ),
        ],
        scope: Annotated[
            str,
            Field(
                default="All entities", description="Defines the scope for the action."
            ),
        ],
    ) -> dict:
        """Delete entity indicators in Microsoft Defender ATP. Supported entities: Filehash, URL, IP Address. Note: only MD5, SHA1 and SHA256 hashes are supported.

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
            final_target_entities = []  # Pass empty list for entities when using scope
            final_scope = scope
            is_predefined_scope = True

        # Fetch integration instance identifier
        try:
            instance_response = await bindings.http_client.get(
                Endpoints.LIST_INTEGRATION_INSTANCES.format(
                    INTEGRATION_NAME="MicrosoftDefenderATP"
                )
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            print(f"Error fetching instance for MicrosoftDefenderATP: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}

        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                return {
                    "Status": "Failed",
                    "Message": "Instance found but identifier is missing.",
                }

            script_params = {}

            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope,
                actionProvider="Scripts",
                actionName="MicrosoftDefenderATP_Delete Entity Indicators",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "MicrosoftDefenderATP_Delete Entity Indicators",
                    "ScriptParametersEntityFields": json.dumps(script_params),
                },
            )

            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION, req=action_data.model_dump()
                )
                return execution_response
            except Exception as e:
                print(
                    f"Error executing action MicrosoftDefenderATP_Delete Entity Indicators for MicrosoftDefenderATP: {e}"
                )
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(
                f"Warning: No active integration instance found for MicrosoftDefenderATP"
            )
            return {"Status": "Failed", "Message": "No active instance found."}
