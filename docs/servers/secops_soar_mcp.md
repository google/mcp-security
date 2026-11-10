# Google SecOps SOAR MCP server

The `secops-soar-mcp` server connects MCP clients to Google Security Operations SOAR for case triage, alert and event inspection, entity lookups, and third-party response actions. It always registers 17 core case-management tools and optionally loads any subset of 294 pre-built marketplace integration modules via the `--integrations` CLI flag.

## Configuration

### Prerequisites and authentication

`secops-soar-mcp` authenticates exclusively with an `AppKey` header derived from `SOAR_APP_KEY`:

1. `SOAR_URL`: Base URL of your Google SecOps SOAR instance (for example, `https://your-soar-instance.siemplify-soar.com:443`). Do not use a `*.backstory.chronicle.security` SIEM URL; see [Finding your `SOAR_URL`](../usage_guide.md#setting-up-environment-variables) if startup logs `Failed to fetch valid scopes from SOAR`.
2. `SOAR_APP_KEY`: API key created in Google SecOps SOAR under **Settings > Advanced > API Keys**.

On macOS and Linux:

```bash
export SOAR_URL="https://your-soar-instance.example.com"
export SOAR_APP_KEY="your-soar-api-key"
```

On Windows PowerShell:

```powershell
$Env:SOAR_URL = "https://your-soar-instance.example.com"
$Env:SOAR_APP_KEY = "your-soar-api-key"
```

### MCP client configuration

To load marketplace integration modules with `--integrations`, run `server.py` from a local Git clone (`marketplace.*` imports resolve relative to `server/secops-soar/secops_soar_mcp`):

```json
{
  "mcpServers": {
    "secops-soar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/secops-soar/secops_soar_mcp",
        "run",
        "server.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {
        "SOAR_URL": "https://your-soar-instance.example.com",
        "SOAR_APP_KEY": "your-soar-api-key"
      }
    }
  }
}
```

To keep `SOAR_APP_KEY` out of your client configuration file, pass `--env-file` to `uv`:

```json
{
  "mcpServers": {
    "secops-soar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/secops-soar/secops_soar_mcp",
        "run",
        "--env-file",
        "/path/to/mcp-security/.env",
        "server.py",
        "--integrations",
        "CSV,OKTA"
      ],
      "env": {}
    }
  }
}
```

If you only need the 17 core case and entity tools, you can also run the published PyPI package via `uvx --from secops-soar-mcp secops_soar_mcp`.

> **Note:** Enable only the integrations your workflow uses (1 to 3 modules is typical). Each marketplace integration registers between 4 and 40+ action tools; loading many modules at once expands tool schemas in the model's context window. Integration selection is controlled only by the `--integrations` CLI argument (there is no `SOAR_INTEGRATIONS` environment variable).

For corporate proxy and custom TLS CA configuration (`HTTP_PROXY`, `HTTPS_PROXY`, and `SSL_CERT_FILE`), see [Corporate proxies and custom TLS certificates](../usage_guide.md#corporate-proxies-and-custom-tls-certificates).

## Core tools (17 tools)

These 17 tools are always registered regardless of `--integrations`.

### Case lifecycle and triage

- **`list_cases()`**
  - Lists active SOAR cases with case ID, title, priority, stage, status, assignee, and creation timestamp.
- **`get_case_full_details(case_id)`**
  - Retrieves full details for `case_id`, combining case metadata, alert summaries, involved entities, case comments, and tags.
- **`create_case(name, priority=None, description=None, environment=None)`**
  - Creates a manual SOAR case. Optional `priority` accepts `"PriorityInfo"`, `"PriorityLow"`, `"PriorityMedium"`, `"PriorityHigh"`, or `"PriorityCritical"`.
- **`post_case_comment(case_id, comment)`**
  - Posts a text comment to the case wall of `case_id`.
- **`change_case_priority(case_id, case_priority)`**
  - Updates the priority of `case_id` (`"PriorityInfo"`, `"PriorityLow"`, `"PriorityMedium"`, `"PriorityHigh"`, or `"PriorityCritical"`).
- **`update_case_description(case_id, description)`**
  - Replaces the description text on `case_id`.
- **`assign_case(case_id, user)`**
  - Assigns `case_id` to an analyst username, email address, or SOC role.
- **`change_case_stage(case_id, stage)`**
  - Moves `case_id` to another configured workflow stage (for example, `"Triage"`, `"Investigation"`, `"Assessment"`, or `"Incident"`).
- **`add_case_tag(case_id, tag)`**
  - Attaches a classification or workflow tag to `case_id`.
- **`remove_case_tag(case_id, tag)`**
  - Removes an existing tag from `case_id`.
- **`close_case(case_id, root_cause, comment, reason, tags=None)`**
  - Closes `case_id`. `reason` must be one of `"Malicious"`, `"NotMalicious"`, `"Maintenance"`, or `"Inconclusive"`. Optional `tags` accepts comma-separated tags to apply on closure.

### Alerts and underlying events

- **`list_alerts_by_case(case_id)`**
  - Lists all alerts grouped under `case_id`, including alert ID, rule generator, severity, vendor, product, and environment.
- **`list_alert_group_identifiers_by_case(case_id)`**
  - Returns the `alert_group_identifiers` strings for `case_id`. Pass these identifiers when invoking marketplace integration action tools against a case.
- **`list_events_by_alert(case_id, alert_id)`**
  - Lists the security events attached to `alert_id` inside `case_id`, including raw event fields.

### Entities

- **`get_entities_by_alert_group_identifiers(case_id, alert_group_identifiers)`**
  - Lists entities (IP addresses, hostnames, users, hashes, domains) involved in the specified `alert_group_identifiers` within `case_id`.
- **`get_entity_details(entity_identifier, entity_type, entity_environment)`**
  - Retrieves full enrichment data, first-seen and last-seen timestamps, suspicious flags, and related case IDs for a specific entity (`entity_identifier`, `entity_type`, and `entity_environment`).
- **`search_entity(term=None, type=None, is_suspicious=None, is_internal_asset=None, is_enriched=None, network_name=None, environment_name=None)`**
  - Searches entities across the SOAR platform with optional filters for `term`, `type` (list of entity types), `is_suspicious`, `is_internal_asset`, `is_enriched`, `network_name`, and `environment_name`.

## Dynamic marketplace integration tools

Passing `--integrations <Name1>,<Name2>` loads the corresponding Python modules from `server/secops-soar/secops_soar_mcp/marketplace/` (integration names are matched case-insensitively with underscores ignored, so `--integrations ServiceNow,EmailV2,CSV,Okta` loads `servicenow.py`, `emailv2.py`, `csv.py`, and `okta.py`).

Browse the full catalog of over 290 integration references in [SOAR integrations](../soar_integrations/index.md). Every marketplace action executes within the context of a SOAR case and accepts `case_id`, `alert_group_identifiers` (obtainable via `list_alert_group_identifiers_by_case`), optional `target_entities`, and optional `scope`.

Representative marketplace modules and verified tool names:

### ServiceNow (`--integrations ServiceNow`)

- `service_now_create_incident` and `service_now_create_alert_incident`: Create a ServiceNow incident linked to a SOAR case or alert group.
- `service_now_update_incident`, `service_now_get_incident`, and `service_now_close_incident`: Update fields, fetch status, or resolve an existing incident by `incident_number`.
- `service_now_add_comment` and `service_now_ping`: Post comments to an incident or verify connectivity.

### Jira (`--integrations Jira`)

- `jira_create_issue` and `jira_create_alert_issue`: Create a Jira issue in `project_key` linked to the active case.
- `jira_update_issue`, `jira_assign_issue`, `jira_add_comment`, `jira_get_issues`, and `jira_list_issues`: Manage and query Jira issues from case triage.

### Slack (`--integrations Slack`)

- `slack_send_message`, `slack_send_advanced_message`, and `slack_send_interactive_message`: Post responder notifications or approval prompts to a Slack channel or user.
- `slack_list_channels`, `slack_create_channel`, and `slack_get_channel_or_user_conversation_history`: Manage incident channels and retrieve thread history.

### EmailV2 (`--integrations EmailV2`)

- `email_v2_send_email`, `email_v2_send_thread_reply`, and `email_v2_forward_email`: Send outbound notifications or replies from a configured mailbox.
- `email_v2_search_email` and `email_v2_save_email_attachments_to_case`: Search mailbox folders and attach evidence to the SOAR case wall.

### CSV (`--integrations CSV`)

- `csv_csv_search_by_entity` and `csv_csv_search_by_string`: Search local CSV files on the SOAR server by case entity or string match.
- `csv_save_json_to_csv`: Serialize JSON output to a CSV file path.

### Okta (`--integrations Okta`)

- `okta_get_user`, `okta_list_users`, and `okta_list_user_groups`: Inspect Okta account status and group memberships.
- `okta_disable_user`, `okta_reset_password`, `okta_assign_role`, and `okta_unassign_role`: Execute identity containment and recovery actions.

## Usage examples

### Triage an open case and open a ServiceNow incident

1. List open cases in the queue:
   `list_cases()`
2. Inspect full case context, alerts, and entities for case `12346`:
   `get_case_full_details(case_id=12346)`
3. Retrieve alert group identifiers and underlying alert events:
   `list_alert_group_identifiers_by_case(case_id=12346)`
   `list_events_by_alert(case_id=12346, alert_id=34567)`
4. Record responder notes and raise priority:
   `post_case_comment(case_id=12346, comment="Confirmed C2 callback on workstation-1234. Escalating to High.")`
   `change_case_priority(case_id=12346, case_priority="PriorityHigh")`
5. Open a linked ServiceNow incident (when started with `--integrations ServiceNow`):

   ```python
   service_now_create_incident(
     case_id=12346,
     alert_group_identifiers=["Malware_Detection_Group_23456"],
     short_description="Malware callback on workstation-1234",
     description="Isolate workstation-1234 and reimage per IR playbook.",
     urgency="1",
     impact="2",
   )
   ```

### Pivot across cases sharing a suspicious entity

1. Fetch alert-group entities for the active case:
   `get_entities_by_alert_group_identifiers(case_id=12346, alert_group_identifiers=["Network_Activity_Group_23457"])`
2. Inspect historical enrichment and associated case IDs for `203.0.113.100`:
   `get_entity_details(entity_identifier="203.0.113.100", entity_type="ADDRESS", entity_environment="Default Environment")`
3. Search SOAR for related suspicious internal assets:
   `search_entity(term="203.0.113.100", is_suspicious=True)`

## Additional resources

- [Google SecOps SOAR overview](https://cloud.google.com/chronicle/docs/soar/overview)
- [Google SecOps SOAR integrations reference](../soar_integrations/index.md)
- [Google SecOps SOAR playbooks documentation](https://cloud.google.com/chronicle/docs/soar/playbooks/overview)
