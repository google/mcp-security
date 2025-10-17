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
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from gti_mcp.server import server
from gti_mcp import tools
from gti_mcp.tools import collections

from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)


@pytest.mark.asyncio(loop_scope="session")
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
        (
            "get_threat_profile",
            {"profile_id": "profile_id"},
            "/api/v3/threat_profiles/profile_id",
            {
                "data": {
                    "id": "profile_id",
                    "type": "threat_profile",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            {
                "id": "profile_id",
                "type": "threat_profile",
                "attributes": {"foo": "foo", "bar": "bar"},
            }
        ),
        (
            "get_hunting_ruleset",
            {"ruleset_id": "ruleset_id"},
            "/api/v3/intelligence/hunting_rulesets/ruleset_id",
            {
                "data": {
                    "id": "ruleset_id",
                    "type": "hunting_ruleset",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }
            },
            {
                "id": "ruleset_id",
                "type": "hunting_ruleset",
                "attributes": {"foo": "foo", "bar": "bar"},
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
            {"hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f", "relationship_name": "associations", "descriptors_only": "True"},
            "/api/v3/files/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),
        (
            "get_entities_related_to_a_domain",
            {"domain": "theevil.com", "relationship_name": "associations", "descriptors_only": "True"},
            "/api/v3/domains/theevil.com/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),   
        (
            "get_entities_related_to_an_ip_address",
            {"ip_address": "8.8.8.8", "relationship_name": "associations", "descriptors_only": "True"},
            "/api/v3/ip_addresses/8.8.8.8/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ), 
        (
            "get_entities_related_to_an_url",
            {"url": "http://theevil.com/", "relationship_name": "associations", "descriptors_only": "True"},
            "/api/v3/urls/aHR0cDovL3RoZWV2aWwuY29tLw/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),
        (
            "get_entities_related_to_a_collection",
            {"id": "collection_id", "relationship_name": "associations", "descriptors_only": "True"},
            "/api/v3/collections/collection_id/relationship/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),  
        (
            "get_threat_profile_recommendations",
            {"profile_id": "profile_id"},
            "/api/v3/threat_profiles/profile_id/relationship/recommendations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),
        (
            "get_threat_profile_associations_timeline",
            {"profile_id": "profile_id"},
            "/api/v3/threat_profiles/profile_id/timeline/associations",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}},
        ),  
        (
            "get_entities_related_to_a_hunting_ruleset",
            {"ruleset_id": "ruleset_id", 
             "relationship_name": "hunting_notification_files"},
            "/api/v3/intelligence/hunting_rulesets/ruleset_id/"
            "relationship/hunting_notification_files",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
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
                "data": {"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}},
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}
        ), 
        (
            "get_collection_timeline_events",
            {"id": "collection_id"},
            "/api/v3/collections/collection_id/timeline/events",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}
        ),
        (
            "get_collection_mitre_tree",
            {"id": "collection_id"},
            "/api/v3/collections/collection_id/mitre_tree",
            {
                "data": {"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}},
            },
            {"type": "object", "id": "obj-id", "attributes": {"foo": "foo"}}
        ), 
        (
            "list_threat_profiles",
            {},
            "/api/v3/threat_profiles",
            {
                "data": [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}],
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
                    rel_name: [{"type": "object", "id": "obj-id", "attributes": {"foo": "foo", "bar": ""}}]
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


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_name", "tool_arguments", "vt_endpoint", "vt_request_params", "vt_object_response", "expected",
    ],
    argvalues=[
        (
            "get_collection_feature_matches",
            {
                "collection_id": "collection_id",
                "feature_type": "attack_techniques",
                "feature_id": "T1497.001",
                "entity_type": "file",
                "search_space": "collection",
                "entity_type_plural": "files",
                "descriptors_only": True,
            },
            "/api/v3/collections/collection_id/features/search",
            {
                "feature_type": "attack_techniques",
                "feature_id": "T1497.001",
                "entity_type": "file",
                "search_space": "collection",
                "type": "files",
                "descriptors_only": "true",
            },
            {
                "data": [{
                    "id": "file_id",
                    "type": "file",
                    "attributes": {"foo": "foo", "bar": "bar"},
                }]
            },
            {
                "id": "file_id",
                "type": "file",
                "attributes": {"foo": "foo", "bar": "bar"},
            },
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_with_params_mock")
async def test_get_collection_feature_matches(
    vt_get_object_with_params_mock,
    tool_name,
    tool_arguments,
    expected,
):
    """Test get_collection_feature_matches tool."""

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
            "get_collections_commonalities",
            {"collection_id": "67869ffd5a02cfc31584dfcf9b7516e7f443cbd1d8cfae4436b5cc38c9fdecf6"},
            "/api/v3/collections/67869ffd5a02cfc31584dfcf9b7516e7f443cbd1d8cfae4436b5cc38c9fdecf6",
            {"attributes": "aggregations"},
            {
                "data": {
                    "id": "67869ffd5a02cfc31584dfcf9b7516e7f443cbd1d8cfae4436b5cc38c9fdecf6",
                    "type": "collection",
                    "links": {
                        "self": "https://www.virustotal.com/api/v3/collections/67869ffd5a02cfc31584dfcf9b7516e7f443cbd1d8cfae4436b5cc38c9fdecf6"
                    },
                    "attributes": {
                        "aggregations": {
                            "files": {
                                "itw_urls": [
                                    {
                                        "value": "https://pcsdl.com/short-url-v2/000585065547/scenario/f91705e56983ba3c3cd940d62bc2ed35___158e5ef2-6f0f-46fd-b1b7-feaa02550432.vbs?protocol=https",
                                        "count": 1,
                                        "total_related": 1,
                                        "prevalence": 1.0
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            (
                "# Commonalities for 67869ffd5a02cfc31584dfcf9b7516e7f443cbd1d8cfae4436b5cc38c9fdecf6\n\n"
                "## files commonalities\n\n"
                "### itw urls\n"
                "- 1 matches of https://pcsdl.com/short-url-v2/000585065547/scenario/f91705e56983ba3c3cd940d62bc2ed35___158e5ef2-6f0f-46fd-b1b7-feaa02550432.vbs?protocol=https with a prevalence of 1\n\n"
            )
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_with_params_mock")
async def test_get_collections_commonalities(
    vt_get_object_with_params_mock,
    tool_name,
    tool_arguments,
    expected,
    vt_object_response
):
    """Test test_get_collections_commonalities tool."""

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool(tool_name, arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError == False
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert isinstance(result.content[0].text, str)
        assert result.content[0].text == expected


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_arguments",
        "vt_endpoint",
        "vt_request_params",
        "vt_object_response",
        "expected",
    ],
    argvalues=[
        (
            {
                "name": "My Collection",
                "description": "Test collection",
                "iocs": ["evil-domain.com", "165.227.148.68"],
                "private": False
            },
            "/api/v3/collections",
            {
                "data": {
                    "attributes": {
                        "name": "My Collection",
                        "description": "Test collection",
                        "private": False,
                    }, 
                    "raw_items": "evil-domain.com, 165.227.148.68",
                    "type": "collection",
                }
            },
            {
                "data": {
                    "id": "new_collection_id",
                    "type": "collection",
                    "attributes": {
                        "name": "My Collection",
                        "description": "Test collection",
                        "foo": "foo",
                        "bar": "bar",
                    },
                    "links": {
                        "self": "/api/v3/collections/new_collection_id"
                    },
                }
            },
            {
                "id": "new_collection_id",
                "type": "collection",
                "attributes": {
                    "name": "My Collection",
                    "description": "Test collection",
                    "foo": "foo",
                    "bar": "bar",
                },
                "links": {
                    "self": "/api/v3/collections/new_collection_id"
                },
            },
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_post_object_mock")
async def test_create_collection(
    vt_post_object_mock,
    tool_arguments,
    expected,
):
    """Test `create_collection` tool."""

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool("create_collection", arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert not result.isError
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_arguments",
        "vt_endpoint",
        "vt_request_params",
        "vt_object_response",
        "expected",
    ],
    argvalues=[
        (
            {
                "id": "my_collection_id",
                "attributes": {"name": "Updated Collection Name", "description": "Updated description."}, 
            },
            "/api/v3/collections/my_collection_id",
            {
                "data": {
                    "attributes": {"name": "Updated Collection Name", "description": "Updated description."}, 
                    "type": "collection",
                }
            },
            {
                "data": {
                    "id": "my_collection_id",
                    "type": "collection",
                    "attributes": {"name": "Updated Collection Name", "description": "Updated description."}, 
                }
            },
            {
                "id": "my_collection_id",
                "type": "collection",
                "attributes": {"name": "Updated Collection Name", "description": "Updated description."},
            },
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_patch_object_mock")
async def test_update_collection_attributes(
    vt_patch_object_mock,
    tool_arguments,
    expected,
):
    """Test `update_collection_attributes` tool."""

    async with client_session(server._mcp_server) as client:
        result = await client.call_tool("update_collection_attributes", arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert not result.isError
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_arguments", "vt_endpoint", "vt_request_params", "vt_object_response"
    ],
    argvalues=[
        # Case 1: Add domains
        (
            {"id": "c_id", "relationship": "domains", "iocs": ["evil.com"], "operation": "add"},
            "/api/v3/collections/c_id/domains",
            {"data": [{"type": "domain", "id": "evil.com"}]},
            {},
        ),
        # Case 2: Add URLs (special handling in the tool)
        (
            {"id": "c_id", "relationship": "urls", "iocs": ["http://bad-url.com/path"], "operation": "add"},
            "/api/v3/collections/c_id/urls",
            {"data": [{"type": "url", "url": "http://bad-url.com/path"}]},
            {},
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_post_object_mock")
async def test_add_iocs_in_collection_success(
    vt_post_object_mock,
    tool_arguments,
    vt_endpoint, 
    vt_request_params, 
    vt_object_response,
):
    """Test successful 'add' operations for `update_iocs_in_collection`."""
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool("update_iocs_in_collection", arguments=tool_arguments)
        assert not result.isError
        assert result.content[0].text == "Sucesssfully updated collection"


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=["tool_arguments", "vt_endpoint", "vt_request_params", "vt_object_response"],
    argvalues=[
        # Case 1: Remove files
        (
            {"id": "c_id", "relationship": "files", "iocs": ["hash123"], "operation": "remove"},
            "/api/v3/collections/c_id/files",
            {"data": [{"type": "file", "id": "hash123"}]},
            {},
        ),
    ],
    indirect=["vt_endpoint", "vt_request_params",  "vt_object_response"],
)
@pytest.mark.usefixtures("vt_delete_object_mock")
async def test_remove_iocs_from_collection_success(
    tool_arguments,
    vt_endpoint, 
    vt_request_params, 
    vt_object_response,
):
    """Test successful 'remove' operations for `update_iocs_in_collection`."""
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool("update_iocs_in_collection", arguments=tool_arguments)
        assert not result.isError
        assert result.content[0].text == "Sucesssfully updated collection"


# Invalid Local Argument Handling
@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_arguments", "expected_error"
    ],
    argvalues=[
        (
            {"id": "c_id", "relationship": "domains", "iocs": ["e.com"], "operation": "invalid_op"},
            "Error: Invalid operation 'invalid_op'. Must be one of 'add' or 'remove'",
        ),
        (
            {"id": "c_id", "relationship": "indicators", "iocs": ["e.com"], "operation": "add"},
            "Error: Invalid IOC type 'indicators'. Must be one of ['domains', 'files', 'ip_addresses', 'urls']",
        ),
    ],
)
async def test_update_iocs_in_collection_invalid_args(tool_arguments, expected_error):
    """Test `update_iocs_in_collection` for invalid local arguments."""
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool("update_iocs_in_collection", arguments=tool_arguments)
        assert not result.isError
        assert result.content[0].text == expected_error

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_arguments", "vt_endpoint", "vt_request_params", "vt_object_response", "expected"
    ],
    argvalues=[
        (
            {"query": "my-brand"},
            "/api/v3/dtm/docs/search",
            {"query": "my-brand"},
            {
                "timed_out": False,
                    "total_docs": 200,
                    "docs" : [
                        {"foo": "foo"},
                        {"bar": "bar"}
                    ]
            },
            {
                "timed_out": False,
                "total_docs": 200,
                "docs" : [
                        {"foo": "foo"},
                        {"bar": "bar"}
                    ]
            },
        )
    ],
    indirect=["vt_endpoint", "vt_request_params", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_post_object_mock")
async def test_search_digital_threat_monitoring(
    vt_post_object_mock,
    tool_arguments,
    expected
):
    """Test `search_digital_threat_monitoring` tool."""
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool("search_digital_threat_monitoring", arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert not result.isError
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        assert json.loads(result.content[0].text) == expected

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_response_text, mock_headers, side_effect, expected_error",
    [
        (
            "<html><body>request timed out</body></html>",
            {"Content-Type": "text/html"},
            None,
            "The request timed out. Please try reducing the scope of your query by using `since` and `until` parameters to add time delimiters",
        ),
        (
            "<html><body>Error</body></html>",
            {"Content-Type": "text/html"},
            None,
            "API returned an HTML error page instead of JSON: <html><body>Error</body></html>",
        ),
        (
            "Invalid JSON",
            {"Content-Type": "application/json"},
            None,
            "Failed to parse server response: Expecting value: line 1 column 1 (char 0).",
        ),
        (
            "",
            {},
            TimeoutError, # Use built-in TimeoutError
            "The request timed out. Please try reducing the scope of your query by using `since` and `until` parameters to add time delimiters",
        ),
        (
            "",
            {},
            RuntimeError("Test Exception"),
            "An unexpected error occurred: Test Exception",
        ),
    ],
)
async def test_search_digital_threat_monitoring_errors(
    mock_response_text, mock_headers, side_effect, expected_error
):
    """Test error handling in search_digital_threat_monitoring."""
    with patch('gti_mcp.tools.files.vt_client') as mock_vt_client:
        mock_client_instance = MagicMock()
        mock_response = MagicMock()

        async def text_async():
            return mock_response_text
        
        async def json_async():
            if mock_response_text == "Invalid JSON":
                raise json.JSONDecodeError("Expecting value", mock_response_text, 0)
            return json.loads(mock_response_text)

        mock_response.text_async = text_async
        mock_response.json_async = json_async
        mock_response.headers = mock_headers

        mock_post_async = AsyncMock() # Use AsyncMock here
        if side_effect:
            mock_post_async.side_effect = side_effect
        else:
            mock_post_async.return_value = mock_response
        
        mock_client_instance.post_async = mock_post_async
        
        # Setup the async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__.return_value = mock_client_instance
        mock_vt_client.return_value = mock_cm

        async with client_session(server._mcp_server) as client:
            result = await client.call_tool(
                "search_digital_threat_monitoring", arguments={"query": "test"}
            )
            assert isinstance(result, mcp.types.CallToolResult)
            assert result.isError == False # The tool call itself doesn't fail
            assert len(result.content) == 1
            content = json.loads(result.content[0].text)
            assert "error" in content
            assert content["error"] == expected_error

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=[
        "tool_name", "tool_arguments", "vt_endpoint", "vt_object_response", "expected",
    ],
    argvalues=[
        (
            "get_entities_related_to_a_collection",
            {"id": "collection_id", "relationship_name": "files", "descriptors_only": "True"},
            "/api/v3/collections/collection_id/relationship/files",
            {
                "data": [],
            },
            [],
        ),  
    ],
    indirect=["vt_endpoint", "vt_object_response"],
)
@pytest.mark.usefixtures("vt_get_object_mock")
async def test_get_entities_related_empty_result(
    vt_get_object_mock,
    tool_name,
    tool_arguments,
    expected    
):
    """Test tools.get_entities_related_to_a_collection when the API returns an empty list."""

    # Execute tool call.
    async with client_session(server._mcp_server) as client:
        result = await client.call_tool(tool_name, arguments=tool_arguments)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError == False
        assert result.structuredContent == {"result": expected}

@pytest.mark.asyncio
async def test_get_collection_rules_all_types():
    mock_ctx = AsyncMock()
    mock_client_instance = AsyncMock()

    # Mock data for aggregations
    mock_aggregations_data = {
        "data": {
            "attributes": {
                "aggregations": {
                    "files": {
                        "crowdsourced_ids_results": [
                            {"id": "ids1", "count": 10, "value": {"message": "IDS Rule 1", "url": "http://ids1.com", "rule": "ids rule content 1"}},
                            {"id": "ids2", "count": 5, "value": {"message": "IDS Rule 2", "url": "http://ids2.com", "rule": "ids rule content 2"}},
                        ],
                        "crowdsourced_sigma_results": [
                            {"id": "sigma1", "count": 8, "value": {"id": "sigma1", "title": "Sigma Rule 1"}},
                        ],
                        "crowdsourced_yara_results": [
                            {"id": "yara1", "count": 12, "value": {"ruleset_id": "yara1"}},
                            {"id": "yara2", "count": 3, "value": {"ruleset_id": "yara2"}},
                            {"id": "yara3", "count": 7, "value": {"ruleset_id": "yara3"}},
                        ],
                    }
                }
            }
        }
    }

    # Mock data for individual rule lookups
    mock_yara_ruleset_data = {
        "yara1": {"data": {"id": "yara1", "attributes": {"name": "Yara Rule 1", "source": "source1", "rules": "yara rule content 1"}}},
        "yara3": {"data": {"id": "yara3", "attributes": {"name": "Yara Rule 3", "source": "source3", "rules": "yara rule content 3"}}},
    }
    mock_sigma_ruleset_data = {
        "sigma1": {"data": {"id": "sigma1", "attributes": {"source_url": "http://sigma1.com", "rule": "sigma rule content 1"}}},
    }

    # Mock data for curated rules
    mock_related_rulesets = {"data": [{"id": "curated1"}]}
    mock_curated_ruleset_data = {
        "curated1": {"data": {"id": "curated1", "attributes": {"rules": "curated yara content 1", "rule_names": ["Curated Rule 1"], "number_of_rules": 1}}},
    }

    async def mock_get_async(url, **kwargs):
        mock_resp = MagicMock()
        if url.startswith("/collections/test_id?attributes=aggregations"):
            async def json_async(): return mock_aggregations_data
            mock_resp.json_async = json_async
        elif url.startswith("/yara_rulesets/"):
            ruleset_id = url.split("/")[-1]
            async def json_async(): return mock_yara_ruleset_data.get(ruleset_id, {"data": {}})
            mock_resp.json_async = json_async
        elif url.startswith("/sigma_rules/"):
            ruleset_id = url.split("/")[-1]
            async def json_async(): return mock_sigma_ruleset_data.get(ruleset_id, {"data": {}})
            mock_resp.json_async = json_async
        elif url == "/collections/test_id/hunting_rulesets":
            async def json_async(): return mock_related_rulesets
            mock_resp.json_async = json_async
        elif url.startswith("/intelligence/hunting_rulesets/"):
            ruleset_id = url.split("/")[-1]
            async def json_async(): return mock_curated_ruleset_data.get(ruleset_id, {"data": {}})
            mock_resp.json_async = json_async
        else:
            async def json_async(): return {}
            mock_resp.json_async = json_async
        return mock_resp

    mock_client_instance.get_async.side_effect = mock_get_async

    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__.return_value = mock_client_instance
    
    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_rules(collection_id="test_id", ctx=mock_ctx, top_n=2)

    expected_result = [
        {"rule_id": "ids1", "rule_name": "IDS Rule 1", "rule_source": "http://ids1.com", "rule_content": "ids rule content 1", "count": 10, "rule_type": "crowdsourced_ids"},
        {"rule_id": "ids2", "rule_name": "IDS Rule 2", "rule_source": "http://ids2.com", "rule_content": "ids rule content 2", "count": 5, "rule_type": "crowdsourced_ids"},
        {"rule_id": "sigma1", "rule_name": "Sigma Rule 1", "rule_source": "http://sigma1.com", "rule_content": "sigma rule content 1", "count": 8, "rule_type": "crowdsourced_sigma"},
        {"rule_id": "yara1", "rule_name": "Yara Rule 1", "rule_source": "source1", "rule_content": "yara rule content 1", "count": 12, "rule_type": "crowdsourced_yara"},
        {"rule_id": "yara3", "rule_name": "Yara Rule 3", "rule_source": "source3", "rule_content": "yara rule content 3", "count": 7, "rule_type": "crowdsourced_yara"},
        {"rule_type": "curated_yara_rule", "rule_name": "Curated Rule 1", "rule_content": "curated yara content 1"},
    ]

    def sort_key(x):
        return (x['rule_type'], -x.get('count', 0), x.get('rule_id', ''), x.get('rule_name', ''))
    
    result.sort(key=sort_key)
    expected_result.sort(key=sort_key)

    assert result == expected_result

@pytest.mark.asyncio
async def test_get_collection_rules_filter_types():
    mock_ctx = AsyncMock()
    mock_client_instance = AsyncMock()

    mock_aggregations_data = {
        "data": {
            "attributes": {
                "aggregations": {
                    "files": {
                        "crowdsourced_ids_results": [
                            {"id": "ids1", "count": 10, "value": {"message": "IDS Rule 1", "url": "http://ids1.com", "rule": "ids rule content 1"}},
                        ],
                        "crowdsourced_sigma_results": [
                            {"id": "sigma1", "count": 8, "value": {"id": "sigma1", "title": "Sigma Rule 1"}},
                        ],
                    }
                }
            }
        }
    }

    async def mock_get_async(url, **kwargs):
        mock_resp = MagicMock()
        if url.startswith("/collections/test_id?attributes=aggregations"):
            async def json_async(): return mock_aggregations_data
            mock_resp.json_async = json_async
        return mock_resp

    mock_client_instance.get_async.side_effect = mock_get_async

    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__.return_value = mock_client_instance
    
    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_rules(collection_id="test_id", ctx=mock_ctx, rule_types=["crowdsourced_ids"])

    expected_result = [
        {"rule_id": "ids1", "rule_name": "IDS Rule 1", "rule_source": "http://ids1.com", "rule_content": "ids rule content 1", "count": 10, "rule_type": "crowdsourced_ids"},
    ]
    assert result == expected_result

@pytest.mark.asyncio
async def test_get_collection_rules_empty():
    mock_ctx = AsyncMock()
    mock_client_instance = AsyncMock()

    async def mock_get_async(url, **kwargs):
        mock_resp = MagicMock()
        async def json_async(): return {"data": {"attributes": {"aggregations": {"files": {}}}}}
        mock_resp.json_async = json_async
        return mock_resp

    mock_client_instance.get_async.side_effect = mock_get_async
    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__.return_value = mock_client_instance
    
    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_rules(collection_id="test_id", ctx=mock_ctx)
    assert result == []

@pytest.mark.asyncio
async def test_get_collection_rules_api_error():
    mock_ctx = AsyncMock()
    mock_client_instance = AsyncMock()
    mock_client_instance.get_async.side_effect = Exception("API Error")
    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__.return_value = mock_client_instance
    
    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_rules(collection_id="test_id", ctx=mock_ctx)
    assert result == []

@pytest.mark.asyncio
async def test_get_collection_rules_partial_error():
    mock_ctx = AsyncMock()
    mock_client_instance = AsyncMock()

    mock_aggregations_data = {
        "data": {
            "attributes": {
                "aggregations": {
                    "files": {
                        "crowdsourced_yara_results": [
                            {"id": "yara1", "count": 12, "value": {"ruleset_id": "yara1"}},
                        ],
                    }
                }
            }
        }
    }

    async def mock_get_async(url, **kwargs):
        mock_resp = MagicMock()
        if url.startswith("/collections/test_id?attributes=aggregations"):
            async def json_async(): return mock_aggregations_data
            mock_resp.json_async = json_async
        elif url.startswith("/yara_rulesets/"):
            raise Exception("Yara lookup failed")
        elif url == "/collections/test_id/hunting_rulesets":
             async def json_async(): return {"data": []}
             mock_resp.json_async = json_async
        return mock_resp

    mock_client_instance.get_async.side_effect = mock_get_async
    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__.return_value = mock_client_instance
    
    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_rules(collection_id="test_id", ctx=mock_ctx)
    assert result == []