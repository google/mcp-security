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
"""Security Operations MCP tools for SOAR Entity Investigation and Discovery."""

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
async def get_involved_entity(
    case_id: str,
    alert_id: str,
    involved_entity_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve detailed properties of an involved entity associated with a case alert.

    Args:
        case_id (str): The Case ID or full resource name.
        alert_id (str): The Alert ID or full resource name.
        involved_entity_id (str): The unique involved entity identifier.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Detailed InvolvedEntity object including type, identifier,
            suspicious flag, environment, and enrichments.
    """
    try:
        if not case_id or not alert_id or not involved_entity_id:
            return {"error": "case_id, alert_id, and involved_entity_id parameters are all required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        short_entity_id = involved_entity_id.split("/")[-1]

        url = (
            f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/"
            f"{short_alert_id}/involvedEntities/{short_entity_id}"
        )

        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {
                "error": f"Failed to get involved entity: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting involved entity %s: %s", involved_entity_id, e)
        return {"error": f"Failed to get involved entity: {str(e)}"}


@server.tool()
async def list_involved_entities(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List all entities (IPs, domains, hashes, users, hostnames) involved in a case alert.

    Args:
        case_id (str): The Case ID or full resource name.
        alert_id (str): The Alert ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        filter_query (Optional[str]): Filter expression.
        page_size (int): Max entities to return. Defaults to 50.
        page_token (Optional[str]): Pagination token.

    Returns:
        Dict[str, Any]: List of InvolvedEntity objects and pagination token.
    """
    try:
        if not case_id or not alert_id:
            return {"error": "Both case_id and alert_id parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]

        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/{short_alert_id}/involvedEntities"
        params: Dict[str, Any] = {"pageSize": page_size}
        if filter_query:
            params["filter"] = filter_query
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list involved entities: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing involved entities for alert %s: %s", alert_id, e)
        return {"error": f"Failed to list involved entities: {str(e)}"}


@server.tool()
async def get_entities_by_alert_group_identifiers(
    case_id: str,
    alert_group_identifiers: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve entities involved in specific alert groups within a Case.

    Args:
        case_id (str): The Case ID or full resource name.
        alert_group_identifiers (List[str]): List of alert group identifiers.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Entities linked to the specified alert group identifiers.
    """
    try:
        if not case_id or not alert_group_identifiers:
            return {"error": "Both case_id and alert_group_identifiers parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}:getEntitiesByAlertGroupIdentifiers"

        body = {"caseId": short_case_id, "alertGroupIdentifiers": alert_group_identifiers}
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to get entities by alert group identifiers: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting entities by alert groups for case %s: %s", case_id, e)
        return {"error": f"Failed to get entities by alert group identifiers: {str(e)}"}


@server.tool()
async def get_entity_details(
    entity_identifier: str,
    entity_type: str,
    entity_environment: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch detailed information and enrichments for a specific entity known to the SOAR platform.

    Args:
        entity_identifier (str): The unique identifier of the entity (e.g., "192.168.1.100", "user@corp.com").
        entity_type (str): The type of the entity (e.g., "IP Address", "Hostname", "User", "Hash").
        entity_environment (Optional[str]): The environment context (e.g., "Production", "Corporate").
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Detailed entity attributes, risk scores, and enrichment metadata.
    """
    try:
        if not entity_identifier or not entity_type:
            return {"error": "Both entity_identifier and entity_type parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}:fetchFullEntityDetails"

        body = {
            "entityIdentifier": entity_identifier,
            "entityType": entity_type,
            "entityEnvironment": entity_environment or "Default",
        }
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to get entity details: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting entity details for %s: %s", entity_identifier, e)
        return {"error": f"Failed to get entity details: {str(e)}"}


@server.tool()
async def search_entity(
    term: Optional[str] = None,
    entity_types: Optional[List[str]] = None,
    is_suspicious: Optional[bool] = None,
    is_internal_asset: Optional[bool] = None,
    is_enriched: Optional[bool] = None,
    network_name: Optional[List[str]] = None,
    environment_name: Optional[List[str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 50,
) -> Dict[str, Any]:
    """Search for entities across the SOAR platform matching specific attributes and flags.

    Args:
        term (Optional[str]): Partial string to match against entity names or identifiers.
        entity_types (Optional[List[str]]): List of types to filter by (e.g. ['IP Address', 'Hostname']).
        is_suspicious (Optional[bool]): Filter for entities flagged as suspicious.
        is_internal_asset (Optional[bool]): Filter for internal assets.
        is_enriched (Optional[bool]): Filter for entities with threat intelligence enrichment.
        network_name (Optional[List[str]]): Filter by network identifiers.
        environment_name (Optional[List[str]]): Filter by environment names.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        page_size (int): Max entities to return. Defaults to 50.

    Returns:
        Dict[str, Any]: List of matching entity objects.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle, version='v1alpha')}:searchEntities"

        # 1. Try standard GET with indicator query parameter
        if term:
            get_params = {"indicator": term, "pageSize": page_size}
            get_resp = chronicle.session.get(url, params=get_params)
            if get_resp.status_code == 200:
                return get_resp.json()

        # 2. Fall back to structured POST request
        body: Dict[str, Any] = {"pageSize": page_size}
        if term:
            body["term"] = term
        if entity_types:
            body["type"] = entity_types
        if is_suspicious is not None:
            body["isSuspicious"] = is_suspicious
        if is_internal_asset is not None:
            body["isInternalAsset"] = is_internal_asset
        if is_enriched is not None:
            body["isEnriched"] = is_enriched
        if network_name:
            body["networkName"] = network_name
        if environment_name:
            body["environmentName"] = environment_name

        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to search entities: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error searching entities: %s", e)
        return {"error": f"Failed to search entities: {str(e)}"}
