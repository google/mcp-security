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
"""Security Operations MCP tools for threat intelligence."""

import logging
from typing import Optional

from secops_mcp.server import server, get_chronicle_client

# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def get_threat_intel(
    query: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    region: Optional[str] = None,
) -> str:
    """Get answers to general security domain questions. Additionally, tool can answer specific threat intelligence questions and provide summaries about threat actors, IOCs, CVEs, and other threat intelligence topics.

    Args:
        query: The security or threat intelligence question
        project_id: Google Cloud project ID (defaults to config)
        customer_id: Chronicle customer ID (defaults to config)
        region: Chronicle region (defaults to config)

    Returns:
        Formatted answer from the Gemini model
    """
    try:
        logger.info(f'Getting threat intelligence for query: {query}')
        
        chronicle = get_chronicle_client(project_id, customer_id, region)
        
        # Call the Gemini method from the SecOps SDK
        response = chronicle.gemini(query)
        
        # Handle GeminiResponse object
        if hasattr(response, 'get_text_content'):
            # This is a GeminiResponse object, extract text content
            return response.get_text_content()
        elif hasattr(response, 'blocks') and isinstance(response.blocks, list):
            # Handle direct access to blocks if get_text_content isn't available
            text_content = []
            for block in response.blocks:
                if hasattr(block, 'block_type') and hasattr(block, 'content'):
                    if block.block_type == "TEXT":
                        text_content.append(block.content)
            return "\n\n".join(text_content) if text_content else "No text content found in response."
        elif isinstance(response, dict) and 'answer' in response:
            # Legacy format or different API response
            return response.get('answer', 'No answer was provided by the model.')
        elif isinstance(response, str):
            # Direct string response
            return response
        else:
            # If response is in an unexpected format, try to convert it to string
            return str(response)
            
    except Exception as e:
        logger.error(f'Error getting threat intelligence: {str(e)}', exc_info=True)
        return f'Error retrieving threat intelligence: {str(e)}' 