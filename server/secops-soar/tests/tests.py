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

"""Integration tests for Chronicle SecOps SOAR MCP tools.

These tests require proper SOAR authentication and configuration to run.

To run these tests:
1. Make sure you have configured SOAR credentials in your environment or .env
2. Run: pytest -xvs server/secops-soar/tests/tests.py
"""

import mcp
import pytest
import json
from typing import Optional

from secops_soar_mcp.server import mcp as mcp_server

from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from tests.conftest import setup_bindings


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize(
    argnames=["tool_name", "tool_arguments", "expected_substring"],
    argvalues=[
        ("list_cases", None, "nextPageToken"),
        ("get_case_full_details", {"case_id": "9675"}, "case_details"),
        ("list_alerts_by_case", {"case_id": "9675"}, "GooglersOnlySoarCases"),
        ("list_alert_group_identifiers_by_case", {"case_id": "9675"}, "["),
        ("change_case_priority", {"case_id": "9675", "case_priority": "PriorityMedium"}, "PriorityMedium"),
        ("post_case_comment", {"case_id": "9675", "comment": "Verification test comment"}, "Verification test comment"),
    ],
)
async def test_tool(tool_name, tool_arguments, expected_substring, setup_bindings):
    response = await call_tool_and_get_text_response(tool_name, tool_arguments)
    assert expected_substring in response


async def call_tool_and_get_text_response(
    tool_name: str,
    tool_arguments: Optional[dict] = None,  # Optional arguments for the tool
) -> str:
    """
    Calls the specified MCP tool, performs standard checks, and returns the text response.
    Raises AssertionError if standard checks fail.
    """
    # Execute tool call.
    async with client_session(mcp_server._mcp_server) as client:
        if tool_arguments:
            result = await client.call_tool(tool_name, tool_arguments)
        else:
            result = await client.call_tool(tool_name)
        assert isinstance(result, mcp.types.CallToolResult)
        assert result.isError is False
        assert len(result.content) == 1
        assert isinstance(result.content[0], mcp.types.TextContent)
        return result.content[0].text


@pytest.mark.asyncio(loop_scope="session")
async def test_server_connection(setup_bindings):
    """Test that the server is running and accessible."""

    async with client_session(mcp_server._mcp_server) as client:
        tools_result = await client.list_tools()
        assert isinstance(tools_result, mcp.ListToolsResult)
        assert len(tools_result.tools) > 0


@pytest.mark.asyncio(loop_scope="session")
async def test_dynamic_alert_events_and_entities(setup_bindings):
    """Dynamically fetch alerts and entities from case 9675 and test related tools."""
    
    # 1. Fetch case details to find alert IDs and entities
    case_details_str = await call_tool_and_get_text_response("get_case_full_details", {"case_id": "9675"})
    case_details = json.loads(case_details_str)
    
    # 2. Get alerts list
    alerts = case_details.get("case_alerts", [])
    if isinstance(alerts, list) and len(alerts) > 0:
        first_alert = alerts[0]
        alert_id = str(first_alert.get("id"))
        
        # Test list_events_by_alert
        events_str = await call_tool_and_get_text_response(
            "list_events_by_alert", 
            {"case_id": "9675", "alert_id": alert_id}
        )
        assert "events" in events_str or "[" in events_str

    # 3. Test entity details and search if case contains entities
    # Fetch environment of the case to use for entity environment parameters
    env = case_details.get("case_details", {}).get("environment", "GooglersOnlySoarCases")
    
    # Run a generic entity search
    search_str = await call_tool_and_get_text_response("search_entity", {"term": "8.8.8.8"})
    assert "[" in search_str
