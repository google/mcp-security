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

import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, TextIO

# Add current directory to Python path for local libs
current_dir = Path(__file__).parent
if (current_dir / "libs").exists():
    sys.path.insert(0, str(current_dir))

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    StdioConnectionParams,
    StdioServerParameters,
)

from libs.adk_utils.callbacks import bac_setup_state_variable, bmc_trim_llm_request
from libs.adk_utils.extensions import MCPToolSetWithSchemaAccess
from libs.adk_utils.tools import get_file_link, list_files, store_file

# Configure logging
logging.basicConfig(level=logging.INFO)
if os.environ.get("MINIMAL_LOGGING", "false").lower() == "true":
    logging.getLogger().setLevel(logging.ERROR)

# Define base directory and server directory
# In Cloud Run, the structure is different - server is at /app/server
if os.path.exists("/app/server"):
    # Running in Cloud Run container
    BASE_DIR = Path("/app")
    SERVER_DIR = BASE_DIR / "server"
else:
    # Running locally
    BASE_DIR = Path(__file__).resolve().parents[2]  # Root of run-with-google-adk
    SERVER_DIR = BASE_DIR.parent / "server"  # Server is in parent directory


def _create_mcp_toolset(
    server_name: str,
    tool_set_name: str,
    env_file_path: Path,
    timeout: float,
    errlog: Optional[TextIO],
    extra_args: Optional[List[str]] = None,
) -> Optional[MCPToolSetWithSchemaAccess]:
    """Helper function to create and configure an MCPToolSet."""
    # Map server names to environment variable names
    env_var_mapping = {
        "scc": "LOAD_SCC_MCP",
        "secops/secops_mcp": "LOAD_SECOPS_MCP", 
        "gti/gti_mcp": "LOAD_GTI_MCP",
        "secops-soar/secops_soar_mcp": "LOAD_SECOPS_SOAR_MCP"
    }
    
    load_var = env_var_mapping.get(server_name, f"LOAD_{server_name.upper().replace('/', '_').replace('-', '_')}_MCP")
    load_value = os.environ.get(load_var, "false")
    logging.info(f"Checking {load_var}: {load_value}")
    
    if load_value.lower() != "true":
        logging.info(f"Skipping {server_name} - not enabled")
        return None

    server_path = SERVER_DIR / server_name
    logging.info(f"Looking for server at: {server_path}")
    if not server_path.exists():
        logging.error(f"Server directory not found: {server_path}")
        logging.error(f"SERVER_DIR is: {SERVER_DIR}")
        logging.error(f"Contents of parent: {list(SERVER_DIR.parent.iterdir()) if SERVER_DIR.parent.exists() else 'parent does not exist'}")
        return None

    args = ["--directory", str(server_path), "run"]
    if env_file_path.exists():
        args.extend(["--env-file", str(env_file_path)])
    
    # Different servers have different entry points
    if server_name == "scc":
        args.append("scc_mcp.py")
    else:
        args.append("server.py")
    if extra_args:
        args.extend(extra_args)

    return MCPToolSetWithSchemaAccess(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(command="uv", args=args),
            timeout=timeout,
        ),
        tool_set_name=tool_set_name,
        errlog=errlog,
    )


def get_all_tools() -> List[MCPToolSetWithSchemaAccess]:
    """Get Tools from All MCP servers."""
    logging.info("Attempting to connect to MCP servers...")
    timeout = float(os.environ.get("STDIO_PARAM_TIMEOUT", "60.0"))
    
    # Try different paths for the .env file
    possible_env_paths = [
        BASE_DIR / "agents" / "google_mcp_security_agent" / ".env",
        Path("/tmp/.env"),  # Cloud Run creates env file here
        Path(".env"),
    ]
    
    env_file_path = None
    for path in possible_env_paths:
        if path.exists():
            env_file_path = path
            logging.info(f"Using env file at: {env_file_path}")
            break
    
    if not env_file_path:
        logging.warning("No .env file found, using environment variables only")
        env_file_path = Path("/tmp/.env")  # Use a dummy path

    # Required temporarily for https://github.com/google/adk-python/issues/1024
    errlog_ae: Optional[TextIO] = sys.stderr
    if os.environ.get("AE_RUN", "false").lower() == "true":
        errlog_ae = None

    toolsets = [
        _create_mcp_toolset(
            "scc", "scc", env_file_path, timeout, errlog_ae
        ),
        _create_mcp_toolset(
            "secops/secops_mcp", "secops_mcp", env_file_path, timeout, errlog_ae
        ),
        _create_mcp_toolset(
            "gti/gti_mcp", "gti_mcp", env_file_path, timeout, errlog_ae
        ),
        _create_mcp_toolset(
            "secops-soar/secops_soar_mcp",
            "secops_soar_mcp",
            env_file_path,
            timeout,
            errlog_ae,
            extra_args=[
                "--integrations",
                os.environ.get("SECOPS_INTEGRATIONS", "CSV,OKTA"),
            ],
        ),
    ]

    valid_toolsets = [ts for ts in toolsets if ts is not None]
    logging.info(f"MCP Toolsets created successfully. Found {len(valid_toolsets)} valid toolsets.")
    return valid_toolsets


def create_agent() -> LlmAgent:
    """Create and configure the LlmAgent."""
    tools = get_all_tools()
    logging.info(f"Got {len(tools)} MCP toolsets from get_all_tools()")
    tools.extend([store_file, get_file_link, list_files])
    logging.info(f"Total tools after adding file tools: {len(tools)}")

    # Get model and instruction with defaults
    model = os.environ.get("GOOGLE_MODEL", "gemini-2.5-flash")
    instruction = os.environ.get(
        "DEFAULT_PROMPT",
        "Help user investigate security issues using Google Secops SIEM, SOAR, Security Command Center(SCC) and Google Threat Intel Tools."
    )
    
    return LlmAgent(
        model=model,
        name="google_mcp_security_agent",
        instruction=instruction,
        tools=tools,
        before_model_callback=bmc_trim_llm_request,
        before_agent_callback=bac_setup_state_variable,
        description="You are the google_mcp_security_agent.",
    )


def main() -> None:
    """Main execution function."""
    logging.info("Agent created successfully.")


if __name__ == "__main__":
    main()

root_agent = create_agent()
