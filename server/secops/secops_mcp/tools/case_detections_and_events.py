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
"""Security Operations MCP tools for Case Detections, Case Events, and Case Evidence Data."""

import logging
from typing import Any, Dict, Optional

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
async def list_case_detections(
    case_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    filter: Optional[str] = None,
    order_by: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List SIEM detections linked to a Case (`GET /v1alpha/{parent}/cases/{case}/caseDetections`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseDetections"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter:
            params["filter"] = filter
        if order_by:
            params["orderBy"] = order_by
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case detections: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case detections: %s", e)
        return {"error": f"Failed to list case detections: {str(e)}"}


@server.tool()
async def get_case_detection(
    case_id: str,
    detection_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get details of a specific SIEM detection in a Case (`GET /v1alpha/{parent}/cases/{case}/caseDetections/{case_detection}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_det = _extract_id(detection_id, "caseDetections")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseDetections/{short_det}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case detection: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case detection: %s", e)
        return {"error": f"Failed to get case detection: {str(e)}"}


@server.tool()
async def list_case_detection_events(
    case_id: str,
    detection_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List underlying UDM events for a specific Case Detection (`GET /v1alpha/{parent}/cases/{case}/caseDetections/{case_detection}:listCaseDetectionEvents`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_det = _extract_id(detection_id, "caseDetections")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseDetections/{short_det}:listCaseDetectionEvents"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case detection events: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case detection events: %s", e)
        return {"error": f"Failed to list case detection events: {str(e)}"}


@server.tool()
async def list_case_events(
    case_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    filter: Optional[str] = None,
    order_by: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List case-level security events across all alerts in a Case (`GET /v1alpha/{parent}/cases/{case}/caseEvents`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseEvents"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter:
            params["filter"] = filter
        if order_by:
            params["orderBy"] = order_by
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case events: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case events: %s", e)
        return {"error": f"Failed to list case events: {str(e)}"}


@server.tool()
async def get_case_event(
    case_id: str,
    event_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a single case-level security event (`GET /v1alpha/{parent}/cases/{case}/caseEvents/{case_event}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_evt = _extract_id(event_id, "caseEvents")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseEvents/{short_evt}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case event: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case event: %s", e)
        return {"error": f"Failed to get case event: {str(e)}"}


@server.tool()
async def list_case_evidence_data(
    case_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    filter: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List evidentiary attachments, artifacts, and blobs on a Case (`GET /v1alpha/{parent}/cases/{case}/caseEvidenceData`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseEvidenceData"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter:
            params["filter"] = filter
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case evidence data: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case evidence data: %s", e)
        return {"error": f"Failed to list case evidence data: {str(e)}"}


@server.tool()
async def get_case_evidence_data(
    case_id: str,
    evidence_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a single Case Evidence Data resource (`GET /v1alpha/{parent}/cases/{case}/caseEvidenceData/{case_evidence_data}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_ev = _extract_id(evidence_id, "caseEvidenceData")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseEvidenceData/{short_ev}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case evidence data: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case evidence data: %s", e)
        return {"error": f"Failed to get case evidence data: {str(e)}"}
