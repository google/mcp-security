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
"""Unit tests for Chronicle 1P Case and Case Alert Management MCP tools."""

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
    list_cases,
    get_case,
    update_case,
    change_case_priority,
    change_case_stage,
    assign_case,
    set_custom_case_fields,
    add_case_tag,
    remove_case_tag,
    add_case_insight,
    pause_case_sla,
    resume_case_sla,
    close_case,
    reopen_case,
)
from secops_mcp.tools.case_alert_management import (
    list_case_alerts,
    get_case_alert,
    update_case_alert,
    change_alert_priority,
    set_alert_custom_fields,
    move_case_alert,
    add_alert_tag,
    remove_alert_tag,
)


@pytest.fixture
def mock_chronicle():
    client = MagicMock()
    client.instance_id = "projects/test-proj/locations/us/instances/test-cust"
    client.base_url = "https://chronicle.googleapis.com/v1alpha"
    client.base_v1_url = "https://chronicle.googleapis.com/v1"

    # Mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = '{"name": "test"}'
    mock_resp.json.return_value = {"name": "test", "cases": []}
    client.session.get.return_value = mock_resp
    client.session.post.return_value = mock_resp
    client.session.patch.return_value = mock_resp

    return client


# --- Case Management Tool Tests ---


@pytest.mark.asyncio
async def test_list_cases(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await list_cases(
            project_id="test-proj",
            customer_id="test-cust",
            region="us",
            filter_query='priority = "HIGH"',
            page_size=25,
        )
        assert "error" not in result
        mock_chronicle.session.get.assert_called_once()
        args, kwargs = mock_chronicle.session.get.call_args
        assert "/cases" in args[0]
        assert kwargs["params"]["pageSize"] == 25
        assert kwargs["params"]["filter"] == 'priority = "HIGH"'


@pytest.mark.asyncio
async def test_get_case(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await get_case(case_id="case_123")
        assert "error" not in result
        mock_chronicle.session.get.assert_called_once()
        args, _ = mock_chronicle.session.get.call_args
        assert "/cases/case_123" in args[0]


@pytest.mark.asyncio
async def test_update_case(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await update_case(
            case_id="case_123",
            update_mask="priority,stage",
            priority="HIGH",
            stage="Containment",
        )
        assert "error" not in result
        mock_chronicle.session.patch.assert_called_once()
        args, kwargs = mock_chronicle.session.patch.call_args
        assert "/cases/case_123" in args[0]
        assert kwargs["params"]["updateMask"] == "priority,stage"
        assert kwargs["json"]["priority"] == "PRIORITY_HIGH"
        assert kwargs["json"]["stage"] == "Containment"


@pytest.mark.asyncio
async def test_change_case_priority_trigger(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await change_case_priority(
            case_ids=["case_1", "case_2"],
            priority="CRITICAL",
        )
        assert result["status"] == "SUCCESS"
        mock_chronicle.session.post.assert_called_once()
        args, kwargs = mock_chronicle.session.post.call_args
        assert ":executeBulkChangePriority" in args[0]
        assert kwargs["json"]["priority"] == "PRIORITY_CRITICAL"
        assert len(kwargs["json"]["names"]) == 2


@pytest.mark.asyncio
async def test_change_case_stage_trigger(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await change_case_stage(
            case_ids="case_1",
            stage="Triage",
        )
        assert result["status"] == "SUCCESS"
        mock_chronicle.session.post.assert_called_once()
        args, kwargs = mock_chronicle.session.post.call_args
        assert ":executeBulkChangeStage" in args[0]
        assert kwargs["json"]["stage"] == "Triage"


@pytest.mark.asyncio
async def test_assign_case_trigger(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await assign_case(
            case_ids="case_1",
            assignee="analyst@example.com",
        )
        assert result["status"] == "SUCCESS"
        mock_chronicle.session.post.assert_called_once()
        args, kwargs = mock_chronicle.session.post.call_args
        assert ":executeBulkAssign" in args[0]
        assert kwargs["json"]["assignee"] == "analyst@example.com"


@pytest.mark.asyncio
async def test_set_custom_case_fields_trigger(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        result = await set_custom_case_fields(
            case_id="case_1",
            custom_fields={"Department": "SecOps", "Impact": "High"},
        )
        assert "error" not in result
        mock_chronicle.session.patch.assert_called_once()
        args, kwargs = mock_chronicle.session.patch.call_args
        assert "/cases/case_1" in args[0]
        assert kwargs["params"]["updateMask"] == "custom_field_values"
        assert len(kwargs["json"]["customFieldValues"]) == 2


@pytest.mark.asyncio
async def test_add_and_remove_case_tag(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        add_res = await add_case_tag(case_id="case_1", tag="Phishing")
        assert "error" not in add_res
        rem_res = await remove_case_tag(case_id="case_1", tag="Phishing")
        assert "error" not in rem_res


@pytest.mark.asyncio
async def test_sla_and_case_closure(mock_chronicle):
    with patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle):
        pause_res = await pause_case_sla(case_id="case_1", reason="Waiting for customer response")
        assert pause_res["status"] == "SUCCESS"
        resume_res = await resume_case_sla(case_id="case_1")
        assert resume_res["status"] == "SUCCESS"

        close_res = await close_case(case_ids="case_1", closure_reason="Resolved", comment="Fixed")
        assert close_res["status"] == "SUCCESS"
        reopen_res = await reopen_case(case_ids="case_1", comment="New activity detected")
        assert reopen_res["status"] == "SUCCESS"


# --- Case Alert Management Tool Tests ---


@pytest.mark.asyncio
async def test_list_case_alerts(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        result = await list_case_alerts(case_id="case_1")
        assert "error" not in result
        mock_chronicle.session.get.assert_called_once()
        args, _ = mock_chronicle.session.get.call_args
        assert "/cases/case_1/caseAlerts" in args[0]


@pytest.mark.asyncio
async def test_get_case_alert(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        result = await get_case_alert(case_id="case_1", alert_id="alert_99")
        assert "error" not in result
        mock_chronicle.session.get.assert_called_once()
        args, _ = mock_chronicle.session.get.call_args
        assert "/cases/case_1/caseAlerts/alert_99" in args[0]


@pytest.mark.asyncio
async def test_change_alert_priority_trigger(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        result = await change_alert_priority(
            case_id="case_1",
            alert_id="alert_99",
            priority="CRITICAL",
        )
        assert "error" not in result
        mock_chronicle.session.patch.assert_called_once()
        args, kwargs = mock_chronicle.session.patch.call_args
        assert "/cases/case_1/caseAlerts/alert_99" in args[0]
        assert kwargs["params"]["updateMask"] == "priority"
        assert kwargs["json"]["priority"] == "PRIORITY_CRITICAL"


@pytest.mark.asyncio
async def test_set_alert_custom_fields_trigger(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        result = await set_alert_custom_fields(
            case_id="case_1",
            alert_id="alert_99",
            custom_fields={"MalwareFamily": "Emotet"},
        )
        assert "error" not in result
        mock_chronicle.session.patch.assert_called_once()
        args, kwargs = mock_chronicle.session.patch.call_args
        assert "/cases/case_1/caseAlerts/alert_99" in args[0]
        assert kwargs["params"]["updateMask"] == "custom_field_values"


@pytest.mark.asyncio
async def test_move_case_alert(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        result = await move_case_alert(
            source_case_id="case_1",
            alert_id="alert_99",
            destination_case_id="case_2",
        )
        assert "error" not in result
        mock_chronicle.session.post.assert_called_once()
        args, kwargs = mock_chronicle.session.post.call_args
        assert "/cases/case_1/caseAlerts/alert_99:move" in args[0]
        assert kwargs["json"]["destinationCaseId"] == "case_2"


@pytest.mark.asyncio
async def test_alert_tags(mock_chronicle):
    with patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle):
        add_res = await add_alert_tag(case_id="case_1", alert_id="alert_99", tag="CriticalAsset")
        assert "error" not in add_res
        rem_res = await remove_alert_tag(case_id="case_1", alert_id="alert_99", tag="CriticalAsset")
        assert "error" not in rem_res


class TestCaseManagementUnit(unittest.TestCase):
    """Unittest TestCase to execute test suite under python -m unittest."""

    def setUp(self):
        self.mock_chronicle = mock_chronicle()

    def test_list_cases(self):
        import asyncio
        asyncio.run(test_list_cases(self.mock_chronicle))

    def test_get_case(self):
        import asyncio
        asyncio.run(test_get_case(self.mock_chronicle))

    def test_update_case(self):
        import asyncio
        asyncio.run(test_update_case(self.mock_chronicle))

    def test_change_case_priority_trigger(self):
        import asyncio
        asyncio.run(test_change_case_priority_trigger(self.mock_chronicle))

    def test_change_case_stage_trigger(self):
        import asyncio
        asyncio.run(test_change_case_stage_trigger(self.mock_chronicle))

    def test_assign_case_trigger(self):
        import asyncio
        asyncio.run(test_assign_case_trigger(self.mock_chronicle))

    def test_set_custom_case_fields_trigger(self):
        import asyncio
        asyncio.run(test_set_custom_case_fields_trigger(self.mock_chronicle))

    def test_add_and_remove_case_tag(self):
        import asyncio
        asyncio.run(test_add_and_remove_case_tag(self.mock_chronicle))

    def test_sla_and_case_closure(self):
        import asyncio
        asyncio.run(test_sla_and_case_closure(self.mock_chronicle))

    def test_list_case_alerts(self):
        import asyncio
        asyncio.run(test_list_case_alerts(self.mock_chronicle))

    def test_get_case_alert(self):
        import asyncio
        asyncio.run(test_get_case_alert(self.mock_chronicle))

    def test_change_alert_priority_trigger(self):
        import asyncio
        asyncio.run(test_change_alert_priority_trigger(self.mock_chronicle))

    def test_set_alert_custom_fields_trigger(self):
        import asyncio
        asyncio.run(test_set_alert_custom_fields_trigger(self.mock_chronicle))

    def test_move_case_alert(self):
        import asyncio
        asyncio.run(test_move_case_alert(self.mock_chronicle))

    def test_alert_tags(self):
        import asyncio
        asyncio.run(test_alert_tags(self.mock_chronicle))

