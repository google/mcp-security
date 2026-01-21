"""Integration tests for Chronicle SecOps Watchlist MCP tools.

These tests exercise the watchlist management functionality by making actual
API calls to the Chronicle service. They require proper authentication and
configuration to run.

To run these tests:
1. Make sure you have created a config.json file in the tests directory with
   your Chronicle credentials (see conftest.py for format)
2. Authenticate with Google Cloud using ADC:
   gcloud auth application-default login
   OR set SECOPS_SA_PATH environment variable to use service account:
   export SECOPS_SA_PATH=/path/to/service-account.json
3. Run: pytest -xvs server/secops/tests/test_secops_watchlist_mcp.py
"""

import uuid
from typing import Dict

import pytest

from secops_mcp.tools.watchlist_management import (
    create_watchlist,
    delete_watchlist,
    get_watchlist,
    list_watchlists,
    update_watchlist,
)


class TestChronicleWatchlistMCP:
    """Test class for Chronicle Watchlist MCP tools."""

    @pytest.mark.asyncio
    async def test_list_watchlists(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing all watchlists.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_watchlists(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Verify response structure
        assert isinstance(result, dict)

        # Should either have watchlists or an error
        if "error" not in result:
            assert "watchlists" in result or "total_in_page" in result

    @pytest.mark.asyncio
    async def test_list_watchlists_as_list(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test listing all watchlists with as_list parameter.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_watchlists(
            as_list=True,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Verify response structure
        assert isinstance(result, dict)

        # Should either have watchlists or an error
        if "error" not in result:
            assert "watchlists" in result
            assert "total_watchlists" in result

    @pytest.mark.asyncio
    async def test_get_watchlist(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test getting details of a watchlist.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # First list watchlists to get an ID
        watchlists_result = await list_watchlists(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Skip test if no watchlists or error
        if "error" in watchlists_result or not watchlists_result.get(
            "watchlists"
        ):
            pytest.skip("No watchlists available to test get_watchlist")

        # Get the first watchlist ID
        watchlist_id = watchlists_result["watchlists"][0]["name"].split("/")[-1]

        # Get watchlist details
        result = await get_watchlist(
            watchlist_id=watchlist_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Verify response structure
        assert isinstance(result, dict)

        # Should either have expected fields or an error
        if "error" not in result:
            assert "name" in result
            assert "displayName" in result

    @pytest.mark.asyncio
    async def test_create_update_delete_watchlist(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test the full lifecycle of a watchlist.

        Tests watchlist creation, updating, and deletion.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Create a unique name with UUID
        unique_id = str(uuid.uuid4())
        name = f"test_watchlist_{unique_id[:8]}"
        display_name = f"Test Watchlist MCP SDK {unique_id[:8]}"

        watchlist_id = None

        # Step 1: Create watchlist
        try:
            create_result = await create_watchlist(
                name=name,
                display_name=display_name,
                multiplying_factor=1.5,
                description="Test watchlist created by MCP SDK",
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            # Skip remaining tests if creation fails
            if "error" in create_result:
                pytest.fail(
                    f"Watchlist creation failed: {create_result['error']}"
                )

            # Verify creation result
            assert "name" in create_result
            assert create_result["displayName"] == display_name
            assert (
                create_result["multiplyingFactor"] == 1.5
                or create_result["multiplyingFactor"] == "1.5"
            )
            watchlist_id = create_result["name"].split("/")[-1]

            print(f"Created watchlist with ID: {watchlist_id}")

            # Step 2: Update watchlist
            update_result = await update_watchlist(
                watchlist_id=watchlist_id,
                display_name=f"Updated Test Watchlist {unique_id[:8]}",
                description="Updated test watchlist description",
                multiplying_factor=2.0,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            # Verify update result
            assert "name" in update_result
            assert "Updated Test Watchlist" in update_result["displayName"]
            assert (
                update_result["multiplyingFactor"] == 2.0
                or update_result["multiplyingFactor"] == "2.0"
            )

            print(f"Updated watchlist: {update_result['displayName']}")

        finally:
            # Always attempt to clean up by deleting the watchlist
            if watchlist_id:
                try:
                    delete_result = await delete_watchlist(
                        watchlist_id=watchlist_id,
                        force=True,
                        project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                        customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                        region=chronicle_config["CHRONICLE_REGION"],
                    )

                    # Verify delete result
                    assert isinstance(delete_result, dict)
                    assert (
                        "success" in delete_result
                        or "message" in delete_result
                        or "error" not in delete_result
                    )

                    print(f"Deleted watchlist with ID: {watchlist_id}")

                except Exception as e:
                    print(f"Warning: Failed to delete test watchlist: {e}")
