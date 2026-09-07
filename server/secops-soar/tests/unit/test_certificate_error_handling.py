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

"""Tests that certificate errors get a helpful message instead of the
generic "wrong SOAR credentials" one, and that HttpClient doesn't swallow
SSL errors as a plain None result (see issue #191)."""

import ssl
from unittest import mock

import aiohttp
import pytest

from secops_soar_mcp import bindings
from secops_soar_mcp.http_client import HttpClient


class _RaisingSession:
    """Minimal aiohttp session stand-in whose .get() raises."""

    def __init__(self, exc: Exception):
        self._exc = exc

    def get(self, *args, **kwargs):
        raise self._exc

    async def close(self):
        pass


@pytest.mark.asyncio
async def test_http_client_get_reraises_ssl_error():
    client = HttpClient("https://example.com", "app-key")
    client._session = _RaisingSession(ssl.SSLCertVerificationError("bad cert"))

    with pytest.raises(ssl.SSLError):
        await client.get("/some/endpoint")


@pytest.mark.asyncio
async def test_http_client_get_swallows_generic_connection_error():
    client = HttpClient("https://example.com", "app-key")
    client._session = _RaisingSession(aiohttp.ClientConnectionError("refused"))

    assert await client.get("/some/endpoint") is None


@pytest.mark.asyncio
async def test_get_valid_scopes_reports_certificate_issue_not_credentials():
    with (
        mock.patch.object(
            bindings,
            "http_client",
            new=mock.AsyncMock(get=mock.AsyncMock(side_effect=ssl.SSLCertVerificationError())),
        ),
        pytest.raises(RuntimeError) as exc_info,
    ):
        await bindings._get_valid_scopes()

    message = str(exc_info.value)
    assert "certifi" in message.lower()
    assert "certificate" in message.lower()
    assert "not" in message.lower() and "credentials" in message.lower()


@pytest.mark.asyncio
async def test_get_valid_scopes_still_blames_credentials_when_no_data():
    with (
        mock.patch.object(
            bindings,
            "http_client",
            new=mock.AsyncMock(get=mock.AsyncMock(return_value=None)),
        ),
        pytest.raises(RuntimeError) as exc_info,
    ):
        await bindings._get_valid_scopes()

    assert "credentials" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_get_valid_scopes_reports_certificate_issue_on_client_ssl_error():
    conn_key = aiohttp.client_reqrep.ConnectionKey("example.com", 443, True, True, None, None, None)
    client_ssl_err = aiohttp.ClientSSLError(conn_key, OSError("handshake failed"))
    with (
        mock.patch.object(
            bindings,
            "http_client",
            new=mock.AsyncMock(get=mock.AsyncMock(side_effect=client_ssl_err)),
        ),
        pytest.raises(RuntimeError) as exc_info,
    ):
        await bindings._get_valid_scopes()
    assert "certificate" in str(exc_info.value).lower()
