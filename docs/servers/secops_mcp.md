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

### Example 5: Curated Rules Management Workflow

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

## Additional Resources

- [Chronicle API Documentation](https://cloud.google.com/chronicle/docs/reference/rest)
- [UDM Schema Reference](https://cloud.google.com/chronicle/docs/reference/udm-field-list)
- [Chronicle Security Operations Overview](https://cloud.google.com/chronicle/docs/overview)
- [Chronicle Query Language Syntax](https://cloud.google.com/chronicle/docs/reference/yara-l-2-0-syntax)
