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
      }
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
# Optional: Uncomment to use service account authentication
# SECOPS_SA_PATH=/path/to/service-account-key.json
```

### Environment Variable Setup

Set up these environment variables in your system:

**For macOS/Linux:**
```bash
export CHRONICLE_PROJECT_ID="your-google-cloud-project-id"
export CHRONICLE_CUSTOMER_ID="your-chronicle-customer-id"
export CHRONICLE_REGION="us"
# Optional: Set this to use service account authentication
# export SECOPS_SA_PATH="/path/to/service-account-key.json"
```

**For Windows PowerShell:**
```powershell
$Env:CHRONICLE_PROJECT_ID = "your-google-cloud-project-id"
$Env:CHRONICLE_CUSTOMER_ID = "your-chronicle-customer-id"
$Env:CHRONICLE_REGION = "us"
# Optional: Set this to use service account authentication
# $Env:SECOPS_SA_PATH = "C:\path\to\service-account-key.json"
```

The `CHRONICLE_REGION` can be one of:
- `us` - United States (default)
- `eu` - Europe
- `asia` - Asia-Pacific

For more detailed instructions on setting up environment variables, refer to the [usage guide](../usage_guide.md#setting-up-environment-variables).

### Authentication

The MCP server supports two authentication methods:

#### 1. Application Default Credentials (ADC) - Default

By default, the server uses Google Cloud Application Default 
Credentials. Authenticate using:

```bash
gcloud auth application-default login
```

This method is recommended for local development and interactive use.

#### 2. Service Account Authentication - Optional

For automated environments, CI/CD pipelines, or when ADC is not 
available, you can use service account authentication by setting the 
`SECOPS_SA_PATH` environment variable:

**For macOS/Linux:**
```bash
export SECOPS_SA_PATH="/path/to/service-account-key.json"
```

**For Windows PowerShell:**
```powershell
$Env:SECOPS_SA_PATH = "C:\path\to\service-account-key.json"
```

The service account must have the appropriate Chronicle permissions 
(see Required Permissions section below).

**Note:** If `SECOPS_SA_PATH` is set, it takes precedence over ADC. 
The server will automatically detect and use the service account for 
all API calls.

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

- **`update_rule(rule_id, rule_text, project_id=None, customer_id=None, region=None)`**
    - **Description:** Updates an existing YARA-L 2.0 detection rule in place in Chronicle SIEM, preserving its rule ID, deployment state, and revision history.
    - **Parameters:**
        - `rule_id` (required): Unique ID of the rule to update (e.g., `"ru_<UUID>"`).
        - `rule_text` (required): Complete, updated YARA-L 2.0 rule definition.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Formatted string with the rule ID, updated revision ID, and rule name.

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

- **`create_retrohunt(rule_id, start_time, end_time, project_id=None, customer_id=None, region=None)`**
    - **Description:** Creates a retrohunt operation to run a detection rule against historical data for threat hunting. Retrohunts enable identifying past security incidents that match current detection logic or newly discovered threat patterns.
    - **Parameters:**
        - `rule_id` (required): Unique ID of the rule to run against historical data (e.g., "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").
        - `start_time` (required): Start of time range in ISO format (e.g., "2024-01-01T00:00:00Z").
        - `end_time` (required): End of time range in ISO format (e.g., "2024-01-08T00:00:00Z").
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing operation details including operation_id for tracking status.
    - **Return Example:**
      ```json
      {
        "operation_id": "oh_077d5ac9-05f1-4331-b33b-d2ff4b09ee50",
        "operation_name": "projects/.../operations/oh_077d5ac9-05f1-4331-b33b-d2ff4b09ee50",
        "rule_id": "ru_19fa6159-b7be-48c0-b822-8a29f749fa0c",
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-08T00:00:00Z",
        "status": "success",
        "message": "Retrohunt created successfully. Use get_retrohunt to check status.",
        "note": "Retrohunts may take minutes to hours depending on data volume."
      }
      ```

- **`get_retrohunt(rule_id, operation_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Retrieves the status and results of a retrohunt operation. Use this to monitor progress of long-running threat hunting operations and access historical detection results.
    - **Parameters:**
        - `rule_id` (required): Rule ID used to create the retrohunt (e.g., "ru_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").
        - `operation_id` (required): Operation ID returned from create_retrohunt (e.g., "oh_077d5ac9-05f1-4331-b33b-d2ff4b09ee50").
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing operation status, progress, and results if complete.
    - **Return Example:**
      ```json
      {
        "operation_id": "oh_077d5ac9-05f1-4331-b33b-d2ff4b09ee50",
        "rule_id": "ru_19fa6159-b7be-48c0-b822-8a29f749fa0c",
        "done": false,
        "status": {},
        "create_time": "2024-01-15T10:30:00Z",
        "progress_percentage": 45,
        "raw_response": { ... }
      }
      ```

- **`search_rule_alerts(start_time, end_time, max_alerts=10, project_id=None, customer_id=None, region=None)`**
    - **Description:** Searches for alerts generated by detection rules across a specified time range. Returns alerts grouped by rule with event samples and metadata.
    - **Parameters:**
        - `start_time` (required): Start of time range in ISO format (e.g., "2024-01-01T00:00:00Z").
        - `end_time` (required): End of time range in ISO format (e.g., "2024-01-02T00:00:00Z").
        - `max_alerts` (optional): Maximum number of alerts to return (default: 10).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing rule alerts grouped by rule and a truncation flag.
    - **Return Example:**
      ```json
      {
        "ruleAlerts": [
          {
            "ruleMetadata": {
              "ruleId": "ru_123456",
              "properties": {
                "name": "Suspicious PowerShell Execution",
                "severity": "MEDIUM"
              }
            },
            "alerts": [
              {
                "id": "alert-abc123",
                "detectionTimestamp": "2024-01-01T14:30:00Z",
                "alertingType": "RULE_MATCH",
                "resultEvents": { ... }
              }
            ]
          }
        ],
        "tooManyAlerts": false
      }
      ```

- **`list_curated_rules(project_id=None, customer_id=None, region=None, page_size=100, page_token=None, as_list=False)`**
    - **Description:** List all curated detection rules available in Chronicle. Retrieves pre-built detection rules provided by Google that cover common security threats and attack patterns.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
        - `page_size` (optional): Maximum number of rules to return per page (default: 100).
        - `page_token` (optional): Token for retrieving next page of results.
        - `as_list` (optional): If True, automatically paginate and return all rules as a list (default: False).
    - **Returns:** Dictionary containing curated rules and pagination metadata.
    - **Return Example:**
      ```json
      {
        "curatedRules": [
          {
            "name": "projects/.../curatedRules/ur_ttp_lol_Atbroker",
            "displayName": "Atbroker.exe Abuse",
            "description": "Detects abuse of Windows Atbroker.exe",
            "severity": "MEDIUM",
            "type": "MULTI_EVENT"
          }
        ],
        "nextPageToken": "token-for-next-page"
      }
      ```

- **`get_curated_rule(rule_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Retrieve specific curated rule details by rule ID. Fetches complete definition and metadata for a specific Google-curated detection rule.
    - **Parameters:**
        - `rule_id` (required): Unique identifier of the curated rule.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing complete curated rule information.

- **`get_curated_rule_by_name(display_name, project_id=None, customer_id=None, region=None)`**
    - **Description:** Find curated rule by display name. Searches for a curated rule matching the specified human-readable name.
    - **Parameters:**
        - `display_name` (required): Display name of the curated rule to find.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing curated rule information if found.

- **`search_curated_detections(rule_id, start_time, end_time, project_id=None, customer_id=None, region=None, list_basis=None, alert_state=None, page_size=100, page_token=None)`**
    - **Description:** Search detections generated by a specific curated rule within a time range. Useful for investigating threats detected by Google-curated detection content.
    - **Parameters:**
        - `rule_id` (required): Unique identifier of the curated rule.
        - `start_time` (required): Start of search time range in ISO 8601 format (e.g., "2025-01-20T00:00:00Z").
        - `end_time` (required): End of search time range in ISO 8601 format.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
        - `list_basis` (optional): Basis for listing detections ("DETECTION_TIME" or "CREATED_TIME").
        - `alert_state` (optional): Filter by alert state ("ALERTING" or "NOT_ALERTING").
        - `page_size` (optional): Maximum number of detections to return (default: 100).
        - `page_token` (optional): Token for retrieving next page.
    - **Returns:** Dictionary containing detections and pagination metadata.

- **`list_curated_rule_sets(project_id=None, customer_id=None, region=None, page_size=100, page_token=None, as_list=False)`**
    - **Description:** List all curated rule sets available in Chronicle. Retrieves collections of related curated rules grouped by threat category or data source.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
        - `page_size` (optional): Maximum number of rule sets to return (default: 100).
        - `page_token` (optional): Token for retrieving next page.
        - `as_list` (optional): If True, automatically paginate and return all rule sets as a list (default: False).
    - **Returns:** Dictionary containing rule sets and pagination metadata.

- **`get_curated_rule_set(rule_set_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Retrieve specific curated rule set details by ID. Provides information about rules included in the set and deployment options.
    - **Parameters:**
        - `rule_set_id` (required): Unique identifier of the curated rule set.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing complete rule set information.

- **`list_curated_rule_set_deployments(project_id=None, customer_id=None, region=None, page_size=100, page_token=None, as_list=False)`**
    - **Description:** List deployment status of all curated rule sets. Shows enabled status, precision level (broad/precise), and alerting configuration.
    - **Parameters:**
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
        - `page_size` (optional): Maximum number of deployments to return (default: 100).
        - `page_token` (optional): Token for retrieving next page.
        - `as_list` (optional): If True, automatically paginate and return all deployments as a list (default: False).
    - **Returns:** Dictionary containing deployment configurations with enabled status, precision level, and alerting settings.

- **`update_curated_rule_set_deployment(category_id, rule_set_id, precision, enabled, alerting, project_id=None, customer_id=None, region=None)`**
    - **Description:** Update deployment configuration for a curated rule set. Enables/disables rule sets, configures precision level (broad or precise), and controls alerting settings.
    - **Parameters:**
        - `category_id` (required): Category ID of the rule set.
        - `rule_set_id` (required): Unique identifier of the rule set.
        - `precision` (required): Detection precision level ("broad" or "precise").
        - `enabled` (required): Whether to enable the rule set for detection (boolean).
        - `alerting` (required): Whether to enable alerting for detections (boolean).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing updated deployment configuration.
    - **Note:** Precision modes:
        - **broad**: More detections, potentially higher false positive rate. Better for comprehensive threat hunting.
        - **precise**: Fewer detections, lower false positive rate. Better for production alerting.

### Rule Exclusions Management

- **`create_rule_exclusion(display_name, refinement_type, query, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create a new rule exclusion in Chronicle SIEM to filter out false positives or exclude specific events from triggering detections. Rule exclusions use UDM query syntax to define which events should be excluded from detection rules.
    - **Parameters:**
        - `display_name` (required): User-friendly name for the exclusion.
        - `refinement_type` (required): Type of exclusion refinement. Use "DETECTION_EXCLUSION" for detection exclusions.
        - `query` (required): UDM query defining which events to exclude (e.g., '(domain = "google.com")' or '(ip = "8.8.8.8")').
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the created exclusion details including name, display_name, and query.
    - **Return Example:**
      ```json
      {
        "name": "projects/123/locations/us/instances/456/findingsRefinements/excl-abc-123",
        "displayName": "Exclude Google Domain",
        "refinementType": "DETECTION_EXCLUSION",
        "query": "(domain = \"google.com\")",
        "createTime": "2024-01-15T10:30:00Z",
        "updateTime": "2024-01-15T10:30:00Z"
      }
      ```

- **`get_rule_exclusion(exclusion_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get detailed information about a specific rule exclusion by its ID, including display name, query, refinement type, and deployment status.
    - **Parameters:**
        - `exclusion_id` (required): Exclusion ID only (e.g., "excl-abc-123"), not the full resource name.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Complete exclusion details including query, refinement_type, and deployment configuration.
    - **Return Example:**
      ```json
      {
        "name": "projects/123/locations/us/instances/456/findingsRefinements/excl-abc-123",
        "displayName": "Exclude Google Domain",
        "refinementType": "DETECTION_EXCLUSION",
        "query": "(domain = \"google.com\")",
        "createTime": "2024-01-15T10:30:00Z",
        "updateTime": "2024-01-15T10:30:00Z"
      }
      ```

- **`list_rule_exclusions(page_size=None, page_token=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List all rule exclusions configured in Chronicle SIEM with pagination support for reviewing and managing exclusions.
    - **Parameters:**
        - `page_size` (optional): Maximum number of exclusions to return per page.
        - `page_token` (optional): Token for retrieving next page of results.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing exclusion data with pagination metadata.
    - **Return Example:**
      ```json
      {
        "findingsRefinements": [
          {
            "name": "projects/123/.../findingsRefinements/excl-abc-123",
            "displayName": "Exclude Google Domain",
            "refinementType": "DETECTION_EXCLUSION",
            "query": "(domain = \"google.com\")"
          },
          {
            "name": "projects/123/.../findingsRefinements/excl-def-456",
            "displayName": "Exclude Scanner IP",
            "refinementType": "DETECTION_EXCLUSION",
            "query": "(ip = \"192.168.1.100\")"
          }
        ],
        "nextPageToken": "token-for-next-page",
        "total_in_page": 2
      }
      ```

- **`patch_rule_exclusion(exclusion_id, display_name=None, query=None, update_mask=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Update an existing rule exclusion's properties including display name and query. Supports partial updates via update_mask to modify only specific fields.
    - **Parameters:**
        - `exclusion_id` (required): Unique identifier of the exclusion to update.
        - `display_name` (optional): New display name for the exclusion.
        - `query` (optional): New UDM query defining which events to exclude.
        - `update_mask` (optional): Comma-separated list of fields to update (e.g., "display_name,query").
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the updated exclusion details.
    - **Return Example:**
      ```json
      {
        "name": "projects/123/locations/us/instances/456/findingsRefinements/excl-abc-123",
        "displayName": "Updated Exclusion Name",
        "refinementType": "DETECTION_EXCLUSION",
        "query": "(domain = \"example.com\")",
        "updateTime": "2024-01-15T14:30:00Z"
      }
      ```

- **`update_rule_exclusion_deployment(exclusion_id, enabled, archived, detection_exclusion_application, project_id=None, customer_id=None, region=None)`**
    - **Description:** Manage deployment settings for a rule exclusion including enable/disable status, archive status, and which rules or rule sets the exclusion should be applied to.
    - **Parameters:**
        - `exclusion_id` (required): Unique identifier of the exclusion.
        - `enabled` (required): Whether the exclusion should be active.
        - `archived` (required): Whether the exclusion should be archived.
        - `detection_exclusion_application` (required): Configuration specifying which rules/rule sets to apply exclusion to. Example: `{"curatedRules": [], "curatedRuleSets": [], "rules": ["rule_123"]}`.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing the updated deployment configuration.
    - **Return Example:**
      ```json
      {
        "enabled": true,
        "archived": false,
        "detectionExclusionApplication": {
          "curatedRules": [],
          "curatedRuleSets": [],
          "rules": ["rule_123", "rule_456"]
        }
      }
      ```

- **`compute_rule_exclusion_activity(exclusion_id, start_time, end_time, project_id=None, customer_id=None, region=None)`**
    - **Description:** Calculate activity statistics for a rule exclusion showing how many events were excluded during the specified time period. Helps measure exclusion effectiveness and impact.
    - **Parameters:**
        - `exclusion_id` (required): Unique identifier of the exclusion.
        - `start_time` (required): Start of time period for activity calculation (timezone-aware datetime object).
        - `end_time` (required): End of time period for activity calculation (timezone-aware datetime object).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing activity statistics including count of excluded events.
    - **Return Example:**
      ```json
      {
        "count": 1247,
        "timeRange": {
          "startTime": "2024-01-01T00:00:00Z",
          "endTime": "2024-01-07T23:59:59Z"
        }
      }
      ```

### Watchlist Management

- **`create_watchlist(name, display_name, multiplying_factor, description, project_id=None, customer_id=None, region=None)`**
    - **Description:** Creates a new watchlist in Chronicle to track high-risk entities and apply risk score multipliers.
    - **Parameters:**
        - `name` (required): Unique identifier for the watchlist (e.g., "critical_threat_actors").
        - `display_name` (required): Human-readable name shown in the UI.
        - `multiplying_factor` (required): Risk score multiplier (e.g., 2.0 doubles the risk score).
        - `description` (required): Purpose and context of the watchlist.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary with created watchlist details including ID and configuration.
    - **Return Example:**
      ```json
      {
        "name": "projects/123/locations/us/instances/456/watchlists/abc-123-def",
        "displayName": "Critical Threat Actors",
        "description": "High-priority threat actors requiring immediate investigation",
        "multiplyingFactor": 2.0,
        "createTime": "2024-01-15T10:30:00Z",
        "updateTime": "2024-01-15T10:30:00Z"
      }
      ```

- **`update_watchlist(watchlist_id, display_name=None, description=None, multiplying_factor=None, entity_population_mechanism=None, watchlist_user_preferences=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Updates an existing watchlist's configuration, risk multiplier, or preferences.
    - **Parameters:**
        - `watchlist_id` (required): Watchlist ID only (e.g., "abc-123-def").
        - `display_name` (optional): New display name for the watchlist.
        - `description` (optional): New description for the watchlist.
        - `multiplying_factor` (optional): New risk score multiplier.
        - `entity_population_mechanism` (optional): Entity population configuration.
        - `watchlist_user_preferences` (optional): User preferences like pinning.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary with updated watchlist details.
    - **Return Example:**
      ```json
      {
        "name": "projects/123/locations/us/instances/456/watchlists/abc-123-def",
        "displayName": "Updated Critical Threat Actors",
        "description": "Increased multiplier due to active campaign",
        "multiplyingFactor": 3.0,
        "updateTime": "2024-01-15T14:22:00Z"
      }
      ```

- **`delete_watchlist(watchlist_id, force=False, project_id=None, customer_id=None, region=None)`**
    - **Description:** Permanently deletes a watchlist from Chronicle. Use caution as this operation cannot be undone.
    - **Parameters:**
        - `watchlist_id` (required): Watchlist ID only (e.g., "abc-123-def").
        - `force` (optional): Force deletion even if dependencies exist (default: False).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary confirming deletion or error details.
    - **Return Example:**
      ```json
      {
        "success": true,
        "watchlist_id": "abc-123-def",
        "message": "Watchlist deleted successfully"
      }
      ```

- **`get_watchlist(watchlist_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Retrieves detailed information about a specific watchlist including configuration and entity membership.
    - **Parameters:**
        - `watchlist_id` (required): Watchlist ID only (e.g., "abc-123-def").
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary with complete watchlist details.
    - **Return Example:**
      ```json
      {
        "name": "projects/123/locations/us/instances/456/watchlists/abc-123-def",
        "displayName": "Critical Threat Actors",
        "description": "High-priority threat actors",
        "multiplyingFactor": 2.0,
        "createTime": "2024-01-15T10:30:00Z",
        "updateTime": "2024-01-15T14:22:00Z",
        "entityCount": 42
      }
      ```

- **`list_watchlists(page_size=None, page_token=None, as_list=False, project_id=None, customer_id=None, region=None)`**
    - **Description:** Lists all watchlists in Chronicle with pagination support.
    - **Parameters:**
        - `page_size` (optional): Number of results per page for pagination.
        - `page_token` (optional): Token for fetching the next page of results.
        - `as_list` (optional): Return all results as a flat list (default: False).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary with watchlists array and pagination metadata.
    - **Return Example:**
      ```json
      {
        "watchlists": [
          {
            "name": "projects/123/locations/us/instances/456/watchlists/abc-123",
            "displayName": "Critical Threat Actors",
            "multiplyingFactor": 2.0
          },
          {
            "name": "projects/123/locations/us/instances/456/watchlists/def-456",
            "displayName": "Suspicious Domains",
            "multiplyingFactor": 1.5
          }
        ],
        "total_in_page": 2
      }
      ```

### Investigation Management

- **`list_investigations(page_size=50, page_token=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List all investigations in Chronicle instance. Returns investigation status, verdict, and confidence. Supports pagination.
    - **Parameters:**
        - `page_size` (optional): Number of investigations to return per page (default: 50).
        - `page_token` (optional): Token for pagination from previous response.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing list of investigations with status, verdict, confidence, and pagination token.

- **`get_investigation(investigation_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Retrieve specific investigation by ID. Returns detailed investigation information including status and verdict.
    - **Parameters:**
        - `investigation_id` (required): The unique identifier of the investigation to retrieve.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing detailed investigation information including display name, status, verdict, confidence, and timestamps.

- **`trigger_investigation(alert_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create new investigation for a specific alert. Returns created investigation details and trigger type.
    - **Parameters:**
        - `alert_id` (required): The unique identifier of the alert to investigate.
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing created investigation details including name, status, and trigger type.

- **`fetch_associated_investigations(detection_type, alert_ids=None, case_ids=None, association_limit_per_detection=5, project_id=None, customer_id=None, region=None)`**
    - **Description:** Retrieve investigations associated with alerts or cases. Supports filtering by detection type (ALERT or CASE). Returns investigation associations with verdict information.
    - **Parameters:**
        - `detection_type` (required): Type of detection to query. Valid values: "ALERT", "CASE", "DETECTION_TYPE_ALERT", "DETECTION_TYPE_CASE".
        - `alert_ids` (optional): List of alert IDs to query. Required if detection_type is ALERT.
        - `case_ids` (optional): List of case IDs to query. Required if detection_type is CASE.
        - `association_limit_per_detection` (optional): Maximum number of investigations to return per detection (default: 5).
        - `project_id` (optional): Google Cloud project ID (defaults to environment config).
        - `customer_id` (optional): Chronicle customer ID (defaults to environment config).
        - `region` (optional): Chronicle region (defaults to environment config or 'us').
    - **Returns:** Dictionary containing investigation associations grouped by detection ID, with verdict and confidence information.

### Dashboard Management Tools (Native SIEM Dashboards, Charts, Queries)

- **`list_dashboards(view=None, page_size=None, page_token=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List native SIEM dashboards in the Chronicle instance.
    - **Parameters:**
        - `view` (optional): NATIVE_DASHBOARD_VIEW_BASIC (default) or NATIVE_DASHBOARD_VIEW_FULL (includes `definition`).
        - `page_size` (optional): Maximum dashboards per page.
        - `page_token` (optional): `nextPageToken` from a previous call.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"nativeDashboards": [...], "nextPageToken": ..., "total_dashboards": N}` or `{"error": ...}`.

- **`get_dashboard(dashboard_id, view=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get a native SIEM dashboard by ID or resource name.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name (`projects/.../nativeDashboards/{id}`).
        - `view` (optional): NATIVE_DASHBOARD_VIEW_BASIC or NATIVE_DASHBOARD_VIEW_FULL.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The NativeDashboard resource or `{"error": ...}`.

- **`create_dashboard(display_name, description=None, access_type="DASHBOARD_PRIVATE", filters=None, dashboard=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create a new (empty) native SIEM dashboard.
    - **Parameters:**
        - `display_name` (required): Title shown to users.
        - `description` (optional): Free-text description.
        - `access_type` (optional): DASHBOARD_PRIVATE (default) or DASHBOARD_PUBLIC; the API rejects requests without it.
        - `filters` (optional): DashboardFilter list placed under `definition.filters`, e.g. `[{"id": "f1", "displayName": "Hostname", "dataSource": "EVENTS", "fieldPath": "principal.hostname", "filterOperatorAndFieldValues": [{"filterOperator": "EQUAL", "fieldValues": ["host-1"]}]}]`.
        - `dashboard` (optional): Additional NativeDashboard fields (camelCase) merged over the generated body, e.g. `{"definition": {...}}`.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The created NativeDashboard (with `name`) or `{"error": ...}`.

- **`update_dashboard(dashboard_id, display_name=None, description=None, filters=None, dashboard=None, update_mask=None, etag=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Update fields of a native SIEM dashboard (PATCH with update mask).
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name.
        - `display_name` (optional): New title.
        - `description` (optional): New description.
        - `filters` (optional): Replacement DashboardFilter list for `definition.filters`.
        - `dashboard` (optional): Raw NativeDashboard fields (camelCase) merged over the generated body.
        - `update_mask` (optional): Comma-separated camelCase field paths (e.g. "displayName,definition.charts"). Merged with the auto-derived mask.
        - `etag` (optional): Optimistic-concurrency etag from `get_dashboard`.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The updated NativeDashboard or `{"error": ...}`.

- **`duplicate_dashboard(dashboard_id, display_name, description=None, access_type="DASHBOARD_PRIVATE", dashboard=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Duplicate a native SIEM dashboard (including its charts and queries).
    - **Parameters:**
        - `dashboard_id` (required): Source dashboard ID or full resource name.
        - `display_name` (required): Title for the copy.
        - `description` (optional): Description for the copy.
        - `access_type` (optional): DASHBOARD_PRIVATE (default) or DASHBOARD_PUBLIC; the API rejects requests without it.
        - `dashboard` (optional): Extra NativeDashboard fields (camelCase) merged into the `nativeDashboard` body.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The new NativeDashboard or `{"error": ...}`.

- **`delete_dashboard(dashboard_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Delete a custom native SIEM dashboard.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"status": "deleted", "dashboard_id": ...}` or `{"error": ...}`.

- **`add_dashboard_chart(dashboard_id, display_name, query=None, time_unit=None, start_time_val=None, start_time=None, end_time=None, visualization=None, description=None, tile_type=None, start_x=None, start_y=None, span_x=None, span_y=None, data_sources=None, chart=None, dashboard_query=None, chart_layout=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Add a chart (and its UDM stats query) to a native SIEM dashboard.
    - **Parameters:**
        - `dashboard_id` (required): Target dashboard ID or full resource name.
        - `display_name` (required): Chart title.
        - `query` (optional): YARA-L 2.0 UDM stats query, e.g. `metadata.event_type = "USER_LOGIN" match: principal.user.userid outcome: $count = count(metadata.id) order: $count desc`.
        - `time_unit` (optional): Relative window unit: SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, YEAR (default DAY when a query is given).
        - `start_time_val` (optional): Relative window length (default 1).
        - `start_time` (optional): Absolute window start (RFC 3339); with `end_time` replaces the relative window.
        - `end_time` (optional): Absolute window end (RFC 3339).
        - `visualization` (optional): DashboardChart `visualization` config (ECharts-style), e.g. `{"series": [{"chartType": "TABLE"}]}`.
        - `description` (optional): Chart description.
        - `tile_type` (optional): TILE_TYPE_VISUALIZATION (default), TILE_TYPE_BUTTON or TILE_TYPE_MARKDOWN.
        - `data_sources` (optional): `chartDatasource. dataSources` for query-backed charts; defaults to `["UDM"]` when a query is given (the API rejects charts without it).
        - `chart` (optional): Raw DashboardChart fields merged over the generated `dashboardChart`.
        - `dashboard_query` (optional): Raw DashboardQuery fields merged over the generated `dashboardQuery`.
        - `chart_layout` (optional): Raw ChartLayout (`{"startX":0,"startY":0,"spanX":48,"spanY":26}`).
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"nativeDashboard": {...}, "dashboardChart": {...}}` or `{"error": ...}`.

- **`edit_dashboard_chart(dashboard_id, chart_id, edit_mask, display_name=None, description=None, query=None, time_unit=None, start_time_val=None, start_time=None, end_time=None, visualization=None, chart=None, dashboard_query=None, etag=None, language_features=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Edit an existing chart and/or its query on a native SIEM dashboard.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name.
        - `chart_id` (required): Chart ID or full `dashboardCharts/{id}` name.
        - `edit_mask` (required): Comma-separated camelCase paths, e.g. "dashboardChart.displayName,dashboardQuery.query,dashboardQuery.input".
        - `display_name` (optional): New chart title.
        - `description` (optional): New chart description.
        - `query` (optional): New YARA-L 2.0 stats query.
        - `time_unit` (optional): Relative window unit (SECOND..YEAR).
        - `start_time_val` (optional): Relative window length.
        - `start_time` (optional): Absolute window start (RFC 3339).
        - `end_time` (optional): Absolute window end (RFC 3339).
        - `visualization` (optional): New `visualization`.
        - `chart` (optional): Raw DashboardChart fields merged over the generated `dashboardChart` (`name` and `etag` are set automatically from the current chart).
        - `dashboard_query` (optional): Raw DashboardQuery fields merged over the generated `dashboardQuery` (`name` is set automatically from `chartDatasource.dashboardQuery`).
        - `etag` (optional): Current chart etag; fetched automatically when omitted.
        - `language_features` (optional): JOINS, STAGES, DATA_TABLES used by the query.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"nativeDashboard": {...}, "dashboardChart": {...}}` or `{"error": ...}`.

- **`remove_dashboard_chart(dashboard_id, chart_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Remove a chart from a native SIEM dashboard.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name.
        - `chart_id` (required): Chart ID or full `dashboardCharts/{id}` name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The updated NativeDashboard or `{"error": ...}`.

- **`duplicate_dashboard_chart(dashboard_id, chart_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Duplicate a chart within a native SIEM dashboard.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name.
        - `chart_id` (required): Chart ID or full `dashboardCharts/{id}` name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"nativeDashboard": {...}, "dashboardChart": {...}}` (the new chart) or `{"error": ...}`.

- **`export_dashboards(dashboard_ids, project_id=None, customer_id=None, region=None)`**
    - **Description:** Export native SIEM dashboards (with charts and queries) as JSON.
    - **Parameters:**
        - `dashboard_ids` (required): One or more dashboard IDs or full resource names. A JSON-array string is accepted.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"inlineDestination": {"dashboards": [...]}}` or `{"error": ...}`.

- **`import_dashboards(dashboards, project_id=None, customer_id=None, region=None)`**
    - **Description:** Import native SIEM dashboards from an inline export payload.
    - **Parameters:**
        - `dashboards` (required): Either the list of NativeDashboardWithChartsAndQueries items, a single item, or the full `export_dashboards` response. JSON strings are accepted.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"results": [{"dashboard": "projects/.../nativeDashboards/<new-id>", "status": {"message": "Dashboard Imported Successfully"}}]}` or `{"error": ...}`.

- **`execute_dashboard_query(query=None, time_unit=None, start_time_val=None, start_time=None, end_time=None, query_id=None, dialect=None, filters=None, clear_cache=None, use_previous_time_range=None, dashboard_query=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Execute a dashboard (UDM stats) query ad hoc and return tabular results.
    - **Parameters:**
        - `query` (optional): YARA-L 2.0 stats query (`match:` / `outcome:` sections) or SQL when `dialect="SQL"`.
        - `time_unit` (optional): SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, YEAR.
        - `start_time_val` (optional): Relative window length (e.g. 7).
        - `start_time` (optional): Absolute window start (RFC 3339); with `end_time` replaces the relative window.
        - `end_time` (optional): Absolute window end (RFC 3339).
        - `query_id` (optional): Saved DashboardQuery ID or resource name to execute instead of an inline query.
        - `dialect` (optional): YL2 (default) or SQL.
        - `filters` (optional): DashboardFilter list, e.g. `[{"fieldPath": "principal.hostname", "dataSource": "EVENTS", "filterOperatorAndFieldValues": [{"filterOperator": "EQUAL", "fieldValues": ["host-1"]}]}]`.
        - `clear_cache` (optional): Bypass the result cache.
        - `use_previous_time_range` (optional): Run against the preceding window of the same length (for comparisons).
        - `dashboard_query` (optional): Raw DashboardQuery fields merged over the generated `query` object.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"results": [{"column": ..., "values": [...]}], "timeWindow": {...}, "queryRuntimeErrors": [...]}` or `{"error": ...}`.

- **`get_dashboard_query(query_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get a saved dashboard query by ID or resource name.
    - **Parameters:**
        - `query_id` (required): Query ID or full `dashboardQueries/{id}` name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The DashboardQuery resource or `{"error": ...}`.

- **`get_dashboard_chart(chart_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get a dashboard chart by ID or resource name.
    - **Parameters:**
        - `chart_id` (required): Chart ID or full `dashboardCharts/{id}` name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The DashboardChart resource or `{"error": ...}`.

- **`list_dashboard_charts(filter=None, page_size=None, page_token=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List dashboard charts in the instance (v1alpha only).
    - **Parameters:**
        - `filter` (optional): Server-side filter expression (e.g. `native_dashboard = "projects/.../nativeDashboards/{id}"`).
        - `page_size` (optional): Maximum charts per page (<= 1000).
        - `page_token` (optional): `nextPageToken` from a previous call.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"dashboardCharts": [...], "nextPageToken": ..., "totalSize": N, "total_charts": N}` or `{"error": ...}`.

- **`batch_get_dashboard_charts(chart_ids, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get several dashboard charts in one call.
    - **Parameters:**
        - `chart_ids` (required): Chart IDs or full resource names. A JSON-array string is accepted.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"dashboardCharts": [...], "total_charts": N}` or `{"error": ...}`.

### Dashboard Scheduled Report and Content Hub Tools

- **`list_dashboard_scheduled_reports(page_size=None, page_token=None, filter_query=None, view=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List scheduled email/GCS reports configured for native dashboards.
    - **Parameters:**
        - `page_size` (optional): Maximum number of reports to return.
        - `page_token` (optional): `nextPageToken` from a previous call.
        - `filter_query` (optional): Case-insensitive substring match applied to `display_name` and `description`.
        - `view` (optional): `DASHBOARD_SCHEDULED_REPORT_VIEW_BASIC` (default) or `DASHBOARD_SCHEDULED_REPORT_VIEW_FULL`.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** API response with `dashboardScheduledReports`, `nextPageToken`, plus `total_reports` for the page, or an error.

- **`get_dashboard_scheduled_report(report_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get a single dashboard scheduled report configuration.
    - **Parameters:**
        - `report_id` (required): Scheduled report ID or full resource name (`projects/.../dashboardScheduledReports/{id}`).
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The `DashboardScheduledReport` resource or an error.

- **`create_dashboard_scheduled_report(display_name, dashboard_id, cron, recipients=None, time_zone=None, file_format=None, description=None, email_subject=None, email_body=None, delivery_type=None, data_access_scopes=None, scheduled_report=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create a scheduled report that emails a native dashboard on a cron.
    - **Parameters:**
        - `display_name` (required): Report name shown in the UI (required).
        - `dashboard_id` (required): Native dashboard ID or full resource name (`projects/.../nativeDashboards/{id}`); becomes `dashboard.name`.
        - `cron` (required): Crontab schedule, 5 fields `min hour dom month dow` (e.g. "0 8 * * 1" = Mondays 08:00).
        - `recipients` (optional): Email recipients (required by the API for email delivery). JSON array string ok.
        - `time_zone` (optional): IANA time zone for the cron (default UTC).
        - `file_format` (optional): `FILE_FORMAT_PDF`, `FILE_FORMAT_CSV`, or `FILE_FORMAT_PNG` (required by the API; defaults to PDF here).
        - `description` (optional): Free-text description.
        - `email_subject` (optional): Email subject line.
        - `email_body` (optional): Email body text.
        - `delivery_type` (optional): `DELIVERY_TYPE_EMAIL_ATTACHMENT` or `DELIVERY_TYPE_GCS_BUCKET`.
        - `data_access_scopes` (optional): Full `dataAccessScopes` resource names for `scopeInfo`.
        - `scheduled_report` (optional): Extra `DashboardScheduledReport` JSON (camelCase keys, e.g. `{"userData": {"pinned": true}, "scopeInfo": {...}}`) merged over the body built from the arguments above.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The created `DashboardScheduledReport` or an error.

- **`update_dashboard_scheduled_report(report_id, update_mask=None, display_name=None, description=None, dashboard_id=None, cron=None, time_zone=None, recipients=None, email_subject=None, email_body=None, delivery_type=None, file_format=None, pinned=None, scheduled_report=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Update fields of an existing dashboard scheduled report (PATCH).
    - **Parameters:**
        - `report_id` (required): Scheduled report ID or full resource name.
        - `update_mask` (optional): Field paths to update. Supported: `display_name`, `description`, `cron_details`, `format`, `delivery_details`, `scope_info`, `dashboard.name`, `user_data.pinned`. Comma-separated string, JSON array, or list.
        - `display_name` (optional): New display name.
        - `description` (optional): New description.
        - `dashboard_id` (optional): New native dashboard ID or full name.
        - `cron` (optional): New crontab string (5 fields).
        - `time_zone` (optional): New IANA time zone.
        - `recipients` (optional): Replacement recipient list (whole `delivery_details` is replaced, so pass all fields).
        - `email_subject` (optional): New email subject.
        - `email_body` (optional): New email body.
        - `delivery_type` (optional): `DELIVERY_TYPE_EMAIL_ATTACHMENT` or `DELIVERY_TYPE_GCS_BUCKET`.
        - `file_format` (optional): `FILE_FORMAT_PDF|CSV|PNG`.
        - `pinned` (optional): Pin/unpin (`user_data.pinned`).
        - `scheduled_report` (optional): Extra resource JSON (camelCase) merged over the generated body, e.g. `{"scopeInfo": {"dataAccessScopes": [...]}, "etag": "..."}`.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The updated `DashboardScheduledReport` or an error.

- **`delete_dashboard_scheduled_report(report_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Delete a dashboard scheduled report.
    - **Parameters:**
        - `report_id` (required): Scheduled report ID or full resource name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"deleted": true, "report_id": ...}` or an error.

- **`fetch_dashboard_scheduled_report_history(report_id, page_size=None, page_token=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Fetch the run history of a dashboard scheduled report (last year).
    - **Parameters:**
        - `report_id` (required): Scheduled report ID or full resource name.
        - `page_size` (optional): Max entries (default 50, max 1000).
        - `page_token` (optional): `nextPageToken` from a previous call.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `reportGenerationDetails`, `runCounts`, `totalSize`, `nextPageToken`, or an error.

- **`duplicate_dashboard_scheduled_report(report_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Duplicate an existing dashboard scheduled report.
    - **Parameters:**
        - `report_id` (required): Source scheduled report ID or full resource name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The new `DashboardScheduledReport` or an error.

- **`trigger_instant_dashboard_report(report_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Send a dashboard scheduled report immediately, outside its schedule.
    - **Parameters:**
        - `report_id` (required): Scheduled report ID or full resource name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The long-running `Operation` (`name`, `done`, optional `metadata`/`response`) or an error.

- **`list_featured_content_dashboards(page_size=None, page_token=None, filter_query=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List Google-curated dashboards available in the Content Hub.
    - **Parameters:**
        - `page_size` (optional): Max results (default and max 100).
        - `page_token` (optional): `nextPageToken` from a previous call.
        - `filter_query` (optional): AIP-160 filter over `name` and `content_metadata.description`; a bare literal (e.g. `"okta"`) does a substring match on both.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `featuredContentNativeDashboards`, `nextPageToken`, plus `total_featured_dashboards` for the page, or an error.

- **`get_featured_content_dashboard(featured_dashboard_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get one Content Hub featured (curated) native dashboard.
    - **Parameters:**
        - `featured_dashboard_id` (required): Featured dashboard ID or full resource name (`projects/.../contentHub/featuredContentNativeDashboards/{id}`).
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The `FeaturedContentNativeDashboard` or an error.

- **`install_featured_content_dashboard(featured_dashboard_id, featured_dashboard=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Install a Content Hub curated dashboard as a native dashboard.
    - **Parameters:**
        - `featured_dashboard_id` (required): Featured dashboard ID or full resource name.
        - `featured_dashboard` (optional): Optional `FeaturedContentNativeDashboard` JSON sent as `featuredContentNativeDashboard` in the body, e.g. to override `dashboardContent.dashboard.displayName` before install. Usually omitted.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** `{"nativeDashboard": "projects/.../nativeDashboards/{id}"}` or an error.

### Legacy (Looker) Dashboard and Migration Tools

- **`create_legacy_dashboard(display_name=None, dashboard_type=None, lookml=None, default_dashboard=None, dashboard=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create a legacy (Looker/LookML) Chronicle dashboard. v1alpha-only.
    - **Parameters:**
        - `display_name` (optional): User-visible dashboard name.
        - `dashboard_type` (optional): ``DASHBOARD_TYPE_USER`` (private to the caller) or ``DASHBOARD_TYPE_CUSTOMER`` (visible to all users). ``DASHBOARD_TYPE_PREDEFINED`` dashboards cannot be created.
        - `lookml` (optional): LookML YAML defining the dashboard.
        - `default_dashboard` (optional): Show this dashboard by default (only one dashboard may be the default).
        - `dashboard` (optional): Full Dashboard resource as a dict or JSON string, e.g. ``{"displayName": "SOC Overview", "type": "DASHBOARD_TYPE_USER", "lookml": "..."}``. Explicit args above override matching keys.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The created Dashboard resource (``name``, ``displayName``, ``type``, ``uri``, ...), or an error message.

- **`get_legacy_dashboard(dashboard_id, view=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get a legacy (Looker) Chronicle dashboard by ID. v1alpha-only.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name ``projects/.../instances/.../dashboards/{id}``.
        - `view` (optional): ``DASHBOARD_VIEW_BASIC`` (default, no LookML), ``DASHBOARD_VIEW_EXPORT`` (LookML, no URI) or ``DASHBOARD_VIEW_FULL`` (everything).
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The Dashboard resource, or an error message.

- **`list_legacy_dashboards(page_size=None, page_token=None, view=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List legacy (Looker) Chronicle dashboards. v1alpha-only.
    - **Parameters:**
        - `page_size` (optional): Maximum dashboards per page.
        - `page_token` (optional): ``nextPageToken`` from a previous call.
        - `view` (optional): ``DASHBOARD_VIEW_BASIC`` (default), ``DASHBOARD_VIEW_EXPORT`` or ``DASHBOARD_VIEW_FULL``.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"dashboards": [...], "nextPageToken": "...", "total_dashboards": N}`` or an error message.

- **`delete_legacy_dashboard(dashboard_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Delete a legacy (Looker) Chronicle dashboard. v1alpha-only.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID or full resource name.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"status": "deleted", "dashboard_id": ...}`` or an error message.

- **`copy_legacy_dashboard(dashboard_id, dashboard_type=None, display_name=None, default_dashboard=None, destination=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Copy a legacy (Looker) dashboard to another dashboard type. v1alpha-only.
    - **Parameters:**
        - `dashboard_id` (required): Source dashboard ID or full resource name.
        - `dashboard_type` (optional): Destination type, required unless given in ``destination``: ``DASHBOARD_TYPE_USER`` or ``DASHBOARD_TYPE_CUSTOMER``.
        - `display_name` (optional): Name for the copy.
        - `default_dashboard` (optional): Make the copy the default.
        - `destination` (optional): Destination Dashboard resource (dict or JSON string), e.g. ``{"displayName": "My copy", "type": "DASHBOARD_TYPE_USER"}``. Explicit args above override matching keys. The request body sent is ``{"destination": {"parent": <instance>, "dashboard": {...}}}``.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The newly created Dashboard resource, or an error.

- **`fetch_migratable_dashboards(page_size=None, page_token=None, view=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List legacy (Looker) dashboards eligible for migration to native. v1alpha-only.
    - **Parameters:**
        - `page_size` (optional): Maximum dashboards per page.
        - `page_token` (optional): ``nextPageToken`` from a previous call.
        - `view` (optional): ``DASHBOARD_VIEW_BASIC`` (default), ``DASHBOARD_VIEW_EXPORT`` or ``DASHBOARD_VIEW_FULL``.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"dashboards": [...], "nextPageToken": "...", "total_dashboards": N}`` or an error message.

- **`batch_migrate_dashboards(dashboards, project_id=None, customer_id=None, region=None)`**
    - **Description:** Migrate legacy (Looker) dashboards to native dashboards. v1alpha-only.
    - **Parameters:**
        - `dashboards` (required): Legacy dashboard IDs or full resource names, as a list or JSON array string. Bare IDs are expanded to ``projects/.../instances/.../dashboards/{id}``.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"migrationJobId": "...", "jobMigrationStatus": "JOB_MIGRATION_STATE_IN_PROGRESS" | "..._SUCCESS" | "..._PARTIAL_SUCCESS" | "..._FAILURE", "endTime": "..."}`` plus ``dashboards_requested``, or an error message.

- **`fetch_dashboard_migration_metrics(project_id=None, customer_id=None, region=None)`**
    - **Description:** Get instance-wide legacy-to-native dashboard migration metrics. v1alpha-only.
    - **Returns:** ``{"totalMigrations", "successRate", "hitlCount", "lookerDashboardCount", "migratedDashboardsCount", "pendingDashboardsCount", "processingDashboardsCount", "failedDashboardsCount"}`` or an error message.

- **`fetch_dashboard_migration_jobs(migration_job_id=None, dashboard_id=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get legacy-to-native dashboard migration jobs and results. v1alpha-only.
    - **Parameters:**
        - `migration_job_id` (optional): Migration job ID to fetch.
        - `dashboard_id` (optional): Legacy dashboard ID or full resource name; restricts results to that dashboard.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"migrationJobs": [{"migrationJobId", "jobMigrationStatus", "startedBy", "startTime", "endTime", "results": [{"dashboard", "title", "status", "errorMessage", "nativeDashboard"}]}], "total_jobs": N}`` or an error message. Result ``status`` values: DASHBOARD_MIGRATION_STATE_PENDING, _IN_PROGRESS, _SUCCESS, _NEEDS_REVIEW, _FAILED.

### Legacy SOAR Dashboard Tools

- **`legacy_soar_get_dashboard_cards(project_id=None, customer_id=None, region=None)`**
    - **Description:** List legacy SOAR dashboards (ID to name map) visible to the caller.
    - **Returns:** ``{"payload": {"<dashboard_id>": "<name>", ...}, "total_dashboards": N}`` or ``{"error": ...}``.

- **`legacy_soar_get_dashboard(dashboard_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get a legacy SOAR dashboard with its configuration and widgets.
    - **Parameters:**
        - `dashboard_id` (required): Numeric dashboard ID (from legacy_soar_get_dashboard_cards).
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": {<LegacySoarDashboardDataModel>}}`` or ``{"error": ...}``.

- **`legacy_soar_get_dashboard_widget_definitions(project_id=None, customer_id=None, region=None)`**
    - **Description:** List the predefined widget definitions available for SOAR dashboards.
    - **Returns:** ``{"payload": [<DashboardWidgetDefinitionDataModel>], "total_definitions": N}`` or ``{"error": ...}``.

- **`legacy_soar_get_dashboard_playbooks(project_id=None, customer_id=None, region=None)`**
    - **Description:** List SOAR playbooks that have data available for dashboard reporting.
    - **Returns:** ``{"payload": [<DashboardPlaybookModel>], "total_playbooks": N}`` or ``{"error": ...}``.

- **`legacy_soar_add_or_update_dashboard(dashboard_id, name=None, creator=None, default_time_range=None, environments=None, allowed_users=None, allowed_users_json=None, widgets=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create or update a legacy SOAR (case management) dashboard.
    - **Parameters:**
        - `dashboard_id` (required): Dashboard ID to update, or 0 to create.
        - `name` (optional): Dashboard display name.
        - `creator` (optional): Creator username.
        - `default_time_range` (optional): One of DASHBOARD_TIME_RANGE_TYPE_UNSPECIFIED, LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `environments` (optional): SOAR environment names the dashboard covers; list or JSON array string.
        - `allowed_users` (optional): Usernames allowed to view the dashboard; list or JSON array string.
        - `allowed_users_json` (optional): Legacy JSON-encoded allowed users string, if the backend expects it.
        - `widgets` (optional): Widget definitions (LegacySoarDashboardWidgetDataModel, camelCase keys) as list or JSON array string.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** The saved dashboard (``id``, ``name``, ``creator``, ``widgets``, ...) or ``{"error": ...}``.

- **`legacy_soar_delete_dashboard(dashboard_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Delete a legacy SOAR dashboard and all of its widgets.
    - **Parameters:**
        - `dashboard_id` (required): Numeric dashboard ID to delete.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"deleted": True, "dashboard_id": ...}`` merged with the (normally empty) API response, or ``{"error": ...}``.

- **`legacy_soar_import_dashboard(dashboard=None, name=None, creator=None, default_time_range=None, environments=None, allowed_users=None, widgets=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Import a legacy SOAR dashboard from an exported JSON definition.
    - **Parameters:**
        - `dashboard` (optional): Exported dashboard object with camelCase keys (``id``, ``name``, ``creator``, ``defaultTimeRange``, ``environments``, ``allowedUsers``, ``widgets``, ...). Dict or JSON string.
        - `name` (optional): Override the dashboard name.
        - `creator` (optional): Override the creator username.
        - `default_time_range` (optional): One of DASHBOARD_TIME_RANGE_TYPE_UNSPECIFIED, LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `environments` (optional): Override environments.
        - `allowed_users` (optional): Override allowed users.
        - `widgets` (optional): Override widget list.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": {<imported dashboard>}}`` or ``{"error": ...}``.

- **`legacy_soar_save_dashboard_as_report_template(name, template_id=None, category=None, report_widgets=None, is_system=None, has_scheduler=None, template=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Save a legacy SOAR dashboard's widgets as a SOAR report template.
    - **Parameters:**
        - `name` (required): Report template name.
        - `template_id` (optional): Existing template ID to overwrite (``id``); omit to create.
        - `category` (optional): ``ROI``, ``MANAGEMENT``, ``SLA``, ``TIER1`` or ``GENERAL``.
        - `report_widgets` (optional): Widget definitions (camelCase) as list or JSON array string.
        - `is_system` (optional): Mark as a system template.
        - `has_scheduler` (optional): Whether a schedule is attached.
        - `template` (optional): Full request object (camelCase keys) used as the base; explicit arguments override.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": {<ReportTemplateDetails>}}`` or ``{"error": ...}``.

- **`legacy_soar_add_or_update_dashboard_widget(widget=None, widget_id=None, dashboard_id=None, title=None, widget_type=None, width_size=None, description=None, order=None, time_filter=None, subject=None, dimension_a=None, dimension_b=None, chart_type=None, results_amount=None, results_order=None, calculate_field=None, extra_fields=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Create or update a widget on a legacy SOAR dashboard.
    - **Parameters:**
        - `widget` (optional): Full widget definition (camelCase keys) as returned by legacy_soar_get_dashboard; dict or JSON string. Explicit arguments below override its keys.
        - `widget_id` (optional): Widget ID (``id``; 0 for new).
        - `dashboard_id` (optional): Owning dashboard ID (``dashboardId``).
        - `title` (optional): Widget title.
        - `widget_type` (optional): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        - `width_size` (optional): ``ONE_BLOCK``, ``TWO_BLOCKS``, ``THREE_BLOCKS``.
        - `description` (optional): Widget description.
        - `order` (optional): Position in the dashboard.
        - `time_filter` (optional): LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `subject` (optional): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        - `dimension_a` (optional): Primary grouping (CustomWidgetObjectEnum), e.g. ``ANALYST``, ``TAG``, ``PRIORITY``, ``RULE_NAME``, ``ENVIRONMENT``, ``PLAYBOOK``, ``PRODUCT``, ``CASE_STATUS``, ``CASE_CLOSE_REASON``, ``STAGE``, ``SLA_STATUS``, ``TASK_STATUS``, ``PLAYBOOK_TOTAL_RUNS``, ``CASE_OPEN_AND_CLOSURE_TRENDS``.
        - `dimension_b` (optional): Secondary grouping, same enum.
        - `chart_type` (optional): ``PIE``, ``HORIZENTAL_BARS``, ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``, ``SOCS_STATUS``, ``ROI``, ``TEXT``, ``IMAGE``, ``NUMBER_STATUS``.
        - `results_amount` (optional): Max result buckets.
        - `results_order` (optional): ``DESCENDING`` or ``ASCENDING``.
        - `calculate_field` (optional): ``COUNT``, ``HANDLING_AVG_TIME``, ``SLA_AVG_REMAINING_TIME``, ``TASK_DUE_DATE_AVG_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        - `extra_fields` (optional): Other camelCase request fields, mainly list filters: ``tagFilters``, ``productFilters``, ``analystFilters``, ``priorityFilter`` (INFORMATIVE/LOW/MEDIUM/ HIGH/CRITICAL), ``environmentFilter``, ``entityTypeFilter``, ``caseStatusesFilter`` (OPENED/CLOSED/ALL/MERGED), ``alertNamesFilter``, ``importanceStatusesFilter`` (bools), ``incidentStatusesFilter`` (bools), ``exceededSlaFilter`` (bools), ``closeReasonsFilter`` (MALICIOUS/NOT_MALICIOUS/MAINTENANCE/ INCONCLUSIVE/UNKNOWN), ``caseRootCauseFilter``, ``caseStageFilter``, ``entityIdentifierFilter``, ``networksFilter``, ``portsFilter``, ``categoryOutcomeFilter``, ``playbooksFilter``, ``integrationsFilter``, ``playbookStatusFilter`` (FINISHED_SUCCESSFULLY/ERROR/ WAITING_FOR_USER_ACTION/DECLINED/PLAYBOOK_CLOSED_ALERT/PENDING/ TERMINATED), ``startStage``, ``endStage``, ``text``, ``groupByField``, ``socAnalystsLoadManagerUsername``.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": {<saved widget>}}`` or ``{"error": ...}``.

- **`legacy_soar_delete_dashboard_widget(widget_id, project_id=None, customer_id=None, region=None)`**
    - **Description:** Delete a single widget from a legacy SOAR dashboard.
    - **Parameters:**
        - `widget_id` (required): Numeric widget ID to delete.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"deleted": True, "widget_id": ...}`` merged with the API response, or ``{"error": ...}``.

- **`legacy_soar_get_dashboard_widget_values(widget=None, widget_id=None, dashboard_id=None, title=None, widget_type=None, width_size=None, description=None, order=None, time_filter=None, subject=None, dimension_a=None, dimension_b=None, chart_type=None, results_amount=None, results_order=None, calculate_field=None, extra_fields=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Compute the data series for a legacy SOAR dashboard widget.
    - **Parameters:**
        - `widget` (optional): Full widget definition (camelCase keys) as returned by legacy_soar_get_dashboard; dict or JSON string. Explicit arguments below override its keys.
        - `widget_id` (optional): Widget ID (``id``; 0 for new).
        - `dashboard_id` (optional): Owning dashboard ID (``dashboardId``).
        - `title` (optional): Widget title.
        - `widget_type` (optional): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        - `width_size` (optional): ``ONE_BLOCK``, ``TWO_BLOCKS``, ``THREE_BLOCKS``.
        - `description` (optional): Widget description.
        - `order` (optional): Position in the dashboard.
        - `time_filter` (optional): LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `subject` (optional): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        - `dimension_a` (optional): Primary grouping (CustomWidgetObjectEnum), e.g. ``ANALYST``, ``TAG``, ``PRIORITY``, ``RULE_NAME``, ``ENVIRONMENT``, ``PLAYBOOK``, ``PRODUCT``, ``CASE_STATUS``, ``CASE_CLOSE_REASON``, ``STAGE``, ``SLA_STATUS``, ``TASK_STATUS``, ``PLAYBOOK_TOTAL_RUNS``, ``CASE_OPEN_AND_CLOSURE_TRENDS``.
        - `dimension_b` (optional): Secondary grouping, same enum.
        - `chart_type` (optional): ``PIE``, ``HORIZENTAL_BARS``, ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``, ``SOCS_STATUS``, ``ROI``, ``TEXT``, ``IMAGE``, ``NUMBER_STATUS``.
        - `results_amount` (optional): Max result buckets.
        - `results_order` (optional): ``DESCENDING`` or ``ASCENDING``.
        - `calculate_field` (optional): ``COUNT``, ``HANDLING_AVG_TIME``, ``SLA_AVG_REMAINING_TIME``, ``TASK_DUE_DATE_AVG_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        - `extra_fields` (optional): Other camelCase request fields, mainly list filters: ``tagFilters``, ``productFilters``, ``analystFilters``, ``priorityFilter`` (INFORMATIVE/LOW/MEDIUM/ HIGH/CRITICAL), ``environmentFilter``, ``entityTypeFilter``, ``caseStatusesFilter`` (OPENED/CLOSED/ALL/MERGED), ``alertNamesFilter``, ``importanceStatusesFilter`` (bools), ``incidentStatusesFilter`` (bools), ``exceededSlaFilter`` (bools), ``closeReasonsFilter`` (MALICIOUS/NOT_MALICIOUS/MAINTENANCE/ INCONCLUSIVE/UNKNOWN), ``caseRootCauseFilter``, ``caseStageFilter``, ``entityIdentifierFilter``, ``networksFilter``, ``portsFilter``, ``categoryOutcomeFilter``, ``playbooksFilter``, ``integrationsFilter``, ``playbookStatusFilter`` (FINISHED_SUCCESSFULLY/ERROR/ WAITING_FOR_USER_ACTION/DECLINED/PLAYBOOK_CLOSED_ALERT/PENDING/ TERMINATED), ``startStage``, ``endStage``, ``text``, ``groupByField``, ``socAnalystsLoadManagerUsername``.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": {<LegacySoarDashboardWidgetValues>}}`` or ``{"error": ...}``.

- **`legacy_soar_get_dashboard_widget_case_ids(widget=None, widget_id=None, dashboard_id=None, title=None, widget_type=None, width_size=None, description=None, order=None, time_filter=None, subject=None, dimension_a=None, dimension_b=None, chart_type=None, results_amount=None, results_order=None, calculate_field=None, extra_fields=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List the SOAR case IDs behind a legacy dashboard widget.
    - **Parameters:**
        - `widget` (optional): Full widget definition (camelCase keys) as returned by legacy_soar_get_dashboard; dict or JSON string. Explicit arguments below override its keys.
        - `widget_id` (optional): Widget ID (``id``; 0 for an ad-hoc widget).
        - `dashboard_id` (optional): Owning dashboard ID (``dashboardId``).
        - `title` (optional): Widget title.
        - `widget_type` (optional): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        - `width_size` (optional): ``ONE_BLOCK``, ``TWO_BLOCKS``, ``THREE_BLOCKS``.
        - `description` (optional): Widget description.
        - `order` (optional): Position in the dashboard.
        - `time_filter` (optional): LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `subject` (optional): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        - `dimension_a` (optional): Primary grouping, e.g. ``ANALYST``, ``PRIORITY``, ``CASE_STATUS``, ``PLAYBOOK``, ``STAGE``.
        - `dimension_b` (optional): Secondary grouping, same enum.
        - `chart_type` (optional): ``PIE``, ``HORIZENTAL_BARS``, ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``, ``NUMBER_STATUS`` and others.
        - `results_amount` (optional): Max result buckets.
        - `results_order` (optional): ``DESCENDING`` or ``ASCENDING``.
        - `calculate_field` (optional): ``COUNT``, ``HANDLING_AVG_TIME``, ``SLA_AVG_REMAINING_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        - `extra_fields` (optional): Other camelCase request fields such as ``caseStatusesFilter``, ``priorityFilter``, ``analystFilters``, ``environmentFilter``, ``playbooksFilter``, ``playbookStatusFilter``; full key list in legacy_soar_add_or_update_dashboard_widget.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": [<case_id>, ...], "total_results": N}`` or ``{"error": ...}``.

- **`legacy_soar_get_dashboard_custom_widget_case_ids(widget=None, widget_id=None, dashboard_id=None, title=None, widget_type=None, width_size=None, description=None, order=None, time_filter=None, subject=None, dimension_a=None, dimension_b=None, chart_type=None, results_amount=None, results_order=None, calculate_field=None, extra_fields=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List the SOAR case IDs behind a CUSTOM legacy dashboard widget.
    - **Parameters:**
        - `widget` (optional): Full widget definition (camelCase keys) as returned by legacy_soar_get_dashboard; dict or JSON string. Explicit arguments below override its keys.
        - `widget_id` (optional): Widget ID (``id``; 0 for an ad-hoc widget).
        - `dashboard_id` (optional): Owning dashboard ID (``dashboardId``).
        - `title` (optional): Widget title.
        - `widget_type` (optional): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        - `width_size` (optional): ``ONE_BLOCK``, ``TWO_BLOCKS``, ``THREE_BLOCKS``.
        - `description` (optional): Widget description.
        - `order` (optional): Position in the dashboard.
        - `time_filter` (optional): LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `subject` (optional): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        - `dimension_a` (optional): Primary grouping, e.g. ``ANALYST``, ``PRIORITY``, ``CASE_STATUS``, ``PLAYBOOK``, ``STAGE``.
        - `dimension_b` (optional): Secondary grouping, same enum.
        - `chart_type` (optional): ``PIE``, ``HORIZENTAL_BARS``, ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``, ``NUMBER_STATUS`` and others.
        - `results_amount` (optional): Max result buckets.
        - `results_order` (optional): ``DESCENDING`` or ``ASCENDING``.
        - `calculate_field` (optional): ``COUNT``, ``HANDLING_AVG_TIME``, ``SLA_AVG_REMAINING_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        - `extra_fields` (optional): Other camelCase request fields such as ``caseStatusesFilter``, ``priorityFilter``, ``analystFilters``, ``environmentFilter``, ``playbooksFilter``, ``playbookStatusFilter``; full key list in legacy_soar_add_or_update_dashboard_widget.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": [<case_id>, ...], "total_results": N}`` or ``{"error": ...}``.

- **`legacy_soar_get_dashboard_playbook_runs(widget=None, widget_id=None, dashboard_id=None, title=None, widget_type=None, width_size=None, description=None, order=None, time_filter=None, subject=None, dimension_a=None, dimension_b=None, chart_type=None, results_amount=None, results_order=None, calculate_field=None, extra_fields=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** List recent SOAR playbook runs behind a legacy dashboard widget.
    - **Parameters:**
        - `widget` (optional): Full widget definition (camelCase keys) as returned by legacy_soar_get_dashboard; dict or JSON string. Explicit arguments below override its keys.
        - `widget_id` (optional): Widget ID (``id``; 0 for an ad-hoc widget).
        - `dashboard_id` (optional): Owning dashboard ID (``dashboardId``).
        - `title` (optional): Widget title.
        - `widget_type` (optional): ``CUSTOM`` or ``PLAYBOOK_MONITORING``.
        - `width_size` (optional): ``ONE_BLOCK``, ``TWO_BLOCKS``, ``THREE_BLOCKS``.
        - `description` (optional): Widget description.
        - `order` (optional): Position in the dashboard.
        - `time_filter` (optional): LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `subject` (optional): ``CASES``, ``ALERTS``, ``TASKS``, ``PLAYBOOKS``.
        - `dimension_a` (optional): Primary grouping, e.g. ``ANALYST``, ``PRIORITY``, ``CASE_STATUS``, ``PLAYBOOK``, ``STAGE``.
        - `dimension_b` (optional): Secondary grouping, same enum.
        - `chart_type` (optional): ``PIE``, ``HORIZENTAL_BARS``, ``VERTICAL_BARS``, ``TABLE``, ``TIME_SERIES``, ``TRENDS``, ``NUMBER_STATUS`` and others.
        - `results_amount` (optional): Max result buckets.
        - `results_order` (optional): ``DESCENDING`` or ``ASCENDING``.
        - `calculate_field` (optional): ``COUNT``, ``HANDLING_AVG_TIME``, ``SLA_AVG_REMAINING_TIME``, ``PERCENTAGE``, ``AVG_RUNTIME``.
        - `extra_fields` (optional): Other camelCase request fields such as ``caseStatusesFilter``, ``priorityFilter``, ``analystFilters``, ``environmentFilter``, ``playbooksFilter``, ``playbookStatusFilter``; full key list in legacy_soar_add_or_update_dashboard_widget.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": [<LegacySoarDashboardPlaybookRunDataModel>], "total_results": N}`` or ``{"error": ...}``.

- **`legacy_soar_get_playbook_monitoring(workflow_identifier=None, time_filter=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get the monitoring dashboard for a SOAR playbook.
    - **Parameters:**
        - `workflow_identifier` (optional): Playbook (workflow) identifier.
        - `time_filter` (optional): One of DASHBOARD_TIME_RANGE_TYPE_UNSPECIFIED, LAST_DAY, LAST_3_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": {<LegacySoarDashboardDataModel>}}`` or ``{"error": ...}``.

- **`legacy_soar_get_cases_time_to_respond(time_range_filter=None, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get the average time-to-respond for SOAR cases in a time range.
    - **Parameters:**
        - `time_range_filter` (optional): One of LAST_DAY, LAST_2_DAYS, LAST_3_DAYS, LAST_4_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR, LAST_13_MONTHS (``CUSTOM`` is the proto default and is not useful here).
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"timeToResponseValue": <int>}`` or ``{"error": ...}``.

- **`legacy_soar_get_opened_and_closed_cases_trends(time_range_type, project_id=None, customer_id=None, region=None)`**
    - **Description:** Get opened vs. closed SOAR case trends over a time range.
    - **Parameters:**
        - `time_range_type` (required): Required. One of LAST_DAY, LAST_2_DAYS, LAST_3_DAYS, LAST_4_DAYS, LAST_WEEK, LAST_2_WEEKS, LAST_MONTH, LAST_3_MONTHS, LAST_6_MONTHS, LAST_YEAR, LAST_13_MONTHS.
        - `project_id`, `customer_id`, `region` (optional): Chronicle instance override (defaults to environment config).
    - **Returns:** ``{"payload": [<GetOpenedAndClosedCasesTrends>], "total_results": N}`` or ``{"error": ...}``.

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

### Example 5: Historical Threat Hunting with Retrohunts

```
User: We just created a new detection rule for a recently discovered attack technique. Can you run it against our data from the past week to see if we missed anything?

AI uses: list_security_rules()

AI: I found your rule "Suspicious Lateral Movement Pattern" with ID ru_19fa6159-b7be-48c0-b822-8a29f749fa0c. Let me run a retrohunt against the past week.

AI uses: create_retrohunt(
  rule_id="ru_19fa6159-b7be-48c0-b822-8a29f749fa0c",
  start_time="2024-01-08T00:00:00Z",
  end_time="2024-01-15T00:00:00Z"
)

AI: I've created retrohunt operation oh_077d5ac9-05f1-4331-b33b-d2ff4b09ee50.
This will scan 7 days of historical data. Let me check the status...

AI uses: get_retrohunt(
  rule_id="ru_19fa6159-b7be-48c0-b822-8a29f749fa0c",
  operation_id="oh_077d5ac9-05f1-4331-b33b-d2ff4b09ee50"
)

AI: The retrohunt is currently 45% complete. I'll continue monitoring it.

[After completion]

AI: The retrohunt has completed! It found 3 historical detections that match your new rule:
- 2024-01-10: Lateral movement from workstation-5678 to server-db01
- 2024-01-12: Unusual authentication pattern on admin-laptop
- 2024-01-14: Suspicious network connections from compromised-host-123

These were incidents we missed before creating this rule. Would you like me to investigate any of these further?
```

### Example 6: Rule Alert Analysis

```
User: Show me all the alerts generated by our detection rules in the past 24 hours.

AI uses: search_rule_alerts(
  start_time="2024-01-14T00:00:00Z",
  end_time="2024-01-15T00:00:00Z",
  max_alerts=50
)

AI: I found alerts from 5 different rules in the past 24 hours:

1. **Suspicious PowerShell Execution** (8 alerts)
   - Most recent: 2024-01-15T08:30:00Z
   - Affected hosts: workstation-1234, admin-laptop, server-web01

2. **Potential Data Exfiltration** (3 alerts)
   - Most recent: 2024-01-15T06:15:00Z
   - Affected hosts: workstation-5678

3. **Unusual Authentication Pattern** (12 alerts)
   - Most recent: 2024-01-15T09:45:00Z
   - Multiple hosts

4. **Malware Execution Detected** (2 alerts - High severity)
   - Most recent: 2024-01-15T07:20:00Z
   - Affected hosts: endpoint-9012

5. **C2 Communication Attempt** (1 alert - Critical)
   - Most recent: 2024-01-15T03:10:00Z
   - Affected hosts: compromised-server-345

The high-severity alerts require immediate attention. Would you like me to investigate the C2 communication attempt first?

### Example 7: Curated Rules Management Workflow

```
User: What pre-built detection rules does Chronicle offer for Azure security monitoring?

AI uses: list_curated_rule_sets(as_list=True)

AI: I found several curated rule sets for Azure security monitoring:

1. "Azure - Network" - Detects network-based threats in Azure environments
2. "Azure - Authentication" - Monitors suspicious authentication patterns
3. "Azure - Storage" - Detects unusual storage access patterns

Would you like to enable any of these?

User: Yes, enable the Azure Network rule set with precise detection mode and alerting turned on.

AI uses: list_curated_rule_sets() to get rule set details
AI extracts category_id and rule_set_id from the rule set information

AI uses: update_curated_rule_set_deployment(
  category_id="110fa43d-7165-2355-1985-a63b7cdf90e8",
  rule_set_id="00ad672e-ebb3-0dd1-2a4d-99bd7c5e5f93",
  precision="precise",
  enabled=True,
  alerting=True
)

AI: Successfully enabled the "Azure - Network" rule set with:
- Precision: Precise (lower false positives, better for production alerting)
- Enabled: Yes
- Alerting: Yes

The rule set is now actively monitoring your Azure network traffic.

User: Can you show me what detections this rule set has generated in the last 7 days?

AI uses: get_curated_rule_set(rule_set_id="00ad672e-ebb3-0dd1-2a4d-99bd7c5e5f93")
AI gets the rule IDs from the rule set

AI uses: search_curated_detections(
  rule_id="ur_azure_network_suspicious_traffic",
  start_time="2025-01-20T00:00:00Z",
  end_time="2025-01-27T23:59:59Z"
)

AI: The Azure Network rule set generated 3 detections in the last 7 days:

1. Suspicious outbound connection from Azure VM to known C2 server
   Detection Time: 2025-01-25T14:23:45Z
   Affected Asset: azure-vm-prod-01

2. Unusual data transfer volume to external Azure Storage
   Detection Time: 2025-01-24T09:15:22Z
   Affected Asset: azure-app-service-02

3. Port scanning activity from Azure container instance
   Detection Time: 2025-01-22T16:48:31Z
   Affected Asset: azure-container-instance-03

Would you like me to investigate any of these detections further?
```

### Example 8: Watchlist Management

```
User: Create a watchlist for critical APT threat actors with a 2.5x risk multiplier.

AI uses: create_watchlist(
  name="apt_threat_actors_2024",
  display_name="APT Threat Actors 2024",
  multiplying_factor=2.5,
  description="High-priority APT groups actively targeting our industry"
)

AI: I've created the "APT Threat Actors 2024" watchlist with a 2.5x risk multiplier.
Watchlist ID: abc-123-def

Any entities added to this watchlist will have their risk scores multiplied by 2.5,
helping prioritize alerts and investigations related to these threat actors.

User: Show me all my watchlists.

AI uses: list_watchlists(as_list=True)

AI: You have 3 watchlists configured:

1. APT Threat Actors 2024 (Risk: 2.5x)
   - Created: 2024-01-15
   - For tracking high-priority APT groups

2. Suspicious Domains (Risk: 1.5x)
   - Created: 2024-01-10
   - Domains flagged by threat intelligence

3. Legacy Monitoring (Risk: 1.2x)
   - Created: 2023-12-01
   - Deprecated systems requiring extra monitoring

User: We have an active campaign. Increase the APT watchlist multiplier to 4.0.

AI uses: update_watchlist(
  watchlist_id="abc-123-def",
  multiplying_factor=4.0,
  description="Increased multiplier due to active campaign against our sector"
)

AI: Updated the APT Threat Actors 2024 watchlist:
- Risk multiplier: 2.5x → 4.0x
- Description updated to note the active campaign

This will significantly elevate the priority of any events involving entities
on this watchlist.

User: The campaign has ended. We can remove the APT watchlist now.

AI uses: delete_watchlist(
  watchlist_id="abc-123-def"
)

AI: Successfully deleted the "APT Threat Actors 2024" watchlist.
Entities previously on this watchlist will now use their base risk scores
without the 4.0x multiplier.
```

### Example 9: Building and Scheduling a SIEM Dashboard

```
User: Build a private dashboard showing login activity by user over the past week.

AI uses: create_dashboard(
  display_name="Login Activity",
  description="Logins by user, past 7 days"
)

AI: Created dashboard "Login Activity" (ID: 41fff27d-...). Adding the chart now.

AI uses: add_dashboard_chart(
  dashboard_id="41fff27d-...",
  display_name="Logins by user",
  query="metadata.event_type = \"USER_LOGIN\"\nmatch:\n  principal.user.userid\noutcome:\n  $count = count(metadata.id)\norder:\n  $count desc\nlimit: 20",
  time_unit="DAY",
  start_time_val=7
)

AI: Added the chart. Preview of the data behind it:

AI uses: execute_dashboard_query(
  query="metadata.event_type = \"USER_LOGIN\"\nmatch:\n  principal.user.userid\noutcome:\n  $count = count(metadata.id)\norder:\n  $count desc\nlimit: 20",
  time_unit="DAY",
  start_time_val=7
)

AI: Top principals: alice (412 logins), svc-backup (288), bob (97).

User: Widen the window to 30 days and email it to the SOC lead every Monday.

AI uses: edit_dashboard_chart(
  dashboard_id="41fff27d-...",
  chart_id="8c86e30e-...",
  edit_mask="dashboardQuery.input",
  time_unit="DAY",
  start_time_val=30
)

AI uses: create_dashboard_scheduled_report(
  display_name="Weekly login activity",
  dashboard_id="41fff27d-...",
  cron="0 9 * * 1",
  time_zone="America/New_York",
  recipients=["soc-lead@example.com"]
)

AI: The chart now covers 30 days and a PDF report is scheduled for 09:00
every Monday (America/New_York).

User: Back the dashboard up so we can restore it in the EU tenant.

AI uses: export_dashboards(dashboard_ids=["41fff27d-..."])
AI uses: import_dashboards(dashboards=<export payload>, project_id="eu-project", region="europe")

AI: Exported one dashboard with its chart and query and imported it into the
EU instance as nativeDashboards/06f7f12a-....
```

## Additional Resources

- [Chronicle API Documentation](https://cloud.google.com/chronicle/docs/reference/rest)
- [UDM Schema Reference](https://cloud.google.com/chronicle/docs/reference/udm-field-list)
- [Chronicle Security Operations Overview](https://cloud.google.com/chronicle/docs/overview)
- [Chronicle Query Language Syntax](https://cloud.google.com/chronicle/docs/reference/yara-l-2-0-syntax)
