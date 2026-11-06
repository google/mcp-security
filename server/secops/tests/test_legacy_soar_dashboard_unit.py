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
"""Unit tests for the legacy SOAR dashboard MCP tools.

Every tool is exercised against a mocked ``chronicle_api_request`` so the
assertions cover the HTTP method, the ``legacySoarDashboard:legacy*`` custom
verb, query params and JSON body that would reach the Chronicle API.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from secops_mcp.tools import legacy_soar_dashboard as mod

MODULE = "secops_mcp.tools.legacy_soar_dashboard"


@pytest.fixture
def chronicle_client():
    with patch(f"{MODULE}.get_chronicle_client") as factory:
        client = MagicMock(name="chronicle")
        factory.return_value = client
        yield client


@pytest.fixture
def api(chronicle_client):
    with patch(f"{MODULE}.chronicle_api_request") as request:
        request.return_value = {}
        yield request


def call_args(api):
    """Return (method, path, kwargs) of the single API call made."""
    assert api.call_count == 1
    args, kwargs = api.call_args
    _, method, path = args
    return method, path, kwargs


WIDGET = {
    "id": 7,
    "dashboardId": 12,
    "title": "Cases by priority",
    "widgetType": "CUSTOM",
    "widthSize": "ONE_BLOCK",
    "subject": "CASES",
    "dimensionA": "PRIORITY",
    "chartType": "PIE",
}


# ---------------------------------------------------------------------------
# GET verbs
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_dashboard_cards(api):
    api.return_value = {"payload": {"1": "SOC Overview", "2": "SLA"}}

    result = await mod.legacy_soar_get_dashboard_cards()

    method, path, kwargs = call_args(api)
    assert (method, path) == ("GET", "legacySoarDashboard:legacyGetDashboardCards")
    assert "params" not in kwargs and "json_body" not in kwargs
    assert result["total_dashboards"] == 2
    assert result["payload"]["1"] == "SOC Overview"


@pytest.mark.asyncio
async def test_get_dashboard_widget_definitions(api):
    api.return_value = {"payload": [{"id": 1}, {"id": 2}, {"id": 3}]}

    result = await mod.legacy_soar_get_dashboard_widget_definitions()

    method, path, _ = call_args(api)
    assert (method, path) == (
        "GET",
        "legacySoarDashboard:legacyGetDashboardWidgetDefinitions",
    )
    assert result["total_definitions"] == 3


@pytest.mark.asyncio
async def test_get_dashboard_playbooks(api):
    api.return_value = {"payload": [{"identifier": "pb-1"}]}

    result = await mod.legacy_soar_get_dashboard_playbooks()

    method, path, _ = call_args(api)
    assert (method, path) == ("GET", "legacySoarDashboard:legacyGetDashboardPlaybooks")
    assert result["total_playbooks"] == 1


@pytest.mark.asyncio
async def test_get_cases_time_to_respond(api):
    api.return_value = {"timeToResponseValue": 42}

    result = await mod.legacy_soar_get_cases_time_to_respond(
        time_range_filter="LAST_WEEK"
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "GET",
        "legacySoarDashboard:legacyGetCasesTimeToRespond",
    )
    assert kwargs["params"] == {"timeRangeFilter": "LAST_WEEK"}
    assert result == {"timeToResponseValue": 42}


@pytest.mark.asyncio
async def test_get_opened_and_closed_cases_trends(api):
    api.return_value = {"payload": [{"opened": 3, "closed": 2}]}

    result = await mod.legacy_soar_get_opened_and_closed_cases_trends(
        time_range_type="LAST_MONTH"
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "GET",
        "legacySoarDashboard:legacyGetOpenedAndClosedCasesTrends",
    )
    assert kwargs["params"] == {"timeRangeType": "LAST_MONTH"}
    assert result["total_results"] == 1


# ---------------------------------------------------------------------------
# POST verbs with an ID payload
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_dashboard(api):
    api.return_value = {"payload": {"id": 12, "widgets": [WIDGET]}}

    result = await mod.legacy_soar_get_dashboard(dashboard_id=12)

    method, path, kwargs = call_args(api)
    assert (method, path) == ("POST", "legacySoarDashboard:legacyGetDashboard")
    assert kwargs["json_body"] == {"legacyPayload": 12}
    assert result["payload"]["id"] == 12


@pytest.mark.asyncio
async def test_delete_dashboard(api):
    result = await mod.legacy_soar_delete_dashboard(dashboard_id=12)

    method, path, kwargs = call_args(api)
    assert (method, path) == ("POST", "legacySoarDashboard:legacyDeleteDashboard")
    assert kwargs["json_body"] == {"legacyPayload": 12}
    assert result == {"deleted": True, "dashboard_id": 12}


@pytest.mark.asyncio
async def test_delete_dashboard_widget(api):
    result = await mod.legacy_soar_delete_dashboard_widget(widget_id=7)

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyDeleteDashboardWidget",
    )
    assert kwargs["json_body"] == {"legacyPayload": 7}
    assert result == {"deleted": True, "widget_id": 7}


# ---------------------------------------------------------------------------
# Dashboard create / import / report template
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_add_or_update_dashboard_compacts_body(api):
    api.return_value = {"id": 99, "name": "SOC Overview"}

    result = await mod.legacy_soar_add_or_update_dashboard(
        dashboard_id=0,
        name="SOC Overview",
        default_time_range="LAST_WEEK",
        environments=["Default Environment"],
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyAddOrUpdateDashboard",
    )
    assert kwargs["json_body"] == {
        "id": 0,
        "name": "SOC Overview",
        "defaultTimeRange": "LAST_WEEK",
        "environments": ["Default Environment"],
    }
    assert result["id"] == 99


@pytest.mark.asyncio
async def test_add_or_update_dashboard_parses_json_string_lists(api):
    await mod.legacy_soar_add_or_update_dashboard(
        dashboard_id=12,
        allowed_users='["alice", "bob"]',
        widgets=json.dumps([WIDGET]),
    )

    _, _, kwargs = call_args(api)
    assert kwargs["json_body"]["allowedUsers"] == ["alice", "bob"]
    assert kwargs["json_body"]["widgets"] == [WIDGET]


@pytest.mark.asyncio
async def test_import_dashboard_overrides_name(api):
    exported = {"id": 5, "name": "Old", "widgets": [WIDGET], "environments": ["E"]}

    await mod.legacy_soar_import_dashboard(dashboard=json.dumps(exported), name="New")

    method, path, kwargs = call_args(api)
    assert (method, path) == ("POST", "legacySoarDashboard:legacyImportDashboard")
    assert kwargs["json_body"] == {**exported, "name": "New"}


@pytest.mark.asyncio
async def test_import_dashboard_requires_content(api):
    result = await mod.legacy_soar_import_dashboard()

    assert "error" in result
    api.assert_not_called()


@pytest.mark.asyncio
async def test_save_dashboard_as_report_template(api):
    await mod.legacy_soar_save_dashboard_as_report_template(
        name="Weekly SOC",
        category="MANAGEMENT",
        report_widgets=[WIDGET],
        has_scheduler=False,
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacySaveDashboardAsReportTemplate",
    )
    assert kwargs["json_body"] == {
        "name": "Weekly SOC",
        "category": "MANAGEMENT",
        "reportWidgets": [WIDGET],
        "hasScheduler": False,
    }


# ---------------------------------------------------------------------------
# Widget definition driven verbs
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_add_or_update_dashboard_widget_explicit_args(api):
    api.return_value = {"payload": {**WIDGET, "id": 101}}

    result = await mod.legacy_soar_add_or_update_dashboard_widget(
        widget_id=0,
        dashboard_id=12,
        title="Cases by priority",
        widget_type="CUSTOM",
        width_size="ONE_BLOCK",
        subject="CASES",
        dimension_a="PRIORITY",
        chart_type="PIE",
        time_filter="LAST_WEEK",
        extra_fields={"caseStatusesFilter": ["OPENED"]},
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyAddOrUpdateDashboardWidget",
    )
    assert kwargs["json_body"] == {
        "id": 0,
        "dashboardId": 12,
        "title": "Cases by priority",
        "widgetType": "CUSTOM",
        "widthSize": "ONE_BLOCK",
        "subject": "CASES",
        "dimensionA": "PRIORITY",
        "chartType": "PIE",
        "timeFilter": "LAST_WEEK",
        "caseStatusesFilter": ["OPENED"],
    }
    assert result["payload"]["id"] == 101


@pytest.mark.asyncio
async def test_add_or_update_dashboard_widget_missing_required(api):
    result = await mod.legacy_soar_add_or_update_dashboard_widget(
        widget_id=0, dashboard_id=12, title="No type"
    )

    assert "widgetType" in result["error"] and "widthSize" in result["error"]
    api.assert_not_called()


@pytest.mark.asyncio
async def test_get_dashboard_widget_values_widget_passthrough_json_string(api):
    api.return_value = {"payload": {"series": []}}

    result = await mod.legacy_soar_get_dashboard_widget_values(
        widget=json.dumps(WIDGET), time_filter="LAST_MONTH"
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyGetDashboardWidgetValues",
    )
    assert kwargs["json_body"] == {**WIDGET, "timeFilter": "LAST_MONTH"}
    assert result == {"payload": {"series": []}}


@pytest.mark.asyncio
async def test_get_dashboard_widget_case_ids(api):
    api.return_value = {"payload": [1, 2, 3]}

    result = await mod.legacy_soar_get_dashboard_widget_case_ids(widget=WIDGET)

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyGetDashboardWidgetCaseIds",
    )
    assert kwargs["json_body"] == WIDGET
    assert result["total_results"] == 3


@pytest.mark.asyncio
async def test_get_dashboard_custom_widget_case_ids(api):
    api.return_value = {"payload": [9]}

    result = await mod.legacy_soar_get_dashboard_custom_widget_case_ids(
        widget=WIDGET, extra_fields='{"analystFilters": ["alice"]}'
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyGetDashboardCustomWidgetCaseIds",
    )
    assert kwargs["json_body"] == {**WIDGET, "analystFilters": ["alice"]}
    assert result["total_results"] == 1


@pytest.mark.asyncio
async def test_get_dashboard_playbook_runs(api):
    api.return_value = {"payload": [{"status": "ERROR"}]}

    result = await mod.legacy_soar_get_dashboard_playbook_runs(
        widget=WIDGET,
        subject="PLAYBOOKS",
        extra_fields={"playbookStatusFilter": ["ERROR"]},
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyGetDashboardPlaybookRuns",
    )
    assert kwargs["json_body"]["subject"] == "PLAYBOOKS"
    assert kwargs["json_body"]["playbookStatusFilter"] == ["ERROR"]
    assert result["total_results"] == 1


@pytest.mark.asyncio
async def test_get_playbook_monitoring(api):
    api.return_value = {"payload": {"name": "Playbook monitoring"}}

    result = await mod.legacy_soar_get_playbook_monitoring(
        workflow_identifier="pb-1", time_filter="LAST_WEEK"
    )

    method, path, kwargs = call_args(api)
    assert (method, path) == (
        "POST",
        "legacySoarDashboard:legacyGetPlaybookMonitoring",
    )
    assert kwargs["json_body"] == {
        "workflowIdentifier": "pb-1",
        "timeFilter": "LAST_WEEK",
    }
    assert result["payload"]["name"] == "Playbook monitoring"


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_api_failure_returns_error_dict(api):
    api.side_effect = RuntimeError("Chronicle API GET ... failed with status 403")

    result = await mod.legacy_soar_get_dashboard_cards()

    assert result == {
        "error": "Error listing legacy SOAR dashboard cards: Chronicle API GET "
        "... failed with status 403"
    }


@pytest.mark.asyncio
async def test_invalid_json_string_returns_error(api):
    result = await mod.legacy_soar_get_dashboard_widget_values(widget="{not json")

    assert "widget must be valid JSON" in result["error"]
    api.assert_not_called()


@pytest.mark.asyncio
async def test_client_factory_receives_tenant_args(api, chronicle_client):
    with patch(f"{MODULE}.get_chronicle_client") as factory:
        factory.return_value = chronicle_client
        await mod.legacy_soar_get_dashboard_cards(
            project_id="p", customer_id="c", region="europe"
        )
        factory.assert_called_once_with("p", "c", "europe")
