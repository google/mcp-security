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
"""Unit tests for security alert formatting."""

import json
from unittest.mock import MagicMock, patch

import pytest

from secops_mcp.tools.security_alerts import (
    do_update_security_alert,
    get_security_alert_by_id,
    get_security_alerts,
)


@pytest.fixture
def chronicle_client():
    with patch(
        "secops_mcp.tools.security_alerts.get_chronicle_client"
    ) as get_chronicle_client:
        client = MagicMock()
        get_chronicle_client.return_value = client
        yield client


@pytest.mark.asyncio
async def test_get_security_alerts_includes_actionable_fields(chronicle_client):
    chronicle_client.get_alerts.return_value = {
        "alerts": {
            "alerts": [
                {
                    "id": "de_f47e71ca",
                    "detection": [{"ruleName": "Phishing"}],
                    "createdTime": "2026-05-28T18:58:18Z",
                    "feedbackSummary": {
                        "status": "OPEN",
                        "verdict": "TRUE_POSITIVE",
                        "severityDisplay": "High",
                    },
                    "caseName": "cases/123",
                }
            ]
        }
    }

    # get_security_alerts currently returns a JSON-encoded display string.
    output = json.loads(
        await get_security_alerts(project_id="test", customer_id="test")
    )

    assert (
        "Alert ID: de_f47e71ca\n"
        "Rule: Phishing\n"
        "Created: 2026-05-28T18:58:18Z\n"
        "Status: OPEN\n"
        "Verdict: TRUE_POSITIVE\n"
        "Severity: High\n"
        "Associated Case: cases/123\n" in output
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("feedback_summary", [None, "invalid", []])
async def test_get_security_alerts_handles_missing_actionable_fields(
    chronicle_client, feedback_summary
):
    chronicle_client.get_alerts.return_value = [
        {
            "ruleName": "Legacy Rule",
            "createdTime": "2026-05-28T19:00:00Z",
            "status": "OPEN",
            "severity": "Medium",
            "feedbackSummary": feedback_summary,
        }
    ]

    output = json.loads(
        await get_security_alerts(project_id="test", customer_id="test")
    )

    assert "Alert ID:" not in output
    assert "Status: OPEN" in output
    assert "Verdict: Unknown" in output
    assert "Severity: Medium" in output


@pytest.mark.asyncio
async def test_get_security_alerts_falls_back_from_empty_feedback_summary(
    chronicle_client,
):
    chronicle_client.get_alerts.return_value = [
        {
            "id": "de_2a5b279c",
            "ruleName": "Untriaged Rule",
            "status": "OPEN",
            "verdict": "FALSE_POSITIVE",
            "severity": "Medium",
            "feedbackSummary": {},
        }
    ]

    output = json.loads(
        await get_security_alerts(project_id="test", customer_id="test")
    )

    assert "Status: OPEN" in output
    assert "Verdict: FALSE_POSITIVE" in output
    assert "Severity: Medium" in output


@pytest.mark.asyncio
async def test_get_security_alerts_preserves_unspecified_verdict(chronicle_client):
    chronicle_client.get_alerts.return_value = [
        {
            "id": "de_92ddcb79",
            "ruleName": "Untriaged Rule",
            "feedbackSummary": {"verdict": "VERDICT_UNSPECIFIED"},
        }
    ]

    output = json.loads(
        await get_security_alerts(project_id="test", customer_id="test")
    )

    assert "Verdict: VERDICT_UNSPECIFIED" in output


@pytest.mark.asyncio
async def test_get_security_alert_by_id_returns_dict(chronicle_client):
    chronicle_client.get_alert.return_value = {
        "id": "de_f47e71ca",
        "detection": [{"ruleName": "Phishing"}],
        "createdTime": "2026-05-28T18:58:18Z",
    }

    result = await get_security_alert_by_id(alert_id="de_f47e71ca")

    assert isinstance(result, dict)
    assert result["id"] == "de_f47e71ca"
    assert result["detection"][0]["ruleName"] == "Phishing"
    chronicle_client.get_alert.assert_called_once_with("de_f47e71ca", True)


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_alert_id", ["", None])
async def test_get_security_alert_by_id_requires_alert_id(
    chronicle_client, invalid_alert_id
):
    result = await get_security_alert_by_id(alert_id=invalid_alert_id)

    assert isinstance(result, dict)
    assert result == {"error": "alert_id is required"}
    chronicle_client.get_alert.assert_not_called()


@pytest.mark.asyncio
async def test_get_security_alert_by_id_handles_error(chronicle_client):
    chronicle_client.get_alert.side_effect = Exception("Alert not found")

    result = await get_security_alert_by_id(alert_id="de_invalid")

    assert isinstance(result, dict)
    assert result == {
        "error": "Error retrieving security alert for de_invalid: Alert not found"
    }


@pytest.mark.asyncio
async def test_do_update_security_alert_returns_dict(chronicle_client):
    chronicle_client.update_alert.return_value = {
        "id": "de_f47e71ca",
        "status": "CLOSED",
        "verdict": "FALSE_POSITIVE",
    }

    result = await do_update_security_alert(
        alert_id="de_f47e71ca",
        status="CLOSED",
        verdict="FALSE_POSITIVE",
    )

    assert isinstance(result, dict)
    assert result["status"] == "CLOSED"
    assert result["verdict"] == "FALSE_POSITIVE"
    chronicle_client.update_alert.assert_called_once_with(
        "de_f47e71ca",
        reason=None,
        status="CLOSED",
        verdict="FALSE_POSITIVE",
        comment=None,
        root_cause=None,
        priority=None,
        severity=None,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_alert_id", ["", None])
async def test_do_update_security_alert_requires_alert_id(
    chronicle_client, invalid_alert_id
):
    result = await do_update_security_alert(alert_id=invalid_alert_id)

    assert isinstance(result, dict)
    assert result == {"error": "alert_id is required"}
    chronicle_client.update_alert.assert_not_called()


@pytest.mark.asyncio
async def test_do_update_security_alert_handles_error(chronicle_client):
    chronicle_client.update_alert.side_effect = Exception("Update failed")

    result = await do_update_security_alert(alert_id="de_f47e71ca", status="CLOSED")

    assert isinstance(result, dict)
    assert result == {
        "error": "Error updating security alert for de_f47e71ca: Update failed"
    }
