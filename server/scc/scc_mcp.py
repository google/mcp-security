# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
from typing import Any, Dict, List

from google.api_core import exceptions as google_exceptions
from google.cloud import asset_v1
from google.cloud import securitycenter_v2
from google.protobuf import json_format 
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("scc-mcp")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scc-mcp")
logger.setLevel(logging.INFO)

# Add handler to see uvicorn/fastapi logs if they use standard logging
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

# --- SCC Client Initialization ---
# The client automatically uses Application Default Credentials (ADC).
# Ensure ADC are configured in the environment where the server runs
# (e.g., by running `gcloud auth application-default login`).
try:
    scc_client = securitycenter_v2.SecurityCenterClient()
    logger.info("Successfully initialized Google Cloud Security Center v2 Client.")
except Exception as e:
    logger.error(f"Failed to initialize Security Center Client: {e}", exc_info=True)
    # Depending on requirements, you might want to exit or prevent tool registration
    scc_client = None # Indicate client is not available

# --- CAI Client Initialization ---
try:
    cai_client = asset_v1.AssetServiceClient()
    logger.info("Successfully initialized Google Cloud Asset Inventory Client.")
except Exception as e:
    logger.error(f"Failed to initialize Cloud Asset Inventory Client: {e}", exc_info=True)
    cai_client = None # Indicate client is not available

# --- Helper Function for Proto to Dict Conversion ---

def proto_message_to_dict(message: Any) -> Dict[str, Any]:
    """Converts a protobuf message to a dictionary."""
    try:
        return json_format.MessageToDict(message._pb)
    except Exception as e:
        logger.error(f"Error converting protobuf message to dict: {e}")
        # Fallback or re-raise depending on desired error handling
        return {"error": "Failed to serialize response part", "details": str(e)}


# --- Security Command Center Tools ---

@mcp.tool()
async def search_findings(
    project_id: str,
    finding_class: str = None,
    severity: str = None,
    state: str = "ACTIVE",
    category: str = None,
    resource_name: str = None,
    resource_type: str = None,
    mute: str = None,
    custom_filter: str = None,
    max_findings: int = 50,
    location: str = "global",
    order_by: str = "event_time desc",
) -> Dict[str, Any]:
    """Name: search_findings

    Description: Searches and lists ALL types of Security Command Center findings for a specific project
                 with flexible filtering. Returns full finding details including descriptions, remediation
                 steps, severity, attack exposure, and all associated metadata. Supports filtering by
                 finding class (VULNERABILITY, THREAT, MISCONFIGURATION, OBSERVATION, SCC_ERROR,
                 POSTURE_VIOLATION, TOXIC_COMBINATION, SENSITIVE_DATA_RISK, CHOKEPOINT), severity,
                 state, category, resource name/type, and mute status.
    Parameters:
    project_id (required): The Google Cloud project ID (e.g., 'my-gcp-project').
    finding_class (optional): Filter by finding class. Valid values: VULNERABILITY, THREAT,
        MISCONFIGURATION, OBSERVATION, SCC_ERROR, POSTURE_VIOLATION, TOXIC_COMBINATION,
        SENSITIVE_DATA_RISK, CHOKEPOINT. Can combine with OR (e.g., 'THREAT OR MISCONFIGURATION').
    severity (optional): Filter by severity. Valid values: CRITICAL, HIGH, MEDIUM, LOW.
        Can combine with OR (e.g., 'HIGH OR CRITICAL').
    state (optional): Filter by state. Valid values: ACTIVE, INACTIVE. Defaults to 'ACTIVE'.
        Set to None or empty string to search all states.
    category (optional): Filter by finding category (e.g., 'PUBLIC_BUCKET_ACL', 'XSS', 'SQL_INJECTION',
        'OPEN_FIREWALL', 'MFA_NOT_ENFORCED', etc.).
    resource_name (optional): Filter by the full resource name associated with the finding.
    resource_type (optional): Filter by resource type (e.g., 'google.compute.Instance', 'google.storage.Bucket').
    mute (optional): Filter by mute status. Valid values: MUTED, UNMUTED, UNDEFINED.
    custom_filter (optional): A raw SCC filter string that will be appended to any other filters using AND.
        Use this for advanced filtering not covered by other parameters.
    max_findings (optional): Maximum number of findings to return. Defaults to 50.
    location (optional): The Google Cloud location for SCC v2 (e.g., 'global', 'us-central1'). Defaults to 'global'.
    order_by (optional): Ordering of results. Defaults to 'event_time desc'. Other options include
        'severity desc', 'create_time desc'.
    """
    if not scc_client:
        return {"error": "Security Center Client not initialized."}

    # Build filter string from parameters
    filter_parts = []

    if state:
        filter_parts.append(f'state="{state}"')

    if finding_class:
        # Support multiple classes with OR
        if " OR " in finding_class.upper():
            classes = [c.strip() for c in finding_class.upper().split(" OR ")]
            class_filter = " OR ".join([f'findingClass="{c}"' for c in classes])
            filter_parts.append(f"({class_filter})")
        else:
            filter_parts.append(f'findingClass="{finding_class.upper()}"')

    if severity:
        # Support multiple severities with OR
        if " OR " in severity.upper():
            sevs = [s.strip() for s in severity.upper().split(" OR ")]
            sev_filter = " OR ".join([f'severity="{s}"' for s in sevs])
            filter_parts.append(f"({sev_filter})")
        else:
            filter_parts.append(f'severity="{severity.upper()}"')

    if category:
        filter_parts.append(f'category="{category}"')

    if resource_name:
        filter_parts.append(f'resourceName="{resource_name}"')

    if resource_type:
        filter_parts.append(f'resource.type="{resource_type}"')

    if mute:
        filter_parts.append(f'mute="{mute.upper()}"')

    if custom_filter:
        filter_parts.append(custom_filter)

    filter_str = " AND ".join(filter_parts) if filter_parts else ""

    # SCC v2: parent must include /locations/{location}
    parent = f"projects/{project_id}/sources/-/locations/{location}"

    logger.info(f"Searching findings for project: {project_id}, filter: {filter_str}")

    try:
        request_args = {
            "parent": parent,
            "filter": filter_str,
            "page_size": min(max_findings, 1000),
            "order_by": order_by,
        }

        response_pager = scc_client.list_findings(request=request_args)

        all_findings = []
        count = 0
        for page in response_pager.pages:
            for item in page.list_findings_results:
                if count >= max_findings:
                    break
                finding_dict = proto_message_to_dict(item.finding)
                all_findings.append(finding_dict)
                count += 1
            if count >= max_findings:
                break

        # Check if more findings exist
        more_findings_exist = count >= max_findings

        return {
            "findings": all_findings,
            "count": len(all_findings),
            "filter_applied": filter_str if filter_str else "No filter (all findings)",
            "more_findings_may_exist": more_findings_exist,
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Project or resource not found for search on {parent}: {e}")
        return {"error": "Not Found", "details": f"Could not find project '{project_id}' or relevant resources. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied for search on {parent}: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument (check filter syntax?) for search on {parent}: {e}")
        return {"error": "Invalid Argument", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred searching findings: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_finding_details(
    project_id: str,
    finding_id: str,
    location: str = "global",
    include_resource_details: bool = True,
) -> Dict[str, Any]:
    """Name: get_finding_details

    Description: Gets the full details of a specific finding by its finding ID, including description,
                 remediation steps, severity, attack exposure, compliance information, MITRE ATT&CK data,
                 vulnerability details, and optionally the affected resource details from Cloud Asset
                 Inventory (CAI). Works for any finding class (VULNERABILITY, THREAT, MISCONFIGURATION, etc.).
    Parameters:
    project_id (required): The Google Cloud project ID (e.g., 'my-gcp-project').
    finding_id (required): The ID of the finding to retrieve.
    location (optional): The Google Cloud location for SCC v2 (e.g., 'global', 'us-central1'). Defaults to 'global'.
    include_resource_details (optional): Whether to fetch additional resource details from Cloud Asset
        Inventory. Defaults to True.
    """
    if not scc_client:
        return {"error": "Security Center Client not initialized."}

    parent = f"projects/{project_id}/sources/-/locations/{location}"
    finding_name_filter = f"projects/{project_id}/sources/-/locations/{location}/findings/{finding_id}"
    filter_str = f'name="{finding_name_filter}"'

    logger.info(f"Getting details for finding {finding_id} in project {project_id}")

    try:
        scc_request_args = {
            "parent": parent,
            "filter": filter_str,
            "page_size": 1,
        }

        response_pager = scc_client.list_findings(request=scc_request_args)
        first_finding = None
        page = next(iter(response_pager.pages), None)
        if page and page.list_findings_results:
            results = list(page.list_findings_results)
            if results:
                first_finding = results[0].finding

        if not first_finding:
            return {"error": "Finding not found", "details": f"No finding with ID '{finding_id}' found in project '{project_id}'."}

        finding_dict = proto_message_to_dict(first_finding)

        result = {
            "finding": finding_dict,
            "finding_id": finding_id,
        }

        # Optionally fetch resource details from CAI
        resource_name_from_finding = finding_dict.get("resourceName")
        if include_resource_details and resource_name_from_finding and cai_client:
            try:
                cai_scope = f"projects/{project_id}"
                cai_request = asset_v1.SearchAllResourcesRequest(
                    scope=cai_scope,
                    query=f'name="{resource_name_from_finding}"',
                    page_size=1,
                )
                cai_response = cai_client.search_all_resources(request=cai_request)
                asset_result = next(iter(cai_response), None)
                if asset_result:
                    result["resource_details_cai"] = proto_message_to_dict(asset_result)
                    logger.info(f"Successfully fetched CAI details for {resource_name_from_finding}")
                else:
                    result["resource_details_cai"] = {"warning": "Resource not found in CAI.", "resource_name": resource_name_from_finding}
            except Exception as cai_e:
                logger.error(f"Error fetching CAI details: {cai_e}")
                result["resource_details_cai"] = {"error": "Failed to fetch resource details from CAI.", "details": str(cai_e)}
        elif include_resource_details and not cai_client:
            result["resource_details_cai"] = {"error": "Cloud Asset Inventory Client not initialized."}

        return result

    except google_exceptions.NotFound as e:
        logger.error(f"Resource not found: {e}")
        return {"error": "Not Found", "details": str(e)}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument: {e}")
        return {"error": "Invalid Argument", "details": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error getting finding details: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def search_findings_by_compliance(
    project_id: str,
    search_text: str = None,
    compliance_standard: str = None,
    compliance_version: str = None,
    compliance_id: str = None,
    severity: str = None,
    state: str = "ACTIVE",
    max_findings: int = 50,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: search_findings_by_compliance

    Description: Searches Security Command Center findings by compliance framework information (e.g., CIS benchmarks,
                 PCI DSS, NIST 800-53, ISO 27001) or by free-text search on finding descriptions and categories.
                 Use this tool when you have a compliance control name or description (e.g.,
                 'ServiceAccount should not have Admin privileges', 'Ensure log metric filter and alerts exist')
                 and want to find the corresponding SCC findings. Also supports filtering by specific compliance
                 standard name, version, and control ID.
    Parameters:
    project_id (required): The Google Cloud project ID (e.g., 'my-gcp-project').
    search_text (optional): Free-text to search across finding descriptions, categories, and compliance standard names.
        Matches if any of these fields contain the search text (case-insensitive). Examples:
        'ServiceAccount should not have Admin privileges', 'log metric filter', 'MFA', 'firewall'.
    compliance_standard (optional): Filter by compliance standard name (case-insensitive partial match).
        Examples: 'CIS', 'CIS Google Cloud Platform', 'PCI DSS', 'NIST 800-53', 'ISO 27001'.
    compliance_version (optional): Filter by compliance standard version (exact match). Examples: '1.3.0', '2.0'.
    compliance_id (optional): Filter by compliance control ID (exact match). Examples: '1.5', '4.1', '6.2.1'.
    severity (optional): Pre-filter by severity at the API level. Valid values: CRITICAL, HIGH, MEDIUM, LOW.
        Supports OR (e.g., 'HIGH OR CRITICAL').
    state (optional): Filter by state. Valid values: ACTIVE, INACTIVE. Defaults to 'ACTIVE'.
        Set to None or empty string to search all states.
    max_findings (optional): Maximum number of matching findings to return. Defaults to 50.
    location (optional): The Google Cloud location for SCC v2. Defaults to 'global'.
    """
    if not scc_client:
        return {"error": "Security Center Client not initialized."}

    if not search_text and not compliance_standard and not compliance_id:
        return {
            "error": "Missing parameters",
            "details": "At least one of search_text, compliance_standard, or compliance_id must be provided.",
        }

    # Build API-level filter (for fields the API supports filtering on)
    filter_parts = []

    if state:
        filter_parts.append(f'state="{state}"')

    if severity:
        if " OR " in severity.upper():
            sevs = [s.strip() for s in severity.upper().split(" OR ")]
            sev_filter = " OR ".join([f'severity="{s}"' for s in sevs])
            filter_parts.append(f"({sev_filter})")
        else:
            filter_parts.append(f'severity="{severity.upper()}"')

    filter_str = " AND ".join(filter_parts) if filter_parts else ""

    parent = f"projects/{project_id}/sources/-/locations/{location}"

    logger.info(
        f"Searching findings by compliance for project: {project_id}, "
        f"search_text='{search_text}', standard='{compliance_standard}', "
        f"version='{compliance_version}', id='{compliance_id}'"
    )

    try:
        # Fetch findings from the API (with API-level filters only)
        # We fetch more than max_findings because client-side filtering will reduce the count
        fetch_limit = max_findings * 10  # Overfetch to account for client-side filtering
        request_args = {
            "parent": parent,
            "filter": filter_str,
            "page_size": min(fetch_limit, 1000),
        }

        response_pager = scc_client.list_findings(request=request_args)

        matched_findings = []
        scanned_count = 0
        search_text_lower = search_text.lower() if search_text else None

        for page in response_pager.pages:
            for item in page.list_findings_results:
                if len(matched_findings) >= max_findings:
                    break
                if scanned_count >= fetch_limit:
                    break

                scanned_count += 1
                finding_dict = proto_message_to_dict(item.finding)

                # --- Client-side compliance filtering ---
                compliances = finding_dict.get("compliances", [])
                description = finding_dict.get("description", "")
                category = finding_dict.get("category", "")

                # Check compliance_standard filter
                if compliance_standard:
                    standard_lower = compliance_standard.lower()
                    has_standard = any(
                        standard_lower in c.get("standard", "").lower()
                        for c in compliances
                    )
                    if not has_standard:
                        continue

                # Check compliance_version filter
                if compliance_version:
                    has_version = any(
                        c.get("version") == compliance_version
                        for c in compliances
                    )
                    if not has_version:
                        continue

                # Check compliance_id filter
                if compliance_id:
                    has_id = any(
                        compliance_id in c.get("ids", [])
                        for c in compliances
                    )
                    if not has_id:
                        continue

                # Check search_text filter (matches description, category, or compliance standard names)
                if search_text_lower:
                    text_match = (
                        search_text_lower in description.lower()
                        or search_text_lower in category.lower()
                        or any(
                            search_text_lower in c.get("standard", "").lower()
                            for c in compliances
                        )
                    )
                    if not text_match:
                        continue

                # Finding passed all filters — enrich with compliance summary
                compliance_summary = []
                for c in compliances:
                    comp_entry = {
                        "standard": c.get("standard"),
                        "version": c.get("version"),
                        "ids": c.get("ids", []),
                    }
                    compliance_summary.append(comp_entry)

                finding_dict["compliance_summary"] = compliance_summary
                matched_findings.append(finding_dict)

            if len(matched_findings) >= max_findings or scanned_count >= fetch_limit:
                break

        return {
            "findings": matched_findings,
            "count": len(matched_findings),
            "scanned_count": scanned_count,
            "filters_applied": {
                "search_text": search_text,
                "compliance_standard": compliance_standard,
                "compliance_version": compliance_version,
                "compliance_id": compliance_id,
                "severity": severity,
                "state": state,
            },
            "more_findings_may_exist": scanned_count >= fetch_limit and len(matched_findings) >= max_findings,
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Project not found for compliance search on {parent}: {e}")
        return {"error": "Not Found", "details": f"Could not find project '{project_id}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied for compliance search on {parent}: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument for compliance search on {parent}: {e}")
        return {"error": "Invalid Argument", "details": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in compliance search: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def top_vulnerability_findings(
    project_id: str,
    max_findings: int = 20,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: top_vulnerability_findings

    Description: Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project,
                 sorted by Attack Exposure Score (descending). Includes the Attack Exposure score in the output if available.
                 Aids prioritization for remediation.
    Parameters:
    project_id (required): The Google Cloud project ID (e.g., 'my-gcp-project').
    max_findings (optional): The maximum number of findings to return. Defaults to 20.
    location (optional): The Google Cloud location for SCC v2 (e.g., 'global', 'us-central1'). Defaults to 'global'.
    """
    if not scc_client:
        return {"error": "Security Center Client not initialized."}

    # SCC v2: parent must include /locations/{location}
    parent = f"projects/{project_id}/sources/-/locations/{location}"
    # Filter for active, high/critical vulnerability findings
    filter_str = 'state="ACTIVE" AND findingClass="VULNERABILITY" AND (severity="HIGH" OR severity="CRITICAL")'

    # Define a larger page size to fetch enough findings for sorting
    fetch_page_size = 20 # Fetch up to 20 findings initially

    logger.info(f"Getting top vulnerability findings for project: {project_id}")
    logger.debug(f"Using parent: {parent}, filter: {filter_str}, fetching up to {fetch_page_size} findings for sorting.")

    try:
        request_args = {
            "parent": parent,
            "filter": filter_str,
            "page_size": fetch_page_size, # Use the larger fetch size here
        }

        response_pager = scc_client.list_findings(request=request_args)

        all_fetched_findings = []
        # Iterate through the first page (up to fetch_page_size)
        page = next(iter(response_pager.pages), None)
        if page:
            for item in page.list_findings_results:
                finding_dict = proto_message_to_dict(item.finding)
                # SCC v2: attackExposure is a nested message { score: float, ... }
                attack_exposure_score = finding_dict.get("attackExposure", {}).get("score")

                finding_summary = {
                    "name": finding_dict.get("name"),
                    "category": finding_dict.get("category"),
                    "resourceName": finding_dict.get("resourceName"),
                    "severity": finding_dict.get("severity"),
                    "description": finding_dict.get("description", "No description provided."),
                    "attackExposureScore": attack_exposure_score, # Include score
                }
                all_fetched_findings.append(finding_summary)

        # Sort the findings: Attack Exposure Score (desc)
        # Treat None scores as lowest (-1.0)
        def sort_key(f):
            # Prioritize Attack Exposure Score (higher is worse)
            # Treat None as -1.0 for sorting purposes to put them last in descending order
            aes = f.get("attackExposureScore", -1.0)
            # Handle potential non-numeric values if they can occur
            aes = float(aes) if aes is not None else -1.0
            # Sort ONLY by Attack Exposure Score
            return aes # Return only AES for sorting

        all_fetched_findings.sort(key=sort_key, reverse=True) # Sort descending by AES

        # Limit results to max_findings
        # Ensure max_findings is not None and is positive before slicing
        final_max_findings = max_findings if max_findings is not None and max_findings > 0 else 20
        sorted_findings = all_fetched_findings[:final_max_findings]

        # Determine if more findings *might* exist beyond the initial fetch_page_size
        more_findings_exist = bool(response_pager.next_page_token) or len(all_fetched_findings) == fetch_page_size

        return {
            "top_findings": sorted_findings, # Return the sorted and limited list
            "count": len(sorted_findings),
             # Indicate if there might be more findings beyond the *initial fetch* limit
            "more_findings_exist_beyond_fetch_limit": more_findings_exist
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Project or resource not found for top findings on {parent}: {e}")
        return {"error": "Not Found", "details": f"Could not find project '{project_id}' or relevant resources. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied for top findings on {parent}: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.InvalidArgument as e:
        # Catch potential filter syntax errors
        logger.error(f"Invalid argument (check filter syntax?) for top findings on {parent}: {e}")
        return {"error": "Invalid Argument", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred getting top findings: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}

@mcp.tool()
async def get_finding_remediation(
    project_id: str,
    resource_name: str = None,
    category: str = None,
    finding_id: str = None,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_finding_remediation

    Description: Gets the remediation steps (nextSteps) for a specific finding within a project,
                 along with details of the affected resource fetched from Cloud Asset Inventory (CAI).
                 The finding can be identified either by its resource_name and category (for ACTIVE findings)
                 or directly by its finding_id (regardless of state).
    Parameters:
    project_id (required): The Google Cloud project ID (e.g., 'my-gcp-project').
    resource_name (optional): The full resource name associated with the finding.
        (e.g., '//container.googleapis.com/projects/my-project/locations/us-central1/clusters/my-cluster')
    category (optional): The category of the finding (e.g., 'GKE_SECURITY_BULLETIN').
    finding_id (optional): The ID of the finding to search for directly.
    location (optional): The Google Cloud location for SCC v2 (e.g., 'global', 'us-central1'). Defaults to 'global'.
    """
    if not scc_client:
        return {"error": "Security Center Client not initialized."}
    # Also check CAI client
    if not cai_client:
        return {"error": "Cloud Asset Inventory Client not initialized."}

    # Input validation
    if not resource_name and not category and not finding_id:
        return {"error": "Missing required parameters", "details": "Either resource_name and category or finding_id must be provided."}

    first_finding_result = None
    scc_error = None
    # SCC v2: parent must include /locations/{location}
    parent = f"projects/{project_id}/sources/-/locations/{location}"
    filter_str = "" # Initialize filter string

    try:
        if finding_id:
            # --- Use list_findings with name filter for finding_id (SCC v2 Client) ---
            # v2 finding names include /locations/{location}/
            finding_name_to_filter = f"projects/{project_id}/sources/-/locations/{location}/findings/{finding_id}"
            filter_str = f'name="{finding_name_to_filter}"'
            logger.info(f"Attempting to list findings by name filter: {filter_str}")
            scc_request_args = {
                "parent": parent,
                "filter": filter_str,
                "page_size": 1, # Expecting only one result for a unique name
            }
        elif resource_name and category:
            # --- Use list_findings for resource/category --- 
            filter_str = f'state="ACTIVE" AND resourceName="{resource_name}" AND category="{category}"'
            logger.info(f"Attempting to list active findings for resource: {resource_name}, category: {category}")
            scc_request_args = {
                "parent": parent,
                "filter": filter_str,
                "page_size": 2, # Fetch 2 to detect multiple matches
            }
        else:
             # This case should be caught by initial validation, but safety check.
             return {"error": "Invalid Arguments", "details": "No valid criteria provided."}

        # --- Perform the list_findings call --- 
        logger.debug(f"Executing list_findings with parent='{parent}', filter='{filter_str}', page_size={scc_request_args['page_size']}")
        scc_response_pager = scc_client.list_findings(request=scc_request_args)
        
        results = []
        page = next(iter(scc_response_pager.pages), None)
        if page and page.list_findings_results:
            results = list(page.list_findings_results)
        
        # --- Process results --- 
        if len(results) >= 1:
            if len(results) > 1 and resource_name: # Warning only needed for resource/category search
                 logger.warning(f"Multiple ({len(results)}) ACTIVE findings found for resource '{resource_name}' and category '{category}'. Using the first one.")
            first_finding_result = results[0].finding
            logger.info(f"Successfully retrieved finding matching criteria.")
        else:
             # Logged later in the 'if first_finding_result:' block
             first_finding_result = None

        # --- Process the found finding (if any) --- 
        if first_finding_result:
            finding_dict = proto_message_to_dict(first_finding_result)
            remediation_steps = finding_dict.get("nextSteps", "No remediation steps provided for this finding.")
            finding_name = finding_dict.get('name')
            description = finding_dict.get("description", "No description available.")
            resource_name_from_finding = finding_dict.get("resourceName")

            logger.info(f"Processing finding {finding_name}. Fetching CAI details...")
            asset_details = None
            if resource_name_from_finding:
                 try:
                     cai_scope = f"projects/{project_id}"
                     cai_request = asset_v1.SearchAllResourcesRequest(
                         scope=cai_scope,
                         query=f'name="{resource_name_from_finding}"',
                         page_size=1,
                     )
                     logger.debug(f"Attempting CAI search with request: {{scope='{cai_scope}', query='{cai_request.query}', page_size=1}}")
                     cai_response = cai_client.search_all_resources(request=cai_request)
                     asset_result = next(iter(cai_response), None)
                     if asset_result:
                         asset_details = proto_message_to_dict(asset_result)
                         logger.info(f"Successfully fetched CAI details for {resource_name_from_finding}")
                     else:
                         logger.warning(f"Could not find asset details in CAI for resource: {resource_name_from_finding} within scope {cai_scope}")
                         asset_details = {"error": "Resource details not found in CAI.", "resource_name": resource_name_from_finding}
                 except google_exceptions.PermissionDenied as cai_e:
                     logger.error(f"Permission denied fetching CAI details for {resource_name_from_finding}: {cai_e}")
                     asset_details = {"error": "Permission Denied fetching resource details from CAI.", "details": str(cai_e)}
                 except google_exceptions.InvalidArgument as cai_e:
                     logger.error(f"Invalid argument fetching CAI details for {resource_name_from_finding}: {cai_e}")
                     asset_details = {"error": "Invalid Argument fetching resource details from CAI.", "details": str(cai_e)}
                 except Exception as cai_e:
                     logger.error(f"An unexpected error occurred fetching CAI details for {resource_name_from_finding}: {cai_e}", exc_info=True)
                     asset_details = {"error": "An unexpected error occurred fetching resource details from CAI.", "details": str(cai_e)}
            else:
                 logger.warning(f"Finding {finding_name} does not have a resourceName, cannot fetch CAI details.")
                 asset_details = {"warning": "Finding does not have an associated resource name."}
            
            return {
                "remediation_steps": remediation_steps,
                "finding_name": finding_name,
                "description": description,
                "resource_name": resource_name_from_finding,
                "resource_details_cai": asset_details,
                "finding_details": finding_dict
            }
        else:
            # --- Handle case where no finding was found --- 
            search_criteria = f"finding ID '{finding_id}' (using name filter)" if finding_id else f"active finding for resource '{resource_name}' and category '{category}'"
            logger.warning(f"No finding found matching {search_criteria} in project '{project_id}'. Filter: {filter_str}")
            return {"message": f"No finding found matching the specified criteria ({search_criteria})."}

    # --- Outer Exception Handling --- 
    except google_exceptions.NotFound as e:
        logger.error(f"Resource not found during SCC operation for project {project_id} (finding_id: {finding_id}, resource: {resource_name}): {e}")
        return {"error": "Not Found", "details": f"Could not find project '{project_id}' or related SCC resources. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied during SCC operation for project {project_id} (finding_id: {finding_id}, resource: {resource_name}): {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument during SCC operation for project {project_id} (finding_id: {finding_id}, resource: {resource_name}): {e}")
        return {"error": "Invalid Argument", "details": f"Check SCC filter syntax or input parameters. {str(e)}"}
    except Exception as e:
        # General fallback, including potential CAI client errors not caught inside
        logger.error(f"An unexpected error occurred in get_finding_remediation: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}

# --- Main execution ---

def main() -> None:
  """Runs the FastMCP server."""
  if not scc_client:
    logger.critical("SCC Client failed to initialize. MCP server cannot serve SCC tools.")

  logger.info("Starting SCC MCP server...")

  mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
