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

# Initialize FastMCP server for the XDR sample
mcp = FastMCP("xdr_sample_server")

# --- XDR Tools ---

@mcp.tool()
def authenticate() -> str:
    """
    Authenticates with the sample XDR server using credentials provided at startup.

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
            "token": f"fictitious-xdr-token-{uuid.uuid4()}"
        }
    }
    return json.dumps(response)

@mcp.tool()
def get_host_information(access_token: str, host_name: str) -> str:
    """
    Retrieves fictitious information for a given host from the XDR system.

    Args:
        access_token: The access token obtained from authentication.
        host_name: The name of the host to query (e.g., 'web-server-iowa').

    Returns:
        A JSON string with fictitious host information.
    """
    # The access_token is ignored in this sample server.
    fictitious_info = {
        "hostname": host_name,
        "ip_address": "10.10.1.123",
        "mac_address": "00:1B:44:11:3A:B7",
        "os": "Ubuntu 22.04.1 LTS",
        "status": "online",
        "first_seen": "2024-08-15T10:00:00Z",
        "last_seen": "2025-06-15T01:21:49Z",
        "agent_version": "7.2.1"
    }
    response = {
        "result": "success",
        "message": "retrieved host information",
        "data": {
            "host_information": fictitious_info
        }
    }
    return json.dumps(response)

@mcp.tool()
def get_alerts_for_host(access_token: str, host_name: str) -> str:
    """
    Retrieves 10 fictitious alerts for a given host.

    Args:
        access_token: The access token obtained from authentication.
        host_name: The name of the host to query (e.g., 'web-server-iowa').

    Returns:
        A JSON string containing a list of 10 fictitious alerts.
    """
    # The access_token is ignored in this sample server.
    fictitious_alerts = [
        f"Suspicious process execution detected on {host_name}: 'powershell.exe -enc ...'",
        f"Malware identified on {host_name}: 'Gen:Variant.Razy.1234'",
        f"Network connection to known malicious IP '123.45.67.89' from {host_name}",
        f"Credential dumping attempt using Mimikatz on {host_name}",
        f"Unusual login activity detected for user 'admin' on {host_name}",
        f"Persistence mechanism established via scheduled task on {host_name}",
        f"Anomalous file modification in system directory on {host_name}",
        f"Lateral movement attempt from {host_name} to 'db-server-iowa'",
        f"High volume of DNS requests for unusual domains from {host_name}",
        f"Policy violation: Unapproved software 'bittorrent.exe' installed on {host_name}"
    ]
    response = {
        "result": "success",
        "message": "retrieved 10 alerts",
        "data": {
            "alerts": fictitious_alerts
        }
    }
    return json.dumps(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample XDR MCP Server")
    parser.add_argument("--client-id", required=True, help="Client ID for authentication")
    parser.add_argument("--client-secret", required=True, help="Client Secret for authentication")
    parser.add_argument("--transport", default="stdio", help="MCP transport mechanism (e.g., stdio, http)")
    args = parser.parse_args()

    # Store parsed arguments in global variables
    CLIENT_ID = args.client_id
    CLIENT_SECRET = args.client_secret

    print(f"Starting XDR Sample MCP Server on transport: {args.transport}")
    print(f"Using Client ID: {CLIENT_ID}")
    mcp.run(transport=args.transport)
