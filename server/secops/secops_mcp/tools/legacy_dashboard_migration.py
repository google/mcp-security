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
"""Security Operations MCP tools for legacy (Looker) dashboards and migration.

Chronicle's legacy dashboards live under ``/dashboards`` and are backed by
Looker (LookML). They are distinct from the native dashboards under
``/nativeDashboards`` (see ``list_dashboards`` / ``get_dashboard``). Every
method in this module is v1alpha-only. The migration tools convert legacy
dashboards into native dashboards and report on migration progress.
"""

import logging
from typing import Any, Dict, List, Optional, Union

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
async def create_legacy_dashboard(
    display_name: Optional[str] = None,
    dashboard_type: Optional[str] = None,
    lookml: Optional[str] = None,
    default_dashboard: Optional[bool] = None,
    dashboard: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a legacy (Looker/LookML) Chronicle dashboard. v1alpha-only.

    Creates a dashboard under ``/dashboards``, the legacy Looker-backed
    dashboard family. The dashboard is defined by a LookML model; the
    recommended source is the ``lookml`` returned by ``get_legacy_dashboard``
    with ``view="DASHBOARD_VIEW_EXPORT"``. For new work prefer native
    dashboards (``create_dashboard``); legacy dashboards exist mainly so they
    can be migrated.

    **Workflow Integration:**
    - Re-create or import a Looker dashboard from exported LookML.
    - Pair with ``batch_migrate_dashboards`` to convert it to a native
      dashboard afterwards.

    **Use Cases:**
    - Restore a legacy dashboard from a LookML backup
    - Stage a legacy dashboard for migration testing

    Args:
        display_name (Optional[str]): User-visible dashboard name.
        dashboard_type (Optional[str]): ``DASHBOARD_TYPE_USER`` (private to
            the caller) or ``DASHBOARD_TYPE_CUSTOMER`` (visible to all users).
            ``DASHBOARD_TYPE_PREDEFINED`` dashboards cannot be created.
        lookml (Optional[str]): LookML YAML defining the dashboard.
        default_dashboard (Optional[bool]): Show this dashboard by default
            (only one dashboard may be the default).
        dashboard (Optional[Union[Dict[str, Any], str]]): Full Dashboard
            resource as a dict or JSON string, e.g.
            ``{"displayName": "SOC Overview", "type": "DASHBOARD_TYPE_USER",
            "lookml": "..."}``. Explicit args above override matching keys.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: The created Dashboard resource (``name``,
            ``displayName``, ``type``, ``uri``, ...), or an error message.

    Example Usage:
        create_legacy_dashboard(display_name="SOC Overview",
            dashboard_type="DASHBOARD_TYPE_USER", lookml=lookml_text)

    Next Steps (using MCP-enabled tools):
        - ``get_legacy_dashboard`` to confirm the result
        - ``batch_migrate_dashboards`` to convert it to a native dashboard
    """
    try:
        logger.info("Creating legacy dashboard %s", display_name)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _build_dashboard_resource(
            dashboard, display_name, dashboard_type, lookml, default_dashboard
        )
        if not body:
            return {
                "error": "Provide display_name/lookml or a dashboard resource"
            }
        return chronicle_api_request(
            chronicle, "POST", _DASHBOARDS_PATH, json_body=body
        )
    except Exception as e:
        logger.error("Error creating legacy dashboard: %s", e, exc_info=True)
        return {"error": f"Error creating legacy dashboard: {e}"}


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
    Use ``view="DASHBOARD_VIEW_EXPORT"`` to include the LookML definition,
    which is the input format for ``create_legacy_dashboard``. The response's
    ``migrationInfo`` (when present) shows whether this dashboard has already
    been migrated to a native dashboard and which one.

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
        - ``batch_migrate_dashboards`` if not yet migrated
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
    - Inventory legacy dashboards ahead of a migration.
    - Compare with ``fetch_migratable_dashboards`` to see which are eligible.

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
        - ``fetch_migratable_dashboards`` to see migration eligibility
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
    an editable user copy. This stays within the legacy family; to produce a
    native dashboard use ``batch_migrate_dashboards`` instead.

    **Workflow Integration:**
    - Copy a predefined dashboard, then migrate the copy to native.
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
        - ``batch_migrate_dashboards`` with the new dashboard's ``name``
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


@server.tool()
async def fetch_migratable_dashboards(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    view: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List legacy (Looker) dashboards eligible for migration to native. v1alpha-only.

    Calls ``GET /dashboards:fetchMigratable``. Returns the subset of legacy
    dashboards that Chronicle can convert into native dashboards, each with
    a ``migrationInfo`` block (``state``, ``migrationJobId``,
    ``nativeDashboard``). This is the first step of the Looker-to-native
    migration workflow. The call may take several minutes on large instances.

    **Workflow Integration:**
    - Run before ``batch_migrate_dashboards`` to pick candidates.
    - Re-run afterwards; ``migrationInfo.state`` reflects progress.

    **Use Cases:**
    - Plan a dashboard migration
    - Find dashboards still in ``DASHBOARD_MIGRATION_STATE_PENDING``

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
        fetch_migratable_dashboards(page_size=100)

    Next Steps (using MCP-enabled tools):
        - ``batch_migrate_dashboards(dashboards=[...names...])``
        - ``fetch_dashboard_migration_metrics`` for an instance-wide summary
    """
    try:
        logger.info("Fetching migratable legacy dashboards")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        response = chronicle_api_request(
            chronicle,
            "GET",
            f"{_DASHBOARDS_PATH}:fetchMigratable",
            params={
                "pageSize": page_size,
                "pageToken": page_token,
                "view": view,
            },
        )
        response["total_dashboards"] = len(response.get("dashboards", []))
        return response
    except Exception as e:
        logger.error(
            "Error fetching migratable dashboards: %s", e, exc_info=True
        )
        return {"error": f"Error fetching migratable dashboards: {e}"}


@server.tool()
async def batch_migrate_dashboards(
    dashboards: Union[List[str], str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Migrate legacy (Looker) dashboards to native dashboards. v1alpha-only.

    Calls ``POST /dashboards:batchMigrate`` with the legacy dashboard resource
    names. Chronicle starts an asynchronous migration job that builds a native
    dashboard (``/nativeDashboards``) for each input. The response carries
    ``migrationJobId`` and ``jobMigrationStatus``; poll
    ``fetch_dashboard_migration_jobs`` for per-dashboard results. Some
    dashboards may end in ``DASHBOARD_MIGRATION_STATE_NEEDS_REVIEW`` and
    require manual checking in the Chronicle UI.

    **Workflow Integration:**
    - Feed it the ``name`` values from ``fetch_migratable_dashboards``.
    - Follow up with ``fetch_dashboard_migration_jobs(migration_job_id=...)``.

    **Use Cases:**
    - Bulk-convert Looker dashboards to native dashboards
    - Re-run migration for dashboards that previously failed

    Args:
        dashboards (Union[List[str], str]): Legacy dashboard IDs or full
            resource names, as a list or JSON array string. Bare IDs are
            expanded to ``projects/.../instances/.../dashboards/{id}``.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"migrationJobId": "...", "jobMigrationStatus":
            "JOB_MIGRATION_STATE_IN_PROGRESS" | "..._SUCCESS" |
            "..._PARTIAL_SUCCESS" | "..._FAILURE", "endTime": "..."}``
            plus ``dashboards_requested``, or an error message.

    Example Usage:
        batch_migrate_dashboards(dashboards=["1234abcd", "5678efgh"])

    Next Steps (using MCP-enabled tools):
        - ``fetch_dashboard_migration_jobs(migration_job_id=<id>)``
        - ``get_dashboard`` (native) on each result's ``nativeDashboard``
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        parsed = parse_json_arg(dashboards, "dashboards")
        if isinstance(dashboards, str) and parsed is None:
            parsed = [dashboards]
        if not isinstance(parsed, list) or not parsed:
            return {"error": "dashboards must be a non-empty list of names"}
        names = [_dashboard_name(chronicle, str(d)) for d in parsed]
        logger.info("Batch migrating %d legacy dashboard(s)", len(names))
        response = chronicle_api_request(
            chronicle,
            "POST",
            f"{_DASHBOARDS_PATH}:batchMigrate",
            json_body={"dashboards": names},
        )
        response["dashboards_requested"] = names
        return response
    except Exception as e:
        logger.error("Error batch migrating dashboards: %s", e, exc_info=True)
        return {"error": f"Error batch migrating dashboards: {e}"}


@server.tool()
async def fetch_dashboard_migration_metrics(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get instance-wide legacy-to-native dashboard migration metrics. v1alpha-only.

    Calls ``GET /dashboards:fetchMigrationMetrics``. Summarizes the Looker
    dashboard migration for the whole instance: how many Looker dashboards
    exist, how many have been migrated, are pending, processing or failed,
    the overall success rate, and how many needed human-in-the-loop review.

    **Workflow Integration:**
    - Report migration progress without enumerating dashboards.
    - Decide whether another ``batch_migrate_dashboards`` round is needed.

    **Use Cases:**
    - Track migration completion for a tenant
    - Spot a high ``failedDashboardsCount`` or ``hitlCount``

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"totalMigrations", "successRate", "hitlCount",
            "lookerDashboardCount", "migratedDashboardsCount",
            "pendingDashboardsCount", "processingDashboardsCount",
            "failedDashboardsCount"}`` or an error message.

    Example Usage:
        fetch_dashboard_migration_metrics()

    Next Steps (using MCP-enabled tools):
        - ``fetch_dashboard_migration_jobs`` to find the failing dashboards
        - ``fetch_migratable_dashboards`` to list what is still pending
    """
    try:
        logger.info("Fetching dashboard migration metrics")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle, "GET", f"{_DASHBOARDS_PATH}:fetchMigrationMetrics"
        )
    except Exception as e:
        logger.error(
            "Error fetching dashboard migration metrics: %s", e, exc_info=True
        )
        return {"error": f"Error fetching dashboard migration metrics: {e}"}


@server.tool()
async def fetch_dashboard_migration_jobs(
    migration_job_id: Optional[str] = None,
    dashboard_id: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get legacy-to-native dashboard migration jobs and results. v1alpha-only.

    Calls ``GET /dashboards:fetchMigrationJobs``. With no filters it returns
    every migration job for the instance; pass ``migration_job_id`` (from
    ``batch_migrate_dashboards``) to inspect one job, or ``dashboard_id`` to
    get only that legacy dashboard's migration result. Each job lists
    ``results`` with per-dashboard ``status``, ``errorMessage`` and the
    created ``nativeDashboard`` resource name.

    **Workflow Integration:**
    - Poll after ``batch_migrate_dashboards`` until ``jobMigrationStatus``
      leaves ``JOB_MIGRATION_STATE_IN_PROGRESS``.
    - Use ``results[].nativeDashboard`` to jump to the native dashboard.

    **Use Cases:**
    - Check whether a migration finished and which dashboards failed
    - Find the native dashboard created from a specific Looker dashboard

    Args:
        migration_job_id (Optional[str]): Migration job ID to fetch.
        dashboard_id (Optional[str]): Legacy dashboard ID or full resource
            name; restricts results to that dashboard.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"migrationJobs": [{"migrationJobId",
            "jobMigrationStatus", "startedBy", "startTime", "endTime",
            "results": [{"dashboard", "title", "status", "errorMessage",
            "nativeDashboard"}]}], "total_jobs": N}`` or an error message.
            Result ``status`` values: DASHBOARD_MIGRATION_STATE_PENDING,
            _IN_PROGRESS, _SUCCESS, _NEEDS_REVIEW, _FAILED.

    Example Usage:
        fetch_dashboard_migration_jobs(migration_job_id="job-123")

    Next Steps (using MCP-enabled tools):
        - ``get_dashboard`` (native) on ``results[].nativeDashboard``
        - ``list_dashboards`` to browse all native dashboards
    """
    try:
        logger.info(
            "Fetching dashboard migration jobs (job=%s, dashboard=%s)",
            migration_job_id,
            dashboard_id,
        )
        chronicle = get_chronicle_client(project_id, customer_id, region)
        params = {
            "migrationJobId": migration_job_id,
            "dashboard": (
                _dashboard_name(chronicle, dashboard_id)
                if dashboard_id
                else None
            ),
        }
        response = chronicle_api_request(
            chronicle,
            "GET",
            f"{_DASHBOARDS_PATH}:fetchMigrationJobs",
            params=params,
        )
        response["total_jobs"] = len(response.get("migrationJobs", []))
        return response
    except Exception as e:
        logger.error(
            "Error fetching dashboard migration jobs: %s", e, exc_info=True
        )
        return {"error": f"Error fetching dashboard migration jobs: {e}"}
