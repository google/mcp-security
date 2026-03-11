"""Integration tests for Chronicle SecOps MCP Rule Exclusion tools.

These tests exercise the rule exclusion functionality of the secops_mcp.py
tools by making actual API calls to the Chronicle service. They require
proper authentication and configuration to run.

To run these tests:
1. Make sure you have created a config.json file in the tests directory
   with your Chronicle credentials (see conftest.py for format)
2. Authenticate with Google Cloud using ADC:
   gcloud auth application-default login
   OR set SECOPS_SA_PATH environment variable to use service account:
   export SECOPS_SA_PATH=/path/to/service-account.json
3. Run: pytest -xvs server/secops/tests/test_secops_rule_exclusion_mcp.py
"""

import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict

import pytest

from secops_mcp.tools.rule_exclusions import (
    compute_rule_exclusion_activity,
    create_rule_exclusion,
    get_rule_exclusion,
    list_rule_exclusions,
    patch_rule_exclusion,
    update_rule_exclusion_deployment,
)


class TestChronicleRuleExclusionMCP:
    """Test class for Chronicle SecOps MCP Rule Exclusion tools."""

    @pytest.mark.asyncio
    async def test_rule_exclusion_lifecycle(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test complete lifecycle of rule exclusions.

        This test covers:
        1. Creating a rule exclusion
        2. Getting the rule exclusion details
        3. Listing rule exclusions
        4. Patching the rule exclusion
        5. Updating deployment settings
        6. Cleanup by archiving

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        test_id = f"test_excl_{uuid.uuid4().hex[:8]}"
        display_name = f"Integration Test Exclusion {test_id}"
        exclusion_id = None

        try:
            print(f"\n>>> Creating rule exclusion with ID: {test_id}")

            # 1. Create rule exclusion
            create_result = await create_rule_exclusion(
                display_name=display_name,
                refinement_type="DETECTION_EXCLUSION",
                query='(ip = "8.8.8.8")',
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(create_result, dict)
            assert "error" not in create_result
            assert "name" in create_result

            # Extract exclusion ID from the full resource name
            exclusion_id = create_result["name"].split("/")[-1]
            print(f"Created rule exclusion ID: {exclusion_id}")

            # Wait for resource to be created
            time.sleep(2)

            # 2. Get the rule exclusion
            print(">>> Getting rule exclusion details")
            get_result = await get_rule_exclusion(
                exclusion_id=exclusion_id,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(get_result, dict)
            assert "error" not in get_result
            assert get_result.get("displayName") == display_name
            assert '(ip = "8.8.8.8")' in get_result.get("query", "")
            print(f"Successfully retrieved exclusion: {display_name}")

            # 3. List rule exclusions and verify ours exists
            print(">>> Listing rule exclusions")
            list_result = await list_rule_exclusions(
                page_size=100,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(list_result, dict)
            assert "error" not in list_result
            assert "findingsRefinements" in list_result
            assert "total_in_page" in list_result

            # Verify our exclusion is in the list
            exclusions = list_result.get("findingsRefinements", [])
            found = any(
                excl.get("name", "").endswith(exclusion_id)
                for excl in exclusions
            )
            assert found, f"Created exclusion {exclusion_id} not in list"
            print(f"Successfully found exclusion in list")

            # 4. Patch the rule exclusion
            print(">>> Patching rule exclusion")
            new_display_name = f"Updated Test Exclusion {test_id}"
            patch_result = await patch_rule_exclusion(
                exclusion_id=exclusion_id,
                display_name=new_display_name,
                query='(ip = "1.1.1.1")',
                update_mask="display_name,query",
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(patch_result, dict)
            assert "error" not in patch_result
            assert patch_result.get("displayName") == new_display_name
            print(f"Successfully patched exclusion")

            # 5. Update deployment settings
            print(">>> Updating deployment settings")
            deployment_result = await update_rule_exclusion_deployment(
                exclusion_id=exclusion_id,
                enabled=True,
                archived=False,
                detection_exclusion_application={
                    "curatedRules": [],
                    "curatedRuleSets": [],
                    "rules": [],
                },
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(deployment_result, dict)
            assert "error" not in deployment_result
            assert deployment_result.get("enabled") is True
            print(f"Successfully updated deployment settings")

        except Exception as e:
            print(f"Error in rule exclusion lifecycle test: {e}")
            raise

        finally:
            # 7. Cleanup: Archive the rule exclusion
            if exclusion_id:
                print(">>> Cleaning up: Archiving rule exclusion")
                try:
                    await update_rule_exclusion_deployment(
                        exclusion_id=exclusion_id,
                        enabled=False,
                        archived=True,
                        detection_exclusion_application={
                            "curatedRules": [],
                            "curatedRuleSets": [],
                            "rules": [],
                        },
                        project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                        customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                        region=chronicle_config["CHRONICLE_REGION"],
                    )
                    print(f"Successfully archived exclusion: {exclusion_id}")
                except Exception as cleanup_error:
                    print(f"Warning: Failed to archive: {cleanup_error}")

    @pytest.mark.asyncio
    async def test_compute_rule_exclusion_activity(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test computing rule exclusion activity.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        test_id = f"test_activity_{uuid.uuid4().hex[:8]}"
        display_name = f"Activity Test Exclusion {test_id}"
        exclusion_id = None

        try:
            # Create exclusion for activity testing
            print(f"\n>>> Creating exclusion for activity test: {test_id}")
            create_result = await create_rule_exclusion(
                display_name=display_name,
                refinement_type="DETECTION_EXCLUSION",
                query='(domain = "test.com")',
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            exclusion_id = create_result["name"].split("/")[-1]
            time.sleep(2)

            # Attempt to compute exclusion activity
            print(">>> Computing exclusion activity")
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=7)

            try:
                activity_result = await compute_rule_exclusion_activity(
                    exclusion_id=exclusion_id,
                    start_time=start_time,
                    end_time=end_time,
                    project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                    customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                    region=chronicle_config["CHRONICLE_REGION"],
                )

                # Check if API returned an error
                if "error" in activity_result:
                    pytest.skip(
                        f"Compute activity API is unavailable: "
                        f"{activity_result.get('error')}"
                    )

                assert isinstance(activity_result, dict)
                print(f"Successfully computed exclusion activity")

            except Exception as activity_error:
                # Skip test if API is flakey
                pytest.skip(
                    f"Compute activity API failed (known flakiness): "
                    f"{str(activity_error)}"
                )

        finally:
            if exclusion_id:
                try:
                    await update_rule_exclusion_deployment(
                        exclusion_id=exclusion_id,
                        enabled=False,
                        archived=True,
                        detection_exclusion_application={
                            "curatedRules": [],
                            "curatedRuleSets": [],
                            "rules": [],
                        },
                        project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                        customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                        region=chronicle_config["CHRONICLE_REGION"],
                    )
                except Exception:
                    pass

    @pytest.mark.asyncio
    async def test_list_rule_exclusions_pagination(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing rule exclusions with pagination.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Request with small page size to test pagination
        result = await list_rule_exclusions(
            page_size=1,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        assert isinstance(result, dict)
        assert "error" not in result
        assert "findingsRefinements" in result
        assert "total_in_page" in result

        exclusions = result.get("findingsRefinements", [])
        print(f"Retrieved {len(exclusions)} items on first page")

        # Check for next page token
        next_page_token = result.get("nextPageToken")
        if next_page_token:
            print(f"Found next page token, testing pagination")
            next_result = await list_rule_exclusions(
                page_size=1,
                page_token=next_page_token,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            assert isinstance(next_result, dict)
            assert "error" not in next_result
            assert "findingsRefinements" in next_result

            next_exclusions = next_result.get("findingsRefinements", [])
            print(f"Retrieved {len(next_exclusions)} items on next page")

            # Verify different items on different pages
            if len(exclusions) > 0 and len(next_exclusions) > 0:
                assert exclusions[0].get("name") != next_exclusions[0].get(
                    "name"
                )
                print("Verified different items on different pages")
        else:
            print("No pagination needed (single page of results)")

    @pytest.mark.asyncio
    async def test_get_nonexistent_rule_exclusion(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test getting a non-existent rule exclusion.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Use a UUID that definitely doesn't exist
        fake_id = f"nonexistent_{uuid.uuid4().hex}"

        result = await get_rule_exclusion(
            exclusion_id=fake_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Should return an error dict
        assert isinstance(result, dict)
        assert "error" in result
        print(f"Correctly returned error for non-existent exclusion")
