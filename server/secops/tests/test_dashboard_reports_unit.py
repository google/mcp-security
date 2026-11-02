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
"""Unit tests for dashboard scheduled report and featured content tools."""

from unittest.mock import MagicMock, patch

import pytest

from secops_mcp.tools import dashboard_reports as dr

INSTANCE = "projects/p/locations/us/instances/i"
REPORTS = "/dashboardScheduledReports"
FEATURED = "/contentHub/featuredContentNativeDashboards"


@pytest.fixture
def api():
    with patch(
        "secops_mcp.tools.dashboard_reports.get_chronicle_client"
    ) as get_client, patch(
        "secops_mcp.tools.dashboard_reports.chronicle_api_request"
    ) as request:
        client = MagicMock()
        client.instance_id = INSTANCE
        get_client.return_value = client
        request.return_value = {"ok": True}
        request.client = client
        yield request


def _call(api):
    """Return (method, path, kwargs) of the single recorded API call."""
    assert api.call_count == 1
    args, kwargs = api.call_args
    assert args[0] is api.client
    return args[1], args[2], kwargs


# --- scheduled reports -----------------------------------------------------


@pytest.mark.asyncio
async def test_list_dashboard_scheduled_reports(api):
    api.return_value = {
        "dashboardScheduledReports": [{"name": "a"}, {"name": "b"}],
        "nextPageToken": "tok",
    }
    result = await dr.list_dashboard_scheduled_reports(
        page_size=10,
        page_token="p",
        filter_query="weekly",
        view="DASHBOARD_SCHEDULED_REPORT_VIEW_FULL",
    )
    method, path, kwargs = _call(api)
    assert (method, path) == ("GET", REPORTS)
    assert kwargs["params"] == {
        "pageSize": 10,
        "pageToken": "p",
        "filter": "weekly",
        "view": "DASHBOARD_SCHEDULED_REPORT_VIEW_FULL",
    }
    assert result["total_reports"] == 2
    assert result["nextPageToken"] == "tok"


@pytest.mark.asyncio
async def test_get_dashboard_scheduled_report_accepts_full_name(api):
    await dr.get_dashboard_scheduled_report(
        report_id=f"{INSTANCE}/dashboardScheduledReports/r1"
    )
    method, path, _ = _call(api)
    assert (method, path) == ("GET", f"{REPORTS}/r1")


@pytest.mark.asyncio
async def test_create_dashboard_scheduled_report_builds_body(api):
    await dr.create_dashboard_scheduled_report(
        display_name="Weekly",
        dashboard_id="dash1",
        cron="0 8 * * 1",
        recipients=["a@example.com"],
        time_zone="UTC",
        file_format="FILE_FORMAT_CSV",
        email_subject="Subj",
        scheduled_report={"userData": {"pinned": True}},
    )
    method, path, kwargs = _call(api)
    assert (method, path) == ("POST", REPORTS)
    assert kwargs["json_body"] == {
        "displayName": "Weekly",
        "dashboard": {"name": f"{INSTANCE}/nativeDashboards/dash1"},
        "cronDetails": {"cron": "0 8 * * 1", "timeZone": "UTC"},
        "deliveryDetails": {
            "emailDelivery": {"recipients": ["a@example.com"], "subject": "Subj"}
        },
        "format": {"fileFormat": "FILE_FORMAT_CSV"},
        "userData": {"pinned": True},
    }


@pytest.mark.asyncio
async def test_create_dashboard_scheduled_report_parses_json_strings(api):
    await dr.create_dashboard_scheduled_report(
        display_name="Daily",
        dashboard_id=f"{INSTANCE}/nativeDashboards/full",
        cron="0 6 * * *",
        recipients='["x@example.com", "y@example.com"]',
        scheduled_report='{"description": "from json", "etag": "e1"}',
    )
    _, _, kwargs = _call(api)
    body = kwargs["json_body"]
    assert body["dashboard"] == {"name": f"{INSTANCE}/nativeDashboards/full"}
    assert body["deliveryDetails"]["emailDelivery"]["recipients"] == [
        "x@example.com",
        "y@example.com",
    ]
    assert body["description"] == "from json"
    assert body["etag"] == "e1"
    assert body["format"] == {"fileFormat": "FILE_FORMAT_PDF"}


@pytest.mark.asyncio
async def test_update_dashboard_scheduled_report_derives_mask(api):
    await dr.update_dashboard_scheduled_report(
        report_id="r1",
        cron="0 7 * * 1-5",
        recipients=["b@example.com"],
        pinned=True,
    )
    method, path, kwargs = _call(api)
    assert (method, path) == ("PATCH", f"{REPORTS}/r1")
    assert kwargs["params"] == {
        "updateMask": "cron_details,delivery_details,user_data.pinned"
    }
    assert kwargs["json_body"] == {
        "cronDetails": {"cron": "0 7 * * 1-5"},
        "deliveryDetails": {"emailDelivery": {"recipients": ["b@example.com"]}},
        "userData": {"pinned": True},
    }


@pytest.mark.asyncio
async def test_update_dashboard_scheduled_report_explicit_mask(api):
    await dr.update_dashboard_scheduled_report(
        report_id="r1",
        display_name="New",
        update_mask="display_name, description",
        scheduled_report='{"description": "d"}',
    )
    _, _, kwargs = _call(api)
    assert kwargs["params"] == {"updateMask": "display_name,description"}
    assert kwargs["json_body"] == {"displayName": "New", "description": "d"}


@pytest.mark.asyncio
async def test_delete_dashboard_scheduled_report(api):
    api.return_value = {}
    result = await dr.delete_dashboard_scheduled_report(report_id="r9")
    method, path, _ = _call(api)
    assert (method, path) == ("DELETE", f"{REPORTS}/r9")
    assert result == {"deleted": True, "report_id": "r9"}


@pytest.mark.asyncio
async def test_fetch_dashboard_scheduled_report_history(api):
    await dr.fetch_dashboard_scheduled_report_history(
        report_id="r1", page_size=20, page_token="t"
    )
    method, path, kwargs = _call(api)
    assert (method, path) == ("GET", f"{REPORTS}/r1:fetchHistory")
    assert kwargs["params"] == {"pageSize": 20, "pageToken": "t"}


@pytest.mark.asyncio
async def test_duplicate_dashboard_scheduled_report(api):
    await dr.duplicate_dashboard_scheduled_report(report_id="r1")
    method, path, kwargs = _call(api)
    assert (method, path) == ("POST", f"{REPORTS}/r1:duplicate")
    assert kwargs["json_body"] == {}


@pytest.mark.asyncio
async def test_trigger_instant_dashboard_report(api):
    api.return_value = {"name": "operations/op1", "done": False}
    result = await dr.trigger_instant_dashboard_report(report_id="r1")
    method, path, kwargs = _call(api)
    assert (method, path) == ("POST", f"{REPORTS}/r1:trigger")
    assert kwargs["json_body"] == {}
    assert result["done"] is False


# --- featured content ------------------------------------------------------


@pytest.mark.asyncio
async def test_list_featured_content_dashboards(api):
    api.return_value = {"featuredContentNativeDashboards": [{"name": "f1"}]}
    result = await dr.list_featured_content_dashboards(
        page_size=5, filter_query="okta"
    )
    method, path, kwargs = _call(api)
    assert (method, path) == ("GET", FEATURED)
    assert kwargs["params"] == {
        "pageSize": 5,
        "pageToken": None,
        "filter": "okta",
    }
    assert result["total_featured_dashboards"] == 1


@pytest.mark.asyncio
async def test_get_featured_content_dashboard(api):
    await dr.get_featured_content_dashboard(
        featured_dashboard_id=f"{INSTANCE}{FEATURED}/okta"
    )
    method, path, _ = _call(api)
    assert (method, path) == ("GET", f"{FEATURED}/okta")


@pytest.mark.asyncio
async def test_install_featured_content_dashboard(api):
    api.return_value = {"nativeDashboard": f"{INSTANCE}/nativeDashboards/new"}
    result = await dr.install_featured_content_dashboard(
        featured_dashboard_id="okta",
        featured_dashboard='{"dashboardContent": {"dashboard": {"displayName": "X"}}}',
    )
    method, path, kwargs = _call(api)
    assert (method, path) == ("POST", f"{FEATURED}/okta:install")
    assert kwargs["json_body"] == {
        "featuredContentNativeDashboard": {
            "dashboardContent": {"dashboard": {"displayName": "X"}}
        }
    }
    assert result["nativeDashboard"].endswith("/nativeDashboards/new")


@pytest.mark.asyncio
async def test_install_featured_content_dashboard_empty_body(api):
    await dr.install_featured_content_dashboard(featured_dashboard_id="okta")
    _, _, kwargs = _call(api)
    assert kwargs["json_body"] == {}


# --- error paths -----------------------------------------------------------


@pytest.mark.asyncio
async def test_api_error_returns_error_dict(api):
    api.side_effect = RuntimeError("Chronicle API GET failed with status 404")
    result = await dr.get_dashboard_scheduled_report(report_id="missing")
    assert "error" in result
    assert "404" in result["error"]


@pytest.mark.asyncio
async def test_invalid_json_arg_returns_error_dict(api):
    result = await dr.create_dashboard_scheduled_report(
        display_name="x", dashboard_id="d", cron="* * * * *", recipients="{bad"
    )
    assert "error" in result
    assert "recipients must be valid JSON" in result["error"]
    api.assert_not_called()
