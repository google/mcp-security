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
        logger.error(f"Error listing cases: {e}")
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
        logger.error(f"Error getting case {case_id}: {e}")
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
        logger.error(f"Error updating case {case_id}: {e}")
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
        logger.error(f"Error changing case priority: {e}")
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
        logger.error(f"Error changing case stage: {e}")
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
        logger.error(f"Error assigning case: {e}")
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
        logger.error(f"Error setting custom case fields: {e}")
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
        logger.error(f"Error adding tag to case: {e}")
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
        logger.error(f"Error removing tag from case: {e}")
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
        logger.error(f"Error adding insight to case: {e}")
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
        logger.error(f"Error pausing SLA on case: {e}")
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
        logger.error(f"Error resuming SLA on case: {e}")
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
        logger.error(f"Error closing case(s): {e}")
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
        logger.error(f"Error reopening case(s): {e}")
        return {"error": f"Failed to reopen case: {str(e)}"}
