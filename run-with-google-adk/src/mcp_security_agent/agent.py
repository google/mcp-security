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
"""ADK v2.x Agent definition and factory for MCP Security Agent."""

import logging
from typing import Optional, Any
from mcp_security_agent.config import AgentSettings
from mcp_security_agent.toolsets import build_mcp_toolsets
from mcp_security_agent.callbacks import bmc_trim_llm_request

logger = logging.getLogger(__name__)

SOC_AGENT_SYSTEM_PROMPT = """You are an expert Autonomous Security Operations Center (SOC) Analyst and Threat Intelligence Assistant.
Your mission is to investigate security alerts, hunt for threats in UDM logs, analyze IoCs with Google Threat Intelligence, triage Cloud Security Command Center (SCC) findings, and execute SOAR remediation playbooks.

Guidelines:
1. Always ground your investigations in factual telemetry retrieved from MCP tools.
2. Formulate clear UDM queries, correlate suspicious IP/domain/hash artifacts, and provide actionable remediation steps.
3. Structure your analysis with clear headings: Executive Summary, Investigation Findings, Artifact Analysis, and Recommended Remediation.
"""


def create_security_agent(settings: Optional[AgentSettings] = None) -> Any:
    """Initializes and returns the configured SOC Security Agent.

    Args:
        settings: Optional AgentSettings instance (defaults to loading from environment).

    Returns:
        Configured LlmAgent instance.
    """
    if settings is None:
        settings = AgentSettings()

    toolsets = build_mcp_toolsets(settings)

    try:
        from google.adk.agents.llm_agent import LlmAgent
    except ImportError:
        logger.warning("google.adk.agents.llm_agent not available; returning dummy agent.")
        return None

    agent = LlmAgent(
        name="SecurityOperationsAgent",
        model=settings.google_model,
        instruction=settings.default_prompt or SOC_AGENT_SYSTEM_PROMPT,
        tools=toolsets,
        before_model_callback=bmc_trim_llm_request,
    )
    return agent


# Expose root_agent for standard ADK CLI discovery (adk run, adk web)
root_agent = create_security_agent()
