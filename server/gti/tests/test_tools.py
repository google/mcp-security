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
import json
import mcp
import pytest

from gti_mcp.server import server
from gti_mcp import tools

from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    "entity_id,entity_collection,entity_type,relationships,tool_name,tool_id_name,gti_id",
    [
        (
            "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
            "files",
            "file",
            tools.FILE_KEY_RELATIONSHIPS,
            "get_file_report",
            "hash",
            "",
        ),
        (
            "theevil.com",
            "domains",
            "domain",
            tools.DOMAIN_KEY_RELATIONSHIPS,
            "get_domain_report",
            "domain",
            "",
        ),
        (
            "8.8.8.8",
            "ip_addresses",
            "ip_address",
            tools.IP_KEY_RELATIONSHIPS,
            "get_ip_address_report",
            "ip_address",
            "",
        ),
        (
            "http://theevil.com/",
            "urls",
            "url",
            tools.URL_KEY_RELATIONSHIPS,
            "get_url_report",
            "url",
            "aHR0cDovL3RoZWV2aWwuY29tLw",
        ),
    ],
)
async def test_get_file_report(
    make_httpserver_ipv4,
    mock_vt_client,
    entity_id,
    entity_collection,
    entity_type,
    relationships,
    tool_name,
    tool_id_name,
    gti_id,
):
    """Test `get_{file,domain,ip_address,url}_report` tools."""

    tool_arguments = {tool_id_name: entity_id}

    # Build API path.
    base_endpoint = f"/api/v3/{entity_collection}/{entity_id}"
    if gti_id:
        # GTI expects url's sha256 or base64 encoded.
        base_endpoint = f"/api/v3/{entity_collection}/{gti_id}"

    # Mock get object request.
    expected = {
        "data": {
            "id": entity_id,
            "type": entity_type,
            "attributes": {"foo": "foo", "bar": "bar"},
        }
    }
    make_httpserver_ipv4.expect_request(
        base_endpoint,
        method="GET",
        headers={"X-Apikey": "dummy_api_key"},
    ).respond_with_json(expected)

    # Mock get relationships requests.
    expected_rels = {}
    for rel_name in relationships:
        resp = {
            "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
        }
        make_httpserver_ipv4.expect_request(
            f"{base_endpoint}/{rel_name}",
            method="GET",
            headers={"X-Apikey": "dummy_api_key"},
        ).respond_with_json(resp)
        expected_rels[rel_name] = resp["data"]
    expected["data"]["relationships"] = expected_rels

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool(tool_name, arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError == False
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected["data"]


@pytest.mark.asyncio(scope="session")
async def test_server_connection():
    """Test that the server is running and accessible."""
    from gti_mcp.server import server

    async with client_session(server._mcp_server) as client:
        tools_result = await client.list_tools()
        assert isinstance(tools_result, mcp.ListToolsResult)
        assert len(tools_result.tools) > 0
