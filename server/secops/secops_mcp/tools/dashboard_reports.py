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
"""Security Operations MCP tools for dashboard scheduled reports and
Content Hub featured dashboards.

Covers the Chronicle ``DashboardScheduledReportService`` (v1alpha-only) and
``FeaturedContentNativeDashboardService`` REST surfaces.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from secops_mcp.server import get_chronicle_client, server
from secops_mcp.utils import chronicle_api_request, parse_json_arg

# Configure logging
logger = logging.getLogger("secops-mcp")

_SCHEDULED_REPORTS = "/dashboardScheduledReports"
_FEATURED_DASHBOARDS = "/contentHub/featuredContentNativeDashboards"


def _compact(value: Any) -> Any:
    """Recursively drop ``None`` values from dicts (and nested lists)."""
    if isinstance(value, dict):
        return {k: _compact(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_compact(v) for v in value if v is not None]
    return value


def _resource_id(value: str) -> str:
    """Return the last path segment of a resource name or a bare ID."""
    return value.rstrip("/").rsplit("/", 1)[-1] if "/" in value else value


def _dashboard_name(chronicle: Any, dashboard: str) -> str:
    """Return the bare native dashboard ID expected in ``dashboard.name``.

    The scheduled-report backend stores and resolves ``dashboard.name`` as the
    bare dashboard ID (verified live: a full
    ``projects/.../nativeDashboards/{id}`` name fails with ``INTERNAL: failed
    to fetch native dashboard details``), so full names are reduced to their
    last path segment.
    """
    del chronicle  # kept for signature stability; no expansion needed
    return _resource_id(dashboard)


def _merge(base: Dict[str, Any], extra: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Shallow-merge ``extra`` over ``base`` (nested dicts merged one level)."""
    if not extra:
        return base
    merged = dict(base)
    for key, val in extra.items():
        if isinstance(val, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **val}
        else:
            merged[key] = val
    return merged


# ---------------------------------------------------------------------------
# Dashboard scheduled reports
# ---------------------------------------------------------------------------


@server.tool()
async def list_dashboard_scheduled_reports(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    filter_query: Optional[str] = None,
    view: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List scheduled email/GCS reports configured for native dashboards.

    Returns the scheduled report configurations (schedule, delivery targets,
    file format, status, last run) in the Chronicle instance. v1alpha-only.

    **Workflow Integration:**
    - Start here to inventory which dashboards are being emailed on a
      schedule before creating, updating, or deleting a report.
    - Pair with `fetch_dashboard_scheduled_report_history` to audit delivery
      success rates.

    **Use Cases:**
    - Audit who receives automated SOC dashboard reports
    - Find reports in SUSPENDED state that need attention
    - Locate a report by name before editing it

    Args:
        page_size (Optional[int]): Maximum number of reports to return.
        page_token (Optional[str]): `nextPageToken` from a previous call.
        filter_query (Optional[str]): Case-insensitive substring match applied
            to `display_name` and `description`.
        view (Optional[str]): `DASHBOARD_SCHEDULED_REPORT_VIEW_BASIC`
            (default) or `DASHBOARD_SCHEDULED_REPORT_VIEW_FULL`.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: API response with `dashboardScheduledReports`,
            `nextPageToken`, plus `total_reports` for the page, or an error.

    Example Usage:
        list_dashboard_scheduled_reports(filter_query="weekly")

    Next Steps (using MCP-enabled tools):
        - `get_dashboard_scheduled_report` for full detail on one report
        - `fetch_dashboard_scheduled_report_history` to check past runs
    """
    try:
        logger.info("Listing dashboard scheduled reports")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "GET",
            _SCHEDULED_REPORTS,
            params={
                "pageSize": page_size,
                "pageToken": page_token,
                "filter": filter_query,
                "view": view,
            },
        )
        result["total_reports"] = len(
            result.get("dashboardScheduledReports", []) or []
        )
        return result
    except Exception as e:
        logger.error("Error listing dashboard scheduled reports: %s", e, exc_info=True)
        return {"error": f"Error listing dashboard scheduled reports: {e}"}


@server.tool()
async def get_dashboard_scheduled_report(
    report_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get a single dashboard scheduled report configuration.

    Returns the full `DashboardScheduledReport` resource: display name,
    dashboard reference, cron schedule and time zone, delivery details
    (email recipients, subject, body), file format, scope, status, etag,
    and the last report generation detail. v1alpha-only.

    **Workflow Integration:**
    - Call before `update_dashboard_scheduled_report` to see current values
      and obtain the `etag`.

    **Use Cases:**
    - Confirm recipients and schedule of a report
    - Check `lastReportGenerationDetail` for the latest failure message

    Args:
        report_id (str): Scheduled report ID or full resource name
            (`projects/.../dashboardScheduledReports/{id}`).
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The `DashboardScheduledReport` resource or an error.

    Example Usage:
        get_dashboard_scheduled_report(report_id="a1b2c3d4")

    Next Steps (using MCP-enabled tools):
        - `update_dashboard_scheduled_report` to change recipients/schedule
        - `trigger_instant_dashboard_report` to send it now
    """
    try:
        rid = _resource_id(report_id)
        logger.info("Getting dashboard scheduled report %s", rid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(chronicle, "GET", f"{_SCHEDULED_REPORTS}/{rid}")
    except Exception as e:
        logger.error("Error getting dashboard scheduled report: %s", e, exc_info=True)
        return {"error": f"Error getting dashboard scheduled report: {e}"}


@server.tool()
async def create_dashboard_scheduled_report(
    display_name: str,
    dashboard_id: str,
    cron: str,
    recipients: Optional[Union[List[str], str]] = None,
    time_zone: Optional[str] = None,
    file_format: Optional[str] = None,
    description: Optional[str] = None,
    email_subject: Optional[str] = None,
    email_body: Optional[str] = None,
    delivery_type: Optional[str] = None,
    data_access_scopes: Optional[Union[List[str], str]] = None,
    scheduled_report: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a scheduled report that emails a native dashboard on a cron.

    Builds a `DashboardScheduledReport` from the common fields and POSTs it
    to `/dashboardScheduledReports`. Any extra or nested fields can be
    supplied via `scheduled_report`, which is merged over the generated
    body. v1alpha-only.

    **Workflow Integration:**
    - Use `list_native_dashboards` (native dashboard tools) to find the
      dashboard ID first.
    - Follow up with `trigger_instant_dashboard_report` to test delivery.

    **Use Cases:**
    - Email a weekly SOC metrics dashboard as PDF to leadership
    - Deliver a daily CSV export of a detections dashboard

    Args:
        display_name (str): Report name shown in the UI (required).
        dashboard_id (str): Native dashboard ID or full resource name
            (`projects/.../nativeDashboards/{id}`); sent as the bare ID in
            `dashboard.name`, which is what the API expects.
        cron (str): Crontab schedule, 5 fields `min hour dom month dow`
            (e.g. "0 8 * * 1" = Mondays 08:00).
        recipients (Optional[Union[List[str], str]]): Email recipients
            (required by the API for email delivery). JSON array string ok.
        time_zone (Optional[str]): IANA time zone for the cron (default UTC).
        file_format (Optional[str]): `FILE_FORMAT_PDF`, `FILE_FORMAT_CSV`, or
            `FILE_FORMAT_PNG` (required by the API; defaults to PDF here).
        description (Optional[str]): Free-text description.
        email_subject (Optional[str]): Email subject line.
        email_body (Optional[str]): Email body text.
        delivery_type (Optional[str]): `DELIVERY_TYPE_EMAIL_ATTACHMENT` or
            `DELIVERY_TYPE_GCS_BUCKET`.
        data_access_scopes (Optional[Union[List[str], str]]): Full
            `dataAccessScopes` resource names for `scopeInfo`.
        scheduled_report (Optional[Union[Dict[str, Any], str]]): Extra
            `DashboardScheduledReport` JSON (camelCase keys, e.g.
            `{"userData": {"pinned": true}, "scopeInfo": {...}}`) merged over
            the body built from the arguments above.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The created `DashboardScheduledReport` or an error.

    Example Usage:
        create_dashboard_scheduled_report(
            display_name="Weekly SOC Summary", dashboard_id="abc123",
            cron="0 8 * * 1", time_zone="America/New_York",
            recipients=["soc-leads@example.com"], file_format="FILE_FORMAT_PDF")

    Next Steps (using MCP-enabled tools):
        - `trigger_instant_dashboard_report` to verify delivery immediately
        - `list_dashboard_scheduled_reports` to confirm it is ACTIVE
    """
    try:
        logger.info("Creating dashboard scheduled report %s", display_name)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        recipient_list = parse_json_arg(recipients, "recipients")
        scopes = parse_json_arg(data_access_scopes, "data_access_scopes")
        extra = parse_json_arg(scheduled_report, "scheduled_report")

        body: Dict[str, Any] = {
            "displayName": display_name,
            "description": description,
            "dashboard": {"name": _dashboard_name(chronicle, dashboard_id)},
            "cronDetails": {"cron": cron, "timeZone": time_zone},
            "deliveryDetails": {
                "emailDelivery": {
                    "recipients": recipient_list,
                    "subject": email_subject,
                    "emailBody": email_body,
                },
                "deliveryType": delivery_type,
            },
            "format": {"fileFormat": file_format or "FILE_FORMAT_PDF"},
            "scopeInfo": {"dataAccessScopes": scopes} if scopes else None,
        }
        body = _compact(_merge(body, extra))
        return chronicle_api_request(
            chronicle, "POST", _SCHEDULED_REPORTS, json_body=body
        )
    except Exception as e:
        logger.error("Error creating dashboard scheduled report: %s", e, exc_info=True)
        return {"error": f"Error creating dashboard scheduled report: {e}"}


@server.tool()
async def update_dashboard_scheduled_report(
    report_id: str,
    update_mask: Optional[Union[List[str], str]] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    dashboard_id: Optional[str] = None,
    cron: Optional[str] = None,
    time_zone: Optional[str] = None,
    recipients: Optional[Union[List[str], str]] = None,
    email_subject: Optional[str] = None,
    email_body: Optional[str] = None,
    delivery_type: Optional[str] = None,
    file_format: Optional[str] = None,
    pinned: Optional[bool] = None,
    scheduled_report: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update fields of an existing dashboard scheduled report (PATCH).

    Sends `PATCH /dashboardScheduledReports/{id}?updateMask=...` with the
    changed fields. If `update_mask` is omitted it is derived from the
    arguments you pass. v1alpha-only.

    **Workflow Integration:**
    - Call `get_dashboard_scheduled_report` first to see current values.

    **Use Cases:**
    - Add or remove email recipients
    - Change the cron schedule or time zone
    - Switch the file format from PDF to CSV
    - Pin a report in the UI

    Args:
        report_id (str): Scheduled report ID or full resource name.
        update_mask (Optional[Union[List[str], str]]): Field paths to update.
            Supported: `display_name`, `description`, `cron_details`,
            `format`, `delivery_details`, `scope_info`, `dashboard.name`,
            `user_data.pinned`. Comma-separated string, JSON array, or list.
        display_name (Optional[str]): New display name.
        description (Optional[str]): New description.
        dashboard_id (Optional[str]): New native dashboard ID or full name.
        cron (Optional[str]): New crontab string (5 fields).
        time_zone (Optional[str]): New IANA time zone.
        recipients (Optional[Union[List[str], str]]): Replacement recipient
            list (whole `delivery_details` is replaced, so pass all fields).
        email_subject (Optional[str]): New email subject.
        email_body (Optional[str]): New email body.
        delivery_type (Optional[str]): `DELIVERY_TYPE_EMAIL_ATTACHMENT` or
            `DELIVERY_TYPE_GCS_BUCKET`.
        file_format (Optional[str]): `FILE_FORMAT_PDF|CSV|PNG`.
        pinned (Optional[bool]): Pin/unpin (`user_data.pinned`).
        scheduled_report (Optional[Union[Dict[str, Any], str]]): Extra
            resource JSON (camelCase) merged over the generated body, e.g.
            `{"scopeInfo": {"dataAccessScopes": [...]}, "etag": "..."}`.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The updated `DashboardScheduledReport` or an error.

    Example Usage:
        update_dashboard_scheduled_report(report_id="a1b2c3d4",
            cron="0 7 * * 1-5", time_zone="UTC")

    Next Steps (using MCP-enabled tools):
        - `get_dashboard_scheduled_report` to confirm the change
    """
    try:
        rid = _resource_id(report_id)
        logger.info("Updating dashboard scheduled report %s", rid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        recipient_list = parse_json_arg(recipients, "recipients")
        extra = parse_json_arg(scheduled_report, "scheduled_report")

        body: Dict[str, Any] = {
            "displayName": display_name,
            "description": description,
        }
        mask: List[str] = []
        if display_name is not None:
            mask.append("display_name")
        if description is not None:
            mask.append("description")
        if dashboard_id is not None:
            body["dashboard"] = {"name": _dashboard_name(chronicle, dashboard_id)}
            mask.append("dashboard.name")
        if cron is not None or time_zone is not None:
            body["cronDetails"] = {"cron": cron, "timeZone": time_zone}
            mask.append("cron_details")
        if any(
            v is not None
            for v in (recipient_list, email_subject, email_body, delivery_type)
        ):
            body["deliveryDetails"] = {
                "emailDelivery": {
                    "recipients": recipient_list,
                    "subject": email_subject,
                    "emailBody": email_body,
                },
                "deliveryType": delivery_type,
            }
            mask.append("delivery_details")
        if file_format is not None:
            body["format"] = {"fileFormat": file_format}
            mask.append("format")
        if pinned is not None:
            body["userData"] = {"pinned": pinned}
            mask.append("user_data.pinned")
        if extra and "scopeInfo" in extra:
            mask.append("scope_info")

        if update_mask is not None:
            if isinstance(update_mask, str) and not update_mask.lstrip().startswith("["):
                mask = [p.strip() for p in update_mask.split(",") if p.strip()]
            else:
                mask = list(parse_json_arg(update_mask, "update_mask") or [])

        body = _compact(_merge(body, extra))
        return chronicle_api_request(
            chronicle,
            "PATCH",
            f"{_SCHEDULED_REPORTS}/{rid}",
            params={"updateMask": ",".join(mask) if mask else None},
            json_body=body,
        )
    except Exception as e:
        logger.error("Error updating dashboard scheduled report: %s", e, exc_info=True)
        return {"error": f"Error updating dashboard scheduled report: {e}"}


@server.tool()
async def delete_dashboard_scheduled_report(
    report_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a dashboard scheduled report.

    Permanently removes the schedule; future deliveries stop. The underlying
    native dashboard is not affected. v1alpha-only.

    **Workflow Integration:**
    - Verify the target with `get_dashboard_scheduled_report` first.

    **Use Cases:**
    - Remove reports for decommissioned dashboards
    - Clean up duplicate or test schedules

    Args:
        report_id (str): Scheduled report ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"deleted": true, "report_id": ...}` or an error.

    Example Usage:
        delete_dashboard_scheduled_report(report_id="a1b2c3d4")

    Next Steps (using MCP-enabled tools):
        - `list_dashboard_scheduled_reports` to confirm removal
    """
    try:
        rid = _resource_id(report_id)
        logger.info("Deleting dashboard scheduled report %s", rid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        chronicle_api_request(chronicle, "DELETE", f"{_SCHEDULED_REPORTS}/{rid}")
        return {"deleted": True, "report_id": rid}
    except Exception as e:
        logger.error("Error deleting dashboard scheduled report: %s", e, exc_info=True)
        return {"error": f"Error deleting dashboard scheduled report: {e}"}


@server.tool()
async def fetch_dashboard_scheduled_report_history(
    report_id: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch the run history of a dashboard scheduled report (last year).

    Calls `GET /dashboardScheduledReports/{id}:fetchHistory`. Each entry has
    `reportTime`, `deliveryStatus` (`DELIVERY_STATE_SUCCEEDED`, `_FAILED`,
    `_IN_PROGRESS`) and `successDetails` or `errorDetails`. Newest first.
    v1alpha-only.

    **Workflow Integration:**
    - Use after a recipient reports a missing email, or periodically to
      audit delivery reliability.

    **Use Cases:**
    - Diagnose why a report stopped arriving
    - Count successful runs (`runCounts`) vs all attempts (`totalSize`)

    Args:
        report_id (str): Scheduled report ID or full resource name.
        page_size (Optional[int]): Max entries (default 50, max 1000).
        page_token (Optional[str]): `nextPageToken` from a previous call.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `reportGenerationDetails`, `runCounts`, `totalSize`,
            `nextPageToken`, or an error.

    Example Usage:
        fetch_dashboard_scheduled_report_history(report_id="a1b2c3d4",
            page_size=20)

    Next Steps (using MCP-enabled tools):
        - `update_dashboard_scheduled_report` to fix bad recipients
        - `trigger_instant_dashboard_report` to retry delivery now
    """
    try:
        rid = _resource_id(report_id)
        logger.info("Fetching history for dashboard scheduled report %s", rid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle,
            "GET",
            f"{_SCHEDULED_REPORTS}/{rid}:fetchHistory",
            params={"pageSize": page_size, "pageToken": page_token},
        )
    except Exception as e:
        logger.error(
            "Error fetching dashboard scheduled report history: %s", e, exc_info=True
        )
        return {"error": f"Error fetching dashboard scheduled report history: {e}"}


@server.tool()
async def duplicate_dashboard_scheduled_report(
    report_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Duplicate an existing dashboard scheduled report.

    Calls `POST /dashboardScheduledReports/{id}:duplicate` and returns the
    newly created copy, which can then be edited independently. v1alpha-only.

    **Workflow Integration:**
    - Clone a known-good report, then `update_dashboard_scheduled_report`
      the copy with a different recipient list or schedule.

    **Use Cases:**
    - Create per-team variants of the same dashboard report
    - Stage schedule changes without touching the original

    Args:
        report_id (str): Source scheduled report ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The new `DashboardScheduledReport` or an error.

    Example Usage:
        duplicate_dashboard_scheduled_report(report_id="a1b2c3d4")

    Next Steps (using MCP-enabled tools):
        - `update_dashboard_scheduled_report` on the returned `name`
    """
    try:
        rid = _resource_id(report_id)
        logger.info("Duplicating dashboard scheduled report %s", rid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle, "POST", f"{_SCHEDULED_REPORTS}/{rid}:duplicate", json_body={}
        )
    except Exception as e:
        logger.error("Error duplicating dashboard scheduled report: %s", e, exc_info=True)
        return {"error": f"Error duplicating dashboard scheduled report: {e}"}


@server.tool()
async def trigger_instant_dashboard_report(
    report_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Send a dashboard scheduled report immediately, outside its schedule.

    Calls `POST /dashboardScheduledReports/{id}:trigger`. This is a
    long-running operation; the response is an `Operation` whose `done`
    flag may be false initially. v1alpha-only.

    **Workflow Integration:**
    - Use right after creating or updating a report to validate delivery.

    **Use Cases:**
    - Send an on-demand copy of a dashboard to stakeholders
    - Retry a failed scheduled delivery

    Args:
        report_id (str): Scheduled report ID or full resource name.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The long-running `Operation` (`name`, `done`,
            optional `metadata`/`response`) or an error.

    Example Usage:
        trigger_instant_dashboard_report(report_id="a1b2c3d4")

    Next Steps (using MCP-enabled tools):
        - `fetch_dashboard_scheduled_report_history` to see the run result
    """
    try:
        rid = _resource_id(report_id)
        logger.info("Triggering instant dashboard report %s", rid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(
            chronicle, "POST", f"{_SCHEDULED_REPORTS}/{rid}:trigger", json_body={}
        )
    except Exception as e:
        logger.error("Error triggering instant dashboard report: %s", e, exc_info=True)
        return {"error": f"Error triggering instant dashboard report: {e}"}


# ---------------------------------------------------------------------------
# Content Hub featured (curated) native dashboards
# ---------------------------------------------------------------------------


@server.tool()
async def list_featured_content_dashboards(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    filter_query: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List Google-curated dashboards available in the Content Hub.

    Calls `GET /contentHub/featuredContentNativeDashboards`. Each entry has
    a `name`, `contentMetadata` (description, etc.), and the full
    `dashboardContent` (dashboard, charts, queries) that would be installed.

    **Workflow Integration:**
    - Browse here before `install_featured_content_dashboard` to add a
      ready-made dashboard to the instance.

    **Use Cases:**
    - Discover curated dashboards for a log source or use case
    - Compare curated chart definitions against custom dashboards

    Args:
        page_size (Optional[int]): Max results (default and max 100).
        page_token (Optional[str]): `nextPageToken` from a previous call.
        filter_query (Optional[str]): AIP-160 filter over `name` and
            `content_metadata.description`; a bare literal (e.g. `"okta"`)
            does a substring match on both.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `featuredContentNativeDashboards`, `nextPageToken`,
            plus `total_featured_dashboards` for the page, or an error.

    Example Usage:
        list_featured_content_dashboards(filter_query="okta")

    Next Steps (using MCP-enabled tools):
        - `get_featured_content_dashboard` for one entry
        - `install_featured_content_dashboard` to install it
    """
    try:
        logger.info("Listing featured content native dashboards")
        chronicle = get_chronicle_client(project_id, customer_id, region)
        result = chronicle_api_request(
            chronicle,
            "GET",
            _FEATURED_DASHBOARDS,
            params={
                "pageSize": page_size,
                "pageToken": page_token,
                "filter": filter_query,
            },
        )
        result["total_featured_dashboards"] = len(
            result.get("featuredContentNativeDashboards", []) or []
        )
        return result
    except Exception as e:
        logger.error("Error listing featured content dashboards: %s", e, exc_info=True)
        return {"error": f"Error listing featured content dashboards: {e}"}


@server.tool()
async def get_featured_content_dashboard(
    featured_dashboard_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get one Content Hub featured (curated) native dashboard.

    Calls `GET /contentHub/featuredContentNativeDashboards/{id}` and returns
    the `FeaturedContentNativeDashboard` including its `dashboardContent`
    (dashboard definition, charts and queries).

    **Workflow Integration:**
    - Inspect the curated charts and UDM queries before installing.

    **Use Cases:**
    - Review what a curated dashboard contains
    - Borrow chart/query definitions for a custom dashboard

    Args:
        featured_dashboard_id (str): Featured dashboard ID or full resource
            name (`projects/.../contentHub/featuredContentNativeDashboards/{id}`).
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: The `FeaturedContentNativeDashboard` or an error.

    Example Usage:
        get_featured_content_dashboard(featured_dashboard_id="okta-overview")

    Next Steps (using MCP-enabled tools):
        - `install_featured_content_dashboard` to install it
    """
    try:
        fid = _resource_id(featured_dashboard_id)
        logger.info("Getting featured content dashboard %s", fid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        return chronicle_api_request(chronicle, "GET", f"{_FEATURED_DASHBOARDS}/{fid}")
    except Exception as e:
        logger.error("Error getting featured content dashboard: %s", e, exc_info=True)
        return {"error": f"Error getting featured content dashboard: {e}"}


@server.tool()
async def install_featured_content_dashboard(
    featured_dashboard_id: str,
    featured_dashboard: Optional[Union[Dict[str, Any], str]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Install a Content Hub curated dashboard as a native dashboard.

    Calls `POST /contentHub/featuredContentNativeDashboards/{id}:install`.
    The server copies the curated dashboard, charts and queries into a new
    `NativeDashboard` owned by the instance and returns its resource name.

    **Workflow Integration:**
    - Browse with `list_featured_content_dashboards`, then install; the
      returned `nativeDashboard` can be managed with the native dashboard
      tools (edit charts, schedule reports).

    **Use Cases:**
    - Quickly stand up a curated dashboard for a newly onboarded log source
    - Re-install a curated dashboard after local edits went wrong

    Args:
        featured_dashboard_id (str): Featured dashboard ID or full resource
            name.
        featured_dashboard (Optional[Union[Dict[str, Any], str]]): Optional
            `FeaturedContentNativeDashboard` JSON sent as
            `featuredContentNativeDashboard` in the body, e.g. to override
            `dashboardContent.dashboard.displayName` before install. Usually
            omitted.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict[str, Any]: `{"nativeDashboard": "projects/.../nativeDashboards/{id}"}`
            or an error.

    Example Usage:
        install_featured_content_dashboard(featured_dashboard_id="okta-overview")

    Next Steps (using MCP-enabled tools):
        - `get_native_dashboard` on the returned name to inspect it
        - `create_dashboard_scheduled_report` to email it on a schedule
    """
    try:
        fid = _resource_id(featured_dashboard_id)
        logger.info("Installing featured content dashboard %s", fid)
        chronicle = get_chronicle_client(project_id, customer_id, region)
        overrides = parse_json_arg(featured_dashboard, "featured_dashboard")
        body = _compact({"featuredContentNativeDashboard": overrides})
        return chronicle_api_request(
            chronicle, "POST", f"{_FEATURED_DASHBOARDS}/{fid}:install", json_body=body
        )
    except Exception as e:
        logger.error("Error installing featured content dashboard: %s", e, exc_info=True)
        return {"error": f"Error installing featured content dashboard: {e}"}
