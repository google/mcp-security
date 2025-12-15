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
from unittest.mock import MagicMock, AsyncMock, patch
from mcp.server.fastmcp import Context
from gti_mcp.tools import collections

@pytest.mark.asyncio
async def test_get_collection_timeline_events_api_error_handled():
    """Test get_collection_timeline_events returns error dict on API error (e.g. 404)."""
    mock_ctx = MagicMock(spec=Context)

    mock_response = MagicMock()
    mock_response.status = 404
    async def json_async():
        return {"error": {"message": "Collection not found"}}
    mock_response.json_async = json_async

    mock_client_instance = MagicMock()
    mock_client_instance.get_async = AsyncMock(return_value=mock_response)

    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_vt_client.__aexit__ = AsyncMock(return_value=None)

    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_timeline_events(id="non_existent_id", ctx=mock_ctx)
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]
        assert "Collection not found" in result[0]["error"]

@pytest.mark.asyncio
async def test_get_collection_mitre_tree_api_error_handled():
    """Test get_collection_mitre_tree returns error dict on API error (e.g. 404)."""
    mock_ctx = MagicMock(spec=Context)

    mock_response = MagicMock()
    mock_response.status = 404
    async def json_async():
        return {"error": {"message": "Collection not found"}}
    mock_response.json_async = json_async

    mock_client_instance = MagicMock()
    mock_client_instance.get_async = AsyncMock(return_value=mock_response)

    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_vt_client.__aexit__ = AsyncMock(return_value=None)

    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_mitre_tree(id="non_existent_id", ctx=mock_ctx)
        assert "error" in result
        assert "Collection not found" in result["error"]

@pytest.mark.asyncio
async def test_get_collection_feature_matches_api_error_handled():
    """Test get_collection_feature_matches returns error dict on API error (e.g. 404)."""
    mock_ctx = MagicMock(spec=Context)

    mock_response = MagicMock()
    mock_response.status = 404
    async def json_async():
        return {"error": {"message": "Collection not found"}}
    mock_response.json_async = json_async

    mock_client_instance = MagicMock()
    mock_client_instance.get_async = AsyncMock(return_value=mock_response)

    mock_vt_client = MagicMock()
    mock_vt_client.__aenter__ = AsyncMock(return_value=mock_client_instance)
    mock_vt_client.__aexit__ = AsyncMock(return_value=None)

    with patch("gti_mcp.tools.collections.vt_client", return_value=mock_vt_client):
        result = await collections.get_collection_feature_matches(
            collection_id="non_existent_id",
            feature_type="ft",
            feature_id="fid",
            entity_type="file",
            search_space="collection",
            entity_type_plural="ets",
            ctx=mock_ctx
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]
        assert "Collection not found" in result[0]["error"]
