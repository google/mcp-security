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
"""Security Operations MCP tools for security rules."""

import logging
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def list_security_rules(
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> Dict[str, Any]:
    """List security detection rules configured in Chronicle SIEM.

    Retrieves the definitions of detection rules currently active or configured
    within the Chronicle SIEM instance.

    **Workflow Integration:**
    - Useful for understanding the detection capabilities currently deployed in the SIEM.
    - Can help identify the specific rule that generated a SIEM alert (obtained via SIEM alert tools
      or from case management/SOAR system details).
    - Provides context for rule tuning, development, or understanding alert logic.

    **Use Cases:**
    - Review the logic or scope of a specific detection rule identified from an alert.
    - Audit the set of active detection rules within the SIEM.
    - Understand which rules might be relevant to a particular threat scenario or TTP.

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Raw response from the Chronicle API, typically containing a list
                        of rule objects with their definitions and metadata. Returns an
                        error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Analyze the rule definition (e.g., the YARA-L code) to understand its trigger conditions.
        - Correlate rule details with specific alerts retrieved from the SIEM or case management system.
        - Use insights for rule optimization, false positive analysis, or developing related detections.
        - Document relevant rule information in associated cases using a case management tool.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        rules_response = chronicle.list_rules()
        return rules_response
    except Exception as e:
        logger.error(f'Error listing security rules: {str(e)}', exc_info=True)
        return {'error': str(e), 'rules': []}

@server.tool()
async def search_security_rules(
    query: str,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> Dict[str, Any]:
    """Search security detection rules configured in Chronicle SIEM.

    Retrieves the definitions of detection rules currently active or configured
    within the Chronicle SIEM instance based on a regex pattern.
    
    **Workflow Integration:**
    - Useful for understanding the detection capabilities currently deployed in the SIEM.
    - Can help identify the specific rule that generated a SIEM alert (obtained via SIEM alert tools
      or from case management/SOAR system details).
    - Provides context for rule tuning, development, or understanding alert logic.

    **Use Cases:**
    - Review the logic or scope of a specific detection rule identified from an alert.
    - Audit the set of active detection rules within the SIEM.
    - Understand which rules might be relevant to a particular threat scenario or TTP.

    **Examples:**
    - Searching for all rules related to a specific MITRE technique like "TA0005" for defense evasion detections.
    - Searching for static data coded into detections like a specific hostname or IP address like "192.168.1.1".
    - Searching for rules that reference a specific log_type like "WORKSPACE"

    Args:
        query (str): Regex string to use for searching SecOps rules.
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Raw response from the Chronicle API, typically containing a list
                        of rule objects with their definitions and metadata. Returns an
                        error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - Analyze the rule definition (e.g., the YARA-L code) to understand its trigger conditions.
        - Correlate rule details with specific alerts retrieved from the SIEM or case management system.
        - Use insights for rule optimization, false positive analysis, or developing related detections.
        - Document relevant rule information in associated cases using a case management tool.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        rules_response = chronicle.search_rules(query)
        return rules_response
    except Exception as e:
        logger.error(f'Error searching security rules: {str(e)}', exc_info=True)
        return {'error': str(e), 'rules': []}

@server.tool()
async def get_rule_detections(
    rule_id: str,
    alert_state: Optional[str] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieves historical detections generated by a specific Chronicle SIEM rule.

    This tool fetches detections based on a rule ID, allowing for investigation
    and analysis of rule performance and threat activity.

    **Workflow Integration:**
    - **Alert Triage:** When an alert is generated by a rule, use this tool to retrieve all historical detections for that rule to understand the context and frequency.
    - **Rule Effectiveness Analysis:** Analyze the volume, timestamps, and details of detections to determine if a rule is too noisy, too quiet, or performing as expected.
    - **Threat Hunting:** If a rule is designed to detect a specific TTP or indicator, use this tool to find all instances where the rule has matched historical data.
    - **Incident Scoping:** During an incident, if a particular rule is relevant, retrieve its detections to help identify the scope and timeline of related events.
    - **Compliance Reporting:** Gather detections for specific rules related to compliance mandates over a certain period.

    **Use Cases:**
    - Retrieve all detections for a rule ID obtained from a SIEM alert or a case management system.
    - Filter detections by their alert state (e.g., "ALERTING", "NOT_ALERTING") to focus on actionable events.
    - Paginate through a large number of detections if a rule is particularly verbose.
    - Monitor the output of a newly deployed or recently modified detection rule.
    - Investigate past occurrences of a threat detected by a specific rule.
    - Assess the Alert to determine liklihood of maliciousness

    Args:
        rule_id (str): Unique ID of the rule to list detections for.
                        Examples: "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" (latest version),
                        "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx@v_12345_67890" (specific version),
                        "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx@-" (all versions).
        alert_state (Optional[str]): If provided, filter by alert state.
                                     Valid values: "UNSPECIFIED", "NOT_ALERTING", "ALERTING".
        page_size (Optional[int]): If provided, the maximum number of detections to return in a single response.
        page_token (Optional[str]): If provided, a token to retrieve the next page of results for pagination.
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the list of detections (under a 'detections' key, typically)
                        and pagination information (e.g., 'nextPageToken'). Returns an error
                        structure if the API call fails. The exact structure depends on the
                        Chronicle API version and client implementation.

    Next Steps (using MCP-enabled tools):
        - **Analyze Composite Detections:** If the CollectionElments contain additional Detection IDs, retrieve those detections and analyze the events as well
        - **Enrich Observables:** Extract indicators (IPs, domains, hashes) from the detection details or related UDM events and use threat intelligence tools for enrichment.
        - **Case Management:** If detections reveal significant activity, create or update incidents in a case management or SOAR system.
        - **Rule Tuning:** Based on the nature and volume of detections (e.g., many false positives), consider modifying the rule logic (using a hypothetical `update_rule` tool) or its alerting configuration (using `enable_rule` or similar).
        - **Retro-Hunting:** If the rule was recently updated or if you want to test variations, initiate a new retrohunt (e.g., using `create_retrohunt`).
        - **Error Checking:** If detections are missing or behavior is unexpected, check for rule execution errors (e.g., using `list_errors`).
        - **Visualize Detections:** Export detection data and use data visualization tools to identify trends or patterns over time.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)

        if not hasattr(chronicle, 'base_url') or not hasattr(chronicle, 'instance_id') or not hasattr(chronicle, 'session'):
            logger.error("Chronicle client from get_chronicle_client is missing expected attributes (base_url, instance_id, session).")
            return {'error': 'Chronicle client misconfigured for direct session access.', 'detections': []}
                
        valid_alert_states = ["UNSPECIFIED", "NOT_ALERTING", "ALERTING"]
        if alert_state:
            if alert_state not in valid_alert_states:
                logger.error(f"Invalid alert_state: {alert_state}. Must be one of {valid_alert_states}")
                raise ValueError(f"alert_state must be one of {valid_alert_states}, got {alert_state}")
        
        detections_response = chronicle.list_detections(rule_id, alert_state, page_size, page_token)
        
        return detections_response
    except ValueError as ve: # Catch specific ValueError from alert_state validation
        logger.error(f'Validation error getting rule detections for rule {rule_id}: {str(ve)}', exc_info=True)
        return {'error': str(ve), 'detections': []}
    except Exception as e:
        logger.error(f'Unexpected error getting rule detections for rule {rule_id}: {str(e)}', exc_info=True)
        return {'error': f'Unexpected error: {str(e)}', 'detections': []}

# Example of how list_errors might be defined as an MCP tool, if needed later.
# This is based on the second function in the first code block provided by the user.
@server.tool()
async def list_rule_errors(
    rule_id: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Lists execution errors for a specific Chronicle SIEM rule.

    Helps in troubleshooting rules that might not be generating detections as expected
    or are failing during execution.

    **Workflow Integration:**
    - **Rule Troubleshooting:** If a rule is not producing expected detections or alerts, check for execution errors.
    - **Rule Development:** After deploying a new or modified rule, check for errors to ensure it's syntactically correct and running properly.
    - **SIEM Health Monitoring:** Periodically check for rules with high error counts to maintain SIEM operational health.

    **Use Cases:**
    - Investigate why a specific rule (e.g., "ru_...") has not generated any detections.
    - Check for errors after modifying and saving a YARA-L rule.
    - Get details of compilation or runtime errors for a given rule version.

    Args:
        rule_id (str): Unique ID of the rule to list errors for.
                        Examples: "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" (latest version),
                        "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx@v_12345_67890" (specific version),
                        "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx@-" (all versions).
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing rule execution errors. The structure depends on the API.
                        Returns an error structure if the API call fails.

    Next Steps (using MCP-enabled tools):
        - **Review Rule Code:** If errors are found, retrieve the rule definition using `list_security_rules` or a hypothetical `get_rule_definition` tool and analyze the YARA-L code.
        - **Validate Rule Syntax:** Use a rule validation tool (like a hypothetical `validate_rule_syntax` tool or offline YARA-L validators) to check for syntax issues.
        - **Modify Rule:** Correct the rule based on error messages and update it in Chronicle.
        - **Re-check Detections:** After fixing errors, use `get_rule_detections` to see if the rule now produces detections.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)

        if not hasattr(chronicle, 'base_url') or not hasattr(chronicle, 'instance_id') or not hasattr(chronicle, 'session'):
            logger.error("Chronicle client from get_chronicle_client is missing expected attributes (base_url, instance_id, session).")
            return {'error': 'Chronicle client misconfigured for direct session access.', 'errors': []}

        
        logger.info(f"Requesting errors for rule_id: {rule_id}")
        response = chronicle.list_errors(rule_id)
        
        return response
        
    except Exception as e:
        logger.error(f'Unexpected error listing rule errors for {rule_id}: {str(e)}', exc_info=True)
        return {'error': f'Unexpected error: {str(e)}', 'errors': []}
    
@server.tool()
async def validate_security_rules(
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    rule_text= str,

) -> Dict[str, Any]:
    """Validate security detection rules in YARA-L2 format.

    Sends a YL2 rule to the Google SecOps API for validation

    **Workflow Integration:**
    - Useful for testing rules before they are deployed, or while they are being developed.
    - Can help identify errors in YARA-L syntax or structure.
    - Provides feedback furing rule development cycle.

    **Use Cases:**
    - Review the syntax and structure of a specific YARA-L detection.
    - Determine if a rule is written correctly.
    - Provide feedback on how to fix syntax and structure errors in a rule.

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Response from the Chronicle API.  Returns "true" if the rule is valid, any other response is an error.

    Next Steps (using MCP-enabled tools):
        - Analyze any error messages.
        - Make changes to the rule to resolve any errors.
        - Use insights for rule optimization, false positive analysis, or developing related detections.
        - validate rule again to ensure errors are gone
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        validate_response = chronicle.validate_rule(rule_text)
        return validate_response
    except Exception as e:
        logger.error(f'Error validating security rules: {str(e)}', exc_info=True)
        return {'error': str(e), 'rules': []}

