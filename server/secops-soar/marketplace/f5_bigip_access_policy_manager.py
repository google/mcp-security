import bindings
from fastmcp import FastMCP
from utils.consts import Endpoints
from utils.models import ApiManualActionDataModel, TargetEntity
import json
from typing import Optional, Any, List, Dict, Union, Annotated
from pydantic import Field


def register_tools(mcp: FastMCP):
    # This function registers all tools (actions) for the F5BIGIPAccessPolicyManager integration.

    @mcp.tool()
    async def f5_bigip_access_policy_manager_ping(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """Test connectivity to the F5 BIG-IP Access Policy Manager with parameters provided at the integration configuration page on the Marketplace tab.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="F5BIGIPAccessPolicyManager")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for F5BIGIPAccessPolicyManager: {e}")
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
                actionName="F5BIGIPAccessPolicyManager_Ping",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "F5BIGIPAccessPolicyManager_Ping", # Assuming same as actionName
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
                print(f"Error executing action F5BIGIPAccessPolicyManager_Ping for F5BIGIPAccessPolicyManager: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for F5BIGIPAccessPolicyManager")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def f5_bigip_access_policy_manager_list_active_sessions(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], limit: Annotated[Optional[str], Field(default=None, description="Specify the maximum number of entries you would like to get in the action.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """The action will list all the currently active sessions in the F5 BIG-IP Access Policy Manager.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="F5BIGIPAccessPolicyManager")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for F5BIGIPAccessPolicyManager: {e}")
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
            if limit is not None:
                script_params["Limit"] = limit
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="F5BIGIPAccessPolicyManager_List Active Sessions",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "F5BIGIPAccessPolicyManager_List Active Sessions", # Assuming same as actionName
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
                print(f"Error executing action F5BIGIPAccessPolicyManager_List Active Sessions for F5BIGIPAccessPolicyManager: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for F5BIGIPAccessPolicyManager")
            return {"Status": "Failed", "Message": "No active instance found."}

    @mcp.tool()
    async def f5_bigip_access_policy_manager_disconnect_sessions(case_id: Annotated[str, Field(..., description="The ID of the case.")], alert_group_identifiers: Annotated[List[str], Field(..., description="Identifiers for the alert groups.")], use_case_entities: Annotated[Optional[bool], Field(default=None, description="Specify whether the action should disconnect sessions using Address and Client IP entities found in the case, or work on the provided parameters only. NOTE - once checked, action will ignore all other parameters in the action")], session_i_ds: Annotated[Optional[str], Field(default=None, description="Specify specific session IDs you would like to disconnect, in a comma separated list")], logon_user_names: Annotated[Optional[str], Field(default=None, description="Specify Logon User Names you would like to disconnect sessions for, in a comma separated list, so only sessions for these Logon User Names will be disconnected.")], client_i_ps: Annotated[Optional[str], Field(default=None, description="Specify Client IPs you would like to disconnect the sessions for,in a comma separated list, so only sessions for these Client IPs will be disconnected.")], target_entities: Annotated[List[TargetEntity], Field(default_factory=list, description="Optional list of specific target entities (Identifier, EntityType) to run the action on.")], scope: Annotated[str, Field(default="All entities", description="Defines the scope for the action.")]) -> dict:
        """The action will disconnect the specified sessions from the F5 BIG-IP instance. Action can work using entities or using parameters, according to the Use Case Entities parameter’s value. Supported entities are Address and User Name. NOTE - Filters will be used with an OR logic, so that every session that even one of the parameters, or entities, will be matched in - will be disconnected.

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
                Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="F5BIGIPAccessPolicyManager")
            )
            instances = instance_response.get("integration_instances", [])
        except Exception as e:
            # Log error appropriately in real code
            print(f"Error fetching instance for F5BIGIPAccessPolicyManager: {e}")
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
            if use_case_entities is not None:
                script_params["Use Case Entities"] = use_case_entities
            if session_i_ds is not None:
                script_params["Session IDs"] = session_i_ds
            if logon_user_names is not None:
                script_params["Logon User Names"] = logon_user_names
            if client_i_ps is not None:
                script_params["Client IPs"] = client_i_ps
    
            # Prepare data model for the API request
            action_data = ApiManualActionDataModel(
                alertGroupIdentifiers=alert_group_identifiers,
                caseId=case_id,
                targetEntities=final_target_entities,
                scope=final_scope,
                isPredefinedScope=is_predefined_scope, # Pass the is_predefined_scope parameter
                actionProvider="Scripts", # Assuming constant based on example
                actionName="F5BIGIPAccessPolicyManager_Disconnect Sessions",
                properties={
                    "IntegrationInstance": instance_identifier,
                    "ScriptName": "F5BIGIPAccessPolicyManager_Disconnect Sessions", # Assuming same as actionName
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
                print(f"Error executing action F5BIGIPAccessPolicyManager_Disconnect Sessions for F5BIGIPAccessPolicyManager: {e}")
                return {"Status": "Failed", "Message": f"Error executing action: {e}"}
        else:
            print(f"Warning: No active integration instance found for F5BIGIPAccessPolicyManager")
            return {"Status": "Failed", "Message": "No active instance found."}
