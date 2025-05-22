# Google Cloud Security Command Center (SCC) MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google Cloud Security Command Center (SCC) and Cloud Asset Inventory (CAI).

## Features

### Available Tools

- **`top_vulnerability_findings(project_id, max_findings=20)`**
    - **Description**: Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project, sorted by Attack Exposure Score (descending). Includes the Attack Exposure score in the output if available. Aids prioritization for remediation.
    - **Parameters**:
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `max_findings` (optional): The maximum number of findings to return. Defaults to 20.

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
- Security Command Center: `roles/securitycenter.adminViewer` or `roles/securitycenter.adminEditor`
- Cloud Asset Inventory: `roles/cloudasset.viewer`

## License

Apache 2.0

## Development

The project is structured as follows:
- `scc_mcp.py`: Main MCP server implementation