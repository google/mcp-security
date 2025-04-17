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
"""Security Operations MCP tools for IoC matches."""

from datetime import datetime, timedelta, timezone
import logging
from typing import Optional

from secops_mcp.server import server, get_chronicle_client

# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def get_ioc_matches(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    hours_back: int = 24,
    max_matches: int = 20,
    region: Optional[str] = None,
) -> str:
    """Get Indicators of Compromise (IoCs) matches from Chronicle.

    Args:
        project_id: Google Cloud project ID (defaults to config)
        customer_id: Chronicle customer ID (defaults to config)
        hours_back: How many hours to look back (default: 24)
        max_matches: Maximum number of matches to return (default: 20)
        region: Chronicle region (defaults to config)

    Returns:
        Formatted string with IoC matches
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours_back)

        iocs = chronicle.list_iocs(
            start_time=start_time, end_time=end_time, max_matches=max_matches
        )

        # Handle different possible response formats
        matches = []
        if isinstance(iocs, dict) and 'matches' in iocs:
            matches = iocs.get('matches', [])
        elif isinstance(iocs, list):
            matches = iocs

        if not matches:
            return 'No IoC matches found for the specified time range.'

        result = f'Found {len(matches)} IoC matches:\n\n'

        for i, match in enumerate(matches, 1):
            # Get the indicator information
            indicator_type = 'Unknown'
            indicator_value = 'Unknown'
            sources = []

            # Try to extract artifactIndicator differently based on response format
            if isinstance(match, dict):
                if 'artifactIndicator' in match and isinstance(
                    match['artifactIndicator'], dict
                ):
                    # Get the first key-value pair from artifactIndicator
                    indicator_dict = match.get('artifactIndicator', {})
                    if indicator_dict:
                        indicator_type = next(iter(indicator_dict.keys()), 'Unknown')
                        indicator_value = next(iter(indicator_dict.values()), 'Unknown')

                sources = match.get('sources', [])

            sources_str = ', '.join(sources) if sources else 'Unknown'

            result += f'IoC {i}:\n'
            result += f'Type: {indicator_type}\n'
            result += f'Value: {indicator_value}\n'
            result += f'Sources: {sources_str}\n\n'

        return result
    except Exception as e:
        return f'Error retrieving IoC matches: {str(e)}' 