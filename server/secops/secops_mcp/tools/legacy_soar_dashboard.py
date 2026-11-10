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
"""Security Operations MCP tools for legacy SOAR dashboards.

These tools wrap the ``LegacySoarDashboardService`` custom verbs
(``legacySoarDashboard:legacy*``) of the Chronicle API. The service is
v1alpha-only and proxies to the SOAR (case management) backend, so the
caller's identity must be mapped to a SOAR user. The dashboards managed here
are SOAR case/playbook dashboards, not SIEM native dashboards.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from secops_mcp.server import get_chronicle_client, server
from secops_mcp.utils import chronicle_api_request, parse_json_arg

# Configure logging
logger = logging.getLogger("secops-mcp")

_VERB_PREFIX = "legacySoarDashboard:"

# Fields the SOAR backend requires on every widget definition payload.
_WIDGET_REQUIRED_FIELDS = ("id", "dashboardId", "title", "widgetType", "widthSize")


def _compact(d: Dict[str, Any]) -> Dict[str, Any]:
    """Drop ``None`` values from a JSON body."""
    return {k: v for k, v in d.items() if v is not None}


def _verb(name: str) -> str:
    """Build the instance-level custom verb path for a legacy SOAR method."""
    return f"{_VERB_PREFIX}{name}"


def _parse_list(value: Any, name: str) -> Optional[List[Any]]:
    """Normalize a list argument that may arrive as a JSON string."""
    parsed = parse_json_arg(value, name)
    if parsed is not None and not isinstance(parsed, list):
        raise TypeError(f"{name} must be a JSON array")
    return parsed


def _parse_dict(value: Any, name: str) -> Dict[str, Any]:
    """Normalize a dict argument that may arrive as a JSON string."""
    parsed = parse_json_arg(value, name)
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise TypeError(f"{name} must be a JSON object")
    return dict(parsed)


def _widget_body(
    *,
    widget: Any,
    widget_id: Optional[int],
    dashboard_id: Optional[int],
    title: Optional[str],
    widget_type: Optional[str],
    width_size: Optional[str],
    description: Optional[str],
    order: Optional[int],
    time_filter: Optional[str],
    subject: Optional[str],
    dimension_a: Optional[str],
    dimension_b: Optional[str],
    chart_type: Optional[str],
    results_amount: Optional[int],
    results_order: Optional[str],
    calculate_field: Optional[str],
    extra_fields: Any,
) -> Dict[str, Any]:
    """Merge a widget passthrough object with explicit overrides.

    Precedence (lowest to highest): ``widget`` -> ``extra_fields`` -> explicit
    keyword arguments. Validates the fields the SOAR backend requires.
    """
    body = _parse_dict(widget, "widget")
    body.update(_parse_dict(extra_fields, "extra_fields"))
    body.update(
        _compact(
            {
                "id": widget_id,
                "dashboardId": dashboard_id,
                "title": title,
                "widgetType": widget_type,
                "widthSize": width_size,
                "description": description,
                "order": order,
                "timeFilter": time_filter,
                "subject": subject,
                "dimensionA": dimension_a,
                "dimensionB": dimension_b,
                "chartType": chart_type,
                "resultsAmount": results_amount,
                "resultsOrder": results_order,
                "calculateField": calculate_field,
            }
        )
    )
    missing = [f for f in _WIDGET_REQUIRED_FIELDS if body.get(f) in (None, "")]
    if missing:
        raise ValueError(
            "Widget definition is missing required field(s): " + ", ".join(missing)
        )
    return body


# ---------------------------------------------------------------------------
# Dashboard discovery and retrieval
# ---------------------------------------------------------------------------


@server.tool()
async def legacy_soar_get_dashboard_cards(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List legacy SOAR dashboards (ID to name map) visible to the caller.

    SOAR (case management) dashboards are served through the Chronicle API
    (v1alpha-only, legacy) and require the caller to be mapped to a SOAR user.
    This is the entry point for discovering dashboard IDs.

    **Workflow Integration:**
    - Call first to resolve a dashboard name to the numeric ID used by every
      other legacy_soar_* tool.

    **Use Cases:**
    - Inventory SOC dashboards before reporting or cleanup
    - Find the ID of the "SOC Overview" dashboard to fetch its widgets

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {"<dashboard_id>": "<name>", ...},
            "total_dashboards": N}`` or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_cards()

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard(dashboard_id=...) for widgets and config
        - legacy_soar_get_dashboard_widget_values(...) to render a widget
    """
    try:
        logger.info("Listing legacy SOAR dashboard cards")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle, "GET", _verb("legacyGetDashboardCards")
        )
        cards = result.get("payload") or {}
        return {**result, "total_dashboards": len(cards)}
    except Exception as e:
        logger.error("Error listing legacy SOAR dashboard cards: %s", e, exc_info=True)
        return {"error": f"Error listing legacy SOAR dashboard cards: {e}"}


@server.tool()
async def legacy_soar_get_dashboard(
    dashboard_id: int,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a legacy SOAR dashboard with its configuration and widgets.

    Returns the SOAR (case management) dashboard data model: name, creator,
    default time range, environments, allowed users and the full list of
    widget definitions. Served through the Chronicle API (v1alpha-only,
    legacy); requires a SOAR-mapped user identity. The API uses POST with the
    ID in the body even though this is a read.

    **Workflow Integration:**
    - Widget objects in ``payload.widgets`` can be passed as the ``widget``
      argument of legacy_soar_get_dashboard_widget_values and related tools.

    **Use Cases:**
    - Review which filters a SOC dashboard applies
    - Export a dashboard definition for legacy_soar_import_dashboard

    Args:
        dashboard_id (int): Numeric dashboard ID (from
            legacy_soar_get_dashboard_cards).
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {<LegacySoarDashboardDataModel>}}`` or
            ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard(dashboard_id=12)

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard_widget_values(widget=<a widget>)
        - legacy_soar_add_or_update_dashboard_widget(...) to modify a widget
    """
    try:
        logger.info("Getting legacy SOAR dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle,
            "POST",
            _verb("legacyGetDashboard"),
            json_body={"legacyPayload": dashboard_id},
        )
    except Exception as e:
        logger.error(
            "Error getting legacy SOAR dashboard %s: %s", dashboard_id, e, exc_info=True
        )
        return {"error": f"Error getting legacy SOAR dashboard {dashboard_id}: {e}"}


@server.tool()
async def legacy_soar_get_dashboard_widget_definitions(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List the predefined widget definitions available for SOAR dashboards.

    Returns the catalog of widget templates (SOC metrics and chart types) that
    can be placed on a legacy SOAR (case management) dashboard. Served through
    the Chronicle API (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Use before legacy_soar_add_or_update_dashboard_widget to pick a valid
      widget type, subject, dimensions and chart type.

    **Use Cases:**
    - Discover which playbook or SLA widgets exist
    - Validate a widget configuration before creating it

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": [<DashboardWidgetDefinitionDataModel>],
            "total_definitions": N}`` or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_widget_definitions()

    Next Steps (using MCP-enabled tools):
        - legacy_soar_add_or_update_dashboard_widget(...)
    """
    try:
        logger.info("Listing legacy SOAR dashboard widget definitions")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle, "GET", _verb("legacyGetDashboardWidgetDefinitions")
        )
        return {**result, "total_definitions": len(result.get("payload") or [])}
    except Exception as e:
        logger.error(
            "Error listing legacy SOAR widget definitions: %s", e, exc_info=True
        )
        return {"error": f"Error listing legacy SOAR widget definitions: {e}"}


@server.tool()
async def legacy_soar_get_dashboard_playbooks(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List SOAR playbooks that have data available for dashboard reporting.

    Served through the Chronicle API (v1alpha-only, legacy) and proxied to
    the SOAR backend; requires a SOAR-mapped user identity.

    **Workflow Integration:**
    - Use the returned playbook identifiers with
      legacy_soar_get_playbook_monitoring or as ``playbooksFilter`` values.

    **Use Cases:**
    - Find which playbooks can be monitored on a dashboard
    - Build a playbook performance report

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": [<DashboardPlaybookModel>],
            "total_playbooks": N}`` or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_playbooks()

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_playbook_monitoring(workflow_identifier=...)
    """
    try:
        logger.info("Listing legacy SOAR dashboard playbooks")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle, "GET", _verb("legacyGetDashboardPlaybooks")
        )
        return {**result, "total_playbooks": len(result.get("payload") or [])}
    except Exception as e:
        logger.error(
            "Error listing legacy SOAR dashboard playbooks: %s", e, exc_info=True
        )
        return {"error": f"Error listing legacy SOAR dashboard playbooks: {e}"}


# ---------------------------------------------------------------------------
# Dashboard mutation
# ---------------------------------------------------------------------------


@server.tool()
async def legacy_soar_add_or_update_dashboard(
    dashboard_id: int,
    name: Optional[str] = None,
    creator: Optional[str] = None,
    default_time_range: Optional[str] = None,
    environments: Optional[Union[List[str], str]] = None,
    allowed_users: Optional[Union[List[str], str]] = None,
    allowed_users_json: Optional[str] = None,
    widgets: Optional[Union[List[Dict[str, Any]], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or update a legacy SOAR (case management) dashboard.

    The dashboard is created when ``dashboard_id`` is new (use 0 for a new
    dashboard) and updated otherwise. Served through the Chronicle API
    (v1alpha-only, legacy); requires a SOAR-mapped user identity.

    **Workflow Integration:**
    - Fetch the current definition with legacy_soar_get_dashboard, modify, and
      send it back here to avoid dropping fields.

    **Use Cases:**
    - Create a new SOC overview dashboard scoped to specific environments
    - Rename a dashboard or change who can view it

    Args:
        dashboard_id (int): Dashboard ID to update, or 0 to create.
        name (Optional[str]): Dashboard display name.
        creator (Optional[str]): Creator username.
        default_time_range (Optional[str]): One of DASHBOARD_TIME_RANGE_TYPE_UNSPECIFIED, LAST_DAY, LAST_3_DAYS,
            LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS,
            LAST_YEAR.
        environments (Optional[Union[List[str], str]]): SOAR environment
            names the dashboard covers; list or JSON array string.
        allowed_users (Optional[Union[List[str], str]]): Usernames allowed to
            view the dashboard; list or JSON array string.
        allowed_users_json (Optional[str]): Legacy JSON-encoded allowed users
            string, if the backend expects it.
        widgets (Optional[Union[List[Dict], str]]): Widget definitions
            (LegacySoarDashboardWidgetDataModel, camelCase keys) as list or
            JSON array string.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: The saved dashboard (``id``, ``name``, ``creator``,
            ``widgets``, ...) or ``{"error": ...}``.

    Example Usage:
        legacy_soar_add_or_update_dashboard(dashboard_id=0, name="SOC Overview",
            default_time_range="LAST_WEEK", environments=["Default Environment"])

    Next Steps (using MCP-enabled tools):
        - legacy_soar_add_or_update_dashboard_widget(dashboard_id=<new id>, ...)
    """
    try:
        logger.info("Adding/updating legacy SOAR dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _compact(
            {
                "id": dashboard_id,
                "name": name,
                "creator": creator,
                "defaultTimeRange": default_time_range,
                "environments": _parse_list(environments, "environments"),
                "allowedUsers": _parse_list(allowed_users, "allowed_users"),
                "allowedUsersJson": allowed_users_json,
                "widgets": _parse_list(widgets, "widgets"),
            }
        )
        return chronicle_api_request(
            chronicle, "POST", _verb("legacyAddOrUpdateDashboard"), json_body=body
        )
    except Exception as e:
        logger.error(
            "Error adding/updating legacy SOAR dashboard %s: %s",
            dashboard_id,
            e,
            exc_info=True,
        )
        return {
            "error": f"Error adding/updating legacy SOAR dashboard {dashboard_id}: {e}"
        }


@server.tool()
async def legacy_soar_delete_dashboard(
    dashboard_id: int,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a legacy SOAR dashboard and all of its widgets.

    Irreversible. Served through the Chronicle API (v1alpha-only, legacy);
    requires a SOAR-mapped user with dashboard action permissions. The API
    uses POST with the ID in the body.

    **Workflow Integration:**
    - Confirm the target with legacy_soar_get_dashboard before deleting.

    **Use Cases:**
    - Remove obsolete or duplicate SOC dashboards

    Args:
        dashboard_id (int): Numeric dashboard ID to delete.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"deleted": True, "dashboard_id": ...}`` merged with
            the (normally empty) API response, or ``{"error": ...}``.

    Example Usage:
        legacy_soar_delete_dashboard(dashboard_id=12)

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard_cards() to confirm removal
    """
    try:
        logger.info("Deleting legacy SOAR dashboard %s", dashboard_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "POST",
            _verb("legacyDeleteDashboard"),
            json_body={"legacyPayload": dashboard_id},
        )
        return {**result, "deleted": True, "dashboard_id": dashboard_id}
    except Exception as e:
        logger.error(
            "Error deleting legacy SOAR dashboard %s: %s",
            dashboard_id,
            e,
            exc_info=True,
        )
        return {"error": f"Error deleting legacy SOAR dashboard {dashboard_id}: {e}"}


@server.tool()
async def legacy_soar_import_dashboard(
    dashboard: Optional[Union[Dict[str, Any], str]] = None,
    name: Optional[str] = None,
    creator: Optional[str] = None,
    default_time_range: Optional[str] = None,
    environments: Optional[Union[List[str], str]] = None,
    allowed_users: Optional[Union[List[str], str]] = None,
    widgets: Optional[Union[List[Dict[str, Any]], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Import a legacy SOAR dashboard from an exported JSON definition.

    Creates a dashboard from a definition exported from another SecOps/SOAR
    instance (or from legacy_soar_get_dashboard). Served through the Chronicle
    API (v1alpha-only, legacy); requires a SOAR-mapped user identity.

    **Workflow Integration:**
    - Pass the exported object as ``dashboard``; explicit arguments override
      individual keys (e.g. to rename on import).

    **Use Cases:**
    - Copy a dashboard between tenants
    - Restore a dashboard from a saved definition

    Args:
        dashboard (Optional[Union[Dict, str]]): Exported dashboard object with
            camelCase keys (``id``, ``name``, ``creator``, ``defaultTimeRange``,
            ``environments``, ``allowedUsers``, ``widgets``, ...). Dict or
            JSON string.
        name (Optional[str]): Override the dashboard name.
        creator (Optional[str]): Override the creator username.
        default_time_range (Optional[str]): One of DASHBOARD_TIME_RANGE_TYPE_UNSPECIFIED, LAST_DAY, LAST_3_DAYS,
            LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS,
            LAST_YEAR.
        environments (Optional[Union[List[str], str]]): Override environments.
        allowed_users (Optional[Union[List[str], str]]): Override allowed
            users.
        widgets (Optional[Union[List[Dict], str]]): Override widget list.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {<imported dashboard>}}`` or
            ``{"error": ...}``.

    Example Usage:
        legacy_soar_import_dashboard(dashboard=exported, name="SOC Overview (copy)")

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard(dashboard_id=<payload.id>)
    """
    try:
        logger.info("Importing legacy SOAR dashboard")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _parse_dict(dashboard, "dashboard")
        body.update(
            _compact(
                {
                    "name": name,
                    "creator": creator,
                    "defaultTimeRange": default_time_range,
                    "environments": _parse_list(environments, "environments"),
                    "allowedUsers": _parse_list(allowed_users, "allowed_users"),
                    "widgets": _parse_list(widgets, "widgets"),
                }
            )
        )
        if not body:
            raise ValueError("Provide a dashboard definition or at least a name")
        return chronicle_api_request(
            chronicle, "POST", _verb("legacyImportDashboard"), json_body=body
        )
    except Exception as e:
        logger.error("Error importing legacy SOAR dashboard: %s", e, exc_info=True)
        return {"error": f"Error importing legacy SOAR dashboard: {e}"}


@server.tool()
async def legacy_soar_save_dashboard_as_report_template(
    name: str,
    template_id: Optional[int] = None,
    category: Optional[str] = None,
    report_widgets: Optional[Union[List[Dict[str, Any]], str]] = None,
    is_system: Optional[bool] = None,
    has_scheduler: Optional[bool] = None,
    template: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Save a legacy SOAR dashboard's widgets as a SOAR report template.

    Turns a set of dashboard widgets into a reusable report template that can
    be rendered or scheduled from the SOAR Reports page. Served through the
    Chronicle API (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Take ``payload.widgets`` from legacy_soar_get_dashboard and pass them as
      ``report_widgets``.

    **Use Cases:**
    - Produce a weekly management report from the SOC dashboard
    - Snapshot a dashboard layout for scheduled distribution

    Args:
        name (str): Report template name.
        template_id (Optional[int]): Existing template ID to overwrite
            (``id``); omit to create.
        category (Optional[str]): ``ROI``, ``MANAGEMENT``, ``SLA``, ``TIER1``
            or ``GENERAL``.
        report_widgets (Optional[Union[List[Dict], str]]): Widget definitions
            (camelCase) as list or JSON array string.
        is_system (Optional[bool]): Mark as a system template.
        has_scheduler (Optional[bool]): Whether a schedule is attached.
        template (Optional[Union[Dict, str]]): Full request object
            (camelCase keys) used as the base; explicit arguments override.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {<ReportTemplateDetails>}}`` or
            ``{"error": ...}``.

    Example Usage:
        legacy_soar_save_dashboard_as_report_template(name="Weekly SOC",
            category="MANAGEMENT", report_widgets=dashboard["payload"]["widgets"])

    Next Steps (using MCP-enabled tools):
        - Review the template in the SOAR Reports UI
    """
    try:
        logger.info("Saving legacy SOAR dashboard as report template %s", name)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _parse_dict(template, "template")
        body.update(
            _compact(
                {
                    "id": template_id,
                    "name": name,
                    "category": category,
                    "reportWidgets": _parse_list(report_widgets, "report_widgets"),
                    "isSystem": is_system,
                    "hasScheduler": has_scheduler,
                }
            )
        )
        return chronicle_api_request(
            chronicle,
            "POST",
            _verb("legacySaveDashboardAsReportTemplate"),
            json_body=body,
        )
    except Exception as e:
        logger.error(
            "Error saving legacy SOAR dashboard as report template: %s",
            e,
            exc_info=True,
        )
        return {"error": f"Error saving legacy SOAR dashboard as report template: {e}"}


# ---------------------------------------------------------------------------
# Widget mutation
# ---------------------------------------------------------------------------


@server.tool()
async def legacy_soar_add_or_update_dashboard_widget(
    widget: Optional[Union[Dict[str, Any], str]] = None,
    widget_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
    title: Optional[str] = None,
    widget_type: Optional[str] = None,
    width_size: Optional[str] = None,
    description: Optional[str] = None,
    order: Optional[int] = None,
    time_filter: Optional[str] = None,
    subject: Optional[str] = None,
    dimension_a: Optional[str] = None,
    dimension_b: Optional[str] = None,
    chart_type: Optional[str] = None,
    results_amount: Optional[int] = None,
    results_order: Optional[str] = None,
    calculate_field: Optional[str] = None,
    extra_fields: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or update a widget on a legacy SOAR dashboard.

    Creates the widget when ``widget_id`` is new (use 0) and updates it
    otherwise. Widgets are pie/bar/table/time-series charts over SOAR cases,
    alerts, tasks or playbooks with extensive filters. Served through the
    Chronicle API (v1alpha-only, legacy); requires a SOAR-mapped user.
    Required fields: ``id``, ``dashboardId``, ``title``, ``widgetType``,
    ``widthSize``.

    **Workflow Integration:**
    - Start from a widget returned by legacy_soar_get_dashboard (pass it as
      ``widget``) and override only what changes.

    **Use Cases:**
    - Add a "Cases by priority" pie chart to a SOC dashboard
    - Change a widget's time range or analyst filter

    Args:
        widget (Optional[Union[Dict, str]]): Full widget definition (camelCase
            keys) as returned by legacy_soar_get_dashboard; dict or JSON
            string. Explicit arguments below override its keys.
        widget_id (Optional[int]): Widget ID (``id``; 0 for new).
        dashboard_id (Optional[int]): Owning dashboard ID (``dashboardId``).
        title (Optional[str]): Widget title.
        widget_type (Optional[str]): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        width_size (Optional[str]): ``ONE_BLOCK``, ``TWO_BLOCKS``,
            ``THREE_BLOCKS``.
        description (Optional[str]): Widget description.
        order (Optional[int]): Position in the dashboard.
        time_filter (Optional[str]): LAST_DAY, LAST_3_DAYS, LAST_WEEK,
            LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        subject (Optional[str]): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        dimension_a (Optional[str]): Primary grouping (CustomWidgetObjectEnum),
            e.g. ``ANALYST``, ``TAG``, ``PRIORITY``, ``RULE_NAME``,
            ``ENVIRONMENT``, ``PLAYBOOK``, ``PRODUCT``, ``CASE_STATUS``,
            ``CASE_CLOSE_REASON``, ``STAGE``, ``SLA_STATUS``, ``TASK_STATUS``,
            ``PLAYBOOK_TOTAL_RUNS``, ``CASE_OPEN_AND_CLOSURE_TRENDS``.
        dimension_b (Optional[str]): Secondary grouping, same enum.
        chart_type (Optional[str]): ``PIE``, ``HORIZENTAL_BARS``,
            ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``,
            ``SOCS_STATUS``, ``ROI``, ``TEXT``, ``IMAGE``, ``NUMBER_STATUS``.
        results_amount (Optional[int]): Max result buckets.
        results_order (Optional[str]): ``DESCENDING`` or ``ASCENDING``.
        calculate_field (Optional[str]): ``COUNT``, ``HANDLING_AVG_TIME``,
            ``SLA_AVG_REMAINING_TIME``, ``TASK_DUE_DATE_AVG_TIME``,
            ``PERCENTAGE``, ``AVG_RUNTIME``.
        extra_fields (Optional[Union[Dict, str]]): Other camelCase request
            fields, mainly list filters: ``tagFilters``, ``productFilters``,
            ``analystFilters``, ``priorityFilter`` (INFORMATIVE/LOW/MEDIUM/
            HIGH/CRITICAL), ``environmentFilter``, ``entityTypeFilter``,
            ``caseStatusesFilter`` (OPENED/CLOSED/ALL/MERGED),
            ``alertNamesFilter``, ``importanceStatusesFilter`` (bools),
            ``incidentStatusesFilter`` (bools), ``exceededSlaFilter`` (bools),
            ``closeReasonsFilter`` (MALICIOUS/NOT_MALICIOUS/MAINTENANCE/
            INCONCLUSIVE/UNKNOWN), ``caseRootCauseFilter``,
            ``caseStageFilter``, ``entityIdentifierFilter``,
            ``networksFilter``, ``portsFilter``, ``categoryOutcomeFilter``,
            ``playbooksFilter``, ``integrationsFilter``,
            ``playbookStatusFilter`` (FINISHED_SUCCESSFULLY/ERROR/
            WAITING_FOR_USER_ACTION/DECLINED/PLAYBOOK_CLOSED_ALERT/PENDING/
            TERMINATED), ``startStage``, ``endStage``, ``text``,
            ``groupByField``, ``socAnalystsLoadManagerUsername``.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {<saved widget>}}`` or ``{"error": ...}``.

    Example Usage:
        legacy_soar_add_or_update_dashboard_widget(widget_id=0, dashboard_id=12,
            title="Cases by priority", widget_type="CUSTOM", width_size="ONE_BLOCK",
            subject="CASES", dimension_a="PRIORITY", chart_type="PIE",
            time_filter="LAST_WEEK")

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard_widget_values(widget=<payload>)
    """
    try:
        logger.info(
            "Adding/updating legacy SOAR dashboard widget %s on dashboard %s",
            widget_id,
            dashboard_id,
        )
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _widget_body(
            widget=widget,
            widget_id=widget_id,
            dashboard_id=dashboard_id,
            title=title,
            widget_type=widget_type,
            width_size=width_size,
            description=description,
            order=order,
            time_filter=time_filter,
            subject=subject,
            dimension_a=dimension_a,
            dimension_b=dimension_b,
            chart_type=chart_type,
            results_amount=results_amount,
            results_order=results_order,
            calculate_field=calculate_field,
            extra_fields=extra_fields,
        )
        return chronicle_api_request(
            chronicle,
            "POST",
            _verb("legacyAddOrUpdateDashboardWidget"),
            json_body=body,
        )
    except Exception as e:
        logger.error(
            "Error adding/updating legacy SOAR dashboard widget: %s", e, exc_info=True
        )
        return {"error": f"Error adding/updating legacy SOAR dashboard widget: {e}"}


@server.tool()
async def legacy_soar_delete_dashboard_widget(
    widget_id: int,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a single widget from a legacy SOAR dashboard.

    Served through the Chronicle API (v1alpha-only, legacy); requires a
    SOAR-mapped user identity. The API uses POST with the ID in the body.

    **Workflow Integration:**
    - Find widget IDs in ``payload.widgets[].id`` from legacy_soar_get_dashboard.

    **Use Cases:**
    - Remove a stale chart from a SOC dashboard

    Args:
        widget_id (int): Numeric widget ID to delete.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"deleted": True, "widget_id": ...}`` merged with
            the API response, or ``{"error": ...}``.

    Example Usage:
        legacy_soar_delete_dashboard_widget(widget_id=345)

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard(dashboard_id=...) to confirm
    """
    try:
        logger.info("Deleting legacy SOAR dashboard widget %s", widget_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "POST",
            _verb("legacyDeleteDashboardWidget"),
            json_body={"legacyPayload": widget_id},
        )
        return {**result, "deleted": True, "widget_id": widget_id}
    except Exception as e:
        logger.error(
            "Error deleting legacy SOAR dashboard widget %s: %s",
            widget_id,
            e,
            exc_info=True,
        )
        return {
            "error": f"Error deleting legacy SOAR dashboard widget {widget_id}: {e}"
        }


# ---------------------------------------------------------------------------
# Widget data queries (all take a widget definition as the POST body)
# ---------------------------------------------------------------------------


async def _widget_query(
    verb: str,
    label: str,
    *,
    widget: Any,
    widget_id: Optional[int],
    dashboard_id: Optional[int],
    title: Optional[str],
    widget_type: Optional[str],
    width_size: Optional[str],
    description: Optional[str],
    order: Optional[int],
    time_filter: Optional[str],
    subject: Optional[str],
    dimension_a: Optional[str],
    dimension_b: Optional[str],
    chart_type: Optional[str],
    results_amount: Optional[int],
    results_order: Optional[str],
    calculate_field: Optional[str],
    extra_fields: Any,
    project_id: Optional[str],
    customer_id: Optional[str],
    region: Optional[str],
) -> Dict[str, Any]:
    """Shared body for the widget-definition driven query verbs."""
    try:
        logger.info("Getting legacy SOAR %s for widget %s", label, widget_id)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _widget_body(
            widget=widget,
            widget_id=widget_id,
            dashboard_id=dashboard_id,
            title=title,
            widget_type=widget_type,
            width_size=width_size,
            description=description,
            order=order,
            time_filter=time_filter,
            subject=subject,
            dimension_a=dimension_a,
            dimension_b=dimension_b,
            chart_type=chart_type,
            results_amount=results_amount,
            results_order=results_order,
            calculate_field=calculate_field,
            extra_fields=extra_fields,
        )
        result = chronicle_api_request(chronicle, "POST", _verb(verb), json_body=body)
        payload = result.get("payload")
        if isinstance(payload, list):
            return {**result, "total_results": len(payload)}
        return result
    except Exception as e:
        logger.error("Error getting legacy SOAR %s: %s", label, e, exc_info=True)
        return {"error": f"Error getting legacy SOAR {label}: {e}"}


@server.tool()
async def legacy_soar_get_dashboard_widget_values(
    widget: Optional[Union[Dict[str, Any], str]] = None,
    widget_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
    title: Optional[str] = None,
    widget_type: Optional[str] = None,
    width_size: Optional[str] = None,
    description: Optional[str] = None,
    order: Optional[int] = None,
    time_filter: Optional[str] = None,
    subject: Optional[str] = None,
    dimension_a: Optional[str] = None,
    dimension_b: Optional[str] = None,
    chart_type: Optional[str] = None,
    results_amount: Optional[int] = None,
    results_order: Optional[str] = None,
    calculate_field: Optional[str] = None,
    extra_fields: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Compute the data series for a legacy SOAR dashboard widget.

    Evaluates a widget definition against SOAR case/alert/playbook data and
    returns the series used to draw the chart. The widget does not have to be
    saved, so this doubles as an ad-hoc SOC metrics query. Served through the
    Chronicle API (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Pass a widget from legacy_soar_get_dashboard as ``widget``, or describe
      an ad-hoc widget with the explicit arguments.

    **Use Cases:**
    - "How many open cases per priority this week?"
    - Fetch the numbers behind a dashboard chart for a report

    Args:
        widget (Optional[Union[Dict, str]]): Full widget definition (camelCase
            keys) as returned by legacy_soar_get_dashboard; dict or JSON
            string. Explicit arguments below override its keys.
        widget_id (Optional[int]): Widget ID (``id``; 0 for new).
        dashboard_id (Optional[int]): Owning dashboard ID (``dashboardId``).
        title (Optional[str]): Widget title.
        widget_type (Optional[str]): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        width_size (Optional[str]): ``ONE_BLOCK``, ``TWO_BLOCKS``,
            ``THREE_BLOCKS``.
        description (Optional[str]): Widget description.
        order (Optional[int]): Position in the dashboard.
        time_filter (Optional[str]): LAST_DAY, LAST_3_DAYS, LAST_WEEK,
            LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        subject (Optional[str]): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        dimension_a (Optional[str]): Primary grouping (CustomWidgetObjectEnum),
            e.g. ``ANALYST``, ``TAG``, ``PRIORITY``, ``RULE_NAME``,
            ``ENVIRONMENT``, ``PLAYBOOK``, ``PRODUCT``, ``CASE_STATUS``,
            ``CASE_CLOSE_REASON``, ``STAGE``, ``SLA_STATUS``, ``TASK_STATUS``,
            ``PLAYBOOK_TOTAL_RUNS``, ``CASE_OPEN_AND_CLOSURE_TRENDS``.
        dimension_b (Optional[str]): Secondary grouping, same enum.
        chart_type (Optional[str]): ``PIE``, ``HORIZENTAL_BARS``,
            ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``,
            ``SOCS_STATUS``, ``ROI``, ``TEXT``, ``IMAGE``, ``NUMBER_STATUS``.
        results_amount (Optional[int]): Max result buckets.
        results_order (Optional[str]): ``DESCENDING`` or ``ASCENDING``.
        calculate_field (Optional[str]): ``COUNT``, ``HANDLING_AVG_TIME``,
            ``SLA_AVG_REMAINING_TIME``, ``TASK_DUE_DATE_AVG_TIME``,
            ``PERCENTAGE``, ``AVG_RUNTIME``.
        extra_fields (Optional[Union[Dict, str]]): Other camelCase request
            fields, mainly list filters: ``tagFilters``, ``productFilters``,
            ``analystFilters``, ``priorityFilter`` (INFORMATIVE/LOW/MEDIUM/
            HIGH/CRITICAL), ``environmentFilter``, ``entityTypeFilter``,
            ``caseStatusesFilter`` (OPENED/CLOSED/ALL/MERGED),
            ``alertNamesFilter``, ``importanceStatusesFilter`` (bools),
            ``incidentStatusesFilter`` (bools), ``exceededSlaFilter`` (bools),
            ``closeReasonsFilter`` (MALICIOUS/NOT_MALICIOUS/MAINTENANCE/
            INCONCLUSIVE/UNKNOWN), ``caseRootCauseFilter``,
            ``caseStageFilter``, ``entityIdentifierFilter``,
            ``networksFilter``, ``portsFilter``, ``categoryOutcomeFilter``,
            ``playbooksFilter``, ``integrationsFilter``,
            ``playbookStatusFilter`` (FINISHED_SUCCESSFULLY/ERROR/
            WAITING_FOR_USER_ACTION/DECLINED/PLAYBOOK_CLOSED_ALERT/PENDING/
            TERMINATED), ``startStage``, ``endStage``, ``text``,
            ``groupByField``, ``socAnalystsLoadManagerUsername``.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {<LegacySoarDashboardWidgetValues>}}``
            or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_widget_values(widget_id=0, dashboard_id=12,
            title="Open cases by priority", widget_type="CUSTOM",
            width_size="ONE_BLOCK", subject="CASES", dimension_a="PRIORITY",
            chart_type="PIE", time_filter="LAST_WEEK",
            extra_fields={"caseStatusesFilter": ["OPENED"]})

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard_widget_case_ids(...) to drill into cases
    """
    return await _widget_query(
        "legacyGetDashboardWidgetValues",
        "dashboard widget values",
        widget=widget,
        widget_id=widget_id,
        dashboard_id=dashboard_id,
        title=title,
        widget_type=widget_type,
        width_size=width_size,
        description=description,
        order=order,
        time_filter=time_filter,
        subject=subject,
        dimension_a=dimension_a,
        dimension_b=dimension_b,
        chart_type=chart_type,
        results_amount=results_amount,
        results_order=results_order,
        calculate_field=calculate_field,
        extra_fields=extra_fields,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
    )


@server.tool()
async def legacy_soar_get_dashboard_widget_case_ids(
    widget: Optional[Union[Dict[str, Any], str]] = None,
    widget_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
    title: Optional[str] = None,
    widget_type: Optional[str] = None,
    width_size: Optional[str] = None,
    description: Optional[str] = None,
    order: Optional[int] = None,
    time_filter: Optional[str] = None,
    subject: Optional[str] = None,
    dimension_a: Optional[str] = None,
    dimension_b: Optional[str] = None,
    chart_type: Optional[str] = None,
    results_amount: Optional[int] = None,
    results_order: Optional[str] = None,
    calculate_field: Optional[str] = None,
    extra_fields: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List the SOAR case IDs behind a legacy dashboard widget.

    Drill-down from a dashboard metric to the underlying cases. Served through
    the Chronicle API (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Use the returned IDs with SOAR case tools (get_case_full_details, etc.).

    **Use Cases:**
    - Find which cases make up the "exceeded SLA" count
    - Build a case list for a specific analyst and time range

    Args:
        widget (Optional[Union[Dict, str]]): Full widget definition (camelCase
            keys) as returned by legacy_soar_get_dashboard; dict or JSON
            string. Explicit arguments below override its keys.
        widget_id (Optional[int]): Widget ID (``id``; 0 for an ad-hoc widget).
        dashboard_id (Optional[int]): Owning dashboard ID (``dashboardId``).
        title (Optional[str]): Widget title.
        widget_type (Optional[str]): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        width_size (Optional[str]): ``ONE_BLOCK``, ``TWO_BLOCKS``,
            ``THREE_BLOCKS``.
        description (Optional[str]): Widget description.
        order (Optional[int]): Position in the dashboard.
        time_filter (Optional[str]): LAST_DAY, LAST_3_DAYS, LAST_WEEK,
            LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        subject (Optional[str]): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        dimension_a (Optional[str]): Primary grouping, e.g. ``ANALYST``,
            ``PRIORITY``, ``CASE_STATUS``, ``PLAYBOOK``, ``STAGE``.
        dimension_b (Optional[str]): Secondary grouping, same enum.
        chart_type (Optional[str]): ``PIE``, ``HORIZENTAL_BARS``,
            ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``,
            ``NUMBER_STATUS`` and others.
        results_amount (Optional[int]): Max result buckets.
        results_order (Optional[str]): ``DESCENDING`` or ``ASCENDING``.
        calculate_field (Optional[str]): ``COUNT``, ``HANDLING_AVG_TIME``,
            ``SLA_AVG_REMAINING_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        extra_fields (Optional[Union[Dict, str]]): Other camelCase request
            fields such as ``caseStatusesFilter``, ``priorityFilter``,
            ``analystFilters``, ``environmentFilter``, ``playbooksFilter``,
            ``playbookStatusFilter``; full key list in
            legacy_soar_add_or_update_dashboard_widget.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": [<case_id>, ...], "total_results": N}``
            or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_widget_case_ids(widget=dashboard_widget)

    Next Steps (using MCP-enabled tools):
        - Inspect individual cases with the SOAR case tools
    """
    return await _widget_query(
        "legacyGetDashboardWidgetCaseIds",
        "dashboard widget case IDs",
        widget=widget,
        widget_id=widget_id,
        dashboard_id=dashboard_id,
        title=title,
        widget_type=widget_type,
        width_size=width_size,
        description=description,
        order=order,
        time_filter=time_filter,
        subject=subject,
        dimension_a=dimension_a,
        dimension_b=dimension_b,
        chart_type=chart_type,
        results_amount=results_amount,
        results_order=results_order,
        calculate_field=calculate_field,
        extra_fields=extra_fields,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
    )


@server.tool()
async def legacy_soar_get_dashboard_custom_widget_case_ids(
    widget: Optional[Union[Dict[str, Any], str]] = None,
    widget_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
    title: Optional[str] = None,
    widget_type: Optional[str] = None,
    width_size: Optional[str] = None,
    description: Optional[str] = None,
    order: Optional[int] = None,
    time_filter: Optional[str] = None,
    subject: Optional[str] = None,
    dimension_a: Optional[str] = None,
    dimension_b: Optional[str] = None,
    chart_type: Optional[str] = None,
    results_amount: Optional[int] = None,
    results_order: Optional[str] = None,
    calculate_field: Optional[str] = None,
    extra_fields: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List the SOAR case IDs behind a CUSTOM legacy dashboard widget.

    Same as legacy_soar_get_dashboard_widget_case_ids but for widgets of type
    ``CUSTOM`` with user-defined dimensions (``subject``/``dimensionA``/
    ``dimensionB``) and filters. Served through the Chronicle API
    (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Use when the widget has ``widgetType: "CUSTOM"``; otherwise prefer
      legacy_soar_get_dashboard_widget_case_ids.

    **Use Cases:**
    - Drill into a custom "Cases by analyst and priority" chart

    Args:
        widget (Optional[Union[Dict, str]]): Full widget definition (camelCase
            keys) as returned by legacy_soar_get_dashboard; dict or JSON
            string. Explicit arguments below override its keys.
        widget_id (Optional[int]): Widget ID (``id``; 0 for an ad-hoc widget).
        dashboard_id (Optional[int]): Owning dashboard ID (``dashboardId``).
        title (Optional[str]): Widget title.
        widget_type (Optional[str]): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        width_size (Optional[str]): ``ONE_BLOCK``, ``TWO_BLOCKS``,
            ``THREE_BLOCKS``.
        description (Optional[str]): Widget description.
        order (Optional[int]): Position in the dashboard.
        time_filter (Optional[str]): LAST_DAY, LAST_3_DAYS, LAST_WEEK,
            LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        subject (Optional[str]): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        dimension_a (Optional[str]): Primary grouping, e.g. ``ANALYST``,
            ``PRIORITY``, ``CASE_STATUS``, ``PLAYBOOK``, ``STAGE``.
        dimension_b (Optional[str]): Secondary grouping, same enum.
        chart_type (Optional[str]): ``PIE``, ``HORIZENTAL_BARS``,
            ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``,
            ``NUMBER_STATUS`` and others.
        results_amount (Optional[int]): Max result buckets.
        results_order (Optional[str]): ``DESCENDING`` or ``ASCENDING``.
        calculate_field (Optional[str]): ``COUNT``, ``HANDLING_AVG_TIME``,
            ``SLA_AVG_REMAINING_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        extra_fields (Optional[Union[Dict, str]]): Other camelCase request
            fields such as ``caseStatusesFilter``, ``priorityFilter``,
            ``analystFilters``, ``environmentFilter``, ``playbooksFilter``,
            ``playbookStatusFilter``; full key list in
            legacy_soar_add_or_update_dashboard_widget.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": [<case_id>, ...], "total_results": N}``
            or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_custom_widget_case_ids(widget=custom_widget)

    Next Steps (using MCP-enabled tools):
        - Inspect individual cases with the SOAR case tools
    """
    return await _widget_query(
        "legacyGetDashboardCustomWidgetCaseIds",
        "dashboard custom widget case IDs",
        widget=widget,
        widget_id=widget_id,
        dashboard_id=dashboard_id,
        title=title,
        widget_type=widget_type,
        width_size=width_size,
        description=description,
        order=order,
        time_filter=time_filter,
        subject=subject,
        dimension_a=dimension_a,
        dimension_b=dimension_b,
        chart_type=chart_type,
        results_amount=results_amount,
        results_order=results_order,
        calculate_field=calculate_field,
        extra_fields=extra_fields,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
    )


@server.tool()
async def legacy_soar_get_dashboard_playbook_runs(
    widget: Optional[Union[Dict[str, Any], str]] = None,
    widget_id: Optional[int] = None,
    dashboard_id: Optional[int] = None,
    title: Optional[str] = None,
    widget_type: Optional[str] = None,
    width_size: Optional[str] = None,
    description: Optional[str] = None,
    order: Optional[int] = None,
    time_filter: Optional[str] = None,
    subject: Optional[str] = None,
    dimension_a: Optional[str] = None,
    dimension_b: Optional[str] = None,
    chart_type: Optional[str] = None,
    results_amount: Optional[int] = None,
    results_order: Optional[str] = None,
    calculate_field: Optional[str] = None,
    extra_fields: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List recent SOAR playbook runs behind a legacy dashboard widget.

    Returns execution records (status, timing, case) for the playbook widget
    described by the request. Served through the Chronicle API (v1alpha-only,
    legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Typically used with ``subject="PLAYBOOKS"`` widgets and the
      ``playbooksFilter`` / ``playbookStatusFilter`` keys in ``extra_fields``.

    **Use Cases:**
    - List failed runs of a playbook over the last week
    - Audit which cases a playbook touched

    Args:
        widget (Optional[Union[Dict, str]]): Full widget definition (camelCase
            keys) as returned by legacy_soar_get_dashboard; dict or JSON
            string. Explicit arguments below override its keys.
        widget_id (Optional[int]): Widget ID (``id``; 0 for an ad-hoc widget).
        dashboard_id (Optional[int]): Owning dashboard ID (``dashboardId``).
        title (Optional[str]): Widget title.
        widget_type (Optional[str]): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        width_size (Optional[str]): ``ONE_BLOCK``, ``TWO_BLOCKS``,
            ``THREE_BLOCKS``.
        description (Optional[str]): Widget description.
        order (Optional[int]): Position in the dashboard.
        time_filter (Optional[str]): LAST_DAY, LAST_3_DAYS, LAST_WEEK,
            LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        subject (Optional[str]): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        dimension_a (Optional[str]): Primary grouping, e.g. ``ANALYST``,
            ``PRIORITY``, ``CASE_STATUS``, ``PLAYBOOK``, ``STAGE``.
        dimension_b (Optional[str]): Secondary grouping, same enum.
        chart_type (Optional[str]): ``PIE``, ``HORIZENTAL_BARS``,
            ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``,
            ``NUMBER_STATUS`` and others.
        results_amount (Optional[int]): Max result buckets.
        results_order (Optional[str]): ``DESCENDING`` or ``ASCENDING``.
        calculate_field (Optional[str]): ``COUNT``, ``HANDLING_AVG_TIME``,
            ``SLA_AVG_REMAINING_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        extra_fields (Optional[Union[Dict, str]]): Other camelCase request
            fields such as ``caseStatusesFilter``, ``priorityFilter``,
            ``analystFilters``, ``environmentFilter``, ``playbooksFilter``,
            ``playbookStatusFilter``; full key list in
            legacy_soar_add_or_update_dashboard_widget.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": [<LegacySoarDashboardPlaybookRunDataModel>],
            "total_results": N}`` or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_dashboard_playbook_runs(widget_id=0, dashboard_id=12,
            title="Failed runs", widget_type="CUSTOM", width_size="ONE_BLOCK",
            subject="PLAYBOOKS", time_filter="LAST_WEEK",
            extra_fields={"playbookStatusFilter": ["ERROR"]})

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_playbook_monitoring(workflow_identifier=...)
    """
    return await _widget_query(
        "legacyGetDashboardPlaybookRuns",
        "dashboard playbook runs",
        widget=widget,
        widget_id=widget_id,
        dashboard_id=dashboard_id,
        title=title,
        widget_type=widget_type,
        width_size=width_size,
        description=description,
        order=order,
        time_filter=time_filter,
        subject=subject,
        dimension_a=dimension_a,
        dimension_b=dimension_b,
        chart_type=chart_type,
        results_amount=results_amount,
        results_order=results_order,
        calculate_field=calculate_field,
        extra_fields=extra_fields,
        project_id=project_id,
        customer_id=customer_id,
        region=region,
    )


# ---------------------------------------------------------------------------
# SOC metrics
# ---------------------------------------------------------------------------


@server.tool()
async def legacy_soar_get_playbook_monitoring(
    workflow_identifier: Optional[str] = None,
    time_filter: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the monitoring dashboard for a SOAR playbook.

    Returns a dashboard-shaped view with total runs, success/failure rates,
    average runtime and trends for one playbook. Served through the Chronicle
    API (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Get playbook identifiers from legacy_soar_get_dashboard_playbooks.

    **Use Cases:**
    - Check whether a playbook's error rate rose this week
    - Report average playbook runtime to management

    Args:
        workflow_identifier (Optional[str]): Playbook (workflow) identifier.
        time_filter (Optional[str]): One of DASHBOARD_TIME_RANGE_TYPE_UNSPECIFIED, LAST_DAY, LAST_3_DAYS,
            LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS,
            LAST_YEAR.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": {<LegacySoarDashboardDataModel>}}`` or
            ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_playbook_monitoring(
            workflow_identifier="<playbook-identifier>", time_filter="LAST_WEEK")

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard_playbook_runs(...) for individual runs
    """
    try:
        logger.info(
            "Getting legacy SOAR playbook monitoring for %s", workflow_identifier
        )
        chronicle = get_chronicle_client(project_id, customer_id, region)
        body = _compact(
            {"workflowIdentifier": workflow_identifier, "timeFilter": time_filter}
        )
        return chronicle_api_request(
            chronicle, "POST", _verb("legacyGetPlaybookMonitoring"), json_body=body
        )
    except Exception as e:
        logger.error(
            "Error getting legacy SOAR playbook monitoring: %s", e, exc_info=True
        )
        return {"error": f"Error getting legacy SOAR playbook monitoring: {e}"}


@server.tool()
async def legacy_soar_get_cases_time_to_respond(
    time_range_filter: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the average time-to-respond for SOAR cases in a time range.

    SOC responsiveness KPI from the SOAR backend. Served through the
    Chronicle API (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Pair with legacy_soar_get_opened_and_closed_cases_trends for a workload
      and responsiveness summary.

    **Use Cases:**
    - Weekly SOC KPI reporting
    - Compare response time across time windows

    Args:
        time_range_filter (Optional[str]): One of LAST_DAY, LAST_2_DAYS, LAST_3_DAYS, LAST_4_DAYS,
            LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS,
            LAST_YEAR, LAST_13_MONTHS
            (``CUSTOM`` is the proto default and is not useful here).
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"timeToResponseValue": <int>}`` or
            ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_cases_time_to_respond(time_range_filter="LAST_WEEK")

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_opened_and_closed_cases_trends(time_range_type="LAST_WEEK")
    """
    try:
        logger.info("Getting legacy SOAR cases time to respond (%s)", time_range_filter)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle,
            "GET",
            _verb("legacyGetCasesTimeToRespond"),
            params={"timeRangeFilter": time_range_filter},
        )
    except Exception as e:
        logger.error(
            "Error getting legacy SOAR cases time to respond: %s", e, exc_info=True
        )
        return {"error": f"Error getting legacy SOAR cases time to respond: {e}"}


@server.tool()
async def legacy_soar_get_opened_and_closed_cases_trends(
    time_range_type: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get opened vs. closed SOAR case trends over a time range.

    Returns a time series of case openings and closures for SOC workload and
    resolution-efficiency reporting. Served through the Chronicle API
    (v1alpha-only, legacy); requires a SOAR-mapped user.

    **Workflow Integration:**
    - Combine with legacy_soar_get_cases_time_to_respond for KPI summaries.

    **Use Cases:**
    - Is the case backlog growing or shrinking?
    - Month-over-month SOC throughput

    Args:
        time_range_type (str): Required. One of LAST_DAY, LAST_2_DAYS, LAST_3_DAYS, LAST_4_DAYS,
            LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS,
            LAST_YEAR, LAST_13_MONTHS.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: ``{"payload": [<GetOpenedAndClosedCasesTrends>],
            "total_results": N}`` or ``{"error": ...}``.

    Example Usage:
        legacy_soar_get_opened_and_closed_cases_trends(time_range_type="LAST_MONTH")

    Next Steps (using MCP-enabled tools):
        - legacy_soar_get_dashboard_widget_case_ids(...) to drill into cases
    """
    try:
        logger.info(
            "Getting legacy SOAR opened/closed case trends (%s)", time_range_type
        )
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "GET",
            _verb("legacyGetOpenedAndClosedCasesTrends"),
            params={"timeRangeType": time_range_type},
        )
        return {**result, "total_results": len(result.get("payload") or [])}
    except Exception as e:
        logger.error(
            "Error getting legacy SOAR opened/closed case trends: %s", e, exc_info=True
        )
        return {"error": f"Error getting legacy SOAR opened/closed case trends: {e}"}
