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
"""Security Operations MCP tools for native SIEM dashboard management.

Covers the Chronicle ``NativeDashboardService`` (``/nativeDashboards``),
``DashboardQueryService`` (``/dashboardQueries``) and
``DashboardChartService`` (``/dashboardCharts``) REST surfaces.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from secops_mcp.server import get_chronicle_client, server
from secops_mcp.utils import chronicle_api_request, parse_json_arg

# Configure logging
logger = logging.getLogger("secops-mcp")

_DASHBOARDS = "/nativeDashboards"
_QUERIES = "/dashboardQueries"
_CHARTS = "/dashboardCharts"


def _compact(d: Dict[str, Any]) -> Dict[str, Any]:
    """Drop ``None`` values from a JSON body."""
    return {k: v for k, v in d.items() if v is not None}


def _short_id(value: str) -> str:
    """Return the last path segment of a resource name (or the value as-is)."""
    return value.rsplit("/", 1)[-1] if "/" in value else value


def _full_name(chronicle: Any, collection: str, value: str) -> str:
    """Return a full resource name for a bare ID under ``collection``."""
    if value.startswith("projects/"):
        return value
    return f"{chronicle.instance_id}/{collection}/{_short_id(value)}"


def _query_input(
    time_unit: Optional[str],
    start_time_val: Optional[int],
    start_time: Optional[str],
    end_time: Optional[str],
) -> Optional[Dict[str, Any]]:
    """Build a ``DashboardQuery.Input`` from relative or absolute time args."""
    if start_time or end_time:
        return {
            "timeWindow": _compact(
                {"startTime": start_time, "endTime": end_time}
            )
        }
    if time_unit or start_time_val is not None:
        return {
            "relativeTime": _compact(
                {"timeUnit": time_unit, "startTimeVal": start_time_val}
            )
        }
    return None


@server.tool()
async def list_dashboards(
    view: Optional[str] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List native SIEM dashboards in the Chronicle instance.

    Returns curated (out-of-the-box) and custom dashboards with their names,
    display names, type, access and timestamps. Use the FULL view to include
    each dashboard's definition (filters and chart layout).

    **Workflow Integration:**
    - Start here to discover dashboard IDs before get/update/export calls.
    - Pair with `list_dashboard_charts` to inventory charts per dashboard.

    **Use Cases:**
    - Inventory dashboards and find curated templates to duplicate
    - Audit which dashboards are public versus private

    Args:
        view (Optional[str]): NATIVE_DASHBOARD_VIEW_BASIC (default) or
            NATIVE_DASHBOARD_VIEW_FULL (includes `definition`).
        page_size (Optional[int]): Maximum dashboards per page.
        page_token (Optional[str]): `nextPageToken` from a previous call.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"nativeDashboards": [...], "nextPageToken": ...,
            "total_dashboards": N}` or `{"error": ...}`.

    Example Usage:
        list_dashboards(view="NATIVE_DASHBOARD_VIEW_FULL", page_size=50)

    Next Steps (using MCP-enabled tools):
        - `get_dashboard` for the full definition of one dashboard
        - `duplicate_dashboard` to clone a curated dashboard for editing
    """
    try:
        logger.info("Listing native dashboards (view=%s)", view)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "GET",
            _DASHBOARDS,
            params={"pageSize": page_size, "pageToken": page_token, "view": view},
        )
        result["total_dashboards"] = len(result.get("nativeDashboards", []))
        return result
    except Exception as e:
        logger.error("Error listing dashboards: %s", e, exc_info=True)
        return {"error": f"Error listing dashboards: {e}"}


@server.tool()
async def get_dashboard(
    dashboard_id: str,
    view: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a native SIEM dashboard by ID or resource name.

    Returns the dashboard metadata and, with the FULL view, its `definition`
    containing `filters` and `charts` (each with `dashboardChart` reference
    and `chartLayout`).

    **Workflow Integration:**
    - Read the definition before `update_dashboard` or `edit_dashboard_chart`.
    - Resolve chart resource names to pass to `get_dashboard_chart`.

    **Use Cases:**
    - Inspect dashboard layout and filters
    - Verify the state after add/remove chart operations

    Args:
        dashboard_id (str): Dashboard ID or full resource name
            (`projects/.../nativeDashboards/{id}`).
        view (Optional[str]): NATIVE_DASHBOARD_VIEW_BASIC or
            NATIVE_DASHBOARD_VIEW_FULL.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The NativeDashboard resource or `{"error": ...}`.

    Example Usage:
        get_dashboard("a1b2c3d4-...", view="NATIVE_DASHBOARD_VIEW_FULL")

    Next Steps (using MCP-enabled tools):
        - `batch_get_dashboard_charts` for all charts referenced in `definition`
        - `execute_dashboard_query` to re-run a chart's query ad hoc
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Getting dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle,
            "GET",
            f"{_DASHBOARDS}/{dashboard_id}",
            params={"view": view},
        )
    except Exception as e:
        logger.error("Error getting dashboard %s: %s", dashboard_id, e, exc_info=True)
        return {"error": f"Error getting dashboard: {e}"}


@server.tool()
async def create_dashboard(
    display_name: str,
    description: Optional[str] = None,
    access_type: str = "DASHBOARD_PRIVATE",
    filters: Optional[Union[List[Dict[str, Any]], str]] = None,
    dashboard: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new (empty) native SIEM dashboard.

    Creates the dashboard shell; add charts afterwards with
    `add_dashboard_chart`. Dashboard-level filters can be supplied at
    creation time or later via `update_dashboard`.

    **Workflow Integration:**
    - First step of building a custom dashboard from scratch.
    - Use `duplicate_dashboard` instead when starting from a curated one.

    **Use Cases:**
    - Build a team-specific dashboard for a detection coverage review
    - Script dashboard provisioning across tenants

    Args:
        display_name (str): Title shown to users.
        description (Optional[str]): Free-text description.
        access_type (str): DASHBOARD_PRIVATE (default) or DASHBOARD_PUBLIC;
            the API rejects requests without it.
        filters (Optional[Union[List[Dict], str]]): DashboardFilter list placed
            under `definition.filters`, e.g.
            `[{"id": "f1", "displayName": "Hostname", "dataSource": "EVENTS",
              "fieldPath": "principal.hostname",
              "filterOperatorAndFieldValues": [{"filterOperator": "EQUAL",
              "fieldValues": ["host-1"]}]}]`.
        dashboard (Optional[Union[Dict, str]]): Additional NativeDashboard
            fields (camelCase) merged over the generated body, e.g.
            `{"definition": {...}}`.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The created NativeDashboard (with `name`) or
            `{"error": ...}`.

    Example Usage:
        create_dashboard("Phishing Overview", access_type="DASHBOARD_PUBLIC")

    Next Steps (using MCP-enabled tools):
        - `add_dashboard_chart` to populate the dashboard
        - `get_dashboard` to confirm the result
    """
    try:
        logger.info("Creating dashboard %s", display_name)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        filters = parse_json_arg(filters, "filters")
        extra = parse_json_arg(dashboard, "dashboard") or {}
        body: Dict[str, Any] = _compact(
            {
                "displayName": display_name,
                "description": description,
                "access": access_type,
                "type": "CUSTOM",
                "definition": {"filters": filters} if filters else None,
            }
        )
        body.update(extra)
        return chronicle_api_request(chronicle, "POST", _DASHBOARDS, json_body=body)
    except Exception as e:
        logger.error("Error creating dashboard: %s", e, exc_info=True)
        return {"error": f"Error creating dashboard: {e}"}


@server.tool()
async def update_dashboard(
    dashboard_id: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    filters: Optional[Union[List[Dict[str, Any]], str]] = None,
    dashboard: Optional[Union[Dict[str, Any], str]] = None,
    update_mask: Optional[str] = None,
    etag: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update fields of a native SIEM dashboard (PATCH with update mask).

    The update mask is derived from the convenience arguments supplied
    (`displayName`, `description`, `definition.filters`). Pass `dashboard`
    plus `update_mask` for any other field, e.g. chart layout changes under
    `definition.charts`.

    **Workflow Integration:**
    - Rename or re-describe dashboards after `create_dashboard`.
    - Change dashboard-level filters without touching charts.

    **Use Cases:**
    - Add a mandatory time-range filter to a dashboard
    - Rearrange chart layout by patching `definition.charts`

    Args:
        dashboard_id (str): Dashboard ID or full resource name.
        display_name (Optional[str]): New title.
        description (Optional[str]): New description.
        filters (Optional[Union[List[Dict], str]]): Replacement DashboardFilter
            list for `definition.filters`.
        dashboard (Optional[Union[Dict, str]]): Raw NativeDashboard fields
            (camelCase) merged over the generated body.
        update_mask (Optional[str]): Comma-separated camelCase field paths
            (e.g. "displayName,definition.charts"). Merged with the
            auto-derived mask.
        etag (Optional[str]): Optimistic-concurrency etag from `get_dashboard`.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The updated NativeDashboard or `{"error": ...}`.

    Example Usage:
        update_dashboard("a1b2...", display_name="SOC Overview v2")

    Next Steps (using MCP-enabled tools):
        - `get_dashboard` with the FULL view to confirm changes
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Updating dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        filters = parse_json_arg(filters, "filters")
        extra = parse_json_arg(dashboard, "dashboard") or {}
        body: Dict[str, Any] = _compact(
            {
                "displayName": display_name,
                "description": description,
                "etag": etag,
                "definition": {"filters": filters} if filters is not None else None,
            }
        )
        body.update(extra)
        mask_parts: List[str] = []
        if display_name is not None:
            mask_parts.append("displayName")
        if description is not None:
            mask_parts.append("description")
        if filters is not None:
            mask_parts.append("definition.filters")
        if update_mask:
            mask_parts.extend(p.strip() for p in update_mask.split(",") if p.strip())
        if not mask_parts:
            return {"error": "update_dashboard requires at least one field to update"}
        mask = ",".join(dict.fromkeys(mask_parts))
        return chronicle_api_request(
            chronicle,
            "PATCH",
            f"{_DASHBOARDS}/{dashboard_id}",
            params={"updateMask": mask},
            json_body=body,
        )
    except Exception as e:
        logger.error("Error updating dashboard %s: %s", dashboard_id, e, exc_info=True)
        return {"error": f"Error updating dashboard: {e}"}


@server.tool()
async def duplicate_dashboard(
    dashboard_id: str,
    display_name: str,
    description: Optional[str] = None,
    access_type: str = "DASHBOARD_PRIVATE",
    dashboard: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Duplicate a native SIEM dashboard (including its charts and queries).

    Copies an existing dashboard, typically a curated one, into a new custom
    dashboard that can be edited freely.

    **Workflow Integration:**
    - Preferred way to customize an out-of-the-box dashboard.
    - Follow with `add_dashboard_chart` / `edit_dashboard_chart`.

    **Use Cases:**
    - Clone the curated "Main Dashboard" and tailor it for a customer
    - Snapshot a dashboard before making large edits

    Args:
        dashboard_id (str): Source dashboard ID or full resource name.
        display_name (str): Title for the copy.
        description (Optional[str]): Description for the copy.
        access_type (str): DASHBOARD_PRIVATE (default) or DASHBOARD_PUBLIC;
            the API rejects requests without it.
        dashboard (Optional[Union[Dict, str]]): Extra NativeDashboard fields
            (camelCase) merged into the `nativeDashboard` body.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The new NativeDashboard or `{"error": ...}`.

    Example Usage:
        duplicate_dashboard("curated-id", display_name="My Main Dashboard")

    Next Steps (using MCP-enabled tools):
        - `list_dashboard_charts` filtered to the new dashboard
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Duplicating dashboard %s as %s", dashboard_id, display_name)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        extra = parse_json_arg(dashboard, "dashboard") or {}
        native = _compact(
            {
                "displayName": display_name,
                "description": description,
                "access": access_type,
                "type": "CUSTOM",
            }
        )
        native.update(extra)
        return chronicle_api_request(
            chronicle,
            "POST",
            f"{_DASHBOARDS}/{dashboard_id}:duplicate",
            json_body={"nativeDashboard": native},
        )
    except Exception as e:
        logger.error(
            "Error duplicating dashboard %s: %s", dashboard_id, e, exc_info=True
        )
        return {"error": f"Error duplicating dashboard: {e}"}


@server.tool()
async def delete_dashboard(
    dashboard_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a custom native SIEM dashboard.

    Permanently removes the dashboard. Curated dashboards cannot be deleted.

    **Workflow Integration:**
    - Clean up after `duplicate_dashboard` experiments or `import_dashboards`.

    **Use Cases:**
    - Remove obsolete or duplicate dashboards

    Args:
        dashboard_id (str): Dashboard ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"status": "deleted", "dashboard_id": ...}` or
            `{"error": ...}`.

    Example Usage:
        delete_dashboard("a1b2c3d4-...")

    Next Steps (using MCP-enabled tools):
        - `list_dashboards` to confirm removal
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Deleting dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle, "DELETE", f"{_DASHBOARDS}/{dashboard_id}"
        )
        return {"status": "deleted", "dashboard_id": dashboard_id, "response": result}
    except Exception as e:
        logger.error("Error deleting dashboard %s: %s", dashboard_id, e, exc_info=True)
        return {"error": f"Error deleting dashboard: {e}"}


@server.tool()
async def add_dashboard_chart(
    dashboard_id: str,
    display_name: str,
    query: Optional[str] = None,
    time_unit: Optional[str] = None,
    start_time_val: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    visualization: Optional[Union[Dict[str, Any], str]] = None,
    description: Optional[str] = None,
    tile_type: Optional[str] = None,
    start_x: Optional[int] = None,
    start_y: Optional[int] = None,
    span_x: Optional[int] = None,
    span_y: Optional[int] = None,
    data_sources: Optional[Union[List[str], str]] = None,
    chart: Optional[Union[Dict[str, Any], str]] = None,
    dashboard_query: Optional[Union[Dict[str, Any], str]] = None,
    chart_layout: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Add a chart (and its UDM stats query) to a native SIEM dashboard.

    Builds an `AddChartRequest` with `dashboardChart`, `dashboardQuery` and
    `chartLayout`. Validate the query first with `execute_dashboard_query`.

    **Workflow Integration:**
    - Follows `create_dashboard` / `duplicate_dashboard`.
    - Layout defaults to `startX=0, startY=0, spanX=48, spanY=26` (curated
      charts use spans like 45x26; the API accepts spanX up to 96). `startX`
      and `startY` are always sent because the API rejects layouts without
      them.

    **Use Cases:**
    - Add a "Top alerting rules" table to a SOC overview dashboard
    - Add a markdown or button tile (`tile_type`, no query)

    Args:
        dashboard_id (str): Target dashboard ID or full resource name.
        display_name (str): Chart title.
        query (Optional[str]): YARA-L 2.0 UDM stats query, e.g.
            `metadata.event_type = "USER_LOGIN" match: principal.user.userid
            outcome: $count = count(metadata.id) order: $count desc`.
        time_unit (Optional[str]): Relative window unit: SECOND, MINUTE, HOUR,
            DAY, WEEK, MONTH, YEAR (default DAY when a query is given).
        start_time_val (Optional[int]): Relative window length (default 1).
        start_time (Optional[str]): Absolute window start (RFC 3339); with
            `end_time` replaces the relative window.
        end_time (Optional[str]): Absolute window end (RFC 3339).
        visualization (Optional[Union[Dict, str]]): DashboardChart
            `visualization` config (ECharts-style), e.g.
            `{"series": [{"chartType": "TABLE"}]}`.
        description (Optional[str]): Chart description.
        tile_type (Optional[str]): TILE_TYPE_VISUALIZATION (default),
            TILE_TYPE_BUTTON or TILE_TYPE_MARKDOWN.
        start_x, start_y, span_x, span_y (Optional[int]): Grid layout.
        data_sources (Optional[Union[List[str], str]]): `chartDatasource.
            dataSources` for query-backed charts; defaults to `["UDM"]`
            when a query is given (the API rejects charts without it).
        chart (Optional[Union[Dict, str]]): Raw DashboardChart fields merged
            over the generated `dashboardChart`.
        dashboard_query (Optional[Union[Dict, str]]): Raw DashboardQuery
            fields merged over the generated `dashboardQuery`.
        chart_layout (Optional[Union[Dict, str]]): Raw ChartLayout
            (`{"startX":0,"startY":0,"spanX":48,"spanY":26}`).
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"nativeDashboard": {...}, "dashboardChart": {...}}`
            or `{"error": ...}`.

    Example Usage:
        add_dashboard_chart("a1b2...", "Logins by user",
            query='metadata.event_type = "USER_LOGIN" match: principal.user.userid outcome: $c = count(metadata.id)',
            time_unit="DAY", start_time_val=7, visualization={"series": [{"chartType": "TABLE"}]})

    Next Steps (using MCP-enabled tools):
        - `get_dashboard_chart` on the returned chart name
        - `edit_dashboard_chart` to tweak the query or visualization
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Adding chart %s to dashboard %s", display_name, dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        chart_extra = parse_json_arg(chart, "chart") or {}
        query_extra = parse_json_arg(dashboard_query, "dashboard_query") or {}
        layout_extra = parse_json_arg(chart_layout, "chart_layout") or {}
        visualization = parse_json_arg(visualization, "visualization")

        chart_body: Dict[str, Any] = _compact(
            {
                "displayName": display_name,
                "description": description,
                "tileType": tile_type,
                "visualization": visualization,
            }
        )
        chart_body.update(chart_extra)
        data_sources = parse_json_arg(data_sources, "data_sources")
        if (query or query_extra or data_sources) and "chartDatasource" not in chart_body:
            chart_body["chartDatasource"] = {"dataSources": data_sources or ["UDM"]}

        query_body: Optional[Dict[str, Any]] = None
        if query or query_extra:
            if query and not (time_unit or start_time_val is not None or start_time):
                time_unit, start_time_val = "DAY", 1
            query_body = _compact(
                {
                    "query": query,
                    "input": _query_input(
                        time_unit, start_time_val, start_time, end_time
                    ),
                }
            )
            query_body.update(query_extra)

        layout: Dict[str, Any] = {
            "startX": start_x if start_x is not None else 0,
            "startY": start_y if start_y is not None else 0,
            "spanX": span_x if span_x is not None else 48,
            "spanY": span_y if span_y is not None else 26,
        }
        layout.update(layout_extra)

        body = _compact(
            {
                "dashboardChart": chart_body,
                "dashboardQuery": query_body,
                "chartLayout": layout,
            }
        )
        return chronicle_api_request(
            chronicle, "POST", f"{_DASHBOARDS}/{dashboard_id}:addChart", json_body=body
        )
    except Exception as e:
        logger.error(
            "Error adding chart to dashboard %s: %s", dashboard_id, e, exc_info=True
        )
        return {"error": f"Error adding dashboard chart: {e}"}


@server.tool()
async def edit_dashboard_chart(
    dashboard_id: str,
    chart_id: str,
    edit_mask: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    query: Optional[str] = None,
    time_unit: Optional[str] = None,
    start_time_val: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    visualization: Optional[Union[Dict[str, Any], str]] = None,
    chart: Optional[Union[Dict[str, Any], str]] = None,
    dashboard_query: Optional[Union[Dict[str, Any], str]] = None,
    etag: Optional[str] = None,
    language_features: Optional[Union[List[str], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Edit an existing chart and/or its query on a native SIEM dashboard.

    Sends an `EditChartRequest`. `edit_mask` names the fields being changed,
    using camelCase `dashboardChart.*` and `dashboardQuery.*` paths. The API
    enforces optimistic concurrency: the tool fetches the chart (and, when
    the query is edited, its saved DashboardQuery) first and sends the current
    `etag` values plus the query `name`, unless you pass them in `chart` /
    `dashboard_query`.

    **Workflow Integration:**
    - Use after `get_dashboard_chart` / `get_dashboard_query` to see current
      values and the chart's `name`.

    **Use Cases:**
    - Change a chart's time window from 1 day to 7 days
    - Switch a visualization from bar to table

    Args:
        dashboard_id (str): Dashboard ID or full resource name.
        chart_id (str): Chart ID or full `dashboardCharts/{id}` name.
        edit_mask (str): Comma-separated camelCase paths, e.g.
            "dashboardChart.displayName,dashboardQuery.query,dashboardQuery.input".
        display_name (Optional[str]): New chart title.
        description (Optional[str]): New chart description.
        query (Optional[str]): New YARA-L 2.0 stats query.
        time_unit (Optional[str]): Relative window unit (SECOND..YEAR).
        start_time_val (Optional[int]): Relative window length.
        start_time (Optional[str]): Absolute window start (RFC 3339).
        end_time (Optional[str]): Absolute window end (RFC 3339).
        visualization (Optional[Union[Dict, str]]): New `visualization`.
        chart (Optional[Union[Dict, str]]): Raw DashboardChart fields merged
            over the generated `dashboardChart` (`name` and `etag` are set
            automatically from the current chart).
        dashboard_query (Optional[Union[Dict, str]]): Raw DashboardQuery
            fields merged over the generated `dashboardQuery` (`name` is set
            automatically from `chartDatasource.dashboardQuery`).
        etag (Optional[str]): Current chart etag; fetched automatically when
            omitted.
        language_features (Optional[Union[List[str], str]]): JOINS, STAGES,
            DATA_TABLES used by the query.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"nativeDashboard": {...}, "dashboardChart": {...}}`
            or `{"error": ...}`.

    Example Usage:
        edit_dashboard_chart("dash-id", "chart-id",
            edit_mask="dashboardQuery.input", time_unit="DAY", start_time_val=7)

    Next Steps (using MCP-enabled tools):
        - `execute_dashboard_query` to preview the new results
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Editing chart %s on dashboard %s", chart_id, dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        chart_extra = parse_json_arg(chart, "chart") or {}
        query_extra = parse_json_arg(dashboard_query, "dashboard_query") or {}
        visualization = parse_json_arg(visualization, "visualization")
        language_features = parse_json_arg(language_features, "language_features")
        chart_name = _full_name(chronicle, "dashboardCharts", chart_id)

        current: Dict[str, Any] = {}
        if not (etag or chart_extra.get("etag")) or (
            (query or query_extra) and not query_extra.get("name")
        ):
            current = chronicle_api_request(
                chronicle, "GET", f"{_CHARTS}/{_short_id(chart_id)}"
            )

        chart_body: Dict[str, Any] = _compact(
            {
                "name": chart_name,
                "displayName": display_name,
                "description": description,
                "visualization": visualization,
                "etag": etag or current.get("etag"),
            }
        )
        chart_body.update(chart_extra)

        query_body: Dict[str, Any] = _compact(
            {
                "name": (current.get("chartDatasource") or {}).get("dashboardQuery"),
                "query": query,
                "input": _query_input(time_unit, start_time_val, start_time, end_time),
            }
        )
        query_body.update(query_extra)
        if list(query_body) == ["name"]:
            query_body = {}
        elif query_body and query_body.get("name") and not query_body.get("etag"):
            saved_query = chronicle_api_request(
                chronicle, "GET", f"{_QUERIES}/{_short_id(query_body['name'])}"
            )
            if saved_query.get("etag"):
                query_body["etag"] = saved_query["etag"]

        body = _compact(
            {
                "dashboardChart": chart_body,
                "dashboardQuery": query_body or None,
                "editMask": edit_mask,
                "languageFeatures": language_features,
            }
        )
        return chronicle_api_request(
            chronicle, "POST", f"{_DASHBOARDS}/{dashboard_id}:editChart", json_body=body
        )
    except Exception as e:
        logger.error(
            "Error editing chart %s on dashboard %s: %s",
            chart_id,
            dashboard_id,
            e,
            exc_info=True,
        )
        return {"error": f"Error editing dashboard chart: {e}"}


@server.tool()
async def remove_dashboard_chart(
    dashboard_id: str,
    chart_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Remove a chart from a native SIEM dashboard.

    Sends `:removeChart` with the chart resource name; the chart and its
    query are detached from the dashboard.

    **Workflow Integration:**
    - Use `get_dashboard` (FULL view) to find chart names first.

    **Use Cases:**
    - Prune unused or broken charts from a dashboard

    Args:
        dashboard_id (str): Dashboard ID or full resource name.
        chart_id (str): Chart ID or full `dashboardCharts/{id}` name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The updated NativeDashboard or `{"error": ...}`.

    Example Usage:
        remove_dashboard_chart("dash-id", "chart-id")

    Next Steps (using MCP-enabled tools):
        - `get_dashboard` to verify the layout
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Removing chart %s from dashboard %s", chart_id, dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = {"dashboardChart": _full_name(chronicle, "dashboardCharts", chart_id)}
        return chronicle_api_request(
            chronicle,
            "POST",
            f"{_DASHBOARDS}/{dashboard_id}:removeChart",
            json_body=body,
        )
    except Exception as e:
        logger.error(
            "Error removing chart %s from dashboard %s: %s",
            chart_id,
            dashboard_id,
            e,
            exc_info=True,
        )
        return {"error": f"Error removing dashboard chart: {e}"}


@server.tool()
async def duplicate_dashboard_chart(
    dashboard_id: str,
    chart_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Duplicate a chart within a native SIEM dashboard.

    Sends `:duplicateChart`; the copy (chart plus query) is appended to the
    same dashboard.

    **Workflow Integration:**
    - Clone a chart, then `edit_dashboard_chart` the copy with a variant query.

    **Use Cases:**
    - Create per-environment variants of the same visualization

    Args:
        dashboard_id (str): Dashboard ID or full resource name.
        chart_id (str): Chart ID or full `dashboardCharts/{id}` name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"nativeDashboard": {...}, "dashboardChart": {...}}`
            (the new chart) or `{"error": ...}`.

    Example Usage:
        duplicate_dashboard_chart("dash-id", "chart-id")

    Next Steps (using MCP-enabled tools):
        - `edit_dashboard_chart` on the returned `dashboardChart.name`
    """
    try:
        dashboard_id = _short_id(dashboard_id)
        logger.info("Duplicating chart %s on dashboard %s", chart_id, dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = {"dashboardChart": _full_name(chronicle, "dashboardCharts", chart_id)}
        return chronicle_api_request(
            chronicle,
            "POST",
            f"{_DASHBOARDS}/{dashboard_id}:duplicateChart",
            json_body=body,
        )
    except Exception as e:
        logger.error(
            "Error duplicating chart %s on dashboard %s: %s",
            chart_id,
            dashboard_id,
            e,
            exc_info=True,
        )
        return {"error": f"Error duplicating dashboard chart: {e}"}


@server.tool()
async def export_dashboards(
    dashboard_ids: Union[List[str], str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Export native SIEM dashboards (with charts and queries) as JSON.

    Returns an inline export (`inlineDestination.dashboards[]`, each holding
    `dashboard`, `dashboardCharts` and `dashboardQueries`) that can be fed to
    `import_dashboards` in another tenant.

    **Workflow Integration:**
    - Back up dashboards before edits; migrate dashboards between tenants.

    **Use Cases:**
    - Version-control dashboard definitions
    - Promote a dashboard from a lab tenant to production

    Args:
        dashboard_ids (Union[List[str], str]): One or more dashboard IDs or
            full resource names. A JSON-array string is accepted.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"inlineDestination": {"dashboards": [...]}}` or
            `{"error": ...}`.

    Example Usage:
        export_dashboards(["dash-1", "dash-2"])

    Next Steps (using MCP-enabled tools):
        - `import_dashboards` with `inlineDestination.dashboards`
    """
    try:
        logger.info("Exporting dashboards")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        if isinstance(dashboard_ids, str) and not dashboard_ids.lstrip().startswith("["):
            ids: List[str] = [dashboard_ids]
        else:
            ids = parse_json_arg(dashboard_ids, "dashboard_ids") or []
        names = [_full_name(chronicle, "nativeDashboards", i) for i in ids]
        return chronicle_api_request(
            chronicle, "POST", f"{_DASHBOARDS}:export", json_body={"names": names}
        )
    except Exception as e:
        logger.error("Error exporting dashboards: %s", e, exc_info=True)
        return {"error": f"Error exporting dashboards: {e}"}


@server.tool()
async def import_dashboards(
    dashboards: Union[List[Dict[str, Any]], Dict[str, Any], str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Import native SIEM dashboards from an inline export payload.

    Accepts the `dashboards` array produced by `export_dashboards` (items of
    `{"dashboard": {...}, "dashboardCharts": [...], "dashboardQueries": [...]}`).
    Send the export payload unmodified: the API requires `dashboard.name`
    and `dashboard.etag` to be present and assigns a new ID on import. Each
    `results[]` entry carries the new dashboard resource name and a status.

    **Workflow Integration:**
    - Second half of an export/import migration between tenants.

    **Use Cases:**
    - Restore dashboards from backup
    - Deploy a standard dashboard set to a new tenant

    Args:
        dashboards (Union[List[Dict], Dict, str]): Either the list of
            NativeDashboardWithChartsAndQueries items, a single item, or the
            full `export_dashboards` response. JSON strings are accepted.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"results": [{"dashboard": "projects/.../nativeDashboards/<new-id>",
            "status": {"message": "Dashboard Imported Successfully"}}]}` or
            `{"error": ...}`.

    Example Usage:
        import_dashboards(export_result["inlineDestination"]["dashboards"])

    Next Steps (using MCP-enabled tools):
        - `list_dashboards` to find the imported dashboards
    """
    try:
        logger.info("Importing dashboards")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        payload = parse_json_arg(dashboards, "dashboards")
        if isinstance(payload, dict):
            if "inlineDestination" in payload:
                payload = payload["inlineDestination"].get("dashboards", [])
            elif "dashboards" in payload:
                payload = payload["dashboards"]
            else:
                payload = [payload]
        if not payload:
            return {"error": "import_dashboards requires at least one dashboard"}
        body = {"source": {"dashboards": payload}}
        return chronicle_api_request(
            chronicle, "POST", f"{_DASHBOARDS}:import", json_body=body
        )
    except Exception as e:
        logger.error("Error importing dashboards: %s", e, exc_info=True)
        return {"error": f"Error importing dashboards: {e}"}


@server.tool()
async def execute_dashboard_query(
    query: Optional[str] = None,
    time_unit: Optional[str] = None,
    start_time_val: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    query_id: Optional[str] = None,
    dialect: Optional[str] = None,
    filters: Optional[Union[List[Dict[str, Any]], str]] = None,
    clear_cache: Optional[bool] = None,
    use_previous_time_range: Optional[bool] = None,
    dashboard_query: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute a dashboard (UDM stats) query ad hoc and return tabular results.

    Runs the same engine that powers dashboard charts, without saving
    anything. Provide either an inline `query` or the `query_id` of a saved
    DashboardQuery. Defaults to the past 1 DAY when no window is given.

    **Workflow Integration:**
    - Validate a query before `add_dashboard_chart` / `edit_dashboard_chart`.
    - Re-run a chart's query with different filters for investigation.

    **Use Cases:**
    - Quick aggregation such as top hosts by alert count
    - Preview what a chart will render

    Args:
        query (Optional[str]): YARA-L 2.0 stats query (`match:` / `outcome:`
            sections) or SQL when `dialect="SQL"`.
        time_unit (Optional[str]): SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, YEAR.
        start_time_val (Optional[int]): Relative window length (e.g. 7).
        start_time (Optional[str]): Absolute window start (RFC 3339); with
            `end_time` replaces the relative window.
        end_time (Optional[str]): Absolute window end (RFC 3339).
        query_id (Optional[str]): Saved DashboardQuery ID or resource name to
            execute instead of an inline query.
        dialect (Optional[str]): YL2 (default) or SQL.
        filters (Optional[Union[List[Dict], str]]): DashboardFilter list, e.g.
            `[{"fieldPath": "principal.hostname", "dataSource": "EVENTS",
              "filterOperatorAndFieldValues": [{"filterOperator": "EQUAL",
              "fieldValues": ["host-1"]}]}]`.
        clear_cache (Optional[bool]): Bypass the result cache.
        use_previous_time_range (Optional[bool]): Run against the preceding
            window of the same length (for comparisons).
        dashboard_query (Optional[Union[Dict, str]]): Raw DashboardQuery
            fields merged over the generated `query` object.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"results": [{"column": ..., "values": [...]}],
            "timeWindow": {...}, "queryRuntimeErrors": [...]}` or `{"error": ...}`.

    Example Usage:
        execute_dashboard_query(
            query='metadata.event_type = "NETWORK_CONNECTION" match: principal.hostname outcome: $c = count(metadata.id) order: $c desc limit: 10',
            time_unit="DAY", start_time_val=7)

    Next Steps (using MCP-enabled tools):
        - `add_dashboard_chart` with the validated query
        - `search_security_events` to drill into underlying events
    """
    try:
        logger.info("Executing dashboard query")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        filters = parse_json_arg(filters, "filters")
        query_extra = parse_json_arg(dashboard_query, "dashboard_query") or {}
        if not (time_unit or start_time_val is not None or start_time or query_extra.get("input")):
            time_unit, start_time_val = "DAY", 1
        query_obj: Dict[str, Any] = _compact(
            {
                "name": _full_name(chronicle, "dashboardQueries", query_id)
                if query_id
                else None,
                "query": query,
                "input": _query_input(time_unit, start_time_val, start_time, end_time),
                "dialect": dialect,
            }
        )
        query_obj.update(query_extra)
        if not (query_obj.get("query") or query_obj.get("name")):
            return {"error": "execute_dashboard_query requires `query` or `query_id`"}
        body = _compact(
            {
                "query": query_obj,
                "filters": filters,
                "clearCache": clear_cache,
                "usePreviousTimeRange": use_previous_time_range,
            }
        )
        return chronicle_api_request(
            chronicle, "POST", f"{_QUERIES}:execute", json_body=body
        )
    except Exception as e:
        logger.error("Error executing dashboard query: %s", e, exc_info=True)
        return {"error": f"Error executing dashboard query: {e}"}


@server.tool()
async def get_dashboard_query(
    query_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a saved dashboard query by ID or resource name.

    Returns the DashboardQuery (`query`, `input`, `dialect`, `dashboardChart`
    back-reference, `etag`).

    **Workflow Integration:**
    - Resolve a chart's `chartDatasource.dashboardQuery` to its query text.

    **Use Cases:**
    - Inspect the exact query behind a chart before editing it

    Args:
        query_id (str): Query ID or full `dashboardQueries/{id}` name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The DashboardQuery resource or `{"error": ...}`.

    Example Usage:
        get_dashboard_query("q-123")

    Next Steps (using MCP-enabled tools):
        - `execute_dashboard_query` with `query_id` to run it
    """
    try:
        query_id = _short_id(query_id)
        logger.info("Getting dashboard query %s", query_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(chronicle, "GET", f"{_QUERIES}/{query_id}")
    except Exception as e:
        logger.error("Error getting dashboard query %s: %s", query_id, e, exc_info=True)
        return {"error": f"Error getting dashboard query: {e}"}


@server.tool()
async def get_dashboard_chart(
    chart_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a dashboard chart by ID or resource name.

    Returns the DashboardChart (`displayName`, `tileType`, `chartDatasource`
    with the query reference, `visualization`, `nativeDashboard` owner).

    **Workflow Integration:**
    - Inspect a chart before `edit_dashboard_chart`.

    **Use Cases:**
    - Read a chart's visualization config to replicate it elsewhere

    Args:
        chart_id (str): Chart ID or full `dashboardCharts/{id}` name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The DashboardChart resource or `{"error": ...}`.

    Example Usage:
        get_dashboard_chart("chart-123")

    Next Steps (using MCP-enabled tools):
        - `get_dashboard_query` on `chartDatasource.dashboardQuery`
    """
    try:
        chart_id = _short_id(chart_id)
        logger.info("Getting dashboard chart %s", chart_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(chronicle, "GET", f"{_CHARTS}/{chart_id}")
    except Exception as e:
        logger.error("Error getting dashboard chart %s: %s", chart_id, e, exc_info=True)
        return {"error": f"Error getting dashboard chart: {e}"}


@server.tool()
async def list_dashboard_charts(
    filter: Optional[str] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List dashboard charts in the instance (v1alpha only).

    Returns `dashboardCharts`, `nextPageToken` and `totalSize`. Default page
    size is 100 (max 1000).

    **Workflow Integration:**
    - Inventory charts across dashboards, or find charts by display name.

    **Use Cases:**
    - Find every chart that belongs to a given dashboard
    - Locate charts by title for bulk edits

    Args:
        filter (Optional[str]): Server-side filter expression (e.g.
            `native_dashboard = "projects/.../nativeDashboards/{id}"`).
        page_size (Optional[int]): Maximum charts per page (<= 1000).
        page_token (Optional[str]): `nextPageToken` from a previous call.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"dashboardCharts": [...], "nextPageToken": ...,
            "totalSize": N, "total_charts": N}` or `{"error": ...}`.

    Example Usage:
        list_dashboard_charts(page_size=200)

    Next Steps (using MCP-enabled tools):
        - `get_dashboard_chart` for full chart details
    """
    try:
        logger.info("Listing dashboard charts (filter=%s)", filter)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "GET",
            _CHARTS,
            params={"pageSize": page_size, "pageToken": page_token, "filter": filter},
        )
        result["total_charts"] = len(result.get("dashboardCharts", []))
        return result
    except Exception as e:
        logger.error("Error listing dashboard charts: %s", e, exc_info=True)
        return {"error": f"Error listing dashboard charts: {e}"}


@server.tool()
async def batch_get_dashboard_charts(
    chart_ids: Union[List[str], str],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get several dashboard charts in one call.

    Sends `GET /dashboardCharts:batchGet` with repeated `names` query
    parameters. Handy after `get_dashboard` (FULL view), whose
    `definition.charts[].dashboardChart` lists the chart resource names.

    **Workflow Integration:**
    - Fetch all charts of a dashboard in a single request.

    **Use Cases:**
    - Render or audit a whole dashboard's chart configs at once

    Args:
        chart_ids (Union[List[str], str]): Chart IDs or full resource names.
            A JSON-array string is accepted.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"dashboardCharts": [...], "total_charts": N}` or
            `{"error": ...}`.

    Example Usage:
        batch_get_dashboard_charts(["chart-1", "chart-2"])

    Next Steps (using MCP-enabled tools):
        - `get_dashboard_query` for each `chartDatasource.dashboardQuery`
    """
    try:
        logger.info("Batch getting dashboard charts")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        if isinstance(chart_ids, str) and not chart_ids.lstrip().startswith("["):
            ids: List[str] = [chart_ids]
        else:
            ids = parse_json_arg(chart_ids, "chart_ids") or []
        names = [_full_name(chronicle, "dashboardCharts", i) for i in ids]
        result = chronicle_api_request(
            chronicle, "GET", f"{_CHARTS}:batchGet", params={"names": names}
        )
        result["total_charts"] = len(result.get("dashboardCharts", []))
        return result
    except Exception as e:
        logger.error("Error batch getting dashboard charts: %s", e, exc_info=True)
        return {"error": f"Error batch getting dashboard charts: {e}"}
