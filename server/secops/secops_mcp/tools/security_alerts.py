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
"""Security Operations MCP tools for security alerts."""

from datetime import datetime, timedelta, timezone
import logging
from typing import Optional

from secops_mcp.server import server, get_chronicle_client

# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def get_security_alerts(
    project_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    hours_back: int = 24,
    max_alerts: int = 10,
    status_filter: str = 'feedback_summary.status != "CLOSED"',
    region: Optional[str] = None,
) -> str:
    """Get security alerts from Chronicle.

    Args:
        project_id: Google Cloud project ID (defaults to config)
        customer_id: Chronicle customer ID (defaults to config)
        hours_back: How many hours to look back (default: 24)
        max_alerts: Maximum number of alerts to return (default: 10)
        status_filter: Query string to filter alerts by status (default: exclude
          closed)
        region: Chronicle region (defaults to config)

    Returns:
        Formatted string with security alerts
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours_back)

        alert_response = chronicle.get_alerts(
            start_time=start_time,
            end_time=end_time,
            snapshot_query=status_filter,
            max_alerts=max_alerts,
        )

        # The response format depends on the secops library version
        # Try to handle both formats
        if isinstance(alert_response, dict):
            alert_list = alert_response.get('alerts', {}).get('alerts', [])
        else:
            # Might be a direct list of alerts in the standard library
            alert_list = alert_response if isinstance(alert_response, list) else []

        if not alert_list:
            return 'No security alerts found for the specified time range.'

        result = f'Found {len(alert_list)} security alerts:\n\n'

        for i, alert in enumerate(alert_list, 1):
            # Try to access fields with different possible structures
            rule_name = None
            if (
                'detection' in alert
                and isinstance(alert['detection'], list)
                and len(alert['detection']) > 0
            ):
                rule_name = alert['detection'][0].get('ruleName', 'Unknown Rule')
            else:
                rule_name = alert.get('ruleName', 'Unknown Rule')

            created_time = alert.get('createdTime', 'Unknown')

            # Try different possible status field paths
            status = 'Unknown'
            if 'feedbackSummary' in alert and isinstance(
                alert['feedbackSummary'], dict
            ):
                status = alert['feedbackSummary'].get('status', 'Unknown')
            elif 'status' in alert:
                status = alert.get('status', 'Unknown')

            # Try different possible severity field paths
            severity = 'Unknown'
            if 'feedbackSummary' in alert and isinstance(
                alert['feedbackSummary'], dict
            ):
                severity = alert['feedbackSummary'].get('severityDisplay', 'Unknown')
            elif 'severity' in alert:
                severity = alert.get('severity', 'Unknown')

            result += f'Alert {i}:\n'
            result += f'Rule: {rule_name}\n'
            result += f'Created: {created_time}\n'
            result += f'Status: {status}\n'
            result += f'Severity: {severity}\n'

            # Add case information if available
            case_name = alert.get('caseName')
            if case_name:
                result += f'Associated Case: {case_name}\n'

            result += '\n'

        return result
    except Exception as e:
        return f'Error retrieving security alerts: {str(e)}' 