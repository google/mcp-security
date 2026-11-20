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
"""SecOps tool parameters that default to None must accept an explicit null."""

from unittest.mock import MagicMock, patch

import pytest

mcp_memory = pytest.importorskip("mcp.shared.memory")
client_session = mcp_memory.create_connected_server_and_client_session

from secops_mcp.server import server  # noqa: E402


@pytest.mark.asyncio
async def test_none_default_params_accept_null() -> None:
    """Params defaulting to None must accept an explicit null.

    Some MCP clients send every optional argument, using the advertised
    default (null). If the schema type excludes null, the call is rejected
    at argument validation instead of falling back to the default.
    """
    async with client_session(server._mcp_server) as client:
        tools_result = await client.list_tools()

    offenders = []
    for tool in tools_result.tools:
        for name, prop in tool.inputSchema.get("properties", {}).items():
            if "default" not in prop or prop["default"] is not None:
                continue
            types = [prop.get("type")] + [
                option.get("type") for option in prop.get("anyOf", [])
            ]
            if "null" not in types:
                offenders.append(f"{tool.name}.{name}")

    assert offenders == []


@pytest.mark.asyncio
async def test_search_udm_accepts_null_project_id() -> None:
    """Explicit null project, customer and region behave like omitting them."""
    chronicle = MagicMock()
    chronicle.search_udm.return_value = {"events": [], "total_events": 0}

    with patch(
        "secops_mcp.tools.search.get_chronicle_client", return_value=chronicle
    ) as get_client:
        async with client_session(server._mcp_server) as client:
            result = await client.call_tool(
                "search_udm",
                arguments={
                    "query": 'metadata.event_type = "USER_LOGIN"',
                    "project_id": None,
                    "customer_id": None,
                    "region": None,
                },
            )

    assert not result.isError, result.content[0].text
    get_client.assert_called_once_with(None, None, None)
