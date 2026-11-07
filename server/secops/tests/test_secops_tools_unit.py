"Unit tests for time range parameters in search tools."

import sys
import os
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta

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
    
    # Make @server.tool() a pass-through decorator
    def tool_decorator(*args, **kwargs):
        def wrapper(func):
            return func
        return wrapper
    
    # We need to mock FastMCP class to return an instance that has .tool method
    mock_fastmcp_instance = MagicMock()
    mock_fastmcp_instance.tool.side_effect = tool_decorator
    
    sys.modules["mcp.server.fastmcp"].FastMCP.return_value = mock_fastmcp_instance

from secops_mcp.tools.search import search_udm
from secops_mcp.tools.udm_search import export_udm_search_csv
from secops_mcp.tools.security_events import search_security_events
from secops_mcp.tools.stats import get_stats

@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    # Setup return values for common methods
    client.search_udm.return_value = {"total_events": 0, "events": []}
    client.fetch_udm_search_csv.return_value = {"csv": {"row": []}}
    client.translate_nl_to_udm.return_value = "metadata.event_type = 'USER_LOGIN'"
    client.get_stats.return_value = {
        "columns": ["metadata.event_type", "count"],
        "rows": [
            {"metadata.event_type": "USER_LOGIN", "count": 150},
            {"metadata.event_type": "NETWORK_CONNECTION", "count": 42},
        ],
        "total_rows": 2,
    }
    return client

@pytest.fixture
def mock_get_client(mock_chronicle_client):
    with patch('secops_mcp.tools.search.get_chronicle_client', return_value=mock_chronicle_client) as m1, \
         patch('secops_mcp.tools.udm_search.get_chronicle_client', return_value=mock_chronicle_client) as m2, \
         patch('secops_mcp.tools.security_events.get_chronicle_client', return_value=mock_chronicle_client) as m3, \
         patch('secops_mcp.tools.stats.get_chronicle_client', return_value=mock_chronicle_client) as m4:
        yield mock_chronicle_client

@pytest.mark.asyncio
async def test_search_udm_with_start_time(mock_get_client):
    """Test search_udm with explicit start_time."""
    start_time_iso = "2023-01-01T10:00:00Z"
    
    await search_udm(
        query="test",
        start_time=start_time_iso,
        project_id="test", 
        customer_id="test"
    )
    
    # Verify search_udm was called with the correct datetime object
    call_args = mock_get_client.search_udm.call_args
    assert call_args is not None
    _, kwargs = call_args
    
    assert "start_time" in kwargs
    assert isinstance(kwargs["start_time"], datetime)
    assert kwargs["start_time"].year == 2023
    assert kwargs["start_time"].month == 1
    assert kwargs["start_time"].day == 1
    assert kwargs["start_time"].hour == 10

@pytest.mark.asyncio
async def test_search_udm_with_start_and_end_time(mock_get_client):
    """Test search_udm with explicit start and end times."""
    start_time_iso = "2023-01-01T10:00:00Z"
    end_time_iso = "2023-01-02T10:00:00Z"
    
    await search_udm(
        query="test",
        start_time=start_time_iso,
        end_time=end_time_iso,
        project_id="test",
        customer_id="test"
    )
    
    call_args = mock_get_client.search_udm.call_args
    _, kwargs = call_args
    
    assert kwargs["start_time"].day == 1
    assert kwargs["end_time"].day == 2

@pytest.mark.asyncio
async def test_export_udm_search_csv_with_times(mock_get_client):
    """Test export_udm_search_csv with explicit times."""
    start_time_iso = "2023-01-01T10:00:00Z"
    
    await export_udm_search_csv(
        query="test",
        fields=["test"],
        start_time=start_time_iso,
        project_id="test",
        customer_id="test"
    )
    
    call_args = mock_get_client.fetch_udm_search_csv.call_args
    _, kwargs = call_args
    
    assert kwargs["start_time"].year == 2023

@pytest.mark.asyncio
async def test_search_security_events_with_times(mock_get_client):
    """Test search_security_events with explicit times."""
    start_time_iso = "2023-01-01T10:00:00Z"
    
    await search_security_events(
        text="test query",
        start_time=start_time_iso,
        project_id="test",
        customer_id="test"
    )
    
    call_args = mock_get_client.search_udm.call_args
    _, kwargs = call_args
    
    assert kwargs["start_time"].year == 2023

@pytest.mark.asyncio
async def test_hours_back_fallback_deterministic(mock_get_client):
    """Test hours_back fallback using time mocking for determinism."""
    hours_back = 48
    fixed_now = datetime(2024, 1, 10, 12, 0, 0, tzinfo=timezone.utc)
    
    # Mock datetime in utils module to freeze time
    with patch('secops_mcp.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_now
        # We also need fromisoformat to work if called, but it's not called in fallback path
        # However, parse_time_range imports datetime class, so we are mocking that class.
        # We need to ensure fromisoformat works or isn't called.
        # It IS called if start_time/end_time are strings. Here they are None.
        
        await search_udm(
            query="test",
            hours_back=hours_back,
            project_id="test",
            customer_id="test"
        )
    
    call_args = mock_get_client.search_udm.call_args
    _, kwargs = call_args
    
    expected_end = fixed_now
    expected_start = fixed_now - timedelta(hours=hours_back)
    
    assert kwargs["end_time"] == expected_end
    assert kwargs["start_time"] == expected_start

@pytest.mark.asyncio
async def test_end_time_only_fallback(mock_get_client):
    """Test using end_time without start_time uses hours_back."""
    end_time_iso = "2023-01-02T10:00:00Z"
    hours_back = 24
    
    await search_udm(
        query="test",
        end_time=end_time_iso,
        hours_back=hours_back,
        project_id="test",
        customer_id="test"
    )
    
    call_args = mock_get_client.search_udm.call_args
    _, kwargs = call_args
    
    assert kwargs["end_time"].day == 2
    # Start time should be 24 hours before end time (Jan 1)
    assert kwargs["start_time"].day == 1
    assert kwargs["start_time"].hour == 10

@pytest.mark.asyncio
async def test_invalid_date_format(mock_get_client):
    """Test that invalid date format returns an error structure."""
    invalid_date = "yesterday"
    
    result = await search_udm(
        query="test",
        start_time=invalid_date,
        project_id="test",
        customer_id="test"
    )
    
    assert "error" in result
    assert "Error parsing date format" in result["error"]
    assert "yesterday" in result["error"]

@pytest.mark.asyncio
async def test_start_after_end(mock_get_client):
    """Test that start time after end time returns an error."""
    start_time_iso = "2023-01-02T10:00:00Z"
    end_time_iso = "2023-01-01T10:00:00Z"
    
    result = await search_udm(
        query="test",
        start_time=start_time_iso,
        end_time=end_time_iso,
        project_id="test",
        customer_id="test"
    )
    
    assert "error" in result
    assert "cannot be after end time" in result["error"]

@pytest.mark.asyncio
async def test_export_csv_invalid_date(mock_get_client):
    """Test that export_udm_search_csv returns error string on invalid date."""
    invalid_date = "yesterday"

    result = await export_udm_search_csv(
        query="test",
        fields=["test"],
        start_time=invalid_date,
        project_id="test",
        customer_id="test"
    )

    assert isinstance(result, str)
    assert "Error parsing date format" in result
    assert "yesterday" in result


# ---------------------------------------------------------------------------
# Stats tool tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_stats_returns_structured_result(mock_get_client):
    """Stats results contain typed columns, rows, and total_rows."""
    result = await get_stats(
        query="| stats count() as count by metadata.event_type",
        hours_back=24,
        project_id="test",
        customer_id="test",
    )

    assert "error" not in result, f"Unexpected error: {result.get('error')}"
    assert result["total_rows"] == 2
    assert result["columns"] == ["metadata.event_type", "count"]
    assert len(result["rows"]) == 2
    # Verify row values are typed correctly (int, not string)
    login_row = next(r for r in result["rows"] if r["metadata.event_type"] == "USER_LOGIN")
    assert login_row["count"] == 150


@pytest.mark.asyncio
async def test_get_stats_passes_correct_time_range(mock_get_client):
    """Explicit ISO start/end times are parsed and forwarded as datetime objects."""
    result = await get_stats(
        query="| stats count() by metadata.event_type",
        start_time="2024-03-01T00:00:00Z",
        end_time="2024-03-02T00:00:00Z",
        project_id="test",
        customer_id="test",
    )

    assert "error" not in result
    call_args = mock_get_client.get_stats.call_args
    _, kwargs = call_args
    assert isinstance(kwargs["start_time"], datetime)
    assert kwargs["start_time"].year == 2024
    assert kwargs["start_time"].month == 3
    assert kwargs["start_time"].day == 1
    assert isinstance(kwargs["end_time"], datetime)
    assert kwargs["end_time"].day == 2


@pytest.mark.asyncio
async def test_get_stats_passes_max_values_param(mock_get_client):
    """max_values is forwarded to the underlying chronicle client."""
    await get_stats(
        query="| stats count() by principal.ip",
        max_values=100,
        project_id="test",
        customer_id="test",
    )

    call_kwargs = mock_get_client.get_stats.call_args[1]
    assert call_kwargs["max_values"] == 100


@pytest.mark.asyncio
async def test_get_stats_invalid_date_returns_error(mock_get_client):
    """Invalid ISO date returns error dict — not an exception."""
    result = await get_stats(
        query="| stats count() by metadata.event_type",
        start_time="not-a-date",
        project_id="test",
        customer_id="test",
    )

    assert "error" in result
    assert "Error parsing date format" in result["error"]
    assert result["columns"] == []
    assert result["rows"] == []
    assert result["total_rows"] == 0
    # Chronicle client must NOT have been called on a bad date
    mock_get_client.get_stats.assert_not_called()


@pytest.mark.asyncio
async def test_get_stats_api_error_returns_error_dict(mock_get_client):
    """A runtime exception from the Chronicle client surfaces as an error dict."""
    mock_get_client.get_stats.side_effect = Exception("Chronicle API unavailable")

    result = await get_stats(
        query="| stats count() by metadata.event_type",
        project_id="test",
        customer_id="test",
    )

    assert "error" in result
    assert "Chronicle API unavailable" in result["error"]
    assert result["columns"] == []
    assert result["rows"] == []
    assert result["total_rows"] == 0
