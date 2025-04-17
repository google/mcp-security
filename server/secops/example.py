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
#
#!/usr/bin/env python3
"""Example usage of the Google Security Operations MCP server.

This example demonstrates how to use the secops-mcp server to perform
security operations tasks using Google Security Operations, including natural
language search.
"""

import argparse
import asyncio
from datetime import datetime, timedelta, timezone
import json
import os

# Example configuration - defaults to environment variables if available
PROJECT_ID = os.environ.get(
    'CHRONICLE_PROJECT_ID', 'your-google-cloud-project-id'
)
CUSTOMER_ID = os.environ.get(
    'CHRONICLE_CUSTOMER_ID', 'your-chronicle-customer-id'
)
REGION = os.environ.get('CHRONICLE_REGION', 'us')


# Chronicle security examples
async def security_examples(
    project_id: str, customer_id: str, region: str
) -> None:
  """Run examples of Chronicle security API calls.

  Args:
      project_id: Google Cloud project ID
      customer_id: Chronicle customer ID
      region: Chronicle region
  """
  print('\n=== Chronicle Security API Examples ===\n')

  # Example 1: Search for network connection events using UDM query
  print('Example 1: Search for network connection events using UDM query')
  events_result = await search_security_events(
      text='metadata.event_type = "NETWORK_CONNECTION"',
      project_id=project_id,
      customer_id=customer_id,
      region=region,
      hours_back=24,
      max_events=5,
  )

  # Handling the JSON response
  total_events = events_result.get('total_events', 0)
  event_list = events_result.get('events', [])

  print(
      f'Found {total_events} events, showing details for'
      f' {len(event_list)} events:'
  )

  # Process the events
  for i, event_wrapper in enumerate(event_list, 1):
    # Extract the actual event data from the wrapper
    event = event_wrapper.get('event', {})

    # Extract metadata
    metadata = event.get('metadata', {})
    event_time = metadata.get('eventTimestamp', 'Unknown')
    event_type = metadata.get('eventType', 'Unknown')

    print(f'\nEvent {i}:')
    print(f'  Time: {event_time}')
    print(f'  Type: {event_type}')

    # Extract principal data (source)
    principal = event.get('principal', {})
    if 'ip' in principal:
      print(f"  Source IP: {', '.join(principal.get('ip', ['Unknown']))}")
    if 'port' in principal:
      print(f"  Source Port: {principal.get('port', 'Unknown')}")

    # Extract target data (destination)
    target = event.get('target', {})
    if 'ip' in target:
      print(f"  Target IP: {', '.join(target.get('ip', ['Unknown']))}")
    if 'port' in target:
      print(f"  Target Port: {target.get('port', 'Unknown')}")

    # Extract network info
    network = event.get('network', {})
    if 'ipProtocol' in network:
      print(f"  Protocol: {network.get('ipProtocol', 'Unknown')}")
    if 'application_protocol' in network:
      print(f"  Application: {network.get('application_protocol', 'Unknown')}")

  # Example 2: Get security alerts
  print('\nExample 2: Get security alerts')
  alerts = await get_security_alerts(
      project_id=project_id,
      customer_id=customer_id,
      region=region,
      hours_back=24,
      max_alerts=5,
  )
  print(alerts)

  # Example 3: Look up an entity (example IP address)
  print('\nExample 3: Look up an entity')
  entity_info = await lookup_entity(
      entity_value='8.8.8.8',  # Example IP address (Google DNS)
      project_id=project_id,
      customer_id=customer_id,
      region=region,
  )
  print(entity_info)

  # Example 4: List security rules
  print('\nExample 4: List security rules')
  rules = await list_security_rules(
      project_id=project_id, customer_id=customer_id, region=region
  )
  print(rules)

  # Example 5: Get IoC matches
  print('\nExample 5: Get IoC matches')
  iocs = await get_ioc_matches(
      project_id=project_id,
      customer_id=customer_id,
      region=region,
      hours_back=24,
      max_matches=5,
  )
  print(iocs)

  # Example 6: Natural language security event search
  print('\nExample 6: Natural language security event search')
  nl_queries = [
      'Show me network connections from the last hour',
      'Find login attempts',
  ]

  for query in nl_queries:
    print(f"\nNatural language query: '{query}'")
    nl_events = await search_security_events(
        text=query,  # Using the text parameter for natural language
        project_id=project_id,
        customer_id=customer_id,
        region=region,
        hours_back=6,
        max_events=5,
    )

    # Process results
    total_nl_events = nl_events.get('total_events', 0)
    nl_event_list = nl_events.get('events', [])

    print(
        f'Found {total_nl_events} events, showing details for'
        f' {len(nl_event_list)} events:'
    )

    # Display the first few events
    for i, event_wrapper in enumerate(nl_event_list[:3], 1):
      # Extract the actual event data from the wrapper
      event = event_wrapper.get('event', {})

      # Extract metadata
      metadata = event.get('metadata', {})
      event_time = metadata.get('eventTimestamp', 'Unknown')
      event_type = metadata.get('eventType', 'Unknown')

      print(f'\nEvent {i}:')
      print(f'  Time: {event_time}')
      print(f'  Type: {event_type}')

      # Extract IP information
      principal = event.get('principal', {})
      target = event.get('target', {})

      principal_ip = (
          principal.get('ip', ['Unknown']) if 'ip' in principal else ['None']
      )
      target_ip = target.get('ip', ['Unknown']) if 'ip' in target else ['None']

      print(f"  Source IP: {', '.join(principal_ip)}")
      print(f"  Target IP: {', '.join(target_ip)}")

  # Example 7: Interactive natural language query
  print('\nExample 7: Interactive natural language query')
  try:
    custom_query = input(
        "Enter a natural language query (e.g., 'Show me suspicious activity'): "
    )
    if custom_query:
      print(f"\nNatural language query: '{custom_query}'")
      custom_events = await search_security_events(
          text=custom_query,
          project_id=project_id,
          customer_id=customer_id,
          region=region,
          hours_back=24,
          max_events=10,
      )

      # Process results
      total_custom_events = custom_events.get('total_events', 0)
      custom_event_list = custom_events.get('events', [])

      print(
          f'Found {total_custom_events} events, showing'
          f' {len(custom_event_list)} events'
      )

      # Display the events
      for i, event_wrapper in enumerate(custom_event_list, 1):
        event = event_wrapper.get('event', {})
        metadata = event.get('metadata', {})
        event_time = metadata.get('eventTimestamp', 'Unknown')
        event_type = metadata.get('eventType', 'Unknown')

        print(f'\nEvent {i}:')
        print(f'  Time: {event_time}')
        print(f'  Type: {event_type}')
  except KeyboardInterrupt:
    print('\nInteractive query cancelled.')


async def main() -> None:
  """Parse command line arguments and run security examples."""
  parser = argparse.ArgumentParser(
      description='Security Operations MCP examples'
  )
  parser.add_argument(
      '--project-id',
      help='Google Cloud project ID',
      default=os.environ.get('CHRONICLE_PROJECT_ID', ''),
  )
  parser.add_argument(
      '--customer-id',
      help='Chronicle customer ID',
      default=os.environ.get('CHRONICLE_CUSTOMER_ID', ''),
  )
  parser.add_argument(
      '--region',
      help='Chronicle region',
      default=os.environ.get('CHRONICLE_REGION', 'us'),
  )
  parser.add_argument(
      '--verbose', action='store_true', help='Show more detailed output'
  )
  args = parser.parse_args()

  # Use defaults if not provided
  if not args.project_id:
    args.project_id = '725716774503'  # Default value
    print(f'Using default project ID: {args.project_id}')

  if not args.customer_id:
    args.customer_id = 'c3c6260c1c9340dcbbb802603bbf9636'  # Default value
    print(f'Using default customer ID: {args.customer_id}')

  print(
      f'Using Chronicle settings: project_id={args.project_id},'
      f' customer_id={args.customer_id}, region={args.region}'
  )

  await security_examples(args.project_id, args.customer_id, args.region)


# Import the functions after defining the example functions to avoid circular imports
from secops_mcp import (
    search_security_events,
    get_security_alerts,
    lookup_entity,
    list_security_rules,
    get_ioc_matches,
)

if __name__ == '__main__':
  asyncio.run(main())
