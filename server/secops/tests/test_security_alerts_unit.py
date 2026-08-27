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

from secops_mcp.tools.security_alerts import get_security_alerts


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
async def test_get_security_alerts_keeps_empty_feedback_summary_authoritative(
    chronicle_client,
):
    chronicle_client.get_alerts.return_value = [
        {
            "id": "de_2a5b279c",
            "ruleName": "Untriaged Rule",
            "status": "OPEN",
            "severity": "Medium",
            "feedbackSummary": {},
        }
    ]

    output = json.loads(
        await get_security_alerts(project_id="test", customer_id="test")
    )

    assert "Status: Unknown" in output
    assert "Verdict: Unknown" in output
    assert "Severity: Unknown" in output


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
