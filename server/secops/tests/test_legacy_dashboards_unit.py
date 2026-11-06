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
"""Unit tests for legacy (Looker) dashboard and migration MCP tools."""

from unittest.mock import MagicMock, patch

import pytest

from secops_mcp.tools.legacy_dashboards import (
    copy_legacy_dashboard,
    delete_legacy_dashboard,
    get_legacy_dashboard,
    list_legacy_dashboards,
)

MODULE = "secops_mcp.tools.legacy_dashboards"
INSTANCE = "projects/p1/locations/us/instances/inst-1"


@pytest.fixture
def chronicle_client():
    with patch(f"{MODULE}.get_chronicle_client") as factory:
        client = MagicMock()
        client.instance_id = INSTANCE
        factory.return_value = client
        yield client


@pytest.fixture
def api_request():
    with patch(f"{MODULE}.chronicle_api_request") as request:
        yield request


def call_of(api_request):
    """Return (method, path, params, json_body) of the single API call."""
    api_request.assert_called_once()
    args, kwargs = api_request.call_args
    return args[1], args[2], kwargs.get("params"), kwargs.get("json_body")


@pytest.mark.asyncio
async def test_get_legacy_dashboard_accepts_full_name(
    chronicle_client, api_request
):
    api_request.return_value = {"name": f"{INSTANCE}/dashboards/d1"}

    result = await get_legacy_dashboard(
        f"{INSTANCE}/dashboards/d1", view="DASHBOARD_VIEW_EXPORT"
    )

    assert result == {"name": f"{INSTANCE}/dashboards/d1"}
    assert call_of(api_request) == (
        "GET",
        "/dashboards/d1",
        {"view": "DASHBOARD_VIEW_EXPORT"},
        None,
    )


@pytest.mark.asyncio
async def test_list_legacy_dashboards(chronicle_client, api_request):
    api_request.return_value = {
        "dashboards": [{"name": "a"}, {"name": "b"}],
        "nextPageToken": "tok2",
    }

    result = await list_legacy_dashboards(page_size=2, page_token="tok1")

    assert result["total_dashboards"] == 2
    assert result["nextPageToken"] == "tok2"
    assert call_of(api_request) == (
        "GET",
        "/dashboards",
        {"pageSize": 2, "pageToken": "tok1", "view": None},
        None,
    )


@pytest.mark.asyncio
async def test_delete_legacy_dashboard(chronicle_client, api_request):
    api_request.return_value = {}

    result = await delete_legacy_dashboard("d1")

    assert result == {"status": "deleted", "dashboard_id": "d1"}
    assert call_of(api_request) == ("DELETE", "/dashboards/d1", None, None)


@pytest.mark.asyncio
async def test_copy_legacy_dashboard(chronicle_client, api_request):
    api_request.return_value = {"name": f"{INSTANCE}/dashboards/d2"}

    result = await copy_legacy_dashboard(
        "d1", dashboard_type="DASHBOARD_TYPE_USER", display_name="Copy"
    )

    assert result == {"name": f"{INSTANCE}/dashboards/d2"}
    assert call_of(api_request) == (
        "POST",
        "/dashboards/d1:copy",
        None,
        {
            "destination": {
                "parent": INSTANCE,
                "dashboard": {
                    "displayName": "Copy",
                    "type": "DASHBOARD_TYPE_USER",
                },
            }
        },
    )


@pytest.mark.asyncio
async def test_copy_legacy_dashboard_json_string_destination(
    chronicle_client, api_request
):
    api_request.return_value = {}

    await copy_legacy_dashboard(
        "d1", destination='{"type": "DASHBOARD_TYPE_CUSTOMER", "displayName": "X"}'
    )

    _, _, _, body = call_of(api_request)
    assert body["destination"]["dashboard"] == {
        "type": "DASHBOARD_TYPE_CUSTOMER",
        "displayName": "X",
    }


@pytest.mark.asyncio
async def test_copy_legacy_dashboard_requires_type(
    chronicle_client, api_request
):
    result = await copy_legacy_dashboard("d1", display_name="no type")

    assert "error" in result
    api_request.assert_not_called()


@pytest.mark.asyncio
async def test_error_path_returns_error_dict(chronicle_client, api_request):
    api_request.side_effect = RuntimeError("boom 403")

    result = await get_legacy_dashboard("d1")

    assert result == {"error": "Error getting legacy dashboard: boom 403"}
