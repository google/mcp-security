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

from google.cloud import orgpolicy_v2
from google.api_core import exceptions as google_exceptions
from google.cloud.cloudsecuritycompliance_v1alpha.services.config import ConfigClient
from google.protobuf import json_format 
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("compliance-mcp")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("compliance-mcp")
logger.setLevel(logging.INFO)

# Add handler to see uvicorn/fastapi logs if they use standard logging
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

# --- Cloud Security Compliance Client Initialization ---
# The client automatically uses Application Default Credentials (ADC).
# Ensure ADC are configured in the environment where the server runs
# (e.g., by running `gcloud auth application-default login`).
try:
    config_client = ConfigClient()
    logger.info("Successfully initialized Google Cloud Security Compliance Config Client.")
except Exception as e:
    logger.error(f"Failed to initialize Cloud Security Compliance Config Client: {e}", exc_info=True)
    config_client = None

# --- Org Policy Client Initialization ---
# The client automatically uses Application Default Credentials (ADC).
# Ensure ADC are configured in the environment where the server runs
# (e.g., by running `gcloud auth application-default login`).
try:
    orgpolicy_client = orgpolicy_v2.OrgPolicyClient()
    logger.info("Successfully initialized Org Policy Client.")
except Exception as e:
    logger.error(f"Failed to initialize Org Policy Client: {e}", exc_info=True)
    orgpolicy_client = None # Indicate client is not available

# --- Helper Function for Proto to Dict Conversion ---

def proto_message_to_dict(message: Any) -> Dict[str, Any]:
    """Converts a protobuf message to a dictionary."""
    try:
        return json_format.MessageToDict(message._pb)
    except Exception as e:
        logger.error(f"Error converting protobuf message to dict: {e}")
        # Fallback or re-raise depending on desired error handling
        return {"error": "Failed to serialize response part", "details": str(e)}


# --- Cloud Security Compliance Tools ---

# --- List Frameworks tool ---
@mcp.tool()
async def list_frameworks(
    parent: str,
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_frameworks

    Description: Lists available compliance frameworks for a given parent resource (organization, folder, or project).
                 Returns information about available compliance frameworks and their details.
    Parameters:
    parent (required): The parent resource name (e.g., 'organizations/123456', 'folders/123456', or 'projects/my-project').
    page_size (optional): The maximum number of frameworks to return. Defaults to 50.
    """
    if not config_client:
        return {"error": "Cloud Security Compliance Config Client not initialized."}

    logger.info(f"Listing frameworks for parent: {parent}")

    try:
        # Append "/locations/global" to parent as required by the API
        request_args = {
            "parent": f"{parent}/locations/global",
            "page_size": page_size,
        }
        logger.info(f"Request args for list_frameworks: {request_args}")
        

        response_pager = config_client.list_frameworks(request=request_args)

        all_frameworks = []
        # Iterate through the first page
        page = next(iter(response_pager.pages), None)
        if page:
            for framework in page.frameworks:
                framework_dict = proto_message_to_dict(framework)
                
                framework_summary = {
                    "name": framework_dict.get("name"),
                    "displayName": framework_dict.get("displayName"),
                    "description": framework_dict.get("description"),
                    "category": framework_dict.get("category"),
                    "state": framework_dict.get("state"),
                    "createTime": framework_dict.get("createTime"),
                    "updateTime": framework_dict.get("updateTime"),
                    "version": framework_dict.get("version"),
                }
                all_frameworks.append(framework_summary)

        # Check if more frameworks exist
        more_frameworks_exist = bool(response_pager.next_page_token)

        return {
            "frameworks": all_frameworks,
            "count": len(all_frameworks),
            "more_frameworks_exist": more_frameworks_exist
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource not found: {parent}: {e}")
        return {"error": "Not Found", "details": f"Could not find parent resource '{parent}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied for listing frameworks on {parent}: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument for listing frameworks on {parent}: {e}")
        return {"error": "Invalid Argument", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred listing frameworks: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}

# --- List Constraints tool ---
@mcp.tool()
async def list_constraints(
    parent: str
) -> Dict[str, str]:
    """Name: list all available constraints
    Description: Returns details of all available Org Policy constraints for a given resource:[organization/project/folder].
    Parameters:
    parent (required): The Google Cloud resource that parents the constraint. Must be in one of the following forms:
     * `projects/{project_number}`
     * `projects/{project_id}`
     * `folders/{folder_id}`
     * `organizations/{organization_id}`
    """
    if not orgpolicy_client:
        return {"error": "Org Polciy Client not initialized."}

    logger.info(f"getting all constraints for parent: {parent}")

    try:

        constraints_iter = orgpolicy_client.list_constraints(request={"parent": parent})
        constraints_map = {}

        for constraint in constraints_iter:
            # Each constraint has .name, .display_name, .description, etc.
            constraints_map[constraint.name] = {
                "display_name": constraint.display_name,
                "description": constraint.description
            }

        return constraints_map

    except Exception as e:
        logger.error(f"Error listing constraints for {parent}: {e}", exc_info=True)
        return {"error": str(e)}
    

# --- List Active Policies tool ---
@mcp.tool()
async def list_active_policies(
    parent: str
) -> Dict[str, Any]:
    """Name: list active/enforced policy details
    Description: Returns details of all active/enforced Org Policy policies for a given resource:[organization/project/folder].
    Parameters:
    parent (required): The Google Cloud resource that parents the policies. Must be in one of the following forms:
     * `projects/{project_number}`
     * `projects/{project_id}`
     * `folders/{folder_id}`
     * `organizations/{organization_id}`
    """
    if not orgpolicy_client:
        return {"error": "Org Polciy Client not initialized."}

    logger.info(f"getting all active policies for parent: {parent}")

    try:
        # Step 1: Fetch all policies and filter for enforced ones
        policies = orgpolicy_client.list_policies(request={"parent": parent})
        active_policies_constraint_id_set = set()

        for policy in policies:
            rules = getattr(policy.spec, "rules", []) if policy.spec else []
            is_enforced = any(getattr(rule, "enforce", False) for rule in rules)
            if is_enforced:
                policy_name = policy.name
                # Extract constraint_id from policy_name
                # Example: "projects/{project_number}/policies/{constraint_id}"
                if "/policies/" in policy_name:
                    constraint_id = policy_name.split("/policies/")[-1]
                    active_policies_constraint_id_set.add(constraint_id)
                else:
                    continue

        # Step 2: Fetch all constraints for the parent
        constraints = orgpolicy_client.list_constraints(request={"parent": parent})
        constraint_desc_map = {}
        for constraint in constraints:
            # constraint.name is like "projects/123/constraints/serviceuser.services"
            # We want to map by just the constraint_name part
            constraint_id = constraint.name.split("/constraints/")[-1]
            if constraint_id in active_policies_constraint_id_set:
                constraint_desc_map[constraint_id] = {
                    "description": constraint.description,
                    "display_name": constraint.display_name}

        return constraint_desc_map

    except Exception as e:
        logger.error(f"Error listing active policies for {parent}: {e}", exc_info=True)
        return {"error": str(e)}


# --- Main execution ---

def main() -> None:
  """Runs the FastMCP server."""
  if not config_client:
    logger.critical("Cloud Security Compliance Config Client failed to initialize. MCP server cannot serve compliance tools.")

  logger.info("Starting Cloud Security Compliance MCP server...")

  mcp.run(transport="stdio")

if __name__ == "__main__":
    main() 