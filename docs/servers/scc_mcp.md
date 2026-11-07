# Security Command Center MCP server

The `scc-mcp` server connects MCP clients to the Google Cloud Security Command Center (SCC) v2 API and the Cloud Asset Inventory (CAI) API. Every tool accepts either a Google Cloud `project_id` or an `organization_id` along with an SCC v2 `location` (default `"global"`).

## Configuration

### Authentication and IAM permissions

1. Authenticate Application Default Credentials (ADC), or configure Workload Identity or `GOOGLE_APPLICATION_CREDENTIALS` in automated environments:

   ```bash
   ACCOUNT="you@example.com"
   gcloud auth login "$ACCOUNT" --update-adc
   ```

2. Grant the caller the required IAM roles on the target project or organization:
   - Read findings: `roles/securitycenter.findingsViewer` or `roles/securitycenter.adminViewer`
   - Mute or unmute findings (`set_finding_mute`): `roles/securitycenter.findingsStateSetter` or `roles/securitycenter.adminEditor`
   - Enrich affected resources (`get_finding_details`, `get_finding_remediation`): `roles/cloudasset.viewer`

3. Enable the required APIs on your Google Cloud project:
   - Security Command Center API: `securitycenter.googleapis.com`
   - Cloud Asset Inventory API: `cloudasset.googleapis.com`

### MCP client configuration

Run from a local Git clone to access all 6 SCC v2 tools on `main`:

```json
{
  "mcpServers": {
    "scc-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-security/server/scc",
        "run",
        "scc_mcp.py"
      ],
      "env": {}
    }
  }
}
```

Or run the published PyPI package with `uvx`:

```json
{
  "mcpServers": {
    "scc-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "scc-mcp",
        "scc_mcp"
      ],
      "env": {}
    }
  }
}
```

> **Note:** Until the next PyPI release of `scc-mcp` lands, run from a local Git clone when you need `search_findings`, `get_finding_details`, `search_findings_by_compliance`, or `set_finding_mute`.

For corporate proxy and custom TLS CA configuration (`GRPC_DEFAULT_SSL_ROOTS_FILE_PATH` and `REQUESTS_CA_BUNDLE`), see [Corporate proxies and custom TLS certificates](../usage_guide.md#corporate-proxies-and-custom-tls-certificates).

## Tools

All 6 tools require either `project_id` or `organization_id`. When `organization_id` is set, the server queries `organizations/<organization_id>/sources/-/locations/<location>` across all projects in that organization.

### Finding search and details

- **`search_findings(project_id=None, organization_id=None, finding_class=None, severity=None, state="ACTIVE", category=None, resource_name=None, resource_type=None, mute=None, custom_filter=None, max_findings=50, location="global", order_by="event_time desc")`**
  - Lists Security Command Center v2 findings for a project or organization with server-side filtering.
  - **Parameters:**
    - `project_id` (optional): Google Cloud project ID (for example, `"your-project-id"`). Provide either `project_id` or `organization_id`.
    - `organization_id` (optional): Google Cloud organization ID (for example, `"123456789012"`).
    - `finding_class` (optional): Filter by finding class: `VULNERABILITY`, `THREAT`, `MISCONFIGURATION`, `OBSERVATION`, `SCC_ERROR`, `POSTURE_VIOLATION`, `TOXIC_COMBINATION`, `SENSITIVE_DATA_RISK`, or `CHOKEPOINT`. Combine multiple classes with `OR` or commas (for example, `"THREAT OR MISCONFIGURATION"`).
    - `severity` (optional): Filter by `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`. Combine values with `OR` or commas (for example, `"HIGH OR CRITICAL"`).
    - `state` (optional): `"ACTIVE"` (default), `"INACTIVE"`, or `""` to return both states.
    - `category` (optional): Exact finding category (for example, `"PUBLIC_BUCKET_ACL"` or `"OPEN_FIREWALL"`).
    - `resource_name` (optional): Full Cloud Asset resource name associated with the finding.
    - `resource_type` (optional): Resource type filter (for example, `"google.compute.Instance"` or `"google.storage.Bucket"`).
    - `mute` (optional): `"MUTED"`, `"UNMUTED"`, or `"UNDEFINED"`.
    - `custom_filter` (optional): Raw SCC filter expression appended with `AND`.
    - `max_findings` (optional): Maximum findings to return (default `50`, capped at `1000` per page).
    - `location` (optional): SCC v2 location (default `"global"`).
    - `order_by` (optional): Sort order (default `"event_time desc"`; also supports `"severity desc"` and `"create_time desc"`).
  - **Returns:** Dictionary containing `findings`, `count`, `filter_applied`, and `more_findings_may_exist`.

- **`get_finding_details(project_id=None, organization_id=None, finding_id=None, location="global", include_resource_details=True)`**
  - Retrieves full metadata for a single finding by ID across any finding class, including description, remediation steps, attack exposure, compliance mappings, MITRE ATT&CK fields, vulnerability CVE records, and optional Cloud Asset Inventory metadata.
  - **Parameters:**
    - `project_id` (optional): Google Cloud project ID. Provide either `project_id` or `organization_id`.
    - `organization_id` (optional): Google Cloud organization ID.
    - `finding_id` (required): Finding ID to look up.
    - `location` (optional): SCC v2 location (default `"global"`).
    - `include_resource_details` (optional): Fetch affected asset metadata from Cloud Asset Inventory when `True` (default `True`).
  - **Returns:** Dictionary containing `finding`, `finding_id`, and `resource_details_cai` (when requested).

- **`search_findings_by_compliance(project_id=None, organization_id=None, search_text=None, compliance_standard=None, compliance_version=None, compliance_id=None, severity=None, state="ACTIVE", max_findings=50, location="global")`**
  - Searches findings by compliance framework metadata (such as CIS benchmarks, PCI DSS, NIST 800-53, or ISO 27001) or by case-insensitive text across finding descriptions, categories, and compliance standard names. Provide at least one of `search_text`, `compliance_standard`, or `compliance_id`.
  - **Parameters:**
    - `project_id` (optional): Google Cloud project ID. Provide either `project_id` or `organization_id`.
    - `organization_id` (optional): Google Cloud organization ID.
    - `search_text` (optional): Case-insensitive substring matched against finding description, category, or compliance standard name.
    - `compliance_standard` (optional): Case-insensitive partial standard name (for example, `"CIS"`, `"PCI DSS"`, `"NIST 800-53"`, or `"ISO 27001"`).
    - `compliance_version` (optional): Exact benchmark or standard version (for example, `"1.3.0"` or `"2.0"`).
    - `compliance_id` (optional): Exact control identifier (for example, `"1.5"` or `"6.2.1"`).
    - `severity` (optional): API pre-filter for `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` (supports `OR`).
    - `state` (optional): `"ACTIVE"` (default), `"INACTIVE"`, or `""` for all states.
    - `max_findings` (optional): Maximum matching findings to return (default `50`).
    - `location` (optional): SCC v2 location (default `"global"`).
  - **Returns:** Dictionary containing `findings` (each enriched with `compliance_summary`), `count`, `scanned_count`, `filters_applied`, and `more_findings_may_exist`.

### Vulnerability prioritization, remediation, and muting

- **`top_vulnerability_findings(project_id=None, organization_id=None, max_findings=20, location="global")`**
  - Lists active `HIGH` and `CRITICAL` findings of class `VULNERABILITY` sorted by `attackExposureScore` descending. Over-fetches up to `10x` `max_findings` (capped at `1000`) before sorting so high-exposure findings beyond the first API page surface reliably.
  - **Parameters:**
    - `project_id` (optional): Google Cloud project ID. Provide either `project_id` or `organization_id`.
    - `organization_id` (optional): Google Cloud organization ID.
    - `max_findings` (optional): Maximum findings to return after sorting (default `20`).
    - `location` (optional): SCC v2 location (default `"global"`).
  - **Returns:** Dictionary containing `top_findings` (`name`, `category`, `resourceName`, `severity`, `description`, `nextSteps`, `attackExposureScore`), `count`, `fetched_for_sorting`, and `more_findings_exist_beyond_fetch_limit`.

- **`get_finding_remediation(project_id=None, organization_id=None, resource_name=None, category=None, finding_id=None, location="global")`**
  - Retrieves remediation instructions (`nextSteps`) for a finding together with Cloud Asset Inventory metadata for the affected resource. Identify the target either with `finding_id` (any state) or with both `resource_name` and `category` (`ACTIVE` findings).
  - **Parameters:**
    - `project_id` (optional): Google Cloud project ID. Provide either `project_id` or `organization_id`.
    - `organization_id` (optional): Google Cloud organization ID.
    - `resource_name` (optional): Full resource name (required when `finding_id` is omitted).
    - `category` (optional): Finding category such as `"GKE_SECURITY_BULLETIN"` (required when `finding_id` is omitted).
    - `finding_id` (optional): Finding ID to look up directly.
    - `location` (optional): SCC v2 location (default `"global"`).
  - **Returns:** Dictionary containing `remediation_steps`, `finding_name`, `description`, `resource_name`, `resource_details_cai`, and `finding_details`.

- **`set_finding_mute(project_id=None, organization_id=None, finding_id=None, mute=None, location="global")`**
  - Mutes or unmutes an SCC v2 finding by resolving its canonical source path and calling `SetMuteFindingRequest`. Muted findings stay stored for compliance reporting while hidden from default active queues.
  - **Parameters:**
    - `project_id` (optional): Google Cloud project ID. Provide either `project_id` or `organization_id`.
    - `organization_id` (optional): Google Cloud organization ID.
    - `finding_id` (required): Finding ID to update.
    - `mute` (required): Target mute state, either `"MUTED"` or `"UNMUTED"`.
    - `location` (optional): SCC v2 location (default `"global"`).
  - **Returns:** Dictionary containing `success`, `finding_name`, `mute_state`, and the updated `finding`.

## Usage examples

### Triage top exposed vulnerabilities and fetch remediation steps

1. Rank high-exposure vulnerabilities across an organization:

   ```python
   top_vulnerability_findings(organization_id="123456789012", max_findings=10)
   ```

2. Pull remediation steps and Cloud Asset Inventory metadata for a specific finding:

   ```python
   get_finding_remediation(
     project_id="your-project-id",
     resource_name="//storage.googleapis.com/projects/your-project-id/buckets/example-bucket",
     category="PUBLIC_BUCKET_ACL",
   )
   ```

### Audit CIS compliance controls and mute accepted risk

1. Find active `HIGH` or `CRITICAL` CIS benchmark violations across a project:

   ```python
   search_findings_by_compliance(
     project_id="your-project-id",
     compliance_standard="CIS",
     severity="HIGH OR CRITICAL",
   )
   ```

2. Mute a documented exception after review:

   ```python
   set_finding_mute(
     project_id="your-project-id",
     finding_id="a1b2c3d4e5f678901234567890abcdef",
     mute="MUTED",
   )
   ```

## Additional resources

- [Security Command Center documentation](https://cloud.google.com/security-command-center/docs)
- [Attack exposure scores in Security Command Center](https://cloud.google.com/security-command-center/docs/concepts-attack-path-and-exposure-concepts)
- [Cloud Asset Inventory documentation](https://cloud.google.com/asset-inventory/docs)
