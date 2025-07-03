# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import uuid
import sys
from typing import Optional

# To run this, you need the MCP SDK installed.
# If not available, we'll use a placeholder class for demonstration.
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Warning: 'mcp.server.fastmcp' not found. Using a placeholder class.", file=sys.stderr)
    class FastMCP:
        def __init__(self, name):
            self._name = name
            self._tools = {}
        def tool(self):
            def decorator(f):
                self._tools[f.__name__] = f
                return f
            return decorator
        def run(self, transport=None):
            print(f"Running mock MCP server '{self._name}' with transport '{transport}'")
            print("This is a placeholder and will not actually listen for requests.")

# --- Configuration Variables (populated by argparse) ---
CLIENT_ID: Optional[str] = None
CLIENT_SECRET: Optional[str] = None

# Initialize FastMCP server for the IDP sample
mcp = FastMCP("idp_sample_server")

# --- IDP Tools ---

@mcp.tool()
def authenticate() -> str:
    """
    Authenticates with the sample IDP server using credentials provided at startup.

    Returns:
        A JSON string with the authentication result.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        response = {
            "result": "failure",
            "message": "authentication failed: server is not configured with client_id and client_secret.",
            "data": {}
        }
        return json.dumps(response)

    # The startup arguments are validated, now we return a mock success response.
    response = {
        "result": "success",
        "message": "authentication successful",
        "data": {
            "token": f"fictitious-idp-token-{uuid.uuid4()}"
        }
    }
    return json.dumps(response)

@mcp.tool()
def get_recent_login(access_token: str, user_name: str) -> str:
    """
    Retrieves 3 fictitious recent logins for a user from the IDP system.

    Args:
        access_token: The access token obtained from authentication.
        user_name: The user to query (e.g., 'oleg').

    Returns:
        A JSON string with fictitious login details.
    """
    # The access_token is ignored in this sample server.
    fictitious_logins = [
        {
            "from_ip": "74.125.224.72",
            "to_ip": "35.227.100.20",
            "to_service": "google_workspace",
            "outcome": "success",
            "timestamp": "2025-06-15T01:15:10Z"
        },
        {
            "from_ip": "104.18.32.221",
            "to_ip": "52.94.236.48",
            "to_service": "office_365",
            "outcome": "success",
            "timestamp": "2025-06-14T22:30:05Z"
        },
        {
            "from_ip": "192.150.187.43", # Fictitious IP from a different region
            "to_ip": "3.235.100.90",
            "to_service": "aws_console",
            "outcome": "failure",
            "timestamp": "2025-06-14T18:05:00Z"
        }
    ]
    response = {
        "result": "success",
        "message": "retrieved 3 previous logins",
        "data": {
            "logins": fictitious_logins
        }
    }
    return json.dumps(response)

@mcp.tool()
def get_user_trust_assessment(access_token: str, user_name: str) -> str:
    """
    Retrieves a fictitious trust assessment score for a given user.

    Args:
        access_token: The access token obtained from authentication.
        user_name: The name of the user to assess (e.g., 'oleg').

    Returns:
        A JSON string containing a fictitious trust assessment.
    """
    # The access_token and user_name are ignored in this sample server.
    response = {
        "result": "success",
        "message": "user trust assessment retrieved",
        "data": {
            "trust_level": "medium_risk",
            "reasons": [
                "Recent failed login from an unrecognized IP address.",
                "Consistent login pattern from primary location."
            ],
            "score": 55 # A score out of 100
        }
    }
    return json.dumps(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample IDP MCP Server")
    parser.add_argument("--client-id", required=True, help="Client ID for authentication")
    parser.add_argument("--client-secret", required=True, help="Client Secret for authentication")
    parser.add_argument("--transport", default="stdio", help="MCP transport mechanism (e.g., http, stdio)")
    args = parser.parse_args()

    # Store parsed arguments in global variables
    CLIENT_ID = args.client_id
    CLIENT_SECRET = args.client_secret

    print(f"Starting IDP Sample MCP Server on transport: {args.transport}")
    print(f"Using Client ID: {CLIENT_ID}")
    mcp.run(transport=args.transport)

