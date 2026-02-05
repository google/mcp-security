"""Integration tests for advanced security rules MCP tools.

These tests exercise the advanced rule operations including retrohunts
and rule alert searches by making actual API calls to Chronicle service.
They require proper authentication and configuration to run.

To run these tests:
1. Make sure you have created a config.json file in the tests directory
   with your Chronicle credentials (see conftest.py for format)
2. Authenticate with Google Cloud using ADC:
   gcloud auth application-default login
   OR set SECOPS_SA_PATH environment variable to use service account:
   export SECOPS_SA_PATH=/path/to/service-account.json
3. Run: pytest -xvs server/secops/tests/test_adv_rules_mcp.py
"""

from datetime import datetime, timedelta, timezone
from typing import Dict

import pytest

from secops_mcp.tools.security_rules import (
    create_retrohunt,
    get_retrohunt,
    list_security_rules,
    search_rule_alerts,
)


class TestAdvancedSecurityRulesMCP:
    """Test class for advanced security rules MCP tools."""

    @pytest.mark.asyncio
    async def test_retrohunt_end_to_end(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test complete retrohunt workflow: list rules, create, check.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # List rules to get a valid rule_id
        rules_response = await list_security_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=10,
        )

        # Verify rules response
        assert isinstance(rules_response, dict)
        assert "rules" in rules_response or "error" in rules_response

        # Check if we have rules to work with
        if "error" in rules_response:
            pytest.skip(f"Error listing rules: {rules_response['error']}")

        rules = rules_response.get("rules", [])
        if not rules or len(rules) == 0:
            pytest.skip("No rules available to test retrohunt")

        # Get first rule ID
        first_rule = rules[0]
        rule_id = first_rule.get("name", "").split("/")[-1]

        if not rule_id:
            pytest.skip("Could not extract rule_id from rules response")

        print(f"Using rule_id: {rule_id}")

        # Define time range for retrohunt
        # Use a range ending a few hours ago to avoid data availability issues
        now = datetime.now(timezone.utc)
        end_time = now - timedelta(hours=6)
        start_time = end_time - timedelta(days=1)

        # Format as ISO strings
        start_iso = start_time.isoformat()
        end_iso = end_time.isoformat()

        # Create retrohunt
        create_result = await create_retrohunt(
            rule_id=rule_id,
            start_time=start_iso,
            end_time=end_iso,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Verify create result is a dict
        assert isinstance(create_result, dict)
        assert "rule_id" in create_result
        assert "status" in create_result

        # Verify rule_id matches
        assert create_result["rule_id"] == rule_id

        # Check if creation was successful
        if create_result["status"] != "success":
            error_msg = create_result.get("error", "Unknown error")
            print(f"Error: {error_msg}")
            if "raw_response" in create_result:
                print(f"Raw response: {create_result['raw_response']}")
            pytest.skip(f"Retrohunt creation failed: {error_msg}")

        # Should have operation_id and operation_name on success
        assert "operation_id" in create_result
        assert "operation_name" in create_result
        assert isinstance(create_result["operation_id"], str)
        assert len(create_result["operation_id"]) > 0

        operation_id = create_result["operation_id"]

        # Get retrohunt status
        status_result = await get_retrohunt(
            rule_id=rule_id,
            operation_id=operation_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Verify status result is a dict
        assert isinstance(status_result, dict)

        # Should have expected keys
        assert "operation_id" in status_result
        assert "rule_id" in status_result
        assert "done" in status_result

        # done should be a boolean
        assert isinstance(status_result["done"], bool)

        # Verify operation_id and rule_id match
        assert status_result["operation_id"] == operation_id
        assert status_result["rule_id"] == rule_id

    @pytest.mark.asyncio
    async def test_search_rule_alerts(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test searching rule alerts.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Search for alerts in the last 24 hours
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=24)

        # Format as ISO strings
        start_iso = start_time.isoformat()
        end_iso = end_time.isoformat()

        result = await search_rule_alerts(
            start_time=start_iso,
            end_time=end_iso,
            max_alerts=10,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # This should return a dict
        assert isinstance(result, dict)

        # Should have ruleAlerts key or error key
        assert "ruleAlerts" in result or "error" in result

        # If ruleAlerts present, verify structure
        if "ruleAlerts" in result:
            rule_alerts = result["ruleAlerts"]
            assert isinstance(rule_alerts, list)

            # Should have tooManyAlerts flag
            assert "tooManyAlerts" in result
            assert isinstance(result["tooManyAlerts"], bool)

            # If alerts present, verify structure
            if len(rule_alerts) > 0:
                first_rule_alert = rule_alerts[0]
                assert isinstance(first_rule_alert, dict)

                # Should have ruleMetadata and alerts
                assert "ruleMetadata" in first_rule_alert
                assert "alerts" in first_rule_alert

                # Verify alerts is a list
                assert isinstance(first_rule_alert["alerts"], list)

    @pytest.mark.asyncio
    async def test_search_rule_alerts_with_max_alerts(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test searching rule alerts with custom max_alerts limit.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Search for alerts in the last 48 hours with small limit
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=48)

        # Format as ISO strings
        start_iso = start_time.isoformat()
        end_iso = end_time.isoformat()

        result = await search_rule_alerts(
            start_time=start_iso,
            end_time=end_iso,
            max_alerts=5,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # This should return a dict
        assert isinstance(result, dict)

        # Should have ruleAlerts key or error key
        assert "ruleAlerts" in result or "error" in result

        # Should have tooManyAlerts flag
        if "ruleAlerts" in result:
            assert "tooManyAlerts" in result
            assert isinstance(result["tooManyAlerts"], bool)
