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

"""Unit tests for Chronicle Case Close Definitions MCP tools."""

import importlib.util
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure server/secops is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

# Mock mcp if not installed
if importlib.util.find_spec("mcp") is None:
    mock_mcp = MagicMock()
    sys.modules["mcp"] = mock_mcp
    sys.modules["mcp.server"] = MagicMock()
    sys.modules["mcp.server.fastmcp"] = MagicMock()

    def tool_decorator(*args, **kwargs):
        def wrapper(func):
            return func
        return wrapper

    mock_fastmcp_instance = MagicMock()
    mock_fastmcp_instance.tool.side_effect = tool_decorator
    sys.modules["mcp.server.fastmcp"].FastMCP.return_value = mock_fastmcp_instance

from secops_mcp.tools.case_close_definitions import list_case_close_definitions


@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    return client


@pytest.mark.asyncio
async def test_list_case_close_definitions_success(mock_chronicle_client):
    """Test listing case close definitions successfully with default parameters."""
    expected_response = {
        "caseCloseDefinitions": [
            {
                "name": "projects/p/locations/us/instances/i/caseCloseDefinitions/def1",
                "closeReason": "MALICIOUS",
                "rootCause": "Phishing credential harvest",
            },
            {
                "name": "projects/p/locations/us/instances/i/caseCloseDefinitions/def2",
                "closeReason": "NOT_MALICIOUS",
                "rootCause": "Authorized Security Test",
            },
        ],
        "nextPageToken": "",
        "totalSize": 2,
    }

    with patch("secops_mcp.tools.case_close_definitions.get_chronicle_client", return_value=mock_chronicle_client), \
         patch("secops_mcp.tools.case_close_definitions.chronicle_paginated_request", return_value=expected_response) as mock_request:
        result = await list_case_close_definitions()

        mock_request.assert_called_once()
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["path"] == "caseCloseDefinitions"
        assert call_kwargs["page_size"] == 50
        assert call_kwargs["page_token"] is None
        assert result == expected_response


@pytest.mark.asyncio
async def test_list_case_close_definitions_with_filters(mock_chronicle_client):
    """Test listing case close definitions with filter, order_by, and pagination."""
    expected_response = {
        "caseCloseDefinitions": [
            {
                "name": "projects/p/locations/us/instances/i/caseCloseDefinitions/def1",
                "closeReason": "MALICIOUS",
                "rootCause": "Phishing credential harvest",
            }
        ],
        "nextPageToken": "token123",
        "totalSize": 1,
    }

    with patch("secops_mcp.tools.case_close_definitions.get_chronicle_client", return_value=mock_chronicle_client) as mock_get_client, \
         patch("secops_mcp.tools.case_close_definitions.chronicle_paginated_request", return_value=expected_response) as mock_request:
        result = await list_case_close_definitions(
            page_size=10,
            page_token="tok_abc",
            filter="close_reason='MALICIOUS'",
            order_by="root_cause desc",
            project_id="my-proj",
            customer_id="my-cust",
            region="europe",
        )

        mock_get_client.assert_called_once_with("my-proj", "my-cust", "europe")
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["page_size"] == 10
        assert call_kwargs["page_token"] == "tok_abc"
        assert call_kwargs["extra_params"] == {
            "filter": "close_reason='MALICIOUS'",
            "orderBy": "root_cause desc",
        }
        assert result == expected_response


@pytest.mark.asyncio
async def test_list_case_close_definitions_error_handling(mock_chronicle_client):
    """Test that API errors are caught and returned formatted."""
    with patch("secops_mcp.tools.case_close_definitions.get_chronicle_client", return_value=mock_chronicle_client), \
         patch("secops_mcp.tools.case_close_definitions.chronicle_paginated_request", side_effect=Exception("API failure")):
        result = await list_case_close_definitions()

        assert isinstance(result, dict)
        assert "error" in result
        assert "API failure" in result["error"]
