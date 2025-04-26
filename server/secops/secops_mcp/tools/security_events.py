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

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def search_security_events(
    text: str,
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    max_events: int = 100,
    region: str = None,
) -> Dict[str, Any]:
    """Search for security events in Chronicle SIEM using natural language.

    Allows searching Chronicle event logs using natural language queries, which are
    automatically translated into UDM queries for execution.

    **Workflow Integration:**
    - Ideal for deep investigation after an initial alert, case, or entity has been prioritized.
    - Use it to retrieve detailed UDM event logs from Chronicle SIEM related to specific indicators
      or activities, going beyond high-level summaries from other tools.
    - Helps validate findings from other security platforms (SOAR, EDR, TI) by examining the
      underlying log evidence.

    **Use Cases:**
    - Investigate specific activities or test hypotheses during incident analysis.
    - Retrieve raw event logs related to specific indicators (IPs, domains, users, hosts)
      or activities (e.g., logins, file modifications, network connections) within a
      defined time window when granular detail is needed.

    Examples of natural language queries for investigation:
    - "Show network connections involving IP 10.0.0.5 in the last 6 hours"
    - "Find login events for user 'admin' yesterday"
    - "List file modifications on host 'server1' today"
    - "Search for DNS lookups to 'malicious.example.com' in the past 3 days"

    Note: When searching for email addresses, use only lowercase letters.

    Args:
        text (str): Natural language description of the events you want to find.
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        hours_back (int): How many hours back from the current time to search. Defaults to 24.
        max_events (int): Maximum number of event records to return. Defaults to 100.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - 'udm_query' (str | None): The translated UDM query used for the search, or None if translation failed.
            - 'events' (Dict): A dictionary containing the search results:
                - 'events' (List[Dict]): The list of UDM event records found.
                - 'total_events' (int): The total number of events matching the query (may exceed `max_events`).
                - 'error' (str | None): An error message if the search failed.

    Next Steps (using MCP-enabled tools):
        - Analyze the returned UDM event records for relevant details (e.g., specific commands executed, full connection details, file paths).
        - Extract new indicators (IPs, domains, hashes, users) from the events.
        - Use entity lookup tools (like `lookup_entity`) or threat intelligence tools
          to enrich newly found indicators.
        - Correlate findings with data from other security tools (e.g., EDR process details,
          network flow data, cloud audit logs) via their respective MCP tools.
        - Document findings in a relevant case management or ticketing system using an appropriate MCP tool.
        - Use findings to inform response actions (e.g., blocking an IP, isolating a host) via SOAR or endpoint MCP tools.

    **Troubleshooting & Iterative Searching:**

    If your initial natural language search doesn't return the expected events, consider the following iterative steps:

    1.  **Check the Translated Query:** Examine the `udm_query` field in the response. This shows how your natural language was translated into UDM. Does it accurately reflect your intent? Are the correct UDM fields being targeted?
    2.  **Broaden the Search:**
        *   **Remove Specific Event Types:** If you initially filtered by `metadata.event_type` (e.g., "USER_LOGIN"), try removing that constraint to search across all event types. Example: "Find any events involving IP 1.2.3.4" instead of "Find login events involving IP 1.2.3.4".
        *   **Simplify the Query:** Reduce the complexity of your natural language query to focus on the core entity or activity.
    3.  **Target Alternative UDM Fields:** Chronicle's UDM has many fields. If searching for an entity like a user or IP doesn't work with a simple query, the identifier might be in a less common field. Try specifying fields often used for:
        *   **Users:** `principal.user.userid`, `target.user.userid`, `src.user.userid`, `network.email.from`, `network.email.to`, `about.user.userid`
        *   **IPs:** `principal.ip`, `target.ip`, `src.ip`, `observer.ip`, `network.ip`, `about.ip`
        *   **Hostnames:** `principal.hostname`, `target.hostname`, `src.hostname`, `about.hostname`
        *   **URLs:** `target.url`, `about.url`
        *   **Hashes:** `target.file.md5`, `target.file.sha1`, `target.file.sha256`, `principal.process.file.md5`, etc.
        *   **Natural Language Example:** Instead of "Events for user john.doe@example.com", try "Events where the target email address is john.doe@example.com" or "Events where the principal user ID is john.doe@example.com".
    4.  **Refine Time Window:** Ensure the `hours_back` parameter covers the expected timeframe of the events.
    5.  **Consult UDM Schema:** If specific fields are known, referencing the Chronicle UDM schema can help formulate more precise natural language queries targeting those fields.

    **Example Iteration:**

    *   **Initial Query (Fails):** "Find login events for user charlie.brown@cymbalgroup.com"
        *   *Returned `udm_query`: `metadata.event_type = "USER_LOGIN" user = "charlie.brown@cymbalgroup.com"`*
        *   *Result: 0 events*
    *   **Iteration 1 (Broaden):** "Find any events where the user is 'charlie.brown@cymbalgroup.com'"
        *   *Returned `udm_query`: `email = "charlie.brown@cymbalgroup.com"`*
        *   *Result: 6 events (Success!)* - This indicates the user identifier was primarily in an `email` field, not the generic `user` field, and removing the `USER_LOGIN` constraint helped.
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
