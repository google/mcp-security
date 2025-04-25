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
from google.cloud import securitycenter
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
    scc_client = securitycenter.SecurityCenterClient()
    logger.info("Successfully initialized Google Cloud Security Center Client.")
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
async def top_vulnerability_findings(
    project_id: str,
    max_findings: int = 20,
) -> Dict[str, Any]:
    """Name: top_vulnerability_findings

    Description: Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project,
                 sorted by Attack Exposure Score (descending). Includes the Attack Exposure score in the output if available.
                 Aids prioritization for remediation.
    Parameters:
    project_id (required): The Google Cloud project ID (e.g., 'my-gcp-project').
    max_findings (optional): The maximum number of findings to return. Defaults to 20.
    """
    if not scc_client:
        return {"error": "Security Center Client not initialized."}

    parent = f"projects/{project_id}/sources/-" # Search across all sources in the project
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
                # Extract scores, handling potential absence
                attack_exposure_score = finding_dict.get("attackExposureScore") # Directly under finding

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
    finding_id: str = None
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
    parent = f"projects/{project_id}/sources/-" # Define parent once
    filter_str = "" # Initialize filter string

    try:
        if finding_id:
            # --- Use list_findings with name filter for finding_id (V1 Client) --- 
            finding_name_to_filter = f"projects/{project_id}/sources/-/findings/{finding_id}"
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
