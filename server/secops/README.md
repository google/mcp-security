# Chronicle SecOps MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google's
Chronicle Security Operations suite.
[MCP Info](https://modelcontextprotocol.io/introduction)

## Features

### Security Tools

- **`search_security_events(text, project_id=None, customer_id=None, hours_back=24, max_events=100, region=None)`**
    - Searches for security events in Chronicle using natural language. Translates the natural language query (`text`) into a UDM query and executes it.

- **`get_security_alerts(project_id=None, customer_id=None, hours_back=24, max_alerts=10, status_filter='feedback_summary.status != "CLOSED"', region=None)`**
    - Retrieves security alerts from Chronicle, filtered by time range and status.

- **`lookup_entity(entity_value, project_id=None, customer_id=None, hours_back=24, region=None)`**
    - Looks up an entity (IP, domain, hash, etc.) in Chronicle.

- **`list_security_rules(project_id=None, customer_id=None, region=None)`**
    - Lists security detection rules from Chronicle.

- **`search_security_rules(query, project_id=None, customer_id=None, region=None)`**
    - Searches security detection rules from Chronicle using regex.

- **`get_detection_rule(rule_id, project_id=None, customer_id=None, region=None)`**
    - Retrieves complete YARA-L detection rule code and metadata from Chronicle by Rule Id.

- **`get_ioc_matches(project_id=None, customer_id=None, hours_back=24, max_matches=20, region=None)`**
    - Retrieves Indicators of Compromise (IoCs) matches from Chronicle within a specified time range.

- **`get_threat_intel(query, project_id=None, customer_id=None, region=None)`**
    - Get answers to general security domain questions and specific threat intelligence information using Chronicle's AI capabilities.

### Log Ingestion Tools

- **`ingest_raw_log(log_type, log_message, project_id=None, customer_id=None, region=None, forwarder_id=None, labels=None, log_entry_time=None, collection_time=None)`**
    - Ingest raw logs directly into Chronicle SIEM. Supports various formats (JSON, XML, CEF, etc.) and batch ingestion.

- **`ingest_udm_events(udm_events, project_id=None, customer_id=None, region=None)`**
    - Ingest events already formatted in Chronicle's Unified Data Model (UDM) format, bypassing the parsing stage.

- **`get_available_log_types(project_id=None, customer_id=None, region=None, search_term=None)`**
    - Get available log types supported by Chronicle for ingestion, optionally filtered by search term.

### Parser Management Tools

- **`create_parser(log_type, parser_code, project_id=None, customer_id=None, region=None, validated_on_empty_logs=True)`**
    - Create a custom parser for a specific log type to transform raw logs into Chronicle's UDM format.

- **`get_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
    - Get details of a specific parser including its configuration and metadata.

- **`activate_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
    - Activate a parser, making it the active parser for the specified log type.

- **`deactivate_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
    - Deactivate a parser, stopping it from processing incoming logs of the specified type.

- **`run_parser_against_sample_logs(log_type, parser_code, sample_logs, project_id=None, customer_id=None, region=None, parser_extension_code=None, statedump_allowed=False)`**
    - Test parser configuration against sample log entries to validate parsing logic before deployment.

### Data Table Management Tools

- **`create_data_table(name, description, header, project_id=None, customer_id=None, region=None, rows=None)`**
    - Create a structured data table that can be referenced in detection rules. Supports multiple column types (STRING, CIDR, INT64, BOOL).

- **`add_rows_to_data_table(table_name, rows, project_id=None, customer_id=None, region=None)`**
    - Add new rows to an existing data table, expanding the dataset available for detection rules.

- **`list_data_table_rows(table_name, project_id=None, customer_id=None, region=None, max_rows=50)`**
    - List rows in a data table to review contents and verify data integrity.

- **`delete_data_table_rows(table_name, row_ids, project_id=None, customer_id=None, region=None)`**
    - Delete specific rows from a data table based on their row IDs.

### Reference List Management Tools

- **`create_reference_list(name, description, entries, project_id=None, customer_id=None, region=None, syntax_type="STRING")`**
    - Create a reference list containing values that can be referenced in detection rules. Supports STRING, CIDR, and REGEX syntax types.

- **`get_reference_list(name, project_id=None, customer_id=None, region=None, include_entries=True)`**
    - Get details and contents of a reference list including metadata and entries.

- **`update_reference_list(name, project_id=None, customer_id=None, region=None, entries=None, description=None)`**
    - Update the contents or description of an existing reference list.

### Feed Management Tools

- **`list_feeds(project_id=None, customer_id=None, region=None)`**
    - Lists all configured feeds in Chronicle, providing details such as feed name, status, log type, and source type.

- **`get_feed(feed_id, project_id=None, customer_id=None, region=None)`**
    - Get detailed information about a specific feed by ID, including connection settings, log type, state, and metadata.

- **`create_feed(display_name, feed_details, project_id=None, customer_id=None, region=None)`**
    - Creates a new feed configuration for ingesting data into Chronicle. Supports various feed types including HTTP, S3, GCS, and GCP SCC.

- **`update_feed(feed_id, display_name=None, feed_details=None, project_id=None, customer_id=None, region=None)`**
    - Modifies the configuration of an existing feed. Can update the display name, connection settings, or other properties.

- **`enable_feed(feed_id, project_id=None, customer_id=None, region=None)`**
    - Activates a feed that is currently in the INACTIVE state, allowing it to resume data ingestion.

- **`disable_feed(feed_id, project_id=None, customer_id=None, region=None)`**
    - Stops data ingestion for a feed by setting its state to INACTIVE. The feed configuration remains but no new data will be processed.

- **`delete_feed(feed_id, project_id=None, customer_id=None, region=None)`**
    - Permanently removes a feed configuration from Chronicle. This action cannot be undone.

- **`generate_feed_secret(feed_id, project_id=None, customer_id=None, region=None)`**
    - Creates a new authentication secret for feeds that support authentication (e.g., HTTP feeds with basic auth). This replaces any existing secret.

### API Capabilities

The MCP server provides the following capabilities:

1.  **Search Security Events**: Search for security events in Chronicle
2.  **Get Security Alerts**: Retrieve security alerts
3.  **Lookup Entity**: Look up entity information (IP, domain, hash, etc.)
4.  **List Security Rules**: List detection rules
5.  **Search Security Rules**: Searches detection rules using regex
6.  **Get IoC Matches**: Get Indicators of Compromise matches
7.  **Get Threat Intel**: Get AI-powered threat intelligence answers
8.  **Log Ingestion**: Ingest raw logs and UDM events
9.  **Parser Management**: Create, manage, and test log parsers
10. **Data Table Management**: Create and manage structured data tables for detection rules
11. **Reference List Management**: Create and manage reference lists for detection rules
12. **Feed Management**: Create, update, enable, disable, and delete data feeds

### Example

See `example.py` for a complete example of using the MCP server.

## Tool Categories and Use Cases

### Security Operations Tools
These tools focus on core security operations tasks:
- **Event Search & Investigation**: Use `search_security_events` to find security events using natural language queries
- **Alert Management**: Use `get_security_alerts` to retrieve and monitor security alerts
- **Entity Analysis**: Use `lookup_entity` to investigate IPs, domains, hashes, and other indicators
- **Rule Management**: Use `list_security_rules` and `search_security_rules` to manage detection rules
- **Threat Intelligence**: Use `get_ioc_matches` and `get_threat_intel` for IOC analysis and AI-powered insights

### Data Ingestion & Parsing Tools
These tools help you get data into Chronicle:
- **Raw Log Ingestion**: Use `ingest_raw_log` for logs in their original format (JSON, XML, CEF, etc.)
- **UDM Event Ingestion**: Use `ingest_udm_events` for pre-formatted security events
- **Parser Development**: Use the parser management tools to create custom parsers for unique log formats
- **Testing**: Use `run_parser_against_sample_logs` to validate parser logic before deployment
- **Feed Management**: Use feed management tools (`list_feeds`, `create_feed`, etc.) to configure and manage data collection sources

### Context Data Management Tools
These tools help you maintain reference data for enhanced detections:
- **Data Tables**: Use for structured data with multiple columns (e.g., asset inventories with criticality ratings)
- **Reference Lists**: Use for simple lists of values (e.g., IP addresses, domains, usernames)
- **Detection Enhancement**: Both data tables and reference lists can be referenced in detection rules to make them more dynamic and maintainable

## Configuration

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

**NOTE:** For OSX users, if you used [this one-liner](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to install uv, use the full path to the uv binary for the "command" value below, as uv will not be placed in the system path for Claude to use! For example: `/Users/yourusername/.local/bin/uv` instead of just `uv`.

#### Using uv (Recommended)

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/secops/secops_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "${CHRONICLE_PROJECT_ID}",
        "CHRONICLE_CUSTOMER_ID": "${CHRONICLE_CUSTOMER_ID}",
        "CHRONICLE_REGION": "${CHRONICLE_REGION}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

#### Using pip

You can also use pip instead of uv to install and run the MCP server:

```json
{
  "mcpServers": {
    "secops": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /path/to/the/repo/server/secops && pip install -e . && secops_mcp"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "${CHRONICLE_PROJECT_ID}",
        "CHRONICLE_CUSTOMER_ID": "${CHRONICLE_CUSTOMER_ID}",
        "CHRONICLE_REGION": "${CHRONICLE_REGION}"
      },
      "disabled": false,
      "autoApprove": [
        "get_ioc_matches",
        "search_security_events",
        "get_security_alerts"
      ],
      "alwaysAllow": [
        "get_ioc_matches"
      ]
    }
  }
}
```

#### When to use uv vs pip

- **uv**: Recommended for most users as it provides faster package installation, better dependency resolution, and supports loading environment variables from a file with the `--env-file` option.
- **pip**: Use when you prefer the standard Python package manager or when you need specific environment setup requirements.

### Environment Variable Setup

Set up these environment variables in your system:

**For macOS/Linux:**
```bash
export CHRONICLE_PROJECT_ID="your-google-cloud-project-id"
export CHRONICLE_CUSTOMER_ID="your-chronicle-customer-id"
export CHRONICLE_REGION="us"
```

**For Windows PowerShell:**
```powershell
$Env:CHRONICLE_PROJECT_ID = "your-google-cloud-project-id"
$Env:CHRONICLE_CUSTOMER_ID = "your-chronicle-customer-id"
$Env:CHRONICLE_REGION = "us"
```

The `CHRONICLE_REGION` can be one of:
- `us` - United States (default)
- `eu` - Europe
- `asia` - Asia-Pacific

## License

Apache 2.0

## Development

The project is structured as follows:

- `server.py`: Main MCP server implementation
- `example.py`: Example usage of the MCP server 
