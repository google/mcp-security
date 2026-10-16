# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Proxy routing for the SOAR HTTP client."""

import json
from unittest import mock

import pytest

from secops_soar_mcp import bindings
from secops_soar_mcp.http_client import HttpClient


class _Response:
    status = 200

    def __init__(self):
        self.content = mock.Mock(read=mock.AsyncMock(return_value=json.dumps({"ok": True}).encode()))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def raise_for_status(self):
        pass

    async def json(self):
        return {"ok": True}


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["get", "post", "patch"])
@pytest.mark.parametrize("proxy", [None, "http://proxy.example.com:8080"])
async def test_http_client_routes_requests_with_optional_proxy(method, proxy):
    client = HttpClient("https://soar.example.com", "app-key", proxy=proxy)
    session = mock.Mock()
    response = _Response()
    getattr(session, method).return_value = response
    client._session = session

    params = {"page": 1}
    body = {"name": "case"}
    if method == "get":
        result = await client.get("/cases", params=params)
        expected = {"params": params, "headers": {"AppKey": "app-key"}, "proxy": proxy}
    else:
        result = await getattr(client, method)("/cases", req=body, params=params)
        expected = {
            "json": body,
            "params": params,
            "headers": {"AppKey": "app-key"},
            "proxy": proxy,
        }

    assert result == {"ok": True}
    getattr(session, method).assert_called_once_with("https://soar.example.com/cases", **expected)


@pytest.mark.asyncio
@pytest.mark.parametrize("proxy", [None, "http://proxy.example.com:8080"])
async def test_bind_passes_optional_soar_proxy_from_environment(monkeypatch, proxy):
    monkeypatch.setenv("SOAR_URL", "https://soar.example.com")
    monkeypatch.setenv("SOAR_APP_KEY", "app-key")
    if proxy is None:
        monkeypatch.delenv("SOAR_PROXY", raising=False)
    else:
        monkeypatch.setenv("SOAR_PROXY", proxy)

    with mock.patch.object(bindings, "_get_valid_scopes", new=mock.AsyncMock(return_value=set())):
        await bindings.bind()

    assert bindings.http_client.base_url == "https://soar.example.com"
    assert bindings.http_client.app_key == "app-key"
    assert bindings.http_client.proxy == proxy
    await bindings.cleanup()
