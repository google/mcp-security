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
"""Security Operations MCP tools for SOAR Playbook Management and Execution."""

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
async def list_playbooks(
    playbook_types: Optional[List[str]] = None,
    filter_query: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List all available playbooks (automated workflows) configured in the Chronicle SOAR instance.

    Args:
        playbook_types (Optional[List[str]]): Filter by playbook types (e.g. ['REGULAR', 'NESTED']).
        filter_query (Optional[str]): Additional filter expression.
        page_size (int): Max playbooks to return. Defaults to 50.
        page_token (Optional[str]): Pagination token.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: List of playbook objects and metadata.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/playbooks"

        params: Dict[str, Any] = {"pageSize": page_size}
        if playbook_types:
            params["playbookTypes"] = playbook_types
        if filter_query:
            params["filter"] = filter_query
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list playbooks: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing playbooks: %s", e)
        return {"error": f"Failed to list playbooks: {str(e)}"}


@server.tool()
async def get_playbook(
    playbook_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get full details, configuration, trigger conditions, and step definitions for a specific playbook.

    Args:
        playbook_id (str): The unique Playbook ID or resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Detailed Playbook object.
    """
    try:
        if not playbook_id:
            return {"error": "playbook_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = playbook_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/playbooks/{short_id}"

        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {
                "error": f"Failed to get playbook: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting playbook %s: %s", playbook_id, e)
        return {"error": f"Failed to get playbook: {str(e)}"}


@server.tool()
async def list_playbook_instances(
    case_id: str,
    alert_group_identifier: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List historical and active playbook execution instances for a given Case and/or Alert Group.

    Args:
        case_id (str): The Case ID or full resource name.
        alert_group_identifier (Optional[str]): Optional alert group identifier to filter executions.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: List of playbook execution cards and step outcomes.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}:listPlaybookInstances"

        params: Dict[str, Any] = {}
        if alert_group_identifier:
            params["alertGroupIdentifier"] = alert_group_identifier

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list playbook instances: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing playbook instances for case %s: %s", case_id, e)
        return {"error": f"Failed to list playbook instances: {str(e)}"}


@server.tool()
async def execute_playbook(
    case_id: str,
    playbook_id: str,
    alert_group_identifier: Optional[str] = None,
    scope: Optional[str] = None,
    target_entities: Optional[List[Dict[str, Any]]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute/trigger a specific SOAR playbook manually on a Case or Alert.

    Args:
        case_id (str): The Case ID to run the playbook on.
        playbook_id (str): The ID of the playbook to execute.
        alert_group_identifier (Optional[str]): Optional target alert group identifier.
        scope (Optional[str]): Execution scope (e.g. 'All entities', 'Specific entities').
        target_entities (Optional[List[Dict[str, Any]]]): Entities to pass to the playbook execution.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Playbook execution tracking status and instance ID.
    """
    try:
        if not case_id or not playbook_id:
            return {"error": "Both case_id and playbook_id parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_playbook_id = playbook_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/playbooks/{short_playbook_id}:execute"

        body: Dict[str, Any] = {"playbookId": short_playbook_id}
        if alert_group_identifier:
            body["alertGroupIdentifier"] = alert_group_identifier
        if scope:
            body["scope"] = scope
        if target_entities:
            body["targetEntities"] = target_entities

        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to execute playbook: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error executing playbook %s on case %s: %s", playbook_id, case_id, e)
        return {"error": f"Failed to execute playbook: {str(e)}"}


@server.tool()
async def trigger_playbook(
    case_id: str,
    playbook_id: str,
    alert_group_identifier: Optional[str] = None,
    scope: Optional[str] = None,
    target_entities: Optional[List[Dict[str, Any]]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Alias for execute_playbook. Manually triggers a SOAR playbook workflow on a case or alert."""
    return await execute_playbook(
        case_id=case_id,
        playbook_id=playbook_id,
        alert_group_identifier=alert_group_identifier,
        scope=scope,
        target_entities=target_entities,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
    )
