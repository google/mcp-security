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

"""Unit tests for SecOps SOAR HttpClient session configuration."""

from unittest import mock

import pytest
from secops_soar_mcp.http_client import HttpClient


@pytest.mark.asyncio
async def test_http_client_session_trusts_env():
    """Ensure HttpClient initializes ClientSession with trust_env=True for proxies."""
    client = HttpClient("https://example.com", "app-key")
    session = client._get_session()
    try:
        assert session.trust_env is True
    finally:
        await session.close()


def test_http_client_passes_trust_env_to_client_session():
    """Ensure HttpClient explicitly passes trust_env=True to aiohttp.ClientSession."""
    client = HttpClient("https://example.com", "app-key")
    with mock.patch("aiohttp.ClientSession") as mock_session_cls:
        session = client._get_session()
        mock_session_cls.assert_called_once_with(trust_env=True)
        assert session == mock_session_cls.return_value
