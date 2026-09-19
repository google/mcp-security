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
"""Security Operations MCP tools for Case Wall Records (`CaseWallRecordService`)."""

import logging
from typing import Any, Dict, List, Optional

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
async def list_case_wall_records(
    case_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    filter: Optional[str] = None,
    order_by: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List unified activity timeline records on a Case Wall (`GET /v1alpha/{parent}/cases/{case}/caseWallRecords`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter:
            params["filter"] = filter
        if order_by:
            params["orderBy"] = order_by
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case wall records: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case wall records: %s", e)
        return {"error": f"Failed to list case wall records: {str(e)}"}


@server.tool()
async def get_case_wall_record(
    case_id: str,
    wall_record_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a single Case Wall Record (`GET /v1alpha/{parent}/cases/{case}/caseWallRecords/{case_wall_record}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rec = _extract_id(wall_record_id, "caseWallRecords")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords/{short_rec}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case wall record: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case wall record: %s", e)
        return {"error": f"Failed to get case wall record: {str(e)}"}


@server.tool()
async def set_favourite_wall_record(
    case_id: str,
    wall_record_id: str,
    is_favourite: bool,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Pin or unpin a Case Wall Record as a favorite (`POST /v1alpha/{parent}/cases/{case}/caseWallRecords/{case_wall_record}:setFavouriteWallRecord`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rec = _extract_id(wall_record_id, "caseWallRecords")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords/{short_rec}:setFavouriteWallRecord"
        response = chronicle.session.post(url, json={"isFavourite": is_favourite})
        if response.status_code != 200:
            return {"error": f"Failed to set favourite wall record: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error setting favourite wall record: %s", e)
        return {"error": f"Failed to set favourite wall record: {str(e)}"}


@server.tool()
async def add_case_wall_record_tags(
    case_id: str,
    wall_record_id: str,
    tags: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Add tags to a Case Wall Record (`POST /v1alpha/{parent}/cases/{case}/caseWallRecords/{case_wall_record}:addCaseWallRecordTags`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rec = _extract_id(wall_record_id, "caseWallRecords")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords/{short_rec}:addCaseWallRecordTags"
        response = chronicle.session.post(url, json={"tags": tags})
        if response.status_code != 200:
            return {"error": f"Failed to add wall record tags: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error adding wall record tags: %s", e)
        return {"error": f"Failed to add wall record tags: {str(e)}"}


@server.tool()
async def remove_case_wall_record_tags(
    case_id: str,
    wall_record_id: str,
    tags: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Remove tags from a Case Wall Record (`POST /v1alpha/{parent}/cases/{case}/caseWallRecords/{case_wall_record}:removeCaseWallRecordTags`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rec = _extract_id(wall_record_id, "caseWallRecords")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords/{short_rec}:removeCaseWallRecordTags"
        response = chronicle.session.post(url, json={"tags": tags})
        if response.status_code != 200:
            return {"error": f"Failed to remove wall record tags: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error removing wall record tags: %s", e)
        return {"error": f"Failed to remove wall record tags: {str(e)}"}


@server.tool()
async def fetch_case_activities_count(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch aggregated activity counts by record type for a Case Wall (`GET /v1alpha/{parent}/cases/{case}/caseWallRecords:fetchCaseActivitiesCount`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords:fetchCaseActivitiesCount"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to fetch case activities count: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error fetching case activities count: %s", e)
        return {"error": f"Failed to fetch case activities count: {str(e)}"}


@server.tool()
async def query_available_case_wall_record_tags(
    case_id: str,
    query: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Query available tags for Case Wall Records (`POST /v1alpha/{parent}/cases/{case}/caseWallRecords:queryAvailableCaseWallRecordTags`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseWallRecords:queryAvailableCaseWallRecordTags"
        body: Dict[str, Any] = {}
        if query:
            body["query"] = query
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {"error": f"Failed to query available wall record tags: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error querying available wall record tags: %s", e)
        return {"error": f"Failed to query available wall record tags: {str(e)}"}
