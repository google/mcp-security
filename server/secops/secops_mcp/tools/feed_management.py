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
"""Security Operations MCP tools for feed management."""

import logging
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger("secops-mcp")


@server.tool()
async def list_feeds(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List all feeds configured in Chronicle.

    Retrieves a list of all feeds that are configured in the
    Chronicle instance, providing details such as feed name, status,
    log type, and source type.

    **Workflow Integration:**
    - Use this tool to get an overview of all data ingestion feeds configured
      in your Chronicle instance.
    - Helpful for auditing data sources, troubleshooting missing data,
      or planning data source expansion.
    - Can be used in conjunction with log ingestion or parser management tools
      to ensure complete data collection coverage.

    **Use Cases:**
    - Inventory all data sources feeding into Chronicle SIEM
    - Verify that critical security log sources are properly configured
    - Identify feeds that may be inactive/disabled or experiencing issues
    - Audit feed configurations as part of security reviews

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the list of feeds and their
            details, or an error message if the operation fails.

    Example Usage:
        list_feeds()

    Next Steps (using MCP-enabled tools):
        - Check if specific critical log sources are properly configured
        - Identify and investigate any inactive/disabled feeds
        - Review feed configurations for proper log type mappings
        - Use parser management tools to verify parsers for these feeds
    """
    try:
        logger.info("Listing feeds")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Get all feeds
        feeds = chronicle.list_feeds()

        # Process feeds into a structured response
        result = {
            "feeds": [],
            "total_feeds": len(feeds),
            "active_feeds": 0,
            "disabled_feeds": 0,
        }

        # Count active and disabled feeds
        for feed in feeds:
            feed_state = feed.get("state", "UNKNOWN")
            if feed_state == "ACTIVE":
                result["active_feeds"] += 1
            elif feed_state == "INACTIVE":
                result["disabled_feeds"] += 1

            # Add feed details to result
            result["feeds"].append(feed)

        return result
    except Exception as e:
        logger.error(f"Error listing feeds: {e}", exc_info=True)
        return {"error": f"Error listing feeds: {e}"}


@server.tool()
async def get_feed(
    feed_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get detailed information about a specific feed.

    Retrieves complete configuration details for a specified feed by its ID,
    including connection settings, log type, state, and metadata.

    **Workflow Integration:**
    - Use this tool to get detailed information about a specific feed when
      troubleshooting data ingestion issues.
    - Can be used to verify configuration details before making changes
      to a feed.
    - Helpful for auditing specific feed configurations as part of security
      reviews or compliance checks.

    **Use Cases:**
    - Troubleshoot data ingestion issues for a specific feed
    - Verify detailed configuration settings before updating a feed
    - Check authentication and connection details for a feed
    - Review feed metadata and labels

    Args:
        feed_id (str): The ingestion feed identifier to retrieve details for.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the complete feed details,
            or an error message if the operation fails.

    Example Usage:
        get_feed(feed_id="123456789")

    Next Steps (using MCP-enabled tools):
        - Update feed configuration if needed
        - Check feed status and troubleshoot if inactive
        - Verify log parsing is working correctly using parser management tools
        - Search for recent events from this feed using security events search
    """
    try:
        logger.info(f"Getting details for feed with ID: {feed_id}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Get feed details
        feed = chronicle.get_feed(feed_id)

        if not feed:
            return {"error": f"Feed with ID {feed_id} not found"}

        return feed
    except Exception as e:
        logger.error(f"Error getting feed: {e}", exc_info=True)
        return {"error": f"Error getting feed: {e}"}


@server.tool()
async def create_feed(
    display_name: str,
    feed_details: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new feed in Chronicle.

    Creates a new feed configuration for ingesting security data into Chronicle.
    Supports various feed types including HTTP, S3, GCS, and GCP SCC.

    **Workflow Integration:**
    - Use this tool when adding new data sources to your Chronicle instance.
    - Helpful for automating data source onboarding processes.
    - Can be integrated with broader security data source management workflows.

    **Use Cases:**
    - Set up a new log source for ingestion into Chronicle
    - Configure endpoint for receiving security telemetry
    - Add new cloud storage source for security logs
    - Set up GCP Security Command Center integration

    Args:
        display_name (str): User-friendly name for the feed.
        feed_details (Dict[str, Any]): Dictionary containing feed configuration
            details. Must include:
            - logType (str): The Chronicle log type (e.g., "WINEVTLOG")
            - feedSourceType (str): Type of feed ("HTTP", "S3", "GCS", etc.)
            - Source-specific settings (httpSettings, s3Settings, etc.)
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the newly created feed details,
            or an error message if the operation fails.

    Example Usage:
        create_feed(
            display_name="Windows Event Logs Feed",
            feed_details={
                "logType": "WINEVTLOG",
                "feedSourceType": "HTTP",
                "httpSettings": {
                    "uri": "https://example.com/logs",
                    "sourceType": "FILES"
                },
                "labels": {"environment": "production"}
            }
        )

    Next Steps (using MCP-enabled tools):
        - Verify feed was created successfully using list_feeds
        - Check if data is flowing with security_events search
        - Configure alert rules for the new data source
        - Document the new data source in your security operations runbook
    """
    try:
        logger.info(f"Creating new feed: {display_name}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Create the feed
        return chronicle.create_feed(
            display_name=display_name, details=feed_details
        )

    except Exception as e:
        logger.error(f"Error creating feed: {e}", exc_info=True)
        return {"error": f"Error creating feed: {e}"}


@server.tool()
async def update_feed(
    feed_id: str,
    display_name: Optional[str] = None,
    feed_details: Dict[str, Any] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an existing feed in Chronicle.

    Modifies the configuration of an existing feed in Chronicle. Can
    update the display name, connection settings, or other properties.

    **Workflow Integration:**
    - Use this tool when needing to modify existing feed configurations.
    - Useful for updating connection details when data sources change.
    - Can be part of feed maintenance workflows or remediation processes.

    **Use Cases:**
    - Update feed endpoint URL after infrastructure changes
    - Modify authentication credentials
    - Change feed labels or metadata
    - Update feed configuration parameters

    Args:
        feed_id (str): The ID of the feed to update.
        display_name (Optional[str]): New display name for the feed.
            If None, the existing name is retained.
        feed_details (Optional[Dict[str, Any]]): Dictionary containing updated
            feed configuration details. Only specified fields will be updated.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the updated feed details,
            or an error message if the operation fails.

    Example Usage:
        update_feed(
            feed_id="123456789",
            display_name="Updated Windows Logs Feed",
            feed_details={
                "httpSettings": {
                    "uri": "https://new-endpoint.example.com/logs"
                },
                "labels": {"updated": "true"}
            }
        )

    Next Steps (using MCP-enabled tools):
        - Verify the feed updated correctly using get_feed
        - Check if data is still flowing with security_events search
        - Update documentation to reflect the changes
        - Monitor the feed for any issues after the update
    """
    try:
        logger.info(f"Updating feed with ID: {feed_id}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Update the feed
        return chronicle.update_feed(
            feed_id=feed_id,
            display_name=display_name,
            details=feed_details or {},
        )
    except Exception as e:
        logger.error(f"Error updating feed: {e}", exc_info=True)
        return {"error": f"Error updating feed: {e}"}


@server.tool()
async def enable_feed(
    feed_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Enable a inactive feed in Chronicle.

    Activates a feed that is currently in the INACTIVE state, allowing it
    to resume data ingestion.

    **Workflow Integration:**
    - Use this tool to re-enable feeds that were temporarily disabled.
    - Can be part of incident recovery workflows.
    - Useful for scheduled maintenance procedures.

    **Use Cases:**
    - Resume data collection after maintenance
    - Re-enable a feed that was temporarily disabled
    - Restore data flow as part of incident recovery
    - Enable feeds after troubleshooting connectivity issues

    Args:
        feed_id (str): The feed identifier which is to be enabled.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the updated feed status,
            or an error message if the operation fails.

    Example Usage:
        enable_feed(feed_id="123456789")

    Next Steps (using MCP-enabled tools):
        - Verify the feed is enabled using get_feed
        - Check if data is flowing correctly with security_events search
        - Update any incident tickets or maintenance records
        - Monitor the feed for any issues after enabling
    """
    try:
        logger.info(f"Enabling feed with ID: {feed_id}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Enable the feed
        enabled_feed = chronicle.enable_feed(feed_id)

        # Format the response
        result = {
            "id": feed_id,
            "state": enabled_feed.get("state", "UNKNOWN"),
            "message": "Feed enabled successfully",
        }

        return result
    except Exception as e:
        logger.error(f"Error enabling feed: {e}", exc_info=True)
        return {"error": f"Error enabling feed: {e}"}


@server.tool()
async def disable_feed(
    feed_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Disable an active feed in Chronicle.

    Stops data ingestion for a feed by setting its state to INACTIVE.
    The feed configuration remains but no new data will be processed.

    **Workflow Integration:**
    - Use this tool when needing to temporarily stop data collection.
    - Can be part of maintenance workflows or incident response.
    - Useful when troubleshooting data quality issues.

    **Use Cases:**
    - Temporarily stop data ingestion during source maintenance
    - Disable problematic feeds causing data quality issues
    - Pause data collection during infrastructure changes
    - Stop unused feeds to optimize resource usage

    Args:
        feed_id (str): The ID of the feed to disable.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the updated feed status,
            or an error message if the operation fails.

    Example Usage:
        disable_feed(feed_id="123456789")

    Next Steps (using MCP-enabled tools):
        - Verify the feed is inactive/disabled using get_feed
        - Update any maintenance tickets or documentation
        - Set a reminder to re-enable the feed when appropriate
        - Document the reason for disabling in your security operations runbook
    """
    try:
        logger.info(f"Disabling feed with ID: {feed_id}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Disable the feed
        disabled_feed = chronicle.disable_feed(feed_id)

        # Format the response
        result = {
            "id": feed_id,
            "state": disabled_feed.get("state", "UNKNOWN"),
            "message": "Feed disabled successfully",
        }

        return result
    except Exception as e:
        logger.error(f"Error disabling feed: {e}", exc_info=True)
        return {"error": f"Error disabling feed: {e}"}


@server.tool()
async def delete_feed(
    feed_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a feed from Chronicle.

    Permanently removes a feed from Chronicle. This action cannot be undone
    and will stop any data ingestion from this feed.

    **Workflow Integration:**
    - Use this tool when decommissioning data sources.
    - Part of cleanup workflows for removing unused configurations.
    - Should be used carefully and typically after disabling first.

    **Use Cases:**
    - Remove decommissioned data sources
    - Clean up test or temporary feed configurations
    - Remove duplicate or obsolete feed setups
    - Part of environment cleanup during migrations

    Args:
        feed_id (str): The ID of the feed to delete.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the operation status,
            or an error message if the operation fails.

    Example Usage:
        delete_feed(feed_id="123456789")

    Next Steps (using MCP-enabled tools):
        - Verify the feed was deleted using list_feeds
        - Update documentation to reflect the removal
        - Review any rules or dashboards that may have depended on this data
        - Consider archiving historical data if needed
    """
    try:
        logger.info(f"Deleting feed with ID: {feed_id}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Delete the feed
        chronicle.delete_feed(feed_id)

        # Format the response
        result = {"id": feed_id, "message": "Feed deleted successfully"}

        return result
    except Exception as e:
        logger.error(f"Error deleting feed: {e}", exc_info=True)
        return {"error": f"Error deleting feed: {e}"}


@server.tool()
async def generate_feed_secret(
    feed_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate authentication secret for a feed.

    Generates a new secret for https push feeds which do not support jwt tokens.
    This replaces any existing secret.

    **Workflow Integration:**
    - Use this tool when setting up authenticated feeds or rotating credentials.
    - Part of secure feed management and credential rotation workflows.
    - Important for maintaining secure data collection channels.

    **Use Cases:**
    - Generate initial authentication secret for a new feed
    - Rotate credentials as part of security best practices
    - Reset authentication after suspected compromise
    - Update credentials during security review processes

    Args:
        feed_id (str): The ID of the feed to generate a secret for.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the secret generation status,
            potentially including the new secret value (depending on API behavior),
            or an error message if the operation fails.

    Example Usage:
        generate_feed_secret(feed_id="123456789")

    Next Steps (using MCP-enabled tools):
        - Update the data source configuration with the new secret
        - Verify data continues flowing using security_events search
        - Document the secret rotation in your security operations runbook
        - Set a reminder for next credential rotation
    """
    try:
        logger.info(f"Generating secret for feed with ID: {feed_id}")
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Generate the secret
        secret_result = chronicle.generate_secret(feed_id)

        # Format the response
        result = {"id": feed_id, "message": "Secret generated successfully"}

        # Add secret to response if returned by the API
        if secret_result and "secret" in secret_result:
            result["secret"] = secret_result["secret"]

        return result
    except Exception as e:
        logger.error(f"Error generating feed secret: {e}", exc_info=True)
        return {"error": f"Error generating feed secret: {e}"}
