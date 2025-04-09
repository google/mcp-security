import bindings
from fastmcp import FastMCP
from utils.consts import Endpoints
from utils.models import ApiManualActionDataModel, TargetEntity
import json
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the SumoLogicCloudSIEM integration.

    @mcp.tool()
    async def sumo_logic_cloud_siem_add_tags_to_insight(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], insight_id: Annotated[str, Field(..., description="Specify the ID of the insight to which action needs to add tags.")], tags: Annotated[str, Field(..., description="Specify a comma-separated list of tags that needs to be added in insight.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add tags to insight in Sumo Logic Cloud SIEM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SumoLogicCloudSIEM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SumoLogicCloudSIEM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["caseId"] = case_id
            script_params["alertGroupIdentifiers"] = alert_group_identifiers
            script_params["scope"] = scope
            script_params["Insight ID"] = insight_id
            script_params["Tags"] = tags
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SumoLogicCloudSIEM_Add Tags To Insight",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SumoLogicCloudSIEM_Add Tags To Insight", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump() # Assumes Pydantic v2
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action SumoLogicCloudSIEM_Add Tags To Insight for SumoLogicCloudSIEM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SumoLogicCloudSIEM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sumo_logic_cloud_siem_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the Sumo Logic Cloud SIEM with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SumoLogicCloudSIEM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SumoLogicCloudSIEM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["caseId"] = case_id
            script_params["alertGroupIdentifiers"] = alert_group_identifiers
            script_params["scope"] = scope
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SumoLogicCloudSIEM_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SumoLogicCloudSIEM_Ping", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump() # Assumes Pydantic v2
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action SumoLogicCloudSIEM_Ping for SumoLogicCloudSIEM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SumoLogicCloudSIEM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sumo_logic_cloud_siem_update_insight(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], insight_id: Annotated[str, Field(..., description="Specify the ID of the insight needs to be updated.")], status: Annotated[List[Any], Field(..., description="Specify what status to set for the insight.")], assignee_type: Annotated[List[Any], Field(..., description="Specify the assignee type for the \"Assignee\" parameter.")], assignee: Annotated[Optional[str], Field(default=None, description="Specify the assignee identifier.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Update insight status in Sumo Logic Cloud SIEM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SumoLogicCloudSIEM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SumoLogicCloudSIEM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["caseId"] = case_id
            script_params["alertGroupIdentifiers"] = alert_group_identifiers
            script_params["scope"] = scope
            script_params["Insight ID"] = insight_id
            script_params["Status"] = status
            script_params["Assignee Type"] = assignee_type
            if assignee is not None:
                script_params["Assignee"] = assignee
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SumoLogicCloudSIEM_Update Insight",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SumoLogicCloudSIEM_Update Insight", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump() # Assumes Pydantic v2
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action SumoLogicCloudSIEM_Update Insight for SumoLogicCloudSIEM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SumoLogicCloudSIEM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sumo_logic_cloud_siem_enrich_entities(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], create_insight: Annotated[Optional[bool], Field(default=None, description="If enabled, action will create an insight containing all of the retrieved information about the entity.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Enrich entities using information from Sumo Logic Cloud SIEM. Supported entities: Hostname, User, IP address.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SumoLogicCloudSIEM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SumoLogicCloudSIEM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["caseId"] = case_id
            script_params["alertGroupIdentifiers"] = alert_group_identifiers
            script_params["scope"] = scope
            if create_insight is not None:
                script_params["Create Insight"] = create_insight
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SumoLogicCloudSIEM_Enrich Entities",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SumoLogicCloudSIEM_Enrich Entities", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump() # Assumes Pydantic v2
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action SumoLogicCloudSIEM_Enrich Entities for SumoLogicCloudSIEM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SumoLogicCloudSIEM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sumo_logic_cloud_siem_add_comment_to_insight(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], insight_id: Annotated[str, Field(..., description="Specify the ID of the insight to which action needs to add a comment.")], comment: Annotated[str, Field(..., description="Specify the comment that needs to be added in insight.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Add a comment to insight in Sumo Logic Cloud SIEM.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SumoLogicCloudSIEM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SumoLogicCloudSIEM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["caseId"] = case_id
            script_params["alertGroupIdentifiers"] = alert_group_identifiers
            script_params["scope"] = scope
            script_params["Insight ID"] = insight_id
            script_params["Comment"] = comment
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SumoLogicCloudSIEM_Add Comment To Insight",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SumoLogicCloudSIEM_Add Comment To Insight", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump() # Assumes Pydantic v2
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action SumoLogicCloudSIEM_Add Comment To Insight for SumoLogicCloudSIEM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SumoLogicCloudSIEM")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def sumo_logic_cloud_siem_search_entity_signals(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], lowest_severity_to_return: Annotated[Optional[str], Field(default=None, description="Specify the lowest severity number that will be used to return signals. Maximum: 10.")], time_frame: Annotated[Optional[List[Any]], Field(default=None, description="Specify a time frame for the results. If \"Custom\" is selected, you also need to provide \"Start Time\". If \"30 Minutes Around Alert Time\" is selected, action will search the alerts 30 minutes before the alert happened till the 30 minutes after the alert has happened.  Same idea applies to \"1 Hour Around Alert Time\" and \"5 Minutes Around Alert Time\".")], start_time: Annotated[Optional[str], Field(default=None, description="Specify the start time for the results. This parameter is mandatory, if \"Custom\" is selected for the \"Time Frame\" parameter. Format: ISO 8601")], end_time: Annotated[Optional[str], Field(default=None, description="Specify the end time for the results. Format: ISO 8601. If nothing is provided and \"Custom\" is selected for the \"Time Frame\" parameter then this parameter will use current time.")], max_signals_to_return: Annotated[Optional[str], Field(default=None, description="Specify how many signals to return per entity. Default: 50.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Search signals related to entities in Sumo Logic Cloud SIEM. Supported entities: IP Address, Hostname, Username.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="SumoLogicCloudSIEM")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for SumoLogicCloudSIEM: {e}")
            return {"Status": "Failed", "Message": f"Error fetching instance: {e}"}
    
        if instances:
            instance_identifier = instances[0].get("identifier")
            if not instance_identifier:
                # Log error or handle missing identifier
                return {"Status": "Failed", "Message": "Instance found but identifier is missing."}
    
            # Construct parameters dictionary for the API call
            script_params = {}
            script_params["caseId"] = case_id
            script_params["alertGroupIdentifiers"] = alert_group_identifiers
            script_params["scope"] = scope
            if lowest_severity_to_return is not None:
                script_params["Lowest Severity To Return"] = lowest_severity_to_return
            if time_frame is not None:
                script_params["Time Frame"] = time_frame
            if start_time is not None:
                script_params["Start Time"] = start_time
            if end_time is not None:
                script_params["End Time"] = end_time
            if max_signals_to_return is not None:
                script_params["Max Signals To Return"] = max_signals_to_return
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="SumoLogicCloudSIEM_Search Entity Signals",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "SumoLogicCloudSIEM_Search Entity Signals", # Assuming same as actionName
                    "ScriptParametersEntityFields": json.dumps(script_params)
                }
            )
    
            # Execute the action via HTTP POST
            try:
                execution_response = await bindings.http_client.post(
                    Endpoints.EXECUTE_MANUAL_ACTION,
                    req=action_data.model_dump() # Assumes Pydantic v2
                )
                return execution_response
            except Exception as e:
                # Log error appropriately
                print(f"Error executing action SumoLogicCloudSIEM_Search Entity Signals for SumoLogicCloudSIEM: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for SumoLogicCloudSIEM")
            return {"Status": "Failed", "Message": "No active instance found."}
