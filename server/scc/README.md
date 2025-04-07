# Google Cloud Security Command Center (SCC) MCP Server

This directory contains an MCP server (`scc_mcp.py`) that enables interaction with Google Cloud Security Command Center (SCC) via MCP clients.

## Authentication

The server uses Google Cloud's authentication mechanisms. Ensure you have one of the following configured in the environment where the server runs:

1.  Application Default Credentials (ADC) set up (e.g., via `gcloud auth application-default login`).
2.  The `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to a valid service account key file.

## Authorization

Appropriate IAM permissions are required on the target Google Cloud project(s) to list findings (e.g., `securitycenter.findings.list`) and search resources in Cloud Asset Inventory (`cloudasset.assets.searchAllResources`).

## Client Configuration Example

Add the following configuration to your MCP client (e.g., `claude_desktop_config.json` or `cline_mcp_settings.json`), ensuring the path in `args` points to the correct location of `scc_mcp.py`:

```json
{
  "mcpServers": {
    // ... other servers ...
    "scc-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/the/repo/server/scc",
        "run",
        "scc_mcp.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
    // ... other servers ...
  }
}
```

## Available Tools

### `top_vulnerability_findings`

*   **Description**: Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project, sorted by Attack Exposure Score (descending). Includes the Attack Exposure score in the output if available. Aids prioritization for remediation.
*   **Parameters**:
    *   `project_id` (string, required): The Google Cloud project ID (e.g., 'my-gcp-project').
    *   `max_findings` (integer, optional): The maximum number of findings to return. Defaults to 20.
*   **Returns**: A dictionary containing `top_findings` (a list of finding summaries including `attackExposureScore`), `count`, and `more_findings_exist_beyond_fetch_limit`.

### `get_finding_remediation`

*   **Description**: Gets the remediation steps (nextSteps) for a specific finding within a project, along with details of the affected resource fetched from Cloud Asset Inventory (CAI). The finding can be identified either by its `resource_name` and `category` (for ACTIVE findings) or directly by its `finding_id` (using the V1 client's list_findings with a name filter).
*   **Parameters**:
    *   `project_id` (string, required): The Google Cloud project ID (e.g., 'my-gcp-project').
    *   `resource_name` (string, optional): The full resource name associated with the finding (e.g., '//compute.googleapis.com/...'). Required if `finding_id` is not provided.
    *   `category` (string, optional): The category of the finding (e.g., 'PUBLIC_IP_ADDRESS'). Required if `finding_id` is not provided.
    *   `finding_id` (string, optional): The specific ID of the finding. Required if `resource_name` and `category` are not provided.
*   **Returns**: A dictionary containing `remediation_steps`, `finding_name`, `description`, `resource_name`, `resource_details_cai` (from Cloud Asset Inventory), and the full `finding_details` from SCC.
#