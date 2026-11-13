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
"""SCC tool parameters that default to None must accept an explicit null."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

mcp_memory = pytest.importorskip("mcp.shared.memory")
client_session = mcp_memory.create_connected_server_and_client_session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import scc_mcp  # noqa: E402


@pytest.mark.asyncio
async def test_none_default_params_accept_null() -> None:
    """Params defaulting to None must accept an explicit null.

    Some MCP clients send every optional argument, using the advertised
    default (null). If the schema type excludes null, the call is rejected
    at argument validation instead of falling back to the default.
    """
    async with client_session(scc_mcp.mcp._mcp_server) as client:
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
async def test_search_findings_accepts_null_severity() -> None:
    """An explicit null `severity` behaves like omitting it."""
    scc_client = MagicMock()
    scc_client.list_findings.return_value.pages = []

    with patch.object(scc_mcp, "scc_client", scc_client):
        async with client_session(scc_mcp.mcp._mcp_server) as client:
            result = await client.call_tool(
                "search_findings",
                arguments={"project_id": "my-proj", "severity": None},
            )

    assert not result.isError, result.content[0].text
    request = scc_client.list_findings.call_args.kwargs["request"]
    assert request["filter"] == 'state="ACTIVE"'
