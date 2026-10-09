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
"""Security Operations MCP tools for SOAR Connector Events."""

import logging
from typing import Any, Dict, Optional

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
async def list_connector_events(
    connector_id: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List connector events ingested through Chronicle SOAR connectors.

    Args:
        connector_id (Optional[str]): Optional filter by connector identifier.
        filter_query (Optional[str]): Filter expression.
        order_by (Optional[str]): Sort order (e.g. "create_time desc").
        page_size (int): Max events to return. Defaults to 50.
        page_token (Optional[str]): Pagination token.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: List of connector event objects and pagination metadata.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/connectorEvents"

        params: Dict[str, Any] = {"pageSize": page_size}
        if connector_id:
            params["connectorId"] = connector_id
        if filter_query:
            params["filter"] = filter_query
        if order_by:
            params["orderBy"] = order_by
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list connector events: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing connector events: %s", e)
        return {"error": f"Failed to list connector events: {str(e)}"}


@server.tool()
async def get_connector_event(
    connector_event_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve full details of a specific connector event.

    Args:
        connector_event_id (str): The unique connector event ID or resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Detailed connector event object.
    """
    try:
        if not connector_event_id:
            return {"error": "connector_event_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = connector_event_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/connectorEvents/{short_id}"

        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {
                "error": f"Failed to get connector event: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting connector event %s: %s", connector_event_id, e)
        return {"error": f"Failed to get connector event: {str(e)}"}
