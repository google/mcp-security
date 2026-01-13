import logging
import google.auth
import os
from google.auth.transport.requests import Request
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# 1. Setup scopes
SCOPES = ["https://www.googleapis.com/auth/chronicle"]

def get_access_token():
    creds, _ = google.auth.default(scopes=SCOPES)
    auth_req = Request()
    creds.refresh(auth_req)
    return creds.token

# 2. Configure Toolset
toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=os.getenv("REMOTE_MCP_URL", "https://chronicle.googleapis.com/mcp"),
        headers={
            "Authorization": f"Bearer {get_access_token()}",
            "Accept": "application/json",
            "x-goog-user-project": os.getenv("PROJECT_ID")
        }
    )
)

# 3. Create Agent
root_agent = Agent(
    name="oc_agent",
    model=os.getenv("GOOGLE_MODEL", "gemini-2.5-pro"),
    description="ADK Agent to test the Remote SecOps MCP Server",
    instruction=f"""You are an Agent that tests the remote MCP server's tools.

    When using the SecOps MCP, use these parameters for EVERY request:
    Customer ID: {os.getenv("CUSTOMER_ID")}
    Region: {os.getenv("REGION", "us")}
    Project ID: {os.getenv("PROJECT_ID")}
    """,
    tools=[toolset],
)
