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
"""Security Operations MCP tools for investigation management."""

import logging
from typing import Any, Dict, List, Optional

from secops_mcp.server import get_chronicle_client, server


logger = logging.getLogger("secops-mcp")


@server.tool()
async def list_investigations(
    page_size: int = 50,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List all investigations in Chronicle instance.

    Retrieves a paginated list of all investigations with their status,
    verdict, and confidence information. Supports pagination for large
    result sets.

    **Workflow Integration:**
    - Use to get an overview of all active investigations
    - Essential for monitoring investigation status across the environment
    - Can be used to identify investigations that need attention
    - Helps track investigation progress and outcomes

    **Use Cases:**
    - "List all active investigations from the past week"
    - "Show me all investigations with high confidence verdicts"
    - "What investigations are currently in progress?"
    - "Get an overview of recent investigation activity"

    Args:
        page_size (int): Number of investigations to return per page.
            Defaults to 50.
        page_token (Optional[str]): Token for pagination. Use the
            next_page_token from previous response to get next page.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing list of investigations with
            their display names, status, verdict, confidence, and pagination
            token. Returns error message if retrieval fails.

    Next Steps (using MCP-enabled tools):
        - Use `get_investigation` to get detailed info for specific
          investigations
        - Use `fetch_associated_investigations` to find investigations
          linked to alerts or cases
        - For investigations needing action, use alert or case management
          tools
        - Use entity lookup tools on indicators found in investigations
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        print(f"Listing investigations (page_size={page_size})...")

        result = chronicle.list_investigations(
            page_size=page_size, page_token=page_token
        )

        investigations = result.get("investigations", [])
        print(f"Successfully retrieved {len(investigations)} investigation(s)")
        return result

    except Exception as e:
        error_msg = f"Error listing investigations: {str(e)}"
        print(error_msg)
        return {"error": error_msg}


@server.tool()
async def get_investigation(
    investigation_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve specific investigation by ID.

    Gets detailed information for a specific investigation including status,
    verdict, confidence, and associated metadata.

    **Workflow Integration:**
    - Use after listing investigations to get detailed information
    - Essential for reviewing investigation findings and recommendations
    - Can be used to check investigation progress and status
    - Helps analysts understand automated analysis results

    **Use Cases:**
    - "Get details for investigation inv_123"
    - "What's the verdict for this investigation?"
    - "Show me the confidence score for this investigation"
    - "Retrieve investigation findings and recommendations"

    Args:
        investigation_id (str): The unique identifier of the investigation
            to retrieve.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing detailed investigation
            information including display name, status, verdict, confidence,
            and timestamps. Returns error message if retrieval fails.

    Next Steps (using MCP-enabled tools):
        - Based on verdict, use alert or case management tools to update
          status
        - Use `fetch_associated_investigations` to find related
          investigations
        - For high-confidence verdicts, consider creating cases or alerts
        - Use entity lookup tools on indicators found in investigation
    """
    try:
        if not investigation_id:
            return {
                "error": (
                    "investigation_id parameter is required and cannot be "
                    "empty"
                )
            }

        chronicle = get_chronicle_client(project_id, customer_id, region)
        print(f"Retrieving investigation: {investigation_id}...")

        investigation = chronicle.get_investigation(
            investigation_id=investigation_id
        )

        if not investigation:
            return {
                "error": f"Investigation not found: {investigation_id}",
                "investigation_id": investigation_id,
            }

        print(f"Successfully retrieved investigation: {investigation_id}")
        return investigation

    except Exception as e:
        error_msg = (
            f"Error retrieving investigation {investigation_id}: {str(e)}"
        )
        print(error_msg)
        return {"error": error_msg}


@server.tool()
async def trigger_investigation(
    alert_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create new investigation for a specific alert.

    Triggers automated investigation analysis for a given alert. Returns
    the created investigation details including status and trigger type.

    **Workflow Integration:**
    - Use after identifying high-priority alerts that need investigation
    - Essential for initiating automated analysis and recommendations
    - Can be used as part of incident response workflows
    - Helps automate investigation processes for security alerts

    **Use Cases:**
    - "Trigger an investigation for this high-priority alert"
    - "Create an investigation for alert_123"
    - "Start automated analysis for this suspicious alert"
    - "Initiate investigation for this security event"

    Args:
        alert_id (str): The unique identifier of the alert to investigate.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing created investigation details
            including name, status, and trigger type. Returns error message
            if creation fails.

    Next Steps (using MCP-enabled tools):
        - Use `get_investigation` to check investigation progress and
          results
        - Use `list_investigations` to see all investigations
        - Based on investigation verdict, update alert status using
          `do_update_security_alert`
        - Use entity lookup tools on indicators found in investigation
        - Consider creating a case if investigation confirms threat
    """
    try:
        if not alert_id:
            return {
                "error": "alert_id parameter is required and cannot be empty"
            }

        chronicle = get_chronicle_client(project_id, customer_id, region)
        print(f"Triggering investigation for alert: {alert_id}...")

        investigation = chronicle.trigger_investigation(alert_id=alert_id)

        if not investigation:
            return {
                "error": (
                    f"Failed to trigger investigation for alert: {alert_id}"
                ),
                "alert_id": alert_id,
            }

        result = {
            "message": "Successfully triggered investigation",
            "alert_id": alert_id,
            "investigation": {
                "name": investigation.get("name"),
                "display_name": investigation.get("displayName"),
                "status": investigation.get("status"),
                "trigger_type": investigation.get("triggerType"),
                "create_time": investigation.get("createTime"),
            },
        }

        print(f"Successfully triggered investigation for alert: {alert_id}")
        return result

    except Exception as e:
        error_msg = (
            f"Error triggering investigation for alert {alert_id}: {str(e)}"
        )
        print(error_msg)
        return {"error": error_msg}


@server.tool()
async def fetch_associated_investigations(
    detection_type: str,
    alert_ids: Optional[List[str]] = None,
    case_ids: Optional[List[str]] = None,
    association_limit_per_detection: int = 5,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve investigations associated with alerts or cases.

    Fetches investigations linked to specific alerts or cases. Supports
    filtering by detection type (ALERT or CASE) and returns investigation
    associations with verdict information.

    **Workflow Integration:**
    - Use to find all investigations related to specific alerts or cases
    - Essential for understanding investigation history and outcomes
    - Can be used to correlate multiple investigations
    - Helps track investigation progress across related detections

    **Use Cases:**
    - "What investigations are associated with this alert?"
    - "Show me all investigations for these cases"
    - "Find investigations related to alert_123 and alert_456"
    - "Get investigation history for this case"

    Args:
        detection_type (str): Type of detection to query. Valid values:
            "ALERT", "CASE", "DETECTION_TYPE_ALERT", "DETECTION_TYPE_CASE".
        alert_ids (Optional[List[str]]): List of alert IDs to query.
            Required if detection_type is ALERT.
        case_ids (Optional[List[str]]): List of case IDs to query.
            Required if detection_type is CASE.
        association_limit_per_detection (int): Maximum number of
            investigations to return per detection. Defaults to 5.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing investigation associations
            grouped by detection ID, with verdict and confidence information.
            Returns error message if retrieval fails.

    Next Steps (using MCP-enabled tools):
        - Use `get_investigation` to get detailed info for specific
          investigations
        - Based on verdicts, use alert or case management tools to update
          status
        - Use `trigger_investigation` to create new investigations if
          needed
        - Use entity lookup tools on indicators found in investigations
    """
    try:
        detection_type_upper = detection_type.upper()
        valid_types = [
            "ALERT",
            "CASE",
            "DETECTION_TYPE_ALERT",
            "DETECTION_TYPE_CASE",
        ]

        if detection_type_upper not in valid_types:
            return {
                "error": (
                    f"Invalid detection_type: {detection_type}. "
                    f'Valid values: {", ".join(valid_types)}'
                )
            }

        is_alert_type = detection_type_upper in [
            "ALERT",
            "DETECTION_TYPE_ALERT",
        ]

        if is_alert_type and not alert_ids:
            return {
                "error": (
                    "alert_ids parameter is required when detection_type "
                    "is ALERT"
                )
            }

        if not is_alert_type and not case_ids:
            return {
                "error": (
                    "case_ids parameter is required when detection_type "
                    "is CASE"
                )
            }

        chronicle = get_chronicle_client(project_id, customer_id, region)

        detection_label = "alert" if is_alert_type else "case"
        ids = alert_ids if is_alert_type else case_ids
        print(
            f"Fetching investigations for {len(ids)} "
            f"{detection_label}(s)..."
        )

        result = chronicle.fetch_associated_investigations(
            detection_type=detection_type,
            alert_ids=alert_ids,
            case_ids=case_ids,
            association_limit_per_detection=association_limit_per_detection,
        )

        associations_list = result.get("associationsList", {})

        associations_dict = {}
        total_investigations = 0

        for detection_id, data in associations_list.items():
            investigations = data.get("investigations", [])
            total_investigations += len(investigations)

            inv_list = []
            for inv in investigations:
                inv_dict = {
                    "name": inv.get("name"),
                    "display_name": inv.get("displayName"),
                    "verdict": inv.get("verdict"),
                    "confidence": inv.get("confidence"),
                    "status": inv.get("status"),
                }
                inv_list.append(inv_dict)

            associations_dict[detection_id] = {
                "investigation_count": len(inv_list),
                "investigations": inv_list,
            }

        response = {
            "message": (
                f"Successfully retrieved investigations for "
                f"{len(associations_dict)} {detection_label}(s)"
            ),
            "detection_type": detection_type,
            "total_detections": len(associations_dict),
            "total_investigations": total_investigations,
            "associations": associations_dict,
        }

        print(
            f"Successfully retrieved {total_investigations} "
            f"investigation(s) for {len(associations_dict)} "
            f"{detection_label}(s)"
        )
        return response

    except Exception as e:
        error_msg = f"Error fetching associated investigations: {str(e)}"
        print(error_msg)
        return {"error": error_msg}
