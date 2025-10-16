"""Integration tests for Chronicle SecOps MCP tools.

These tests exercise the full functionality of the secops_mcp.py tools
by making actual API calls to the Chronicle service. They require proper
authentication and configuration to run.

To run these tests:
1. Make sure you have created a config.json file in the tests directory with
   your Chronicle credentials (see conftest.py for format)
2. Authenticate with Google Cloud using ADC: 
   gcloud auth application-default login
3. Run: pytest -xvs server/secops/tests/test_secops_mcp.py
"""

import uuid
from typing import Dict

import pytest

from secops_mcp.tools.security_events import search_security_events
from secops_mcp.tools.feed_management import (
    create_feed,
    delete_feed,
    disable_feed,
    enable_feed,
    get_feed,
    list_feeds,
    update_feed,
)
from secops_mcp.tools.security_alerts import get_security_alerts, get_security_alert_by_id, do_update_security_alert
from secops_mcp.tools.entity_lookup import lookup_entity
from secops_mcp.tools.security_rules import list_security_rules, get_rule_detections, list_rule_errors, search_security_rules
from secops_mcp.tools.ioc_matches import get_ioc_matches
from secops_mcp.tools.threat_intel import get_threat_intel


class TestChronicleSecOpsMCP:
    """Test class for Chronicle SecOps MCP tools."""

    @pytest.mark.asyncio
    async def test_search_security_events_basic(self, chronicle_config: Dict[str, str]) -> None:
        """Test basic search for security events using natural language.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test with a simple natural language query
        result = await search_security_events(
            text="Show me network connections from the last 24 hours",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=24,
            max_events=10,
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "udm_query" in result
        assert "events" in result
        
        # Verify UDM query was generated
        assert isinstance(result["udm_query"], str)
        assert len(result["udm_query"]) > 0
        
        # Verify events structure
        events = result["events"]
        assert isinstance(events, dict)
        assert "total_events" in events
        
        # Note: We don't assert events were found as that depends on data in the system
        # Instead we verify the API call worked and returned the expected structure

    @pytest.mark.asyncio
    async def test_search_security_events_with_time_range(self, chronicle_config: Dict[str, str]) -> None:
        """Test search with a specific time range.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test with a more specific query and time range
        result = await search_security_events(
            text="Show me connections to IP address 8.8.8.8",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=72,  # Looking back 3 days
            max_events=20,
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, dict)
        assert "udm_query" in result
        assert "events" in result
        
        # Verify the UDM query includes the specific IP
        assert "8.8.8.8" in result["udm_query"]
    
    @pytest.mark.asyncio
    async def test_search_security_events_detailed_query(self, chronicle_config: Dict[str, str]) -> None:
        """Test search with a detailed security query.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test with a detailed query that should generate complex UDM
        result = await search_security_events(
            text="Show me failed login attempts for admin users in the last 24 hours",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=24,
            max_events=50,
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, dict)
        assert "udm_query" in result
        
        # The UDM query should be reasonably complex
        udm_query = result["udm_query"] 
        assert len(udm_query) > 20
        
        # Keywords that might appear in this query
        login_keywords = ["login", "auth", "failed", "admin", "user"]
        # At least one of these keywords should be in the query
        assert any(keyword in udm_query.lower() for keyword in login_keywords)
    
    @pytest.mark.asyncio
    async def test_get_security_alerts(self, chronicle_config: Dict[str, str]) -> None:
        """Test retrieving security alerts.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test basic alert retrieval
        result = await get_security_alerts(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=168,  # 1 week
            max_alerts=10,
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        
        # The result should either indicate alerts were found or none were found
        assert "Found" in result or "No security alerts found" in result
        
        # If alerts were found, verify basic structure in the response
        if "Found" in result:
            assert "Alert " in result
            assert "Rule:" in result
            assert "Created:" in result
            assert "Status:" in result
            assert "Severity:" in result
    
    @pytest.mark.asyncio
    async def test_get_security_alerts_with_status_filter(self, chronicle_config: Dict[str, str]) -> None:
        """Test retrieving security alerts with a status filter.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test alert retrieval with a specific status filter
        result = await get_security_alerts(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=720,  # 30 days
            max_alerts=20,
            status_filter="",  # No filter to get all alerts
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        
        # Another test with different status filter
        result_open = await get_security_alerts(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=720,  # 30 days
            max_alerts=20,
            status_filter="feedback_summary.status = \"OPEN\"",  # Only open alerts
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result_open, str)
    
    @pytest.mark.asyncio
    async def test_lookup_entity_ip(self, chronicle_config: Dict[str, str]) -> None:
        """Test looking up an IP entity.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test lookup of a common IP (Google DNS)
        result = await lookup_entity(
            entity_value="8.8.8.8",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=168,  # 1 week
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        assert "Entity Summary for 8.8.8.8" in result
        
        # Either entity information is found or not found message
        assert "Primary Entity" in result or "No information found" in result
    
    @pytest.mark.asyncio
    async def test_lookup_entity_domain(self, chronicle_config: Dict[str, str]) -> None:
        """Test looking up a domain entity.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test lookup of a common domain
        result = await lookup_entity(
            entity_value="google.com",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=168,  # 1 week
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        assert "Entity Summary for google.com" in result
    
    @pytest.mark.asyncio
    async def test_lookup_entity_hash(self, chronicle_config: Dict[str, str]) -> None:
        """Test looking up a file hash entity.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test lookup of a file hash (made-up example)
        # Note: This might not find results in your dataset
        result = await lookup_entity(
            entity_value="44d88612fea8a8f36de82e1278abb02f",  # Example MD5
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=720,  # 30 days
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        
        # The test can pass if we either get information about the entity or a message saying no information was found
        # This is because the test hash may not exist in the current dataset
        assert ("Entity Summary for 44d88612fea8a8f36de82e1278abb02f" in result or 
                "No information found for entity: 44d88612fea8a8f36de82e1278abb02f" in result)
    
    @pytest.mark.asyncio
    async def test_list_security_rules(self, chronicle_config: Dict[str, str]) -> None:
        """Test listing security detection rules.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_security_rules(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        # This should return either a valid response or an error dict
        assert isinstance(result, dict)
        
        # Expect either rules list or error
        assert "rules" in result or "error" in result
        
        # If rules are present, verify structure
        if "rules" in result and isinstance(result["rules"], list) and len(result["rules"]) > 0:
            # Check the first rule has expected fields
            first_rule = result["rules"][0]
            assert isinstance(first_rule, dict)
            
            # Just check if it has any keys, don't validate specific field names
            # since API response format might vary
            assert len(first_rule.keys()) > 0
        
        # Test passes if we get a valid dictionary response

    @pytest.mark.asyncio
    async def test_search_security_rules(self, chronicle_config: Dict[str, str]) -> None:
        """Test searching security detection rules.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await search_security_rules(
            query=".*",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        # This should return either a valid response or an error dict
        assert isinstance(result, dict)
        
        # Expect either rules list or error
        assert "rules" in result or "error" in result
        
        # If rules are present, verify structure
        if "rules" in result and isinstance(result["rules"], list) and len(result["rules"]) > 0:
            # Check the first rule has expected fields
            first_rule = result["rules"][0]
            assert isinstance(first_rule, dict)
            
            # Just check if it has any keys, don't validate specific field names
            # since API response format might vary
            assert len(first_rule.keys()) > 0
        
        # Test passes if we get a valid dictionary response
    
    @pytest.mark.asyncio
    async def test_get_ioc_matches(self, chronicle_config: Dict[str, str]) -> None:
        """Test retrieving IoC matches.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await get_ioc_matches(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            hours_back=24,
            max_matches=20,
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        
        # Should either find matches or indicate none found
        assert "Found" in result or "No IoC matches found" in result
        
        # If matches found, verify structure
        if "Found" in result and "IoC matches" in result:
            assert "Type:" in result
            assert "Value:" in result
            assert "Sources:" in result
    
    @pytest.mark.asyncio
    async def test_get_threat_intel(self, chronicle_config: Dict[str, str]) -> None:
        """Test getting threat intelligence.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test with common threat actor query
        result = await get_threat_intel(
            query="Tell me about APT29 threat actor",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        
        # The result should contain information about APT29
        assert "APT29" in result or "APT-29" in result or "Cozy Bear" in result
    
    @pytest.mark.asyncio
    async def test_get_threat_intel_cve(self, chronicle_config: Dict[str, str]) -> None:
        """Test getting threat intelligence about a CVE.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test with a CVE query
        result = await get_threat_intel(
            query="What is CVE-2021-44228 and how serious is it?",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"], 
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should have information about Log4j
        assert "CVE-2021-44228" in result or "Log4j" in result or "Log4Shell" in result
    
    @pytest.mark.asyncio
    async def test_get_threat_intel_general(self, chronicle_config: Dict[str, str]) -> None:
        """Test getting general threat intelligence information.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Test with a general security question
        result = await get_threat_intel(
            query="What are best practices for detecting lateral movement in a network?",
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should be about lateral movement
        assert "lateral movement" in result.lower() or "network" in result.lower() 


    @pytest.mark.asyncio
    async def test_get_rule_detections(self, chronicle_config: Dict[str, str]) -> None:
        """Test listing detections by rule id.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        rule_id = "ru_<insert rule_id>"

        if "insert" in rule_id:
            pytest.skip("No rule id provided to test get_rule_detections")

        result = await get_rule_detections(
            rule_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        # This should return either a valid response or an error dict
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_rule_detection_errors(self, chronicle_config: Dict[str, str]) -> None:
        """Test listing errors for detection rules.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        rule_id = "ru_<insert rule_id>"

        if "insert" in rule_id:
            pytest.skip("No rule id provided to test get_rule_detection_errors")

        result = await list_rule_errors(
            rule_id,
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )
        
        # This should return either a valid response or an error dict
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_do_update_security_alert(self, chronicle_config: Dict[str, str]) -> None:
        """Test updating Alert details by alert id
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        alert_id = "de_<insert_detection_id>"
        
        if "insert" in alert_id:
            pytest.skip("No alert id provided to test do_update_security_alert")

        result = await do_update_security_alert(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            comment = "Hello from SecOps MCP",
            priority="PRIORITY_MEDIUM",
            severity=50,
            alert_id=alert_id
        )
        
        # This should return either a valid response or an error dict
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_security_alert_by_id(self, chronicle_config: Dict[str, str]) -> None:
        """Test listing errors for detection rules.
        
        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        alert_id = "de_<insert_detection_id>"

        if "insert" in alert_id:
            pytest.skip("No alert id provided to test get_security_alert_by_id")

        result = await get_security_alert_by_id(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
            alert_id=alert_id
        )
        
        # This should return either a valid response or an error dict
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_list_feeds(self, chronicle_config: Dict[str, str]) -> None:
        """Test listing feeds.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        result = await list_feeds(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Verify response structure
        assert isinstance(result, dict)

        # Expect either feeds list or error
        assert "feeds" in result or "error" in result

        # Verify feeds list structure if no error
        if "feeds" in result and not "error" in result:
            assert "total_feeds" in result
            assert isinstance(result["feeds"], list)

            # Check counters
            assert "active_feeds" in result
            assert "disabled_feeds" in result
            assert isinstance(result["active_feeds"], int)
            assert isinstance(result["disabled_feeds"], int)

            # If we have feeds, check the structure of the first one
            if result["feeds"]:
                first_feed = result["feeds"][0]
                assert "name" in first_feed
                assert "displayName" in first_feed
                assert "state" in first_feed
                assert "details" in first_feed
                assert "feedSourceType" in first_feed["details"]
                assert "logType" in first_feed["details"]

    @pytest.mark.asyncio
    async def test_get_feed(self, chronicle_config: Dict[str, str]) -> None:
        """Test getting details of a feed.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # First list feeds to get an ID
        feeds_result = await list_feeds(
            project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
            customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
            region=chronicle_config["CHRONICLE_REGION"],
        )

        # Skip test if no feeds or error
        if "error" in feeds_result or not feeds_result.get("feeds"):
            pytest.skip("No feeds available to test get_feed")

        # Get the first feed ID
        feed_id = feeds_result["feeds"][0]["name"].split("/")[-1]

        # Get feed details
        result = await get_feed(
            feed_id=feed_id,
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
            assert "state" in result
            assert "details" in result

    @pytest.mark.asyncio
    async def test_create_update_disable_delete_feed(
        self, chronicle_config: Dict[str, str]
    ) -> None:
        """Test the full lifecycle of a feed.

        Tests feed creation, updating, disabling/enabling and deletion.

        Args:
            chronicle_config: Dictionary with Chronicle configuration
        """
        # Create a unique display name with UUID
        unique_id = str(uuid.uuid4())
        display_name = f"Test Feed MCP SDK {unique_id[:8]}"
        feed_details = {
            "logType": f"projects/{chronicle_config['CHRONICLE_PROJECT_ID']}/locations/us/instances/{chronicle_config['CHRONICLE_CUSTOMER_ID']}/logTypes/WINEVTLOG",
            "feedSourceType": "HTTP",
            "httpSettings": {
                "uri": "https://example.com/test_feed",
                "sourceType": "FILES",
            },
            "labels": {"environment": "test", "created_by": "mcp_test"},
        }

        feed_id = None
        # Step 1: Create feed
        try:
            create_result = await create_feed(
                display_name=display_name,
                feed_details=feed_details,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            # Skip remaining tests if creation fails
            if "error" in create_result:
                pytest.fail(f"Feed creation failed: {create_result['error']}")

            # Verify creation result
            assert "name" in create_result
            assert create_result["displayName"] == display_name
            feed_id = create_result["name"].split("/")[-1]

            # Step 2: Update feed
            update_result = await update_feed(
                feed_id=feed_id,
                display_name=f"Updated Test MCP Feed {unique_id[:8]}",
                feed_details={
                    "logType": f"projects/{chronicle_config["CHRONICLE_PROJECT_ID"]}/locations/{chronicle_config["CHRONICLE_REGION"]}/instances/{chronicle_config["CHRONICLE_CUSTOMER_ID"]}/logTypes/WINEVTLOG",
                    "feedSourceType": "HTTP",
                    "httpSettings": {
                        "uri": "https://example.com/updated_feed",
                        "sourceType": "FILES",
                    },
                    "labels": {
                        "environment": "test",
                        "created_by": "mcp_test",
                    },
                },
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            # Verify update result
            assert "name" in update_result
            assert "Updated Test MCP Feed" in update_result["displayName"]

            # Step 3: Disable feed
            disable_result = await disable_feed(
                feed_id=feed_id,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            # Verify disable result
            assert "id" in disable_result
            assert disable_result["state"] == "INACTIVE"

            # Step 4: Enable feed
            enable_result = await enable_feed(
                feed_id=feed_id,
                project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                region=chronicle_config["CHRONICLE_REGION"],
            )

            # Verify enable result
            assert "id" in enable_result
            assert enable_result["state"] == "ACTIVE"

        finally:
            # Always attempt to clean up by deleting the feed
            if feed_id:
                try:
                    delete_result = await delete_feed(
                        feed_id=feed_id,
                        project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
                        customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
                        region=chronicle_config["CHRONICLE_REGION"],
                    )

                    # Verify delete result
                    assert "id" in delete_result
                    assert "message" in delete_result
                except Exception as e:
                    print(f"Warning: Failed to delete test feed: {e}")
