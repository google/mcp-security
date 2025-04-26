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
from typing import Any, Dict

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
