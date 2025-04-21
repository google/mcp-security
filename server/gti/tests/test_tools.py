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
    argnames=[
        "tool_name", "tool_arguments", "vt_endpoint", "vt_object_response", "abridged_relationships", "expected",
    ],
    argvalues=[
        (
            "get_file_report",
            {"hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"},
            "/api/v3/files/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
            {
                "data": {
                    "id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
                    "type": "file",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            tools.FILE_KEY_RELATIONSHIPS,
            {
                "id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
                "type": "file",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in tools.FILE_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "get_file_behavior_report",
            {"file_behaviour_id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f_VirusTotal Jujubox"},
            "/api/v3/file_behaviours/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f_VirusTotal Jujubox",
            {
                "data": {
                    "id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f_VirusTotal Jujubox",
                    "type": "file_behaviour",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            [
                "contacted_domains",
                "contacted_ips",
                "contacted_urls",
                "dropped_files",
                "embedded_domains",
                "embedded_ips",
                "embedded_urls",
                "associations",
            ],
            {
                "id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f_VirusTotal Jujubox",
                "type": "file_behaviour",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in [
                        "contacted_domains",
                        "contacted_ips",
                        "contacted_urls",
                        "dropped_files",
                        "embedded_domains",
                        "embedded_ips",
                        "embedded_urls",
                        "associations",
                    ]
                },
            },
        ),
        (
            "get_domain_report",
            {"domain": "theevil.com"},
            "/api/v3/domains/theevil.com",
            {
                "data": {
                    "id": "theevil.com",
                    "type": "domain",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            tools.DOMAIN_KEY_RELATIONSHIPS,
            {
                "id": "theevil.com",
                "type": "domain",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in tools.DOMAIN_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "get_ip_address_report",
            {"ip_address": "8.8.8.8"},
            "/api/v3/ip_addresses/8.8.8.8",
            {
                "data": {
                    "id": "8.8.8.8",
                    "type": "ip_address",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            tools.IP_KEY_RELATIONSHIPS,
            {
                "id": "8.8.8.8",
                "type": "ip_address",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in tools.IP_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "get_url_report",
            {"url": "http://theevil.com/"},
            "/api/v3/urls/aHR0cDovL3RoZWV2aWwuY29tLw",
            {
                "data": {
                    "id": "970281e76715a46d571ac5bbcef540145f54e1a112751ccf616df2b3c6fe9de4",
                    "type": "url",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            tools.URL_KEY_RELATIONSHIPS,
            {
                "id": "970281e76715a46d571ac5bbcef540145f54e1a112751ccf616df2b3c6fe9de4",
                "type": "url",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in tools.URL_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "get_collection_report",
            {"id": "collection_id"},
            "/api/v3/collections/collection_id",
            {
                "data": {
                    "id": "collection_id",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            tools.COLLECTION_KEY_RELATIONSHIPS,
            {
                "id": "collection_id",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
    ],
    indirect=["vt_endpoint", "vt_object_response", "abridged_relationships"],
)
@pytest.mark.usefixtures("vt_get_object_mock")
async def test_get_ioc_report(
    vt_get_object_mock,
    tool_name,
    tool_arguments,
    expected    
):
    """Test `get_{file,file_behaviour,domain,ip_address,url}_report` tools."""

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool(tool_name, arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError == False
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_name", "tool_arguments", "vt_endpoint", "vt_object_response", "expected",
    ],
    argvalues=[
        (
            "get_entities_related_to_a_file",
            {"hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f", "relationship_name": "associations"},
            "/api/v3/files/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ), 
        (
            "get_entities_related_to_a_domain",
            {"domain": "theevil.com", "relationship_name": "associations"},
            "/api/v3/domains/theevil.com/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),   
        (
            "get_entities_related_to_an_ip_address",
            {"ip_address": "8.8.8.8", "relationship_name": "associations"},
            "/api/v3/ip_addresses/8.8.8.8/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ), 
        (
            "get_entities_related_to_an_url",
            {"url": "http://theevil.com/", "relationship_name": "associations"},
            "/api/v3/urls/aHR0cDovL3RoZWV2aWwuY29tLw/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),
        (
            "get_entities_related_to_a_collection",
            {"id": "collection_id", "relationship_name": "associations"},
            "/api/v3/collections/collection_id/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),     
    ],
    indirect=["vt_endpoint", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_request_mock")
async def test_get_entities_related(
    vt_get_request_mock,
    tool_name,
    tool_arguments,
    expected    
):
    """Test `get_{file,file_behaviour,domain,ip_address,url,collection}_report` tools."""

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool(tool_name, arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError == False
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected


@pytest.mark.asyncio(scope="session")
async def test_server_connection():
    """Test that the server is running and accessible."""

    async with client_session(server._mcp_server) as client:
        tools_result = await client.list_tools()
        assert isinstance(tools_result, mcp.ListToolsResult)
        assert len(tools_result.tools) > 0
