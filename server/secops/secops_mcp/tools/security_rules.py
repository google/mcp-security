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

from secops_mcp.server import server, get_chronicle_client

# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def list_security_rules(
    project_id: Optional[str] = None, 
    customer_id: Optional[str] = None, 
    region: Optional[str] = None
) -> Dict[str, Any]:
    """List security detection rules from Chronicle.

    Args:
        project_id: Google Cloud project ID (defaults to config)
        customer_id: Chronicle customer ID (defaults to config)
        region: Chronicle region (defaults to config)

    Returns:
        Raw response from the Chronicle API containing security detection rules
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)
        rules_response = chronicle.list_rules()
        return rules_response
    except Exception as e:
        logger.error(f'Error listing security rules: {str(e)}', exc_info=True)
        return {'error': str(e), 'rules': []} 