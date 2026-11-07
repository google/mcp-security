# Google Security Operations SIEM MCP server

The `google-secops-mcp` (`secops_mcp`) server connects MCP clients to Google Security Operations (Google SecOps) SIEM using the official [Google SecOps SDK for Python (`secops-wrapper`)](https://github.com/google/secops-wrapper). It registers 69 local stdio tools across UDM search, entity enrichment, alerts, custom YARA-L 2.0 detection rules, curated detections, exclusions, data tables, reference lists, watchlists, investigations, log ingestion, feeds, and parsers.

> **Tip:** If you prefer a Google-managed HTTPS endpoint without running a local Python process, see [Remote MCP server for Google SecOps](../remote_server.md). Use this local stdio server when you need SDK-backed helpers not exposed on the remote endpoint (such as `export_udm_search_csv`, `test_rule`, `ingest_raw_log`, `ingest_udm_events`, or `run_parser_against_sample_logs`) or per-call multi-tenant `project_id`, `customer_id`, and `region` overrides.

## Configuration

### Prerequisites and IAM roles

1. Access to a Google Security Operations SIEM tenant (`CHRONICLE_CUSTOMER_ID`, a UUID such as `a1b2c3d4-e5f6-4321-abcd-ef1234567890`) bound to a Google Cloud project (`CHRONICLE_PROJECT_ID`) with `chronicle.googleapis.com` enabled.
2. IAM roles on `CHRONICLE_PROJECT_ID`:
   - Read-only search, triage, and rule inspection: `roles/chronicle.viewer` (or granular viewer roles)
   - Rule authoring, exclusions, watchlists, feeds, parsers, and ingestion: `roles/chronicle.editor` or `roles/chronicle.admin`

### Authentication

By default, `secops_mcp` uses Application Default Credentials (ADC):

```bash
ACCOUNT="you@example.com"
gcloud auth login "$ACCOUNT" --update-adc
```

For headless automation or service-account execution where ADC is unavailable, set `SECOPS_SA_PATH` to a service account key file path. When `SECOPS_SA_PATH` is set, it takes precedence over ADC.

### Environment variables

On macOS and Linux:

```bash
export CHRONICLE_PROJECT_ID="your-project-id"
export CHRONICLE_CUSTOMER_ID="a1b2c3d4-e5f6-4321-abcd-ef1234567890"
export CHRONICLE_REGION="us"
# Optional: override ADC with a service account JSON key
# export SECOPS_SA_PATH="/path/to/service-account-key.json"
```

On Windows PowerShell:

```powershell
$Env:CHRONICLE_PROJECT_ID = "your-project-id"
$Env:CHRONICLE_CUSTOMER_ID = "a1b2c3d4-e5f6-4321-abcd-ef1234567890"
$Env:CHRONICLE_REGION = "us"
```

`CHRONICLE_REGION` defaults to `"us"` and accepts multi-region and regional Google SecOps API codes (such as `"us"`, `"eu"`, `"asia-southeast1"`, or `"europe-west2"`). Every tool also accepts optional `project_id`, `customer_id`, and `region` arguments to override the environment defaults on individual calls.

### MCP client configuration

Run from a local Git clone to access all 69 tools on `main` (including `update_rule`), loading environment variables from `.env`:

```json
{
  "mcpServers": {
    "secops": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/secops/secops_mcp",
        "run",
        "--env-file",
        "/path/to/mcp-security/.env",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

Or run the published PyPI package via `uvx`:

```json
{
  "mcpServers": {
    "secops": {
      "command": "uvx",
      "args": [
        "--from",
        "google-secops-mcp",
        "secops_mcp"
      ],
      "env": {
        "CHRONICLE_PROJECT_ID": "your-project-id",
        "CHRONICLE_CUSTOMER_ID": "a1b2c3d4-e5f6-4321-abcd-ef1234567890",
        "CHRONICLE_REGION": "us"
      }
    }
  }
}
```

For corporate proxy and custom TLS CA configuration (`HTTP_PROXY`, `HTTPS_PROXY`, and `REQUESTS_CA_BUNDLE`), see [Corporate proxies and custom TLS certificates](../usage_guide.md#corporate-proxies-and-custom-tls-certificates).

## Tools

All 69 tools accept optional `project_id`, `customer_id`, and `region` parameters that fall back to `CHRONICLE_PROJECT_ID`, `CHRONICLE_CUSTOMER_ID`, and `CHRONICLE_REGION`.

### UDM event search and export (4 tools)

- **`search_security_events(text, project_id=None, customer_id=None, hours_back=24, start_time=None, end_time=None, max_events=100, region=None)`**
  - Translates a natural-language request (`text`) into a Unified Data Model (UDM) query and executes it against Google SecOps SIEM over `hours_back` (default `24`) or an explicit ISO 8601 `start_time` and `end_time` window, returning both the generated UDM query and up to `max_events` events.
- **`search_udm(query, hours_back=24, start_time=None, end_time=None, max_events=None, project_id=None, customer_id=None, region=None)`**
  - Executes an explicit UDM query string (for example, `metadata.event_type = "PROCESS_LAUNCH" and target.process.file.full_path = /powershell/ nocase`) over `hours_back` or an ISO 8601 `start_time` and `end_time` range.
- **`export_udm_search_csv(query, fields, hours_back=24, start_time=None, end_time=None, case_insensitive=True, project_id=None, customer_id=None, region=None)`**
  - Exports UDM search results for `query` across the specified UDM `fields` list as CSV text.
- **`find_udm_field_values(query, page_size=None, project_id=None, customer_id=None, region=None)`**
  - Searches and autocompletes observed UDM field values matching `query` to verify exact field contents before writing UDM searches or YARA-L 2.0 rules.

### Entity enrichment, IOC matches, and threat intelligence (3 tools)

- **`lookup_entity(entity_value, project_id=None, customer_id=None, hours_back=24, region=None)`**
  - Summarizes Google SecOps entity context, first-seen and last-seen timestamps, related alerts, and activity counts for an IP address, domain, file hash, hostname, or username over `hours_back`.
- **`get_ioc_matches(project_id=None, customer_id=None, hours_back=24, max_matches=20, region=None)`**
  - Lists Indicators of Compromise (IOCs) that matched ingested telemetry within `hours_back` (up to `max_matches`).
- **`get_threat_intel(query, project_id=None, customer_id=None, region=None)`**
  - Answers threat actor, vulnerability, and security domain questions using Google SecOps integrated Gemini intelligence.

### Security alerts (3 tools)

- **`get_security_alerts(project_id=None, customer_id=None, hours_back=24, max_alerts=10, status_filter='feedback_summary.status != "CLOSED"', region=None)`**
  - Lists SIEM security alerts generated over `hours_back` matching `status_filter` (excludes closed alerts by default).
- **`get_security_alert_by_id(project_id=None, customer_id=None, region=None, alert_id=None, include_detections=True)`**
  - Retrieves full metadata and optional underlying rule detections (`include_detections=True`) for a single SIEM `alert_id`.
- **`do_update_security_alert(project_id=None, customer_id=None, region=None, alert_id=None, reason=None, priority=None, status=None, verdict=None, severity=None, comment=None, root_cause=None)`**
  - Updates feedback fields (`status`, `priority`, `verdict`, `severity`, `reason`, `root_cause`, and `comment`) on SIEM `alert_id`.

### Custom YARA-L 2.0 detection rules and retrohunts (12 tools)

Google SecOps detection rules are written in **YARA-L 2.0**, an event correlation and detection language built for UDM security logs (distinct from standard YARA, which scans binary files and payloads).

- **`list_security_rules(project_id=None, customer_id=None, region=None, page_size=100, page_token=None)`**
  - Lists custom YARA-L 2.0 detection rules with pagination (`page_size`, `page_token`).
- **`search_security_rules(query, project_id=None, customer_id=None, region=None)`**
  - Searches custom YARA-L 2.0 detection rules by regex pattern (`query`).
- **`get_detection_rule(rule_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves the full YARA-L 2.0 source text and revision metadata for `rule_id` (such as `"ru_a1b2c3d4-e5f6-4321-abcd-ef1234567890"`).
- **`validate_rule(rule_text, project_id=None, customer_id=None, region=None)`**
  - Validates YARA-L 2.0 syntax and UDM field types for `rule_text` without saving a rule. Always run `validate_rule` before `create_rule` or `update_rule`.
- **`test_rule(rule_text, project_id=None, customer_id=None, region=None, hours_back=168, max_results=100)`**
  - Evaluates draft YARA-L 2.0 `rule_text` streamingly against historical UDM events over `hours_back` (default `168` hours, 7 days) without persisting the rule, returning up to `max_results` sample detections.
- **`create_rule(rule_text, project_id=None, customer_id=None, region=None)`**
  - Creates a new custom YARA-L 2.0 detection rule from `rule_text`.
- **`update_rule(rule_id, rule_text, project_id=None, customer_id=None, region=None)`**
  - Updates an existing YARA-L 2.0 rule (`rule_id`) in place, creating a new rule revision while preserving its `rule_id`, deployment state, and detection history.
- **`get_rule_detections(rule_id, alert_state=None, page_size=None, page_token=None, project_id=None, customer_id=None, region=None, start_time=None, end_time=None, list_basis=None)`**
  - Lists historical detections produced by `rule_id`, optionally filtered by `alert_state` (`"ALERTING"` or `"NOT_ALERTING"`), ISO 8601 `start_time` and `end_time`, and `list_basis` (`"DETECTION_TIME"` or `"CREATED_TIME"`).
- **`list_rule_errors(rule_id, project_id=None, customer_id=None, region=None)`**
  - Lists runtime execution errors recorded for `rule_id`.
- **`create_retrohunt(rule_id, start_time, end_time, project_id=None, customer_id=None, region=None)`**
  - Starts an asynchronous retrohunt for `rule_id` across the ISO 8601 window from `start_time` to `end_time` and returns an `operation_id`.
- **`get_retrohunt(rule_id, operation_id, project_id=None, customer_id=None, region=None)`**
  - Checks completion status and progress for a retrohunt `operation_id` on `rule_id`.
- **`search_rule_alerts(start_time, end_time, max_alerts=10, project_id=None, customer_id=None, region=None)`**
  - Searches rule-generated alerts across all custom YARA-L 2.0 rules between ISO 8601 `start_time` and `end_time`, grouped by rule.

### Curated rules and rule set deployments (8 tools)

- **`list_curated_rules(project_id=None, customer_id=None, region=None, page_size=100, page_token=None, as_list=False)`**
  - Lists Google-managed curated detection rules (`as_list=True` auto-paginates all pages).
- **`get_curated_rule(rule_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves metadata for a curated rule by `rule_id` (for example, `"ur_..."`).
- **`get_curated_rule_by_name(display_name, project_id=None, customer_id=None, region=None)`**
  - Looks up a curated rule matching `display_name`.
- **`search_curated_detections(rule_id, start_time, end_time, project_id=None, customer_id=None, region=None, list_basis=None, alert_state=None, page_size=100, page_token=None)`**
  - Searches detections produced by curated rule `rule_id` between ISO 8601 `start_time` and `end_time`.
- **`list_curated_rule_sets(project_id=None, customer_id=None, region=None, page_size=100, page_token=None, as_list=False)`**
  - Lists Google Cloud Threat Intelligence (GCTI) curated rule sets.
- **`get_curated_rule_set(rule_set_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves details for a curated rule set by `rule_set_id`.
- **`list_curated_rule_set_deployments(project_id=None, customer_id=None, region=None, page_size=100, page_token=None, as_list=False)`**
  - Lists enabled state, `precision` tier (`"broad"` or `"precise"`), and alerting status across curated rule sets.
- **`update_curated_rule_set_deployment(category_id, rule_set_id, precision, enabled, alerting, project_id=None, customer_id=None, region=None)`**
  - Enables or disables a curated rule set (`category_id`, `rule_set_id`), sets `precision` (`"broad"` for wider hunting coverage or `"precise"` for lower-noise production alerting), and toggles `alerting`.

### Rule exclusions (6 tools)

- **`create_rule_exclusion(display_name, refinement_type, query, project_id=None, customer_id=None, region=None)`**
  - Creates a findings refinement exclusion (`refinement_type="DETECTION_EXCLUSION"`) defined by UDM filter `query`.
- **`get_rule_exclusion(exclusion_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves details and deployment bindings for `exclusion_id`.
- **`list_rule_exclusions(page_size=None, page_token=None, project_id=None, customer_id=None, region=None)`**
  - Lists configured rule exclusions with pagination.
- **`patch_rule_exclusion(exclusion_id, display_name=None, query=None, update_mask=None, project_id=None, customer_id=None, region=None)`**
  - Updates `display_name`, `query`, or both on `exclusion_id` using optional comma-separated `update_mask`.
- **`update_rule_exclusion_deployment(exclusion_id, enabled, archived, detection_exclusion_application, project_id=None, customer_id=None, region=None)`**
  - Attaches or detaches `exclusion_id` across `curatedRules`, `curatedRuleSets`, or custom `rules` via `detection_exclusion_application` and sets `enabled` and `archived` flags.
- **`compute_rule_exclusion_activity(exclusion_id, start_time, end_time, project_id=None, customer_id=None, region=None)`**
  - Computes match counts suppressed by `exclusion_id` between `start_time` and `end_time`.

### Data tables (4 tools)

Data tables store structured multi-column lookup rows referenced by YARA-L 2.0 rules and UDM searches.

- **`create_data_table(name, description, header, project_id=None, customer_id=None, region=None, rows=None)`**
  - Creates a multi-column data table with column schema `header` (mapping column names to column types) and optional initial `rows`.
- **`add_rows_to_data_table(table_name, rows, project_id=None, customer_id=None, region=None)`**
  - Appends `rows` (list of string value lists) to `table_name`.
- **`list_data_table_rows(table_name, project_id=None, customer_id=None, region=None, max_rows=50)`**
  - Lists up to `max_rows` rows from `table_name` along with row IDs.
- **`delete_data_table_rows(table_name, row_ids, project_id=None, customer_id=None, region=None)`**
  - Deletes the specified `row_ids` from `table_name`.

### Reference lists (3 tools)

Reference lists store single-column string, regex, or CIDR entries referenced with `in %list_name` inside YARA-L 2.0 rules and UDM queries.

- **`create_reference_list(name, description, entries, project_id=None, customer_id=None, region=None, syntax_type="STRING")`**
  - Creates a reference list (`syntax_type` accepts `"STRING"`, `"REGEX"`, or `"CIDR"`).
- **`get_reference_list(name, project_id=None, customer_id=None, region=None, include_entries=True)`**
  - Retrieves metadata and optional `entries` (`include_entries=True`) for reference list `name`.
- **`update_reference_list(name, project_id=None, customer_id=None, region=None, entries=None, description=None)`**
  - Updates `entries`, `description`, or both on reference list `name`.

### Watchlists (5 tools)

- **`create_watchlist(name, display_name, multiplying_factor, description, project_id=None, customer_id=None, region=None)`**
  - Creates an entity watchlist that multiplies entity risk scores by `multiplying_factor`.
- **`update_watchlist(watchlist_id, display_name=None, description=None, multiplying_factor=None, entity_population_mechanism=None, watchlist_user_preferences=None, project_id=None, customer_id=None, region=None)`**
  - Updates display metadata, `multiplying_factor`, population rules, or pinning preferences on `watchlist_id`.
- **`delete_watchlist(watchlist_id, force=False, project_id=None, customer_id=None, region=None)`**
  - Deletes `watchlist_id` (`force=True` deletes even when dependent entities exist).
- **`get_watchlist(watchlist_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves configuration and entity counts for `watchlist_id`.
- **`list_watchlists(page_size=None, page_token=None, as_list=False, project_id=None, customer_id=None, region=None)`**
  - Lists configured watchlists (`as_list=True` auto-paginates).

### Investigations (4 tools)

- **`list_investigations(page_size=50, page_token=None, project_id=None, customer_id=None, region=None)`**
  - Lists autonomous investigations in the tenant along with status, verdict, and confidence.
- **`get_investigation(investigation_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves findings, status, verdict, and confidence for `investigation_id`.
- **`trigger_investigation(alert_id, project_id=None, customer_id=None, region=None)`**
  - Launches a new investigation scoped to SIEM `alert_id`.
- **`fetch_associated_investigations(detection_type, alert_ids=None, case_ids=None, association_limit_per_detection=5, project_id=None, customer_id=None, region=None)`**
  - Retrieves investigations linked to `alert_ids` (`detection_type="ALERT"`) or `case_ids` (`detection_type="CASE"`).

### Log ingestion (3 tools)

- **`get_available_log_types(project_id=None, customer_id=None, region=None, search_term=None)`**
  - Lists supported Google SecOps ingestion `log_type` codes, optionally filtered by `search_term`.
- **`ingest_raw_log(log_type, log_message, project_id=None, customer_id=None, region=None, forwarder_id=None, labels=None, log_entry_time=None, collection_time=None)`**
  - Ingests a raw log string or list of raw log strings under `log_type` (for example, `"OKTA"` or `"WINDOWS_SYSMON"`), with optional `forwarder_id`, `labels`, and ISO 8601 timestamps.
- **`ingest_udm_events(udm_events, project_id=None, customer_id=None, region=None)`**
  - Ingests one UDM event dictionary or a list of structured UDM event dictionaries directly into Google SecOps SIEM (useful for detection-engineering synthetic event testing).

### Feed management (8 tools)

- **`list_feeds(project_id=None, customer_id=None, region=None)`**: Lists configured data feeds.
- **`get_feed(feed_id, project_id=None, customer_id=None, region=None)`**: Retrieves configuration and state for `feed_id`.
- **`create_feed(display_name, feed_details, project_id=None, customer_id=None, region=None)`**: Creates a new data feed from `feed_details`.
- **`update_feed(feed_id, display_name=None, feed_details=None, project_id=None, customer_id=None, region=None)`**: Updates `display_name` or `feed_details` on `feed_id`.
- **`enable_feed(feed_id, project_id=None, customer_id=None, region=None)`**: Enables an inactive feed.
- **`disable_feed(feed_id, project_id=None, customer_id=None, region=None)`**: Disables an active feed.
- **`delete_feed(feed_id, project_id=None, customer_id=None, region=None)`**: Deletes `feed_id`.
- **`generate_feed_secret(feed_id, project_id=None, customer_id=None, region=None)`**: Generates an authentication secret for webhook or push `feed_id` types.

### Parser management (6 tools)

- **`list_parsers(log_type="-", page_size=None, page_token=None, filter=None, project_id=None, customer_id=None, region=None)`**
  - Lists custom Logstash-style CBN parsers across all log types (`log_type="-"`) or for a single `log_type`.
- **`get_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
  - Retrieves parser code and lifecycle state for `parser_id` under `log_type`.
- **`run_parser_against_sample_logs(log_type, parser_code, sample_logs, project_id=None, customer_id=None, region=None, parser_extension_code=None, statedump_allowed=False)`**
  - Tests `parser_code` (and optional `parser_extension_code`) against `sample_logs` in memory and returns the resulting UDM output or parse errors before deployment.
- **`create_parser(log_type, parser_code, project_id=None, customer_id=None, region=None, validated_on_empty_logs=True)`**
  - Submits a new custom parser for `log_type`.
- **`activate_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
  - Activates validated custom parser `parser_id` for `log_type`.
- **`deactivate_parser(log_type, parser_id, project_id=None, customer_id=None, region=None)`**
  - Deactivates custom parser `parser_id` for `log_type`.

## Usage examples

### Validate, backtest, and deploy a YARA-L 2.0 rule

1. Discover exact UDM field values in your tenant before authoring the rule:

   ```python
   find_udm_field_values(query="powershell")
   ```

2. Validate syntax and backtest the draft YARA-L 2.0 rule over 7 days of historical UDM logs without saving:

   ```python
   validate_rule(rule_text=draft_yaral2_rule)
   test_rule(rule_text=draft_yaral2_rule, hours_back=168, max_results=50)
   ```

3. Persist the rule or update an existing rule ID in place:

   ```python
   create_rule(rule_text=draft_yaral2_rule)
   # Or update an existing rule revision in place:
   update_rule(
     rule_id="ru_a1b2c3d4-e5f6-4321-abcd-ef1234567890",
     rule_text=updated_yaral2_rule,
   )
   ```

4. Run a 7-day historical retrohunt and poll its operation status:

   ```python
   create_retrohunt(
     rule_id="ru_a1b2c3d4-e5f6-4321-abcd-ef1234567890",
     start_time="2026-04-01T00:00:00Z",
     end_time="2026-04-08T00:00:00Z",
   )
   get_retrohunt(
     rule_id="ru_a1b2c3d4-e5f6-4321-abcd-ef1234567890",
     operation_id="oh_a1b2c3d4-e5f6-4321-abcd-ef1234567890",
   )
   ```

### Hunt UDM telemetry and export results to CSV

1. Run a natural-language or explicit UDM search for encoded PowerShell execution:

   ```python
   search_udm(
     query='metadata.event_type = "PROCESS_LAUNCH" and target.process.command_line = /-(enc|encodedcommand)/ nocase',
     hours_back=72,
     max_events=100,
   )
   ```

2. Enrich a destination IP found in the process events:

   ```python
   lookup_entity(entity_value="203.0.113.100", hours_back=168)
   ```

3. Export matching fields to CSV for incident reporting:

   ```python
   export_udm_search_csv(
     query='principal.ip = "10.0.0.25" and target.ip = "203.0.113.100"',
     fields=[
       "metadata.event_timestamp",
       "metadata.event_type",
       "principal.hostname",
       "principal.user.userid",
       "target.process.command_line",
     ],
     hours_back=72,
   )
   ```

## Additional resources

- [Google Security Operations documentation](https://cloud.google.com/chronicle/docs/overview)
- [Google Security Operations REST API reference](https://cloud.google.com/chronicle/docs/reference/rest)
- [Unified Data Model (UDM) field list](https://cloud.google.com/chronicle/docs/reference/udm-field-list)
- [YARA-L 2.0 language syntax reference](https://cloud.google.com/chronicle/docs/reference/yara-l-2-0-syntax)
