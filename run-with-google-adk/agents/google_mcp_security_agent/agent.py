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

# Load environment variables from .env file if available
try:
    import dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

# Add appropriate directory to Python path for libs in different environments
current_dir = Path(__file__).parent
possible_libs_paths = [
    current_dir / "libs",  # ADK deployment - libs copied to agent dir
    current_dir.parent / "libs",  # Local development - libs in parent dir
    current_dir.parent.parent / "libs",  # Alternative structure
    Path("/app/libs"),  # Cloud Run
]

libs_path_added = False
for libs_path in possible_libs_paths:
    if libs_path.exists():
        # Add the parent directory of libs to Python path
        sys.path.insert(0, str(libs_path.parent))
        logging.info(f"Added {libs_path.parent} to Python path for libs access")
        libs_path_added = True
        break

if not libs_path_added:
    logging.warning("No libs directory found in any expected location")
    logging.warning(f"Current directory: {current_dir}")
    logging.warning(f"Searched paths: {[str(p) for p in possible_libs_paths]}")

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)

from libs.adk_utils.callbacks import bac_setup_state_variable, bmc_trim_llm_request
from libs.adk_utils.tools import get_file_link, list_files, store_file

# Configure logging
logging.basicConfig(level=logging.INFO)
if os.environ.get("MINIMAL_LOGGING", "false").lower() == "true":
    logging.getLogger().setLevel(logging.ERROR)

# Define base directory and server directory
# Check for different deployment environments in order of priority

# Check if we're in ADK deployment environment (temp directory)
current_file_dir = Path(__file__).parent  # agents/google_mcp_security_agent
agent_server_dir = current_file_dir / "server"  # Look for server in same dir as agent

if agent_server_dir.exists():
    # ADK deployment - server was copied to agent directory
    BASE_DIR = current_file_dir
    SERVER_DIR = agent_server_dir
elif os.path.exists("/app/server"):
    # Running in Cloud Run container
    BASE_DIR = Path("/app")
    SERVER_DIR = BASE_DIR / "server"
elif os.path.exists("./server"):
    # Running locally - server is in current directory
    BASE_DIR = Path(".")
    SERVER_DIR = Path("./server")
else:
    # Running locally - server is in parent directory
    BASE_DIR = Path(__file__).resolve().parents[2]  # Root of run-with-google-adk
    SERVER_DIR = BASE_DIR.parent / "server"  # Server is in parent directory

logging.info(f"🔧 Environment detection:")
logging.info(f"   Current working directory: {Path.cwd()}")
logging.info(f"   BASE_DIR: {BASE_DIR.absolute()}")
logging.info(f"   SERVER_DIR: {SERVER_DIR.absolute()}")
logging.info(f"   SERVER_DIR exists: {SERVER_DIR.exists()}")
if SERVER_DIR.exists():
    logging.info(f"   SERVER_DIR contents: {list(SERVER_DIR.iterdir())}")
else:
    logging.error(f"🚨 SERVER_DIR does not exist! Looking for 'server' directory in current location...")
    current_contents = list(Path.cwd().iterdir())
    logging.error(f"🚨 Current directory contents: {current_contents}")
    # Try to find any directory that might contain server code
    for item in current_contents:
        if item.is_dir() and ("server" in item.name.lower() or any(s in item.name for s in ["scc", "secops", "gti", "soar"])):
            logging.error(f"🚨 Found potential server directory: {item}")
            try:
                logging.error(f"🚨   Contents: {list(item.iterdir())}")
            except Exception:
                pass


def _create_mcp_toolset(
    server_name: str,
    tool_set_name: str,
    env_file_path: Path,
    timeout: float,
    errlog: Optional[TextIO],
    extra_args: Optional[List[str]] = None,
) -> Optional[MCPToolset]:
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

    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(command="uv", args=args),
            timeout=timeout,
        ),
        errlog=errlog,
    )


def get_all_tools() -> List[MCPToolset]:
    """Get Tools from All MCP servers."""
    logging.info("Attempting to connect to MCP servers...")
    timeout = float(os.environ.get("STDIO_PARAM_TIMEOUT", "60.0"))
    
    # Try different paths for the .env file
    possible_env_paths = [
        BASE_DIR / "agents" / "google_mcp_security_agent" / ".env",
        Path("/tmp/.env"),  # Cloud Run creates env file here
        Path(".env"),
        # For ADK deployments - staging directory
        Path("agents/google_mcp_security_agent/.env"),
        # Additional fallback paths
        Path("./google_mcp_security_agent/.env"),
    ]
    
    env_file_path = None
    logging.info("=" * 80)
    logging.info("🔍 SEARCHING FOR .ENV FILE...")
    for i, path in enumerate(possible_env_paths):
        logging.info(f"   {i+1}. Checking: {path.absolute()}")
        if path.exists():
            env_file_path = path
            logging.info(f"✅ Found .env file at: {env_file_path.absolute()}")
            break
        else:
            logging.info(f"❌ Not found: {path.absolute()}")
    
    if not env_file_path:
        logging.error("=" * 80)
        logging.error("🚨 CRITICAL ERROR: No .env file found!")
        logging.error("🚨 This will cause ALL MCP servers to be DISABLED!")
        logging.error("🚨 Searched in:")
        for path in possible_env_paths:
            logging.error(f"🚨   - {path.absolute()}")
        logging.error("🚨 Current working directory: " + str(Path.cwd()))
        logging.error("🚨 Directory contents:")
        try:
            for item in Path.cwd().iterdir():
                logging.error(f"🚨   {item}")
        except Exception as e:
            logging.error(f"🚨   Error listing directory: {e}")
        logging.error("=" * 80)
        logging.warning("No .env file found, using environment variables only")
        env_file_path = Path("/tmp/.env")  # Use a dummy path
    else:
        # Load environment variables from the found .env file
        if HAS_DOTENV:
            try:
                logging.info(f"🔧 Loading environment variables from: {env_file_path}")
                dotenv.load_dotenv(env_file_path, override=False)
                logging.info("✅ Environment variables loaded successfully")
                
                # Log MCP server statuses
                mcp_vars = ["LOAD_SCC_MCP", "LOAD_SECOPS_MCP", "LOAD_GTI_MCP", "LOAD_SECOPS_SOAR_MCP"]
                enabled_count = 0
                for var in mcp_vars:
                    value = os.environ.get(var, "false")
                    status = "✅ ENABLED" if value.lower() == "true" else "❌ DISABLED"
                    logging.info(f"   {var}: {value} ({status})")
                    if value.lower() == "true":
                        enabled_count += 1
                
                if enabled_count == 0:
                    logging.error("🚨 WARNING: NO MCP servers are enabled! Check your .env file.")
                else:
                    logging.info(f"📊 {enabled_count}/{len(mcp_vars)} MCP servers enabled")
                
            except Exception as e:
                logging.error(f"🚨 Error loading .env file: {e}")
                logging.error("🚨 Will use existing environment variables")
        else:
            logging.warning("🚨 python-dotenv not available, cannot load .env file")
            logging.warning("🚨 Install with: pip install python-dotenv")

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
