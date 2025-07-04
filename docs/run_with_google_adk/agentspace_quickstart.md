# Quick Start: Deploy to AgentSpace (via Agent Engine)

This path is for users who want to integrate the agent with the full AgentSpace ecosystem, enabling more advanced features and interactions.

### Prerequisites

-   Complete the prerequisites from the [Cloud Run Quick Start](cloud_run_quickstart.md).
-   Ensure your `.env` file is correctly configured with your project details.

### Deployment and Registration Steps

1.  **Deploy to Agent Engine:**
    This step provisions the agent in Vertex AI Agent Engine.
    ```bash
    make adk-deploy
    ```
    After deployment, note the `AGENT_ENGINE_RESOURCE_NAME` from the output.

2.  **Update Environment:**
    Add the resource name to your `.env` file.
    ```bash
    make env-update KEY=AGENT_ENGINE_RESOURCE_NAME VALUE=<your-resource-name-from-previous-step>
    ```

3.  **Configure OAuth for AgentSpace:**
    This is a crucial step to allow AgentSpace to securely communicate with your agent.
    ```bash
    make oauth-setup
    ```
    This interactive command will guide you through creating an OAuth client, generating an authorization URL, and linking it to your AgentSpace project. This process generates the required `OAUTH_AUTH_ID`.

4.  **Register with AgentSpace:**
    With OAuth configured, you can now register your agent.
    ```bash
    make agentspace-register
    ```

5.  **Verify and Test:**
    Finally, verify the integration and test the agent's functionality.
    ```bash
    make agentspace-verify
    make test-agent MSG="List available security tools."
