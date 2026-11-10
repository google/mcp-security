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
"""Unit tests for native SIEM dashboard management tools."""

import json
from unittest.mock import MagicMock, patch

import pytest

from secops_mcp.tools import dashboard_management as dm

MODULE = "secops_mcp.tools.dashboard_management"
INSTANCE = "projects/p/locations/us/instances/c"


@pytest.fixture
def chronicle_client():
    with patch(f"{MODULE}.get_chronicle_client") as factory:
        client = MagicMock()
        client.instance_id = INSTANCE
        factory.return_value = client
        yield client


@pytest.fixture
def api(chronicle_client):
    with patch(f"{MODULE}.chronicle_api_request") as req:
        req.return_value = {"ok": True}
        yield req


def call(api):
    """Return (method, path, params, json_body) of the single API call."""
    api.assert_called_once()
    args, kwargs = api.call_args
    return args[1], args[2], kwargs.get("params"), kwargs.get("json_body")


# --- NativeDashboardService ---------------------------------------------------


@pytest.mark.asyncio
async def test_list_dashboards(api):
    api.return_value = {"nativeDashboards": [{"name": "a"}, {"name": "b"}]}
    result = await dm.list_dashboards(
        view="NATIVE_DASHBOARD_VIEW_FULL", page_size=10, page_token="t"
    )
    method, path, params, body = call(api)
    assert (method, path) == ("GET", "/nativeDashboards")
    assert params == {
        "pageSize": 10,
        "pageToken": "t",
        "view": "NATIVE_DASHBOARD_VIEW_FULL",
    }
    assert body is None
    assert result["total_dashboards"] == 2


@pytest.mark.asyncio
async def test_get_dashboard_normalizes_resource_name(api):
    await dm.get_dashboard(
        f"{INSTANCE}/nativeDashboards/d1", view="NATIVE_DASHBOARD_VIEW_BASIC"
    )
    method, path, params, _ = call(api)
    assert (method, path) == ("GET", "/nativeDashboards/d1")
    assert params == {"view": "NATIVE_DASHBOARD_VIEW_BASIC"}


@pytest.mark.asyncio
async def test_create_dashboard_merges_passthrough(api):
    await dm.create_dashboard(
        "SOC",
        description="desc",
        access_type="DASHBOARD_PUBLIC",
        filters=[{"id": "f1"}],
        dashboard={"etag": "x"},
    )
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards")
    assert body == {
        "displayName": "SOC",
        "description": "desc",
        "access": "DASHBOARD_PUBLIC",
        "type": "CUSTOM",
        "definition": {"filters": [{"id": "f1"}]},
        "etag": "x",
    }


@pytest.mark.asyncio
async def test_create_dashboard_parses_json_string_filters(api):
    await dm.create_dashboard("SOC", filters=json.dumps([{"id": "f1"}]))
    _, _, _, body = call(api)
    assert body["definition"] == {"filters": [{"id": "f1"}]}
    assert "description" not in body


@pytest.mark.asyncio
async def test_update_dashboard_builds_mask(api):
    await dm.update_dashboard(
        "d1",
        display_name="New",
        filters=[],
        dashboard={"definition": {"charts": []}},
        update_mask="definition.charts",
        etag="e1",
    )
    method, path, params, body = call(api)
    assert (method, path) == ("PATCH", "/nativeDashboards/d1")
    assert params == {"updateMask": "displayName,definition.filters,definition.charts"}
    assert body == {
        "displayName": "New",
        "etag": "e1",
        "definition": {"charts": []},
    }


@pytest.mark.asyncio
async def test_update_dashboard_requires_a_field(api):
    result = await dm.update_dashboard("d1")
    assert "error" in result
    api.assert_not_called()


@pytest.mark.asyncio
async def test_duplicate_dashboard(api):
    await dm.duplicate_dashboard("d1", "Copy", access_type="DASHBOARD_PRIVATE")
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards/d1:duplicate")
    assert body == {
        "nativeDashboard": {
            "displayName": "Copy",
            "access": "DASHBOARD_PRIVATE",
            "type": "CUSTOM",
        }
    }


@pytest.mark.asyncio
async def test_delete_dashboard(api):
    api.return_value = {}
    result = await dm.delete_dashboard("d1")
    method, path, _, _ = call(api)
    assert (method, path) == ("DELETE", "/nativeDashboards/d1")
    assert result["status"] == "deleted"


@pytest.mark.asyncio
async def test_add_dashboard_chart_defaults(api):
    await dm.add_dashboard_chart(
        "d1",
        "Logins",
        query="metadata.event_type = \"USER_LOGIN\"",
        visualization={"series": [{"chartType": "TABLE"}]},
    )
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards/d1:addChart")
    assert body == {
        "dashboardChart": {
            "displayName": "Logins",
            "visualization": {"series": [{"chartType": "TABLE"}]},
            "chartDatasource": {"dataSources": ["UDM"]},
        },
        "dashboardQuery": {
            "query": "metadata.event_type = \"USER_LOGIN\"",
            "input": {"relativeTime": {"timeUnit": "DAY", "startTimeVal": 1}},
        },
        "chartLayout": {"startX": 0, "startY": 0, "spanX": 48, "spanY": 26},
    }


@pytest.mark.asyncio
async def test_add_dashboard_chart_absolute_window_and_layout(api):
    await dm.add_dashboard_chart(
        "d1",
        "Chart",
        query="q",
        start_time="2026-01-01T00:00:00Z",
        end_time="2026-01-02T00:00:00Z",
        start_x=6,
        start_y=0,
        span_x=3,
        span_y=2,
        chart_layout=json.dumps({"spanY": 8}),
    )
    _, _, _, body = call(api)
    assert body["dashboardQuery"]["input"] == {
        "timeWindow": {
            "startTime": "2026-01-01T00:00:00Z",
            "endTime": "2026-01-02T00:00:00Z",
        }
    }
    assert body["chartLayout"] == {"startX": 6, "startY": 0, "spanX": 3, "spanY": 8}


@pytest.mark.asyncio
async def test_add_dashboard_chart_markdown_tile_has_no_query(api):
    await dm.add_dashboard_chart(
        "d1", "Notes", tile_type="TILE_TYPE_MARKDOWN", chart={"markdown": {"text": "x"}}
    )
    _, _, _, body = call(api)
    assert "dashboardQuery" not in body
    assert "chartDatasource" not in body["dashboardChart"]
    assert body["dashboardChart"]["tileType"] == "TILE_TYPE_MARKDOWN"
    assert body["dashboardChart"]["markdown"] == {"text": "x"}


@pytest.mark.asyncio
async def test_edit_dashboard_chart_fetches_etag_and_query_name(api):
    api.side_effect = [
        {
            "name": f"{INSTANCE}/dashboardCharts/c1",
            "etag": "etag-1",
            "chartDatasource": {"dashboardQuery": f"{INSTANCE}/dashboardQueries/q1"},
        },
        {"name": f"{INSTANCE}/dashboardQueries/q1", "etag": "qetag-1"},
        {"ok": True},
    ]
    await dm.edit_dashboard_chart(
        "d1",
        "c1",
        edit_mask="dashboardQuery.input,dashboardChart.displayName",
        display_name="Renamed",
        time_unit="DAY",
        start_time_val=7,
        language_features=["STAGES"],
    )
    assert api.call_count == 3
    get_args = api.call_args_list[0].args
    assert (get_args[1], get_args[2]) == ("GET", "/dashboardCharts/c1")
    get_q = api.call_args_list[1].args
    assert (get_q[1], get_q[2]) == ("GET", "/dashboardQueries/q1")
    args, kwargs = api.call_args_list[2]
    assert (args[1], args[2]) == ("POST", "/nativeDashboards/d1:editChart")
    assert kwargs["json_body"] == {
        "dashboardChart": {
            "name": f"{INSTANCE}/dashboardCharts/c1",
            "displayName": "Renamed",
            "etag": "etag-1",
        },
        "dashboardQuery": {
            "name": f"{INSTANCE}/dashboardQueries/q1",
            "etag": "qetag-1",
            "input": {"relativeTime": {"timeUnit": "DAY", "startTimeVal": 7}},
        },
        "editMask": "dashboardQuery.input,dashboardChart.displayName",
        "languageFeatures": ["STAGES"],
    }


@pytest.mark.asyncio
async def test_edit_dashboard_chart_with_explicit_etag_skips_fetch(api):
    await dm.edit_dashboard_chart(
        "d1", "c1", edit_mask="dashboardChart.displayName", display_name="X", etag="e9"
    )
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards/d1:editChart")
    assert body["dashboardChart"]["etag"] == "e9"
    assert "dashboardQuery" not in body


@pytest.mark.asyncio
async def test_remove_dashboard_chart_uses_full_chart_name(api):
    await dm.remove_dashboard_chart("d1", "c1")
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards/d1:removeChart")
    assert body == {"dashboardChart": f"{INSTANCE}/dashboardCharts/c1"}


@pytest.mark.asyncio
async def test_duplicate_dashboard_chart_accepts_full_name(api):
    full = f"{INSTANCE}/dashboardCharts/c1"
    await dm.duplicate_dashboard_chart(f"{INSTANCE}/nativeDashboards/d1", full)
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards/d1:duplicateChart")
    assert body == {"dashboardChart": full}


@pytest.mark.asyncio
async def test_export_dashboards(api):
    await dm.export_dashboards(["d1", f"{INSTANCE}/nativeDashboards/d2"])
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards:export")
    assert body == {
        "names": [
            f"{INSTANCE}/nativeDashboards/d1",
            f"{INSTANCE}/nativeDashboards/d2",
        ]
    }


@pytest.mark.asyncio
async def test_export_dashboards_single_string_id(api):
    await dm.export_dashboards("d1")
    _, _, _, body = call(api)
    assert body == {"names": [f"{INSTANCE}/nativeDashboards/d1"]}


@pytest.mark.asyncio
async def test_import_dashboards_accepts_export_response(api):
    item = {"dashboard": {"displayName": "X"}, "dashboardCharts": []}
    await dm.import_dashboards({"inlineDestination": {"dashboards": [item]}})
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/nativeDashboards:import")
    assert body == {"source": {"dashboards": [item]}}


@pytest.mark.asyncio
async def test_import_dashboards_json_string_list(api):
    item = {"dashboard": {"displayName": "X"}}
    await dm.import_dashboards(json.dumps([item]))
    _, _, _, body = call(api)
    assert body == {"source": {"dashboards": [item]}}


@pytest.mark.asyncio
async def test_execute_dashboard_query_defaults_to_past_day(api):
    await dm.execute_dashboard_query(query="q", clear_cache=True)
    method, path, _, body = call(api)
    assert (method, path) == ("POST", "/dashboardQueries:execute")
    assert body == {
        "query": {
            "query": "q",
            "input": {"relativeTime": {"timeUnit": "DAY", "startTimeVal": 1}},
        },
        "clearCache": True,
    }


@pytest.mark.asyncio
async def test_execute_dashboard_query_saved_query_and_filters(api):
    filters = [{"fieldPath": "principal.hostname"}]
    await dm.execute_dashboard_query(
        query_id="q1",
        time_unit="HOUR",
        start_time_val=6,
        dialect="YL2",
        filters=json.dumps(filters),
        use_previous_time_range=True,
    )
    _, _, _, body = call(api)
    assert body == {
        "query": {
            "name": f"{INSTANCE}/dashboardQueries/q1",
            "input": {"relativeTime": {"timeUnit": "HOUR", "startTimeVal": 6}},
            "dialect": "YL2",
        },
        "filters": filters,
        "usePreviousTimeRange": True,
    }


@pytest.mark.asyncio
async def test_execute_dashboard_query_requires_query(api):
    result = await dm.execute_dashboard_query()
    assert "error" in result
    api.assert_not_called()


@pytest.mark.asyncio
async def test_get_dashboard_query(api):
    await dm.get_dashboard_query(f"{INSTANCE}/dashboardQueries/q1")
    method, path, params, _ = call(api)
    assert (method, path) == ("GET", "/dashboardQueries/q1")
    assert params is None


# --- DashboardChartService ----------------------------------------------------


@pytest.mark.asyncio
async def test_get_dashboard_chart(api):
    await dm.get_dashboard_chart("c1")
    method, path, _, _ = call(api)
    assert (method, path) == ("GET", "/dashboardCharts/c1")


@pytest.mark.asyncio
async def test_list_dashboard_charts(api):
    api.return_value = {"dashboardCharts": [{"name": "c1"}], "totalSize": 1}
    result = await dm.list_dashboard_charts(filter='display_name = "x"', page_size=5)
    method, path, params, _ = call(api)
    assert (method, path) == ("GET", "/dashboardCharts")
    assert params == {"pageSize": 5, "pageToken": None, "filter": 'display_name = "x"'}
    assert result["total_charts"] == 1


@pytest.mark.asyncio
async def test_batch_get_dashboard_charts(api):
    api.return_value = {"dashboardCharts": [{}, {}]}
    result = await dm.batch_get_dashboard_charts(["c1", f"{INSTANCE}/dashboardCharts/c2"])
    method, path, params, body = call(api)
    assert (method, path) == ("GET", "/dashboardCharts:batchGet")
    assert params == {
        "names": [f"{INSTANCE}/dashboardCharts/c1", f"{INSTANCE}/dashboardCharts/c2"]
    }
    assert body is None
    assert result["total_charts"] == 2


# --- Error paths --------------------------------------------------------------


@pytest.mark.asyncio
async def test_api_failure_returns_error_dict(api):
    api.side_effect = RuntimeError("HTTP 404: not found")
    result = await dm.get_dashboard("missing")
    assert result == {"error": "Error getting dashboard: HTTP 404: not found"}


@pytest.mark.asyncio
async def test_invalid_json_string_returns_error(api):
    result = await dm.create_dashboard("SOC", filters="{not json")
    assert "error" in result
    assert "filters must be valid JSON" in result["error"]
    api.assert_not_called()
