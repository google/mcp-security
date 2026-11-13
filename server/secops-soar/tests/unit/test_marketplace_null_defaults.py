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
"""Marketplace tool parameters that default to None must accept an explicit null."""

import importlib.util
import json
import sys
from pathlib import Path
from unittest import mock

import pytest

mcp_memory = pytest.importorskip("mcp.shared.memory")
client_session = mcp_memory.create_connected_server_and_client_session

from mcp.server.fastmcp import FastMCP  # noqa: E402

MARKETPLACE_DIR = (
    Path(__file__).resolve().parents[2]
    / "secops_soar_mcp"
    / "marketplace"
)


def _load_marketplace_module(path: Path):
    """Import a marketplace module from its file.

    Loading by path also covers modules with dots in their filenames
    (e.g. tenable.io.py), which a dotted import name cannot reach.
    """
    name = "secops_soar_mcp.marketplace." + path.stem.replace(".", "_")
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.asyncio
async def test_none_default_params_accept_null() -> None:
    """Params defaulting to None must accept an explicit null.

    Some MCP clients send every optional argument, using the advertised
    default (null). If the schema type excludes null, the call is rejected
    at argument validation instead of falling back to the default.
    """
    server = FastMCP("marketplace-null-defaults")
    for path in sorted(MARKETPLACE_DIR.glob("*.py")):
        if path.name != "__init__.py":
            _load_marketplace_module(path).register_tools(server)

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

    assert offenders == [], f"{len(offenders)} offenders, e.g. {offenders[:5]}"


@pytest.mark.asyncio
async def test_csv_save_json_to_csv_accepts_null_overwrite() -> None:
    """An explicit null `overwrite` behaves like omitting it."""
    from secops_soar_mcp.marketplace import csv

    server = FastMCP("csv-null-default")
    csv.register_tools(server)

    fake_client = mock.AsyncMock()
    fake_client.get.return_value = {"integration_instances": [{"identifier": "csv-1"}]}
    fake_client.post.return_value = {"Status": "Completed"}

    with (
        mock.patch.object(csv.bindings, "http_client", fake_client),
        mock.patch.object(csv.bindings, "valid_scopes", {"All entities"}),
    ):
        async with client_session(server._mcp_server) as client:
            result = await client.call_tool(
                "csv_save_json_to_csv",
                arguments={
                    "case_id": "1",
                    "alert_group_identifiers": ["group-1"],
                    "json_object": "{}",
                    "file_path": "out.csv",
                    "target_entities": [],
                    "overwrite": None,
                },
            )

    assert not result.isError, result.content[0].text
    request = fake_client.post.call_args.kwargs["req"]
    script_params = json.loads(request["properties"]["ScriptParametersEntityFields"])
    assert "Overwrite" not in script_params
