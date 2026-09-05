# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""GEPA Optimizer script for server/secops MCP tools.

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


def secops_metric_fn(data_inst, output: str) -> float:
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
    server_py = server_dir / "secops_mcp" / "server.py"
    dataset_json = opt_dir / "mcp_dataset.json"

    if not server_py.exists():
        logger.error("MCP Server script not found at %s", server_py)
        sys.exit(1)

    dataset = load_dataset(dataset_json)
    logger.info("Loaded dataset with %d items", len(dataset))

    # The Chronicle SecOps tools we wish to optimize
    raw_tool_names = [
        "search_security_events",
        "get_security_alerts",
        "get_security_alert_by_id",
        "do_update_security_alert",
        "lookup_entity",
        "list_security_rules",
        "search_security_rules",
        "get_ioc_matches",
        "get_threat_intel",
        "search_udm",
        "export_udm_search_csv",
        "find_udm_field_values"
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
        metric_fn=secops_metric_fn,
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[str(server_py)],
        ),
        base_system_prompt=(
            "You are a security analyst with access to the Chronicle SecOps SIEM platform. "
            "Your goal is to determine which security event search, alert management, rule management, "
            "or threat intelligence tool to call and what parameters to pass based on the user's query."
        ),
        enable_two_pass=False,
        failure_score=0.0,
    )

    # Seed candidates with original tool descriptions
    seed_candidate = {
        "tool_description_search_security_events": (
            "Search for security events in Chronicle SIEM using natural language. "
            "Allows searching Chronicle event logs using natural language queries, which are "
            "automatically translated into UDM queries for execution. "
            "Ideal for deep investigation after an initial alert, case, or entity has been prioritized."
        ),
        "tool_description_get_security_alerts": (
            "Get security alerts directly from Chronicle SIEM. "
            "Retrieves a list of recent security alerts generated within Chronicle, based on "
            "detection rules or other alert sources configured in the SIEM."
        ),
        "tool_description_get_security_alert_by_id": (
            "Get security alert by ID directly from Chronicle SIEM. "
            "Gets an alert by ID. "
            "Use this for direct monitoring of SIEM alert activity, potentially identifying "
            "issues before they are ingested or processed by other platforms."
        ),
        "tool_description_do_update_security_alert": (
            "Update security alert attributes directly in Chronicle SIEM. "
            "Modifies specific fields of an existing security alert within Chronicle based on its ID. "
            "This function allows for updates to an alert's status, severity, verdict, assigned scores, comments, and other metadata."
        ),
        "tool_description_lookup_entity": (
            "Look up an entity (IP, domain, hash, user, etc.) in Chronicle SIEM for enrichment. "
            "Provides a comprehensive summary of an entity's activity based on historical log data "
            "within Chronicle over a specified time period. This tool queries Chronicle SIEM directly."
        ),
        "tool_description_list_security_rules": (
            "List security detection rules configured in Chronicle SIEM, with support for pagination. "
            "Retrieves the definitions of detection rules currently active or configured "
            "within the Chronicle SIEM instance."
        ),
        "tool_description_search_security_rules": (
            "Search security detection rules configured in Chronicle SIEM. "
            "Retrieves the definitions of detection rules currently active or configured "
            "within the Chronicle SIEM instance based on a regex pattern."
        ),
        "tool_description_get_ioc_matches": (
            "Get IoC matches directly from Chronicle SIEM. "
            "Retrieves recent IoC matches observed within the SIEM environment."
        ),
        "tool_description_get_threat_intel": (
            "Retrieve threat intelligence from Chronicle SIEM. "
            "Queries threat intelligence data and returns detailed summaries regarding "
            "threat actors, campaigns, CVEs, or general best practices."
        ),
        "tool_description_search_udm": (
            "Search UDM events using UDM query in Chronicle. "
            "Accepts raw YARA-L UDM query strings to locate underlying event records "
            "in the Chronicle database over a specified time range."
        ),
        "tool_description_export_udm_search_csv": (
            "Export UDM search results as a formatted CSV string. "
            "Useful for downloading logs for external reporting or offline triage."
        ),
        "tool_description_find_udm_field_values": (
            "Find UDM field values for autocomplete. "
            "Searches for values matching a query string in specified UDM fields."
        )
    }

    logger.info("Starting GEPA optimization loop...")
    result = gepa.optimize(
        seed_candidate=seed_candidate,
        trainset=dataset,
        valset=dataset,
        adapter=adapter,
        reflection_lm=reflection_model,
        reflection_minibatch_size=len(dataset),
        max_metric_calls=300,
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
