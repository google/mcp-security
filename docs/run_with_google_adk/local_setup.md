# Detailed Local Setup Guide

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
