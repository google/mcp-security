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
"""Security Operations MCP tools for entity lookup."""

import logging
from datetime import datetime, timedelta, timezone

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def lookup_entity(
    entity_value: str,
    project_id: str = None,
    customer_id: str = None,
    hours_back: int = 24,
    region: str = None,
) -> str:
    """Look up an entity (IP, domain, hash, user, etc.) in Chronicle SIEM for enrichment.

    Provides a comprehensive summary of an entity's activity based on historical log data
    within Chronicle over a specified time period. This tool queries Chronicle SIEM directly.
    Chronicle automatically attempts to detect the entity type from the value provided.

    **Workflow Integration:**
    - Use this tool after identifying key entities (IPs, domains, users, hashes) from any source
      (e.g., an alert, a SOAR case, threat intelligence report, cloud posture finding).
    - Provides historical context and activity summary for an entity directly from SIEM logs.
    - Complements information available in other security platforms (SOAR, EDR, Cloud Security)
      by offering a log-centric perspective.

    **Use Cases:**
    - Quickly understand the context and prevalence of indicators (e.g., '192.168.1.1',
      'evil.com', 'user@example.com', 'hashvalue') by examining SIEM log data.
    - Reveal historical context, broader relationships, or activity patterns potentially
      missed by other tools.
    - Enrich entities identified in alerts, cases, or reports with SIEM-derived context.

    **Output Summary:**
    The summary includes information observed within the specified time window (`hours_back`):
    - Primary entity details (type, first/last seen within the window).
    - Related entities observed interacting with the primary entity in logs.
    - Associated Chronicle alerts triggered involving the entity within the window.
    - Timeline summary (event/alert counts over the specified period).
    - Prevalence information (if available).

    Args:
        entity_value (str): Value to look up (e.g., IP address, domain name, file hash, username).
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        hours_back (int): How many hours of historical data to consider for the summary. Defaults to 24.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.

    Returns:
        str: A formatted string summarizing the entity information found in Chronicle within the specified time window,
             including first/last seen, related entities, and associated alerts.
             Returns 'No information found...' if the entity is not found in the specified timeframe.

    Example Usage:
        lookup_entity(entity_value="198.51.100.10", hours_back=72)

    Next Steps (using MCP-enabled tools):
        - Analyze the summary for suspicious patterns or relationships.
        - If more detailed event logs are needed, use a tool to search SIEM events
          (like `search_security_events`) targeting this entity's value.
        - Correlate findings with data from other security tools (e.g., EDR IoAs, network alerts,
          cloud posture findings, user risk scores) via their respective MCP tools.
        - Document findings in a relevant case management or ticketing system using an appropriate MCP tool.
    """
    try:
        chronicle = get_chronicle_client(project_id, customer_id, region)

        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours_back)

        entity_summary = chronicle.summarize_entity(
            value=entity_value,
            start_time=start_time,
            end_time=end_time,
        )

        # Handle case where no entity was found
        if not entity_summary or (
            hasattr(entity_summary, 'primary_entity') and
            not entity_summary.primary_entity
        ):
            return f'No information found for entity: {entity_value}'

        result = f'Entity Summary for {entity_value}:\n\n'

        # Process primary entity
        primary_entity = None
        if hasattr(entity_summary, 'primary_entity'):
            primary_entity = entity_summary.primary_entity

        if primary_entity:
            result += f'Primary Entity:\n'

            # Get entity type
            entity_type = 'Unknown'
            if hasattr(primary_entity, 'metadata') and hasattr(primary_entity.metadata, 'entity_type'):
                entity_type = primary_entity.metadata.entity_type

            # Get metrics
            first_seen = 'Unknown'
            last_seen = 'Unknown'
            if hasattr(primary_entity, 'metric') and primary_entity.metric:
                if hasattr(primary_entity.metric, 'first_seen'):
                    first_seen = primary_entity.metric.first_seen
                if hasattr(primary_entity.metric, 'last_seen'):
                    last_seen = primary_entity.metric.last_seen

            result += f'Entity Type: {entity_type}\n'
            result += f'First Seen: {first_seen}\n'
            result += f'Last Seen: {last_seen}\n\n'

        # Process related entities if available
        related_entities = []
        if hasattr(entity_summary, 'related_entities'):
            related_entities = entity_summary.related_entities

        if related_entities:
            result += f'Related Entities ({len(related_entities)}):\n'
            for i, entity in enumerate(related_entities[:5], 1):  # Limit to 5 related entities
                entity_type = 'Unknown'
                if hasattr(entity, 'metadata') and hasattr(entity.metadata, 'entity_type'):
                    entity_type = entity.metadata.entity_type

                result += f'{i}. Type: {entity_type}\n'

            if len(related_entities) > 5:
                result += f'... and {len(related_entities) - 5} more related entities\n'

            result += '\n'

        # Process alerts if available
        alert_counts = []
        if hasattr(entity_summary, 'alert_counts'):
            alert_counts = entity_summary.alert_counts

        if alert_counts:
            result += 'Associated Alerts:\n'
            for alert in alert_counts:
                rule = 'Unknown'
                count = 0

                if hasattr(alert, 'rule'):
                    rule = alert.rule
                if hasattr(alert, 'count'):
                    count = alert.count

                result += f'- Rule: {rule}, Count: {count}\n'

            # Add info about pagination if more alerts are available
            if hasattr(entity_summary, 'has_more_alerts') and entity_summary.has_more_alerts:
                result += '(More alerts available)\n'

            result += '\n'

        # Add timeline information if available
        if hasattr(entity_summary, 'timeline') and entity_summary.timeline:
            timeline = entity_summary.timeline
            if hasattr(timeline, 'buckets') and timeline.buckets:
                total_events = sum(bucket.event_count for bucket in timeline.buckets if hasattr(bucket, 'event_count'))
                total_alerts = sum(bucket.alert_count for bucket in timeline.buckets if hasattr(bucket, 'alert_count'))

                result += 'Timeline Summary:\n'
                result += f'Total Events: {total_events}\n'
                result += f'Total Alerts: {total_alerts}\n\n'

        # Add prevalence information if available
        if hasattr(entity_summary, 'prevalence') and entity_summary.prevalence:
            result += 'Prevalence Information Available\n\n'

        return result
    except Exception as e:
        logger.error(f'Error looking up entity: {str(e)}', exc_info=True)
        return f'Error looking up entity: {str(e)}'
