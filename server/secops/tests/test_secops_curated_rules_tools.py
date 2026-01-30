"""Integration tests for Chronicle SecOps MCP curated rules tools.

These tests exercise the curated rules management functionality by making
actual API calls to the Chronicle service. They require proper
authentication and configuration to run.

To run these tests:
1. Create a config.json file in the tests directory with your Chronicle
   credentials (see conftest.py for format)
2. Authenticate with Google Cloud using ADC:
   gcloud auth application-default login
   OR set SECOPS_SA_PATH environment variable:
   export SECOPS_SA_PATH=/path/to/service-account.json
3. Run: pytest -xvs server/secops/tests/test_secops_curated_rules_tools.py
"""

from datetime import datetime, timedelta, timezone
from typing import Dict

import pytest

from secops_mcp.tools.curated_rules_management import (
    get_curated_rule,
    get_curated_rule_by_name,
    list_curated_rule_set_deployments,
    list_curated_rule_sets,
    list_curated_rules,
    get_curated_rule_set,
    search_curated_detections,
    update_curated_rule_set_deployment,
)


class TestCuratedRulesManagement:
    """Test class for Chronicle curated rules management tools."""

    @pytest.mark.asyncio
    async def test_list_curated_rules(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing curated rules.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_curated_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=10,
        )

        assert isinstance(result, dict)
        assert "curatedRules" in result

        if result.get("curatedRules"):
            assert isinstance(result["curatedRules"], list)
            first_rule = result["curatedRules"][0]
            assert isinstance(first_rule, dict)

    @pytest.mark.asyncio
    async def test_list_curated_rules_as_list(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing curated rules with as_list parameter.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_curated_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            as_list=True,
        )

        assert isinstance(result, dict)
        assert "curatedRules" in result
        assert isinstance(result["curatedRules"], list)

    @pytest.mark.asyncio
    async def test_get_curated_rule(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test retrieving a specific curated rule.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        list_result = await list_curated_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=1,
        )

        if not list_result.get("curatedRules"):
            pytest.skip("No curated rules available to test")

        rule_id = list_result["curatedRules"][0].get("name", "").split("/")[-1]

        result = await get_curated_rule(
            rule_id=rule_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        assert isinstance(result, dict)
        if "error" not in result:
            assert "name" in result or len(result) > 0

    @pytest.mark.asyncio
    async def test_get_curated_rule_by_name(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test finding a curated rule by display name.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        list_result = await list_curated_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=1,
        )

        if not list_result.get("curatedRules"):
            pytest.skip("No curated rules available to test")

        display_name = list_result["curatedRules"][0].get("displayName", "")

        if not display_name:
            pytest.skip("No display name available for testing")

        result = await get_curated_rule_by_name(
            display_name=display_name,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_search_curated_detections(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test searching detections from curated rules.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        list_result = await list_curated_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=1,
        )

        if not list_result.get("curatedRules"):
            pytest.skip("No curated rules available to test")

        rule_id = list_result["curatedRules"][0].get("name", "").split("/")[-1]

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=7)

        result = await search_curated_detections(
            rule_id=rule_id,
            start_time=start_time.isoformat().replace("+00:00", "Z"),
            end_time=end_time.isoformat().replace("+00:00", "Z"),
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=10,
        )

        assert isinstance(result, dict)
        if not result or "curatedDetections" not in result:
            pytest.skip(
                "No detections found for the rule in the time range"
            )
        assert isinstance(result["curatedDetections"], list)

    @pytest.mark.asyncio
    async def test_list_curated_rule_sets(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing curated rule sets.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_curated_rule_sets(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=10,
        )

        assert isinstance(result, dict)
        assert "curatedRuleSets" in result

        if result.get("curatedRuleSets"):
            assert isinstance(result["curatedRuleSets"], list)
            first_set = result["curatedRuleSets"][0]
            assert isinstance(first_set, dict)

    @pytest.mark.asyncio
    async def test_list_curated_rule_sets_as_list(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing curated rule sets with as_list parameter.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_curated_rule_sets(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            as_list=True,
        )

        assert isinstance(result, dict)
        assert "curatedRuleSets" in result
        assert isinstance(result["curatedRuleSets"], list)

    @pytest.mark.asyncio
    async def test_get_curated_rule_set(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test retrieving a specific curated rule set.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        list_result = await list_curated_rule_sets(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=1,
        )

        if not list_result.get("curatedRuleSets"):
            pytest.skip("No curated rule sets available to test")

        rule_set_id = (
            list_result["curatedRuleSets"][0].get("name", "").split("/")[-1]
        )

        result = await get_curated_rule_set(
            rule_set_id=rule_set_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        assert isinstance(result, dict)
        if "error" not in result:
            assert "name" in result or len(result) > 0

    @pytest.mark.asyncio
    async def test_list_curated_rule_set_deployments(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing curated rule set deployments.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_curated_rule_set_deployments(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=10,
        )

        assert isinstance(result, dict)
        assert "curatedRuleSetDeployments" in result

        if result.get("curatedRuleSetDeployments"):
            assert isinstance(result["curatedRuleSetDeployments"], list)
            first_deployment = result["curatedRuleSetDeployments"][0]
            assert isinstance(first_deployment, dict)

    @pytest.mark.asyncio
    async def test_list_curated_rule_set_deployments_as_list(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing deployments with as_list parameter.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_curated_rule_set_deployments(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            as_list=True,
        )

        assert isinstance(result, dict)
        assert "curatedRuleSetDeployments" in result
        assert isinstance(result["curatedRuleSetDeployments"], list)

    @pytest.mark.asyncio
    async def test_update_curated_rule_set_deployment(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test updating curated rule set deployment configuration.

        This test captures the original deployment state, updates to
        opposite values to verify the change works, then restores the
        original state.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        rule_sets_result = await list_curated_rule_sets(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            page_size=1,
        )

        if not rule_sets_result.get("curatedRuleSets"):
            pytest.skip("No curated rule sets available")

        first_rule_set = rule_sets_result["curatedRuleSets"][0]
        rule_set_name = first_rule_set.get("name", "")
        name_parts = rule_set_name.split("/")

        try:
            category_index = name_parts.index("curatedRuleSetCategories")
            category_id = name_parts[category_index + 1]
            rule_set_id = name_parts[-1]
        except (ValueError, IndexError):
            pytest.skip(
                "Unable to extract category_id or rule_set_id " "from name"
            )

        deployment_found = False
        original_precision = None
        original_enabled = None
        original_alerting = None

        for precision in ["precise", "broad"]:
            deployments = await list_curated_rule_set_deployments(
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            for deployment in deployments.get("curatedRuleSetDeployments", []):
                if rule_set_id in deployment.get(
                    "name", ""
                ) and precision in deployment.get("name", ""):
                    original_enabled = deployment.get("enabled", False)
                    original_alerting = deployment.get("alerting", False)
                    original_precision = precision
                    deployment_found = True
                    break

            if deployment_found:
                break

        if not deployment_found or original_enabled is None:
            pytest.skip(f"No deployment found for rule set {rule_set_id}")

        try:
            result = await update_curated_rule_set_deployment(
                category_id=category_id,
                rule_set_id=rule_set_id,
                precision=original_precision,
                enabled=not original_enabled,
                alerting=not original_alerting,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(result, dict)
            if "error" not in result:
                assert "name" in result or len(result) > 0

            verify_result = await list_curated_rule_set_deployments(
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            for deployment in verify_result.get(
                "curatedRuleSetDeployments", []
            ):
                if rule_set_id in deployment.get(
                    "name", ""
                ) and original_precision in deployment.get("name", ""):
                    if "enabled" in deployment:
                        assert deployment.get("enabled") == (
                            not original_enabled
                        )
                    if "alerting" in deployment:
                        assert deployment.get("alerting") == (
                            not original_alerting
                        )
                    break

        finally:
            await update_curated_rule_set_deployment(
                category_id=category_id,
                rule_set_id=rule_set_id,
                precision=original_precision,
                enabled=original_enabled,
                alerting=original_alerting,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

    @pytest.mark.asyncio
    async def test_update_curated_rule_set_deployment_invalid_precision(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test update with invalid precision value.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await update_curated_rule_set_deployment(
            category_id="test-category",
            rule_set_id="test-rule-set",
            precision="invalid",
            enabled=True,
            alerting=False,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "Invalid precision value" in result["error"]
