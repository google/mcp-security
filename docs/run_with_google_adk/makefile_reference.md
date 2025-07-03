# Makefile Commands Reference

This project uses a `Makefile` to simplify common operations. Run `make help` to see all available commands.

### Environment Management
- `make env-check`: Validate required environment variables.
- `make config-show`: Display the current configuration (masks secrets).
- `make env-update KEY=... VALUE=...`: Update a variable in the `.env` file.

### OAuth Management
- `make oauth-setup`: Run the complete OAuth setup workflow.
- `make oauth-client`: Guide for creating an OAuth client.
- `make oauth-uri`: Generate an OAuth authorization URI.
- `make oauth-link`: Link OAuth credentials to AgentSpace.
- `make oauth-verify`: Verify the OAuth configuration.

### Agent Engine Deployment
- `make adk-deploy`: Deploy the agent to Agent Engine.
- `make test-agent`: Test the deployed agent with a message.
- `make agents-list`: List all deployed Agent Engine instances.
- `make agents-delete INDEX=...`: Delete a specific Agent Engine instance.

### AgentSpace Integration
- `make agentspace-register`: Register the agent with AgentSpace.
- `make agentspace-update`: Update an existing AgentSpace registration.
- `make agentspace-verify`: Verify the AgentSpace integration.
- `make agentspace-url`: Get the AgentSpace UI URL.

### Cloud Run Deployment
- `make cloudrun-deploy`: Deploy the agent to Cloud Run.
- `make cloudrun-test`: Test the deployed Cloud Run service.
- `make cloudrun-logs`: View logs for the Cloud Run service.
- `make cloudrun-url`: Get the URL for the Cloud Run service.
