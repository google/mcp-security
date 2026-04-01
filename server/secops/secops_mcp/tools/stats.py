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
"""Security Operations MCP tools for Chronicle stats/aggregation queries."""

import logging
from typing import Any, Dict, Optional

from secops_mcp.server import get_chronicle_client, server
from secops_mcp.utils import parse_time_range

logger = logging.getLogger("secops-mcp")


@server.tool()
async def get_stats(
    query: str,
    hours_back: int = 24,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    max_values: int = 60,
    max_events: int = 10000,
    case_insensitive: bool = True,
    timeout: int = 120,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> Dict[str, Any]:
    """Run a stats/aggregation query against Chronicle UDM events.

    Executes a Chronicle UDM query containing a `| stats` pipeline operator and
    returns aggregated results as structured columns and rows. Stats queries are
    significantly faster than full event fetches because they return summary data
    only — ideal for long-tail analysis, frequency counts, top-N rankings, and
    time-bucketed roll-ups.

    **When to use get_stats vs search_udm:**
    - Use `get_stats` when you need counts, aggregations, or summaries (e.g., top
      source IPs, event frequency by user, distinct process names per host).
    - Use `search_udm` when you need the raw event details themselves.

    **Stats Query Syntax:**
    Stats queries use the standard UDM filter syntax followed by a `| stats`
    pipeline. The stats operator supports:
    - `count()` — total number of matching events
    - `count_distinct(field)` — unique values of a field
    - `min(field)`, `max(field)`, `sum(field)`, `avg(field)` — numeric aggregates
    - `array_distinct(field)` — collect unique values into a list
    - `by field1, field2` — group results by one or more fields
    - `| sort column desc` — sort results
    - `| head N` — limit to top N rows

    **Example Queries:**
    ```
    # Top 10 source IPs by login failure count
    metadata.event_type = "USER_LOGIN" AND security_result.action = "BLOCK"
    | stats count() as failures by principal.ip
    | sort failures desc
    | head 10

    # Unique users per hostname over the window
    | stats count_distinct(principal.user.userid) as unique_users by target.hostname

    # Process execution frequency (LOLBin hunting)
    metadata.event_type = "PROCESS_LAUNCH"
    | stats count() as launches, array_distinct(principal.hostname) as hosts
      by target.process.file.full_path
    | sort launches desc

    # Event volume bucketed by type
    | stats count() as total by metadata.event_type | sort total desc
    ```

    **Workflow Integration:**
    - Use to triage alerts by frequency before deep-diving into raw events.
    - Identify rare/anomalous values (long-tail) — low-count rows in `count() by field`.
    - Scope the blast radius of an incident (how many hosts? how many users?).
    - Feed results into `search_udm` with specific values to get the full event context.

    Args:
        query (str): UDM query with a `| stats` operator. Filter predicates before
                    the pipe are optional — an empty filter returns stats over all
                    events in the time window.
        hours_back (int): Hours to look back from now when start_time is not given.
                         Defaults to 24.
        start_time (Optional[str]): Start of time range in ISO 8601 format
                                   (e.g. "2024-01-15T00:00:00Z"). Overrides hours_back.
        end_time (Optional[str]): End of time range in ISO 8601 format. Defaults to now.
        max_values (int): Maximum number of aggregated rows (buckets) to return.
                         Defaults to 60. Increase for high-cardinality group-by fields.
        max_events (int): Maximum raw events scanned during aggregation. Defaults to
                         10000. Increase for more complete results on busy environments.
        case_insensitive (bool): Whether string comparisons are case-insensitive.
                                Defaults to True.
        timeout (int): Request timeout in seconds. Defaults to 120. Increase for
                      complex queries over large time windows.
        project_id (Optional[str]): Google Cloud project ID. Defaults to env config.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to env config.
        region (Optional[str]): Chronicle region (e.g. "us", "europe"). Defaults to env config.

    Returns:
        Dict[str, Any]: A dictionary with:
            - "columns" (List[str]): Ordered list of column names from the stats query.
            - "rows" (List[Dict]): Each row is a dict mapping column name to its value.
              Values are typed: int, float, str, datetime, list, or None.
            - "total_rows" (int): Number of rows returned.
            Returns {"error": str, "columns": [], "rows": [], "total_rows": 0} on failure.

    Example Output:
        {
            "columns": ["principal.ip", "failures"],
            "rows": [
                {"principal.ip": "10.1.2.3", "failures": 412},
                {"principal.ip": "192.168.0.55", "failures": 87}
            ],
            "total_rows": 2
        }

    Next Steps (using MCP-enabled tools):
        - Pivot on high-count rows by passing specific values to `search_udm` for
          full event context.
        - Use `lookup_entity` on suspicious IPs or hostnames surfaced by stats.
        - Build detection rules targeting aggregation patterns identified here.
        - Export raw matching events with `export_udm_search_csv` for the top offenders.
    """
    try:
        try:
            start_dt, end_dt = parse_time_range(start_time, end_time, hours_back)
        except ValueError as e:
            logger.error(f"Error parsing date format: {str(e)}", exc_info=True)
            return {
                "error": f"Error parsing date format: {str(e)}. Use ISO 8601 format (e.g., 2024-01-15T12:00:00Z)",
                "columns": [],
                "rows": [],
                "total_rows": 0,
            }

        logger.info(
            f"Running stats query - Query: {query}, "
            f"Time Range: {start_dt} to {end_dt}, max_values: {max_values}"
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        results = chronicle.get_stats(
            query=query,
            start_time=start_dt,
            end_time=end_dt,
            max_values=max_values,
            timeout=timeout,
            max_events=max_events,
            case_insensitive=case_insensitive,
        )

        total_rows = results.get("total_rows", 0)
        logger.info(f"Stats query returned {total_rows} rows across {len(results.get('columns', []))} columns")

        return results

    except Exception as e:
        logger.error(f"Error running stats query: {str(e)}", exc_info=True)
        return {"error": str(e), "columns": [], "rows": [], "total_rows": 0}
