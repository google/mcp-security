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
"""Security Operations MCP tools for searching security events."""

from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Dict, Optional

from secops_mcp.server import server, get_chronicle_client

# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def search_security_events(
    text: str,
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    hours_back: int = 24,
    max_events: int = 100,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """Search for security events in Chronicle using natural language.

    This function allows you to search for events using everyday language instead
    of requiring UDM query syntax. The natural language query will be automatically translated
    into a Chronicle UDM query for execution.

    Examples of natural language queries:
    - "Show me network connections from yesterday for the domain google.com"
    - "Display connections to IP address 192.168.1.100"

    When searching for email addresses, use only lowercase letters.

    Args:
        text: Natural language description of the events you want to find
        project_id: Google Cloud project ID (defaults to config)
        customer_id: Chronicle customer ID (defaults to config)
        hours_back: How many hours to look back (default: 24)
        max_events: Maximum number of events to return (default: 100)
        region: Chronicle region (defaults to config)

    Returns:
        Dictionary containing the UDM query and search results, including events
        and metadata.
    """
    try:
        logger.info(
            f'Searching security events with natural language query: {text}'
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours_back)

        logger.info(f'Search time range: {start_time} to {end_time}')

        # Use the new natural language search method
        udm_query = chronicle.translate_nl_to_udm(text)
        logger.info(f'YL2 UDM Query: {udm_query}')

        events = chronicle.search_udm(
            query=udm_query,
            start_time=start_time,
            end_time=end_time,
            max_events=max_events,
        )

        # For compatibility with old format, check if we need to transform response
        if isinstance(events, dict) and 'events' in events:
            total_events = events.get('total_events', 0)
            event_list = events.get('events', [])
        else:
            # This might be the case with the standard library format
            event_list = events if isinstance(events, list) else []
            total_events = len(event_list)
            events = {'events': event_list, 'total_events': total_events}

        logger.info(
            f'Search results: {total_events} total events,'
            f' {len(event_list)} returned'
        )

        # Return a new dictionary with UDM query first, then events data
        return {'udm_query': udm_query, 'events': events}

    except Exception as e:
        logger.error(f'Error searching security events: {str(e)}', exc_info=True)
        # Return an error object that can be processed by the model
        return {
            'udm_query': None,
            'events': {'error': str(e), 'events': [], 'total_events': 0},
        } 