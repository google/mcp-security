# Copyright 2025 Google LLC
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
import pytest
import pytest_asyncio
import pytest_httpserver
from unittest import mock
import vt
import typing


@pytest.fixture(name='vt_endpoint')
def fixture_vt_endpoint(request) -> str:
  return request.param


@pytest.fixture(name='vt_object_response')
def fixture_vt_object_response(request) -> dict[str, typing.Any]:
  return request.param


@pytest.fixture(name='abridged_relationships')
def fixture_abridged_relationships(request) -> list[str]:
  return request.param


@pytest_asyncio.fixture(name="mock_vt_client", loop_scope="session", autouse=True)
async def fixture_mock_vt_client(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer, session_mocker
):
  """Mocks the VirusTotal client."""
  client = vt.Client(
      "dummy_api_key",
      host=f"http://{make_httpserver_ipv4.host}:{make_httpserver_ipv4.port}",
      timeout=500,
  )
  m = mock.AsyncMock()
  m.return_value = client
  session_mocker.patch("gti_mcp.server.new_vt_client", side_effect=m)
  return m


@pytest.fixture(name="vt_get_object_mock")
def fixture_vt_get_object_mock(
    make_httpserver_ipv4, vt_endpoint, vt_object_response, abridged_relationships):
  # Mock get object request.
  make_httpserver_ipv4.expect_request(
      vt_endpoint,
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(vt_object_response)
  # Mock get relationships requests.
  for rel_name in abridged_relationships:
    make_httpserver_ipv4.expect_request(
        f"{vt_endpoint}/{rel_name}",
        method="GET",
        headers={"X-Apikey": "dummy_api_key"},
    ).respond_with_json({
        "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
    })
  return make_httpserver_ipv4


@pytest.fixture(name="vt_get_request_mock")
def fixture_vt_get_request_mock(
    make_httpserver_ipv4, vt_endpoint, vt_object_response):
  # Mock get object request.
  make_httpserver_ipv4.expect_request(
      vt_endpoint,
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(vt_object_response)
  return make_httpserver_ipv4
