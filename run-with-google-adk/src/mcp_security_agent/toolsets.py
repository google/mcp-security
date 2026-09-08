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
"""Multi-transport MCP toolsets builder for Google ADK."""

import logging
from pathlib import Path
from typing import Any, List
from mcp_security_agent.config import AgentSettings

logger = logging.getLogger(__name__)


def build_mcp_toolsets(settings: AgentSettings) -> List[Any]:
    """Builds and returns all configured MCP toolsets using native ADK transports.

    Args:
        settings: Initialized AgentSettings instance.

    Returns:
        List of initialized MCP toolset objects for the ADK agent.
    """
    toolsets = []
    
    # Locate repo server directory relative to this package
    pkg_dir = Path(__file__).resolve().parents[2]  # run-with-google-adk
    repo_root = pkg_dir.parent
    server_dir = repo_root / "server"

    try:
        from google.adk.tools.mcp_tool.mcp_toolset import (
            McpToolset,
            StdioConnectionParams,
            StdioServerParameters,
        )
    except ImportError:
        logger.warning("google.adk.tools.mcp_tool not available; using mock/fallback toolset representation.")
        return toolsets

    # 1. Google SecOps SIEM MCP
    if settings.load_secops_mcp:
        if settings.secops_mcp_url:
            logger.info("Configuring SecOps SIEM MCP via Remote URL: %s", settings.secops_mcp_url)
        else:
            secops_dir = server_dir / "secops"
            logger.info("Configuring SecOps SIEM MCP via Stdio subprocess at %s", secops_dir)
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["--directory", str(secops_dir), "run", "secops_mcp/server.py"],
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    # 2. Security Command Center (SCC) MCP
    if settings.load_scc_mcp:
        if settings.scc_mcp_url:
            logger.info("Configuring SCC MCP via Remote URL: %s", settings.scc_mcp_url)
        else:
            scc_dir = server_dir / "scc"
            logger.info("Configuring SCC MCP via Stdio subprocess at %s", scc_dir)
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["--directory", str(scc_dir), "run", "scc_mcp.py"],
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    # 3. Google Threat Intelligence (GTI) MCP
    if settings.load_gti_mcp:
        if settings.gti_mcp_url:
            logger.info("Configuring GTI MCP via Remote URL: %s", settings.gti_mcp_url)
        else:
            gti_dir = server_dir / "gti"
            logger.info("Configuring GTI MCP via Stdio subprocess at %s", gti_dir)
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["--directory", str(gti_dir), "run", "gti_mcp/server.py"],
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    # 4. SecOps SOAR MCP
    if settings.load_secops_soar_mcp:
        if settings.secops_soar_mcp_url:
            logger.info("Configuring SecOps SOAR MCP via Remote URL: %s", settings.secops_soar_mcp_url)
        else:
            soar_dir = server_dir / "secops-soar"
            logger.info("Configuring SecOps SOAR MCP via Stdio subprocess at %s", soar_dir)
            conn = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["--directory", str(soar_dir), "run", "secops_soar_mcp/server.py"],
                ),
                timeout=settings.stdio_timeout_seconds,
            )
            toolsets.append(McpToolset(connection_params=conn))

    return toolsets
