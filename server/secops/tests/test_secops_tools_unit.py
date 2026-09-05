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
from secops_mcp.tools.security_rules import get_rule_detections, test_rule as secops_test_rule
from secops_mcp.tools.ioc_matches import get_ioc_matches

@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    # Setup return values for common methods
    client.search_udm.return_value = {"total_events": 0, "events": []}
    client.fetch_udm_search_csv.return_value = {"csv": {"row": []}}
    client.translate_nl_to_udm.return_value = "metadata.event_type = 'USER_LOGIN'"
    client.list_iocs.return_value = {"matches": []}
    return client

@pytest.fixture
def mock_get_client(mock_chronicle_client):
    with patch('secops_mcp.tools.search.get_chronicle_client', return_value=mock_chronicle_client) as m1, \
         patch('secops_mcp.tools.udm_search.get_chronicle_client', return_value=mock_chronicle_client) as m2, \
         patch('secops_mcp.tools.security_events.get_chronicle_client', return_value=mock_chronicle_client) as m3, \
         patch('secops_mcp.tools.security_rules.get_chronicle_client', return_value=mock_chronicle_client), \
         patch('secops_mcp.tools.ioc_matches.get_chronicle_client', return_value=mock_chronicle_client):
        yield mock_chronicle_client


@pytest.mark.asyncio
async def test_get_rule_detections_forwards_filters(mock_get_client):
    """Test detection filters use the Chronicle SDK parameter names."""
    expected = {"detections": []}

    def list_detections(
        rule_id,
        start_time=None,
        end_time=None,
        list_basis=None,
        alert_state=None,
        page_size=None,
        page_token=None,
    ):
        if start_time:
            start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return expected

    mock_get_client.list_detections.side_effect = list_detections

    result = await get_rule_detections(
        "ru_test",
        alert_state="ALERTING",
        page_size=25,
        page_token="next-page",
    )

    assert result == expected
    call_args = mock_get_client.list_detections.call_args
    assert call_args.args == ("ru_test",)
    assert call_args.kwargs["alert_state"] == "ALERTING"
    assert call_args.kwargs["page_size"] == 25
    assert call_args.kwargs["page_token"] == "next-page"


@pytest.mark.asyncio
async def test_get_rule_detections_forwards_time_range(mock_get_client):
    """Test detection time range parameters are converted and forwarded."""
    await get_rule_detections(
        "ru_test",
        start_time="2025-01-20T00:00:00Z",
        end_time="2025-01-27T23:59:59Z",
        list_basis="DETECTION_TIME",
    )

    call_args = mock_get_client.list_detections.call_args
    assert call_args.kwargs["start_time"] == datetime(
        2025, 1, 20, tzinfo=timezone.utc
    )
    assert call_args.kwargs["end_time"] == datetime(
        2025, 1, 27, 23, 59, 59, tzinfo=timezone.utc
    )
    assert call_args.kwargs["list_basis"] == "DETECTION_TIME"

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


# =========================================================================
# Tests for test_rule (PR #143)
# =========================================================================

@pytest.mark.asyncio
async def test_test_rule_buffers_end_time_to_start_of_hour(mock_get_client):
    """Test test_rule buffers end_time to start of current hour."""
    mock_get_client.run_rule_test.return_value = [
        {"type": "detection", "detection": {"ruleName": "test_rule", "id": "d-1"}},
        {"type": "progress", "percentDone": 100},
    ]

    result = await secops_test_rule(
        rule_text="rule test { condition: true }",
        project_id="my-proj",
        customer_id="my-cust",
        region="us",
        hours_back=24,
    )

    # Verify run_rule_test was invoked
    mock_get_client.run_rule_test.assert_called_once()
    _, kwargs = mock_get_client.run_rule_test.call_args

    # Check end_time has minute, second, microsecond set to 0 (buffered to start of hour)
    end_time = kwargs["end_time"]
    start_time = kwargs["start_time"]
    assert end_time.minute == 0
    assert end_time.second == 0
    assert end_time.microsecond == 0

    # Check start_time is 24 hours before end_time
    assert end_time - start_time == timedelta(hours=24)

    # Check output contains detection summary
    assert "Total Detections: 1" in result
    assert "Rule successfully detected 1 event(s)" in result


# =========================================================================
# Tests for get_ioc_matches formatting (Issue #264)
# =========================================================================

@pytest.mark.asyncio
async def test_get_ioc_matches_multi_indicator(mock_get_client):
    """Test get_ioc_matches surfaces all indicator fields (e.g. domain and url)."""
    mock_get_client.list_iocs.return_value = {
        "matches": [
            {
                "artifactIndicator": {
                    "domain": "bad-domain.com",
                    "url": "https://bad-domain.com/malware.exe",
                },
                "sources": ["US_CERT", "MANDIANT"],
                "firstSeenTime": "2025-01-01T00:00:00Z",
                "lastSeenTime": "2025-01-02T00:00:00Z",
                "category": "MALWARE",
                "severity": "HIGH",
                "confidence": "HIGH",
                "associatedEntity": "workstation-01",
            }
        ]
    }

    result = await get_ioc_matches()

    assert "Found 1 IoC matches:" in result
    assert "domain=bad-domain.com" in result or "domain: bad-domain.com" in result
    assert "url=https://bad-domain.com/malware.exe" in result or "url: https://bad-domain.com/malware.exe" in result
    assert "First Seen: 2025-01-01T00:00:00Z" in result
    assert "Last Seen: 2025-01-02T00:00:00Z" in result
    assert "Category: MALWARE" in result
    assert "Severity: HIGH" in result
    assert "Confidence: HIGH" in result
    assert "Associated Entity: workstation-01" in result or "Associated: workstation-01" in result
    assert "Sources: US_CERT, MANDIANT" in result


@pytest.mark.asyncio
async def test_get_ioc_matches_snake_case_fields(mock_get_client):
    """Test get_ioc_matches handles snake_case keys from SDK response."""
    mock_get_client.list_iocs.return_value = {
        "matches": [
            {
                "artifact_indicator": {
                    "hash_sha256": "abcdef1234567890",
                    "file_name": "trojan.exe",
                },
                "sources": ["VIRUSTOTAL"],
                "first_seen_time": "2025-01-10T12:00:00Z",
                "last_seen_time": "2025-01-11T12:00:00Z",
                "ioc_category": "TROJAN",
                "ioc_severity": "CRITICAL",
                "ioc_confidence": "HIGH",
                "associated_entity": "host-finance",
            }
        ]
    }

    result = await get_ioc_matches()

    assert "Found 1 IoC matches:" in result
    assert "hash_sha256" in result and "abcdef1234567890" in result
    assert "file_name" in result and "trojan.exe" in result
    assert "First Seen: 2025-01-10T12:00:00Z" in result
    assert "Last Seen: 2025-01-11T12:00:00Z" in result
    assert "Category: TROJAN" in result
    assert "Severity: CRITICAL" in result
    assert "Confidence: HIGH" in result
    assert "host-finance" in result
    assert "Sources: VIRUSTOTAL" in result


@pytest.mark.asyncio
async def test_get_ioc_matches_no_matches(mock_get_client):
    """Test get_ioc_matches returns friendly message when no matches found."""
    mock_get_client.list_iocs.return_value = {"matches": []}
    result = await get_ioc_matches()
    assert result == "No IoC matches found for the specified time range."
>>>>>>> 077b983 (fix(secops): surface all indicator fields and metadata in get_ioc_matches)

