"""Integration tests for Chronicle SecOps Investigation Management tools.

These tests exercise the investigation management functionality including
cases, investigations, and their associations. They require proper
authentication and configuration to run.

To run these tests:
1. Make sure you have created a config.json file in the tests directory
   with your Chronicle credentials (see conftest.py for format)
2. Authenticate with Google Cloud using ADC:
   gcloud auth application-default login
3. Run: pytest -xvs server/secops/tests/test_secops_investigations_mcp.py
"""

from datetime import datetime, timedelta, timezone
from typing import Dict

import pytest

from secops_mcp.tools.investigation_management import (
    fetch_associated_investigations,
    get_investigation,
    list_investigations,
    trigger_investigation,
)


class TestChronicleInvestigationsMCP:
    """Test class for Chronicle Investigation Management MCP tools."""

    @pytest.mark.asyncio
    async def test_list_investigations(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing investigations.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_investigations(
            page_size=10,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        assert isinstance(result, dict)

        if "error" not in result:
            assert "investigations" in result
            assert isinstance(result["investigations"], list)

    @pytest.mark.asyncio
    async def test_get_investigation(
        self, chronicle_config: Dict[str, str], chronicle_client
    ) -> None:
        """Test getting a specific investigation.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
            chronicle_client: Chronicle client fixture
        """
        investigations_result = await list_investigations(
            page_size=1,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        if "investigations" in investigations_result:
            investigations = investigations_result["investigations"]
            if investigations:
                investigation_name = investigations[0].get("name")
                if investigation_name:
                    investigation_id = investigation_name.split("/")[-1]
                    result = await get_investigation(
                        investigation_id=investigation_id,
                        project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                        customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                        region=chronicle_config["CHRONICLE_REGION"],
                    )

                    assert isinstance(result, dict)
                    assert "error" not in result
                    assert "name" in result

    @pytest.mark.asyncio
    async def test_trigger_investigation(
        self, chronicle_config: Dict[str, str], chronicle_client
    ) -> None:
        """Test triggering investigation for a real alert.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
            chronicle_client: Chronicle client fixture
        """
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=30)

        alerts = chronicle_client.get_alerts(
            start_time=start_time,
            end_time=end_time,
            max_alerts=5,
        )

        alert_list = alerts.get("alerts", {}).get("alerts", [])

        if alert_list:
            alert_id = alert_list[0].get("name")
            if alert_id:
                result = await trigger_investigation(
                    alert_id=alert_id,
                    project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                    customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                    region=chronicle_config["CHRONICLE_REGION"],
                )

                assert isinstance(result, dict)
                if "error" not in result:
                    assert "investigation" in result
                    assert "alert_id" in result
                    assert result["alert_id"] == alert_id

    @pytest.mark.asyncio
    async def test_fetch_associated_investigations(
        self, chronicle_config: Dict[str, str], chronicle_client
    ) -> None:
        """Test fetching investigations associated with alerts.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
            chronicle_client: Chronicle client fixture
        """
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=30)

        alerts = chronicle_client.get_alerts(
            start_time=start_time,
            end_time=end_time,
            max_alerts=3,
        )

        alert_list = alerts.get("alerts", {}).get("alerts", [])
        alert_ids = [
            alert.get("name") for alert in alert_list if alert.get("name")
        ]

        if alert_ids:
            result = await fetch_associated_investigations(
                detection_type="ALERT",
                alert_ids=alert_ids,
                association_limit_per_detection=3,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(result, dict)
            if "error" not in result:
                assert "detection_type" in result
                assert "associations" in result
                assert isinstance(result["associations"], dict)
