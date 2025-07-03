# Quick Start: Deploy to Cloud Run

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
