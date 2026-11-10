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
"""Security Operations MCP tools for legacy (Looker) dashboards.

Chronicle's legacy dashboards live under ``/dashboards`` and are backed by
Looker (LookML). They are distinct from the native dashboards under
``/nativeDashboards`` (see ``list_dashboards`` / ``get_dashboard``). Every
method in this module is v1alpha-only. The migration tools convert legacy
dashboards into native dashboards and report on migration progress.
"""

import logging
from typing import Any, Dict, Optional, Union

from secops_mcp.server import get_chronicle_client, server
from secops_mcp.utils import chronicle_api_request, parse_json_arg

# Configure logging
logger = logging.getLogger("secops-mcp")

_DASHBOARDS_PATH = "/dashboards"


def _compact(d: Dict[str, Any]) -> Dict[str, Any]:
    """Drop ``None`` values from a JSON body."""
    return {k: v for k, v in d.items() if v is not None}


def _dashboard_id(value: str) -> str:
    """Return the bare dashboard ID from an ID or a full resource name."""
    return value.rsplit("/", 1)[-1] if "/" in value else value


def _dashboard_name(chronicle: Any, value: str) -> str:
    """Return the full ``.../dashboards/{id}`` resource name."""
    if value.startswith("projects/"):
        return value
    return f"{chronicle.instance_id}{_DASHBOARDS_PATH}/{_dashboard_id(value)}"


def _build_dashboard_resource(
    dashboard: Optional[Union[Dict[str, Any], str]],
    display_name: Optional[str],
    dashboard_type: Optional[str],
    lookml: Optional[str],
    default_dashboard: Optional[bool],
) -> Dict[str, Any]:
    """Merge a raw Dashboard dict with convenience fields."""
    body = dict(parse_json_arg(dashboard, "dashboard") or {})
    body.update(
        _compact(
            {
                "displayName": display_name,
                "type": dashboard_type,
                "lookml": lookml,
                "defaultDashboard": default_dashboard,
            }
        )
    )
    return body


@server.tool()
async def get_legacy_dashboard(
    dashboard_id: str,
    view: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a legacy (Looker) Chronicle dashboard by ID. v1alpha-only.

    Retrieves one dashboard from the legacy ``/dashboards`` collection.
    Use ``view="DASHBOARD_VIEW_EXPORT"`` to request the LookML definition.
    The response's ``migrationInfo`` (when present) shows whether this
    dashboard has already been migrated to a native dashboard and which one.

    **Workflow Integration:**
    - Inspect a legacy dashboard before deciding to migrate or delete it.
    - Export LookML for backup or re-creation.

    **Use Cases:**
    - Check ``migrationInfo.state`` / ``migrationInfo.nativeDashboard``
    - Export a dashboard definition as LookML

    Args:
        dashboard_id (str): Dashboard ID or full resource name
            ``projects/.../instances/.../dashboards/{id}``.
        view (Optional[str]): ``DASHBOARD_VIEW_BASIC`` (default, no LookML),
            ``DASHBOARD_VIEW_EXPORT`` (LookML, no URI) or
            ``DASHBOARD_VIEW_FULL`` (everything).
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: The Dashboard resource, or an error message.

    Example Usage:
        get_legacy_dashboard("1234abcd", view="DASHBOARD_VIEW_EXPORT")

    Next Steps (using MCP-enabled tools):
        - ``get_dashboard`` (native) on ``migrationInfo.nativeDashboard``
        - ``copy_legacy_dashboard`` to make an editable copy
    """
    try:
        logger.info("Getting legacy dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle,
            "GET",
            f"{_DASHBOARDS_PATH}/{_dashboard_id(dashboard_id)}",
            params={"view": view},
        )
    except Exception as e:
        logger.error("Error getting legacy dashboard: %s", e, exc_info=True)
        return {"error": f"Error getting legacy dashboard: {e}"}


@server.tool()
async def list_legacy_dashboards(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    view: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List legacy (Looker) Chronicle dashboards. v1alpha-only.

    Lists the legacy ``/dashboards`` collection: predefined (read-only,
    Chronicle-provided), user and customer dashboards. This is NOT the native
    dashboard list; use ``list_dashboards`` for ``/nativeDashboards``. The API
    exposes no filter parameter, only paging and ``view``.

    **Workflow Integration:**
    - Inventory legacy dashboards ahead of a migration to native dashboards.

    **Use Cases:**
    - Audit which Looker dashboards still exist in the instance
    - Find dashboard IDs for ``get_legacy_dashboard`` / ``delete_legacy_dashboard``

    Args:
        page_size (Optional[int]): Maximum dashboards per page.
        page_token (Optional[str]): ``nextPageToken`` from a previous call.
        view (Optional[str]): ``DASHBOARD_VIEW_BASIC`` (default),
            ``DASHBOARD_VIEW_EXPORT`` or ``DASHBOARD_VIEW_FULL``.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"dashboards": [...], "nextPageToken": "...",
            "total_dashboards": N}`` or an error message.

    Example Usage:
        list_legacy_dashboards(page_size=50)

    Next Steps (using MCP-enabled tools):
        - ``get_legacy_dashboard`` for details and ``migrationInfo``
        - ``list_dashboards`` to view the native dashboards
    """
    try:
        logger.info("Listing legacy dashboards (page_size=%s)", page_size)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        response = chronicle_api_request(
            chronicle,
            "GET",
            _DASHBOARDS_PATH,
            params={
                "pageSize": page_size,
                "pageToken": page_token,
                "view": view,
            },
        )
        response["total_dashboards"] = len(response.get("dashboards", []))
        return response
    except Exception as e:
        logger.error("Error listing legacy dashboards: %s", e, exc_info=True)
        return {"error": f"Error listing legacy dashboards: {e}"}


@server.tool()
async def delete_legacy_dashboard(
    dashboard_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a legacy (Looker) Chronicle dashboard. v1alpha-only.

    Permanently removes a dashboard from the legacy ``/dashboards``
    collection. Predefined and other ``readOnly`` dashboards cannot be
    deleted. Deleting a legacy dashboard does not affect any native dashboard
    it was migrated into.

    **Workflow Integration:**
    - Clean up legacy dashboards after confirming the migrated native
      dashboard (``migrationInfo.nativeDashboard``) is correct.

    **Use Cases:**
    - Retire Looker dashboards once migration is complete
    - Remove obsolete user or customer dashboards

    Args:
        dashboard_id (str): Dashboard ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"status": "deleted", "dashboard_id": ...}`` or an
            error message.

    Example Usage:
        delete_legacy_dashboard("1234abcd")

    Next Steps (using MCP-enabled tools):
        - ``list_legacy_dashboards`` to confirm removal
    """
    try:
        logger.info("Deleting legacy dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        bare_id = _dashboard_id(dashboard_id)
        chronicle_api_request(
            chronicle, "DELETE", f"{_DASHBOARDS_PATH}/{bare_id}"
        )
        return {"status": "deleted", "dashboard_id": bare_id}
    except Exception as e:
        logger.error("Error deleting legacy dashboard: %s", e, exc_info=True)
        return {"error": f"Error deleting legacy dashboard: {e}"}


@server.tool()
async def copy_legacy_dashboard(
    dashboard_id: str,
    dashboard_type: Optional[str] = None,
    display_name: Optional[str] = None,
    default_dashboard: Optional[bool] = None,
    destination: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Copy a legacy (Looker) dashboard to another dashboard type. v1alpha-only.

    Calls ``POST /dashboards/{id}:copy``. The copy is created as a new legacy
    dashboard of the destination type (``DASHBOARD_TYPE_USER`` or
    ``DASHBOARD_TYPE_CUSTOMER``); ``DASHBOARD_TYPE_PREDEFINED`` cannot be a
    destination. Typical use is turning a read-only predefined dashboard into
    an editable user copy. This stays within the legacy family; migrating to
    a native dashboard is done in the Chronicle UI migration wizard.

    **Workflow Integration:**
    - Copy a predefined dashboard so it can be edited.
    - Promote a personal dashboard to a customer-wide one.

    **Use Cases:**
    - Create an editable copy of a Chronicle-provided dashboard
    - Share a user dashboard with all users of the instance

    Args:
        dashboard_id (str): Source dashboard ID or full resource name.
        dashboard_type (Optional[str]): Destination type, required unless
            given in ``destination``: ``DASHBOARD_TYPE_USER`` or
            ``DASHBOARD_TYPE_CUSTOMER``.
        display_name (Optional[str]): Name for the copy.
        default_dashboard (Optional[bool]): Make the copy the default.
        destination (Optional[Union[Dict[str, Any], str]]): Destination
            Dashboard resource (dict or JSON string), e.g.
            ``{"displayName": "My copy", "type": "DASHBOARD_TYPE_USER"}``.
            Explicit args above override matching keys. The request body sent
            is ``{"destination": {"parent": <instance>, "dashboard": {...}}}``.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: The newly created Dashboard resource, or an error.

    Example Usage:
        copy_legacy_dashboard("predef-1", dashboard_type="DASHBOARD_TYPE_USER",
            display_name="My Overview")

    Next Steps (using MCP-enabled tools):
        - ``get_legacy_dashboard`` on the new dashboard's ``name``
    """
    try:
        logger.info("Copying legacy dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        dest_dashboard = _build_dashboard_resource(
            destination, display_name, dashboard_type, None, default_dashboard
        )
        if not dest_dashboard.get("type"):
            return {
                "error": "dashboard_type (or destination.type) is required "
                "and must be DASHBOARD_TYPE_USER or DASHBOARD_TYPE_CUSTOMER"
            }
        body = {
            "destination": {
                "parent": chronicle.instance_id,
                "dashboard": dest_dashboard,
            }
        }
        return chronicle_api_request(
            chronicle,
            "POST",
            f"{_DASHBOARDS_PATH}/{_dashboard_id(dashboard_id)}:copy",
            json_body=body,
        )
    except Exception as e:
        logger.error("Error copying legacy dashboard: %s", e, exc_info=True)
        return {"error": f"Error copying legacy dashboard: {e}"}
