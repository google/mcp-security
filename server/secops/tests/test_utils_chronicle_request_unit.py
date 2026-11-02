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
"""Unit tests for the shared Chronicle REST helpers in secops_mcp.utils."""

from unittest.mock import MagicMock

import pytest

from secops_mcp.utils import (
    chronicle_api_request,
    instance_base_url,
    parse_json_arg,
)

INSTANCE = "projects/p/locations/us/instances/abc"


def _client(base_url):
    client = MagicMock()
    client.base_url = base_url
    client.instance_id = INSTANCE
    response = MagicMock()
    response.status_code = 200
    response.content = b'{"ok": true}'
    response.json.return_value = {"ok": True}
    client.session.request.return_value = response
    return client


def test_instance_base_url_with_string_base_url_swaps_version():
    client = _client("https://us-chronicle.googleapis.com/v1alpha")
    assert (
        instance_base_url(client, "v1")
        == f"https://us-chronicle.googleapis.com/v1/{INSTANCE}"
    )


def test_instance_base_url_with_callable_base_url_passes_version():
    def base_url(version):
        return f"https://us-chronicle.googleapis.com/{version}"

    client = _client(base_url)
    assert (
        instance_base_url(client, "v1beta")
        == f"https://us-chronicle.googleapis.com/v1beta/{INSTANCE}"
    )


def test_chronicle_api_request_subresource_path_and_param_filtering():
    client = _client("https://us-chronicle.googleapis.com/v1alpha")
    result = chronicle_api_request(
        client,
        "GET",
        "/nativeDashboards",
        params={"pageSize": 10, "pageToken": None},
    )
    assert result == {"ok": True}
    client.session.request.assert_called_once_with(
        "GET",
        f"https://us-chronicle.googleapis.com/v1alpha/{INSTANCE}/nativeDashboards",
        params={"pageSize": 10},
        json=None,
        timeout=120,
    )


def test_chronicle_api_request_instance_custom_verb_path():
    client = _client("https://us-chronicle.googleapis.com/v1alpha")
    chronicle_api_request(
        client, "POST", "legacySoarDashboard:legacyGetDashboard", json_body={"a": 1}
    )
    url = client.session.request.call_args.args[1]
    assert url.endswith(f"{INSTANCE}/legacySoarDashboard:legacyGetDashboard")
    assert client.session.request.call_args.kwargs["json"] == {"a": 1}


def test_chronicle_api_request_absolute_resource_name():
    client = _client("https://us-chronicle.googleapis.com/v1alpha")
    chronicle_api_request(client, "GET", f"{INSTANCE}/dashboardCharts/c1")
    url = client.session.request.call_args.args[1]
    assert url == (
        f"https://us-chronicle.googleapis.com/v1alpha/{INSTANCE}/dashboardCharts/c1"
    )


def test_chronicle_api_request_raises_on_http_error():
    client = _client("https://us-chronicle.googleapis.com/v1alpha")
    client.session.request.return_value.status_code = 404
    client.session.request.return_value.text = "not found"
    with pytest.raises(RuntimeError, match="status 404: not found"):
        chronicle_api_request(client, "GET", "/nativeDashboards/missing")


def test_chronicle_api_request_empty_body_returns_empty_dict():
    client = _client("https://us-chronicle.googleapis.com/v1alpha")
    client.session.request.return_value.content = b""
    assert chronicle_api_request(client, "DELETE", "/nativeDashboards/d1") == {}


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, None),
        ("", None),
        ({"a": 1}, {"a": 1}),
        ([1, 2], [1, 2]),
        ('{"a": 1}', {"a": 1}),
        ("[1, 2]", [1, 2]),
    ],
)
def test_parse_json_arg_accepts_native_and_string_forms(value, expected):
    assert parse_json_arg(value, "x") == expected


def test_parse_json_arg_rejects_invalid_json():
    with pytest.raises(ValueError, match="x must be valid JSON"):
        parse_json_arg("{not json", "x")
