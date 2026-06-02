# Copyright 2026 Google LLC
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
"""
SecOps SOAR MCP Tool Docstring Optimization using the official GEPA library.
Configured for Vertex AI Model Garden via LiteLLM.
"""

import os
import sys
import json
import logging
from pathlib import Path
import asyncio

# 1. Apply asyncio subprocess reader limit monkey patch
original_create_subprocess_exec = asyncio.create_subprocess_exec
async def patched_create_subprocess_exec(*args, **kwargs):
    kwargs['limit'] = 10 * 1024 * 1024  # 10MB buffer
    return await original_create_subprocess_exec(*args, **kwargs)
asyncio.create_subprocess_exec = patched_create_subprocess_exec

# 2. Load environment variables using dotenv
import dotenv
env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    dotenv.load_dotenv(env_path)

# 3. Configure Google Cloud Vertex AI credentials for LiteLLM
for var in ["GOOGLE_APPLICATION_CREDENTIALS", "VERTEX_PROJECT", "VERTEX_LOCATION"]:
    if not os.getenv(var):
        raise ValueError(
            f"Missing required environment variable: {var}. "
            "Please specify it in your environment or in the .env file."
        )

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# 4. Import GEPA and configure LiteLLM retries
try:
    import gepa
    from gepa.adapters.mcp_adapter import MCPAdapter
    from mcp import StdioServerParameters
    import litellm
    
    # Configure LiteLLM retry and drop parameter behaviors
    litellm.num_retries = 5
    litellm.drop_params = True
except ImportError as e:
    logger.error("Failed to import GEPA or required dependencies: %s", e)
    sys.exit(1)


def load_dataset(dataset_path: Path) -> list:
    """Loads the evaluation dataset."""
    with open(dataset_path, "r") as f:
        return json.load(f)


def soar_metric_fn(data_inst, output: str) -> float:
    """
    Evaluation Metric: Scores 1.0 if the model correctly selects the expected tool
    and extracts all targeted parameters correctly.
    """
    import time
    time.sleep(1.5)  # Safe spacing to avoid hitting Vertex free-tier RPM limits

    try:
        cleaned = output.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        parsed = json.loads(cleaned)
    except Exception:
        return 0.0

    if isinstance(parsed, list):
        if len(parsed) > 0:
            parsed = parsed[0]
        else:
            return 0.0

    if not isinstance(parsed, dict):
        return 0.0

    if parsed.get("action") != "call_tool":
        return 0.0

    selected_tool = parsed.get("tool")
    expected_tool = data_inst.get("reference_answer")
    if selected_tool != expected_tool:
        return 0.0

    arguments = parsed.get("arguments", {})
    expected_args = data_inst.get("tool_arguments", {})

    for k, v in expected_args.items():
        if k not in arguments:
            return 0.0
        
        actual_val = arguments[k]
        if isinstance(v, list) and isinstance(actual_val, list):
            if len(v) != len(actual_val) or sorted(v) != sorted(actual_val):
                return 0.0
        elif isinstance(v, str) and isinstance(actual_val, str):
            if v.lower() not in actual_val.lower():
                return 0.0
        elif actual_val != v:
            return 0.0

    return 1.0


def main():
    opt_dir = Path(__file__).parent
    server_dir = opt_dir.parent
    server_py = server_dir / "secops_soar_mcp" / "server.py"
    dataset_json = opt_dir / "mcp_dataset.json"

    if not server_py.exists():
        logger.error("MCP Server script not found at %s", server_py)
        sys.exit(1)

    dataset = load_dataset(dataset_json)
    logger.info("Loaded dataset with %d items", len(dataset))

    # The SOAR tools we wish to optimize
    raw_tool_names = [
        "list_cases",
        "post_case_comment",
        "list_alerts_by_case",
        "list_alert_group_identifiers_by_case",
        "list_events_by_alert",
        "change_case_priority",
        "get_entities_by_alert_group_identifiers",
        "get_entity_details",
        "search_entity",
        "get_case_full_details"
    ]

    # Target Vertex AI Model Garden models
    task_model = "vertex_ai/gemini-2.5-flash"
    reflection_model = "vertex_ai/gemini-2.5-pro"

    logger.info("Initializing MCPAdapter targeting local stdio server...")
    logger.info("Task Model: %s", task_model)
    logger.info("Reflection Model: %s", reflection_model)

    adapter = MCPAdapter(
        tool_names=raw_tool_names,
        task_model=task_model,
        metric_fn=soar_metric_fn,
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[str(server_py)],
        ),
        base_system_prompt=(
            "You are a security analyst with access to the Chronicle SecOps SOAR platform. "
            "Your goal is to determine which case management or incident response tool to call "
            "and what parameters to pass based on the user's query."
        ),
        enable_two_pass=False,
        failure_score=0.0,
    )

    # Seed candidates with original tool descriptions
    seed_candidate = {
        "tool_description_list_cases": (
            "List cases available in the Security Orchestration, Automation, and Response (SOAR) platform. "
            "In a SOAR context, a 'case' typically represents a security incident, investigation, "
            "or a container for related alerts and response actions. Listing cases provides an "
            "overview of ongoing or past security events being managed by the platform. "
            "This is useful for getting a high-level list of recent security issues or finding "
            "a specific incident to investigate further."
        ),
        "tool_description_post_case_comment": (
            "Post a comment to a specific case within the SOAR platform. "
            "Cases are used to track security incidents and investigations. Adding comments "
            "is essential for documenting findings, communication between analysts, recording "
            "actions taken, or providing updates on the investigation progress."
        ),
        "tool_description_list_alerts_by_case": (
            "List the security alerts associated with a specific case ID in the SOAR platform. "
            "Alerts are notifications generated by security tools (like SIEMs, EDRs) indicating "
            "potential security issues. In SOAR, alerts are often grouped into cases for "
            "investigation and response. Listing alerts for a case helps understand the "
            "scope of the incident, the specific events that triggered it, and the evidence collected."
        ),
        "tool_description_list_alert_group_identifiers_by_case": (
            "List alert group identifiers associated with a specific case ID in the SOAR platform. "
            "In this SOAR implementation, alerts within a case can be grouped using identifiers, "
            "potentially for correlation, playbook execution stages, or analyst assignment. "
            "Retrieving these identifiers helps understand the internal structure of a case "
            "or target specific alert groupings for automation or analysis."
        ),
        "tool_description_list_events_by_alert": (
            "List the underlying security events associated with a specific alert within a given case. "
            "Security alerts (often derived from detection rules or IoC matches) are typically "
            "triggered by one or more underlying events ingested into the security platform "
            "(e.g., Chronicle). These events provide the raw data (likely in UDM format) "
            "needed to validate the alert, understand the specific activity, and perform deep-dive investigations."
        ),
        "tool_description_change_case_priority": (
            "Change the priority level of a specific case in the SOAR platform. "
            "Case priority (e.g., PriorityUnspecified, PriorityInfo, PriorityLow, PriorityMedium, "
            "PriorityHigh, PriorityCritical) helps security teams triage incidents and focus "
            "on the most urgent threats based on the *currently available information*. Remember that priority can change as more context is "
            "gathered during the investigation. The priority might be adjusted during the "
            "investigation lifecycle based on new findings."
        ),
        "tool_description_get_entities_by_alert_group_identifiers": (
            "Retrieve entities (e.g., IP addresses, hostnames, users) involved in specific alert groups within a case. "
            "Understanding which entities are associated with alerts is fundamental for incident "
            "investigation and response. This tool allows fetching entities linked to one or "
            "more alert groups, which can be crucial for identifying affected assets, potential "
            "attack vectors, or compromised accounts. The description also notes it can be used "
            "to get target entities for manual actions, implying these entities might be inputs "
            "for subsequent response playbooks or manual interventions."
        ),
        "tool_description_get_entity_details": (
            "Fetch detailed information about a specific entity known to the SOAR platform. "
            "Entities (like IPs, domains, users, assets) are central to security investigations. "
            "This tool retrieves comprehensive details about a specific entity based on its "
            "identifier, type, and environment. This information might include enrichment data "
            "(e.g., threat intelligence, asset inventory details), related alerts or cases, "
            "observed activity, and risk scores, providing crucial context for analysis."
        ),
        "tool_description_search_entity": (
            "Search for entities within the SOAR platform based on various criteria. "
            "This tool provides a flexible way to find entities (assets, users, IOCs, etc.) "
            "matching specific attributes. It allows searching by term (e.g., part of a hostname), "
            "entity type, suspicion status, asset status (internal/external), enrichment status, "
            "network, or environment. This is useful for exploring the entity database, finding "
            "potentially related entities during an investigation, or identifying assets with "
            "specific characteristics."
        ),
        "tool_description_get_case_full_details": (
            "Retrieve comprehensive details for a specific case by aggregating its core information, associated alerts, and comments. "
            "This tool provides a consolidated view of a security case by fetching its primary details "
            "(like status, priority, description), all linked security alerts, and the full history "
            "of comments added by analysts or automation. This aggregated information is essential "
            "for getting a complete understanding of an incident's context, scope, investigation "
            "progress, and collaborative notes without making multiple separate API calls."
        )
    }

    logger.info("Starting GEPA optimization loop...")
    result = gepa.optimize(
        seed_candidate=seed_candidate,
        trainset=dataset,
        valset=dataset,
        adapter=adapter,
        reflection_lm=reflection_model,
        max_metric_calls=150,
    )

    logger.info("Optimization finished!")
    best_candidate = result.candidates[result.best_idx]
    best_score = result.val_aggregate_scores[result.best_idx]
    logger.info("Best achieved score: %.2f", best_score)

    # Save results
    result_path = opt_dir / "gepa_optimization_results.json"
    with open(result_path, "w") as f:
        json.dump({
            "best_score": best_score,
            "optimized_tool_descriptions": best_candidate
        }, f, indent=2)
    logger.info("Optimized results successfully saved to %s", result_path)


if __name__ == "__main__":
    main()
