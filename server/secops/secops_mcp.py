# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#!/usr/bin/env python3
"""Example usage of the Chronicle Security Operations MCP server.

This example demonstrates how to use the secops-mcp server to perform
security operations tasks using Chronicle, including natural language search.
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging
import os
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from mcp.server.fastmcp import FastMCP
from secops import SecOpsClient

# Initialize FastMCP server
mcp = FastMCP('secops-mcp')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('secops-mcp')

# Constants
USER_AGENT = 'secops-app/1.0'

# Default Chronicle configuration from environment variables
DEFAULT_PROJECT_ID = os.environ.get('CHRONICLE_PROJECT_ID', '725716774503')
DEFAULT_CUSTOMER_ID = os.environ.get(
    'CHRONICLE_CUSTOMER_ID', 'c3c6260c1c9340dcbbb802603bbf9636'
)
DEFAULT_REGION = os.environ.get('CHRONICLE_REGION', 'us')


# Initialize SecOpsClient
def get_chronicle_client(
    project_id: str = None, customer_id: str = None, region: str = None
) -> Any:
  """Initialize and return a Chronicle client.

  Args:
      project_id: Google Cloud project ID (defaults to CHRONICLE_PROJECT_ID env
        var)
      customer_id: Chronicle customer ID (defaults to CHRONICLE_CUSTOMER_ID env
        var)
      region: Chronicle region (defaults to CHRONICLE_REGION env var or "us")

  Returns:
      Initialized Chronicle client
  """
  # Use provided values or defaults from environment variables
  project_id = project_id or DEFAULT_PROJECT_ID
  customer_id = customer_id or DEFAULT_CUSTOMER_ID
  region = region or DEFAULT_REGION

  if not project_id or not customer_id:
    raise ValueError(
        'Chronicle project_id and customer_id must be provided either '
        'as parameters or through environment variables '
        '(CHRONICLE_PROJECT_ID, CHRONICLE_CUSTOMER_ID)'
    )

  client = SecOpsClient()
  chronicle = client.chronicle(
      customer_id=customer_id, project_id=project_id, region=region
  )
  return chronicle


# Chronicle Security Tools
@mcp.tool()
async def search_security_events(
    text: str,
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    max_events: int = 100,
    region: str = None,
) -> Dict[str, Any]:
  """Search for security events in Chronicle using natural language.

  This function allows you to search for events using everyday language instead
  of requiring
  UDM query syntax. The natural language query will be automatically translated
  into a
  Chronicle UDM query for execution.

  Examples of natural language queries:
  - "Show me network connections from yesterday for the domain google.com"
  - "Display connections to IP address 192.168.1.100"

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
    logger.info(f'Searching security events with natural language query: {text}')

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
        f'Search results: {total_events} total events, {len(event_list)} returned'
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


@mcp.tool()
async def get_security_alerts(
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    max_alerts: int = 10,
    status_filter: str = 'feedback_summary.status != "CLOSED"',
    region: str = None,
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
      if 'feedbackSummary' in alert and isinstance(alert['feedbackSummary'], dict):
        status = alert['feedbackSummary'].get('status', 'Unknown')
      elif 'status' in alert:
        status = alert.get('status', 'Unknown')

      # Try different possible severity field paths
      severity = 'Unknown'
      if 'feedbackSummary' in alert and isinstance(alert['feedbackSummary'], dict):
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


@mcp.tool()
async def lookup_entity(
    entity_value: str,
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    region: str = None,
) -> str:
  """Look up an entity (IP, domain, hash, etc.) in Chronicle.

  Args:
      entity_value: Value to look up (IP, domain, hash, etc.)
      project_id: Google Cloud project ID (defaults to config)
      customer_id: Chronicle customer ID (defaults to config)
      hours_back: How many hours to look back (default: 24)
      region: Chronicle region (defaults to config)

  Returns:
      Entity summary information
  """
  try:
    chronicle = get_chronicle_client(project_id, customer_id, region)

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_back)

    entity_summary = chronicle.summarize_entity(
        start_time=start_time,
        end_time=end_time,
        value=entity_value,
        return_alerts=True,
    )

    # Handle different possible response formats
    entities = []
    if hasattr(entity_summary, 'entities'):
      entities = entity_summary.entities
    elif isinstance(entity_summary, dict) and 'entities' in entity_summary:
      entities = entity_summary.get('entities', [])
    elif isinstance(entity_summary, list):
      entities = entity_summary

    if not entities:
      return f'No information found for entity: {entity_value}'

    result = f'Entity Summary for {entity_value}:\n\n'

    for entity in entities:
      # Try to access fields with different possible structures
      entity_type = 'Unknown'
      first_seen = 'Unknown'
      last_seen = 'Unknown'
      count = 0
      asset = None

      # Try to get entity_type
      if hasattr(entity, 'metadata') and hasattr(entity.metadata, 'entity_type'):
        entity_type = entity.metadata.entity_type
      elif isinstance(entity, dict) and 'metadata' in entity:
        if isinstance(entity['metadata'], dict):
          entity_type = entity['metadata'].get('entityType', 'Unknown')

      # Try to get metrics
      if hasattr(entity, 'metric'):
        first_seen = entity.metric.first_seen
        last_seen = entity.metric.last_seen
        count = entity.metric.count
      elif isinstance(entity, dict) and 'metric' in entity:
        if isinstance(entity['metric'], dict):
          first_seen = entity['metric'].get('firstSeen', 'Unknown')
          last_seen = entity['metric'].get('lastSeen', 'Unknown')
          count = entity['metric'].get('count', 0)

      # Try to get asset
      if hasattr(entity, 'metadata') and hasattr(entity.metadata, 'asset'):
        asset = entity.metadata.asset
      elif isinstance(entity, dict) and 'metadata' in entity:
        if isinstance(entity['metadata'], dict):
          asset = entity['metadata'].get('asset')

      result += f'Entity Type: {entity_type}\n'
      result += f'First Seen: {first_seen}\n'
      result += f'Last Seen: {last_seen}\n'
      result += f'Event Count: {count}\n'

      # Add asset information if available
      if asset:
        result += f'Asset: {asset}\n'

      result += '\n'

    # Add alert information if available
    alert_counts = []
    if hasattr(entity_summary, 'alert_counts'):
      alert_counts = entity_summary.alert_counts
    elif isinstance(entity_summary, dict) and 'alertCounts' in entity_summary:
      alert_counts = entity_summary.get('alertCounts', [])

    if alert_counts:
      result += 'Associated Alerts:\n'
      for alert in alert_counts:
        rule = 'Unknown'
        count = 0

        if hasattr(alert, 'rule'):
          rule = alert.rule
          count = alert.count
        elif isinstance(alert, dict):
          rule = alert.get('rule', 'Unknown')
          count = alert.get('count', 0)

        result += f'- Rule: {rule}, Count: {count}\n'

    return result
  except Exception as e:
    return f'Error looking up entity: {str(e)}'


@mcp.tool()
async def list_security_rules(
    project_id: str = None, customer_id: str = None, region: str = None
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


@mcp.tool()
async def get_ioc_matches(
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    max_matches: int = 20,
    region: str = None,
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


def main() -> None:
  """Run the MCP server for SecOps tools.

  This function initializes and starts the MCP server with all the defined
  tools.
  """
  # Initialize and run the server
  mcp.run(transport='stdio')


if __name__ == '__main__':
  main()
