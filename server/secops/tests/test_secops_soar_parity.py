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
"""Unit tests for SOAR Parity MCP tools in secops."""

import asyncio
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure server/secops is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

# Mock secops if not installed
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
    import mcp.server.fastmcp
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

# Mock pytest if not installed
try:
    import pytest
except ImportError:
    mock_pytest = MagicMock()
    mock_pytest.mark.asyncio = lambda f: f
    mock_pytest.fixture = lambda f: f
    sys.modules["pytest"] = mock_pytest
    pytest = mock_pytest

from secops_mcp.tools.case_management import (
    list_case_comments,
    create_case_comment,
    post_case_comment,
    get_case_full_details,
)
from secops_mcp.tools.case_alert_management import (
    list_alert_group_identifiers_by_case,
    list_events_by_alert,
    list_involved_events,
)
from secops_mcp.tools.entity_investigation import (
    get_involved_entity,
    list_involved_entities,
    get_entities_by_alert_group_identifiers,
    get_entity_details,
    search_entity,
)
from secops_mcp.tools.integration_management import (
    list_integrations,
    list_integration_actions,
    list_integration_instances,
    execute_integration_instance_test,
    execute_manual_action,
    get_action_result_by_id,
)
from secops_mcp.tools.playbook_management import (
    list_playbooks,
    get_playbook,
    list_playbook_instances,
    execute_playbook,
    trigger_playbook,
)
from secops_mcp.tools.connector_event_management import (
    list_connector_events,
    get_connector_event,
)


@pytest.fixture
def mock_chronicle():
    client = MagicMock()
    client.instance_id = "projects/test-proj/locations/us/instances/test-cust"
    client.base_url = "https://chronicle.googleapis.com/v1alpha"
    client.base_v1_url = "https://chronicle.googleapis.com/v1"

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = '{"name": "test"}'
    mock_resp.json.return_value = {"name": "test", "items": []}
    client.session.get.return_value = mock_resp
    client.session.post.return_value = mock_resp
    client.session.patch.return_value = mock_resp

    return client


# --- Case Comments and Full Details Tests ---


@pytest.mark.asyncio
async def test_case_comments(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        list_res = await list_case_comments(case_id="case_123")
        assert "error" not in list_res
        mock_chronicle.session.get.assert_called()

        create_res = await create_case_comment(case_id="case_123", comment="Test comment")
        assert "error" not in create_res
        mock_chronicle.session.post.assert_called()

        post_res = await post_case_comment(case_id="case_123", comment="Alias comment")
        assert "error" not in post_res


@pytest.mark.asyncio
async def test_get_case_full_details(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        res = await get_case_full_details(case_id="case_123")
        assert "error" not in res
        assert "case_details" in res
        assert "case_alerts" in res
        assert "case_comments" in res


# --- Alert Group Identifiers and Events Tests ---


@pytest.mark.asyncio
async def test_alert_group_and_events(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        groups_res = await list_alert_group_identifiers_by_case(case_id="case_123")
        assert "error" not in groups_res

        events_res = await list_events_by_alert(case_id="case_123", alert_id="alert_456")
        assert "error" not in events_res

        inv_events_res = await list_involved_events(case_id="case_123", alert_id="alert_456")
        assert "error" not in inv_events_res


# --- Entity Investigation Tests ---


@pytest.mark.asyncio
async def test_entity_investigation(mock_chronicle):
    with patch("secops_mcp.tools.entity_investigation.get_chronicle_client", return_value=mock_chronicle):
        inv_ent = await get_involved_entity(case_id="c1", alert_id="a1", involved_entity_id="e1")
        assert "error" not in inv_ent

        list_inv = await list_involved_entities(case_id="c1", alert_id="a1")
        assert "error" not in list_inv

        by_groups = await get_entities_by_alert_group_identifiers(case_id="c1", alert_group_identifiers=["g1"])
        assert "error" not in by_groups

        ent_details = await get_entity_details(entity_identifier="192.168.1.1", entity_type="IP Address")
        assert "error" not in ent_details

        search_res = await search_entity(term="corp", is_suspicious=True)
        assert "error" not in search_res


# --- Integration Management Tests ---


@pytest.mark.asyncio
async def test_integration_management(mock_chronicle):
    with patch("secops_mcp.tools.integration_management.get_chronicle_client", return_value=mock_chronicle):
        integrations = await list_integrations()
        assert "error" not in integrations

        actions = await list_integration_actions(integration_id="SiemplifyUtilities")
        assert "error" not in actions

        instances = await list_integration_instances(integration_id="SiemplifyUtilities")
        assert "error" not in instances

        inst_test = await execute_integration_instance_test(
            integration_id="VirusTotalV3",
            instance_id="3e9496eb-09cd-4b3c-a4ce-4c788d6663a7",
        )
        assert "error" not in inst_test

        exec_action = await execute_manual_action(
            case_id="c1",
            action_name="SiemplifyUtilities_Ping",
            properties={"ScriptName": "SiemplifyUtilities_Ping"},
        )
        assert "error" not in exec_action

        action_res = await get_action_result_by_id(action_result_id="res_123")
        assert "error" not in action_res


# --- Playbook Management Tests ---


@pytest.mark.asyncio
async def test_playbook_management(mock_chronicle):
    with patch("secops_mcp.tools.playbook_management.get_chronicle_client", return_value=mock_chronicle):
        playbooks = await list_playbooks(playbook_types=["REGULAR"])
        assert "error" not in playbooks

        playbook = await get_playbook(playbook_id="pb_123")
        assert "error" not in playbook

        instances = await list_playbook_instances(case_id="c1")
        assert "error" not in instances

        exec_pb = await execute_playbook(case_id="c1", playbook_id="pb_123")
        assert "error" not in exec_pb

        trig_pb = await trigger_playbook(case_id="c1", playbook_id="pb_123")
        assert "error" not in trig_pb


# --- Connector Events Tests ---


@pytest.mark.asyncio
async def test_connector_events(mock_chronicle):
    with patch("secops_mcp.tools.connector_event_management.get_chronicle_client", return_value=mock_chronicle):
        events = await list_connector_events(connector_id="conn_1")
        assert "error" not in events

        event = await get_connector_event(connector_event_id="ev_123")
        assert "error" not in event


class TestSoarParityUnit(unittest.TestCase):
    """Unittest test runner for all SOAR parity tools."""

    def setUp(self):
        self.mock_chronicle = mock_chronicle()

    def test_case_comments(self):
        asyncio.run(test_case_comments(self.mock_chronicle))

    def test_get_case_full_details(self):
        asyncio.run(test_get_case_full_details(self.mock_chronicle))

    def test_alert_group_and_events(self):
        asyncio.run(test_alert_group_and_events(self.mock_chronicle))

    def test_entity_investigation(self):
        asyncio.run(test_entity_investigation(self.mock_chronicle))

    def test_integration_management(self):
        asyncio.run(test_integration_management(self.mock_chronicle))

    def test_playbook_management(self):
        asyncio.run(test_playbook_management(self.mock_chronicle))

    def test_connector_events(self):
        asyncio.run(test_connector_events(self.mock_chronicle))
