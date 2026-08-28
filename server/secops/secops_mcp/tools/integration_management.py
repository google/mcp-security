# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Security Operations MCP tools for SOAR Integrations and Manual Action Execution."""

import logging
from typing import Any, Dict, List, Optional

from secops_mcp.server import get_chronicle_client, server

logger = logging.getLogger("secops-mcp")


def _get_base_endpoint(chronicle: Any, version: str = "v1") -> str:
    """Get the base REST endpoint for Chronicle 1P resources."""
    if version == "v1" and hasattr(chronicle, "base_v1_url") and chronicle.base_v1_url:
        return f"{chronicle.base_v1_url}/{chronicle.instance_id}"
    base_url = chronicle.base_url
    if version == "v1" and "/v1alpha" in base_url:
        base_url = base_url.replace("/v1alpha", "/v1")
    return f"{base_url}/{chronicle.instance_id}"


@server.tool()
async def list_integrations(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List all SOAR Integrations configured for a Chronicle instance.

    Retrieves a paginated list of third-party tool connections (EDR, Firewall, SIEM, TI, Ticketing).

    Args:
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        filter_query (Optional[str]): Filter expression (e.g. 'Identifier = "SiemplifyUtilities"').
        order_by (Optional[str]): Sort order (e.g. "DisplayName asc").
        page_size (int): Max results per page. Defaults to 50.
        page_token (Optional[str]): Pagination token.

    Returns:
        Dict[str, Any]: List of integration objects and pagination metadata.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/integrations"

        params: Dict[str, Any] = {"pageSize": page_size}
        if filter_query:
            params["filter"] = filter_query
        if order_by:
            params["orderBy"] = order_by
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list integrations: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing integrations: %s", e)
        return {"error": f"Failed to list integrations: {str(e)}"}


@server.tool()
async def list_integration_actions(
    integration_id: str = "-",
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List all actions provided by a SOAR Integration (or across all integrations if integration_id='-').

    Args:
        integration_id (str): Integration ID or '-' for all integrations.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        filter_query (Optional[str]): Filter expression.
        order_by (Optional[str]): Sort order.
        page_size (int): Max results per page. Defaults to 50.
        page_token (Optional[str]): Pagination token.

    Returns:
        Dict[str, Any]: List of integration actions (e.g. 'block_ip', 'get_user_details').
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = integration_id.split("/")[-1] if integration_id != "-" else "-"
        url = f"{_get_base_endpoint(chronicle)}/integrations/{short_id}/actions"

        params: Dict[str, Any] = {"pageSize": page_size}
        if filter_query:
            params["filter"] = filter_query
        if order_by:
            params["orderBy"] = order_by
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list integration actions: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing integration actions: %s", e)
        return {"error": f"Failed to list integration actions: {str(e)}"}


@server.tool()
async def list_integration_instances(
    integration_id: str = "-",
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List configured instances of an integration to retrieve instance GUIDs for action execution.

    Args:
        integration_id (str): Integration ID or '-' for all integrations.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        filter_query (Optional[str]): Filter expression.
        order_by (Optional[str]): Sort order.
        page_size (int): Max instances to return. Defaults to 50.
        page_token (Optional[str]): Pagination token.

    Returns:
        Dict[str, Any]: List of integration instances with instance GUIDs.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = integration_id.split("/")[-1] if integration_id != "-" else "-"
        url = f"{_get_base_endpoint(chronicle)}/integrations/{short_id}/instances"

        params: Dict[str, Any] = {"pageSize": page_size}
        if filter_query:
            params["filter"] = filter_query
        if order_by:
            params["orderBy"] = order_by
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list integration instances: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing integration instances: %s", e)
        return {"error": f"Failed to list integration instances: {str(e)}"}


@server.tool()
async def execute_manual_action(
    case_id: str,
    action_name: str,
    action_provider: str = "Scripts",
    properties: Optional[Dict[str, Any]] = None,
    target_entities: Optional[List[Dict[str, Any]]] = None,
    alert_group_identifiers: Optional[List[str]] = None,
    scope: Optional[str] = None,
    is_predefined_scope: bool = True,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute a manual SOAR action or script on a case, alert, or target entities.

    Executes response actions such as isolating hosts, blocking IPs, disabling accounts,
    or executing threat intelligence queries.

    Args:
        case_id (str): The Case ID.
        action_name (str): Action name (e.g. 'SiemplifyUtilities_Ping', 'VirusTotal_Enrich IP').
        action_provider (str): Provider name, typically 'Scripts'. Defaults to 'Scripts'.
        properties (Optional[Dict[str, Any]]): Dictionary containing `ScriptName`, `IntegrationInstance` GUID,
            and `ScriptParametersEntityFields` JSON string.
        target_entities (Optional[List[Dict[str, Any]]]): Entities targeted by this action.
        alert_group_identifiers (Optional[List[str]]): Alert group identifiers associated with action.
        scope (Optional[str]): Action scope (e.g. 'All entities').
        is_predefined_scope (bool): Whether predefined scope is used. Defaults to True.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Action execution result or tracking ID.
    """
    try:
        if not case_id or not action_name:
            return {"error": "Both case_id and action_name parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}:executeManualAction"

        body: Dict[str, Any] = {
            "caseId": short_case_id,
            "actionName": action_name,
            "actionProvider": action_provider,
            "isPredefinedScope": is_predefined_scope,
        }
        if properties:
            body["properties"] = properties
        if target_entities:
            body["targetEntities"] = target_entities
        if alert_group_identifiers:
            body["alertGroupIdentifiers"] = alert_group_identifiers
        if scope:
            body["scope"] = scope

        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to execute manual action: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error executing manual action %s: %s", action_name, e)
        return {"error": f"Failed to execute manual action: {str(e)}"}


@server.tool()
async def get_action_result_by_id(
    action_result_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve the result and execution logs of an asynchronous SOAR action execution by its result ID.

    Args:
        action_result_id (str): The action result execution ID.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Execution status, output data, logs, and affected entities.
    """
    try:
        if not action_result_id:
            return {"error": "action_result_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/actionResults/{action_result_id}"

        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {
                "error": f"Failed to get action result: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting action result %s: %s", action_result_id, e)
        return {"error": f"Failed to get action result: {str(e)}"}
