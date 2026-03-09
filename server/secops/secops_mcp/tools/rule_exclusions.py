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
"""Security Operations MCP tools for rule exclusions."""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server

# Configure logging
logger = logging.getLogger("secops-mcp")


@server.tool()
async def create_rule_exclusion(
    display_name: str,
    refinement_type: str,
    query: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new rule exclusion in Chronicle SIEM.

    Creates a rule exclusion to filter out false positives or exclude
    specific events from triggering detections. Rule exclusions use UDM
    query syntax to define which events should be excluded from detection
    rules.

    **Workflow Integration:**
    - Use to create exclusions for known false positives.
    - Essential for tuning detection rules and reducing alert noise.
    - Enables filtering of test/development environment traffic.
    - Supports exclusion of legitimate administrative activities.

    **Use Cases:**
    - Exclude specific IP addresses from brute force detection rules.
    - Filter out test environment traffic from production detections.
    - Exclude legitimate administrative tools from malware detections.
    - Remove known-good domains from suspicious DNS detections.
    - Filter scheduled tasks from anomaly detection rules.

    Args:
        display_name (str): User-friendly name for the exclusion.
        refinement_type (str): Type of exclusion refinement. Use
            "DETECTION_EXCLUSION" for detection exclusions.
        query (str): UDM query defining which events to exclude.
            Example: '(domain = "google.com")' or
            '(ip = "8.8.8.8")'.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing the created exclusion
            details including name, display_name, and query. Returns
            error dict if creation fails.

    Example Usage:
        # Exclude specific domain from detections
        create_rule_exclusion(
            display_name="Exclude Google Domain",
            refinement_type="DETECTION_EXCLUSION",
            query='(domain = "google.com")',
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Exclude IP address from brute force rule
        create_rule_exclusion(
            display_name="Exclude Scanner IP",
            refinement_type="DETECTION_EXCLUSION",
            query='(ip = "192.168.1.100")',
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Apply exclusion to specific rules using
          update_rule_exclusion_deployment.
        - Monitor exclusion activity using
          compute_rule_exclusion_activity.
        - Review exclusion effectiveness by checking alert volumes.
        - Document exclusion justification for compliance.
        - Periodically review exclusions to ensure still valid.
    """
    try:
        logger.info(
            f"Creating rule exclusion: {display_name} with type "
            f"{refinement_type}"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Create the rule exclusion and return SDK response directly
        return chronicle.create_rule_exclusion(
            display_name=display_name,
            refinement_type=refinement_type,
            query=query,
        )

    except Exception as e:
        logger.error(
            f"Error creating rule exclusion {display_name}: {str(e)}",
            exc_info=True,
        )
        return {
            "error": f"Error creating rule exclusion {display_name}: "
            f"{str(e)}"
        }


@server.tool()
async def get_rule_exclusion(
    exclusion_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get detailed information about a specific rule exclusion.

    Retrieves complete configuration and details for a rule exclusion
    by its ID, including display name, query, refinement type, and
    deployment status.

    **Workflow Integration:**
    - Use to review exclusion configuration before modifications.
    - Essential for auditing exclusion effectiveness and accuracy.
    - Helps understand which events are being filtered out.
    - Supports troubleshooting detection rule behavior.

    **Use Cases:**
    - Review exclusion query syntax for accuracy.
    - Verify exclusion is applied to correct rules.
    - Audit exclusions for compliance reporting.
    - Troubleshoot unexpected missing detections.
    - Document exclusion contents for security reviews.

    Args:
        exclusion_id (str): Exclusion ID only (e.g., "abc-123-def"),
            not the full resource name. Extract from the "name" field
            returned by list_rule_exclusions or create_rule_exclusion.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Complete exclusion details including query,
            refinement_type, and deployment configuration. Returns error
            dict if retrieval fails.

    Example Usage:
        # First, create or list exclusions to get the ID
        exclusions = list_rule_exclusions()
        # Extract ID from full name (last part after '/')
        exclusion_id = exclusions["findingsRefinements"][0]["name"].split(
            "/"
        )[-1]

        # Get exclusion details using just the ID
        exclusion = get_rule_exclusion(
            exclusion_id=exclusion_id,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Update exclusion configuration using patch_rule_exclusion.
        - Review which rules are using this exclusion.
        - Check exclusion activity using
          compute_rule_exclusion_activity.
        - Modify deployment settings if needed.
        - Export exclusion data for documentation or analysis.
    """
    try:
        logger.info(f"Getting rule exclusion details: {exclusion_id}")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Get exclusion details
        exclusion = chronicle.get_rule_exclusion(exclusion_id)

        if not exclusion:
            return {
                "error": f"Rule exclusion with ID {exclusion_id} not "
                "found"
            }

        return exclusion

    except Exception as e:
        error_msg = f"Error getting rule exclusion {exclusion_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def list_rule_exclusions(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List all rule exclusions in Chronicle SIEM.

    Retrieves a list of all rule exclusions configured in Chronicle
    with their basic details. Supports pagination for large result sets.

    **Workflow Integration:**
    - Use to get an overview of all configured exclusions.
    - Essential for exclusion inventory and management.
    - Helps identify exclusions for review or consolidation.
    - Supports auditing of false positive management.

    **Use Cases:**
    - Inventory all exclusions for security posture review.
    - Find specific exclusions by name or query pattern.
    - Audit exclusion coverage across detection rules.
    - Identify unused or obsolete exclusions for cleanup.
    - Generate reports on exclusion usage and effectiveness.

    Args:
        page_size (Optional[int]): Maximum number of exclusions to
            return per page. If not specified, uses Chronicle's default.
        page_token (Optional[str]): Token for retrieving next page of
            results. Obtained from previous response.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing exclusion data with
            pagination metadata. Typically includes "findingsRefinements"
            list and optional "nextPageToken". Returns error dict if
            listing fails.

    Example Usage:
        # List exclusions with pagination
        exclusions = list_rule_exclusions(
            page_size=50,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )
        for exclusion in exclusions.get("findingsRefinements", []):
            print(f"Exclusion: {exclusion.get('displayName')}")

        # Get next page if available
        next_token = exclusions.get("nextPageToken")
        if next_token:
            next_page = list_rule_exclusions(
                page_size=50,
                page_token=next_token,
                project_id="my-project",
                customer_id="my-customer",
                region="us"
            )

    Next Steps (using MCP-enabled tools):
        - Review exclusion configurations for optimization.
        - Use get_rule_exclusion for detailed information.
        - Identify and delete obsolete exclusions.
        - Check exclusion activity to measure effectiveness.
        - Document exclusion purposes and ownership.
    """
    try:
        logger.info("Listing rule exclusions")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Build parameters for list_rule_exclusions call
        kwargs = {}
        if page_size is not None:
            kwargs["page_size"] = page_size
        if page_token is not None:
            kwargs["page_token"] = page_token

        # List exclusions
        exclusions = chronicle.list_rule_exclusions(**kwargs)

        # Add summary statistics
        exclusion_count = len(exclusions.get("findingsRefinements", []))
        result = {**exclusions, "total_in_page": exclusion_count}
        return result

    except Exception as e:
        error_msg = f"Error listing rule exclusions: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def patch_rule_exclusion(
    exclusion_id: str,
    display_name: Optional[str] = None,
    query: Optional[str] = None,
    update_mask: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an existing rule exclusion in Chronicle SIEM.

    Updates exclusion properties including display name and query.
    Supports partial updates via update_mask to modify only specific
    fields.

    **Workflow Integration:**
    - Use to modify exclusion properties as requirements change.
    - Essential for refining exclusion queries for better accuracy.
    - Enables updating display names for better organization.
    - Supports iterative tuning of exclusion definitions.

    **Use Cases:**
    - Refine exclusion query to be more specific.
    - Update display name to reflect current purpose.
    - Broaden exclusion to cover additional scenarios.
    - Narrow exclusion to reduce over-filtering.
    - Fix incorrect exclusion query syntax.

    Args:
        exclusion_id (str): Unique identifier of the exclusion to
            update.
        display_name (Optional[str]): New display name for the exclusion.
        query (Optional[str]): New UDM query defining which events to
            exclude. Example: '(ip = "8.8.8.8")'.
        update_mask (Optional[str]): Comma-separated list of fields to
            update. Example: "display_name,query". If not specified,
            updates all provided fields.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing the updated exclusion
            details, or an error dictionary if update fails.

    Example Usage:
        # Update query only
        patch_rule_exclusion(
            exclusion_id="abc-123-def",
            query='(ip = "10.0.0.1" OR ip = "10.0.0.2")',
            update_mask="query",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Update both display name and query
        patch_rule_exclusion(
            exclusion_id="abc-123-def",
            display_name="Updated Exclusion Name",
            query='(domain = "example.com")',
            update_mask="display_name,query",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Verify changes using get_rule_exclusion.
        - Monitor impact of updated query on alert volumes.
        - Review exclusion activity after changes.
        - Document reason for changes in security operations log.
        - Test exclusion effectiveness with sample events.
    """
    try:
        logger.info(f"Patching rule exclusion: {exclusion_id}")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Update the exclusion and return SDK response directly
        return chronicle.patch_rule_exclusion(
            exclusion_id=exclusion_id,
            display_name=display_name,
            query=query,
            update_mask=update_mask,
        )

    except Exception as e:
        logger.error(
            f"Error patching rule exclusion {exclusion_id}: {str(e)}",
            exc_info=True,
        )
        return {
            "error": f"Error patching rule exclusion {exclusion_id}: "
            f"{str(e)}"
        }


@server.tool()
async def update_rule_exclusion_deployment(
    exclusion_id: str,
    enabled: bool,
    archived: bool,
    detection_exclusion_application: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Manage deployment settings for a rule exclusion.

    Updates exclusion deployment configuration including enable/disable
    status, archive status, and which rules or rule sets the exclusion
    should be applied to.

    **Workflow Integration:**
    - Use to enable or disable exclusions without deletion.
    - Essential for applying exclusions to specific rules or rule sets.
    - Enables archiving of obsolete exclusions for historical reference.
    - Supports dynamic exclusion management based on threat landscape.

    **Use Cases:**
    - Apply exclusion to specific detection rules only.
    - Enable exclusion during maintenance windows.
    - Disable exclusion temporarily for investigation.
    - Apply exclusion to entire curated rule sets.
    - Archive exclusions that are no longer needed but should be kept.

    Args:
        exclusion_id (str): Unique identifier of the exclusion.
        enabled (bool): Whether the exclusion should be active.
        archived (bool): Whether the exclusion should be archived.
        detection_exclusion_application (Dict[str, Any]): Configuration
            specifying which rules/rule sets to apply exclusion to.
            Example: {
                "curatedRules": ["rule_id_1", "rule_id_2"],
                "curatedRuleSets": ["rule_set_id_1"],
                "rules": ["custom_rule_id_1"]
            }
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing the updated deployment
            configuration, or an error dictionary if update fails.

    Example Usage:
        # Enable exclusion and apply to specific rules
        update_rule_exclusion_deployment(
            exclusion_id="abc-123-def",
            enabled=True,
            archived=False,
            detection_exclusion_application={
                "curatedRules": [],
                "curatedRuleSets": [],
                "rules": ["rule_123", "rule_456"]
            },
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Disable exclusion temporarily
        update_rule_exclusion_deployment(
            exclusion_id="abc-123-def",
            enabled=False,
            archived=False,
            detection_exclusion_application={
                "curatedRules": [],
                "curatedRuleSets": [],
                "rules": []
            },
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Monitor alert volumes after enabling/disabling exclusion.
        - Verify exclusion is applied to correct rules.
        - Check exclusion activity using
          compute_rule_exclusion_activity.
        - Document deployment changes for audit trail.
        - Review rule detections to ensure proper filtering.
    """
    try:
        logger.info(
            f"Updating rule exclusion deployment: {exclusion_id} "
            f"(enabled={enabled}, archived={archived})"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Update deployment settings
        return chronicle.update_rule_exclusion_deployment(
            exclusion_id=exclusion_id,
            enabled=enabled,
            archived=archived,
            detection_exclusion_application=detection_exclusion_application,
        )

    except Exception as e:
        logger.error(
            f"Error updating rule exclusion deployment {exclusion_id}: "
            f"{str(e)}",
            exc_info=True,
        )
        return {
            "error": f"Error updating rule exclusion deployment "
            f"{exclusion_id}: {str(e)}"
        }


@server.tool()
async def compute_rule_exclusion_activity(
    exclusion_id: str,
    start_time: datetime,
    end_time: datetime,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Calculate activity statistics for a rule exclusion.

    Computes statistics showing how many events were excluded by this
    exclusion during the specified time period. Helps measure exclusion
    effectiveness and impact.

    **Workflow Integration:**
    - Use to measure exclusion effectiveness and impact.
    - Essential for auditing false positive reduction efforts.
    - Helps identify over-filtering exclusions.
    - Supports reporting on exclusion usage and value.

    **Use Cases:**
    - Measure how many events an exclusion filtered.
    - Identify exclusions with high activity (may be over-filtering).
    - Find unused exclusions with zero activity.
    - Report on false positive reduction metrics.
    - Justify exclusion retention or removal decisions.

    Args:
        exclusion_id (str): Unique identifier of the exclusion.
        start_time (datetime): Start of time period for activity
            calculation. Should be timezone-aware datetime object.
        end_time (datetime): End of time period for activity calculation.
            Should be timezone-aware datetime object.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing activity statistics
            including count of excluded events. Returns error dict if
            computation fails.

    Example Usage:
        from datetime import datetime, timedelta, timezone

        # Calculate activity for last 7 days
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=7)

        activity = compute_rule_exclusion_activity(
            exclusion_id="abc-123-def",
            start_time=start_time,
            end_time=end_time,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )
        print(f"Events excluded: {activity.get('count', 0)}")

        # Calculate activity for specific date range
        start_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 31, tzinfo=timezone.utc)

        activity = compute_rule_exclusion_activity(
            exclusion_id="abc-123-def",
            start_time=start_time,
            end_time=end_time,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Review high-activity exclusions for over-filtering.
        - Consider removing zero-activity exclusions.
        - Document exclusion effectiveness metrics.
        - Adjust exclusion queries based on activity patterns.
        - Generate reports on false positive reduction.
    """
    try:
        logger.info(
            f"Computing rule exclusion activity for {exclusion_id} from "
            f"{start_time} to {end_time}"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Compute exclusion activity
        activity = chronicle.compute_rule_exclusion_activity(
            exclusion_id=exclusion_id,
            start_time=start_time,
            end_time=end_time,
        )

        return activity

    except Exception as e:
        error_msg = (
            f"Error computing rule exclusion activity for "
            f"{exclusion_id}: {str(e)}"
        )
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
