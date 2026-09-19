# Copyright 2025 Google LLC
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
"""Unit tests for case management MCP tools."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure server/secops is in path to import secops_mcp
current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

# Mock secops if not installed (for unit testing without dependencies)
try:
    import secops
except ImportError:
    mock_secops = MagicMock()
    sys.modules["secops"] = mock_secops
    sys.modules["secops.chronicle"] = MagicMock()
    sys.modules["secops.chronicle.client"] = MagicMock()
    sys.modules["secops.chronicle.utils"] = MagicMock()
    sys.modules["secops.chronicle.utils.request_utils"] = MagicMock()
    sys.modules["secops.exceptions"] = MagicMock()

# Mock mcp if not installed
try:
    import mcp
except ImportError:
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

    sys.modules["mcp.server.fastmcp"].FastMCP.return_value = (
        mock_fastmcp_instance
    )

from secops.chronicle.client import APIVersion
from secops_mcp.tools.case_management import (
    create_case,
    create_manual_case,
    create_or_update_case,
)


@pytest.fixture
def mock_chronicle_client():
    return MagicMock()


@pytest.mark.asyncio
async def test_create_case_success(mock_chronicle_client):
    """Test successful case package creation via create_case."""
    case_payload = {"cases": [{"id": "c1", "title": "Test Case"}]}
    expected_response = {"status": "SUCCESS"}

    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ) as mock_get_client,
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            return_value=expected_response,
        ) as mock_request,
    ):
        result = await create_case(
            case_data=case_payload,
            project_id="proj-123",
            customer_id="cust-456",
            region="us",
        )

        mock_get_client.assert_called_once_with("proj-123", "cust-456", "us")
        mock_request.assert_called_once_with(
            mock_chronicle_client,
            method="POST",
            endpoint_path="legacyCases:createCase",
            api_version=APIVersion.V1ALPHA,
            json=case_payload,
            error_message="Failed to create case package",
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_create_case_empty_payload():
    """Test create_case with empty payload."""
    result = await create_case(case_data={})
    assert result == {"error": "case_data parameter is required and cannot be empty"}


@pytest.mark.asyncio
async def test_create_case_error_handling(mock_chronicle_client):
    """Test create_case error handling."""
    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ),
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            side_effect=Exception("API failure"),
        ),
    ):
        result = await create_case(case_data={"key": "value"})
        assert "error" in result
        assert "Error creating case package: API failure" in result["error"]


@pytest.mark.asyncio
async def test_create_manual_case_success(mock_chronicle_client):
    """Test successful manual case creation via create_manual_case."""
    case_payload = {
        "title": "Manual Case",
        "priority": "HIGH",
        "tags": ["suspicious"],
    }
    expected_response = {"name": "cases/m123"}

    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ) as mock_get_client,
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            return_value=expected_response,
        ) as mock_request,
    ):
        result = await create_manual_case(
            case_data=case_payload,
            project_id="proj-123",
            customer_id="cust-456",
            region="us",
        )

        mock_get_client.assert_called_once_with("proj-123", "cust-456", "us")
        mock_request.assert_called_once_with(
            mock_chronicle_client,
            method="POST",
            endpoint_path="legacyCases:createManualCase",
            api_version=APIVersion.V1ALPHA,
            json=case_payload,
            error_message="Failed to create manual case",
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_create_manual_case_empty_payload():
    """Test create_manual_case with empty payload."""
    result = await create_manual_case(case_data={})
    assert result == {"error": "case_data parameter is required and cannot be empty"}


@pytest.mark.asyncio
async def test_create_or_update_case_success(mock_chronicle_client):
    """Test successful case upsert via create_or_update_case."""
    case_payload = {"caseId": "c123", "summary": "Updated summary"}
    expected_response = {"caseId": "c123", "status": "OPEN"}

    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ) as mock_get_client,
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            return_value=expected_response,
        ) as mock_request,
    ):
        result = await create_or_update_case(
            case_data=case_payload,
            project_id="proj-123",
            customer_id="cust-456",
            region="us",
        )

        mock_get_client.assert_called_once_with("proj-123", "cust-456", "us")
        mock_request.assert_called_once_with(
            mock_chronicle_client,
            method="POST",
            endpoint_path="legacyCreateOrUpdateCase",
            api_version=APIVersion.V1ALPHA,
            json=case_payload,
            error_message="Failed to create or update case",
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_create_or_update_case_empty_payload():
    """Test create_or_update_case with empty payload."""
    result = await create_or_update_case(case_data={})
    assert result == {"error": "case_data parameter is required and cannot be empty"}
