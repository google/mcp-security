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


@pytest.mark.asyncio(scope="session")
async def test_server_connection():
    """Test that the server is running and accessible."""

    async with client_session(server._mcp_server) as client:
        tools_result = await client.list_tools()
        assert isinstance(tools_result, mcp.ListToolsResult)
        assert len(tools_result.tools) > 0


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_name", "tool_arguments", "vt_endpoint", "vt_object_response", "expected",
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
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.FILE_KEY_RELATIONSHIPS
                    }
                }
            },
            {
                "id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
                "type": "file",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
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
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
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
                    }
                }
            },
            {
                "id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f_VirusTotal Jujubox",
                "type": "file_behaviour",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
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
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.DOMAIN_KEY_RELATIONSHIPS
                    }
                }
            },
            {
                "id": "theevil.com",
                "type": "domain",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
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
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.IP_KEY_RELATIONSHIPS
                    }
                }
            },
            {
                "id": "8.8.8.8",
                "type": "ip_address",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
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
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.URL_KEY_RELATIONSHIPS
                    }
                }
            },
            {
                "id": "970281e76715a46d571ac5bbcef540145f54e1a112751ccf616df2b3c6fe9de4",
                "type": "url",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
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
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }
            },
            {
                "id": "collection_id",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
    ],
    indirect=["vt_endpoint", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_mock")
async def test_get_reports(
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
            "/api/v3/files/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ), 
        (
            "get_entities_related_to_a_domain",
            {"domain": "theevil.com", "relationship_name": "associations"},
            "/api/v3/domains/theevil.com/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),   
        (
            "get_entities_related_to_an_ip_address",
            {"ip_address": "8.8.8.8", "relationship_name": "associations"},
            "/api/v3/ip_addresses/8.8.8.8/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ), 
        (
            "get_entities_related_to_an_url",
            {"url": "http://theevil.com/", "relationship_name": "associations"},
            "/api/v3/urls/aHR0cDovL3RoZWV2aWwuY29tLw/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),
        (
            "get_entities_related_to_a_collection",
            {"id": "collection_id", "relationship_name": "associations"},
            "/api/v3/collections/collection_id/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),     
    ],
    indirect=["vt_endpoint", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_mock")
async def test_get_entities_related(
    vt_get_object_mock,
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


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_name", "tool_arguments", "vt_endpoint", "vt_object_response", "expected",
    ],
    argvalues=[
        (
            "get_file_behavior_summary",
            {"hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"},
            "/api/v3/files/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f/behaviour_summary",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}
        ), 
        (
            "get_collection_timeline_events",
            {"id": "collection_id"},
            "/api/v3/collections/collection_id/timeline/events",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}
        ),
        (
            "get_collection_mitre_tree",
            {"id": "collection_id"},
            "/api/v3/collections/collection_id/mitre_tree",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}
        ), 
    ],
    indirect=["vt_endpoint", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_mock")
async def test_get_simple_tools(
    vt_get_object_mock,
    tool_name,
    tool_arguments,
    expected):
    """Test simple tools that just retrieve information from GTI."""

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
        "tool_name", "tool_arguments", "vt_endpoint", "vt_request_params", "vt_object_response", "expected",
    ],
    argvalues=[
        (
            "search_threats",
            {"query": "What is APT44?"},
            "/api/v3/collections",
            {
                "filter": "What is APT44?", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },
            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "search_campaigns",
            {"query": "APT44"},
            "/api/v3/collections",
            {
                "filter": "collection_type:campaign APT44", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },
            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "search_threat_actors",
            {"query": "APT44"},
            "/api/v3/collections",
            {
                "filter": "collection_type:threat-actor APT44", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },
            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "search_malware_families",
            {"query": "APT44"},
            "/api/v3/collections",
            {
                "filter": "collection_type:malware-family APT44", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },
            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "search_software_toolkits",
            {"query": "APT44"},
            "/api/v3/collections",
            {
                "filter": "collection_type:software-toolkit APT44", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },

            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "search_threat_reports",
            {"query": "APT44"},
            "/api/v3/collections",
            {
                "filter": "collection_type:report APT44", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },
            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
        (
            "search_vulnerabilities",
            {"query": "APT44"},
            "/api/v3/collections",
            {
                "filter": "collection_type:vulnerability APT44", 
                "order": "relevance-",
                "relationships": ",".join(tools.COLLECTION_KEY_RELATIONSHIPS),
                "exclude_attributes": tools.COLLECTION_EXCLUDED_ATTRS,
            },
            {
                "data": [{
                    "id": "apt44",
                    "type": "collection",
                    "attributes": {"foo": "foo", "bar": "bar"},
                    "relationships": {
                        rel_name: [{"type": "object", "id": "obj-id"}]
                        for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                    }
                }]
            },
            {
                "id": "apt44",
                "type": "collection",
                "attributes": {"foo": "foo", "bar": "bar"},
                "relationships": {
                    rel_name: [{"type": "object", "id": "obj-id"}]
                    for rel_name in tools.COLLECTION_KEY_RELATIONSHIPS
                }
            },
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_with_params_mock")
async def test_search_threats(
    vt_get_object_with_params_mock,
    tool_name,
    tool_arguments,
    expected    
):
    """Test `search_*` tools.
    
    Tested tools:
        - search_threats
        - search_campaigns
        - search_threat_actors
        - search_malware_families
        - search_software_toolkits
        - search_threat_reports
        - search_vulnerabilities
    """

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool(tool_name, arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError == False
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected

