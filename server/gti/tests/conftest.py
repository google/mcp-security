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
import pytest_asyncio
import pytest_httpserver
from unittest import mock
import vt


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def mock_vt_client(
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
