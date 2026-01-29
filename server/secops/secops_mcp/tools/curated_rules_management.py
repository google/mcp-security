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
"""Security Operations MCP tools for curated rules management."""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server


logger = logging.getLogger("secops-mcp")


@server.tool()
async def list_curated_rules(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 100,
    page_token: Optional[str] = None,
    as_list: bool = False,
) -> Dict[str, Any]:
    """List all curated detection rules available in Chronicle.

    Retrieves pre-built detection rules provided by Google Chronicle
    that can be enabled and deployed without custom development.
    Curated rules cover common security threats and attack patterns.

    **Workflow Integration:**
    - Discover available pre-built detection content from Chronicle.
    - Identify relevant curated rules for specific threat scenarios.
    - Review rule descriptions and coverage before deployment.
    - Complement custom detection rules with Google-maintained content.

    **Use Cases:**
    - Browse available curated rules for ransomware detection.
    - Find curated rules covering specific MITRE ATT&CK techniques.
    - Identify pre-built rules for cloud security monitoring.
    - Review available detection content before enabling rule sets.
    - Audit currently available curated detection capabilities.

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.
        page_size (int): Maximum number of rules to return per page.
            Defaults to 100.
        page_token (Optional[str]): Token for retrieving next page of
            results.
        as_list (bool): If True, automatically paginate and return all
            rules as a list. Defaults to False.

    Returns:
        Dict[str, Any]: Response containing curated rules and
            pagination metadata. Structure includes:
            - curatedRules: List of curated rule objects
            - nextPageToken: Token for pagination (if more results)
            Returns error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Review specific rule details using `get_curated_rule`.
        - Enable relevant rules via `update_curated_rule_set_deployment`.
        - Search for detections using `search_curated_detections`.
        - Deploy rule sets containing multiple curated rules.
    """
    try:
        logger.info(f"Listing curated rules (page_size={page_size})")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        if as_list:
            rules = chronicle.list_curated_rules(as_list=True)
            return {"curatedRules": rules}
        else:
            return chronicle.list_curated_rules(
                page_size=page_size, page_token=page_token
            )

    except Exception as e:
        logger.error(f"Error listing curated rules: {str(e)}", exc_info=True)
        return {"error": str(e), "curatedRules": []}


@server.tool()
async def get_curated_rule(
    rule_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve specific curated rule details by rule ID.

    Fetches the complete definition and metadata for a specific
    Google-curated detection rule. Provides detailed information
    about rule logic, severity, and detection capabilities.

    **Workflow Integration:**
    - Review complete details of a specific curated rule.
    - Understand detection logic before enabling the rule.
    - Analyze rule metadata including severity and coverage.
    - Evaluate rule fit for your security monitoring needs.

    **Use Cases:**
    - Review details of a curated rule identified from search.
    - Understand what threats a specific curated rule detects.
    - Analyze rule logic before enabling it in production.
    - Document curated rule capabilities for security teams.
    - Compare multiple curated rules for similar threats.

    Args:
        rule_id (str): Unique identifier of the curated rule to
            retrieve. Example: "ur_ttp_lol_Atbroker"
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Complete curated rule information including:
            - Rule definition and metadata
            - Description and severity
            - Detection logic details
            Returns error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Enable the rule via `update_curated_rule_set_deployment`.
        - Search for historical detections using
            `search_curated_detections`.
        - Review related rules in the same rule set.
        - Configure alerting settings for the rule.
    """
    try:
        logger.info(f"Retrieving curated rule: {rule_id}")

        chronicle = get_chronicle_client(project_id, customer_id, region)
        rule = chronicle.get_curated_rule(rule_id)

        logger.info(f"Successfully retrieved curated rule: {rule_id}")
        return rule

    except Exception as e:
        logger.error(
            f"Error retrieving curated rule {rule_id}: {str(e)}",
            exc_info=True,
        )
        return {
            "error": f"Error retrieving curated rule: {str(e)}",
            "rule": {},
        }


@server.tool()
async def get_curated_rule_by_name(
    display_name: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Find curated rule by display name.

    Searches for a curated rule matching the specified display name.
    Note: This performs a linear scan of all curated rules and may
    be inefficient for large rule sets.

    **Workflow Integration:**
    - Find curated rules by their human-readable names.
    - Locate specific rules when only the display name is known.
    - Search for rules mentioned in security documentation.

    **Use Cases:**
    - Find "Atbroker.exe Abuse" rule by name.
    - Locate specific rules referenced in threat intelligence.
    - Search for rules by threat technique names.

    Args:
        display_name (str): Display name of the curated rule to find.
            Example: "Atbroker.exe Abuse"
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Curated rule information if found. Returns
            error structure if not found or API call fails.

    Next Steps (using MCP-enabled tools):
        - Enable the rule via `update_curated_rule_set_deployment`.
        - Review rule details using `get_curated_rule`.
        - Search for detections using `search_curated_detections`.
    """
    try:
        logger.info(f"Searching for curated rule by name: {display_name}")

        chronicle = get_chronicle_client(project_id, customer_id, region)
        rule = chronicle.get_curated_rule_by_name(display_name)

        if rule:
            logger.info(f"Found curated rule: {display_name}")
            return rule
        else:
            return {
                "error": f"Curated rule not found: {display_name}",
                "rule": {},
            }

    except Exception as e:
        logger.error(
            f"Error finding curated rule by name {display_name}: " f"{str(e)}",
            exc_info=True,
        )
        return {
            "error": f"Error finding curated rule: {str(e)}",
            "rule": {},
        }


@server.tool()
async def search_curated_detections(
    rule_id: str,
    start_time: str,
    end_time: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    list_basis: Optional[str] = None,
    alert_state: Optional[str] = None,
    page_size: int = 100,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Search detections generated by a specific curated rule.

    Retrieves detections from a curated rule within a specified time
    range. Useful for investigating threats detected by Google-curated
    detection content and analyzing rule effectiveness.

    **Workflow Integration:**
    - Investigate threats detected by curated rules.
    - Analyze curated rule effectiveness and alert volume.
    - Review historical detections for specific threat patterns.
    - Scope incidents based on curated rule matches.

    **Use Cases:**
    - Retrieve all detections from a curated ransomware rule.
    - Analyze alert frequency for specific curated detections.
    - Investigate threats detected by cloud security rules.
    - Filter detections by alert state (ALERTING/NOT_ALERTING).
    - Review detections from recently enabled curated rules.

    Args:
        rule_id (str): Unique identifier of the curated rule. Example:
            "ur_ttp_GCP_MassSecretDeletion"
        start_time (str): Start of search time range in ISO 8601
            format. Example: "2025-01-20T00:00:00Z"
        end_time (str): End of search time range in ISO 8601 format.
            Example: "2025-01-27T23:59:59Z"
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.
        list_basis (Optional[str]): Basis for listing detections.
            Valid values: "DETECTION_TIME", "CREATED_TIME".
        alert_state (Optional[str]): Filter by alert state. Valid
            values: "ALERTING", "NOT_ALERTING".
        page_size (int): Maximum number of detections to return.
            Defaults to 100.
        page_token (Optional[str]): Token for retrieving next page.

    Returns:
        Dict[str, Any]: Response containing detections and pagination
            metadata. Structure includes:
            - curatedDetections: List of detection objects
            - nextPageToken: Token for pagination (if more results)
            Returns error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Analyze detection details and associated events.
        - Enrich indicators using threat intelligence tools.
        - Create or update incidents in case management systems.
        - Review entity details using `lookup_entity`.
        - Investigate related UDM events using `search_udm`.
    """
    try:
        logger.info(
            f"Searching curated detections for rule {rule_id} "
            f"from {start_time} to {end_time}"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        result = chronicle.search_curated_detections(
            rule_id=rule_id,
            start_time=start_dt,
            end_time=end_dt,
            list_basis=list_basis,
            alert_state=alert_state,
            page_size=page_size,
            page_token=page_token,
        )

        detection_count = len(result.get("curatedDetections", []))
        logger.info(f"Found {detection_count} curated detections")

        return result

    except ValueError as ve:
        logger.error(
            f"Invalid time format for curated detections search: " f"{str(ve)}",
            exc_info=True,
        )
        return {
            "error": f"Invalid time format: {str(ve)}",
            "curatedDetections": [],
        }
    except Exception as e:
        logger.error(
            f"Error searching curated detections for rule {rule_id}: "
            f"{str(e)}",
            exc_info=True,
        )
        return {
            "error": str(e),
            "curatedDetections": [],
        }


@server.tool()
async def list_curated_rule_sets(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 100,
    page_token: Optional[str] = None,
    as_list: bool = False,
) -> Dict[str, Any]:
    """List all curated rule sets available in Chronicle.

    Retrieves collections of related curated rules grouped by threat
    category, data source, or detection objective. Rule sets can be
    enabled together for comprehensive coverage.

    **Workflow Integration:**
    - Discover available curated rule set collections.
    - Identify rule sets relevant to your data sources.
    - Review rule set coverage for specific threat categories.
    - Enable multiple related rules simultaneously.

    **Use Cases:**
    - Browse available rule sets for Azure security monitoring.
    - Find rule sets covering ransomware detection.
    - Identify rule sets for specific cloud platforms.
    - Review rule set organization and structure.
    - Audit available pre-built detection content.

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.
        page_size (int): Maximum number of rule sets to return.
            Defaults to 100.
        page_token (Optional[str]): Token for retrieving next page.
        as_list (bool): If True, automatically paginate and return all
            rule sets as a list. Defaults to False.

    Returns:
        Dict[str, Any]: Response containing rule sets and pagination
            metadata. Structure includes:
            - curatedRuleSets: List of rule set objects
            - nextPageToken: Token for pagination (if more results)
            Returns error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Review specific rule set details using
            `get_curated_rule_set`.
        - Enable rule sets via
            `update_curated_rule_set_deployment`.
        - Check deployment status using
            `list_curated_rule_set_deployments`.
        - Review rules within a set using `list_curated_rules`.
    """
    try:
        logger.info(f"Listing curated rule sets (page_size={page_size})")

        chronicle = get_chronicle_client(project_id, customer_id, region)

        if as_list:
            rule_sets = chronicle.list_curated_rule_sets(as_list=True)
            return {"curatedRuleSets": rule_sets}
        else:
            result = chronicle.list_curated_rule_sets(
                page_size=page_size, page_token=page_token
            )
            return result

    except Exception as e:
        logger.error(
            f"Error listing curated rule sets: {str(e)}",
            exc_info=True,
        )
        return {"error": str(e), "curatedRuleSets": []}


@server.tool()
async def get_curated_rule_set(
    rule_set_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve specific curated rule set details by ID.

    Fetches complete configuration and metadata for a specific curated
    rule set. Provides information about the rules included in the set
    and deployment options.

    **Workflow Integration:**
    - Review detailed information about a specific rule set.
    - Understand which rules are included in the set.
    - Analyze rule set coverage before deployment.
    - Plan rule set deployment strategy.

    **Use Cases:**
    - Review rules included in "Azure - Network" rule set.
    - Understand coverage of GCP security monitoring rule set.
    - Analyze rule set configuration before enabling.
    - Document deployed rule set capabilities.
    - Compare multiple rule sets for similar coverage.

    Args:
        rule_set_id (str): Unique identifier of the curated rule set.
            Example: "00ad672e-ebb3-0dd1-2a4d-99bd7c5e5f93"
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Complete rule set information including:
            - Rule set configuration and metadata
            - Included rules and coverage
            - Deployment options and settings
            Returns error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Enable the rule set via
            `update_curated_rule_set_deployment`.
        - Review individual rules using `get_curated_rule`.
        - Check deployment status using
            `list_curated_rule_set_deployments`.
        - Configure alerting settings for the rule set.
    """
    try:
        logger.info(f"Retrieving curated rule set: {rule_set_id}")

        chronicle = get_chronicle_client(project_id, customer_id, region)
        rule_set = chronicle.get_curated_rule_set(rule_set_id)

        logger.info(f"Successfully retrieved curated rule set: {rule_set_id}")
        return rule_set

    except Exception as e:
        logger.error(
            f"Error retrieving curated rule set {rule_set_id}: " f"{str(e)}",
            exc_info=True,
        )
        return {
            "error": f"Error retrieving curated rule set: {str(e)}",
            "ruleSet": {},
        }


@server.tool()
async def list_curated_rule_set_deployments(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
    page_size: int = 100,
    page_token: Optional[str] = None,
    as_list: bool = False,
) -> Dict[str, Any]:
    """List deployment status of all curated rule sets.

    Retrieves deployment configuration for curated rule sets,
    including enabled status, precision level (broad/precise), and
    alerting configuration. Essential for managing curated content.

    **Workflow Integration:**
    - Monitor which curated rule sets are currently enabled.
    - Review alerting configuration for deployed rule sets.
    - Audit detection coverage from curated content.
    - Identify rule sets that need configuration updates.

    **Use Cases:**
    - Check which curated rule sets are currently enabled.
    - Review alerting settings for deployed rule sets.
    - Identify rule sets configured for broad vs precise detection.
    - Audit curated detection coverage across the environment.
    - Find rule sets that need alerting enabled.

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.
        page_size (int): Maximum number of deployments to return.
            Defaults to 100.
        page_token (Optional[str]): Token for retrieving next page.
        as_list (bool): If True, automatically paginate and return all
            deployments as a list. Defaults to False.

    Returns:
        Dict[str, Any]: Response containing deployments and pagination
            metadata. Structure includes:
            - curatedRuleSetDeployments: List of deployment objects
            - nextPageToken: Token for pagination (if more results)
            Each deployment includes enabled status, precision level,
            and alerting configuration.
            Returns error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Update deployment settings using
            `update_curated_rule_set_deployment`.
        - Review rule set details using `get_curated_rule_set`.
        - Enable alerting for specific rule sets.
        - Adjust precision levels based on environment needs.
    """
    try:
        logger.info(
            f"Listing curated rule set deployments " f"(page_size={page_size})"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        if as_list:
            deployments = chronicle.list_curated_rule_set_deployments(
                as_list=True
            )
            return {"curatedRuleSetDeployments": deployments}
        else:
            result = chronicle.list_curated_rule_set_deployments(
                page_size=page_size, page_token=page_token
            )
            return result

    except Exception as e:
        logger.error(
            f"Error listing curated rule set deployments: {str(e)}",
            exc_info=True,
        )
        return {"error": str(e), "curatedRuleSetDeployments": []}


@server.tool()
async def update_curated_rule_set_deployment(
    category_id: str,
    rule_set_id: str,
    precision: str,
    enabled: bool,
    alerting: bool,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Update deployment configuration for a curated rule set.

    Enables or disables a curated rule set, configures precision level
    (broad or precise), and controls alerting settings. Essential for
    managing curated detection content deployment.

    **Workflow Integration:**
    - Enable curated rule sets for specific threat coverage.
    - Configure precision levels to balance coverage and noise.
    - Enable or disable alerting for rule sets.
    - Adjust detection settings based on operational needs.

    **Use Cases:**
    - Enable the "Azure - Network" rule set with precise detection.
    - Turn on alerting for GCP security rule set.
    - Switch rule set from broad to precise detection mode.
    - Disable rule sets that generate excessive false positives.
    - Enable comprehensive cloud security monitoring.

    **Precision Modes:**
    - **broad**: More detections, potentially higher false positive
        rate. Better for comprehensive threat hunting.
    - **precise**: Fewer detections, lower false positive rate.
        Better for production alerting.

    Args:
        category_id (str): Category ID of the rule set. Example:
            "110fa43d-7165-2355-1985-a63b7cdf90e8"
        rule_set_id (str): Unique identifier of the rule set. Example:
            "00ad672e-ebb3-0dd1-2a4d-99bd7c5e5f93"
        precision (str): Detection precision level. Valid values:
            "broad", "precise"
        enabled (bool): Whether to enable the rule set for detection.
        alerting (bool): Whether to enable alerting for detections.
        project_id (Optional[str]): Google Cloud project ID. Defaults
            to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults
            to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us",
            "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Updated deployment configuration including
            status and settings. Returns error structure if the API
            call fails.

    Next Steps (using MCP-enabled tools):
        - Verify deployment status using
            `list_curated_rule_set_deployments`.
        - Monitor detections using `search_curated_detections`.
        - Review generated alerts using `get_security_alerts`.
        - Adjust settings based on alert volume and accuracy.
    """
    try:
        logger.info(
            f"Updating curated rule set deployment: {rule_set_id} "
            f"(enabled={enabled}, precision={precision}, "
            f"alerting={alerting})"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        valid_precision_values = ["broad", "precise"]
        if precision not in valid_precision_values:
            error_msg = (
                f"Invalid precision value: {precision}. "
                f"Must be one of {valid_precision_values}"
            )
            logger.error(error_msg)
            return {"error": error_msg}

        deployment_config = {
            "category_id": category_id,
            "rule_set_id": rule_set_id,
            "precision": precision,
            "enabled": enabled,
            "alerting": alerting,
        }

        result = chronicle.update_curated_rule_set_deployment(deployment_config)

        logger.info(
            f"Successfully updated curated rule set deployment: "
            f"{rule_set_id}"
        )
        return result

    except Exception as e:
        logger.error(
            f"Error updating curated rule set deployment "
            f"{rule_set_id}: {str(e)}",
            exc_info=True,
        )
        return {
            "error": (f"Error updating curated rule set deployment: {str(e)}"),
        }
