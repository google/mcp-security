# Prebuilt ADK Agent Usage Guide

This guide provides instructions on how to run and deploy the prebuilt ADK (Agent Development Kit) agent. It includes two main deployment paths: a simple deployment to **Cloud Run** and a more advanced deployment to **AgentSpace** via Agent Engine for full integration.

## Table of Contents

1.  [Quick Start: Deploy to Cloud Run](#1-quick-start-deploy-to-cloud-run)
2.  [Quick Start: Deploy to AgentSpace (via Agent Engine)](#2-quick-start-deploy-to-agentspace-via-agent-engine)
3.  [Detailed Local Setup Guide](#3-detailed-local-setup-guide)
4.  [Makefile Commands Reference](#4-makefile-commands-reference)
5.  [Advanced Topics](#5-advanced-topics)
    - [Improving Performance and Optimizing Costs](#improving-performance-and-optimizing-costs)
    - [Integrating Custom MCP Servers](#integrating-custom-mcp-servers)
    - [Additional Features](#additional-features)

---

## 1. Quick Start: Deploy to Cloud Run

This path is recommended for users who want a simple, standalone deployment of the agent as a web service.

### Prerequisites

-   Ensure you have `gcloud` CLI installed and configured.
-   Enable the required APIs for Cloud Run deployment. See [Cloud Run Source Deployment Docs](https://cloud.google.com/run/docs/deploying-source-code#before_you_begin).
-   Set the `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` variables in your `.env` file (`run-with-google-adk/agents/google_mcp_security_agent/.env`).

### Deployment Steps

1.  **Deploy the Service:**
    From the `run-with-google-adk` directory, run the following command:
    ```bash
    make cloudrun-deploy
    ```
    This command packages the agent and deploys it as a service on Cloud Run.

2.  **Test the Service:**
    Once deployed, you can test your service using:
    ```bash
    make cloudrun-test
    ```
    This will provide the service URL and send a test request.

> ⚠️ **Security Warning:**
> By default, the Cloud Run service is deployed with unauthenticated invocations enabled for initial testing. It is critical to **secure your service** by enabling IAM authentication. Follow the guide [here](https://cloud.google.com/run/docs/authenticating/developers).

---

## 2. Quick Start: Deploy to AgentSpace (via Agent Engine)

This path is for users who want to integrate the agent with the full AgentSpace ecosystem, enabling more advanced features and interactions.

### Prerequisites

-   Complete the prerequisites from the [Cloud Run Quick Start](#1-quick-start-deploy-to-cloud-run).
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
    ```

---

## 3. Detailed Local Setup Guide

For development purposes, you can run the agent entirely on your local machine.

### Prerequisites
- `python` v3.11+
- `pip`
- `gcloud` CLI

### Setup and Run

```bash
# Clone the repo
git clone https://github.com/google/mcp-security.git

# Navigate to the agent directory
cd mcp-security/run-with-google-adk

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file from the template
cp agents/google_mcp_security_agent/.env.template agents/google_mcp_security_agent/.env

# Edit agents/google_mcp_security_agent/.env with your credentials and settings
# (e.g., GOOGLE_API_KEY, CHRONICLE_PROJECT_ID, etc.)

# Authenticate for Google Cloud APIs
gcloud auth application-default login

# Run the agent with the ADK Web UI
./scripts/run-adk-agent.sh adk_web
```
You can now access the agent's web interface at `http://localhost:8000`.

---

## 4. Makefile Commands Reference

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

---

## 5. Advanced Topics

### Improving Performance and Optimizing Costs
You can control the number of previous interactions sent to the LLM by setting the `MAX_PREV_USER_INTERACTIONS` variable in your `.env` file. A lower number (default is 3) reduces context size, which can improve performance and lower costs.

### Integrating Custom MCP Servers
This agent can be extended to include your own MCP servers. For a detailed guide and examples, please refer to the `docs/development_guide.md` file.

### Additional Features
The agent supports creating files and generating signed URLs for them via the artifact service. For example, you can ask the agent to "add the summary as markdown to summary_146.md" and then "create a link to file summary_146.md".
