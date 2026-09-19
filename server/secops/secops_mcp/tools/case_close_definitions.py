# Copyright 2026 Google LLC
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
"""Security Operations MCP tools for Case Close Definitions, Stage Definitions, Tag Definitions, and Queue Filters."""

import logging
from typing import Any, Dict, List, Optional

from secops.chronicle.case import APIVersion, chronicle_paginated_request
from secops_mcp.server import get_chronicle_client, server

logger = logging.getLogger("secops-mcp")

def _v1alpha_base(chronicle: Any) -> str:
    base = getattr(chronicle, "base_v1alpha_url", None)
    if isinstance(base, str) and base:
        return base
    return str(chronicle.base_url)



def _extract_id(value: str, segment: str) -> str:
    if f"/{segment}/" in value:
        return value.split(f"/{segment}/")[-1].split("/")[0]
    return value


@server.tool()
async def list_case_close_definitions(
    page_size: int = 50,
    page_token: Optional[str] = None,
    filter: Optional[str] = None,
    order_by: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List case close definitions (root causes and close reasons) in Chronicle."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        extra_params: Dict[str, Any] = {}
        if filter:
            extra_params["filter"] = filter
        if order_by:
            extra_params["orderBy"] = order_by

        result = chronicle_paginated_request(
            chronicle,
            path="caseCloseDefinitions",
            items_key="caseCloseDefinitions",
            api_version=APIVersion.V1,
            page_size=page_size,
            page_token=page_token,
            extra_params=extra_params if extra_params else None,
            as_list=False,
        )
        if isinstance(result, list):
            return {"caseCloseDefinitions": result}
        return result
    except Exception as e:
        error_msg = f"Error listing case close definitions: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}


@server.tool()
async def get_case_close_definition(
    close_definition_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a single Case Close Definition (`GET /v1alpha/{parent}/caseCloseDefinitions/{case_close_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(close_definition_id, "caseCloseDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseCloseDefinitions/{short_id}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case close definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case close definition: %s", e)
        return {"error": f"Failed to get case close definition: {str(e)}"}


@server.tool()
async def create_case_close_definition(
    close_reason: str,
    root_cause: str,
    display_Order: Optional[int] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a custom Case Close Definition (`POST /v1alpha/{parent}/caseCloseDefinitions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseCloseDefinitions"
        body: Dict[str, Any] = {"closeReason": close_reason, "rootCause": root_cause}
        if display_Order is not None:
            body["displayOrder"] = display_Order
        response = chronicle.session.post(url, json=body)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create case close definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating case close definition: %s", e)
        return {"error": f"Failed to create case close definition: {str(e)}"}


@server.tool()
async def update_case_close_definition(
    close_definition_id: str,
    definition_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a Case Close Definition (`PATCH /v1alpha/{parent}/caseCloseDefinitions/{case_close_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(close_definition_id, "caseCloseDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseCloseDefinitions/{short_id}"
        params = {"updateMask": update_mask} if update_mask else {}
        response = chronicle.session.patch(url, params=params, json=definition_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update case close definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating case close definition: %s", e)
        return {"error": f"Failed to update case close definition: {str(e)}"}


@server.tool()
async def delete_case_close_definition(
    close_definition_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a Case Close Definition (`DELETE /v1alpha/{parent}/caseCloseDefinitions/{case_close_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(close_definition_id, "caseCloseDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseCloseDefinitions/{short_id}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete case close definition: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "close_definition_id": short_id}
    except Exception as e:
        logger.error("Error deleting case close definition: %s", e)
        return {"error": f"Failed to delete case close definition: {str(e)}"}


@server.tool()
async def list_case_stage_definitions(
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List Case Stage Definitions (`GET /v1alpha/{parent}/caseStageDefinitions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseStageDefinitions"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case stage definitions: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case stage definitions: %s", e)
        return {"error": f"Failed to list case stage definitions: {str(e)}"}


@server.tool()
async def get_case_stage_definition(
    stage_definition_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a Case Stage Definition (`GET /v1alpha/{parent}/caseStageDefinitions/{case_stage_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(stage_definition_id, "caseStageDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseStageDefinitions/{short_id}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case stage definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case stage definition: %s", e)
        return {"error": f"Failed to get case stage definition: {str(e)}"}


@server.tool()
async def create_case_stage_definition(
    stage_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a Case Stage Definition (`POST /v1alpha/{parent}/caseStageDefinitions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseStageDefinitions"
        response = chronicle.session.post(url, json=stage_payload)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create case stage definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating case stage definition: %s", e)
        return {"error": f"Failed to create case stage definition: {str(e)}"}


@server.tool()
async def update_case_stage_definition(
    stage_definition_id: str,
    stage_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a Case Stage Definition (`PATCH /v1alpha/{parent}/caseStageDefinitions/{case_stage_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(stage_definition_id, "caseStageDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseStageDefinitions/{short_id}"
        params = {"updateMask": update_mask} if update_mask else {}
        response = chronicle.session.patch(url, params=params, json=stage_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update case stage definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating case stage definition: %s", e)
        return {"error": f"Failed to update case stage definition: {str(e)}"}


@server.tool()
async def delete_case_stage_definition(
    stage_definition_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a Case Stage Definition (`DELETE /v1alpha/{parent}/caseStageDefinitions/{case_stage_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(stage_definition_id, "caseStageDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseStageDefinitions/{short_id}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete case stage definition: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "stage_definition_id": short_id}
    except Exception as e:
        logger.error("Error deleting case stage definition: %s", e)
        return {"error": f"Failed to delete case stage definition: {str(e)}"}


@server.tool()
async def list_case_tag_definitions(
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List Case Tag Definitions (`GET /v1alpha/{parent}/caseTagDefinitions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseTagDefinitions"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case tag definitions: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case tag definitions: %s", e)
        return {"error": f"Failed to list case tag definitions: {str(e)}"}


@server.tool()
async def get_case_tag_definition(
    tag_definition_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a Case Tag Definition (`GET /v1alpha/{parent}/caseTagDefinitions/{case_tag_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(tag_definition_id, "caseTagDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseTagDefinitions/{short_id}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case tag definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case tag definition: %s", e)
        return {"error": f"Failed to get case tag definition: {str(e)}"}


@server.tool()
async def create_case_tag_definition(
    tag_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a Case Tag Definition (`POST /v1alpha/{parent}/caseTagDefinitions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseTagDefinitions"
        response = chronicle.session.post(url, json=tag_payload)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create case tag definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating case tag definition: %s", e)
        return {"error": f"Failed to create case tag definition: {str(e)}"}


@server.tool()
async def update_case_tag_definition(
    tag_definition_id: str,
    tag_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a Case Tag Definition (`PATCH /v1alpha/{parent}/caseTagDefinitions/{case_tag_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(tag_definition_id, "caseTagDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseTagDefinitions/{short_id}"
        params = {"updateMask": update_mask} if update_mask else {}
        response = chronicle.session.patch(url, params=params, json=tag_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update case tag definition: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating case tag definition: %s", e)
        return {"error": f"Failed to update case tag definition: {str(e)}"}


@server.tool()
async def delete_case_tag_definition(
    tag_definition_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a Case Tag Definition (`DELETE /v1alpha/{parent}/caseTagDefinitions/{case_tag_definition}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(tag_definition_id, "caseTagDefinitions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseTagDefinitions/{short_id}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete case tag definition: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "tag_definition_id": short_id}
    except Exception as e:
        logger.error("Error deleting case tag definition: %s", e)
        return {"error": f"Failed to delete case tag definition: {str(e)}"}


@server.tool()
async def batch_delete_case_tag_definitions(
    names: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Batch delete Case Tag Definitions (`POST /v1alpha/{parent}/caseTagDefinitions:batchDelete`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseTagDefinitions:batchDelete"
        response = chronicle.session.post(url, json={"names": names})
        if response.status_code not in (200, 204):
            return {"error": f"Failed to batch delete case tag definitions: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "count": len(names)}
    except Exception as e:
        logger.error("Error batch deleting case tag definitions: %s", e)
        return {"error": f"Failed to batch delete case tag definitions: {str(e)}"}


@server.tool()
async def list_case_queue_filters(
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List saved Case Queue Filters (`GET /v1alpha/{parent}/caseQueueFilters`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseQueueFilters"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case queue filters: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case queue filters: %s", e)
        return {"error": f"Failed to list case queue filters: {str(e)}"}


@server.tool()
async def get_case_queue_filter(
    queue_filter_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a saved Case Queue Filter (`GET /v1alpha/{parent}/caseQueueFilters/{case_queue_filter}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(queue_filter_id, "caseQueueFilters")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseQueueFilters/{short_id}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case queue filter: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case queue filter: %s", e)
        return {"error": f"Failed to get case queue filter: {str(e)}"}


@server.tool()
async def create_case_queue_filter(
    filter_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a saved Case Queue Filter (`POST /v1alpha/{parent}/caseQueueFilters`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseQueueFilters"
        response = chronicle.session.post(url, json=filter_payload)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create case queue filter: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating case queue filter: %s", e)
        return {"error": f"Failed to create case queue filter: {str(e)}"}


@server.tool()
async def update_case_queue_filter(
    queue_filter_id: str,
    filter_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a saved Case Queue Filter (`PATCH /v1alpha/{parent}/caseQueueFilters/{case_queue_filter}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(queue_filter_id, "caseQueueFilters")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseQueueFilters/{short_id}"
        params = {"updateMask": update_mask} if update_mask else {}
        response = chronicle.session.patch(url, params=params, json=filter_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update case queue filter: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating case queue filter: %s", e)
        return {"error": f"Failed to update case queue filter: {str(e)}"}


@server.tool()
async def delete_case_queue_filter(
    queue_filter_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a saved Case Queue Filter (`DELETE /v1alpha/{parent}/caseQueueFilters/{case_queue_filter}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _extract_id(queue_filter_id, "caseQueueFilters")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/caseQueueFilters/{short_id}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete case queue filter: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "queue_filter_id": short_id}
    except Exception as e:
        logger.error("Error deleting case queue filter: %s", e)
        return {"error": f"Failed to delete case queue filter: {str(e)}"}
