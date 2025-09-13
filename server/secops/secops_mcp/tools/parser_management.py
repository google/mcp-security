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
"""Security Operations MCP tools for parser management."""

import base64
import json
import logging
from typing import Any, Dict, List, Optional

from secops_mcp.server import get_chronicle_client, server


# Configure logging
logger = logging.getLogger('secops-mcp')

@server.tool()
async def create_parser(
    log_type: str,
    parser_code: str,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    validated_on_empty_logs: bool = True,
) -> str:
    """Create a new parser for a specific log type in Chronicle.

    Creates a custom parser using Chronicle's parser configuration language to transform
    raw logs into Chronicle's Unified Data Model (UDM) format. Parsers are essential for
    ingesting custom log formats that aren't natively supported by Chronicle.



    **Workflow Integration:**
    - Use when you need to ingest custom log formats that Chronicle doesn't natively support.
    - Essential for integrating custom applications, proprietary systems, or modified log formats.
    - Enables normalization of diverse log sources into a consistent UDM structure for analysis.
    - Prerequisite for meaningful analysis of custom log sources through Chronicle's detection capabilities.

    **Use Cases:**
    - Create parsers for custom application logs with unique formats.
    - Parse proprietary security tool outputs into UDM format.
    - Handle modified versions of standard log formats that existing parsers can't process.
    - Transform legacy log formats for Chronicle ingestion during SIEM migrations.
    - Parse structured data from APIs or databases into security events.

    Args:
        log_type (str): Chronicle log type identifier for this parser (e.g., "CUSTOM_APP", "WINDOWS_AD").
        parser_code (str): Parser configuration code using Chronicle's parser DSL (typically using filters like mutate, grok, etc.).
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).
        validated_on_empty_logs (bool): Whether to validate the parser even on empty log samples. Defaults to True.

    Returns:
        str: Success message with the created parser ID and details.
             Returns error message if parser creation fails.

    Example Usage:
        parser_text = '''
        filter {
            mutate {
              replace => {
                "event1.idm.read_only_udm.metadata.event_type" => "GENERIC_EVENT"
                "event1.idm.read_only_udm.metadata.vendor_name" =>  "ACME Labs"
              }
            }
            grok {
              match => {
                "message" => ["^(?P<_firstWord>[^\\s]+)\\s.*$"]
              }
              on_error => "_grok_message_failed"
            }
            if ![_grok_message_failed] {
              mutate {
                replace => {
                  "event1.idm.read_only_udm.metadata.description" => "%{_firstWord}"
                }
              }
            }
            mutate {
              merge => {
                "@output" => "event1"
              }
            }
        }
        '''
        
        create_parser(
            log_type="CUSTOM_APP",
            parser_code=parser_text,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Test the parser using `run_parser_against_sample_logs` with sample log data.
        - Activate the parser using `activate_parser` once testing is complete.
        - Ingest logs using `ingest_raw_log` with the specified log_type.
        - Monitor parsing success and adjust the parser configuration if needed.
        - Create detection rules that leverage the parsed UDM fields.
    """
    try:
        logger.info(f'Creating parser for log type: {log_type}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Create the parser
        parser = chronicle.create_parser(
            log_type=log_type,
            parser_code=parser_code,
            validated_on_empty_logs=validated_on_empty_logs
        )

        # Extract parser ID from the response
        parser_id = parser.get("name", "").split("/")[-1]
        state = parser.get("state", "Unknown")
        
        result = f'Successfully created parser for log type: {log_type}\n'
        result += f'Parser ID: {parser_id}\n'
        result += f'State: {state}\n'
        
        if validated_on_empty_logs:
            result += 'Parser was validated on empty logs during creation.'
        
        return result

    except Exception as e:
        logger.error(f'Error creating parser for log type {log_type}: {str(e)}', exc_info=True)
        return f'Error creating parser for log type {log_type}: {str(e)}'

@server.tool()
async def get_parser(
    log_type: str,
    parser_id: str,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> str:
    """Get details of a specific parser in Chronicle.

    Retrieves the configuration and metadata for a specific parser, including its current
    state, parser code, and other properties. Useful for reviewing existing parsers or
    copying configurations for new parsers.



    **Workflow Integration:**
    - Use to review existing parser configurations before modifications.
    - Essential for troubleshooting parsing issues by examining the current parser logic.
    - Helps understand how specific log types are being processed in Chronicle.
    - Useful for copying parser configurations as templates for new parsers.

    **Use Cases:**
    - Review parser code to understand how logs are being transformed.
    - Troubleshoot parsing issues by examining the current configuration.
    - Copy existing parser configurations as starting points for new parsers.
    - Audit parser configurations for compliance or security reviews.
    - Understand the parsing logic for specific log types during investigations.

    Args:
        log_type (str): Chronicle log type identifier for the parser.
        parser_id (str): Unique identifier of the parser to retrieve.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).

    Returns:
        str: Formatted parser details including ID, state, and configuration code.
             Returns error message if parser retrieval fails.

    Example Usage:
        get_parser(
            log_type="OKTA",
            parser_id="pa_12345678-1234-1234-1234-123456789012",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Modify the parser configuration if needed and create an updated version.
        - Test the parser using `run_parser_against_sample_logs` with representative log samples.
        - Use the configuration as a template for creating parsers for similar log types.
        - Activate or deactivate the parser based on your requirements.
    """
    try:
        logger.info(f'Getting parser {parser_id} for log type: {log_type}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Get the parser
        parser = chronicle.get_parser(log_type=log_type, id=parser_id)

        parser_name = parser.get("name", "").split("/")[-1]
        state = parser.get("state", "Unknown")
        create_time = parser.get("createTime", "Unknown")
        
        result = f'Parser Details:\n\n'
        result += f'Parser ID: {parser_name}\n'
        result += f'Log Type: {log_type}\n'
        result += f'State: {state}\n'
        result += f'Created: {create_time}\n\n'
        
        # Extract and decode parser code if available
        parser_code = parser.get("text", "")
        if not parser_code and "cbn" in parser:
            # Decode base64 encoded parser code
            try:
                parser_code = base64.b64decode(parser["cbn"]).decode('utf-8')
            except Exception as decode_error:
                logger.warning(f"Failed to decode parser code: {decode_error}")
                parser_code = "Could not decode parser code"
        
        if parser_code:
            result += f'Parser Code:\n{parser_code}\n'
        else:
            result += 'Parser code not available in response.\n'
        
        return result

    except Exception as e:
        logger.error(f'Error getting parser {parser_id} for log type {log_type}: {str(e)}', exc_info=True)
        return f'Error getting parser {parser_id} for log type {log_type}: {str(e)}'

@server.tool()
async def activate_parser(
    log_type: str,
    parser_id: str,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> str:
    """Activate a parser for a specific log type in Chronicle.

    Activates a parser, making it the active parser for the specified log type. Once activated,
    the parser will be used to process all incoming logs of that type. Only one parser can be
    active for each log type at a time.



    **Workflow Integration:**
    - Use after creating and testing a parser to make it operational.
    - Essential step for putting new or updated parsers into production.
    - Enables the parser to process incoming logs and generate searchable UDM events.
    - Required before logs of the specified type can be properly parsed and analyzed.

    **Use Cases:**
    - Activate a newly created parser after successful testing.
    - Switch to an updated parser version with improved parsing logic.
    - Restore a previously working parser after troubleshooting parsing issues.
    - Deploy parser changes as part of log ingestion pipeline updates.

    Args:
        log_type (str): Chronicle log type identifier for the parser.
        parser_id (str): Unique identifier of the parser to activate.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).

    Returns:
        str: Success message confirming parser activation.
             Returns error message if activation fails.

    Example Usage:
        activate_parser(
            log_type="CUSTOM_APP",
            parser_id="pa_12345678-1234-1234-1234-123456789012",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Ingest test logs using `ingest_raw_log` to verify the parser is working correctly.
        - Monitor parsing success rates and troubleshoot any issues.
        - Search for parsed events using `search_security_events` to confirm proper UDM conversion.
        - Create detection rules that leverage the newly parsed UDM fields.
        - Set up monitoring for the log type to ensure continued parsing success.
    """
    try:
        logger.info(f'Activating parser {parser_id} for log type: {log_type}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Activate the parser
        chronicle.activate_parser(log_type=log_type, id=parser_id)

        result = f'Successfully activated parser for log type: {log_type}\n'
        result += f'Parser ID: {parser_id}\n'
        result += 'The parser is now active and will process incoming logs of this type.'
        
        return result

    except Exception as e:
        logger.error(f'Error activating parser {parser_id} for log type {log_type}: {str(e)}', exc_info=True)
        return f'Error activating parser {parser_id} for log type {log_type}: {str(e)}'

@server.tool()
async def deactivate_parser(
    log_type: str,
    parser_id: str,
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
) -> str:
    """Deactivate a parser for a specific log type in Chronicle.

    Deactivates a parser, stopping it from processing incoming logs of the specified type.
    After deactivation, logs of this type will not be parsed until another parser is activated
    or the same parser is reactivated.



    **Workflow Integration:**
    - Use when you need to temporarily stop parsing for a specific log type.
    - Essential for troubleshooting parsing issues by stopping problematic parsers.
    - Useful before deploying updated parser versions to prevent conflicts.
    - Helps manage parser lifecycle during development and testing phases.

    **Use Cases:**
    - Temporarily stop parsing while troubleshooting issues with the current parser.
    - Deactivate a parser before activating an updated version.
    - Stop parsing for log types that are no longer needed or relevant.
    - Prevent parsing during maintenance windows or system changes.
    - Disable problematic parsers that are causing ingestion errors.

    **Warning:**
    After deactivation, incoming logs of this type will not be parsed into UDM format and may
    not be searchable or usable for detection until a parser is reactivated.

    Args:
        log_type (str): Chronicle log type identifier for the parser.
        parser_id (str): Unique identifier of the parser to deactivate.
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).

    Returns:
        str: Success message confirming parser deactivation.
             Returns error message if deactivation fails.

    Example Usage:
        deactivate_parser(
            log_type="CUSTOM_APP",
            parser_id="pa_12345678-1234-1234-1234-123456789012",
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Activate an updated parser version if this was part of a parser update process.
        - Monitor log ingestion to ensure no critical parsing is stopped unintentionally.
        - Test and validate any replacement parser before activating it.
        - Document the reason for deactivation for operational tracking.
    """
    try:
        logger.info(f'Deactivating parser {parser_id} for log type: {log_type}')

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Deactivate the parser
        chronicle.deactivate_parser(log_type=log_type, id=parser_id)

        result = f'Successfully deactivated parser for log type: {log_type}\n'
        result += f'Parser ID: {parser_id}\n'
        result += 'WARNING: Incoming logs of this type will not be parsed until a parser is activated.'
        
        return result

    except Exception as e:
        logger.error(f'Error deactivating parser {parser_id} for log type {log_type}: {str(e)}', exc_info=True)
        return f'Error deactivating parser {parser_id} for log type {log_type}: {str(e)}'

@server.tool()
async def run_parser_against_sample_logs(
    log_type: str,
    parser_code: str,
    sample_logs: List[str],
    project_id: str = None,
    customer_id: str = None,
    region: str = None,
    parser_extension_code: Optional[str] = None,
    statedump_allowed: bool = False,
) -> str:
    """Run a parser against sample logs to test parsing logic.

    Tests parser configuration against sample log entries to validate parsing logic before
    deployment. This is essential for ensuring parsers work correctly with your specific
    log formats and produce the expected UDM output.



    **Workflow Integration:**
    - Essential testing step before creating or activating parsers in production.
    - Use during parser development to iteratively refine parsing logic.
    - Validate parser behavior with real log samples from your environment.
    - Verify that parsing produces the expected UDM fields and values.

    **Use Cases:**
    - Test new parser configurations with representative log samples.
    - Validate parser changes before deploying to production.
    - Troubleshoot parsing issues by examining parser output step-by-step.
    - Verify that parser handles edge cases and varied log formats correctly.
    - Understand how specific log fields are mapped to UDM structure.

    **Parser Testing Best Practices:**
    - Use diverse log samples that represent different scenarios and edge cases.
    - Include both typical and edge-case log formats in your test samples.
    - Verify that critical fields are correctly parsed and mapped to appropriate UDM fields.
    - Test with logs that might cause parsing failures to ensure robust error handling.

    Args:
        log_type (str): Chronicle log type identifier for the parser.
        parser_code (str): Parser configuration code to test.
        sample_logs (List[str]): List of sample log entries to test against (max 1000 logs, 10MB per log, 50MB total).
        project_id (str): Google Cloud project ID (required).
        customer_id (str): Chronicle customer ID (required).
        region (str): Chronicle region (e.g., "us", "europe") (required).
        parser_extension_code (Optional[str]): Additional parser extension code if needed.
        statedump_allowed (bool): Whether to allow statedump filters in the parser. Defaults to False.

    Returns:
        str: Formatted results showing parsing outcomes for each sample log, including any UDM events
             generated and parsing errors encountered. Returns error message if testing fails.

    Example Usage:
        sample_logs = [
            '{"message": "ERROR: Failed authentication attempt", "timestamp": "2024-02-09T10:30:00Z"}',
            '{"message": "WARNING: Suspicious activity detected", "timestamp": "2024-02-09T10:31:00Z"}',
            '{"message": "INFO: User logged in successfully", "timestamp": "2024-02-09T10:32:00Z"}'
        ]
        
        parser_text = '''
        filter {
            mutate {
              replace => {
                "event1.idm.read_only_udm.metadata.event_type" => "GENERIC_EVENT"
                "event1.idm.read_only_udm.metadata.vendor_name" =>  "ACME Labs"
              }
            }
            grok {
              match => {
                "message" => ["^(?P<_firstWord>[^\\s]+)\\s.*$"]
              }
              on_error => "_grok_message_failed"
            }
            if ![_grok_message_failed] {
              mutate {
                replace => {
                  "event1.idm.read_only_udm.metadata.description" => "%{_firstWord}"
                }
              }
            }
            mutate {
              merge => {
                "@output" => "event1"
              }
            }
        }
        '''
        
        run_parser_against_sample_logs(
            log_type="CUSTOM_APP",
            parser_code=parser_text,
            sample_logs=sample_logs,
            project_id="my-project",
            customer_id="my-customer",
            region="us"
        )

    Next Steps (using MCP-enabled tools):
        - Analyze the parsing results to ensure UDM events are generated correctly.
        - Refine the parser code based on the test results and retest as needed.
        - Create the parser using `create_parser` once testing is successful.
        - Activate the parser using `activate_parser` to put it into production.
        - Ingest real logs using `ingest_raw_log` and verify parsing works in production.
    """
    try:
        logger.info(f'Running parser test for log type: {log_type} with {len(sample_logs)} sample logs')

        # Validate input constraints
        if len(sample_logs) > 1000:
            return "Error: Maximum of 1000 sample logs allowed per test."
        
        total_size = sum(len(log.encode('utf-8')) for log in sample_logs)
        if total_size > 50 * 1024 * 1024:  # 50MB
            return "Error: Total sample logs size exceeds 50MB limit."
        
        for i, log in enumerate(sample_logs):
            if len(log.encode('utf-8')) > 10 * 1024 * 1024:  # 10MB
                return f"Error: Sample log {i+1} exceeds 10MB size limit."

        
        
        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Run the parser
        result = chronicle.run_parser(
            log_type=log_type,
            parser_code=parser_code,
            parser_extension_code=parser_extension_code,
            logs=sample_logs,
            statedump_allowed=statedump_allowed
        )

        # Process and format the results
        response = f'Parser test results for log type: {log_type}\n'
        response += f'Tested {len(sample_logs)} sample log(s)\n\n'

        if "runParserResults" in result:
            for i, parser_result in enumerate(result["runParserResults"]):
                response += f'Log {i+1} Results:\n'
                
                # Check for parsed events
                if "parsedEvents" in parser_result and parser_result["parsedEvents"]:
                    parsed_events = parser_result["parsedEvents"]
                    if isinstance(parsed_events, dict) and "events" in parsed_events:
                        events = parsed_events["events"]
                        response += f'  Successfully parsed {len(events)} UDM event(s)\n'
                        
                        # Show first event details
                        if events:
                            first_event = events[0]
                            if "event" in first_event:
                                event_data = first_event["event"]
                                if "metadata" in event_data:
                                    metadata = event_data["metadata"]
                                    event_type = metadata.get("eventType", "Unknown")
                                    response += f'  Event Type: {event_type}\n'
                                    if "description" in metadata:
                                        response += f'  Description: {metadata["description"]}\n'
                    else:
                        response += f'  Parsed events: {parsed_events}\n'
                else:
                    response += '  No parsed events generated\n'
                
                # Check for errors
                if "errors" in parser_result and parser_result["errors"]:
                    errors = parser_result["errors"]
                    response += f'  Parsing errors: {errors}\n'
                
                response += '\n'
        else:
            response += f'Unexpected result format: {result}'

        return response

    except Exception as e:
        logger.error(f'Error running parser test for log type {log_type}: {str(e)}', exc_info=True)
        return f'Error running parser test for log type {log_type}: {str(e)}' 