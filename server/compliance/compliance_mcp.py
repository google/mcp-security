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
        request_args = {
            "parent": parent,
            "page_size": page_size,
        }

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

# --- Main execution ---

def main() -> None:
  """Runs the FastMCP server."""
  if not config_client:
    logger.critical("Cloud Security Compliance Config Client failed to initialize. MCP server cannot serve compliance tools.")

  logger.info("Starting Cloud Security Compliance MCP server...")

  mcp.run(transport="stdio")

if __name__ == "__main__":
    main() 