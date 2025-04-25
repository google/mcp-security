# SecOps SOAR MCP Server

This server provides tools for interacting with a Security Orchestration, Automation, and Response (SOAR) platform, specifically Google SecOps SOAR (formerly Siemplify). It includes core case management functionalities and dynamically loads integration-specific tools.

## Configuration

### Prerequisites

1. **Google SecOps SOAR Instance** - An operational SOAR platform
2. **API Access** - SOAR API key with appropriate permissions
3. **Integration Modules** - (Optional) Specific integration modules for additional functionality

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

```json
"secops-soar": {
      "command": "uv",
      "args": [

        "--directory",
        "/path/to/the/repo/server/secops-soar",
        "run",
        "secops_soar_mcp.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {
        "SOAR_URL": "https://your-soar-instance.example.com",
        "SOAR_APP_KEY": "your-soar-api-key"
      },
      "disabled": false,
      "autoApprove": []
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
        "/path/to/the/repo/server/secops-soar",
        "run",
        "--env-file",
        "/path/to/the/repo/.env",
        "secops_soar_mcp.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {},
      ...
```

Example .env file:
```
SOAR_URL=https://your-soar-instance.example.com
SOAR_APP_KEY=your-soar-api-key
```

### Environment Variable Setup

Set up these environment variables in your system:

**For macOS/Linux:**
```bash
export SOAR_URL="https://your-soar-instance.example.com"
export SOAR_APP_KEY="your-soar-api-key"
```

**For Windows PowerShell:**
```powershell
$Env:SOAR_URL = "https://your-soar-instance.example.com"
$Env:SOAR_APP_KEY = "your-soar-api-key"
```

For more detailed instructions on setting up environment variables, refer to the [usage guide](../usage_guide.md#setting-up-environment-variables).

### Available Integrations

The `--integrations` flag in the server configuration allows you to enable specific integrations. The integration modules are located in the `marketplace/` directory. Here's a subset of the available integrations:

- **ServiceNow** - Create/update tickets in ServiceNow
- **CSV** - Export data to CSV files
- **Siemplify** - Advanced Siemplify-specific features
- **Jira** - Create/update Jira issues
- **Slack** - Send notifications to Slack
- **Email** - Send email notifications
- **VirusTotal** - Enrich indicators with VirusTotal data
- **Active Directory** - Query and manage Active Directory
- **Microsoft Defender ATP** - Integration with Microsoft Defender for Endpoint
- **Splunk** - Query and retrieve data from Splunk
- **Sentinel One** - Endpoint protection and response
- **QRadar** - Integration with IBM QRadar SIEM
- **Recorded Future** - Threat intelligence enrichment
- **Tenable.io** - Vulnerability management
- **Rapid7 InsightVM** - Vulnerability management
- **Tanium** - Endpoint management and security
- **Zscaler** - Cloud security
- **And many more** - Over 100 integrations are available in the marketplace

For detailed documentation on each integration, see the [SOAR Integrations](../soar_integrations/index.md) section.

Refer to the files in the `server/secops-soar/marketplace/` directory for a complete list of available integrations. Each integration module provides specific tools for interacting with the corresponding service.

### Authentication Methods

The server supports two authentication methods:

1. **API Key** (Recommended)
   - Set `SOAR_APP_KEY` environment variable
   - Create this key in the SOAR platform under Settings > API Keys

2. **Username/Password** (Legacy)
   - Set `SOAR_USERNAME` and `SOAR_PASSWORD` environment variables
   - Not recommended for production deployments

## Core Tools (Case Management & Entities)

These tools are always available.

- **`list_cases()`**
    - **Description:** Lists available cases in the SOAR platform.
    - **Returns:** A list of cases with basic information like ID, name, status, and priority.
    - **Return Example:**
      ```json
      [
        {
          "id": 12345,
          "identifier": "SEC-12345",
          "name": "Suspicious Login Attempts",
          "description": "Multiple failed login attempts from external IP",
          "priority": "High",
          "status": "In Progress",
          "assignedUser": "john.analyst",
          "creationTime": "2023-09-15T10:30:45Z"
        },
        {
          "id": 12346,
          "identifier": "SEC-12346",
          "name": "Malware Detection - Emotet",
          "description": "Emotet malware detected on user workstation",
          "priority": "Critical",
          "status": "New",
          "assignedUser": null,
          "creationTime": "2023-09-15T11:22:33Z"
        }
      ]
      ```

- **`post_case_comment(case_id, comment)`**
    - **Description:** Adds a textual comment to a specific case.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
        - `comment` (required): The comment text to add.
    - **Returns:** Confirmation of comment addition with timestamp and author information.
    - **Return Example:**
      ```json
      {
        "success": true,
        "comment_id": 56789,
        "timestamp": "2023-09-15T14:22:10Z",
        "author": "claude_assistant",
        "text": "Analysis complete: Malware matches Emotet signature. Recommend isolating the host."
      }
      ```

- **`list_alerts_by_case(case_id)`**
    - **Description:** Lists all alerts associated with a specific case ID.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
    - **Returns:** A list of alerts with their details.
    - **Return Example:**
      ```json
      [
        {
          "id": 34567,
          "name": "Malware Detection",
          "rule": "AV Detection - Emotet",
          "description": "Antivirus detected Emotet malware on workstation",
          "severity": "High",
          "creationTime": "2023-09-15T11:20:15Z",
          "deviceVendor": "Microsoft Defender",
          "deviceProduct": "Endpoint Protection",
          "environment": "Corporate"
        },
        {
          "id": 34568,
          "name": "Suspicious Network Connection",
          "rule": "Outbound C2 Traffic",
          "description": "Connection to known C2 server",
          "severity": "Critical",
          "creationTime": "2023-09-15T11:22:33Z",
          "deviceVendor": "Palo Alto",
          "deviceProduct": "Firewall",
          "environment": "Corporate"
        }
      ]
      ```

- **`list_alert_group_identifiers_by_case(case_id)`**
    - **Description:** Lists the unique group identifiers for alerts within a specific case.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
    - **Returns:** A list of alert group identifiers.
    - **Return Example:**
      ```json
      [
        "Malware_Detection_Group_23456",
        "Network_Activity_Group_23457"
      ]
      ```

- **`list_events_by_alert(case_id, alert_id)`**
    - **Description:** Lists the events associated with a particular alert within a given case.
    - **Parameters:**
        - `case_id` (required): The ID of the case containing the alert.
        - `alert_id` (required): The ID of the specific alert.
    - **Returns:** A list of events with their details.
    - **Return Example:**
      ```json
      [
        {
          "id": 78901,
          "name": "Malware Detected",
          "description": "Emotet malware detected in file: malicious.exe",
          "eventTime": "2023-09-15T11:20:10Z",
          "rawData": {
            "fileName": "malicious.exe",
            "filePath": "C:\\Users\\user\\Downloads\\",
            "fileHash": "a1b2c3d4e5f6g7h8i9j0",
            "malwareType": "Trojan",
            "malwareFamily": "Emotet"
          }
        },
        {
          "id": 78902,
          "name": "Process Creation",
          "description": "Suspicious process created from malicious.exe",
          "eventTime": "2023-09-15T11:20:15Z",
          "rawData": {
            "parentProcess": "malicious.exe",
            "childProcess": "svchost.exe",
            "commandLine": "svchost.exe -k netsvcs",
            "pid": 4567,
            "user": "user123"
          }
        }
      ]
      ```

- **`change_case_priority(case_id, case_priority)`**
    - **Description:** Modifies the priority level of a specific case.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
        - `case_priority` (required): The desired priority level (e.g., "PriorityLow", "PriorityMedium", "PriorityHigh", "PriorityCritical").
    - **Returns:** Confirmation of the priority change.
    - **Return Example:**
      ```json
      {
        "success": true,
        "case_id": 12345,
        "previous_priority": "PriorityMedium",
        "new_priority": "PriorityHigh",
        "timestamp": "2023-09-15T14:30:22Z"
      }
      ```

- **`get_entities_by_alert_group_identifiers(case_id, alert_group_identifiers)`**
    - **Description:** Retrieves entities (like IPs, users, hosts) involved in one or more alert groups within a case. Can also be used to get target entities for manual actions.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
        - `alert_group_identifiers` (required): A list of alert group identifiers.
    - **Returns:** A list of entities with their details.
    - **Return Example:**
      ```json
      [
        {
          "identifier": "10.0.0.25",
          "entityType": "IP Address",
          "environment": "Corporate",
          "isSuspicious": true,
          "isEnriched": true,
          "enrichmentData": {
            "geolocation": {
              "country": "United States",
              "city": "New York"
            },
            "organization": "Example Corp",
            "isInternal": true
          }
        },
        {
          "identifier": "user123",
          "entityType": "User",
          "environment": "Corporate",
          "isSuspicious": false,
          "isEnriched": true,
          "enrichmentData": {
            "department": "Finance",
            "title": "Accountant",
            "manager": "manager456",
            "email": "user123@example.com"
          }
        }
      ]
      ```

- **`get_entity_details(entity_identifier, entity_type, entity_environment)`**
    - **Description:** Fetches detailed information about a specific entity identified by its identifier, type, and environment.
    - **Parameters:**
        - `entity_identifier` (required): The unique identifier of the entity.
        - `entity_type` (required): The type of the entity (e.g., "IP Address", "User").
        - `entity_environment` (required): The environment the entity belongs to.
    - **Returns:** Detailed information about the entity.
    - **Return Example:**
      ```json
      {
        "identifier": "10.0.0.25",
        "entityType": "IP Address",
        "environment": "Corporate",
        "firstSeen": "2023-08-01T08:15:30Z",
        "lastSeen": "2023-09-15T14:22:10Z",
        "associatedCases": [12345, 12340, 12335],
        "isSuspicious": true,
        "isEnriched": true,
        "enrichmentData": {
          "geolocation": {
            "country": "United States",
            "city": "New York",
            "coordinates": {
              "latitude": 40.7128,
              "longitude": -74.0060
            }
          },
          "organization": "Example Corp",
          "isInternal": true,
          "subnet": "10.0.0.0/24",
          "assetType": "Workstation",
          "owner": "user123",
          "department": "Finance"
        }
      }
      ```

- **`search_entity(term=None, type=None, is_suspicious=None, is_internal_asset=None, is_enriched=None, network_name=None, environment_name=None)`**
    - **Description:** Searches for entities within the SOAR platform based on various optional criteria.
    - **Parameters:** (All optional)
        - `term`: A search term (e.g., an IP address, username).
        - `type`: A list of entity types to filter by.
        - `is_suspicious`: Boolean filter for suspicious status.
        - `is_internal_asset`: Boolean filter for internal asset status.
        - `is_enriched`: Boolean filter for enrichment status.
        - `network_name`: List of network names to filter by.
        - `environment_name`: List of environment names to filter by.
    - **Returns:** A list of entities matching the search criteria.
    - **Return Example:**
      ```json
      [
        {
          "identifier": "10.0.0.25",
          "entityType": "IP Address",
          "environment": "Corporate",
          "isSuspicious": true,
          "isInternalAsset": true
        },
        {
          "identifier": "user123",
          "entityType": "User",
          "environment": "Corporate",
          "isSuspicious": false,
          "isInternalAsset": true
        }
      ]
      ```

- **`get_case_full_details(case_id)`**
    - **Description:** Retrieves comprehensive details for a single case, including its basic information, associated alerts, and comments.
    - **Parameters:**
        - `case_id` (required): The ID of the case.
    - **Returns:** Comprehensive details about the case.
    - **Return Example:**
      ```json
      {
        "id": 12345,
        "identifier": "SEC-12345",
        "name": "Suspicious Login Attempts",
        "description": "Multiple failed login attempts from external IP",
        "priority": "High",
        "status": "In Progress",
        "assignedUser": "john.analyst",
        "creationTime": "2023-09-15T10:30:45Z",
        "modificationTime": "2023-09-15T14:30:22Z",
        "alerts": [
          {
            "id": 34567,
            "name": "Failed Login Attempt",
            "severity": "Medium",
            "count": 12
          }
        ],
        "entities": [
          {
            "identifier": "203.0.113.100",
            "entityType": "IP Address",
            "isSuspicious": true
          },
          {
            "identifier": "admin.user",
            "entityType": "User",
            "isSuspicious": false
          }
        ],
        "comments": [
          {
            "id": 56789,
            "author": "john.analyst",
            "text": "Investigating source IP",
            "timestamp": "2023-09-15T11:30:45Z"
          },
          {
            "id": 56790,
            "author": "claude_assistant",
            "text": "IP belongs to known threat actor group APT28",
            "timestamp": "2023-09-15T14:22:10Z"
          }
        ],
        "tags": ["brute-force", "external-threat"]
      }
      ```

## Dynamic Integration Tools (Marketplace)

This server can dynamically load additional tools based on integrations enabled via the `--integrations` command-line flag when the server is started. These tools correspond to modules found in the `marketplace/` directory.

### Available Integrations

For detailed documentation on each integration, see the [SOAR Integrations](../soar_integrations/index.md) section.

#### ServiceNow Integration

Tools for creating and managing ServiceNow tickets:

- **`servicenow_create_ticket(case_id, summary=None, description=None, priority=None, ticket_type="Incident")`**
  - Creates a ServiceNow ticket linked to a SOAR case

- **`servicenow_update_ticket(case_id, ticket_number, status=None, resolution_notes=None)`**
  - Updates an existing ServiceNow ticket

#### CSV Integration

Tools for exporting data to CSV files:

- **`csv_export_case(case_id, file_path=None)`**
  - Exports case details to a CSV file

- **`csv_export_entities(case_id, entity_types=None, file_path=None)`**
  - Exports entities from a case to a CSV file

#### Jira Integration

Tools for creating and managing Jira issues:

- **`jira_create_issue(case_id, project_key, issue_type="Bug", summary=None, description=None, priority=None)`**
  - Creates a Jira issue linked to a SOAR case

- **`jira_update_issue(case_id, issue_key, status=None, resolution=None, comment=None)`**
  - Updates an existing Jira issue

#### Slack Integration

Tools for sending notifications to Slack:

- **`slack_send_notification(case_id, channel, message=None, include_details=True)`**
  - Sends a notification about a case to a Slack channel

#### Email Integration

Tools for sending email notifications:

- **`email_send_notification(case_id, recipients, subject=None, body=None, include_details=True)`**
  - Sends an email notification about a case

## Usage Examples

### Example 1: Case Investigation Workflow

```
User: What security cases need my attention right now?

AI uses: list_cases()

AI: I found 3 open cases:

1. SEC-12345: Suspicious Login Attempts (High Priority)
   Status: In Progress, Assigned to: john.analyst

2. SEC-12346: Malware Detection - Emotet (Critical Priority)
   Status: New, Unassigned

3. SEC-12347: Data Exfiltration Alert (Medium Priority)
   Status: New, Unassigned

User: Tell me more about the Emotet malware case.

AI uses: get_case_full_details(12346)

AI: Case SEC-12346: Malware Detection - Emotet
Critical Priority, Created: 15 minutes ago

Alerts:
- Malware Detection (High): AV detected Emotet malware
- Suspicious Network Connection (Critical): Connection to C2 server

Entities:
- workstation-1234 (Hostname)
- user123 (User)
- 203.0.113.100 (IP Address, Suspicious)

No comments on this case yet.

User: What events were captured in the malware detection alert?

AI uses: list_alerts_by_case(12346)
[AI identifies the alert ID as 34567]

AI uses: list_events_by_alert(12346, 34567)

AI: The malware detection alert contains these events:

1. Malware Detected (2023-09-15 11:20:10)
   Emotet malware detected in file: malicious.exe
   File location: C:\Users\user\Downloads\
   File hash: a1b2c3d4e5f6g7h8i9j0

2. Process Creation (2023-09-15 11:20:15)
   Suspicious process created from malicious.exe
   Command: svchost.exe -k netsvcs
   PID: 4567, User: user123

User: Add a comment to the case that I'm investigating this and change priority to high.

AI uses: post_case_comment(12346, "Starting investigation of the Emotet malware detection. Will isolate affected host.")

AI uses: change_case_priority(12346, "PriorityHigh")

AI: I've added your comment to the case and changed the priority to High.

User: Can you create a ServiceNow ticket for this case?

AI uses: servicenow_create_ticket(
  case_id=12346,
  summary="Emotet Malware Incident - workstation-1234",
  description="Emotet malware detected on workstation-1234. User workstation has been isolated. Need IT assistance with remediation.",
  priority="High"
)

AI: Created ServiceNow ticket INC0012345 for this case. The ticket is assigned to the Security Incident Response team with High priority.
```

### Example 2: Entity Investigation

```
User: Can you find information about the suspicious IP address in the malware case?

AI uses: get_entities_by_alert_group_identifiers(12346, ["Network_Activity_Group_23457"])
[AI identifies the suspicious IP as 203.0.113.100]

AI uses: get_entity_details("203.0.113.100", "IP Address", "Corporate")

AI: IP Address: 203.0.113.100
- Classification: External, Suspicious
- First seen: 2023-09-15 11:22:10
- Associated with 1 case (SEC-12346)
- Enrichment data:
  - Country: Russia
  - City: Moscow
  - ISP: Example Telecom
  - Known malicious: Yes (Confidence: High)
  - Threat intelligence tags: Emotet C2, Botnet Infrastructure

User: Are there any other entities in our environment that have communicated with this IP?

AI uses: search_entity(term="203.0.113.100")

AI: I found 3 entities that have had communications with this IP:

1. workstation-1234 (Hostname)
   Status: Suspicious, Last communication: 2023-09-15 11:22:10

2. workstation-5678 (Hostname)
   Status: Suspicious, Last communication: 2023-09-15 09:15:30

3. user456 (User)
   Status: Under investigation
```

## Additional Resources

- [Google SecOps SOAR Documentation](https://cloud.google.com/chronicle/docs/soar/overview)
- [SOAR API Reference](https://cloud.google.com/chronicle/docs/soar/api/overview)
- [SOAR Playbook Development Guide](https://cloud.google.com/chronicle/docs/soar/playbooks/overview)
