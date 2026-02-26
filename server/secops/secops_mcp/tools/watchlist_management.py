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
"""Security Operations MCP tools for watchlist management."""

import logging
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server

# Configure logging
logger = logging.getLogger("secops-mcp")


@server.tool()
async def create_watchlist(
    name: str,
    display_name: str,
    multiplying_factor: float,
    description: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new watchlist in Chronicle SIEM.

    Creates a watchlist for managing entity risk scores and monitoring
    specific entities. Watchlists apply risk multipliers to entities and
    can be used to track high-risk actors, privileged accounts, or other
    entities requiring special attention.

    **Workflow Integration:**
    - Use to create watchlists for tracking high-risk entities or VIPs.
    - Essential for entity risk management and monitoring workflows.
    - Enables risk score amplification for watchlisted entities.
    - Supports both manual and automated entity population mechanisms.

    **Use Cases:**
    - Create watchlist for monitoring privileged accounts.
    - Track suspicious IP addresses with elevated risk scores.
    - Monitor executive accounts for targeted attacks.
    - Track threat actor infrastructure with high risk multipliers.
    - Create watchlists for regulatory compliance monitoring.

    Args:
        name (str): Unique name for the watchlist (used internally).
        display_name (str): User-friendly display name for the watchlist.
        multiplying_factor (float): Risk score multiplier for entities
            on this watchlist (e.g., 1.5 increases risk by 50%).
        description (str): Description of the watchlist's purpose.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing the created watchlist details,
            or an error dictionary if watchlist creation fails.

    Example Usage:
        # Create watchlist for privileged accounts
        create_watchlist(
            name="privileged_accounts",
            display_name="Privileged User Accounts",
            multiplying_factor=2.0,
            description="High-risk accounts with elevated privileges",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Create watchlist for suspicious IPs
        create_watchlist(
            name="suspicious_ips",
            display_name="Suspicious IP Addresses",
            multiplying_factor=1.5,
            description="IP addresses with suspicious activity",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Add entities to the watchlist through entity management tools.
        - Monitor watchlist impact on entity risk scores.
        - Create detection rules leveraging watchlist membership.
        - Review entities on the watchlist regularly for accuracy.
        - Adjust risk multipliers based on threat intelligence updates.
    """
    try:
        logger.info(
            f"Creating watchlist: {name} with multiplier "
            f"{multiplying_factor}"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Create the watchlist and return SDK response directly
        return chronicle.create_watchlist(
            name=name,
            display_name=display_name,
            multiplying_factor=multiplying_factor,
            description=description,
        )

    except Exception as e:
        logger.error(
            f"Error creating watchlist {name}: {str(e)}", exc_info=True
        )
        return {"error": f"Error creating watchlist {name}: {str(e)}"}


@server.tool()
async def update_watchlist(
    watchlist_id: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    multiplying_factor: Optional[float] = None,
    entity_population_mechanism: Optional[Dict[str, Any]] = None,
    watchlist_user_preferences: Optional[Dict[str, Any]] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an existing watchlist in Chronicle SIEM.

    Updates watchlist properties including display name, description,
    risk multiplier, entity population mechanism, and user preferences.
    Only provided parameters will be updated.

    **Workflow Integration:**
    - Use to modify watchlist properties as requirements change.
    - Essential for adjusting risk multipliers based on threat landscape.
    - Enables configuration of automated entity population mechanisms.
    - Supports user preference updates like pinning watchlists.

    **Use Cases:**
    - Increase risk multiplier for a watchlist during active threats.
    - Update description to reflect current monitoring objectives.
    - Change entity population mechanism from manual to automated.
    - Pin important watchlists for quick access.
    - Adjust watchlist configuration based on operational feedback.

    Args:
        watchlist_id (str): Unique identifier of the watchlist to update.
        display_name (Optional[str]): New display name for the watchlist.
        description (Optional[str]): New description for the watchlist.
        multiplying_factor (Optional[float]): New risk score multiplier.
        entity_population_mechanism (Optional[Dict[str, Any]]): Entity
            population configuration (e.g., {"manual": {}}).
        watchlist_user_preferences (Optional[Dict[str, Any]]): User
            preferences (e.g., {"pinned": True}).
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing the updated watchlist details,
            or an error dictionary if update fails.

    Example Usage:
        # Update risk multiplier
        update_watchlist(
            watchlist_id="abc-123-def",
            multiplying_factor=3.0,
            description="Increased multiplier due to active campaign",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Pin watchlist and update display name
        update_watchlist(
            watchlist_id="abc-123-def",
            display_name="Critical Threat Actors",
            watchlist_user_preferences={"pinned": True},
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Verify changes using `get_watchlist` to confirm updates.
        - Monitor impact of risk multiplier changes on entity scores.
        - Review entities on watchlist after configuration changes.
        - Document reason for changes in security operations log.
        - Communicate significant changes to security team members.
    """
    try:
        logger.info(f"Updating watchlist: {watchlist_id}")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Update the watchlist and return SDK response directly
        return chronicle.update_watchlist(
            watchlist_id=watchlist_id,
            display_name=display_name,
            description=description,
            multiplying_factor=multiplying_factor,
            entity_population_mechanism=entity_population_mechanism,
            watchlist_user_preferences=watchlist_user_preferences,
        )

    except Exception as e:
        logger.error(
            f"Error updating watchlist {watchlist_id}: {str(e)}", exc_info=True
        )
        return {"error": f"Error updating watchlist {watchlist_id}: {str(e)}"}


@server.tool()
async def delete_watchlist(
    watchlist_id: str,
    force: bool = False,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a watchlist from Chronicle SIEM.

    Permanently removes a watchlist from Chronicle. Use the force parameter
    to handle dependencies. This operation cannot be undone.

    **Workflow Integration:**
    - Use to remove obsolete or unused watchlists.
    - Essential for maintaining clean watchlist configurations.
    - Supports forced deletion to handle dependencies.
    - Part of watchlist lifecycle management workflows.

    **Use Cases:**
    - Remove watchlists that are no longer needed.
    - Clean up test or temporary watchlists.
    - Delete duplicate watchlists created by mistake.
    - Remove watchlists after threat campaigns end.
    - Consolidate multiple watchlists into single lists.

    **Warning:**
    This operation permanently deletes the watchlist. Ensure entities
    on the watchlist are migrated to other watchlists if still needed.

    Args:
        watchlist_id (str): Unique identifier of the watchlist to delete.
        force (bool): Force deletion even if dependencies exist.
            Defaults to False.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary confirming watchlist deletion,
            or an error dictionary if deletion fails.

    Example Usage:
        # Delete watchlist
        delete_watchlist(
            watchlist_id="abc-123-def",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Force delete watchlist with dependencies
        delete_watchlist(
            watchlist_id="abc-123-def",
            force=True,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Verify deletion using `list_watchlists`.
        - Migrate critical entities to other watchlists if needed.
        - Update detection rules that referenced the deleted watchlist.
        - Document the reason for deletion in operations log.
        - Review entity risk scores after watchlist removal.
    """
    try:
        logger.info(f"Deleting watchlist: {watchlist_id} (force={force})")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Delete the watchlist
        result = chronicle.delete_watchlist(watchlist_id, force=force)

        # If delete returns None or empty, return success confirmation
        if not result:
            return {
                "success": True,
                "watchlist_id": watchlist_id,
                "message": "Watchlist deleted successfully",
            }

        return result

    except Exception as e:
        logger.error(
            f"Error deleting watchlist {watchlist_id}: {str(e)}", exc_info=True
        )
        return {"error": f"Error deleting watchlist {watchlist_id}: {str(e)}"}


@server.tool()
async def get_watchlist(
    watchlist_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Get detailed information about a specific watchlist.

    Retrieves complete configuration and details for a watchlist by its ID,
    including display name, description, risk multiplier, entity population
    mechanism, and current entities on the watchlist.

    **Workflow Integration:**
    - Use to review watchlist configuration and entity membership.
    - Essential for auditing watchlist effectiveness and accuracy.
    - Helps understand entity risk score calculations.
    - Supports troubleshooting watchlist-related detection rules.

    **Use Cases:**
    - Review entities currently on a watchlist.
    - Verify watchlist configuration before making changes.
    - Audit risk multipliers for compliance reporting.
    - Troubleshoot entity risk score calculations.
    - Document watchlist contents for security reviews.

    Args:
        watchlist_id (str): Watchlist ID only (e.g., "abc-123-def"), not
            the full resource name. Extract from the "name" field returned
            by list_watchlists or create_watchlist.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Complete watchlist details including configuration
            and entity information. Returns error dict if retrieval fails.

    Example Usage:
        # First, list watchlists to get the ID
        watchlists = list_watchlists()
        # Extract ID from the full name (last part after '/')
        watchlist_id = watchlists["watchlists"][0]["name"].split("/")[-1]

        # Get watchlist details using just the ID
        watchlist = get_watchlist(
            watchlist_id=watchlist_id,  # Just the ID, not full name
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Review entity list for accuracy and relevance.
        - Update watchlist configuration using `update_watchlist`.
        - Remove outdated entities from the watchlist.
        - Create detection rules leveraging watchlist membership.
        - Export watchlist data for reporting or analysis.
    """
    try:
        logger.info(f"Getting watchlist details: {watchlist_id}")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Get watchlist details
        watchlist = chronicle.get_watchlist(watchlist_id)

        if not watchlist:
            return {"error": f"Watchlist with ID {watchlist_id} not found"}

        return watchlist

    except Exception as e:
        error_msg = f"Error getting watchlist {watchlist_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def list_watchlists(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    as_list: bool = False,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List all watchlists in Chronicle SIEM.

    Retrieves a list of all watchlists configured in Chronicle with their
    basic details. Supports pagination for large result sets and optional
    automatic pagination with the as_list parameter.

    **Workflow Integration:**
    - Use to get an overview of all configured watchlists.
    - Essential for watchlist inventory and management.
    - Helps identify watchlists for review or consolidation.
    - Supports auditing of entity risk management configuration.

    **Use Cases:**
    - Inventory all watchlists for security posture review.
    - Find specific watchlists by name or description.
    - Audit risk multipliers across all watchlists.
    - Identify unused or obsolete watchlists for cleanup.
    - Generate reports on watchlist coverage and usage.

    Args:
        page_size (Optional[int]): Maximum number of watchlists to return
            per page. If not specified, uses Chronicle's default.
        page_token (Optional[str]): Token for retrieving next page of
            results. Obtained from previous response.
        as_list (bool): If True, automatically fetches all pages and
            returns a list of watchlists. If False, returns paginated
            response with metadata. Defaults to False.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary containing watchlist data. If as_list
            is False, includes pagination metadata. If as_list is True,
            contains a direct list of all watchlists. Returns error dict
            if listing fails.

    Example Usage:
        # List watchlists with pagination
        watchlists = list_watchlists(
            page_size=50,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )
        for watchlist in watchlists.get("watchlists", []):
            print(f"Watchlist: {watchlist.get('displayName')}")

        # Get all watchlists as a list (auto-pagination)
        all_watchlists = list_watchlists(
            as_list=True,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )
        for watchlist in all_watchlists.get("watchlists", []):
            print(f"Watchlist: {watchlist.get('displayName')}")

    Next Steps (using MCP-enabled tools):
        - Review watchlist configurations for optimization.
        - Use `get_watchlist` for detailed information on specific lists.
        - Identify and delete obsolete watchlists.
        - Document watchlist purposes and ownership.
        - Create new watchlists for emerging threat scenarios.
    """
    try:
        logger.info("Listing watchlists")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Build parameters for list_watchlists call
        kwargs = {}
        if page_size is not None:
            kwargs["page_size"] = page_size
        if page_token is not None:
            kwargs["page_token"] = page_token
        if as_list:
            kwargs["as_list"] = as_list

        # List watchlists
        watchlists = chronicle.list_watchlists(**kwargs)

        # If as_list=True, watchlists is a direct list
        # If as_list=False, it's a dict with pagination metadata
        if as_list:
            # Convert list to dict format for consistency
            return {
                "watchlists": watchlists,
                "total_watchlists": len(watchlists),
            }
        else:
            # Add summary statistics
            watchlist_count = len(watchlists.get("watchlists", []))
            result = {**watchlists, "total_in_page": watchlist_count}
            return result

    except Exception as e:
        error_msg = f"Error listing watchlists: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
