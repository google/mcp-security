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

import logging
from datetime import datetime, timedelta, timezone

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def get_ioc_matches(
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    max_matches: int = 20,
    region: str = None,
) -> str:
    """Get Indicators of Compromise (IoCs) matches from Chronicle SIEM.

    Retrieves IoCs (e.g., malicious IPs, domains, hashes) from configured threat
    intelligence feeds that have been observed matching events in Chronicle logs
    within the specified time window.

    **Workflow Integration:**
    - Use this to proactively identify potential threats based on IoC matches within SIEM data,
      potentially before specific detection rules trigger or cases are created in other systems.
    - Can provide early warning signs or context during investigations initiated from alerts
      or intelligence originating from any connected security tool (SIEM, EDR, TI platforms, etc.).
    - Complements rule-based alerts by showing matches against known bad indicators from
      threat intelligence feeds integrated with the SIEM.

    **Use Cases:**
    - Monitor for recent sightings of known malicious indicators within SIEM logs.
    - Identify assets that may have interacted with known bad infrastructure or files, based on log evidence.
    - Supplement investigations by checking if involved entities match known IoCs curated by threat intelligence sources.

    Args:
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        hours_back (int): How many hours back to look for IoC matches. Defaults to 24.
        max_matches (int): Maximum number of IoC matches to return. Defaults to 20.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        str: A formatted string summarizing the IoC matches found, including the IoC type,
             value, and the threat intelligence sources that identified it. Returns
             'No IoC matches found...' if none are found in the time range.

    Next Steps (using MCP-enabled tools):
        - Investigate the assets or events associated with the matched IoCs.
        - Use entity lookup tools to get broader context on the matched IoC value (IP, domain, hash).
        - Use SIEM event search tools to find the specific events in logs that triggered the IoC match.
        - Check if related cases exist in your case management/SOAR system or create one if the match indicates a significant threat.
        - Correlate IoC match details with findings from other security tools (EDR, Network, Cloud) via their MCP tools.
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
