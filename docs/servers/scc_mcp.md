# Security Command Center (SCC) MCP Server

This server provides tools for interacting with Google Cloud Security Command Center (SCC) and Cloud Asset Inventory (CAI).

**Note:** This server requires Application Default Credentials (ADC) to be configured in the environment where it runs (e.g., via `gcloud auth application-default login`).

## Tools

- **`top_vulnerability_findings(project_id, max_findings=20)`**
    - **Description:** Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project, sorted by Attack Exposure Score (descending). Includes the Attack Exposure score in the output if available. Aids prioritization for remediation.
    - **Parameters:**
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `max_findings` (optional): The maximum number of findings to return. Defaults to 20.

- **`get_finding_remediation(project_id, resource_name=None, category=None, finding_id=None)`**
    - **Description:** Gets the remediation steps (`nextSteps`) for a specific finding within a project, along with details of the affected resource fetched from Cloud Asset Inventory (CAI). The finding can be identified either by its `resource_name` and `category` (for ACTIVE findings) or directly by its `finding_id` (regardless of state).
    - **Parameters:**
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `resource_name` (optional): The full resource name associated with the finding (e.g., `//container.googleapis.com/projects/my-project/locations/us-central1/clusters/my-cluster`). Required if `finding_id` is not provided.
        - `category` (optional): The category of the finding (e.g., `GKE_SECURITY_BULLETIN`). Required if `finding_id` is not provided.
        - `finding_id` (optional): The ID of the finding to search for directly (e.g., `finding123`). Required if `resource_name` and `category` are not provided.
