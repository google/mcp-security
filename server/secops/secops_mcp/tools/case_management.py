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
"""Security Operations MCP tools for case management."""

import logging
from typing import Any, Dict, Optional

from secops.chronicle.client import APIVersion
from secops.chronicle.utils.request_utils import chronicle_request
from secops_mcp.server import get_chronicle_client, server

# Configure logging
logger = logging.getLogger("secops-mcp")


@server.tool()
async def create_case(
    case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Ingest a package of cases and alerts into Chronicle SIEM.

    Ingests a package of cases and alerts into the data processing engine
    for bulk-loading security alerts and event data using legacyCases:createCase
    (v1alpha API).

    **Workflow Integration:**
    - Use for ingesting bulk packages of cases and security alerts into Chronicle.
    - Essential for automated alert ingestion pipelines and migration workflows.

    **Use Cases:**
    - "Ingest a package of cases and alerts into Chronicle"
    - "Bulk load security alerts and event data"

    Args:
        case_data (Dict[str, Any]): Dictionary payload containing case and alert details.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary response from Chronicle API, or an error dictionary.
    """
    try:
        if not case_data:
            return {"error": "case_data parameter is required and cannot be empty"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Ingesting case package via legacyCases:createCase")

        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:createCase",
            api_version=APIVersion.V1ALPHA,
            json=case_data,
            error_message="Failed to create case package",
        )
    except Exception as e:
        error_msg = f"Error creating case package: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def create_manual_case(
    case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Programmatically create a manual case in Chronicle SIEM.

    Creates a manual case with custom case properties, priority, tags,
    and attached playbooks using legacyCases:createManualCase (v1alpha API).

    **Workflow Integration:**
    - Use when creating ad-hoc manual cases programmatically.
    - Enables custom case properties, tags, and playbook attachments.

    **Use Cases:**
    - "Create a manual case with priority and tags"
    - "Programmatically initiate an incident investigation case"

    Args:
        case_data (Dict[str, Any]): Dictionary payload containing case properties
            (e.g., custom case properties, priority, tags, playbooks).
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary response from Chronicle API, or an error dictionary.
    """
    try:
        if not case_data:
            return {"error": "case_data parameter is required and cannot be empty"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Creating manual case via legacyCases:createManualCase")

        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCases:createManualCase",
            api_version=APIVersion.V1ALPHA,
            json=case_data,
            error_message="Failed to create manual case",
        )
    except Exception as e:
        error_msg = f"Error creating manual case: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}


@server.tool()
async def create_or_update_case(
    case_data: Dict[str, Any],
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new case or update an existing case in Chronicle SIEM.

    Creates a new case or updates an existing case using legacy case schema
    payloads via legacyCreateOrUpdateCase (v1alpha API).

    **Workflow Integration:**
    - Use when upserting case data using legacy case schema payloads.
    - Useful for synchronizing case state across external platforms and Chronicle.

    **Use Cases:**
    - "Create or update a case using legacy case schema"
    - "Upsert incident case details in Chronicle"

    Args:
        case_data (Dict[str, Any]): Dictionary payload representing the legacy case schema.
        project_id (Optional[str]): Google Cloud project ID. Defaults to
            environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to
            environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").
            Defaults to environment configuration.

    Returns:
        Dict[str, Any]: Dictionary response from Chronicle API, or an error dictionary.
    """
    try:
        if not case_data:
            return {"error": "case_data parameter is required and cannot be empty"}

        chronicle = get_chronicle_client(project_id, customer_id, region)
        logger.info("Creating or updating case via legacyCreateOrUpdateCase")

        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path="legacyCreateOrUpdateCase",
            api_version=APIVersion.V1ALPHA,
            json=case_data,
            error_message="Failed to create or update case",
        )
    except Exception as e:
        error_msg = f"Error creating or updating case: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg}
