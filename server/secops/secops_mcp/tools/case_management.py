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
"""Security Operations MCP tools for Chronicle 1P Case Management."""

import logging
from typing import Any, Dict, List, Optional, Union

from secops.chronicle.client import APIVersion
from secops.chronicle.utils.request_utils import chronicle_request
from secops_mcp.server import get_chronicle_client, server

logger = logging.getLogger("secops-mcp")


def _format_case_name(instance_id: str, case_id: str) -> str:
    """Format full case resource name if only ID is provided."""
    if case_id.startswith("projects/"):
        return case_id
    return f"{instance_id}/cases/{case_id}"


def _get_base_endpoint(chronicle: Any, version: str = "v1") -> str:
    """Get the base REST endpoint for Chronicle 1P resources."""
    if version == "v1" and hasattr(chronicle, "base_v1_url") and chronicle.base_v1_url:
        return f"{chronicle.base_v1_url}/{chronicle.instance_id}"
    base_url = chronicle.base_url
    if version == "v1" and "/v1alpha" in base_url:
        base_url = base_url.replace("/v1alpha", "/v1")
    return f"{base_url}/{chronicle.instance_id}"


@server.tool()
async def list_cases(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List Cases in Chronicle using the 1P CaseService REST API.

    Retrieves a paginated list of cases from the Chronicle instance. Supports
    filtering by priority, stage, status, assignee, and tags.

    **Workflow Integration:**
    - Discover open or assigned cases requiring investigation.
    - Monitor case queue health and workload distribution across SOC analysts.
    - Query cases matching specific detection rules or severity levels.

    **Use Cases:**
    - "List all open cases assigned to me"
    - "Show high priority cases in the Triage stage"
    - "Retrieve recent cases created in the last 24 hours"

    Args:
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
        filter_query (Optional[str]): Filter expression (e.g.,
            'priority = "HIGH" AND status = "OPEN"').
        order_by (Optional[str]): Sort order for results (e.g., "create_time desc").
        page_size (int): Number of cases to return per page (max 100). Defaults to 50.
        page_token (Optional[str]): Pagination token for retrieving next page.

    Returns:
        Dict[str, Any]: Dictionary containing list of cases and nextPageToken.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases"

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
                "error": f"Failed to list cases: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing cases: %s", e)
        return {"error": f"Failed to list cases: {str(e)}"}


@server.tool()
async def get_case(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get full details of a specific Case using the 1P CaseService REST API.

    Retrieves comprehensive metadata for a single case, including its priority,
    stage, assignee, display name, tags, SLA status, and custom fields.

    **Workflow Integration:**
    - Inspect case state before executing triage or remediation actions.
    - Verify updated priorities, stages, or custom field values.

    Args:
        case_id (str): Case ID (e.g., "case_12345") or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Case object with detailed properties.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        url = f"{_get_base_endpoint(chronicle)}/cases/{case_name.split('/')[-1]}"

        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {
                "error": f"Failed to get case {case_id}: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error getting case %s: %s", case_id, e)
        return {"error": f"Failed to get case: {str(e)}"}


@server.tool()
async def update_case(
    case_id: str,
    update_mask: str,
    display_name: Optional[str] = None,
    priority: Optional[str] = None,
    stage: Optional[str] = None,
    assignee: Optional[str] = None,
    custom_field_values: Optional[List[Dict[str, Any]]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a Case in Chronicle using the 1P CaseService.UpdateCase REST API.

    Updates selected fields on a case, such as priority, stage, assignee,
    display name, or custom fields.

    **Reaction Triggers Activated:**
    - Setting `priority` triggers **Case Priority Changed**.
    - Setting `stage` triggers **Case Stage Changed**.
    - Setting `assignee` triggers **Case Assignee Changed**.
    - Setting `custom_field_values` triggers **Custom Case Field Changed**.

    Args:
        case_id (str): Case ID or full resource name.
        update_mask (str): Comma-separated list of fields being updated
            (e.g., "priority,stage", "assignee", "custom_field_values").
        display_name (Optional[str]): Updated case title.
        priority (Optional[str]): Updated priority level (e.g., "PRIORITY_LOW",
            "PRIORITY_MEDIUM", "PRIORITY_HIGH", "PRIORITY_CRITICAL", "LOW", "HIGH").
        stage (Optional[str]): Target stage (e.g., "Triage", "Containment", "Remediation").
        assignee (Optional[str]): Analyst email or username.
        custom_field_values (Optional[List[Dict[str, Any]]]): List of custom field
            objects with `fieldName` and `value`.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: The updated Case object.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}
        if not update_mask:
            return {"error": "update_mask parameter is required (e.g., 'priority', 'stage')"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}"

        body: Dict[str, Any] = {"name": case_name}
        if display_name is not None:
            body["displayName"] = display_name
        if priority is not None:
            # Normalize priority if needed
            p_upper = priority.upper()
            if not p_upper.startswith("PRIORITY_") and p_upper in ["LOW", "MEDIUM", "HIGH", "CRITICAL", "INFO"]:
                p_upper = f"PRIORITY_{p_upper}"
            body["priority"] = p_upper
        if stage is not None:
            body["stage"] = stage
        if assignee is not None:
            body["assignee"] = assignee
        if custom_field_values is not None:
            body["customFieldValues"] = custom_field_values

        params = {"updateMask": update_mask}
        response = chronicle.session.patch(url, params=params, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to update case {case_id}: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error updating case %s: %s", case_id, e)
        return {"error": f"Failed to update case: {str(e)}"}


@server.tool()
async def change_case_priority(
    case_ids: Union[str, List[str]],
    priority: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Change the priority level for one or more cases using Chronicle 1P REST API.

    Triggers the **Case Priority Changed** reaction trigger in SOAR playbooks.

    Args:
        case_ids (Union[str, List[str]]): Single case ID or list of case IDs.
        priority (str): New priority level ("PRIORITY_LOW", "PRIORITY_MEDIUM",
            "PRIORITY_HIGH", "PRIORITY_CRITICAL", or short names "LOW", "MEDIUM", "HIGH", "CRITICAL").
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Success status or execution confirmation.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        ids = [case_ids] if isinstance(case_ids, str) else case_ids
        if not ids:
            return {"error": "case_ids cannot be empty"}

        p_upper = priority.upper()
        if not p_upper.startswith("PRIORITY_") and p_upper in ["LOW", "MEDIUM", "HIGH", "CRITICAL", "INFO"]:
            p_upper = f"PRIORITY_{p_upper}"

        full_names = [_format_case_name(chronicle.instance_id, cid) for cid in ids]
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkChangePriority"

        body = {"names": full_names, "priority": p_upper}
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to change case priority: {response.status_code} - {response.text}"
            }
        return {"status": "SUCCESS", "message": f"Updated priority to {p_upper} for {len(full_names)} case(s)"}
    except Exception as e:
        logger.error("Error changing case priority: %s", e)
        return {"error": f"Failed to change case priority: {str(e)}"}


@server.tool()
async def change_case_stage(
    case_ids: Union[str, List[str]],
    stage: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Change the investigation stage for one or more cases using Chronicle 1P REST API.

    Triggers the **Case Stage Changed** reaction trigger in SOAR playbooks.

    Args:
        case_ids (Union[str, List[str]]): Single case ID or list of case IDs.
        stage (str): Target investigation lifecycle stage (e.g. "Triage", "Containment", "Remediation", "Closure").
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Success status or execution confirmation.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        ids = [case_ids] if isinstance(case_ids, str) else case_ids
        if not ids:
            return {"error": "case_ids cannot be empty"}
        if not stage:
            return {"error": "stage parameter is required"}

        full_names = [_format_case_name(chronicle.instance_id, cid) for cid in ids]
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkChangeStage"

        body = {"names": full_names, "stage": stage}
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to change case stage: {response.status_code} - {response.text}"
            }
        return {"status": "SUCCESS", "message": f"Updated stage to '{stage}' for {len(full_names)} case(s)"}
    except Exception as e:
        logger.error("Error changing case stage: %s", e)
        return {"error": f"Failed to change case stage: {str(e)}"}


@server.tool()
async def assign_case(
    case_ids: Union[str, List[str]],
    assignee: Optional[str] = None,
    soc_role: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Assign one or more cases to a user or SOC role using Chronicle 1P REST API.

    Triggers the **Case Assignee Changed** reaction trigger in SOAR playbooks.

    Args:
        case_ids (Union[str, List[str]]): Single case ID or list of case IDs.
        assignee (Optional[str]): User email or username to assign the case(s) to.
        soc_role (Optional[str]): SOC role identifier to assign the case(s) to.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Success status or execution confirmation.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        ids = [case_ids] if isinstance(case_ids, str) else case_ids
        if not ids:
            return {"error": "case_ids cannot be empty"}
        if not assignee and not soc_role:
            return {"error": "Either assignee or soc_role must be provided"}

        full_names = [_format_case_name(chronicle.instance_id, cid) for cid in ids]
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkAssign"

        body: Dict[str, Any] = {"names": full_names}
        if assignee:
            body["assignee"] = assignee
        if soc_role:
            body["socRole"] = soc_role

        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to assign case(s): {response.status_code} - {response.text}"
            }
        assigned_target = assignee or soc_role
        return {"status": "SUCCESS", "message": f"Assigned {len(full_names)} case(s) to {assigned_target}"}
    except Exception as e:
        logger.error("Error assigning case: %s", e)
        return {"error": f"Failed to assign case: {str(e)}"}


@server.tool()
async def set_custom_case_fields(
    case_id: str,
    custom_fields: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Set custom field values on a Case using Chronicle 1P REST API.

    Triggers the **Custom Case Field Changed** reaction trigger in SOAR playbooks.

    Args:
        case_id (str): Case ID or full resource name.
        custom_fields (Dict[str, Any]): Dictionary mapping custom field names to values.
            Example: {"ImpactLevel": "High", "Department": "Finance"}
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Updated Case object.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}
        if not custom_fields:
            return {"error": "custom_fields dictionary cannot be empty"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}"

        custom_field_values = [
            {"fieldName": k, "value": str(v) if not isinstance(v, (dict, list)) else str(v)}
            for k, v in custom_fields.items()
        ]

        body = {
            "name": case_name,
            "customFieldValues": custom_field_values,
        }
        params = {"updateMask": "custom_field_values"}
        response = chronicle.session.patch(url, params=params, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to set custom case fields: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error setting custom case fields: %s", e)
        return {"error": f"Failed to set custom case fields: {str(e)}"}


@server.tool()
async def add_case_tag(
    case_id: str,
    tag: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Add a categorization tag to a Case using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID or full resource name.
        tag (str): Tag string to add to the case.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Response confirmation.
    """
    try:
        if not case_id or not tag:
            return {"error": "Both case_id and tag parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:addTag"

        response = chronicle.session.post(url, json={"tag": tag})
        if response.status_code != 200:
            return {
                "error": f"Failed to add tag to case: {response.status_code} - {response.text}"
            }
        return response.json() if response.text else {"status": "SUCCESS", "message": f"Added tag '{tag}'"}
    except Exception as e:
        logger.error("Error adding tag to case: %s", e)
        return {"error": f"Failed to add tag: {str(e)}"}


@server.tool()
async def remove_case_tag(
    case_id: str,
    tag: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Remove a categorization tag from a Case using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID or full resource name.
        tag (str): Tag string to remove.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Response confirmation.
    """
    try:
        if not case_id or not tag:
            return {"error": "Both case_id and tag parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:removeTag"

        response = chronicle.session.post(url, json={"tag": tag})
        if response.status_code != 200:
            return {
                "error": f"Failed to remove tag from case: {response.status_code} - {response.text}"
            }
        return response.json() if response.text else {"status": "SUCCESS", "message": f"Removed tag '{tag}'"}
    except Exception as e:
        logger.error("Error removing tag from case: %s", e)
        return {"error": f"Failed to remove tag: {str(e)}"}


@server.tool()
async def add_case_insight(
    case_id: str,
    content: str,
    insight_type: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Add an analyst note or automation insight to a Case using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID or full resource name.
        content (str): Text content of the insight or observation.
        insight_type (Optional[str]): Type/classification of the insight.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Created insight details.
    """
    try:
        if not case_id or not content:
            return {"error": "Both case_id and content parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:createInsight"

        body: Dict[str, Any] = {"content": content}
        if insight_type:
            body["type"] = insight_type

        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to add insight to case: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error adding insight to case: %s", e)
        return {"error": f"Failed to add insight: {str(e)}"}


@server.tool()
async def pause_case_sla(
    case_id: str,
    reason: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Pause the SLA timer for a Case using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID or full resource name.
        reason (str): Justification for pausing the SLA.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Status confirmation.
    """
    try:
        if not case_id or not reason:
            return {"error": "Both case_id and reason parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:pauseSla"

        response = chronicle.session.post(url, json={"reason": reason})
        if response.status_code != 200:
            return {
                "error": f"Failed to pause SLA: {response.status_code} - {response.text}"
            }
        return {"status": "SUCCESS", "message": f"Paused SLA on case {case_id}"}
    except Exception as e:
        logger.error("Error pausing SLA on case: %s", e)
        return {"error": f"Failed to pause SLA: {str(e)}"}


@server.tool()
async def resume_case_sla(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Resume a paused SLA timer for a Case using Chronicle 1P REST API.

    Args:
        case_id (str): Case ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Status confirmation.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:resumeSla"

        response = chronicle.session.post(url, json={})
        if response.status_code != 200:
            return {
                "error": f"Failed to resume SLA: {response.status_code} - {response.text}"
            }
        return {"status": "SUCCESS", "message": f"Resumed SLA on case {case_id}"}
    except Exception as e:
        logger.error("Error resuming SLA on case: %s", e)
        return {"error": f"Failed to resume SLA: {str(e)}"}


@server.tool()
async def close_case(
    case_ids: Union[str, List[str]],
    closure_reason: str,
    root_cause: Optional[str] = None,
    comment: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Close one or more cases with reason and root cause using Chronicle 1P REST API.

    Args:
        case_ids (Union[str, List[str]]): Single case ID or list of case IDs.
        closure_reason (str): Reason for closing the case (e.g. "False Positive", "Resolved", "Maintenance").
        root_cause (Optional[str]): Detailed root cause description.
        comment (Optional[str]): Closure commentary or summary note.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Status confirmation.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        ids = [case_ids] if isinstance(case_ids, str) else case_ids
        if not ids:
            return {"error": "case_ids cannot be empty"}
        if not closure_reason:
            return {"error": "closure_reason parameter is required"}

        full_names = [_format_case_name(chronicle.instance_id, cid) for cid in ids]
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkClose"

        body: Dict[str, Any] = {
            "names": full_names,
            "closureReason": closure_reason,
        }
        if root_cause:
            body["rootCause"] = root_cause
        if comment:
            body["comment"] = comment

        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to close case(s): {response.status_code} - {response.text}"
            }
        return {"status": "SUCCESS", "message": f"Closed {len(full_names)} case(s)"}
    except Exception as e:
        logger.error("Error closing case(s): %s", e)
        return {"error": f"Failed to close case: {str(e)}"}


@server.tool()
async def reopen_case(
    case_ids: Union[str, List[str]],
    comment: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Reopen one or more closed cases with an explanatory comment using Chronicle 1P REST API.

    Args:
        case_ids (Union[str, List[str]]): Single case ID or list of case IDs.
        comment (str): Reason explaining why the case is being reopened.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Status confirmation.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        ids = [case_ids] if isinstance(case_ids, str) else case_ids
        if not ids:
            return {"error": "case_ids cannot be empty"}
        if not comment:
            return {"error": "comment parameter is required explaining why the case is being reopened"}

        full_names = [_format_case_name(chronicle.instance_id, cid) for cid in ids]
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkReopen"

        body = {"names": full_names, "comment": comment}
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to reopen case(s): {response.status_code} - {response.text}"
            }
        return {"status": "SUCCESS", "message": f"Reopened {len(full_names)} case(s)"}
    except Exception as e:
        logger.error("Error reopening case(s): %s", e)
        return {"error": f"Failed to reopen case: {str(e)}"}


@server.tool()
async def list_case_comments(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    filter_query: Optional[str] = None,
    order_by: Optional[str] = None,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """List all case comments for a given Case in Chronicle using 1P CaseCommentService.

    Retrieves a paginated list of comments associated with a specific SOAR case,
    essential for understanding the timeline of investigation and reviewing analyst notes.

    Args:
        case_id (str): The Case ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.
        filter_query (Optional[str]): Filter expression (e.g., 'user = "analyst@example.com"').
        order_by (Optional[str]): Sort order (e.g., "create_time desc").
        page_size (int): Max number of comments to return. Defaults to 50.
        page_token (Optional[str]): Pagination token for next page.

    Returns:
        Dict[str, Any]: List of CaseComment objects and pagination token.
    """
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}/caseComments"

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
                "error": f"Failed to list case comments: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error listing comments for case %s: %s", case_id, e)
        return {"error": f"Failed to list case comments: {str(e)}"}


@server.tool()
async def create_case_comment(
    case_id: str,
    comment: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new comment on a Case in Chronicle using 1P CaseCommentService.

    Adds a new structured comment to an existing SOAR case for documenting findings,
    decisions, and analyst notes.

    Args:
        case_id (str): The Case ID or full resource name.
        comment (str): The text content of the comment.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: The created CaseComment object.
    """
    try:
        if not case_id or not comment:
            return {"error": "Both case_id and comment parameters are required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}/caseComments"

        body = {"comment": comment}
        response = chronicle.session.post(url, json=body)
        if response.status_code != 200:
            return {
                "error": f"Failed to create case comment: {response.status_code} - {response.text}"
            }
        return response.json()
    except Exception as e:
        logger.error("Error creating comment for case %s: %s", case_id, e)
        return {"error": f"Failed to create case comment: {str(e)}"}


@server.tool()
async def post_case_comment(
    case_id: str,
    comment: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Alias for create_case_comment. Posts a comment to a specific case within SOAR."""
    return await create_case_comment(
        case_id=case_id,
        comment=comment,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
    )


@server.tool()
async def get_case_full_details(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve consolidated, full details for a case by aggregating metadata, alerts, and comments.

    Fetches the core case object, associated security alerts, and comment timeline in parallel,
    providing a comprehensive 360-degree incident investigation overview in a single call.

    Args:
        case_id (str): The Case ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer/instance ID.
        region (Optional[str]): Chronicle region.

    Returns:
        Dict[str, Any]: Aggregated dictionary containing `case_details`, `case_alerts`,
            `case_comments`, and `alert_count`.
    """
    import asyncio
    try:
        if not case_id:
            return {"error": "case_id parameter is required"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        case_name = _format_case_name(chronicle.instance_id, case_id)
        short_id = case_name.split("/")[-1]
        base = _get_base_endpoint(chronicle)

        case_url = f"{base}/cases/{short_id}"
        alerts_url = f"{base}/cases/{short_id}/caseAlerts"
        comments_url = f"{base}/cases/{short_id}/caseComments"

        # Execute requests in parallel using thread executor / session calls
        loop = asyncio.get_event_loop()
        case_fut = loop.run_in_executor(None, lambda: chronicle.session.get(case_url))
        alerts_fut = loop.run_in_executor(None, lambda: chronicle.session.get(alerts_url))
        comments_fut = loop.run_in_executor(None, lambda: chronicle.session.get(comments_url))

        case_res, alerts_res, comments_res = await asyncio.gather(
            case_fut, alerts_fut, comments_fut, return_exceptions=True
        )

        def _safe_json(res):
            if isinstance(res, Exception):
                return {"error": str(res)}
            if hasattr(res, "status_code") and res.status_code == 200:
                return res.json()
            return {"status_code": getattr(res, "status_code", None), "text": getattr(res, "text", str(res))}

        case_data = _safe_json(case_res)
        alerts_data = _safe_json(alerts_res)
        comments_data = _safe_json(comments_res)

        alerts_list = alerts_data.get("caseAlerts", []) if isinstance(alerts_data, dict) else []

        return {
            "case_id": short_id,
            "case_details": case_data,
            "case_alerts": alerts_data,
            "alert_count": len(alerts_list),
            "case_comments": comments_data,
        }
    except Exception as e:
        logger.error("Error retrieving full details for case %s: %s", case_id, e)
        return {"error": f"Failed to get full case details: {str(e)}"}


# ============================================================================
# Case Creation & LegacyCaseService Endpoints (Chronicle v1alpha)
# ============================================================================


@server.tool()
async def create_case(
    case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Ingest a package of cases and alerts into Chronicle SIEM via legacyCases:createCase (v1alpha)."""
    try:
        if not case_data:
            return {"error": "case_data parameter is required and cannot be empty"}
        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Ingesting case package via legacyCases:createCase")
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:createCase",
            api_version=APIVersion.V1ALPHA,
            json=case_data,
            error_message="Failed to create case package",
        )
    except Exception as e:
        error_msg = f"Error creating case package: {str(e)}"
        logger.error("%s", error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def create_manual_case(
    case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Programmatically create a manual case in Chronicle SIEM via legacyCases:createManualCase (v1alpha)."""
    try:
        if not case_data:
            return {"error": "case_data parameter is required and cannot be empty"}
        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Creating manual case via legacyCases:createManualCase")
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:createManualCase",
            api_version=APIVersion.V1ALPHA,
            json=case_data,
            error_message="Failed to create manual case",
        )
    except Exception as e:
        error_msg = f"Error creating manual case: {str(e)}"
        logger.error("%s", error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def create_or_update_case(
    case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new case or update an existing case via legacy:legacyCreateOrUpdateCase (v1alpha)."""
    try:
        if not case_data:
            return {"error": "case_data parameter is required and cannot be empty"}
        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Creating or updating case via legacy:legacyCreateOrUpdateCase")
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacy:legacyCreateOrUpdateCase",
            api_version=APIVersion.V1ALPHA,
            json=case_data,
            error_message="Failed to create or update case",
        )
    except Exception as e:
        error_msg = f"Error creating or updating case: {str(e)}"
        logger.error("%s", error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def batch_get_legacy_cases(
    case_ids: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Batch retrieve cases by ID via legacy:legacyBatchGetCases (v1alpha)."""
    try:
        if not case_ids:
            return {"error": "case_ids parameter is required and cannot be empty"}
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="GET",
            endpoint_path="legacy:legacyBatchGetCases",
            api_version=APIVersion.V1ALPHA,
            params={"names": case_ids},
            error_message="Failed to batch get legacy cases",
        )
    except Exception as e:
        logger.error("Error in batch_get_legacy_cases: %s", e)
        return {"error": f"Failed to batch get legacy cases: {str(e)}"}


@server.tool()
async def merge_cases(
    case_ids: List[str],
    target_case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Merge multiple cases into a single target case via cases:merge (v1)."""
    try:
        if not case_ids or not target_case_id:
            return {"error": "Both case_ids and target_case_id are required"}
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases:merge"
        payload = {
            "casesIds": [int(cid) for cid in case_ids],
            "caseToMergeWith": int(target_case_id),
        }
        response = chronicle.session.post(url, json=payload)
        if response.status_code != 200:
            return {"error": f"Failed to merge cases: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error merging cases: %s", e)
        return {"error": f"Failed to merge cases: {str(e)}"}


@server.tool()
async def get_or_create_case_summary(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate or retrieve the AI summary for a case via cases/{id}:getOrCreateCaseSummary (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases/{short_id}:getOrCreateCaseSummary"
        response = chronicle.session.post(url, json={})
        if response.status_code != 200:
            return {"error": f"Failed to get/create case summary: {response.status_code} - {response.text}"}
        return response.json() if response.text else {}
    except Exception as e:
        logger.error("Error getting/creating case summary: %s", e)
        return {"error": f"Failed to get/create case summary: {str(e)}"}


@server.tool()
async def get_case_overview(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve case overview dashboard data via cases/{id}:caseOverviewData (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:caseOverviewData"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case overview: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case overview: %s", e)
        return {"error": f"Failed to get case overview: {str(e)}"}


@server.tool()
async def resolve_case_overview_widget(
    case_id: str,
    widget_id: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve overview widget data for a case via cases/{id}:resolveOverviewWidget (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}:resolveOverviewWidget"
        params = {"widgetId": widget_id} if widget_id else {}
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to resolve case overview widget: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error resolving case overview widget: %s", e)
        return {"error": f"Failed to resolve case overview widget: {str(e)}"}


@server.tool()
async def query_case_views(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Query dynamic case views via cases/{id}:queryCaseViews (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases/{short_id}:queryCaseViews"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to query case views: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error querying case views: %s", e)
        return {"error": f"Failed to query case views: {str(e)}"}


@server.tool()
async def count_case_priorities(
    filter_query: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Count cases grouped by priority via cases:countPriorities (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases:countPriorities"
        params = {"filter": filter_query} if filter_query else {}
        response = chronicle.session.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to count case priorities: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error counting case priorities: %s", e)
        return {"error": f"Failed to count case priorities: {str(e)}"}


@server.tool()
async def generate_case_report(
    report_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a formatted investigation report for a case via cases:generateReport (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases:generateReport"
        response = chronicle.session.post(url, json=report_data)
        if response.status_code != 200:
            return {"error": f"Failed to generate case report: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error generating case report: %s", e)
        return {"error": f"Failed to generate case report: {str(e)}"}


@server.tool()
async def batch_attach_case_evidence(
    case_id: str,
    evidence_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Batch attach UDM events or artifacts as evidence to a case via cases/{id}:batchAttachEvidence (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases/{short_id}:batchAttachEvidence"
        response = chronicle.session.post(url, json=evidence_payload)
        if response.status_code != 200:
            return {"error": f"Failed to attach case evidence: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error attaching case evidence: %s", e)
        return {"error": f"Failed to attach case evidence: {str(e)}"}


@server.tool()
async def batch_detach_case_evidence(
    case_id: str,
    evidence_payload: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Batch detach evidence items from a case via cases/{id}:batchDetachEvidence (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases/{short_id}:batchDetachEvidence"
        response = chronicle.session.post(url, json=evidence_payload)
        if response.status_code != 200:
            return {"error": f"Failed to detach case evidence: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error detaching case evidence: %s", e)
        return {"error": f"Failed to detach case evidence: {str(e)}"}


@server.tool()
async def execute_bulk_add_tag(
    cases_ids: List[int],
    tags: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Add tags across multiple cases in bulk via cases:executeBulkAddTag (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkAddTag"
        payload = {"casesIds": cases_ids, "tags": tags}
        response = chronicle.session.post(url, json=payload)
        if response.status_code != 200:
            return {"error": f"Failed bulk add tag: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error in execute_bulk_add_tag: %s", e)
        return {"error": f"Failed bulk add tag: {str(e)}"}


@server.tool()
async def execute_bulk_assign_case(
    cases_ids: List[int],
    assignee: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Assign multiple cases in bulk via cases:executeBulkAssign (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkAssign"
        payload = {"casesIds": cases_ids, "userName": assignee}
        response = chronicle.session.post(url, json=payload)
        if response.status_code != 200:
            return {"error": f"Failed bulk assign case: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error in execute_bulk_assign_case: %s", e)
        return {"error": f"Failed bulk assign case: {str(e)}"}


@server.tool()
async def execute_bulk_change_priority(
    cases_ids: List[int],
    priority: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Change priority across multiple cases in bulk via cases:executeBulkChangePriority (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkChangePriority"
        payload = {"casesIds": cases_ids, "priority": priority}
        response = chronicle.session.post(url, json=payload)
        if response.status_code != 200:
            return {"error": f"Failed bulk change priority: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error in execute_bulk_change_priority: %s", e)
        return {"error": f"Failed bulk change priority: {str(e)}"}


@server.tool()
async def execute_bulk_change_stage(
    cases_ids: List[int],
    stage: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Change stage across multiple cases in bulk via cases:executeBulkChangeStage (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        url = f"{_get_base_endpoint(chronicle)}/cases:executeBulkChangeStage"
        payload = {"casesIds": cases_ids, "stage": stage}
        response = chronicle.session.post(url, json=payload)
        if response.status_code != 200:
            return {"error": f"Failed bulk change stage: {response.status_code} - {response.text}"}
        return response.json() if response.text else {"status": "SUCCESS"}
    except Exception as e:
        logger.error("Error in execute_bulk_change_stage: %s", e)
        return {"error": f"Failed bulk change stage: {str(e)}"}


@server.tool()
async def fetch_wiz_related_issues(
    case_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch Wiz-related cloud security posture issues for a case via cases/{id}:fetchWizRelatedIssues (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases/{short_id}:fetchWizRelatedIssues"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to fetch Wiz related issues: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error fetching Wiz related issues: %s", e)
        return {"error": f"Failed to fetch Wiz related issues: {str(e)}"}





@server.tool()
async def add_evidence_to_case(
    evidence_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Attach legacy evidence to a case via legacyCases:addEvidence (v1alpha)."""
    try:
        if not evidence_data:
            return {"error": "evidence_data parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:addEvidence",
            api_version=APIVersion.V1ALPHA,
            json=evidence_data,
            error_message="Failed to add evidence to case",
        )
    except Exception as e:
        logger.error("Error adding evidence to case: %s", e)
        return {"error": f"Failed to add evidence to case: {str(e)}"}


@server.tool()
async def investigator_extend_case_graph(
    graph_request: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Extend the investigation graph for a case via legacyCases:investigatorExtendCaseGraph (v1alpha)."""
    try:
        if not graph_request:
            return {"error": "graph_request parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:investigatorExtendCaseGraph",
            api_version=APIVersion.V1ALPHA,
            json=graph_request,
            error_message="Failed to extend case graph",
        )
    except Exception as e:
        logger.error("Error extending case graph: %s", e)
        return {"error": f"Failed to extend case graph: {str(e)}"}


@server.tool()
async def simulate_alert(
    simulation_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Simulate a specific alert within a test case via legacyCases:simulateAlert (v1alpha)."""
    try:
        if not simulation_data:
            return {"error": "simulation_data parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:simulateAlert",
            api_version=APIVersion.V1ALPHA,
            json=simulation_data,
            error_message="Failed to simulate alert",
        )
    except Exception as e:
        logger.error("Error simulating alert: %s", e)
        return {"error": f"Failed to simulate alert: {str(e)}"}


@server.tool()
async def generate_use_cases(
    generation_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Simulate and generate test use cases in the case queue via legacyCases:generateUseCases (v1alpha)."""
    try:
        if not generation_data:
            return {"error": "generation_data parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:generateUseCases",
            api_version=APIVersion.V1ALPHA,
            json=generation_data,
            error_message="Failed to generate use cases",
        )
    except Exception as e:
        logger.error("Error generating use cases: %s", e)
        return {"error": f"Failed to generate use cases: {str(e)}"}


@server.tool()
async def inject_sample_data(
    sample_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Inject sample telemetry/alert data into a legacy case via legacyCases:injectSampleData (v1alpha)."""
    try:
        if not sample_data:
            return {"error": "sample_data parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:injectSampleData",
            api_version=APIVersion.V1ALPHA,
            json=sample_data,
            error_message="Failed to inject sample data",
        )
    except Exception as e:
        logger.error("Error injecting sample data: %s", e)
        return {"error": f"Failed to inject sample data: {str(e)}"}


@server.tool()
async def create_simulated_custom_case(
    custom_case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a custom simulated case via legacyCases:createSimulatedCustomCase (v1alpha)."""
    try:
        if not custom_case_data:
            return {"error": "custom_case_data parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:createSimulatedCustomCase",
            api_version=APIVersion.V1ALPHA,
            json=custom_case_data,
            error_message="Failed to create simulated custom case",
        )
    except Exception as e:
        logger.error("Error creating simulated custom case: %s", e)
        return {"error": f"Failed to create simulated custom case: {str(e)}"}


@server.tool()
async def get_custom_cases(
    environment: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List custom simulated cases in the environment via legacyCases:getCustomCases (v1alpha)."""
    try:
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        params = {"environment": environment} if environment else {}
        return chronicle_request(
            chronicle,
            method="GET",
            endpoint_path="legacyCases:getCustomCases",
            api_version=APIVersion.V1ALPHA,
            params=params,
            error_message="Failed to get custom cases",
        )
    except Exception as e:
        logger.error("Error getting custom cases: %s", e)
        return {"error": f"Failed to get custom cases: {str(e)}"}


@server.tool()
async def get_custom_case_details(
    custom_case_query: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get details of a custom simulated case via legacyCases:getCustomCaseDetails (v1alpha)."""
    try:
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:getCustomCaseDetails",
            api_version=APIVersion.V1ALPHA,
            json=custom_case_query,
            error_message="Failed to get custom case details",
        )
    except Exception as e:
        logger.error("Error getting custom case details: %s", e)
        return {"error": f"Failed to get custom case details: {str(e)}"}


@server.tool()
async def export_custom_case(
    custom_case_name: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Export a custom simulated case as a JSON package via legacyCases:exportCustomCase (v1alpha)."""
    try:
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="GET",
            endpoint_path="legacyCases:exportCustomCase",
            api_version=APIVersion.V1ALPHA,
            params={"customCaseName": custom_case_name},
            error_message="Failed to export custom case",
        )
    except Exception as e:
        logger.error("Error exporting custom case: %s", e)
        return {"error": f"Failed to export custom case: {str(e)}"}


@server.tool()
async def import_custom_case(
    case_package: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Import a custom simulated case package via legacyCases:importCustomCase (v1alpha)."""
    try:
        if not case_package:
            return {"error": "case_package parameter is required"}
        from secops.chronicle.client import APIVersion
        from secops.chronicle.utils.request_utils import chronicle_request

        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:importCustomCase",
            api_version=APIVersion.V1ALPHA,
            json=case_package,
            error_message="Failed to import custom case",
        )
    except Exception as e:
        logger.error("Error importing custom case: %s", e)
        return {"error": f"Failed to import custom case: {str(e)}"}


@server.tool()
async def get_case_comment(
    case_id: str,
    comment_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve a specific comment on a case via cases/{case_id}/caseComments/{comment_id} (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        short_comment_id = comment_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}/caseComments/{short_comment_id}"
        response = chronicle.session.get(url)
        if response.status_code != 200:
            return {"error": f"Failed to get case comment: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error getting case comment: %s", e)
        return {"error": f"Failed to get case comment: {str(e)}"}


@server.tool()
async def update_case_comment(
    case_id: str,
    comment_id: str,
    comment: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an existing comment on a case via PATCH cases/{case_id}/caseComments/{comment_id} (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        short_comment_id = comment_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}/caseComments/{short_comment_id}"
        response = chronicle.session.patch(
            url, params={"updateMask": "comment"}, json={"comment": comment}
        )
        if response.status_code != 200:
            return {"error": f"Failed to update case comment: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error updating case comment: %s", e)
        return {"error": f"Failed to update case comment: {str(e)}"}


@server.tool()
async def delete_case_comment(
    case_id: str,
    comment_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a comment from a case via DELETE cases/{case_id}/caseComments/{comment_id} (v1)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        short_comment_id = comment_id.split("/")[-1]
        url = f"{_get_base_endpoint(chronicle)}/cases/{short_id}/caseComments/{short_comment_id}"
        response = chronicle.session.delete(url)
        if response.status_code not in (200, 204):
            return {"error": f"Failed to delete case comment: {response.status_code} - {response.text}"}
        return {"status": "SUCCESS", "deleted_comment_id": short_comment_id}
    except Exception as e:
        logger.error("Error deleting case comment: %s", e)
        return {"error": f"Failed to delete case comment: {str(e)}"}


@server.tool()
async def batch_create_case_comments(
    case_id: str,
    comments: List[str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Batch create multiple comments on a case via cases/{case_id}/caseComments:batchCreate (v1alpha)."""
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        short_id = _format_case_name(chronicle.instance_id, case_id).split("/")[-1]
        url = f"{_get_base_endpoint(chronicle, 'v1alpha')}/cases/{short_id}/caseComments:batchCreate"
        requests_payload = [{"caseComment": {"comment": c}} for c in comments]
        response = chronicle.session.post(url, json={"requests": requests_payload})
        if response.status_code != 200:
            return {"error": f"Failed to batch create case comments: {response.status_code} - {response.text}"}
        return response.json()
    except Exception as e:
        logger.error("Error batch creating case comments: %s", e)
        return {"error": f"Failed to batch create case comments: {str(e)}"}


