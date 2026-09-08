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
"""Demo Identity Provider (IDP) sub-agent integration example for ADK v2."""

import os
import logging
from pathlib import Path
from typing import Optional, Any
from mcp_security_agent.callbacks import bmc_trim_llm_request

logger = logging.getLogger(__name__)


def create_demo_idp_agent(
    model: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> Any:
    """Initializes and returns the demo IDP sub-agent.

    Args:
        model: Model name (defaults to GOOGLE_MODEL env var or gemini-2.5-flash).
        client_id: IDP client ID (defaults to IDP_CLIENT_ID env var).
        client_secret: IDP client secret (defaults to IDP_CLIENT_SECRET env var).

    Returns:
        Configured LlmAgent instance or None if dependencies are missing.
    """
    model_name = model or os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
    cid = client_id or os.getenv("IDP_CLIENT_ID", "demo-client-id")
    csec = client_secret or os.getenv("IDP_CLIENT_SECRET", "demo-client-secret")

    try:
        from google.adk.agents.llm_agent import LlmAgent
        from google.adk.tools.mcp_tool.mcp_toolset import (
            McpToolset,
            StdioConnectionParams,
            StdioServerParameters,
        )
    except ImportError:
        logger.warning("google.adk not available; skipping demo IDP agent creation.")
        return None

    # Resolve path to sample IDP MCP server
    sample_dir = Path(__file__).resolve().parents[1]
    idp_server_path = sample_dir / "mcp_servers" / "demo_idp" / "idp_mcp_server.py"

    timeout = float(os.getenv("STDIO_PARAM_TIMEOUT", "60.0"))

    conn = StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[
                str(idp_server_path),
                "--client-id",
                cid,
                "--client-secret",
                csec,
            ],
        ),
        timeout=timeout,
    )
    tools = [McpToolset(connection_params=conn)]

    agent = LlmAgent(
        model=model_name,
        name="demo_idp_agent",
        instruction=(
            "You help users gather identity information from the IDP backend during investigations. "
            "Formulate search queries and analyze user account statuses."
        ),
        tools=tools,
        before_model_callback=bmc_trim_llm_request,
        description="Demo IDP agent for identity lookup and authentication troubleshooting.",
    )
    return agent
