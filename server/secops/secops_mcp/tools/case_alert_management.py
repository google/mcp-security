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
"""Security Operations MCP tools for Chronicle 1P Case Alert Management."""

import logging
from typing import Any, Dict, List, Optional

from secops_mcp.server import get_chronicle_client, server

logger = logging.getLogger("secops-mcp")

def _v1alpha_base(chronicle: Any) -> str:
    base = getattr(chronicle, "base_v1alpha_url", None)
    if isinstance(base, str) and base:
        return base
    return str(chronicle.base_url)



def _format_case_alert_name(instance_id: str, case_id: str, alert_id: str) -> str:
    """Format full case alert resource name."""
    if alert_id.startswith("projects/"):
        return alert_id
    if case_id.startswith("projects/"):
        return f"{case_id}/caseAlerts/{alert_id}"
    return f"{instance_id}/cases/{case_id}/caseAlerts/{alert_id}"


def _get_base_endpoint(chronicle: Any, version: str = "v1") -> str:
    """Get the base REST endpoint for Chronicle 1P resources."""
    if version == "v1" and hasattr(chronicle, "base_v1_url") and chronicle.base_v1_url:
        return f"{chronicle.base_v1_url}/{chronicle.instance_id}"
    base_url = chronicle.base_url
    if version == "v1" and "/v1alpha" in base_url:
        base_url = base_url.replace("/v1alpha", "/v1")
    return f"{base_url}/{chronicle.instance_id}"


@server.tool()
async def list_case_alerts(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List CaseAlerts within a specific Case using the 1P CaseAlertService REST API.

    Retrieves all alerts associated with a given case, including their status,
    priority, detection rule details, and SLA information.

    **Workflow Integration:**
    - Examine all alerts grouped into a security incident case.
    - Filter for unresolved alerts or critical severity detections.

    Args:
        case_id (str): The ID or name of the case whose alerts to list.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        filter_query (Optional[str]): Filter expression (e.g. 'priority = "HIGH"').
        page_size (int): Number of alerts to return per page. Defaults to 50.
        page_token (Optional[str]): Token for retrieving the next page.

    Returns:
        Dict[str, Any]: List of CaseAlert objects and pagination token.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts"

        params: Dict[str, Any] = {"pageSize": page_size}
        if filter_query:
            params["filter"] = filter_query
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {
                "error": f"Failed to list case alerts: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing case alerts for case %s: %s", case_id, e)
        return {"error": f"Failed to list case alerts: {str(e)}"}


@server.tool()
async def get_case_alert(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get details of a specific CaseAlert using the 1P CaseAlertService REST API.

    Args:
        case_id (str): The Case ID or full resource name.
        alert_id (str): The Alert ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Detailed CaseAlert object.
    """
    try:
        if not case_id or not alert_id:
            return {"error": "Both case_id and alert_id parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/{short_alert_id}"

        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {
                "error": f"Failed to get case alert {alert_id}: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting case alert %s: %s", alert_id, e)
        return {"error": f"Failed to get case alert: {str(e)}"}


@server.tool()
async def update_case_alert(
    case_id: str,
    alert_id: str,
    update_mask: str,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    custom_field_values: Optional[List[Dict[str, Any]]] = None,
    closure_reason: Optional[str] = None,
    closure_comment: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a CaseAlert in Chronicle using the 1P CaseAlertService.UpdateCaseAlert REST API.

    Modifies alert properties such as priority, status, custom field values, or closure feedback.

    **Reaction Triggers Activated:**
    - Setting `priority` triggers **Alert Priority Changed**.
    - Setting `custom_field_values` triggers **Alert Custom Field Changed**.

    Args:
        case_id (str): Case ID or full resource name.
        alert_id (str): Alert ID or full resource name.
        update_mask (str): Comma-separated list of fields being updated
            (e.g., "priority", "status", "custom_field_values", "feedback_summary").
        priority (Optional[str]): Updated priority ("PRIORITY_LOW", "PRIORITY_MEDIUM",
            "PRIORITY_HIGH", "PRIORITY_CRITICAL", or short names "LOW", "MEDIUM", "HIGH", "CRITICAL").
        status (Optional[str]): Updated alert status (e.g., "OPEN", "CLOSED").
        custom_field_values (Optional[List[Dict[str, Any]]]): Custom fields to attach to the alert.
        closure_reason (Optional[str]): Closure justification if closing the alert.
        closure_comment (Optional[str]): Notes explaining the closure.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: The updated CaseAlert object.
    """
    try:
        if not case_id or not alert_id:
            return {"error": "Both case_id and alert_id parameters are required"}
        if not update_mask:
            return {"error": "update_mask parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        alert_name = _format_case_alert_name(chronicle.instance_id, short_case_id, short_alert_id)
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/{short_alert_id}"

        body: Dict[str, Any] = {"name": alert_name}
        if priority is not None:
            p_upper = priority.upper()
            if not p_upper.startswith("PRIORITY_") and p_upper in ["LOW", "MEDIUM", "HIGH", "CRITICAL", "INFO"]:
                p_upper = f"PRIORITY_{p_upper}"
            body["priority"] = p_upper
        if status is not None:
            body["status"] = status
        if custom_field_values is not None:
            body["customFieldValues"] = custom_field_values
        if closure_reason is not None or closure_comment is not None:
            body["feedbackSummary"] = {
                "closureReason": closure_reason,
                "comment": closure_comment,
            }

        params = {"updateMask": update_mask}
        response = chronicle.session.patch(url, params=params, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to update case alert: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error updating case alert %s: %s", alert_id, e)
        return {"error": f"Failed to update case alert: {str(e)}"}


@server.tool()
async def change_alert_priority(
    case_id: str,
    alert_id: str,
    priority: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Change the priority level of a CaseAlert using Chronicle 1P REST API.

    Triggers the **Alert Priority Changed** reaction trigger in SOAR playbooks.

    Args:
        case_id (str): The Case ID containing the alert.
        alert_id (str): The Alert ID to update.
        priority (str): New priority ("PRIORITY_LOW", "PRIORITY_MEDIUM",
            "PRIORITY_HIGH", "PRIORITY_CRITICAL", or short names "LOW", "MEDIUM", "HIGH", "CRITICAL").
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Updated CaseAlert object or status confirmation.
    """
    try:
        p_upper = priority.upper()
        if not p_upper.startswith("PRIORITY_") and p_upper in ["LOW", "MEDIUM", "HIGH", "CRITICAL", "INFO"]:
            p_upper = f"PRIORITY_{p_upper}"

        return await update_case_alert(
            case_id=case_id,
            alert_id=alert_id,
            update_mask="priority",
            priority=p_upper,
            project_id=project_id,
            customer_id=customer_id,
            region=region,
        )
    except Exception as e:
        logger.error("Error changing alert priority: %s", e)
        return {"error": f"Failed to change alert priority: {str(e)}"}


@server.tool()
async def set_alert_custom_fields(
    case_id: str,
    alert_id: str,
    custom_fields: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Set custom field values on a CaseAlert using Chronicle 1P REST API.

    Triggers the **Alert Custom Field Changed** reaction trigger in SOAR playbooks.

    Args:
        case_id (str): The Case ID containing the alert.
        alert_id (str): The Alert ID to update.
        custom_fields (Dict[str, Any]): Dictionary mapping custom field names to values.
            Example: {"MalwareFamily": "Emotet", "Confidence": "High"}
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Updated CaseAlert object.
    """
    try:
        if not custom_fields:
            return {"error": "custom_fields dictionary cannot be empty"}

        custom_field_values = [
            {"fieldName": k, "value": str(v) if not isinstance(v, (dict, list)) else str(v)}
            for k, v in custom_fields.items()
        ]

        return await update_case_alert(
            case_id=case_id,
            alert_id=alert_id,
            update_mask="custom_field_values",
            custom_field_values=custom_field_values,
            project_id=project_id,
            customer_id=customer_id,
            region=region,
        )
    except Exception as e:
        logger.error("Error setting alert custom fields: %s", e)
        return {"error": f"Failed to set alert custom fields: {str(e)}"}


@server.tool()
async def move_case_alert(
    source_case_id: str,
    alert_id: str,
    destination_case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Move a CaseAlert from one Case to another using Chronicle 1P REST API.

    Args:
        source_case_id (str): Case ID currently containing the alert.
        alert_id (str): Alert ID to move.
        destination_case_id (str): Destination Case ID or resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: MoveAlertResponse confirmation.
    """
    try:
        if not source_case_id or not alert_id or not destination_case_id:
            return {"error": "source_case_id, alert_id, and destination_case_id parameters are all required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_src_case_id = source_case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        short_dest_case_id = destination_case_id.split("/")[-1]

        url = f"{_get_base_endpoint(chronicle)}/cases/{short_src_case_id}/caseAlerts/{short_alert_id}:move"

        body = {"destinationCaseId": short_dest_case_id}
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to move alert: {response.status_code} - {response.text}"
            }
        return response.json() if response.text else {"status": "SUCCESS", "message": f"Moved alert {short_alert_id} to case {short_dest_case_id}"}
    except Exception as e:
        logger.error("Error moving case alert: %s", e)
        return {"error": f"Failed to move case alert: {str(e)}"}


@server.tool()
async def add_alert_tag(
    case_id: str,
    alert_id: str,
    tag: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Add a categorization tag to a CaseAlert using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID containing the alert.
        alert_id (str): Alert ID.
        tag (str): Tag string to add to the alert.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Response confirmation.
    """
    try:
        if not case_id or not alert_id or not tag:
            return {"error": "case_id, alert_id, and tag parameters are all required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/{short_alert_id}:addTag"

        response = chronicle.session.post(url, json={"tag": tag})
        if response.status_code != 200:
            return {
                "error": f"Failed to add tag to alert: {response.status_code} - {response.text}"
            }
        return response.json() if response.text else {"status": "SUCCESS", "message": f"Added tag '{tag}' to alert"}
    except Exception as e:
        logger.error("Error adding tag to alert: %s", e)
        return {"error": f"Failed to add tag to alert: {str(e)}"}


@server.tool()
async def remove_alert_tag(
    case_id: str,
    alert_id: str,
    tag: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Remove a categorization tag from a CaseAlert using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID containing the alert.
        alert_id (str): Alert ID.
        tag (str): Tag string to remove.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Response confirmation.
    """
    try:
        if not case_id or not alert_id or not tag:
            return {"error": "case_id, alert_id, and tag parameters are all required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/{short_alert_id}:removeTag"

        response = chronicle.session.post(url, json={"tag": tag})
        if response.status_code != 200:
            return {
                "error": f"Failed to remove tag from alert: {response.status_code} - {response.text}"
            }
        return response.json() if response.text else {"status": "SUCCESS", "message": f"Removed tag '{tag}' from alert"}
    except Exception as e:
        logger.error("Error removing tag from alert: %s", e)
        return {"error": f"Failed to remove tag from alert: {str(e)}"}


@server.tool()
async def list_alert_group_identifiers_by_case(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List alert group identifiers associated with a specific Case in Chronicle SOAR.

    Retrieves grouping keys used for correlation, playbook execution stages, or analyst assignment.

    Args:
        case_id (str): The Case ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        page_size (int): Max number of results. Defaults to 50.
        page_token (Optional[str]): Pagination token.

    Returns:
        Dict[str, Any]: List of alert group identifier strings and pagination info.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}:listAlertGroupIdentifiers"

        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            # Fallback to extracting from list_case_alerts if dedicated endpoint is not active
            alerts_res = await list_case_alerts(case_id=short_case_id, project_id=project_id, customer_id=customer_id, region=region)
            if "caseAlerts" in alerts_res:
                group_ids = list({
                    gid for a in alerts_res["caseAlerts"]
                    for gid in a.get("alertGroupIdentifiers", [])
                })
                return {"alertGroupIdentifiers": group_ids, "caseId": short_case_id}
            return {
                "error": f"Failed to list alert group identifiers: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing alert group identifiers for case %s: %s", case_id, e)
        return {"error": f"Failed to list alert group identifiers: {str(e)}"}


@server.tool()
async def list_events_by_alert(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List the underlying security events (UDM events) associated with a specific alert.

    Retrieves the raw ground truth telemetry events that triggered the alert,
    vital for verifying alerts, inspecting command lines, network connections, and forensic analysis.

    Args:
        case_id (str): The Case ID containing the alert.
        alert_id (str): The Alert ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        page_size (int): Max number of events to return. Defaults to 50.
        page_token (Optional[str]): Pagination token.

    Returns:
        Dict[str, Any]: List of raw/UDM event objects linked to the alert.
    """
    try:
        if not case_id or not alert_id:
            return {"error": "Both case_id and alert_id parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case_id = case_id.split("/")[-1]
        short_alert_id = alert_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_case_id}/caseAlerts/{short_alert_id}:listEvents"

        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token

        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            # Fallback to get_case_alert with expand=events
            alert_detail = await get_case_alert(case_id=short_case_id, alert_id=short_alert_id, project_id=project_id, customer_id=customer_id, region=region)
            if "events" in alert_detail:
                return {"events": alert_detail["events"], "alertId": short_alert_id}
            return {
                "error": f"Failed to list events for alert: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing events for alert %s: %s", alert_id, e)
        return {"error": f"Failed to list events for alert: {str(e)}"}


@server.tool()
async def list_involved_events(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Alias for list_events_by_alert. Retrieves security telemetry events for a case alert."""
    return await list_events_by_alert(
        case_id=case_id,
        alert_id=alert_id,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
        page_size=page_size,
        page_token=page_token,
    )


def _extract_case_id(case_id: str) -> str:
    if "/cases/" in case_id:
        return case_id.split("/cases/")[-1].split("/")[0]
    return str(case_id)


def _extract_alert_id(alert_id: str) -> str:
    if "/caseAlerts/" in alert_id:
        return alert_id.split("/caseAlerts/")[-1].split("/")[0]
    return str(alert_id)


@server.tool()
async def set_alert_sla(
    case_id: str,
    alert_id: str,
    sla_expiration_time: str,
    sla_critical_expiration_time: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Set the SLA expiration times on a Case Alert (`POST /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:setAlertSla`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:setAlertSla"
        body: Dict[str, Any] = {"slaExpirationTime": sla_expiration_time}
        if sla_critical_expiration_time:
            body["slaCriticalExpirationTime"] = sla_critical_expiration_time
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {"error": f"Failed to set alert SLA: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error setting alert SLA: %s", e)
        return {"error": f"Failed to set alert SLA: {str(e)}"}


@server.tool()
async def pause_alert_sla(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Pause the SLA countdown timer on a Case Alert (`POST /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:pauseAlertSla`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:pauseAlertSla"
        response = chronicle.session.post(url, json={})
        if response.status_code != 200:
            return {"error": f"Failed to pause alert SLA: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error pausing alert SLA: %s", e)
        return {"error": f"Failed to pause alert SLA: {str(e)}"}


@server.tool()
async def resume_alert_sla(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Resume a paused SLA countdown timer on a Case Alert (`POST /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:resumeAlertSla`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:resumeAlertSla"
        response = chronicle.session.post(url, json={})
        if response.status_code != 200:
            return {"error": f"Failed to resume alert SLA: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error resuming alert SLA: %s", e)
        return {"error": f"Failed to resume alert SLA: {str(e)}"}


@server.tool()
async def get_alert_overview(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the dynamic UI overview layout and resolved data for a Case Alert (`GET /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:getAlertOverview`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:getAlertOverview"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get alert overview: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting alert overview: %s", e)
        return {"error": f"Failed to get alert overview: {str(e)}"}


@server.tool()
async def resolve_alert_overview_widget(
    case_id: str,
    alert_id: str,
    widget_definition: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve data for a dynamic widget on the Case Alert overview tab (`POST /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:resolveAlertOverviewWidget`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:resolveAlertOverviewWidget"
        response = chronicle.session.post(url, json={"widgetDefinition": widget_definition})
        if response.status_code != 200:
            return {"error": f"Failed to resolve alert overview widget: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error resolving alert overview widget: %s", e)
        return {"error": f"Failed to resolve alert overview widget: {str(e)}"}


@server.tool()
async def fetch_alert_recommendation(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch AI/ML triage recommendations and similar alerts for a Case Alert (`GET /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:fetchAlertRecommendation`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:fetchAlertRecommendation"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to fetch alert recommendation: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error fetching alert recommendation: %s", e)
        return {"error": f"Failed to fetch alert recommendation: {str(e)}"}


@server.tool()
async def create_alert_recommendation_long_running(
    case_id: str,
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Trigger an async LRO to generate AI/ML triage recommendations for a Case Alert (`POST /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}:createAlertRecommendationLongRunning`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}:createAlertRecommendationLongRunning"
        response = chronicle.session.post(url, json={})
        if response.status_code != 200:
            return {"error": f"Failed to create alert recommendation LRO: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error creating alert recommendation LRO: %s", e)
        return {"error": f"Failed to create alert recommendation LRO: {str(e)}"}


@server.tool()
async def list_alert_views(
    case_id: str,
    alert_id: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List customizable alert view configurations for a Case Alert (`GET /v1alpha/{parent}/cases/{case}/caseAlerts/{case_alert}/alertViews`)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_case = _extract_case_id(case_id)
        short_alert = _extract_alert_id(alert_id)
        url = f"{_v1alpha_base(chronicle)}/{chronicle.instance_id}/cases/{short_case}/caseAlerts/{short_alert}/alertViews"
        params: Dict[str, Any] = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to list alert views: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error listing alert views: %s", e)
        return {"error": f"Failed to list alert views: {str(e)}"}


