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
"""Unit tests for the consolidated case management MCP tool suite."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

from secops.chronicle.client import APIVersion
from secops_mcp.tools.case_alert_management import (
    create_alert_recommendation_long_running,
    fetch_alert_recommendation,
    get_alert_overview,
    list_alert_views,
    pause_alert_sla,
    resolve_alert_overview_widget,
    resume_alert_sla,
    set_alert_sla,
)
from secops_mcp.tools.case_close_definitions import (
    create_case_close_definition,
    create_case_queue_filter,
    create_case_stage_definition,
    create_case_tag_definition,
    list_case_close_definitions,
    list_case_queue_filters,
    list_case_stage_definitions,
    list_case_tag_definitions,
)
from secops_mcp.tools.case_detections_and_events import (
    get_case_detection,
    get_case_event,
    get_case_evidence_data,
    list_case_detection_events,
    list_case_detections,
    list_case_events,
    list_case_evidence_data,
)
from secops_mcp.tools.case_management import (
    add_case_tag,
    batch_attach_case_evidence,
    batch_create_case_comments,
    batch_detach_case_evidence,
    batch_get_legacy_cases,
    count_case_priorities,
    create_case,
    create_manual_case,
    create_or_update_case,
    delete_case_comment,
    execute_bulk_add_tag,
    execute_bulk_assign_case,
    execute_bulk_change_priority,
    execute_bulk_change_stage,
    fetch_wiz_related_issues,
    generate_case_report,
    get_case_comment,
    get_case_overview,
    get_or_create_case_summary,
    merge_cases,
    pause_case_sla,
    query_case_views,
    remove_case_tag,
    resolve_case_overview_widget,
    resume_case_sla,
    update_case_comment,
)
from secops_mcp.tools.case_reporting_and_chat import (
    create_agentic_case_report,
    create_case_chat_message,
    export_agentic_case_report,
    list_agentic_case_report_templates,
    list_agentic_case_reports,
    list_case_chat_messages,
)
from secops_mcp.tools.case_wall_records import (
    add_case_wall_record_tags,
    fetch_case_activities_count,
    get_case_wall_record,
    list_case_wall_records,
    query_available_case_wall_record_tags,
    remove_case_wall_record_tags,
    set_favourite_wall_record,
)


@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    client.base_v1alpha_url = "https://us-chronicle.googleapis.com/v1alpha"
    client.instance_id = "projects/proj-123/locations/us/instances/cust-456"
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = '{"status": "OK"}'
    mock_resp.json.return_value = {"status": "OK"}
    client.session.get.return_value = mock_resp
    client.session.post.return_value = mock_resp
    client.session.patch.return_value = mock_resp
    client.session.delete.return_value = mock_resp
    return client


@pytest.mark.asyncio
async def test_create_case_success(mock_chronicle_client):
    """Test successful case package creation via create_case."""
    case_payload = {"cases": [{"id": "c1", "title": "Test Case"}]}
    expected_response = {"status": "SUCCESS"}

    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ) as mock_get_client,
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            return_value=expected_response,
        ) as mock_request,
    ):
        result = await create_case(
            case_data=case_payload,
            project_id="proj-123",
            customer_id="cust-456",
            region="us",
        )

        mock_get_client.assert_called_once_with("proj-123", "cust-456", "us")
        mock_request.assert_called_once_with(
            mock_chronicle_client,
            method="POST",
            endpoint_path="legacyCases:createCase",
            api_version=APIVersion.V1ALPHA,
            json=case_payload,
            error_message="Failed to create case package",
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_create_case_empty_payload():
    """Test create_case with empty payload."""
    result = await create_case(case_data={})
    assert result == {"error": "case_data parameter is required and cannot be empty"}


@pytest.mark.asyncio
async def test_create_manual_case_success(mock_chronicle_client):
    """Test successful manual case creation via create_manual_case."""
    case_payload = {
        "title": "Manual Case",
        "priority": "HIGH",
        "tags": ["suspicious"],
    }
    expected_response = {"name": "cases/m123"}

    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ) as mock_get_client,
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            return_value=expected_response,
        ) as mock_request,
    ):
        result = await create_manual_case(
            case_data=case_payload,
            project_id="proj-123",
            customer_id="cust-456",
            region="us",
        )

        mock_get_client.assert_called_once_with("proj-123", "cust-456", "us")
        mock_request.assert_called_once_with(
            mock_chronicle_client,
            method="POST",
            endpoint_path="legacyCases:createManualCase",
            api_version=APIVersion.V1ALPHA,
            json=case_payload,
            error_message="Failed to create manual case",
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_create_or_update_case_success(mock_chronicle_client):
    """Test successful case upsert via create_or_update_case."""
    case_payload = {"caseId": "c123", "summary": "Updated summary"}
    expected_response = {"caseId": "c123", "status": "OPEN"}

    with (
        patch(
            "secops_mcp.tools.case_management.get_chronicle_client",
            return_value=mock_chronicle_client,
        ) as mock_get_client,
        patch(
            "secops_mcp.tools.case_management.chronicle_request",
            return_value=expected_response,
        ) as mock_request,
    ):
        result = await create_or_update_case(
            case_data=case_payload,
            project_id="proj-123",
            customer_id="cust-456",
            region="us",
        )

        mock_get_client.assert_called_once_with("proj-123", "cust-456", "us")
        mock_request.assert_called_once_with(
            mock_chronicle_client,
            method="POST",
            endpoint_path="legacy:legacyCreateOrUpdateCase",
            api_version=APIVersion.V1ALPHA,
            json=case_payload,
            error_message="Failed to create or update case",
        )
        assert result == expected_response


@pytest.mark.asyncio
async def test_consolidated_case_services(mock_chronicle_client):
    """Verify consolidated CaseService, LegacyCaseService, WallRecord, Detection, Reporting, and Definition tools."""
    with (
        patch("secops_mcp.tools.case_management.get_chronicle_client", return_value=mock_chronicle_client),
        patch("secops_mcp.tools.case_alert_management.get_chronicle_client", return_value=mock_chronicle_client),
        patch("secops_mcp.tools.case_wall_records.get_chronicle_client", return_value=mock_chronicle_client),
        patch("secops_mcp.tools.case_detections_and_events.get_chronicle_client", return_value=mock_chronicle_client),
        patch("secops_mcp.tools.case_reporting_and_chat.get_chronicle_client", return_value=mock_chronicle_client),
        patch("secops_mcp.tools.case_close_definitions.get_chronicle_client", return_value=mock_chronicle_client),
    ):
        assert (await add_case_tag("101", ["phishing"])) == {"status": "OK"}
        assert (await remove_case_tag("101", ["phishing"])) == {"status": "OK"}
        assert (await pause_case_sla("101", "Waiting on customer"))["status"] == "SUCCESS"
        assert (await resume_case_sla("101"))["status"] == "SUCCESS"
        assert (await get_case_overview("101")) == {"status": "OK"}
        assert (await resolve_case_overview_widget("101")) == {"status": "OK"}
        assert (await query_case_views("101")) == {"status": "OK"}
        assert (await count_case_priorities()) == {"status": "OK"}
        assert (await get_or_create_case_summary("101")) == {"status": "OK"}
        assert (await merge_cases(["101", "102"], "101")) == {"status": "OK"}
        assert (await generate_case_report({"caseId": "101"})) == {"status": "OK"}
        assert (await batch_attach_case_evidence("101", {"items": []})) == {"status": "OK"}
        assert (await batch_detach_case_evidence("101", {"items": []})) == {"status": "OK"}
        assert (await execute_bulk_assign_case([101], "analyst@example.com")) == {"status": "OK"}
        assert (await execute_bulk_change_priority([101], "CRITICAL")) == {"status": "OK"}
        assert (await execute_bulk_change_stage([101], "Investigation")) == {"status": "OK"}
        assert (await execute_bulk_add_tag([101], ["tag1"])) == {"status": "OK"}
        assert (await fetch_wiz_related_issues("101")) == {"status": "OK"}
        assert (await get_case_comment("101", "cmt-1")) == {"status": "OK"}
        assert (await update_case_comment("101", "cmt-1", "Updated text")) == {"status": "OK"}
        assert (await delete_case_comment("101", "cmt-1")) == {"status": "SUCCESS", "deleted_comment_id": "cmt-1"}
        assert (await batch_create_case_comments("101", ["Note 1", "Note 2"])) == {"status": "OK"}

        # CaseAlertService
        assert (await set_alert_sla("101", "a1", "2026-10-01T00:00:00Z")) == {"status": "OK"}
        assert (await pause_alert_sla("101", "a1")) == {"status": "OK"}
        assert (await resume_alert_sla("101", "a1")) == {"status": "OK"}
        assert (await get_alert_overview("101", "a1")) == {"status": "OK"}
        assert (await resolve_alert_overview_widget("101", "a1", {"id": "w1"})) == {"status": "OK"}
        assert (await fetch_alert_recommendation("101", "a1")) == {"status": "OK"}
        assert (await create_alert_recommendation_long_running("101", "a1")) == {"status": "OK"}
        assert (await list_alert_views("101", "a1")) == {"status": "OK"}

        # CaseWallRecordService
        assert (await list_case_wall_records("101")) == {"status": "OK"}
        assert (await get_case_wall_record("101", "wr-1")) == {"status": "OK"}
        assert (await set_favourite_wall_record("101", "wr-1", True)) == {"status": "OK"}
        assert (await add_case_wall_record_tags("101", "wr-1", ["t1"])) == {"status": "OK"}
        assert (await remove_case_wall_record_tags("101", "wr-1", ["t1"])) == {"status": "OK"}
        assert (await fetch_case_activities_count("101")) == {"status": "OK"}
        assert (await query_available_case_wall_record_tags("101")) == {"status": "OK"}

        # CaseDetection, CaseEvent, CaseEvidenceData
        assert (await list_case_detections("101")) == {"status": "OK"}
        assert (await get_case_detection("101", "d1")) == {"status": "OK"}
        assert (await list_case_detection_events("101", "d1")) == {"status": "OK"}
        assert (await list_case_events("101")) == {"status": "OK"}
        assert (await get_case_event("101", "e1")) == {"status": "OK"}
        assert (await list_case_evidence_data("101")) == {"status": "OK"}
        assert (await get_case_evidence_data("101", "ev1")) == {"status": "OK"}

        # AgenticCaseReporting & CaseChatMessage
        assert (await create_agentic_case_report("101", {"title": "Report"})) == {"status": "OK"}
        assert (await list_agentic_case_reports("101")) == {"status": "OK"}
        assert (await list_agentic_case_report_templates()) == {"status": "OK"}
        assert (await export_agentic_case_report("101", "r1")) == {"status": "OK"}
        assert (await create_case_chat_message("101", {"content": "Hello"})) == {"status": "OK"}
        assert (await list_case_chat_messages("101")) == {"status": "OK"}

        # Definitions & Queue Filters
        assert (await create_case_close_definition("MALICIOUS", "Ransomware")) == {"status": "OK"}
        assert (await list_case_stage_definitions()) == {"status": "OK"}
        assert (await create_case_stage_definition({"displayName": "Containment"})) == {"status": "OK"}
        assert (await list_case_tag_definitions()) == {"status": "OK"}
        assert (await create_case_tag_definition({"tag": "apt"})) == {"status": "OK"}
        assert (await list_case_queue_filters()) == {"status": "OK"}
        assert (await create_case_queue_filter({"displayName": "My Open High Priority"})) == {"status": "OK"}
