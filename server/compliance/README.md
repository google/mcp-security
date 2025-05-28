# Google Cloud Security Compliance MCP Server

This is an MCP (Model Context Protocol) server for interacting with Google Cloud Security Compliance API.

## Features

### Available Tools

- **`list_frameworks(parent, page_size=50)`**
    - **Description**: Lists available compliance frameworks for a given parent resource (organization, folder, or project). Returns information about available compliance frameworks and their details.
    - **Parameters**:
        - `parent` (required): The parent resource name (e.g., 'organizations/123456', 'folders/123456', or 'projects/my-project').
        - `page_size` (optional): The maximum number of frameworks to return. Defaults to 50.

- **`list_constraints(parent)`**
    - **Description**: Returns details of all available Org Policy constraints for a given resource: (organization, folder, or project). 
    - **Parameters**:
        - `parent` (required): The parent resource name (e.g., 'organizations/123456', 'folders/123456', or 'projects/my-project').

- **`list_active_policies(parent)`**
    - **Description**: Returns details of all active/enforced Org Policy policies for a given resource: (organization, folder, or project). 
    - **Parameters**:
        - `parent` (required): The parent resource name (e.g., 'organizations/123456', 'folders/123456', or 'projects/my-project').
      

## Configuration

### MCP Server Configuration

Add the following configuration to your MCP client's settings file:

```json
{
  "mcpServers": {
    "compliance-mcp": {
      "command": "uv",
      "args": [
        "--env-file=/path/to/your/env",
        "--directory",
        "/path/to/the/repo/server/compliance",
        "run",
        "compliance_mcp.py"
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
- Cloud Security Compliance: `roles/cloudsecuritycompliance.viewer` or `roles/cloudsecuritycompliance.admin`

## License

Apache 2.0

## Development

The project is structured as follows:
- `compliance_mcp.py`: Main MCP server implementation

## Usage Examples

### List Frameworks
```python
# List frameworks for an organization
await list_frameworks("organizations/123456789")

# List frameworks for a project with custom page size
await list_frameworks("projects/my-project-id", page_size=25)
``` 

### List Constraints
```python
# List constraints for an organization
await list_constraints("organizations/123456789")

# List constraints for a project
await list_constraints("projects/my-project-id")
``` 

### List Active Org Policies
```python
# List constraints for an organization
await list_active_policies("organizations/123456789")

# List constraints for a project
await list_active_policies("projects/my-project-id")
``` 