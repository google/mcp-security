# Google Cloud Security Command Center (SCC) MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google Cloud Security Command Center (SCC) and Cloud Asset Inventory (CAI).

## Features

### Available Tools

- **`search_findings(project_id, finding_class=None, severity=None, state="ACTIVE", category=None, ...)`**
    - **Description**: Searches and lists ALL types of Security Command Center findings with flexible filtering. Returns full finding details including descriptions, remediation steps, severity, attack exposure, and all associated metadata.
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `finding_class` (optional): Filter by finding class. Valid values: `VULNERABILITY`, `THREAT`, `MISCONFIGURATION`, `OBSERVATION`, `SCC_ERROR`, `POSTURE_VIOLATION`, `TOXIC_COMBINATION`, `SENSITIVE_DATA_RISK`, `CHOKEPOINT`. Supports OR (e.g., `'THREAT OR MISCONFIGURATION'`).
        - `severity` (optional): Filter by severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Supports OR (e.g., `'HIGH OR CRITICAL'`).
        - `state` (optional): Filter by state: `ACTIVE`, `INACTIVE`. Defaults to `ACTIVE`. Set to `None` for all states.
        - `category` (optional): Filter by finding category (e.g., `PUBLIC_BUCKET_ACL`, `XSS`, `OPEN_FIREWALL`).
        - `resource_name` (optional): Filter by the full resource name associated with the finding.
        - `resource_type` (optional): Filter by resource type (e.g., `google.compute.Instance`).
        - `mute` (optional): Filter by mute status: `MUTED`, `UNMUTED`, `UNDEFINED`.
        - `custom_filter` (optional): Raw SCC filter string appended via AND for advanced filtering.
        - `max_findings` (optional): Maximum number of findings to return. Defaults to 50.
        - `location` (optional): Google Cloud location for SCC v2. Defaults to `global`.
        - `order_by` (optional): Ordering of results. Defaults to `event_time desc`.

- **`get_finding_details(project_id, finding_id, location="global", include_resource_details=True)`**
    - **Description**: Gets the full details of a specific finding by its ID, including description, remediation steps, severity, attack exposure, compliance information, MITRE ATT&CK data, vulnerability details, and optionally the affected resource details from Cloud Asset Inventory (CAI). Works for any finding class.
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID.
        - `finding_id` (required): The ID of the finding to retrieve.
        - `location` (optional): Google Cloud location for SCC v2. Defaults to `global`.
        - `include_resource_details` (optional): Whether to fetch resource details from CAI. Defaults to `True`.

- **`search_findings_by_compliance(project_id, search_text=None, compliance_standard=None, compliance_version=None, compliance_id=None, ...)`**
    - **Description**: Searches SCC findings by compliance framework information (CIS benchmarks, PCI DSS, NIST 800-53, ISO 27001, etc.) or by free-text search on finding descriptions and categories. Use when you have a compliance control name or description (e.g., 'ServiceAccount should not have Admin privileges') and want to find the corresponding SCC findings.
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID.
        - `search_text` (optional): Free-text to search across finding descriptions, categories, and compliance standard names (case-insensitive). Examples: `'ServiceAccount should not have Admin privileges'`, `'log metric filter'`, `'MFA'`.
        - `compliance_standard` (optional): Filter by compliance standard name (case-insensitive partial match). Examples: `'CIS'`, `'PCI DSS'`, `'NIST 800-53'`.
        - `compliance_version` (optional): Filter by standard version (exact match). Examples: `'1.3.0'`, `'2.0'`.
        - `compliance_id` (optional): Filter by control ID (exact match). Examples: `'1.5'`, `'4.1'`.
        - `severity` (optional): Pre-filter by severity. Supports OR (e.g., `'HIGH OR CRITICAL'`).
        - `state` (optional): Filter by state. Defaults to `ACTIVE`.
        - `max_findings` (optional): Maximum findings to return. Defaults to 50.
        - `location` (optional): Google Cloud location for SCC v2. Defaults to `global`.

- **`set_finding_mute(project_id, finding_id, mute, location="global")`**
    - **Description**: Mutes or unmutes a specific SCC finding. Muted findings are hidden from default views but retained for compliance. Use to suppress accepted risks or resurface previously muted findings.
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID.
        - `finding_id` (required): The ID of the finding to mute or unmute.
        - `mute` (required): The mute state to set: `MUTED` or `UNMUTED`.
        - `location` (optional): Google Cloud location for SCC v2. Defaults to `global`.

- **`top_vulnerability_findings(project_id, max_findings=20, location="global")`**
    - **Description**: Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project, sorted by Attack Exposure Score (descending). Fetches up to 10× `max_findings` candidates (capped at 1000) to ensure the sort is meaningful across the full population. Includes Attack Exposure score and remediation steps (`nextSteps`).
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `max_findings` (optional): The maximum number of findings to return. Defaults to 20.
        - `location` (optional): Google Cloud location for SCC v2. Defaults to `global`.

- **`get_finding_remediation(project_id, resource_name=None, category=None, finding_id=None)`**
    - **Description**: Gets the remediation steps (`nextSteps`) for a specific finding within a project, along with details of the affected resource fetched from Cloud Asset Inventory (CAI). The finding can be identified either by its `resource_name` and `category` (for ACTIVE findings) or directly by its `finding_id` (regardless of state).
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `resource_name` (optional): The full resource name associated with the finding (e.g., `//container.googleapis.com/projects/my-project/locations/us-central1/clusters/my-cluster`). Required if `finding_id` is not provided.
        - `category` (optional): The category of the finding (e.g., `GKE_SECURITY_BULLETIN`). Required if `finding_id` is not provided.
        - `finding_id` (optional): The ID of the finding to search for directly (e.g., `finding123`). Required if `resource_name` and `category` are not provided.

## Configuration

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

**NOTE:** For OSX users, if you used [this one-liner](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to install uv, use the full path to the uv binary for the "command" value below, as uv will not be placed in the system path for Claude to use! For example: `/Users/yourusername/.local/bin/uv` instead of just `uv`.

```json
{
  "mcpServers": {
    "scc-mcp": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/scc",
        "run",
        "scc_mcp.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Authentication

The server uses Google Cloud's authentication mechanisms. Ensure you have one of the following configured in the environment where the server runs:

1. Application Default Credentials (ADC) set up (e.g., via `gcloud auth application-default login`).
2. The `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to a valid service account key file.

### Required IAM Permissions

Appropriate IAM permissions are required on the target Google Cloud project(s):
- Security Command Center: `roles/securitycenter.adminViewer` (read-only tools) or `roles/securitycenter.adminEditor` (required for `set_finding_mute`)
- Cloud Asset Inventory: `roles/cloudasset.viewer`

## License

Apache 2.0

## Development

The project is structured as follows:
- `scc_mcp.py`: Main MCP server implementation