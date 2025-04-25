# Security Command Center (SCC) MCP Server

This server provides tools for interacting with Google Cloud Security Command Center (SCC) and Cloud Asset Inventory (CAI).

## Configuration

This server requires Google Cloud authentication to access SCC and CAI APIs:

1. **Set up Google Cloud Authentication** using one of these methods:
   - Application Default Credentials (ADC): `gcloud auth application-default login`
   - Service account key: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
   - Workload Identity (for GKE deployments)

2. **Required IAM Permissions:**
   - Security Command Center: `roles/securitycenter.adminViewer` or `roles/securitycenter.adminEditor`
   - Cloud Asset Inventory: `roles/cloudasset.viewer`

3. **Enable Required APIs** in your Google Cloud Project:
   - Security Command Center API: `securitycenter.googleapis.com`
   - Cloud Asset Inventory API: `cloudasset.googleapis.com`

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

```json
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
      "disabled": false,
      "autoApprove": []
    }
```

This server relies primarily on Google Cloud Authentication, which is typically set up system-wide rather than through environment variables in the configuration.

## Tools

- **`top_vulnerability_findings(project_id, max_findings=20)`**
    - **Description:** Lists the top ACTIVE, HIGH or CRITICAL severity findings of class VULNERABILITY for a specific project, sorted by Attack Exposure Score (descending). Includes the Attack Exposure score in the output if available. Aids prioritization for remediation.
    - **Parameters:**
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `max_findings` (optional): The maximum number of findings to return. Defaults to 20.
    - **Returns:** A structured list of vulnerability findings with the following information for each:
        - Finding ID
        - Category
        - Severity
        - Attack Exposure Score (if available)
        - Resource Name
        - State
        - Description
        - First Observed Time
        - Last Observed Time

- **`get_finding_remediation(project_id, resource_name=None, category=None, finding_id=None)`**
    - **Description:** Gets the remediation steps (`nextSteps`) for a specific finding within a project, along with details of the affected resource fetched from Cloud Asset Inventory (CAI). The finding can be identified either by its `resource_name` and `category` (for ACTIVE findings) or directly by its `finding_id` (regardless of state).
    - **Parameters:**
        - `project_id` (required): The Google Cloud project ID (e.g., 'my-gcp-project').
        - `resource_name` (optional): The full resource name associated with the finding (e.g., `//container.googleapis.com/projects/my-project/locations/us-central1/clusters/my-cluster`). Required if `finding_id` is not provided.
        - `category` (optional): The category of the finding (e.g., `GKE_SECURITY_BULLETIN`). Required if `finding_id` is not provided.
        - `finding_id` (optional): The ID of the finding to search for directly (e.g., `finding123`). Required if `resource_name` and `category` are not provided.
    - **Returns:** A structured report containing:
        - Finding details (category, severity, description)
        - Next steps for remediation
        - Resource metadata from Cloud Asset Inventory
        - Links to relevant documentation

## Usage Examples

### Example 1: Identifying Critical Vulnerabilities

To identify the most critical vulnerabilities in a project for prioritized remediation:

```
1. Call top_vulnerability_findings("my-project-id", 10)
2. Review the returned list, focusing on findings with high Attack Exposure Scores
3. For each critical finding, note the resource_name and category
```

Sample interaction:
```
User: What are the top critical vulnerabilities in my GCP project 'my-project-id'?

AI: I'll check for critical vulnerabilities in your project.

[AI uses the tool: top_vulnerability_findings("my-project-id", 10)]

Here are the top critical vulnerabilities in your project, sorted by exposure risk:

1. PUBLIC_BUCKET_ACL (Attack Exposure Score: 9.8)
   Resource: //storage.googleapis.com/projects/my-project-id/buckets/sensitive-data-bucket
   Description: Bucket has publicly accessible permissions

2. OPEN_FIREWALL (Attack Exposure Score: 8.6)
   Resource: //compute.googleapis.com/projects/my-project-id/global/firewalls/allow-all
   Description: Firewall rule allows unrestricted access
```

### Example 2: Getting Remediation Steps

To obtain detailed remediation guidance for a specific finding:

```
1. Identify the finding using top_vulnerability_findings
2. Call get_finding_remediation with the project_id and either:
   a. resource_name and category (for active findings)
   b. finding_id (for any finding state)
3. Follow the provided remediation steps to resolve the issue
```

Sample interaction:
```
User: How do I fix the PUBLIC_BUCKET_ACL vulnerability for my sensitive-data-bucket?

AI: I'll get the remediation steps for you.

[AI uses the tool: get_finding_remediation(
  project_id="my-project-id",
  resource_name="//storage.googleapis.com/projects/my-project-id/buckets/sensitive-data-bucket",
  category="PUBLIC_BUCKET_ACL"
)]

Here's how to fix this vulnerability:

1. Remove public access by updating bucket permissions:
   - Go to Cloud Storage > Buckets > sensitive-data-bucket
   - Click on "Permissions" tab
   - Remove entries with "allUsers" or "allAuthenticatedUsers"
   - Alternatively, use the gcloud command:
     `gsutil iam ch -d allUsers:objectViewer gs://sensitive-data-bucket`

2. Consider using IAM Conditions to restrict access based on:
   - IP ranges
   - Time-based access
   - Resource attributes

3. Enable bucket-level access logs to monitor access patterns
```

## Additional Resources

- [Security Command Center Documentation](https://cloud.google.com/security-command-center/docs)
- [Understanding Attack Exposure Scores](https://cloud.google.com/security-command-center/docs/concepts-attack-path-and-exposure-concepts)
- [Cloud Asset Inventory Documentation](https://cloud.google.com/asset-inventory/docs)
