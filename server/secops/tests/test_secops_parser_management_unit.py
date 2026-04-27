"""Unit tests for parser management tools."""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch

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
    sys.modules["mcp.server.fastmcp"].FastMCP.return_value = mock_fastmcp_instance

from secops_mcp.tools.parser_management import list_parsers


@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    client.list_parsers.return_value = []
    return client


@pytest.fixture
def mock_get_client(mock_chronicle_client):
    with patch(
        "secops_mcp.tools.parser_management.get_chronicle_client",
        return_value=mock_chronicle_client,
    ):
        yield mock_chronicle_client


@pytest.mark.asyncio
async def test_list_parsers_defaults_pass_wildcard_log_type(mock_get_client):
    """By default, list_parsers should query across all log types with as_list=True."""
    await list_parsers(project_id="test", customer_id="test", region="us")

    mock_get_client.list_parsers.assert_called_once_with(
        log_type="-",
        page_size=None,
        page_token=None,
        filter=None,
        as_list=True,
    )


@pytest.mark.asyncio
async def test_list_parsers_forwards_all_args(mock_get_client):
    """Caller-provided log_type, pagination, and filter should pass through verbatim."""
    await list_parsers(
        log_type="OKTA",
        page_size=25,
        page_token="tok123",
        filter='STATE="ACTIVE"',
        project_id="test",
        customer_id="test",
        region="us",
    )

    mock_get_client.list_parsers.assert_called_once_with(
        log_type="OKTA",
        page_size=25,
        page_token="tok123",
        filter='STATE="ACTIVE"',
        as_list=True,
    )


@pytest.mark.asyncio
async def test_list_parsers_empty_response(mock_get_client):
    """An empty parser list should produce a 'No parsers found' message."""
    mock_get_client.list_parsers.return_value = []

    result = await list_parsers(
        log_type="OKTA", project_id="test", customer_id="test", region="us"
    )

    assert "No parsers found" in result
    assert "OKTA" in result


@pytest.mark.asyncio
async def test_list_parsers_formats_results(mock_get_client):
    """Result should include parser ID, log type, state, type, and create time."""
    mock_get_client.list_parsers.return_value = [
        {
            "name": "projects/p/locations/us/instances/i/logTypes/OKTA/parsers/pa_abc",
            "state": "ACTIVE",
            "type": "CUSTOM",
            "createTime": "2025-01-01T00:00:00Z",
        },
        {
            "name": "projects/p/locations/us/instances/i/logTypes/WINDOWS_AD/parsers/pa_def",
            "state": "INACTIVE",
            "type": "PREBUILT",
            "createTime": "2025-02-02T00:00:00Z",
        },
    ]

    result = await list_parsers(project_id="test", customer_id="test", region="us")

    assert "Found 2 parser(s)" in result
    assert "pa_abc" in result
    assert "pa_def" in result
    # Per-parser log type extracted from the resource name
    assert "OKTA" in result
    assert "WINDOWS_AD" in result
    assert "ACTIVE" in result
    assert "INACTIVE" in result
    assert "CUSTOM" in result
    assert "PREBUILT" in result


@pytest.mark.asyncio
async def test_list_parsers_handles_missing_fields(mock_get_client):
    """Parsers missing optional fields should fall back to 'Unknown' rather than error."""
    mock_get_client.list_parsers.return_value = [{"name": ""}]

    result = await list_parsers(project_id="test", customer_id="test", region="us")

    assert "Unknown" in result


@pytest.mark.asyncio
async def test_list_parsers_returns_error_string_on_exception(mock_get_client):
    """SDK errors should be caught and returned as a formatted error string."""
    mock_get_client.list_parsers.side_effect = RuntimeError("boom")

    result = await list_parsers(
        log_type="OKTA", project_id="test", customer_id="test", region="us"
    )

    assert isinstance(result, str)
    assert "Error listing parsers" in result
    assert "boom" in result
    assert "OKTA" in result
