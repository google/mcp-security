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
from secops_mcp.tools.security_rules import get_rule


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

        # Test threat_description and log_types aliases
        result2 = await generate_threat_detection_opportunity(
            threat_description="WinRM execution",
            log_types=["WINEVTLOG"],
        )
        assert result2 == expected_response
        assert mock_request.call_args.kwargs["json"] == {
            "threat": "WinRM execution",
            "log_types": ["WINEVTLOG"],
        }

        # Test camelCase threatDescription and logTypes
        result3 = await generate_threat_detection_opportunity(
            threatDescription="C2 Beaconing",
            logTypes=["NETWORK"],
        )
        assert result3 == expected_response
        assert mock_request.call_args.kwargs["json"] == {
            "threat": "C2 Beaconing",
            "log_types": ["NETWORK"],
        }

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
async def test_generate_synthetic_events_multi_tdo_batching(mock_get_client):
    """Test generating synthetic events with multiple TDOs batches API calls."""
    tdo1 = {"id": "tdo-1", "log_types": ["WINEVTLOG"]}
    tdo2 = {"id": "tdo-2", "log_types": ["PROCESS"]}
    resp1 = {
        "synthetic_events": [{"feedback_id": "fb-1"}],
        "threat_detection_opportunity_events": [{"threat_detection_opportunity_id": "tdo-1"}],
    }
    resp2 = {
        "synthetic_events": [{"feedback_id": "fb-2"}],
        "threat_detection_opportunity_events": [{"threat_detection_opportunity_id": "tdo-2"}],
    }

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        side_effect=[resp1, resp2],
    ) as mock_request:
        result = await generate_synthetic_events(
            threat_detection_opportunities=[tdo1, tdo2]
        )
        assert result == {
            "synthetic_events": [{"feedback_id": "fb-1"}, {"feedback_id": "fb-2"}],
            "threat_detection_opportunity_events": [
                {"threat_detection_opportunity_id": "tdo-1"},
                {"threat_detection_opportunity_id": "tdo-2"},
            ],
        }
        assert mock_request.call_count == 2


@pytest.mark.asyncio
async def test_generate_synthetic_events_wrapped_dict(mock_get_client):
    """Test unwrapping raw output dictionary from generate_threat_detection_opportunity."""
    tdo = {"id": "tdo-1", "log_types": ["WINEVTLOG"]}
    wrapped_input = {"threat_detection_opportunities": [tdo]}
    expected_response = {"synthetic_events": [{"feedback_id": "fb-1"}]}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        result = await generate_synthetic_events(tdo=wrapped_input)
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
async def test_evaluate_rule_coverage_aliases_and_wrapped_dict(mock_get_client):
    """Test tdo_events alias and unwrapping raw dictionary."""
    events = [
        {
            "threat_detection_opportunity_id": "tdo-1",
            "udms_json": ['{"e": 1}'],
        }
    ]
    expected_op = {"name": "op-wrapped", "done": False}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_op,
    ) as mock_request:
        # Test tdo_events with wrapped dict {"threat_detection_opportunity_events": events}
        result = await evaluate_rule_coverage_long_running(
            tdo_events={"threat_detection_opportunity_events": events}
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
async def test_get_operation_name_aliases_and_normalization(mock_get_client):
    """Test operation_name alias and endpoint normalization."""
    expected_response = {"name": "op-test", "done": True}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        # Test operation_name with 'operations/dea-999'
        res1 = await get_operation(operation_name="operations/dea-999")
        assert res1 == expected_response
        mock_request.assert_called_with(
            mock_get_client,
            method="GET",
            endpoint_path="operations/dea-999",
            api_version="v1alpha",
            timeout=60,
            error_message="Failed to get operation status",
        )

        # Test bare id 'dea-888' auto-prefixed to 'operations/dea-888'
        res2 = await get_operation(operationName="dea-888")
        assert res2 == expected_response
        mock_request.assert_called_with(
            mock_get_client,
            method="GET",
            endpoint_path="operations/dea-888",
            api_version="v1alpha",
            timeout=60,
            error_message="Failed to get operation status",
        )


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


@pytest.mark.asyncio
async def test_generate_rules_multi_tdo_batching_and_context(mock_get_client):
    """Test multi-TDO batching and background_context support in generate_rules."""
    tdo1 = {"id": "tdo-1"}
    tdo2 = {"id": "tdo-2"}
    resp1 = {"generated_rules": [{"rule_text": "rule 1"}]}
    resp2 = {"generated_rules": [{"rule_text": "rule 2"}]}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        side_effect=[resp1, resp2],
    ) as mock_request:
        result = await generate_rules(
            threat_detection_opportunities=[tdo1, tdo2],
            background_context="Windows enterprise environment",
        )
        assert result == {
            "generated_rules": [{"rule_text": "rule 1"}, {"rule_text": "rule 2"}]
        }
        assert mock_request.call_count == 2
        first_call = mock_request.call_args_list[0]
        assert first_call.kwargs["json"] == {
            "threat_detection_opportunity": tdo1,
            "background_context": "Windows enterprise environment",
        }


@pytest.mark.asyncio
async def test_generate_rules_wrapped_dict(mock_get_client):
    """Test generate_rules with wrapped dictionary input."""
    tdo = {"id": "tdo-wrapped"}
    wrapped_input = {"threat_detection_opportunities": [tdo]}
    expected_response = {"generated_rules": [{"rule_text": "rule wrapped"}]}

    with patch(
        "secops_mcp.tools.detection_agent.chronicle_request",
        return_value=expected_response,
    ) as mock_request:
        result = await generate_rules(tdo=wrapped_input)
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
async def test_get_rule_alias():
    """Test get_rule alias delegates to get_detection_rule."""
    mock_client = MagicMock()
    mock_rule = {"ruleId": "ru_12345", "name": "Suspicious_Process"}
    mock_client.get_rule.return_value = mock_rule

    with patch(
        "secops_mcp.tools.security_rules.get_chronicle_client",
        return_value=mock_client,
    ):
        result = await get_rule(
            rule_id="ru_12345",
            project_id="p-1",
            customer_id="c-1",
            region="us",
        )
        assert result == mock_rule
        mock_client.get_rule.assert_called_once_with("ru_12345")
