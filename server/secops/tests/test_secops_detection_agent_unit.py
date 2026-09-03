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
"""Unit tests for Detection Agent MCP tools."""

import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure server/secops is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

# Import the tools to test
from secops_mcp.tools.detection_agent import (
    evaluate_rule_coverage_long_running,
    generate_rules,
    generate_synthetic_events,
    generate_threat_detection_opportunity,
    get_operation,
)


@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    return client


@pytest.fixture
def mock_get_client(mock_chronicle_client):
    with patch(
        "secops_mcp.tools.detection_agent.get_chronicle_client",
        return_value=mock_chronicle_client,
    ):
        yield mock_chronicle_client


@pytest.mark.asyncio
async def test_generate_threat_detection_opportunity_success(mock_get_client):
    """Test generating a threat detection opportunity successfully."""
    expected_response = {
        "threat_detection_opportunities": [
            {
                "id": "tdo-123",
                "summary": "Lateral movement via WinRM",
                "supporting_evidence": ["powershell execution"],
                "log_types": ["WINEVTLOG"],
            }
        ]
    }

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        result = await generate_threat_detection_opportunity(
            threat="Lateral movement via WinRM",
            project_id="test-proj",
            customer_id="test-cust",
            region="us",
        )

        assert result == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":generateThreatDetectionOpportunity",
            api_version="v1alpha",
            json={"threat": "Lateral movement via WinRM"},
            timeout=300,
            error_message="Failed to generate threat detection opportunity",
        )


@pytest.mark.asyncio
async def test_generate_threat_detection_opportunity_alias_and_validation(
    mock_get_client,
):
    """Test alias support (threat_text) and validation on empty input."""
    expected_response = {"threat_detection_opportunities": [{"id": "tdo-456"}]}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        # Test threat_text alias
        result = await generate_threat_detection_opportunity(
            threat_text="Ransomware deployment",
        )
        assert result == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":generateThreatDetectionOpportunity",
            api_version="v1alpha",
            json={"threat": "Ransomware deployment"},
            timeout=300,
            error_message="Failed to generate threat detection opportunity",
        )

    # Test empty input validation
    result_empty = await generate_threat_detection_opportunity(threat="")
    assert "error" in result_empty
    assert "threat" in result_empty["error"].lower()


@pytest.mark.asyncio
async def test_generate_synthetic_events_success(mock_get_client):
    """Test generating synthetic events successfully."""
    tdo = {
        "id": "tdo-123",
        "summary": "Lateral movement via WinRM",
        "log_types": ["WINEVTLOG"],
    }
    expected_response = {
        "synthetic_events": [
            {
                "raw_log": "dGVzdF9sb2c=",
                "udm_json": '{"metadata": {"event_type": "PROCESS_LAUNCH"}}',
                "feedback_id": "fb-123",
            }
        ]
    }

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        result = await generate_synthetic_events(
            threat_detection_opportunity=tdo,
            project_id="test-proj",
            customer_id="test-cust",
            region="us",
        )

        assert result == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":generateSyntheticEvents",
            api_version="v1alpha",
            json={"threat_detection_opportunity": tdo},
            timeout=300,
            error_message="Failed to generate synthetic events",
        )


@pytest.mark.asyncio
async def test_generate_synthetic_events_aliases_and_json_string(
    mock_get_client,
):
    """Test camelCase alias threatDetectionOpportunity and JSON string input."""
    tdo = {
        "id": "tdo-123",
        "summary": "Lateral movement via WinRM",
        "log_types": ["WINEVTLOG"],
    }
    expected_response = {"synthetic_events": []}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        # Test camelCase alias with JSON string
        result = await generate_synthetic_events(
            threatDetectionOpportunity=json.dumps(tdo)
        )
        assert result == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":generateSyntheticEvents",
            api_version="v1alpha",
            json={"threat_detection_opportunity": tdo},
            timeout=300,
            error_message="Failed to generate synthetic events",
        )


@pytest.mark.asyncio
async def test_generate_synthetic_events_validation(mock_get_client):
    """Test validations for missing TDO and missing/empty log_types."""
    # Missing TDO
    res1 = await generate_synthetic_events()
    assert "error" in res1

    # Missing log_types in TDO
    res2 = await generate_synthetic_events(threat_detection_opportunity={"id": "tdo-1"})
    assert "error" in res2
    assert "log_types" in res2["error"]

    # Empty log_types in TDO
    res3 = await generate_synthetic_events(
        threat_detection_opportunity={"id": "tdo-1", "log_types": []}
    )
    assert "error" in res3
    assert "log_types" in res3["error"]


@pytest.mark.asyncio
async def test_api_error_handling(mock_get_client):
    """Test error handling when API request fails."""
    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        side_effect=Exception("API connection timeout"),
    ):
        res1 = await generate_threat_detection_opportunity(threat="sample threat")
        assert "error" in res1
        assert "API connection timeout" in res1["error"]

        res2 = await generate_synthetic_events(
            threat_detection_opportunity={"log_types": ["EDR"]}
        )
        assert "error" in res2
        assert "API connection timeout" in res2["error"]


@pytest.mark.asyncio
async def test_evaluate_rule_coverage_long_running_success(mock_get_client):
    """Test evaluate_rule_coverage_long_running successfully initiates LRO."""
    events = [
        {
            "threat_detection_opportunity_id": "tdo-123",
            "udms_json": ['{"metadata": {"event_type": "PROCESS_LAUNCH"}}'],
        }
    ]
    expected_op = {
        "name": "projects/p/locations/l/instances/i/operations/dea-12345",
        "done": False,
    }

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_op,
    ) as mock_request:
        result = await evaluate_rule_coverage_long_running(
            threat_detection_opportunity_events=events,
            exclude_composite_coverage=True,
            project_id="test-proj",
            customer_id="test-cust",
            region="us",
        )
        assert result == expected_op
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":evaluateRuleCoverageLongRunning",
            api_version="v1alpha",
            json={
                "threat_detection_opportunity_events": events,
                "exclude_composite_coverage": True,
            },
            timeout=300,
            error_message="Failed to evaluate rule coverage",
        )


@pytest.mark.asyncio
async def test_evaluate_rule_coverage_long_running_validation_and_aliases(
    mock_get_client,
):
    """Test alias support and input normalization for coverage evaluation."""
    # Missing input
    res1 = await evaluate_rule_coverage_long_running()
    assert "error" in res1

    # Single dict input with camelCase alias
    expected_op = {"name": "op-1", "done": False}
    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_op,
    ) as mock_request:
        res2 = await evaluate_rule_coverage_long_running(
            threatDetectionOpportunityEvents={
                "threatDetectionOpportunityId": "tdo-999",
                "udmsJson": ['{"e": 1}'],
            },
            excludeCompositeCoverage=False,
        )
        assert res2 == expected_op
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":evaluateRuleCoverageLongRunning",
            api_version="v1alpha",
            json={
                "threat_detection_opportunity_events": [
                    {
                        "threat_detection_opportunity_id": "tdo-999",
                        "udms_json": ['{"e": 1}'],
                    }
                ],
                "exclude_composite_coverage": False,
            },
            timeout=300,
            error_message="Failed to evaluate rule coverage",
        )


@pytest.mark.asyncio
async def test_get_operation_success(mock_get_client):
    """Test get_operation successfully polls an LRO."""
    expected_response = {
        "name": "projects/p/locations/l/instances/i/operations/dea-12345",
        "done": True,
        "response": {"coverage_results": [{"matched_rule": "rule-1"}]},
    }

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        result = await get_operation(
            name="projects/p/locations/l/instances/i/operations/dea-12345"
        )
        assert result == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="GET",
            endpoint_path="operations/dea-12345",
            api_version="v1alpha",
            timeout=60,
            error_message="Failed to get operation status",
        )


@pytest.mark.asyncio
async def test_get_operation_empty_name(mock_get_client):
    """Test get_operation validates empty name."""
    res = await get_operation(name="")
    assert "error" in res


@pytest.mark.asyncio
async def test_generate_rules_success(mock_get_client):
    """Test generate_rules successfully creates YARA-L rules from TDO."""
    tdo = {
        "id": "tdo-123",
        "summary": "Lateral movement via WinRM",
        "log_types": ["WINEVTLOG"],
    }
    expected_response = {
        "instance": "projects/p/locations/l/instances/i",
        "generated_rules": [
            {
                "rule_text": "rule winrm_lateral_movement { ... }",
                "feedback_id": "fb-001",
            }
        ],
    }

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        result = await generate_rules(
            threat_detection_opportunity=tdo,
            project_id="test-proj",
            customer_id="test-cust",
            region="us",
        )
        assert result == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":generateRules",
            api_version="v1alpha",
            json={"threat_detection_opportunity": tdo},
            timeout=300,
            error_message="Failed to generate rules",
        )


@pytest.mark.asyncio
async def test_generate_rules_validation_and_aliases(mock_get_client):
    """Test generate_rules validation and camelCase alias."""
    # Missing TDO
    res1 = await generate_rules()
    assert "error" in res1

    # JSON string input with alias
    tdo = {"id": "tdo-1"}
    expected_response = {"generated_rules": []}
    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        res2 = await generate_rules(threatDetectionOpportunity=json.dumps(tdo))
        assert res2 == expected_response
        mock_request.assert_called_once_with(
            mock_get_client,
            method="POST",
            endpoint_path=":generateRules",
            api_version="v1alpha",
            json={"threat_detection_opportunity": tdo},
            timeout=300,
            error_message="Failed to generate rules",
        )
