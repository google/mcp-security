#!/usr/bin/env python3
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
GTI MCP Tool Docstring Optimization using the official GEPA library
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
    logger.error("Failed to import GEPA or required dependencies. Please check environment: %s", e)
    sys.exit(1)


def load_dataset(dataset_path: Path) -> list:
    """Loads the evaluation dataset."""
    with open(dataset_path, "r") as f:
        return json.load(f)


def gti_metric_fn(data_inst, output: str) -> float:
    """
    Evaluation Metric: Scores 1.0 if model correctly chooses the expected tool
    and specifies all target parameters correctly.
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
        if isinstance(v, str) and isinstance(arguments[k], str):
            if v.lower() not in arguments[k].lower():
                return 0.0
        elif arguments[k] != v:
            return 0.0

    return 1.0


def main():
    # Verify VT_APIKEY environment variable is present
    vt_apikey = os.environ.get("VT_APIKEY")
    if not vt_apikey:
        logger.error("Error: VT_APIKEY environment variable is required for running the local MCP server.")
        sys.exit(1)

    opt_dir = Path(__file__).parent
    server_dir = opt_dir.parent
    server_py = server_dir / "gti_mcp" / "server.py"
    dataset_json = opt_dir / "mcp_dataset.json"

    if not server_py.exists():
        logger.error("MCP Server script not found at %s", server_py)
        sys.exit(1)

    dataset = load_dataset(dataset_json)
    logger.info("Loaded dataset with %d items", len(dataset))

    # Evolve descriptions for these target tools
    raw_tool_names = [
        "search_threats",
        "search_campaigns",
        "search_threat_actors",
        "search_malware_families",
        "search_software_toolkits",
        "search_threat_reports",
        "search_vulnerabilities",
        "get_entities_related_to_a_domain",
        "get_entities_related_to_an_url",
        "get_entities_related_to_an_ip_address",
        "get_entities_related_to_a_file",
        "get_domain_report",
        "get_ip_address_report",
        "get_url_report",
        "get_file_report",
        "get_file_behavior_summary",
        "get_file_behavior_report",
        "search_iocs"
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
        metric_fn=gti_metric_fn,
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[str(server_py)],
        ),
        base_system_prompt=(
            "You are a security analyst with access to the Google Threat Intelligence suite. "
            "Your goal is to determine which tool to call and what parameters to pass based on user query."
        ),
        enable_two_pass=False,  # Optimize JSON first pass selection logic
        failure_score=0.0,
    )

    # Seed candidates with original tool descriptions
    seed_candidate = {
        "tool_description_search_threats": (
            "Search threats in the Google Threat Intelligence platform. "
            "Threats are modeled as collections. Once you get collections from this tool, "
            "you can use get_collection_report to fetch the full reports and their relationships."
        ),
        "tool_description_search_campaigns": (
            "Search threat campaigns in the Google Threat Intelligence platform. "
            "Campaigns are modeled as collections."
        ),
        "tool_description_search_threat_actors": (
            "Search threat actors in the Google Threat Intelligence platform. "
            "Threat actors are modeled as collections."
        ),
        "tool_description_search_malware_families": (
            "Search malware families in the Google Threat Intelligence platform. "
            "Malware families are modeled as collections."
        ),
        "tool_description_search_software_toolkits": (
            "Search software toolkits (or just tools) in the Google Threat Intelligence platform. "
            "Software toolkits are modeled as collections."
        ),
        "tool_description_search_threat_reports": (
            "Search threat reports in the Google Threat Intelligence platform. "
            "Threat reports are modeled as collections."
        ),
        "tool_description_search_vulnerabilities": (
            "Search vulnerabilities (CVEs) in the Google Threat Intelligence platform. "
            "Vulnerabilities are modeled as collections."
        ),
        "tool_description_get_entities_related_to_a_domain": (
            "Retrieve entities related to the given domain. Available relationships: "
            "associations, caa_records, campaigns, cname_records, collections, comments, "
            "communicating_files, downloaded_files, graphs, historical_ssl_certificates, "
            "historical_whois, immediate_parent, malware_families, memory_pattern_parents, "
            "mx_records, ns_records, parent, referrer_files, related_comments, related_reports, "
            "related_threat_actors, reports, resolutions, siblings, soa_records, "
            "software_toolkits, subdomains, urls, user_votes, votes, vulnerabilities."
        ),
        "tool_description_get_entities_related_to_an_url": (
            "Retrieve entities related to the given URL. Available relationships: "
            "analyses, associations, campaigns, collections, comments, communicating_files, "
            "contacted_domains, contacted_ips, downloaded_files, embedded_js_files, last_serving_ip_address, "
            "malware_families, parent_resource_urls, redirects_to, referrer_files, referrer_urls."
        ),
        "tool_description_get_entities_related_to_an_ip_address": (
            "Retrieve entities related to the given IP address. Available relationships: "
            "associations, campaigns, collections, comments, communicating_files, downloaded_files, "
            "graphs, historical_ssl_certificates, historical_whois, malware_families, memory_pattern_parents, "
            "referrer_files, related_comments, related_reports, related_threat_actors, reports, "
            "resolutions, software_toolkits, urls, user_votes, votes, vulnerabilities."
        ),
        "tool_description_get_entities_related_to_a_file": (
            "Retrieve entities related to the given file hash. Available relationships: "
            "analyses, behaviors, carbonblack_children, carbonblack_parents, compressed_parents, "
            "contacted_domains, contacted_ips, contacted_urls, dropped_files, execution_parents, "
            "itw_domains, itw_urls, metadata, memory_pattern_domains, memory_pattern_ips, mutexes_created, "
            "mutexes_opened, overlay_children, overlay_parents, pcap_parents, pe_resource_children, "
            "pe_resource_parents, popular_threat_category, suggested_threat_label, yara_rules."
        ),
        "tool_description_get_domain_report": (
            "Get a comprehensive domain analysis report from Google Threat Intelligence. "
            "Provides attributes, threat classification, and historical metadata for a domain."
        ),
        "tool_description_get_ip_address_report": (
            "Get a comprehensive IP Address analysis report from Google Threat Intelligence. "
            "Provides geolocation, autonomous system details, and threat reputation data."
        ),
        "tool_description_get_url_report": (
            "Get a comprehensive URL analysis report from Google Threat Intelligence. "
            "Provides security analysis, categorizations, and threat category classifications."
        ),
        "tool_description_get_file_report": (
            "Get a comprehensive file analysis report using its hash (MD5/SHA-1/SHA-256). "
            "Provides detection stats, threat classifications, and static metadata."
        ),
        "tool_description_get_file_behavior_summary": (
            "Retrieve a summary of all sandbox execution reports and dynamic analysis details for a file."
        ),
        "tool_description_get_file_behavior_report": (
            "Retrieve a full, detailed sandbox behavior report using a behavior ID formatted as {hash}_{sandbox}."
        ),
        "tool_description_search_iocs": (
            "Search Indicators of Compromise (IOC) in the Google Threat Intelligence platform using VirusTotal query search modifiers."
        )
    }

    logger.info("Starting GEPA optimization loop...")
    result = gepa.optimize(
        seed_candidate=seed_candidate,
        trainset=dataset,
        valset=dataset,
        adapter=adapter,
        reflection_lm=reflection_model,
        max_metric_calls=60,  # iteration and exploration limit bounds
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
