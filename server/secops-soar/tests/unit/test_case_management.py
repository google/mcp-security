# Copyright 2026 Google LLC
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

from unittest.mock import AsyncMock, patch

import pytest
from mcp.server.fastmcp import FastMCP
from secops_soar_mcp import bindings
from secops_soar_mcp.case_management import register_tools
from secops_soar_mcp.utils.consts import Endpoints


@pytest.fixture
def mock_mcp():
    mcp = FastMCP("test-soar")
    register_tools(mcp)
    return mcp


@pytest.mark.asyncio
async def test_list_case_close_root_causes_success(mock_mcp):
    """Test list_case_close_root_causes correctly calls endpoint and formats results."""
    tool = mock_mcp._tool_manager.get_tool("list_case_close_root_causes")
    assert tool is not None, "list_case_close_root_causes tool should be registered"

    mock_records = [
        {"id": 1, "rootCause": "Phishing email", "forCloseReason": 0},
        {"id": 2, "rootCause": "False Positive - Scanner", "forCloseReason": 1},
        {"id": 3, "rootCause": "Scheduled Drill", "forCloseReason": 2},
        {"id": 4, "rootCause": "Insufficient Logs", "forCloseReason": 3},
    ]

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_records
    with patch.object(bindings, "http_client", mock_client):
        result = await tool.fn()

        mock_client.get.assert_awaited_once_with(Endpoints.GET_ROOT_CAUSE_CLOSE_RECORDS)
        assert isinstance(result, dict)
        assert "root_causes" in result
        records = result["root_causes"]
        assert len(records) == 4
        assert records[0] == {
            "id": 1,
            "root_cause": "Phishing email",
            "close_reason": "Malicious",
        }
        assert records[1] == {
            "id": 2,
            "root_cause": "False Positive - Scanner",
            "close_reason": "NotMalicious",
        }
        assert records[2] == {
            "id": 3,
            "root_cause": "Scheduled Drill",
            "close_reason": "Maintenance",
        }
        assert records[3] == {
            "id": 4,
            "root_cause": "Insufficient Logs",
            "close_reason": "Inconclusive",
        }


@pytest.mark.asyncio
async def test_list_case_close_root_causes_handles_none(mock_mcp):
    """Test list_case_close_root_causes handles None/error from http_client."""
    tool = mock_mcp._tool_manager.get_tool("list_case_close_root_causes")
    assert tool is not None

    mock_client = AsyncMock()
    mock_client.get.return_value = None
    with patch.object(bindings, "http_client", mock_client):
        result = await tool.fn()

        assert isinstance(result, dict)
        assert "error" in result


@pytest.mark.asyncio
async def test_list_case_close_root_causes_handles_non_list_response(mock_mcp):
    """Test list_case_close_root_causes handles non-list/error dictionary from http_client."""
    tool = mock_mcp._tool_manager.get_tool("list_case_close_root_causes")
    assert tool is not None

    mock_client = AsyncMock()
    mock_client.get.return_value = {"error": "Unauthorized access"}
    with patch.object(bindings, "http_client", mock_client):
        result = await tool.fn()

        assert isinstance(result, dict)
        assert result == {"error": "Unauthorized access"}

    mock_client.get.return_value = {"message": "Unexpected error format"}
    with patch.object(bindings, "http_client", mock_client):
        result = await tool.fn()

        assert isinstance(result, dict)
        assert "error" in result
