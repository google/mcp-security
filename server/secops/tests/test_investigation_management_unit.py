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
"""Unit tests for investigation management diagnostics.

The MCP stdio transport uses stdout for JSON-RPC, so these tools must report
progress and errors through the secops-mcp logger and leave stdout alone.
"""

import logging
from unittest.mock import MagicMock, patch

import pytest

from secops_mcp.tools.investigation_management import (
    fetch_associated_investigations,
    get_investigation,
    list_investigations,
    trigger_investigation,
)

LOGGER_NAME = "secops-mcp"


@pytest.fixture
def chronicle_client():
    with patch(
        "secops_mcp.tools.investigation_management.get_chronicle_client"
    ) as factory:
        client = MagicMock()
        factory.return_value = client
        yield client


def logs(caplog):
    """Return (level, message) pairs emitted by the secops-mcp logger."""
    return [
        (record.levelname, record.getMessage())
        for record in caplog.records
        if record.name == LOGGER_NAME
    ]


@pytest.mark.asyncio
async def test_list_investigations_logs_progress(
    chronicle_client, caplog, capsys
):
    chronicle_client.list_investigations.return_value = {
        "investigations": [{"name": "investigations/inv-1"}]
    }

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await list_investigations(page_size=10)

    assert result == {"investigations": [{"name": "investigations/inv-1"}]}
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Listing investigations (page_size=10)..."),
        ("INFO", "Successfully retrieved 1 investigation(s)"),
    ]


@pytest.mark.asyncio
async def test_list_investigations_logs_failure(
    chronicle_client, caplog, capsys
):
    chronicle_client.list_investigations.side_effect = RuntimeError("boom")

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await list_investigations()

    assert result == {"error": "Error listing investigations: boom"}
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Listing investigations (page_size=50)..."),
        ("ERROR", "Error listing investigations: boom"),
    ]
    assert caplog.records[-1].exc_info[0] is RuntimeError


@pytest.mark.asyncio
async def test_get_investigation_logs_progress(
    chronicle_client, caplog, capsys
):
    chronicle_client.get_investigation.return_value = {
        "name": "investigations/inv-1"
    }

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await get_investigation(investigation_id="inv-1")

    assert result == {"name": "investigations/inv-1"}
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Retrieving investigation: inv-1..."),
        ("INFO", "Successfully retrieved investigation: inv-1"),
    ]


@pytest.mark.asyncio
async def test_get_investigation_logs_failure(
    chronicle_client, caplog, capsys
):
    chronicle_client.get_investigation.side_effect = ValueError("nope")

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await get_investigation(investigation_id="inv-1")

    assert result == {"error": "Error retrieving investigation inv-1: nope"}
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Retrieving investigation: inv-1..."),
        ("ERROR", "Error retrieving investigation inv-1: nope"),
    ]
    assert caplog.records[-1].exc_info[0] is ValueError


@pytest.mark.asyncio
async def test_trigger_investigation_logs_progress(
    chronicle_client, caplog, capsys
):
    chronicle_client.trigger_investigation.return_value = {
        "name": "investigations/inv-1",
        "displayName": "Triggered investigation",
        "status": "RUNNING",
        "triggerType": "MANUAL",
        "createTime": "2026-05-28T18:58:18Z",
    }

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await trigger_investigation(alert_id="alert-1")

    assert result["message"] == "Successfully triggered investigation"
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Triggering investigation for alert: alert-1..."),
        ("INFO", "Successfully triggered investigation for alert: alert-1"),
    ]


@pytest.mark.asyncio
async def test_trigger_investigation_logs_failure(
    chronicle_client, caplog, capsys
):
    chronicle_client.trigger_investigation.side_effect = RuntimeError("down")

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await trigger_investigation(alert_id="alert-1")

    assert result == {
        "error": "Error triggering investigation for alert alert-1: down"
    }
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Triggering investigation for alert: alert-1..."),
        ("ERROR", "Error triggering investigation for alert alert-1: down"),
    ]
    assert caplog.records[-1].exc_info[0] is RuntimeError


@pytest.mark.asyncio
async def test_fetch_associated_investigations_logs_progress(
    chronicle_client, caplog, capsys
):
    chronicle_client.fetch_associated_investigations.return_value = {
        "associationsList": {
            "alert-1": {
                "investigations": [
                    {
                        "name": "investigations/inv-1",
                        "displayName": "Investigation 1",
                        "verdict": "MALICIOUS",
                        "confidence": "HIGH",
                        "status": "COMPLETE",
                    }
                ]
            }
        }
    }

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await fetch_associated_investigations(
            detection_type="ALERT", alert_ids=["alert-1"]
        )

    assert result["total_investigations"] == 1
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Fetching investigations for 1 alert(s)..."),
        ("INFO", "Successfully retrieved 1 investigation(s) for 1 alert(s)"),
    ]


@pytest.mark.asyncio
async def test_fetch_associated_investigations_logs_failure(
    chronicle_client, caplog, capsys
):
    chronicle_client.fetch_associated_investigations.side_effect = (
        RuntimeError("denied")
    )

    with caplog.at_level(logging.INFO, logger=LOGGER_NAME):
        result = await fetch_associated_investigations(
            detection_type="CASE", case_ids=["case-1"]
        )

    assert result == {
        "error": "Error fetching associated investigations: denied"
    }
    assert capsys.readouterr().out == ""
    assert logs(caplog) == [
        ("INFO", "Fetching investigations for 1 case(s)..."),
        ("ERROR", "Error fetching associated investigations: denied"),
    ]
    assert caplog.records[-1].exc_info[0] is RuntimeError
