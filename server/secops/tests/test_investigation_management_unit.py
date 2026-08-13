"""Unit tests for investigation_management tools - stdout cleanliness verification.

These tests verify that investigation management tools do not pollute stdout,
which is critical for MCP protocol communication.
"""

from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from secops_mcp.tools.investigation_management import (
    list_investigations,
    get_investigation,
    trigger_investigation,
    fetch_associated_investigations,
)


class TestInvestigationManagementStdoutCleanliness:
    """Test that investigation tools do not pollute stdout."""

    @pytest.mark.asyncio
    async def test_list_investigations_success_no_stdout(self, capsys) -> None:
        """Verify list_investigations does not print to stdout on success."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.list_investigations = MagicMock(
                return_value={
                    "investigations": [
                        {
                            "name": "investigations/test123",
                            "displayName": "Test Investigation",
                            "status": "CLOSED",
                        }
                    ],
                    "next_page_token": None,
                }
            )
            mock_get_client.return_value = mock_chronicle

            result = await list_investigations(page_size=10)

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"list_investigations printed to stdout: {captured.out}"
            assert isinstance(result, dict)
            assert "investigations" in result

    @pytest.mark.asyncio
    async def test_list_investigations_error_no_stdout(self, capsys) -> None:
        """Verify list_investigations does not print to stdout on error."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.list_investigations = MagicMock(
                side_effect=Exception("Test error")
            )
            mock_get_client.return_value = mock_chronicle

            result = await list_investigations(page_size=10)

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"list_investigations printed to stdout on error: {captured.out}"
            assert "error" in result

    @pytest.mark.asyncio
    async def test_get_investigation_success_no_stdout(self, capsys) -> None:
        """Verify get_investigation does not print to stdout on success."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.get_investigation = MagicMock(
                return_value={
                    "name": "investigations/test123",
                    "displayName": "Test Investigation",
                    "status": "CLOSED",
                    "verdict": "BENIGN",
                }
            )
            mock_get_client.return_value = mock_chronicle

            result = await get_investigation(investigation_id="test123")

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"get_investigation printed to stdout: {captured.out}"
            assert isinstance(result, dict)
            assert "name" in result

    @pytest.mark.asyncio
    async def test_get_investigation_error_no_stdout(self, capsys) -> None:
        """Verify get_investigation does not print to stdout on error."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.get_investigation = MagicMock(
                side_effect=Exception("Test error")
            )
            mock_get_client.return_value = mock_chronicle

            result = await get_investigation(investigation_id="test123")

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"get_investigation printed to stdout on error: {captured.out}"
            assert "error" in result

    @pytest.mark.asyncio
    async def test_trigger_investigation_success_no_stdout(self, capsys) -> None:
        """Verify trigger_investigation does not print to stdout on success."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.trigger_investigation = MagicMock(
                return_value={
                    "name": "investigations/test123",
                    "displayName": "Triggered Investigation",
                    "status": "OPEN",
                    "triggerType": "MANUAL",
                    "createTime": "2026-08-13T10:00:00Z",
                }
            )
            mock_get_client.return_value = mock_chronicle

            result = await trigger_investigation(alert_id="alert123")

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"trigger_investigation printed to stdout: {captured.out}"
            assert isinstance(result, dict)
            assert "investigation" in result

    @pytest.mark.asyncio
    async def test_trigger_investigation_error_no_stdout(self, capsys) -> None:
        """Verify trigger_investigation does not print to stdout on error."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.trigger_investigation = MagicMock(
                side_effect=Exception("Test error")
            )
            mock_get_client.return_value = mock_chronicle

            result = await trigger_investigation(alert_id="alert123")

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"trigger_investigation printed to stdout on error: {captured.out}"
            assert "error" in result

    @pytest.mark.asyncio
    async def test_fetch_associated_investigations_success_no_stdout(
        self, capsys
    ) -> None:
        """Verify fetch_associated_investigations does not print to stdout on success."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.fetch_associated_investigations = MagicMock(
                return_value={
                    "associationsList": {
                        "alerts/alert123": {
                            "investigations": [
                                {
                                    "name": "investigations/inv123",
                                    "displayName": "Investigation 1",
                                    "verdict": "BENIGN",
                                    "confidence": 0.8,
                                    "status": "CLOSED",
                                }
                            ]
                        }
                    }
                }
            )
            mock_get_client.return_value = mock_chronicle

            result = await fetch_associated_investigations(
                detection_type="ALERT", alert_ids=["alert123"]
            )

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"fetch_associated_investigations printed to stdout: {captured.out}"
            assert isinstance(result, dict)
            assert "associations" in result

    @pytest.mark.asyncio
    async def test_fetch_associated_investigations_error_no_stdout(
        self, capsys
    ) -> None:
        """Verify fetch_associated_investigations does not print to stdout on error."""
        with patch(
            "secops_mcp.tools.investigation_management.get_chronicle_client"
        ) as mock_get_client:
            mock_chronicle = MagicMock()
            mock_chronicle.fetch_associated_investigations = MagicMock(
                side_effect=Exception("Test error")
            )
            mock_get_client.return_value = mock_chronicle

            result = await fetch_associated_investigations(
                detection_type="ALERT", alert_ids=["alert123"]
            )

            captured = capsys.readouterr()
            assert (
                captured.out == ""
            ), f"fetch_associated_investigations printed to stdout on error: {captured.out}"
            assert "error" in result
