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
"""Security Operations MCP tools for UDM search."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def search_udm(
    query: str,
    hours_back: int = 24,
    max_events: Optional[int] = None,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> Dict[str, Any]:
    """Search UDM events using UDM query in Chronicle.

    Args:
        query (str): UDM query to search for events.
        hours_back (int): How many hours back from the current time to search.
        max_events (Optional[int]): Maximum number of events to return.
        project_id (Optional[str]): Google Cloud project ID.
        customer_id (Optional[str]): Chronicle customer ID.
        region (Optional[str]): Chronicle region (e.g., "us", "europe").

    Returns:
        Dict containing the search results with events.
    """
    try:
        logger.info(
            f'Searching UDM events - Query: {query}, Hours back: {hours_back}'
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Calculate time range
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours_back)

        logger.info(f'Search time range: {start_time} to {end_time}')

        # Call the search_udm method on the chronicle client
        search_results = chronicle.search_udm(
            query=query,
            start_time=start_time,
            end_time=end_time,
            max_events=max_events,
        )

        logger.info(f'Successfully found {search_results.get("total_events", 0)} events.')

        return search_results

    except Exception as e:
        logger.error(f'Error searching UDM events: {str(e)}', exc_info=True)
        return {'error': str(e), 'events': []}
