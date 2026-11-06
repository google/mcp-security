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
from unittest import mock
from mcp.server import fastmcp
from gti_mcp.tools import files

@pytest.mark.asyncio
async def test_get_file_behavior_summary_api_error_handled():
    """Test get_file_behavior_summary returns error dict on API error (e.g. 404)."""
    mock_ctx = mock.MagicMock(spec=fastmcp.Context)

    mock_response = mock.MagicMock()
    mock_response.status = 404
    async def json_async():
        return {"error": {"message": "File not found"}}
    mock_response.json_async = json_async

    mock_client_instance = mock.MagicMock()
    mock_client_instance.get_async = mock.AsyncMock(return_value=mock_response)

    mock_vt_client = mock.MagicMock()
    mock_vt_client.__aenter__ = mock.AsyncMock(return_value=mock_client_instance)
    mock_vt_client.__aexit__ = mock.AsyncMock(return_value=None)

    with mock.patch("gti_mcp.tools.files.vt_client", return_value=mock_vt_client):
        result = await files.get_file_behavior_summary(hash="non_existent_hash", ctx=mock_ctx)
        assert "error" in result
        assert "VirusTotal API Error" in result["error"]
        assert "File not found" in result["error"]

@pytest.mark.asyncio
async def test_get_file_behavior_summary_unexpected_format_handled():
    """Test get_file_behavior_summary returns error dict on unexpected response format."""
    mock_ctx = mock.MagicMock(spec=fastmcp.Context)

    mock_response = mock.MagicMock()
    async def json_async():
        return {"something": "unexpected"}
    mock_response.json_async = json_async

    mock_client_instance = mock.MagicMock()
    mock_client_instance.get_async = mock.AsyncMock(return_value=mock_response)

    mock_vt_client = mock.MagicMock()
    mock_vt_client.__aenter__ = mock.AsyncMock(return_value=mock_client_instance)
    mock_vt_client.__aexit__ = mock.AsyncMock(return_value=None)

    with mock.patch("gti_mcp.tools.files.vt_client", return_value=mock_vt_client):
        result = await files.get_file_behavior_summary(hash="some_hash", ctx=mock_ctx)
        assert "error" in result
        assert "Unexpected response format" in result["error"]


@pytest.mark.asyncio
async def test_get_entities_related_to_a_file_invalid_relationship_returns_error_dict():
    """Invalid relationship_name returns an error dict via FastMCP call_tool.

    Invoking through server.call_tool exercises FastMCP outputSchema /
    structured-output validation, so a regression that drops the Union return
    annotation fails this test (ToolError / pydantic list_type).
    """
    from gti_mcp.server import server

    result = await server.call_tool(
        "get_entities_related_to_a_file",
        {
            "hash": "abc",
            "relationship_name": "not_a_real_relationship",
            "descriptors_only": True,
        },
    )
    # FastMCP wraps Union returns as (unstructured, structured) with
    # structured == {"result": <tool return value>}.
    assert isinstance(result, tuple)
    _content, structured = result
    assert isinstance(structured, dict)
    payload = structured.get("result", structured)
    assert isinstance(payload, dict)
    assert "error" in payload
    assert "not_a_real_relationship" in payload["error"]


@pytest.mark.asyncio
async def test_get_entities_related_to_a_file_behaviours_scoped_exclude_attributes():
    """exclude_attributes is sent only for behaviours with descriptors_only=False."""
    mock_ctx = mock.MagicMock(spec=fastmcp.Context)

    captured = {}

    async def fake_fetch(client, collection, resource_id, relationships,
                         params=None, descriptors_only=True, limit=10):
        captured["params"] = params
        captured["descriptors_only"] = descriptors_only
        captured["relationships"] = relationships
        return {relationships[0]: [{"id": "bh-1", "type": "file-behaviour", "attributes": {}}]}

    with mock.patch("gti_mcp.tools.files.vt_client") as vt_client_cm, \
         mock.patch("gti_mcp.tools.files.utils.fetch_object_relationships",
                    side_effect=fake_fetch):
        mock_client = mock.MagicMock()
        vt_client_cm.return_value.__aenter__ = mock.AsyncMock(return_value=mock_client)
        vt_client_cm.return_value.__aexit__ = mock.AsyncMock(return_value=None)

        await files.get_entities_related_to_a_file(
            hash="abc",
            relationship_name="behaviours",
            descriptors_only=False,
            ctx=mock_ctx,
        )
        assert captured["params"] is not None
        assert "exclude_attributes" in captured["params"]
        excluded = captured["params"]["exclude_attributes"].split(",")
        assert "memory_dumps" in excluded
        for keep in (
            "processes_tree",
            "processes_created",
            "command_executions",
            "ip_traffic",
            "http_conversations",
            "files_dropped",
            "attack_techniques",
            "signature_matches",
            "ids_alerts",
            "mutexes_created",
        ):
            assert keep not in excluded

        captured.clear()
        await files.get_entities_related_to_a_file(
            hash="abc",
            relationship_name="contacted_domains",
            descriptors_only=True,
            ctx=mock_ctx,
        )
        assert captured["params"] is None

        captured.clear()
        await files.get_entities_related_to_a_file(
            hash="abc",
            relationship_name="behaviours",
            descriptors_only=True,
            ctx=mock_ctx,
        )
        assert captured["params"] is None


@pytest.mark.asyncio
async def test_get_file_behavior_summary_strips_bulk_keeps_pivots():
    """Summary trim drops memory_dumps/text_highlighted but keeps pivots."""
    mock_ctx = mock.MagicMock(spec=fastmcp.Context)

    mock_response = mock.MagicMock()
    async def json_async():
        return {
            "data": {
                "processes_tree": [{"name": "evil.exe"}],
                "command_executions": ["cmd.exe /c whoami"],
                "ip_traffic": [{"dst": "1.2.3.4"}],
                "attack_techniques": ["T1059"],
                "memory_dumps": ["HUGE"],
                "text_highlighted": ["noise"],
                "tags": ["tag"],
            }
        }
    mock_response.json_async = json_async

    mock_client_instance = mock.MagicMock()
    mock_client_instance.get_async = mock.AsyncMock(return_value=mock_response)

    mock_vt_client = mock.MagicMock()
    mock_vt_client.__aenter__ = mock.AsyncMock(return_value=mock_client_instance)
    mock_vt_client.__aexit__ = mock.AsyncMock(return_value=None)

    with mock.patch("gti_mcp.tools.files.vt_client", return_value=mock_vt_client):
        result = await files.get_file_behavior_summary(hash="abc", ctx=mock_ctx)

    assert "processes_tree" in result
    assert "command_executions" in result
    assert "ip_traffic" in result
    assert "attack_techniques" in result
    assert "memory_dumps" not in result
    assert "text_highlighted" not in result
    assert "tags" not in result
