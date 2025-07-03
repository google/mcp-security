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
BASE_DIR = Path(__file__).resolve().parents[2]  # Root of run-with-google-adk
SERVER_DIR = BASE_DIR / "server"


def _create_mcp_toolset(
    server_name: str,
    tool_set_name: str,
    env_file_path: Path,
    timeout: float,
    errlog: Optional[TextIO],
    extra_args: Optional[List[str]] = None,
) -> Optional[MCPToolSetWithSchemaAccess]:
    """Helper function to create and configure an MCPToolSet."""
    if os.environ.get(f"LOAD_{server_name.upper()}_MCP", "false").lower() != "true":
        return None

    server_path = SERVER_DIR / server_name
    if not server_path.exists():
        logging.error(f"Server directory not found: {server_path}")
        return None

    args = ["--directory", str(server_path), "run"]
    if env_file_path.exists():
        args.extend(["--env-file", str(env_file_path)])
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
    env_file_path = BASE_DIR / "agents" / "google_mcp_security_agent" / ".env"

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

    logging.info("MCP Toolsets created successfully.")
    return [ts for ts in toolsets if ts is not None]


def create_agent() -> LlmAgent:
    """Create and configure the LlmAgent."""
    tools = get_all_tools()
    tools.extend([store_file, get_file_link, list_files])

    return LlmAgent(
        model=os.environ.get("GOOGLE_MODEL"),
        name="google_mcp_security_agent",
        instruction=os.environ.get("DEFAULT_PROMPT"),
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
