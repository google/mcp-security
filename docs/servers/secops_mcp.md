# Chronicle Security Operations (SecOps) MCP Server

This server provides tools for interacting with Chronicle Security Operations using the `secops-py` library.

> This MCP server is built on top of the official [Google SecOps SDK for Python](https://github.com/google/secops-wrapper), which provides a comprehensive wrapper for Google Security Operations APIs.

## Configuration

### Prerequisites

1. **Chronicle Security Operations Account** - You need access to a Chronicle instance
2. **Google Cloud Project** - A project with Chronicle API enabled
3. **API Credentials** - Authentication credentials with appropriate permissions

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

```json
"secops": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops/secops_mcp",
        "run",
        "server.py"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-gcp-project-id",
        "CHRONICLE_CUSTOMER_ID": "your-chronicle-customer-id",
        "CHRONICLE_REGION": "us"
      },
      "disabled": false,
      "autoApprove": []
    }
```

#### `--env-file`

Recommended: use the `--env-file` option in `uv` to move your secrets to an `.env` file for environment variables. You can create this file or use system environment variables as described below.

Your revised config would then be:

```json
      ...
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/secops/secops_mcp",
        "run",
        "--env-file",
        "/path/to/the/repo/.env",
        "server.py"
      ],
      "env": {},
      ...
```

Example .env file:
```
CHRONICLE_PROJECT_ID=your-gcp-project-id
CHRONICLE_CUSTOMER_ID=your-chronicle-customer-id
CHRONICLE_REGION=us
```

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

For more detailed instructions on setting up environment variables, refer to the [usage guide](../usage_guide.md#setting-up-environment-variables).

### Parameter-Based Authentication

Each tool accepts optional parameters for authentication, allowing dynamic configuration:

```
search_security_events(
  text="suspicious PowerShell execution",
  project_id="different-project-id",
  customer_id="different-customer-id",
  region="eu"
)
```

### Required Permissions

The service account or user credentials need the following Chronicle roles:
- `roles/chronicle.viewer` - For read-only operations
- `roles/chronicle.admin` - For administrative operations

## Tools

- **`search_security_events(text, project_id=None, customer_id=None, hours_back=24, max_events=100, region=None)`**
    - **Description:** Searches for security events in Chronicle using natural language. Translates the natural language query (`text`) into a UDM query and executes it.
    - **Parameters:**
        - `text` (required): Natural language description of the events to find.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `max_events` (optional): Maximum number of events to return (default: 100).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the generated `udm_query` and the `events` results.
    - **Return Example:**
      ```json
      {
        "udm_query": "metadata.event_type = \"NETWORK_HTTP\" metadata.product_name = \"Proxy\"",
        "events": [
          {
            "id": "event-id-123",
            "timestamp": "2023-09-15T14:30:45Z",
            "principal": {
              "hostname": "user-workstation",
              "ip": "10.0.0.12"
            },
            "target": {
              "hostname": "suspicious-domain.com",
              "ip": "203.0.113.100"
            },
            "network": {
              "http": {
                "method": "GET",
                "user_agent": "Mozilla/5.0"
              }
            },
            "metadata": {
              "event_type": "NETWORK_HTTP",
              "product_name": "Proxy"
            }
          }
        ]
      }
      ```

- **`get_security_alerts(project_id=None, customer_id=None, hours_back=24, max_alerts=10, status_filter='feedback_summary.status != "CLOSED"', region=None)`**
    - **Description:** Retrieves security alerts from Chronicle, filtered by time range and status.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `max_alerts` (optional): Maximum number of alerts to return (default: 10).
        - `status_filter` (optional): Query string to filter alerts by status (default: excludes closed alerts).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string listing the found security alerts.
    - **Return Example:**
      ```
      ALERT ID: a12b3c45
      RULE NAME: Potential Data Exfiltration
      SEVERITY: High
      CREATION TIME: 2023-09-15T12:34:56Z
      STATUS: NEW
      DESCRIPTION: Large outbound data transfer to rare external domain
      AFFECTED ASSETS: ['workstation-1234', '10.0.0.25']

      ALERT ID: d67e8f90
      RULE NAME: Suspicious PowerShell Command
      SEVERITY: Medium
      CREATION TIME: 2023-09-15T10:11:12Z
      STATUS: IN_PROGRESS
      DESCRIPTION: PowerShell execution with encoded command parameter
      AFFECTED ASSETS: ['admin-laptop', '10.0.0.42']
      ```

- **`lookup_entity(entity_value, project_id=None, customer_id=None, hours_back=24, region=None)`**
    - **Description:** Looks up an entity (IP, domain, hash, etc.) in Chronicle.
    - **Parameters:**
        - `entity_value` (required): Value to look up (IP, domain, hash, etc.).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string summarizing the entity information and associated alerts.
    - **Return Example:**
      ```
      ENTITY: 203.0.113.100 (IP Address)
      RISK SCORE: 7.5 (High)
      CLASSIFICATION: Known Command & Control Server
      FIRST SEEN: 2023-09-10T08:15:30Z
      LAST SEEN: 2023-09-15T14:22:10Z

      ASSOCIATED ALERTS:
      - Potential C2 Communication (High) - 2023-09-15T14:22:10Z
      - Suspicious Outbound Connection (Medium) - 2023-09-12T09:30:45Z

      RECENT ACTIVITIES:
      - 12 DNS resolution requests from 3 internal hosts
      - 8 blocked connection attempts from 2 internal hosts
      - 2 successful connections from workstation-1234
      ```

- **`list_security_rules(project_id=None, customer_id=None, region=None)`**
    - **Description:** Lists security detection rules from Chronicle.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the raw API response with the list of rules.
    - **Return Example:**
      ```json
      {
        "rules": [
          {
            "ruleId": "ru_123456",
            "ruleName": "Potential Data Exfiltration",
            "versionId": "rv_123456",
            "metadata": {
              "author": "Chronicle Security",
              "description": "Detects large outbound data transfers to rare domains",
              "severity": "HIGH"
            },
            "enabledAt": "2023-05-12T00:00:00Z",
            "type": "RULE_TYPE_RETROHUNT"
          },
          {
            "ruleId": "ru_789012",
            "ruleName": "Suspicious PowerShell Execution",
            "versionId": "rv_789012",
            "metadata": {
              "author": "Internal SOC",
              "description": "Detects PowerShell execution with encoding or obfuscation",
              "severity": "MEDIUM"
            },
            "enabledAt": "2023-07-25T00:00:00Z",
            "type": "RULE_TYPE_REAL_TIME"
          }
        ]
      }
      ```

- **`get_ioc_matches(project_id=None, customer_id=None, hours_back=24, max_matches=20, region=None)`**
    - **Description:** Retrieves Indicators of Compromise (IoCs) matches from Chronicle within a specified time range.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `hours_back` (optional): How many hours to look back (default: 24).
        - `max_matches` (optional): Maximum number of matches to return (default: 20).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string listing the found IoC matches.
    - **Return Example:**
      ```
      IOC MATCH:
      INDICATOR: evil-domain.com (Domain)
      CATEGORY: Command & Control
      SOURCE: AlienVault OTX
      SEVERITY: High
      MATCHED EVENT: DNS Query from workstation-1234 at 2023-09-15T11:22:33Z

      IOC MATCH:
      INDICATOR: 4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s (File Hash)
      CATEGORY: Malware
      SOURCE: VirusTotal
      SEVERITY: Critical
      MATCHED EVENT: Process execution on server-5678 at 2023-09-15T09:18:27Z
      ```

- **`get_threat_intel(query, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get answers to general security domain questions and specific threat intelligence information using Chronicle's AI capabilities.
    - **Parameters:**
        - `query` (required): The security or threat intelligence question to ask.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted text response with information about the requested threat intelligence topic.
    - **Return Example:**
      ```
      The threat actor APT28 (also known as Fancy Bear, Sofacy, or Strontium) is a
      Russian state-sponsored advanced persistent threat group associated with
      Russia's military intelligence agency, the GRU.

      Key characteristics:
      - Active since approximately 2004
      - Primarily targets government, military, and security organizations
      - Known for spear-phishing campaigns and exploitation of zero-day vulnerabilities
      - Has been linked to major operations including the 2016 DNC hack and Olympics-related attacks

      Common TTPs include:
      - Spear-phishing with malicious attachments
      - Credential harvesting through fake login pages
      - Use of custom malware including X-Tunnel, X-Agent, and Lojax
      - Zero-day exploitation
      ```

### Log Ingestion Tools

- **`ingest_raw_log(log_type, log_message, project_id=None, customer_id=None, region=None, forwarder_id=None, labels=None, log_entry_time=None, collection_time=None)`**
    - **Description:** Ingest raw logs directly into Chronicle SIEM. Allows ingestion of raw log data in various formats (JSON, XML, CEF, etc.) into Chronicle for parsing and normalization into UDM format. Supports both single log and batch ingestion.
    - **Parameters:**
        - `log_type` (required): Chronicle log type identifier (e.g., "OKTA", "WINEVTLOG_XML", "AWS_CLOUDTRAIL")
        - `log_message` (required): Log content as string or list of strings for batch ingestion
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `forwarder_id` (optional): Custom forwarder ID for log routing
        - `labels` (optional): Custom labels to attach to ingested logs for categorization
        - `log_entry_time` (optional): ISO 8601 timestamp when the log was originally generated
        - `collection_time` (optional): ISO 8601 timestamp when the log was collected
    - **Returns:** Success message with operation details, including any operation IDs for tracking
    - **Use Cases:** Ingest OKTA authentication logs, feed custom application logs, batch ingest historical logs, import logs from external SIEM systems

- **`ingest_udm_events(udm_events, project_id=None, customer_id=None, region=None)`**
    - **Description:** Ingest UDM events directly into Chronicle SIEM. Allows direct ingestion of events already formatted in Chronicle's Unified Data Model (UDM) format, bypassing the parsing stage.
    - **Parameters:**
        - `udm_events` (required): Single UDM event or list of UDM events (properly formatted UDM structures)
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
    - **Returns:** Success message with details about ingested events, including generated event IDs
    - **Use Cases:** Ingest network connection events from custom tools, feed process execution events from custom EDR, create synthetic events for testing, migrate historical security events

- **`get_available_log_types(project_id=None, customer_id=None, region=None, search_term=None)`**
    - **Description:** Get available log types supported by Chronicle for ingestion. Retrieves the list of log types that Chronicle can parse and ingest, optionally filtered by a search term.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `search_term` (optional): Filter log types by name or description containing this term
    - **Returns:** Formatted list of available log types with their IDs and descriptions
    - **Use Cases:** Find correct log type identifier for specific vendor, discover Chronicle's parsing capabilities, validate log type names before ingestion

### Parser Management Tools

- **`create_parser(log_type, parser_code, project_id=None, customer_id=None, region=None, validated_on_empty_logs=True)`**
    - **Description:** Create a new parser for a specific log type in Chronicle. Creates a custom parser using Chronicle's parser configuration language to transform raw logs into Chronicle's Unified Data Model (UDM) format.
    - **Parameters:**
        - `log_type` (required): Chronicle log type identifier for this parser (e.g., "CUSTOM_APP", "WINDOWS_AD")
        - `parser_code` (required): Parser configuration code using Chronicle's parser DSL
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `validated_on_empty_logs` (optional): Whether to validate parser on empty log samples (default: True)
    - **Returns:** Success message with the created parser ID and details
    - **Use Cases:** Create parsers for custom application logs, parse proprietary security tool outputs, handle modified versions of standard log formats

- **`get_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get details of a specific parser including its configuration and metadata.
    - **Parameters:**
        - `log_type` (required): Chronicle log type identifier
        - `parser_id` (required): Unique identifier of the parser to retrieve
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
    - **Returns:** Parser details including configuration, metadata, and status
    - **Use Cases:** Review parser configurations, debug parsing issues, verify parser settings

- **`activate_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Activate a parser, making it the active parser for the specified log type.
    - **Parameters:**
        - `log_type` (required): Chronicle log type identifier
        - `parser_id` (required): Unique identifier of the parser to activate
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
    - **Returns:** Success message confirming parser activation
    - **Use Cases:** Deploy new parsers to production, switch between parser versions, enable custom log processing

- **`deactivate_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Deactivate a parser, stopping it from processing incoming logs of the specified type.
    - **Parameters:**
        - `log_type` (required): Chronicle log type identifier
        - `parser_id` (required): Unique identifier of the parser to deactivate
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
    - **Returns:** Success message confirming parser deactivation
    - **Use Cases:** Disable problematic parsers, perform maintenance, rollback parser deployments

- **`run_parser_against_sample_logs(log_type, parser_code, sample_logs, project_id=None, customer_id=None, region=None, parser_extension_code=None, statedump_allowed=False)`**
    - **Description:** Test parser configuration against sample log entries to validate parsing logic before deployment.
    - **Parameters:**
        - `log_type` (required): Chronicle log type identifier
        - `parser_code` (required): Parser configuration code to test
        - `sample_logs` (required): List of sample log entries to test parsing against
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `parser_extension_code` (optional): Additional parser extension code
        - `statedump_allowed` (optional): Whether to allow state dumps during testing (default: False)
    - **Returns:** Parsing results showing how sample logs would be processed
    - **Use Cases:** Validate parser logic before deployment, debug parsing issues, test parser modifications

### Data Table Management Tools

- **`create_data_table(name, description, header, project_id=None, customer_id=None, region=None, rows=None)`**
    - **Description:** Create a structured data table that can be referenced in detection rules. Supports multiple column types (STRING, CIDR, INT64, BOOL).
    - **Parameters:**
        - `name` (required): Unique name for the data table
        - `description` (required): Description of the data table's purpose
        - `header` (required): List defining column names and types
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `rows` (optional): Initial data rows to populate the table
    - **Returns:** Success message with data table creation details
    - **Use Cases:** Create asset inventories with criticality ratings, maintain lists of approved software, store network zone definitions for detection rules

- **`add_rows_to_data_table(table_name, rows, project_id=None, customer_id=None, region=None)`**
    - **Description:** Add new rows to an existing data table, expanding the dataset available for detection rules.
    - **Parameters:**
        - `table_name` (required): Name of the existing data table
        - `rows` (required): List of data rows to add to the table
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
    - **Returns:** Success message with details of added rows
    - **Use Cases:** Update asset inventories, add new approved software entries, expand network zone definitions

- **`list_data_table_rows(table_name, project_id=None, customer_id=None, region=None, max_rows=50)`**
    - **Description:** List rows in a data table to review contents and verify data integrity.
    - **Parameters:**
        - `table_name` (required): Name of the data table to list
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `max_rows` (optional): Maximum number of rows to return (default: 50)
    - **Returns:** Formatted list of data table rows
    - **Use Cases:** Review data table contents, verify data accuracy, troubleshoot detection rule issues

- **`delete_data_table_rows(table_name, row_ids, project_id=None, customer_id=None, region=None)`**
    - **Description:** Delete specific rows from a data table based on their row IDs.
    - **Parameters:**
        - `table_name` (required): Name of the data table
        - `row_ids` (required): List of row IDs to delete
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
    - **Returns:** Success message with details of deleted rows
    - **Use Cases:** Remove obsolete asset entries, clean up data table contents, remove false positive entries

### Reference List Management Tools

- **`create_reference_list(name, description, entries, project_id=None, customer_id=None, region=None, syntax_type="STRING")`**
    - **Description:** Create a reference list containing values that can be referenced in detection rules. Supports STRING, CIDR, and REGEX syntax types.
    - **Parameters:**
        - `name` (required): Unique name for the reference list
        - `description` (required): Description of the reference list's purpose
        - `entries` (required): List of values to include in the reference list
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `syntax_type` (optional): Type of entries (STRING, CIDR, REGEX) (default: STRING)
    - **Returns:** Success message with reference list creation details
    - **Use Cases:** Create allowlists of IP addresses, maintain lists of known-good domains, store user groups for detection rules

- **`get_reference_list(name, project_id=None, customer_id=None, region=None, include_entries=True)`**
    - **Description:** Get details and contents of a reference list including metadata and entries.
    - **Parameters:**
        - `name` (required): Name of the reference list to retrieve
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `include_entries` (optional): Whether to include list entries in response (default: True)
    - **Returns:** Reference list details including metadata and entries
    - **Use Cases:** Review reference list contents, verify list accuracy, troubleshoot detection rule references

- **`update_reference_list(name, project_id=None, customer_id=None, region=None, entries=None, description=None)`**
    - **Description:** Update the contents or description of an existing reference list.
    - **Parameters:**
        - `name` (required): Name of the reference list to update
        - `project_id` (optional): Google Cloud project ID (defaults to environment config)
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config)
        - `region` (optional): Chronicle region (defaults to environment config or 'us')
        - `entries` (optional): New list entries to replace existing ones
        - `description` (optional): New description for the reference list
    - **Returns:** Success message with update details
    - **Use Cases:** Update IP allowlists, modify domain lists, refresh user group memberships

## Usage Examples

### Example 1: Natural Language Security Event Search

```
User: Can you find security events related to PowerShell running encoded commands in the last 48 hours?

AI uses: search_security_events(
  text="PowerShell encoded commands",
  hours_back=48
)

AI: I found 5 instances of PowerShell with encoded commands:

1. 2023-09-15T09:12:34Z - User admin-john on workstation-1234
   Command: powershell.exe -EncodedCommand ZQBjAGgAbwAgACIASABlAGwAbABvACIAIAA=

2. 2023-09-14T15:30:22Z - System account on server-db01
   Command: powershell.exe -enc <base64 data>
   [Detected by rule: "Suspicious PowerShell Activity"]
```

### Example 2: Entity Investigation Workflow

```
User: We've identified a suspicious IP 203.0.113.100 in our logs. Can you tell me what we know about it?

AI uses: lookup_entity("203.0.113.100")

AI: The IP 203.0.113.100 is a high-risk (score 7.5) entity classified as a known C2 server.
It was first seen in your environment 5 days ago and last seen today.

It's associated with 2 alerts:
- "Potential C2 Communication" (High severity)
- "Suspicious Outbound Connection" (Medium severity)

Recent activity shows 12 DNS requests from 3 hosts, with 2 successful connections
from workstation-1234.

User: Can you find all the events related to this IP?

AI uses: search_security_events(
  text="communications with IP 203.0.113.100",
  hours_back=72
)

AI: [Displays detailed event information about all communications with this IP]
```

### Example 3: Alert Management

```
User: What security alerts have we received in the last 24 hours?

AI uses: get_security_alerts(hours_back=24)

AI: I found 3 open alerts from the last 24 hours:

1. Potential Data Exfiltration (High)
   Created: 2023-09-15T12:34:56Z
   Affected assets: workstation-1234, 10.0.0.25

2. Suspicious PowerShell Command (Medium)
   Created: 2023-09-15T10:11:12Z
   Affected assets: admin-laptop, 10.0.0.42

3. Unusual Authentication Pattern (Low)
   Created: 2023-09-15T08:07:06Z
   Affected assets: user-john, 10.0.0.35
```

### Example 4: Threat Intelligence Research

```
User: Can you tell me about the Lazarus Group threat actor?

AI uses: get_threat_intel(query="Provide information about the Lazarus Group threat actor")

AI: The Lazarus Group is a North Korean state-sponsored threat actor, also known as:
- Hidden Cobra
- Guardians of Peace
- APT38
- Zinc

Key characteristics:
- Active since at least 2009
- Primarily motivated by financial gain and intelligence gathering
- Known for high-profile attacks including the 2014 Sony Pictures hack, 2016 Bangladesh Bank heist, and various cryptocurrency exchange attacks
- Responsible for developing and deploying WannaCry ransomware

Their TTPs include:
- Sophisticated social engineering and spear-phishing
- Custom malware frameworks including BLINDINGCAN and CROWDEDFLOUNDER
- Watering hole attacks against specific industry sectors
- Advanced persistent access into compromised networks

The group continues to evolve tactics and primarily targets financial institutions, cryptocurrency exchanges, and organizations in sectors of strategic interest to North Korea.
```

### Example 5: Log Ingestion and Parser Management Workflow

```
User: I need to ingest custom application logs from our fraud detection system into Chronicle.

AI: I can help you set up log ingestion for your fraud detection system. Let me first check what log types are available:

AI uses: get_available_log_types(search_term="fraud")

AI: I don't see a specific fraud detection log type. Let's check all available log types to find the closest match or we can create a custom parser.

AI uses: get_available_log_types()

AI: Based on the available log types, we can either use a generic format like "JSON" or create a custom parser for your specific fraud logs. Can you provide a sample log entry?

User: Here's a sample log: {"timestamp":"2023-09-15T10:30:00Z","user_id":"12345","action":"transaction","amount":1500.00,"risk_score":8.5,"blocked":true}

AI: Perfect! This looks like JSON format. Let me ingest this log using the JSON log type:

AI uses: ingest_raw_log(
  log_type="JSON",
  log_message='{"timestamp":"2023-09-15T10:30:00Z","user_id":"12345","action":"transaction","amount":1500.00,"risk_score":8.5,"blocked":true}',
  labels={"source": "fraud_detection", "environment": "production"}
)

AI: Successfully ingested 1 log of type JSON. If you need more sophisticated parsing to extract specific fields into UDM format, I can help create a custom parser.

User: Yes, let's create a parser to properly structure these fraud logs.

AI uses: create_parser(
  log_type="FRAUD_DETECTION",
  parser_code='''
  filter {
    json {
      source => "message"
    }
    mutate {
      replace => {
        "event1.idm.read_only_udm.metadata.event_type" => "GENERIC_EVENT"
        "event1.idm.read_only_udm.metadata.product_name" => "Fraud Detection System"
        "event1.idm.read_only_udm.metadata.vendor_name" => "Internal"
        "event1.idm.read_only_udm.principal.user.userid" => "%{user_id}"
        "event1.idm.read_only_udm.metadata.description" => "Fraud detection event for user %{user_id}"
      }
    }
    if [risk_score] {
      if [risk_score] >= 7 {
        mutate {
          replace => {
            "event1.idm.read_only_udm.security_result.severity" => "HIGH"
          }
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
)

AI: Successfully created parser for FRAUD_DETECTION log type. Now let me activate it:

AI uses: activate_parser(log_type="FRAUD_DETECTION", parser_id="[parser-id]")

AI: Parser activated! Now you can ingest fraud detection logs using the FRAUD_DETECTION log type and they'll be properly parsed into UDM format.
```

### Example 6: Data Table and Reference List Management

```
User: I want to create a data table of our critical assets and a reference list of approved IP addresses for detection rules.

AI: I'll help you create both. Let's start with the critical assets data table:

AI uses: create_data_table(
  name="critical_assets",
  description="Critical assets inventory with risk ratings",
  header=[
    {"name": "hostname", "type": "STRING"},
    {"name": "ip_address", "type": "STRING"},
    {"name": "criticality", "type": "STRING"},
    {"name": "owner", "type": "STRING"},
    {"name": "risk_score", "type": "INT64"}
  ],
  rows=[
    ["server-db01", "10.0.1.10", "HIGH", "Database Team", 9],
    ["server-web01", "10.0.1.20", "MEDIUM", "Web Team", 6],
    ["server-file01", "10.0.1.30", "HIGH", "IT Team", 8]
  ]
)

AI: Successfully created the critical_assets data table with 3 initial entries. Now let's create the approved IP addresses reference list:

AI uses: create_reference_list(
  name="approved_ips",
  description="Approved IP addresses for internal communication",
  entries=[
    "10.0.0.0/8",
    "192.168.0.0/16",
    "172.16.0.0/12",
    "203.0.113.0/24"
  ],
  syntax_type="CIDR"
)

AI: Successfully created the approved_ips reference list with CIDR entries. These can now be used in YARA-L detection rules.

User: Can you show me what's in the critical assets table?

AI uses: list_data_table_rows(table_name="critical_assets")

AI: Here are the current entries in the critical_assets table:
1. server-db01 (10.0.1.10) - HIGH criticality, Risk Score: 9, Owner: Database Team
2. server-web01 (10.0.1.20) - MEDIUM criticality, Risk Score: 6, Owner: Web Team  
3. server-file01 (10.0.1.30) - HIGH criticality, Risk Score: 8, Owner: IT Team

User: I need to add a new server to the critical assets.

AI uses: add_rows_to_data_table(
  table_name="critical_assets",
  rows=[
    ["server-backup01", "10.0.1.40", "HIGH", "Backup Team", 9]
  ]
)

AI: Successfully added server-backup01 to the critical_assets table. You can now reference this data table in detection rules to identify events affecting critical assets and apply appropriate risk scoring.
```

## Additional Resources

- [Chronicle API Documentation](https://cloud.google.com/chronicle/docs/reference/rest)
- [UDM Schema Reference](https://cloud.google.com/chronicle/docs/reference/udm-field-list)
- [Chronicle Security Operations Overview](https://cloud.google.com/chronicle/docs/overview)
- [Chronicle Query Language Syntax](https://cloud.google.com/chronicle/docs/reference/yara-l-2-0-syntax)
