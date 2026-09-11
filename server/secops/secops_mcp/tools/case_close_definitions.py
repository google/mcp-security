# Copyright 2026 Google LLC
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
"""Security Operations MCP tools for case close definitions."""

import logging
from typing import Any, Dict, Optional

from secops.chronicle.case import APIVersion, chronicle_paginated_request

from secops_mcp.server import get_chronicle_client, server

logger = logging.getLogger("secops-mcp")


@server.tool()
async def list_case_close_definitions(
    page_size: int = 50,
    page_token: Optional[str] = None,
    filter: Optional[str] = None,
    order_by: Optional[str] = None,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """List case close definitions (root causes and close reasons) in Chronicle.

    Retrieves configured case close definitions which pair root causes with
    valid close reasons (e.g. MALICIOUS, NOT_MALICIOUS, MAINTENANCE, INCONCLUSIVE).
    This tool allows security analysts and automated workflows to discover the valid
    root causes required to close a case or alert.

    **Workflow Integration:**
    - Use prior to closing a case or alert to discover allowed root causes and close reasons
    - Discover tenant-specific root cause classifications and definitions
    - Filter definitions by reason or query string

    **Use Cases:**
    - "What are the allowed root causes for closing a case as MALICIOUS?"
    - "List all case close definitions"
    - "Find case close root causes for false positives"

    Args:
        page_size (int): Number of definitions to return per page. Defaults to 50.
        page_token (Optional[str]): Token for pagination.
        filter (Optional[str]): CEL or standard filter string to restrict definitions.
        order_by (Optional[str]): Field expression to order results.
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment config.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment config.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment config.

    Returns:
        Dict[str, Any]: Dictionary containing list of `caseCloseDefinitions` and pagination tokens,
            or an `error` message upon failure.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Listing case close definitions (page_size=%s)...", page_size)

        extra_params: Dict[str, Any] = {}
        if filter:
            extra_params["filter"] = filter
        if order_by:
            extra_params["orderBy"] = order_by

        result = chronicle_paginated_request(
            chronicle,
            path="caseCloseDefinitions",
            items_key="caseCloseDefinitions",
            api_version=APIVersion.V1,
            page_size=page_size,
            page_token=page_token,
            extra_params=extra_params if extra_params else None,
            as_list=False,
        )

        if isinstance(result, list):
            return {"caseCloseDefinitions": result}
        return result

    except Exception as e:
        error_msg = f"Error listing case close definitions: {e}"
        logger.error("Error listing case close definitions: %s", e)
        return {"error": error_msg}
