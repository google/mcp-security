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
"""Security Operations MCP tools for log ingestion."""

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def ingest_raw_log(
    log_type: str,
    log_message: Union[str, List[str]],
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    forwarder_id: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    log_entry_time: Optional[str] = None,
    collection_time: Optional[str] = None,
) -> str:
    """Ingest raw logs directly into Chronicle SIEM.

    Allows ingestion of raw log data in various formats (JSON, XML, CEF, etc.) into Chronicle
    for parsing and normalization into UDM format. Supports both single log and batch ingestion.



    **Workflow Integration:**
    - Use this tool to feed external log sources directly into Chronicle for analysis.
    - Ingested logs are automatically parsed using Chronicle's configured parsers for the specified log type.
    - Parsed logs become searchable through UDM queries and can trigger detection rules.
    - Essential for integrating custom applications, legacy systems, or non-standard log sources with Chronicle.

    **Use Cases:**
    - Ingest OKTA authentication logs for user behavior analysis.
    - Feed custom application logs into Chronicle for security monitoring.
    - Batch ingest historical logs during initial Chronicle deployment.
    - Import logs from external SIEM or log management systems.
    - Ingest Windows Event logs in XML format for endpoint monitoring.

    Args:
        log_type (str): Chronicle log type identifier (e.g., "OKTA", "WINEVTLOG_XML", "AWS_CLOUDTRAIL").
                       Use get_available_log_types to see supported types.
        log_message (Union[str, List[str]]): Log content as string or list of strings for batch ingestion.
                                           For JSON logs, provide as JSON string. For XML/other formats, provide raw content.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).
        forwarder_id (Optional[str]): Custom forwarder ID for log routing. If not provided, uses default forwarder.
        labels (Optional[Dict[str, str]]): Custom labels to attach to ingested logs for categorization.
        log_entry_time (Optional[str]): ISO 8601 timestamp when the log was originally generated.
        collection_time (Optional[str]): ISO 8601 timestamp when the log was collected.

    Returns:
        str: Success message with operation details, including any operation IDs for tracking.
             Returns error message if ingestion fails.

    Example Usage:
        # Single OKTA log ingestion
        ingest_raw_log(
            log_type="OKTA",
            log_message='{"actor": {"displayName": "John Doe"}, "eventType": "user.session.start"}',
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Batch Windows Event log ingestion
        ingest_raw_log(
            log_type="WINEVTLOG_XML",
            log_message=["<Event>...</Event>", "<Event>...</Event>"],
            project_id="my-project",
            customer_id="my-customer",
            region="us",
            labels={"environment": "production", "source": "domain-controller"}
        )

    Next Steps (using MCP-enabled tools):
        - Verify ingestion success by searching for the ingested logs using `search_security_events`.
        - Monitor for any parsing errors or failed ingestion through Chronicle's ingestion status APIs.
        - Create or update detection rules to analyze the newly ingested log types.
        - Set up alerting for important events found in the ingested logs.
        - Use entity lookup tools to analyze indicators found in the ingested data.
    """
    try:
        logger.info(f'Ingesting raw log of type: {log_type}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Prepare ingestion parameters
        ingestion_params = {
            'log_type': log_type,
            'log_message': log_message
        }

        if forwarder_id:
            ingestion_params['forwarder_id'] = forwarder_id
        if labels:
            ingestion_params['labels'] = labels
        if log_entry_time:
            ingestion_params['log_entry_time'] = datetime.fromisoformat(log_entry_time.replace('Z', '+00:00'))
        if collection_time:
            ingestion_params['collection_time'] = datetime.fromisoformat(collection_time.replace('Z', '+00:00'))

        # Ingest the log(s)
        result = chronicle.ingest_log(**ingestion_params)

        # Format response
        operation = result.get('operation', 'Unknown operation')
        log_count = len(log_message) if isinstance(log_message, list) else 1
        
        response = f'Successfully ingested {log_count} log(s) of type {log_type}.\n'
        response += f'Operation: {operation}'
        
        if labels:
            response += f'\nLabels applied: {labels}'
        
        return response

    except Exception as e:
        logger.error(f'Error ingesting raw log: {str(e)}', exc_info=True)
        return f'Error ingesting raw log: {str(e)}'

@server.tool()
async def ingest_udm_events(
    udm_events: Union[Dict[str, Any], List[Dict[str, Any]]],
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> str:
    """Ingest UDM events directly into Chronicle SIEM.

    Allows direct ingestion of events already formatted in Chronicle's Unified Data Model (UDM)
    format, bypassing the parsing stage. This is useful for custom applications that generate
    structured security events or for migrating pre-normalized data from other SIEMs.



    **Workflow Integration:**
    - Use when you have security data already structured in UDM format from custom applications.
    - Essential for SIEM migrations where data has been pre-normalized to UDM structure.
    - Useful for creating synthetic events for testing detection rules or filling data gaps.
    - Enables integration of custom security tools that can output UDM-formatted events.

    **Use Cases:**
    - Ingest network connection events from custom network monitoring tools.
    - Feed process execution events from custom EDR or host monitoring systems.
    - Create synthetic authentication events for testing user behavior analytics.
    - Migrate historical security events from legacy SIEM systems.
    - Ingest events from custom threat detection algorithms already in UDM format.

    **UDM Event Structure:**
    Each UDM event must include:
    - metadata: Contains event type, timestamp, product/vendor information, and unique ID
    - event-specific fields: Varies by event type (principal, target, network, etc.)

    Args:
        udm_events (Union[Dict[str, Any], List[Dict[str, Any]]]): Single UDM event or list of UDM events.
                                                               Each event must be a properly formatted UDM structure.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).

    Returns:
        str: Success message with details about the ingested events, including any generated event IDs.
             Returns error message if ingestion fails.

    Example Usage:
        # Single network connection event
        network_event = {
            "metadata": {
                "event_timestamp": "2024-02-09T10:30:00Z",
                "event_type": "NETWORK_CONNECTION",
                "product_name": "Custom Network Monitor",
                "vendor_name": "My Company"
            },
            "principal": {
                "hostname": "workstation-1",
                "ip": "192.168.1.100",
                "port": 12345
            },
            "target": {
                "ip": "203.0.113.10",
                "port": 443
            },
            "network": {
                "application_protocol": "HTTPS",
                "direction": "OUTBOUND"
            }
        }
        
        ingest_udm_events(
            udm_events=network_event,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Batch process execution events
        process_events = [
            {
                "metadata": {
                    "event_timestamp": "2024-02-09T10:31:00Z",
                    "event_type": "PROCESS_LAUNCH",
                    "product_name": "Custom EDR",
                    "vendor_name": "My Company"
                },
                "principal": {
                    "hostname": "server-1",
                    "process": {
                        "command_line": "powershell.exe -ExecutionPolicy Bypass",
                        "pid": 1234
                    },
                    "user": {
                        "userid": "admin"
                    }
                }
            }
        ]
        
        ingest_udm_events(
            udm_events=process_events,
            project_id="my-project",
            customer_id="my-customer", 
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Verify ingestion by searching for the events using `search_security_events` with appropriate UDM queries.
        - Check that ingested events trigger expected detection rules using `get_security_alerts`.
        - Use entity lookup tools to analyze any indicators present in the ingested UDM events.
        - Monitor Chronicle's ingestion metrics to ensure events are being processed correctly.
        - Create detection rules specifically targeting the custom event types you're ingesting.
    """
    try:
        logger.info('Ingesting UDM events')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Auto-generate IDs for events that don't have them
        events_to_ingest = udm_events if isinstance(udm_events, list) else [udm_events]
        
        for event in events_to_ingest:
            if 'metadata' in event and 'id' not in event['metadata']:
                event['metadata']['id'] = str(uuid.uuid4())

        # Ingest the UDM events
        result = chronicle.ingest_udm(udm_events=udm_events)

        # Format response
        event_count = len(events_to_ingest)
        response = f'Successfully ingested {event_count} UDM event(s).\n'
        
        # Add event IDs if available
        event_ids = []
        for event in events_to_ingest:
            if 'metadata' in event and 'id' in event['metadata']:
                event_ids.append(event['metadata']['id'])
        
        if event_ids:
            response += f'Event IDs: {", ".join(event_ids[:5])}'  # Show first 5 IDs
            if len(event_ids) > 5:
                response += f' (and {len(event_ids) - 5} more)'
        
        return response

    except Exception as e:
        logger.error(f'Error ingesting UDM events: {str(e)}', exc_info=True)
        return f'Error ingesting UDM events: {str(e)}'

@server.tool()
async def get_available_log_types(
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    search_term: Optional[str] = None,
) -> str:
    """Get available log types supported by Chronicle for ingestion.

    Retrieves the list of log types that Chronicle can parse and ingest, optionally filtered
    by a search term. This is useful for determining the correct log_type parameter when
    ingesting raw logs.



    **Workflow Integration:**
    - Use before ingesting logs to ensure you're using the correct log type identifier.
    - Essential for understanding Chronicle's parsing capabilities for different log sources.
    - Helps identify the appropriate log type when integrating new data sources.

    **Use Cases:**
    - Find the correct log type identifier for a specific vendor or product.
    - Discover what log formats Chronicle can natively parse.
    - Validate log type names before attempting ingestion.

    Args:
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).
        search_term (Optional[str]): Filter log types by name or description containing this term.

    Returns:
        str: Formatted list of available log types with their IDs and descriptions.
             Returns error message if retrieval fails.

    Example Usage:
        # Get all log types
        get_available_log_types(
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

        # Find firewall-related log types
        get_available_log_types(
            project_id="my-project",
            customer_id="my-customer",
            region="us",
            search_term="firewall"
        )

    Next Steps (using MCP-enabled tools):
        - Use the identified log type with `ingest_raw_log` for log ingestion.
        - Check if custom parsers exist for your specific log format using parser management tools.
        - Create custom parsers if your log format isn't supported natively.
    """
    try:
        logger.info(f'Getting available log types, search term: {search_term}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        if search_term:
            # Search for specific log types
            log_types = chronicle.search_log_types(search_term)
        else:
            # Get all log types (limit to first 50 to avoid overwhelming output)
            log_types = chronicle.get_all_log_types()[:50]

        if not log_types:
            return f'No log types found{" matching search term: " + search_term if search_term else ""}.'

        result = f'Found {len(log_types)} log type(s):\n\n'
        
        for log_type in log_types:
            log_id = getattr(log_type, 'id', 'Unknown ID')
            description = getattr(log_type, 'description', 'No description available')
            result += f'ID: {log_id}\n'
            result += f'Description: {description}\n\n'

        if len(log_types) == 50 and not search_term:
            result += '\nNote: Only showing first 50 log types. Use search_term to filter results.'

        return result

    except Exception as e:
        logger.error(f'Error getting available log types: {str(e)}', exc_info=True)
        return f'Error getting available log types: {str(e)}' 