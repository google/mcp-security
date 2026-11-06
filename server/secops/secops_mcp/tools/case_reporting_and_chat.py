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
"""Security Operations MCP tools for Agentic Case Reporting and Case Chat Messages."""

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
async def create_agentic_case_report(
    case_id: str,
    report_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create/generate an AI-authored Agentic Case Report (`POST /v1alpha/{parent}/cases/{case}/agenticCaseReports:generate`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports:generate"
        response = chronicle.session.post(url, json=report_payload)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create agentic case report: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating agentic case report: %s", e)
        return {"error": f"Failed to create agentic case report: {str(e)}"}


@server.tool()
async def update_agentic_case_report(
    case_id: str,
    report_id: str,
    report_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an Agentic Case Report (`PATCH /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}"
        params = {"updateMask": update_mask} if update_mask else {}
        response = chronicle.session.patch(url, params=params, json=report_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update agentic case report: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating agentic case report: %s", e)
        return {"error": f"Failed to update agentic case report: {str(e)}"}


@server.tool()
async def delete_agentic_case_report(
    case_id: str,
    report_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete an Agentic Case Report (`DELETE /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete agentic case report: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "report_id": short_rep}
    except Exception as e:
        logger.error("Error deleting agentic case report: %s", e)
        return {"error": f"Failed to delete agentic case report: {str(e)}"}


@server.tool()
async def get_agentic_case_report(
    case_id: str,
    report_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get an Agentic Case Report (`GET /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get agentic case report: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting agentic case report: %s", e)
        return {"error": f"Failed to get agentic case report: {str(e)}"}


@server.tool()
async def list_agentic_case_reports(
    case_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List Agentic Case Reports on a Case (`GET /v1alpha/{parent}/cases/{case}/agenticCaseReports`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list agentic case reports: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing agentic case reports: %s", e)
        return {"error": f"Failed to list agentic case reports: {str(e)}"}


@server.tool()
async def update_agentic_case_report_template(
    template_id: str,
    template_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an Agentic Case Report Template (`PATCH /v1alpha/{parent}/agenticCaseReportTemplates/{template}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_tpl = _extract_id(template_id, "agenticCaseReportTemplates")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/agenticCaseReportTemplates/{short_tpl}"
        params = {"updateMask": update_mask} if update_mask else {}
        response = chronicle.session.patch(url, params=params, json=template_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update agentic report template: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating agentic report template: %s", e)
        return {"error": f"Failed to update agentic report template: {str(e)}"}


@server.tool()
async def get_agentic_case_report_template(
    template_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get an Agentic Case Report Template (`GET /v1alpha/{parent}/agenticCaseReportTemplates/{template}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_tpl = _extract_id(template_id, "agenticCaseReportTemplates")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/agenticCaseReportTemplates/{short_tpl}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get agentic report template: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting agentic report template: %s", e)
        return {"error": f"Failed to get agentic report template: {str(e)}"}


@server.tool()
async def list_agentic_case_report_templates(
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List Agentic Case Report Templates (`GET /v1alpha/{parent}/agenticCaseReportTemplates`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/agenticCaseReportTemplates"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list agentic report templates: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing agentic report templates: %s", e)
        return {"error": f"Failed to list agentic report templates: {str(e)}"}


@server.tool()
async def create_agentic_case_report_version(
    case_id: str,
    report_id: str,
    version_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a version snapshot of an Agentic Case Report (`POST /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}/versions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}/versions"
        response = chronicle.session.post(url, json=version_payload)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create report version: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating report version: %s", e)
        return {"error": f"Failed to create report version: {str(e)}"}


@server.tool()
async def get_agentic_case_report_version(
    case_id: str,
    report_id: str,
    version_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a specific Agentic Case Report Version (`GET /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}/versions/{version}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        short_ver = _extract_id(version_id, "versions")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}/versions/{short_ver}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get report version: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting report version: %s", e)
        return {"error": f"Failed to get report version: {str(e)}"}


@server.tool()
async def list_agentic_case_report_versions(
    case_id: str,
    report_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List versions of an Agentic Case Report (`GET /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}/versions`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}/versions"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list report versions: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing report versions: %s", e)
        return {"error": f"Failed to list report versions: {str(e)}"}


@server.tool()
async def export_agentic_case_report(
    case_id: str,
    report_id: str,
    export_format: str = "PDF",
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Download/export an Agentic Case Report (`GET /v1alpha/{parent}/cases/{case}/agenticCaseReports/{report}:download`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_rep = _extract_id(report_id, "agenticCaseReports")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/agenticCaseReports/{short_rep}:download"
        response = chronicle.session.get(url, params={"format": export_format})
        if response.status_code != 200:
            return {"error": f"Failed to export agentic case report: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error exporting agentic case report: %s", e)
        return {"error": f"Failed to export agentic case report: {str(e)}"}


@server.tool()
async def create_case_chat_message(
    case_id: str,
    message_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a Case Chat Message (`POST /v1alpha/{parent}/cases/{case}/chatMessages`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages"
        response = chronicle.session.post(url, json=message_payload)
        if response.status_code not in (200, 201):
            return {"error": f"Failed to create case chat message: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating case chat message: %s", e)
        return {"error": f"Failed to create case chat message: {str(e)}"}


@server.tool()
async def get_case_chat_message(
    case_id: str,
    chat_message_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a Case Chat Message (`GET /v1alpha/{parent}/cases/{case}/chatMessages/{chat_message}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_msg = _extract_id(chat_message_id, "chatMessages")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages/{short_msg}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case chat message: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case chat message: %s", e)
        return {"error": f"Failed to get case chat message: {str(e)}"}


@server.tool()
async def list_case_chat_messages(
    case_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List Case Chat Messages (`GET /v1alpha/{parent}/cases/{case}/chatMessages`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list case chat messages: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing case chat messages: %s", e)
        return {"error": f"Failed to list case chat messages: {str(e)}"}


@server.tool()
async def update_case_chat_message(
    case_id: str,
    chat_message_id: str,
    message_payload: Dict[str, Any],
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update or pin/unpin a Case Chat Message (`POST /v1alpha/{parent}/cases/{case}/chatMessages/{chat_message}:pinMessage`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_msg = _extract_id(chat_message_id, "chatMessages")
        if message_payload.get("pinned") is True:
            url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages/{short_msg}:pinMessage"
            response = chronicle.session.post(url, json={})
        elif message_payload.get("pinned") is False:
            url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages/{short_msg}:unpinMessage"
            response = chronicle.session.post(url, json={})
        else:
            url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages/{short_msg}"
            params = {"updateMask": update_mask} if update_mask else {}
            response = chronicle.session.patch(url, params=params, json=message_payload)
        if response.status_code != 200:
            return {"error": f"Failed to update case chat message: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating case chat message: %s", e)
        return {"error": f"Failed to update case chat message: {str(e)}"}


@server.tool()
async def delete_case_chat_message(
    case_id: str,
    chat_message_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a Case Chat Message (`DELETE /v1alpha/{parent}/cases/{case}/chatMessages/{chat_message}`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        short_msg = _extract_id(chat_message_id, "chatMessages")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages/{short_msg}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete case chat message: {response.status_code} - {response.text}"}
        return {"status": "DELETED", "chat_message_id": short_msg}
    except Exception as e:
        logger.error("Error deleting case chat message: %s", e)
        return {"error": f"Failed to delete case chat message: {str(e)}"}


@server.tool()
async def batch_create_case_chat_messages(
    case_id: str,
    requests: List[Dict[str, Any]],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a Case Chat Message with Attachment (`POST /v1alpha/{parent}/cases/{case}/chatMessages:createWithAttachment`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages:createWithAttachment"
        response = chronicle.session.post(url, json={"requests": requests})
        if response.status_code != 200:
            return {"error": f"Failed to batch create case chat messages: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error batch creating case chat messages: %s", e)
        return {"error": f"Failed to batch create case chat messages: {str(e)}"}


@server.tool()
async def batch_update_case_chat_messages(
    case_id: str,
    requests: List[Dict[str, Any]],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get unread Case Chat Messages count (`GET /v1alpha/{parent}/cases/{case}/chatMessages:unreadMessagesCount`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages:unreadMessagesCount"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get unread case chat messages count: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting unread case chat messages count: %s", e)
        return {"error": f"Failed to get unread case chat messages count: {str(e)}"}


@server.tool()
async def batch_delete_case_chat_messages(
    case_id: str,
    names: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Download Case Chat Message Attachment (`GET /v1alpha/{parent}/cases/{case}/chatMessages/{chat_message}/attachments/{attachment}:download`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_id(case_id, "cases")
        target = names[0] if names else ""
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/chatMessages/{target}:download"
        response = chronicle.session.get(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to download case chat attachment: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error downloading case chat attachment: %s", e)
        return {"error": f"Failed to download case chat attachment: {str(e)}"}
