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
"""Unit tests for Security Command Center (SCC) v2 MCP tools."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scc_mcp import (
    _build_or_filter,
    _build_parent,
    get_finding_details,
    get_finding_remediation,
    search_findings,
    search_findings_by_compliance,
    set_finding_mute,
    top_vulnerability_findings,
)


# ---------------------------------------------------------------------------
# Helper tests
# ---------------------------------------------------------------------------

def test_build_parent_project():
    """Verify _build_parent formats project-level v2 paths with location."""
    assert _build_parent(project_id="my-proj", location="global") == "projects/my-proj/sources/-/locations/global"
    assert _build_parent(project_id="my-proj", location="us-central1") == "projects/my-proj/sources/-/locations/us-central1"


def test_build_parent_org():
    """Verify _build_parent formats organization-level v2 paths."""
    assert _build_parent(organization_id="123456789", location="global") == "organizations/123456789/sources/-/locations/global"


def test_build_parent_missing():
    """Verify _build_parent raises ValueError if neither project nor org is given."""
    with pytest.raises(ValueError, match="Either project_id or organization_id must be provided"):
        _build_parent()


def test_build_or_filter_case_insensitivity():
    """Verify _build_or_filter splits correctly on lowercase, uppercase, and commas."""
    assert _build_or_filter("severity", "HIGH OR CRITICAL") == '(severity="HIGH" OR severity="CRITICAL")'
    assert _build_or_filter("severity", "high or critical") == '(severity="HIGH" OR severity="CRITICAL")'
    assert _build_or_filter("severity", "High or Critical") == '(severity="HIGH" OR severity="CRITICAL")'
    assert _build_or_filter("severity", "HIGH, CRITICAL") == '(severity="HIGH" OR severity="CRITICAL")'
    assert _build_or_filter("findingClass", "THREAT") == 'findingClass="THREAT"'
    assert _build_or_filter("findingClass", "") == ""


# ---------------------------------------------------------------------------
# Mock Finding Helper
# ---------------------------------------------------------------------------

def _create_mock_finding_result(
    finding_id="find-123",
    category="OPEN_FIREWALL",
    severity="HIGH",
    finding_class="VULNERABILITY",
    attack_score=0.85,
    resource_name="//compute.googleapis.com/projects/my-proj/zones/us-central1-a/instances/inst-1",
    compliances=None,
    next_steps="Close the port in firewall rules.",
):
    mock_item = MagicMock()
    finding_pb = MagicMock()

    finding_dict = {
        "name": f"projects/my-proj/sources/123/locations/global/findings/{finding_id}",
        "category": category,
        "severity": severity,
        "findingClass": finding_class,
        "resourceName": resource_name,
        "description": f"Test finding description for {category}",
        "nextSteps": next_steps,
        "attackExposure": {"score": attack_score},
        "compliances": compliances or [],
    }

    mock_item.finding._pb = finding_pb
    mock_item.finding.name = finding_dict["name"]

    return mock_item, finding_dict


# ---------------------------------------------------------------------------
# Tool unit tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_findings_success():
    """Verify search_findings executes list_findings and formats response."""
    mock_item, finding_dict = _create_mock_finding_result()

    with patch("scc_mcp.scc_client") as mock_scc, \
         patch("scc_mcp.proto_message_to_dict", return_value=finding_dict):

        mock_page = MagicMock()
        mock_page.list_findings_results = [mock_item]
        mock_page.next_page_token = ""
        mock_scc.list_findings.return_value.pages = [mock_page]

        result = await search_findings(
            project_id="my-proj",
            finding_class="VULNERABILITY",
            severity="high or critical",
            max_findings=10,
        )

        assert result["count"] == 1
        assert len(result["findings"]) == 1
        assert result["findings"][0]["category"] == "OPEN_FIREWALL"
        assert 'findingClass="VULNERABILITY"' in result["filter_applied"]
        assert 'severity="HIGH" OR severity="CRITICAL"' in result["filter_applied"]


@pytest.mark.asyncio
async def test_get_finding_details_success():
    """Verify get_finding_details retrieves finding and enriches from CAI."""
    mock_item, finding_dict = _create_mock_finding_result(finding_id="find-999")

    with patch("scc_mcp.scc_client") as mock_scc, \
         patch("scc_mcp.cai_client") as mock_cai, \
         patch("scc_mcp.proto_message_to_dict", side_effect=[finding_dict, {"asset": "details"}]):

        mock_page = MagicMock()
        mock_page.list_findings_results = [mock_item]
        mock_scc.list_findings.return_value.pages = [mock_page]

        mock_cai_asset = MagicMock()
        mock_cai.search_all_resources.return_value = [mock_cai_asset]

        result = await get_finding_details(
            project_id="my-proj",
            finding_id="find-999",
            include_resource_details=True,
        )

        assert "error" not in result
        assert result["finding_id"] == "find-999"
        assert result["finding"]["category"] == "OPEN_FIREWALL"
        assert result["resource_details_cai"] == {"asset": "details"}


@pytest.mark.asyncio
async def test_search_findings_by_compliance():
    """Verify search_findings_by_compliance filters by compliance benchmark and control ID."""
    mock_item, finding_dict = _create_mock_finding_result(
        compliances=[
            {"standard": "CIS Google Cloud Platform", "version": "1.3.0", "ids": ["1.5", "1.6"]}
        ]
    )

    with patch("scc_mcp.scc_client") as mock_scc, \
         patch("scc_mcp.proto_message_to_dict", return_value=finding_dict):

        mock_page = MagicMock()
        mock_page.list_findings_results = [mock_item]
        mock_scc.list_findings.return_value.pages = [mock_page]

        result = await search_findings_by_compliance(
            organization_id="123456789",
            compliance_standard="CIS",
            compliance_id="1.5",
        )

        assert result["count"] == 1
        assert len(result["findings"]) == 1
        assert result["findings"][0]["compliance_summary"][0]["standard"] == "CIS Google Cloud Platform"


@pytest.mark.asyncio
async def test_top_vulnerability_findings_sorts_by_attack_exposure():
    """Verify top_vulnerability_findings correctly sorts findings descending by Attack Exposure."""
    item1, dict1 = _create_mock_finding_result(finding_id="low-risk", attack_score=0.20)
    item2, dict2 = _create_mock_finding_result(finding_id="high-risk", attack_score=0.95)

    with patch("scc_mcp.scc_client") as mock_scc, \
         patch("scc_mcp.proto_message_to_dict", side_effect=[dict1, dict2]):

        mock_page = MagicMock()
        mock_page.list_findings_results = [item1, item2]
        mock_scc.list_findings.return_value.pages = [mock_page]

        result = await top_vulnerability_findings(project_id="my-proj", max_findings=2)

        assert result["count"] == 2
        # First item should be the highest attack exposure score
        assert result["top_findings"][0]["attackExposureScore"] == 0.95
        assert result["top_findings"][1]["attackExposureScore"] == 0.20
        assert result["top_findings"][0]["nextSteps"] == "Close the port in firewall rules."


@pytest.mark.asyncio
async def test_set_finding_mute_success():
    """Verify set_finding_mute resolves canonical finding name and updates mute state."""
    mock_item, finding_dict = _create_mock_finding_result(finding_id="mute-me")
    mock_updated = MagicMock()

    with patch("scc_mcp.scc_client") as mock_scc, \
         patch("scc_mcp.proto_message_to_dict", return_value={"muted": True}):

        mock_page = MagicMock()
        mock_page.list_findings_results = [mock_item]
        mock_scc.list_findings.return_value.pages = [mock_page]
        mock_scc.set_mute.return_value = mock_updated

        result = await set_finding_mute(
            project_id="my-proj",
            finding_id="mute-me",
            mute="MUTED",
        )

        assert result["success"] is True
        assert result["mute_state"] == "MUTED"
        assert "find-123" in result["finding_name"] or "mute-me" in result["finding_name"]


@pytest.mark.asyncio
async def test_get_finding_remediation_success():
    """Verify get_finding_remediation returns nextSteps and CAI details."""
    mock_item, finding_dict = _create_mock_finding_result(finding_id="rem-123")

    with patch("scc_mcp.scc_client") as mock_scc, \
         patch("scc_mcp.cai_client") as mock_cai, \
         patch("scc_mcp.proto_message_to_dict", side_effect=[finding_dict, {"cai": "info"}]):

        mock_page = MagicMock()
        mock_page.list_findings_results = [mock_item]
        mock_scc.list_findings.return_value.pages = [mock_page]

        mock_cai.search_all_resources.return_value = [MagicMock()]

        result = await get_finding_remediation(
            project_id="my-proj",
            finding_id="rem-123",
        )

        assert result["remediation_steps"] == "Close the port in firewall rules."
        assert result["resource_details_cai"] == {"cai": "info"}
