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
"""Optional string parameters must still accept JSON text.

FastMCP decodes a string argument that holds a JSON object or array when the
parameter is not annotated exactly `str`, which makes a plain `str | None`
parameter reject '{"field": "value"}'.
"""

import json
from typing import Annotated
from unittest import mock

import pytest
from mcp.server.fastmcp import FastMCP
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from pydantic import Field

from secops_soar_mcp.utils.optional_str import OptionalStr

JSON_TEXT = ['{"field": "value"}', '["a", "b"]', "{}", "[]", '{"é": ["ü", 1]}']
PLAIN_TEXT = ["plain text", "true", "false", "123", "1.5", '"quoted"', "", "[not json"]


def _echo_server() -> FastMCP:
    server = FastMCP("optional-str")

    @server.tool()
    async def echo(
        value: Annotated[OptionalStr, Field(default=None, description="Any text.")],
    ) -> dict:
        return {"value": value}

    return server


async def _echo(arguments: dict) -> object:
    async with client_session(_echo_server()._mcp_server) as client:
        result = await client.call_tool("echo", arguments=arguments)
    assert not result.isError, result.content[0].text
    return json.loads(result.content[0].text)["value"]


@pytest.mark.asyncio
@pytest.mark.parametrize("text", JSON_TEXT)
async def test_json_text_arrives_as_equivalent_text(text) -> None:
    value = await _echo({"value": text})

    assert isinstance(value, str)
    assert json.loads(value) == json.loads(text)


@pytest.mark.asyncio
@pytest.mark.parametrize("text", PLAIN_TEXT)
async def test_other_text_arrives_unchanged(text) -> None:
    assert await _echo({"value": text}) == text


@pytest.mark.asyncio
async def test_null_and_omitted_arrive_as_none() -> None:
    assert await _echo({"value": None}) is None
    assert await _echo({}) is None


@pytest.mark.asyncio
async def test_null_text_arrives_as_none() -> None:
    """Known limit: FastMCP decodes "null" before any validator runs."""
    assert await _echo({"value": "null"}) is None


@pytest.mark.asyncio
async def test_schema_is_nullable_string() -> None:
    async with client_session(_echo_server()._mcp_server) as client:
        tool = (await client.list_tools()).tools[0]

    assert tool.inputSchema["properties"]["value"] == {
        "anyOf": [{"type": "string"}, {"type": "null"}],
        "default": None,
        "description": "Any text.",
        "title": "Value",
    }


@pytest.mark.asyncio
async def test_marketplace_json_parameter_reaches_the_action() -> None:
    """arcsight additional_fields documents its format as a JSON object."""
    from secops_soar_mcp.marketplace import arcsight

    server = FastMCP("arcsight-json-text")
    arcsight.register_tools(server)

    fake_client = mock.AsyncMock()
    fake_client.get.return_value = {
        "integration_instances": [{"identifier": "arcsight-1"}]
    }
    fake_client.post.return_value = {"Status": "Completed"}

    with (
        mock.patch.object(arcsight.bindings, "http_client", fake_client),
        mock.patch.object(arcsight.bindings, "valid_scopes", {"All entities"}),
    ):
        async with client_session(server._mcp_server) as client:
            result = await client.call_tool(
                "arcsight_add_entities_to_active_list",
                arguments={
                    "case_id": "1",
                    "alert_group_identifiers": ["group-1"],
                    "active_list_name": "watchlist",
                    "entity_column": "entity",
                    "additional_fields": '{"Column_1": "Value_1"}',
                    "target_entities": [],
                },
            )

    assert not result.isError, result.content[0].text
    request = fake_client.post.call_args.kwargs["req"]
    script_params = json.loads(request["properties"]["ScriptParametersEntityFields"])
    assert json.loads(script_params["Additional Fields"]) == {"Column_1": "Value_1"}
