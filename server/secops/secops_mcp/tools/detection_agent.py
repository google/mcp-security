# Copyright 2025 Google LLC
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
"""Security Operations MCP tools for Detection Engineering and Detection Agent workflows."""

import json
import logging
from typing import Any

from secops.chronicle.utils.request_utils import chronicle_request

from secops_mcp.server import get_chronicle_client, server

# Configure logging
logger = logging.getLogger("secops-mcp")


@server.tool()
async def generate_threat_detection_opportunity(
    threat: str | None = None,
    threat_text: str | None = None,
    threat_description: str | None = None,
    threatDescription: str | None = None,
    log_types: list[str] | None = None,
    logTypes: list[str] | None = None,
    project_id: str | None = None,
    customer_id: str | None = None,
    region: str | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    """Generate a Threat Detection Opportunity (TDO) from raw threat description text.

    Generates a structured Threat Detection Opportunity (TDO) for a given threat,
    which can be a GTI campaign, a threat intelligence report, or an external threat
    scenario described by the user.

    The generated TDO contains MITRE ATT&CK details (tactics, techniques, procedures,
    detection strategies), observed observables/atomics (file hashes, domains, URLs, IPs),
    and a list of relevant log types.

    **Workflow Integration:**
    - This is typically the FIRST tool called for user-supplied threat intelligence
      or detection engineering workflows.
    - The resulting TDO serves as the input to subsequent tools, such as
      `generate_synthetic_events` (to simulate log chains) and `evaluate_rule_coverage`
      (to identify detection gaps and create new YARA-L rules).

    **Security Note:**
    The output TDO is generated from user-supplied input via an LLM. Treat it as untrusted.
    Validate outputs before deploying rules based on it.

    Args:
        threat (Optional[str]): Free-form text describing the threat or campaign.
        threat_text (Optional[str]): Alias for threat parameter.
        threat_description (Optional[str]): Alias for threat parameter.
        threatDescription (Optional[str]): CamelCase alias for threat parameter.
        log_types (Optional[List[str]]): Optional list of relevant log types.
        logTypes (Optional[List[str]]): CamelCase alias for log_types.
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.
        timeout (int): Request timeout in seconds. Defaults to 300s (5 minutes).

    Returns:
        Dict[str, Any]: Dictionary containing `threat_detection_opportunities` or error details.
    """
    try:
        raw_threat = (
            threat or threat_text or threat_description or threatDescription
        )
        if not raw_threat or not raw_threat.strip():
            return {
                "error": "The 'threat' (or 'threat_description') parameter is required and cannot be empty.",
                "threat_detection_opportunities": [],
            }

        payload: dict[str, Any] = {"threat": raw_threat.strip()}
        effective_log_types = log_types or logTypes
        if effective_log_types:
            payload["log_types"] = effective_log_types

        chronicle = get_chronicle_client(project_id, customer_id, region)

        if hasattr(type(chronicle), "generate_threat_detection_opportunity"):
            try:
                return chronicle.generate_threat_detection_opportunity(**payload)
            except TypeError:
                return chronicle.generate_threat_detection_opportunity(
                    threat=raw_threat.strip()
                )

        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path=":generateThreatDetectionOpportunity",
            api_version="v1alpha",
            json=payload,
            timeout=timeout,
            error_message="Failed to generate threat detection opportunity",
        )
    except Exception as e:
        logger.exception("Error generating threat detection opportunity")
        return {"error": str(e), "threat_detection_opportunities": []}


@server.tool()
async def generate_synthetic_events(
    threat_detection_opportunity: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    threatDetectionOpportunity: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    threat_detection_opportunities: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    threatDetectionOpportunities: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    tdo: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    project_id: str | None = None,
    customer_id: str | None = None,
    region: str | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    """Generate synthetic events (both raw logs and UDM) for a given Threat Detection Opportunity (TDO).

    Leverages an LLM to simulate high-fidelity, realistic security log chains and UDM events
    that model the threat scenario described in the TDO.

    **Parameter Requirements:**
    - `threat_detection_opportunity` (or `threat_detection_opportunities`): The Threat Detection Opportunity (TDO)
      object, list of TDO objects, or raw response returned by `generate_threat_detection_opportunity`.
    - Each TDO MUST include a populated `log_types` list (e.g., `["WINEVTLOG", "EDR"]`).

    **Workflow Integration:**
    - Typically called after `generate_threat_detection_opportunity`.
    - The generated synthetic events serve as ground-truth attack data to test detection coverage
      via `evaluate_rule_coverage` or validate new YARA-L rules.

    Args:
        threat_detection_opportunity (Optional[Union[Dict[str, Any], List[Dict[str, Any]], str]]): The TDO object, list of TDOs, or JSON string.
        threatDetectionOpportunity (Optional[Union[Dict[str, Any], List[Dict[str, Any]], str]]): Alias for threat_detection_opportunity.
        threat_detection_opportunities (Optional[Union[Dict[str, Any], List[Dict[str, Any]], str]]): Plural alias.
        threatDetectionOpportunities (Optional[Union[Dict[str, Any], List[Dict[str, Any]], str]]): Plural camelCase alias.
        tdo (Optional[Union[Dict[str, Any], List[Dict[str, Any]], str]]): Short alias.
        project_id (Optional[str]): Google Cloud project ID. Defaults to environment configuration.
        customer_id (Optional[str]): Chronicle customer ID. Defaults to environment configuration.
        region (Optional[str]): Chronicle region (e.g., "us", "europe"). Defaults to environment configuration.
        timeout (int): Request timeout in seconds. Defaults to 300s (5 minutes).

    Returns:
        Dict[str, Any]: Dictionary containing `synthetic_events` (list of raw logs and UDM events) or error details.
    """
    try:
        tdo_input = (
            threat_detection_opportunity
            or threatDetectionOpportunity
            or threat_detection_opportunities
            or threatDetectionOpportunities
            or tdo
        )
        if not tdo_input:
            return {
                "error": "The 'threat_detection_opportunity' (or 'threat_detection_opportunities') parameter is required.",
                "synthetic_events": [],
            }

        if isinstance(tdo_input, str):
            try:
                tdo_input = json.loads(tdo_input)
            except json.JSONDecodeError as err:
                return {
                    "error": f"Failed to parse 'threat_detection_opportunity' JSON string: {err}",
                    "synthetic_events": [],
                }

        # Unwrap if raw wrapper dict was passed (e.g. {"threat_detection_opportunities": [...]})
        if isinstance(tdo_input, dict) and "threat_detection_opportunities" in tdo_input:
            tdo_input = tdo_input["threat_detection_opportunities"]

        # Normalize into list of TDO dictionaries
        tdo_list: list[dict[str, Any]] = []
        if isinstance(tdo_input, list):
            for item in tdo_input:
                if isinstance(item, dict):
                    tdo_list.append(dict(item))
                elif isinstance(item, str):
                    try:
                        parsed = json.loads(item)
                        if isinstance(parsed, dict):
                            tdo_list.append(parsed)
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse TDO JSON string item: %s", item)
        elif isinstance(tdo_input, dict):
            tdo_list.append(dict(tdo_input))
        else:
            return {
                "error": "'threat_detection_opportunity' must be a dictionary, list, or JSON string.",
                "synthetic_events": [],
            }

        if not tdo_list:
            return {
                "error": "No valid threat detection opportunities found in input.",
                "synthetic_events": [],
            }

        def _clean_tdo(tdo_item: dict[str, Any]) -> dict[str, Any] | str:
            raw_log_types = tdo_item.get("log_types") or tdo_item.get("logTypes")
            if not raw_log_types or not isinstance(raw_log_types, list) or len(raw_log_types) == 0:
                return "The TDO MUST include a populated 'log_types' list (e.g., ['WINEVTLOG'])."
            clean_log_types: list[str] = []
            for lt in raw_log_types:
                if isinstance(lt, str):
                    clean_log_types.append(lt)
                elif isinstance(lt, dict):
                    val = lt.get("log_type") or lt.get("logType")
                    if val and isinstance(val, str):
                        clean_log_types.append(val)
            if not clean_log_types:
                return "The TDO MUST include a populated 'log_types' list with valid log type strings."
            tdo_item["log_types"] = clean_log_types
            if "summary" not in tdo_item:
                desc = tdo_item.pop("threat_description", None) or tdo_item.pop("description", None)
                if desc and isinstance(desc, str):
                    tdo_item["summary"] = desc
            return tdo_item

        chronicle = get_chronicle_client(project_id, customer_id, region)

        # Single TDO execution path
        if len(tdo_list) == 1:
            cleaned = _clean_tdo(tdo_list[0])
            if isinstance(cleaned, str):
                return {"error": cleaned, "synthetic_events": []}
            if hasattr(type(chronicle), "generate_synthetic_events"):
                return chronicle.generate_synthetic_events(threat_detection_opportunity=cleaned)
            return chronicle_request(
                chronicle,
                method="POST",
                endpoint_path=":generateSyntheticEvents",
                api_version="v1alpha",
                json={"threat_detection_opportunity": cleaned},
                timeout=timeout,
                error_message="Failed to generate synthetic events",
            )

        # Multi-TDO batching execution path
        aggregated_events: list[Any] = []
        aggregated_tdo_events: list[Any] = []
        for tdo_item in tdo_list:
            cleaned = _clean_tdo(tdo_item)
            if isinstance(cleaned, str):
                continue
            if hasattr(type(chronicle), "generate_synthetic_events"):
                res = chronicle.generate_synthetic_events(threat_detection_opportunity=cleaned)
            else:
                res = chronicle_request(
                    chronicle,
                    method="POST",
                    endpoint_path=":generateSyntheticEvents",
                    api_version="v1alpha",
                    json={"threat_detection_opportunity": cleaned},
                    timeout=timeout,
                    error_message="Failed to generate synthetic events",
                )
            if isinstance(res, dict):
                events = res.get("synthetic_events") or res.get("syntheticEvents") or []
                if isinstance(events, list):
                    aggregated_events.extend(events)
                tdo_events = res.get("threat_detection_opportunity_events") or res.get("threatDetectionOpportunityEvents") or []
                if isinstance(tdo_events, list):
                    aggregated_tdo_events.extend(tdo_events)

        return {
            "synthetic_events": aggregated_events,
            "threat_detection_opportunity_events": aggregated_tdo_events,
        }
    except Exception as e:
        logger.exception("Error generating synthetic events")
        return {"error": str(e), "synthetic_events": []}


@server.tool()
async def evaluate_rule_coverage_long_running(
    threat_detection_opportunity_events: list[dict[str, Any]]
    | dict[str, Any]
    | str
    | None = None,
    threatDetectionOpportunityEvents: list[dict[str, Any]]
    | dict[str, Any]
    | str
    | None = None,
    tdo_events: list[dict[str, Any]] | dict[str, Any] | str | None = None,
    tdoEvents: list[dict[str, Any]] | dict[str, Any] | str | None = None,
    opportunity_events: list[dict[str, Any]] | dict[str, Any] | str | None = None,
    opportunityEvents: list[dict[str, Any]] | dict[str, Any] | str | None = None,
    exclude_composite_coverage: bool = True,
    excludeCompositeCoverage: bool | None = None,
    project_id: str | None = None,
    customer_id: str | None = None,
    region: str | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    """Evaluate rule coverage for a given set of synthetic UDM events via a long-running operation.

    Ingests synthetic UDM events and evaluates whether existing rules trigger on them.
    Returns a Long-Running Operation (LRO) object containing an operation `name`
    (e.g., `projects/.../operations/dea-12345`) and `done: false`.

    **Parameter Requirements:**
    - `threat_detection_opportunity_events`: A list of objects containing
      `threat_detection_opportunity_id` (or `threatDetectionOpportunityId`) and `udms_json` (or `udmsJson`).
    - `exclude_composite_coverage`: Optional boolean (defaults to True) to exclude composite rules
      and reduce evaluation time.

    **Instructions for Polling:**
    - Use the `get_operation` tool, passing the returned `name` parameter to poll for completion.
    - When `done` is true, `result.response` (or `response`) contains `coverage_results` (or `coverageResults`),
      listing all matched rules. If empty, a coverage gap exists.

    Args:
        threat_detection_opportunity_events: List of TDO event mappings or JSON string.
        threatDetectionOpportunityEvents: Alias for threat_detection_opportunity_events.
        tdo_events: Short alias for threat_detection_opportunity_events.
        tdoEvents: CamelCase alias for tdo_events.
        opportunity_events: Alias for threat_detection_opportunity_events.
        opportunityEvents: CamelCase alias for opportunity_events.
        exclude_composite_coverage: Boolean to exclude composite rules. Defaults to True.
        excludeCompositeCoverage: Alias for exclude_composite_coverage.
        project_id: Optional Google Cloud project ID.
        customer_id: Optional Chronicle customer ID.
        region: Optional Chronicle region.
        timeout: Request timeout in seconds. Defaults to 300s.

    Returns:
        Dict representing the Operation object.
    """
    try:
        raw_events = (
            threat_detection_opportunity_events
            or threatDetectionOpportunityEvents
            or tdo_events
            or tdoEvents
            or opportunity_events
            or opportunityEvents
        )
        if not raw_events:
            return {
                "error": "The 'threat_detection_opportunity_events' parameter is required.",
            }

        if isinstance(raw_events, str):
            try:
                raw_events = json.loads(raw_events)
            except json.JSONDecodeError as err:
                return {
                    "error": f"Failed to parse 'threat_detection_opportunity_events' JSON string: {err}"
                }

        # Unwrap if raw wrapper dict was passed
        if isinstance(raw_events, dict):
            if "threat_detection_opportunity_events" in raw_events:
                events_list = raw_events["threat_detection_opportunity_events"]
            elif "threatDetectionOpportunityEvents" in raw_events:
                events_list = raw_events["threatDetectionOpportunityEvents"]
            else:
                events_list = [raw_events]
        elif isinstance(raw_events, list):
            events_list = raw_events
        else:
            return {
                "error": "'threat_detection_opportunity_events' must be a list, dictionary, or JSON string."
            }

        # Normalize entries
        normalized_events: list[dict[str, Any]] = []
        for item in events_list:
            if not isinstance(item, dict):
                continue
            tdo_id = (
                item.get("threat_detection_opportunity_id")
                or item.get("threatDetectionOpportunityId")
                or item.get("id")
            )
            udms = item.get("udms_json") or item.get("udmsJson") or item.get("udm_json")
            if not tdo_id or not udms:
                continue
            if isinstance(udms, str):
                udms = [udms]
            normalized_events.append(
                {
                    "threat_detection_opportunity_id": str(tdo_id),
                    "udms_json": udms,
                }
            )

        if not normalized_events:
            return {
                "error": "No valid threat detection opportunity events found. Each entry must have 'threat_detection_opportunity_id' and 'udms_json'."
            }

        composite_flag = (
            excludeCompositeCoverage
            if excludeCompositeCoverage is not None
            else exclude_composite_coverage
        )

        chronicle = get_chronicle_client(project_id, customer_id, region)

        if hasattr(type(chronicle), "evaluate_rule_coverage_long_running"):
            return chronicle.evaluate_rule_coverage_long_running(
                threat_detection_opportunity_events=normalized_events,
                exclude_composite_coverage=composite_flag,
            )

        return chronicle_request(
            chronicle,
            method="POST",
            endpoint_path=":evaluateRuleCoverageLongRunning",
            api_version="v1alpha",
            json={
                "threat_detection_opportunity_events": normalized_events,
                "exclude_composite_coverage": composite_flag,
            },
            timeout=timeout,
            error_message="Failed to evaluate rule coverage",
        )
    except Exception as e:
        logger.exception("Error in evaluate_rule_coverage_long_running")
        return {"error": str(e)}


@server.tool()
async def get_operation(
    name: str | None = None,
    operation_name: str | None = None,
    operationName: str | None = None,
    project_id: str | None = None,
    customer_id: str | None = None,
    region: str | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    """Get the status and details of a long-running operation in SecOps.

    Retrieves the latest status, progress, and result (if completed) of an asynchronous operation.
    When `done` is true, the response contains the final payload or error details.

    Args:
        name: Full operation resource name (e.g., `projects/.../locations/.../instances/.../operations/...`).
        operation_name: Alias for name parameter.
        operationName: CamelCase alias for name parameter.
        project_id: Optional Google Cloud project ID.
        customer_id: Optional Chronicle customer ID.
        region: Optional Chronicle region.
        timeout: Request timeout in seconds. Defaults to 60s.

    Returns:
        Dict representing the Operation status.
    """
    try:
        raw_name = name or operation_name or operationName
        if not raw_name or not raw_name.strip():
            return {"error": "The 'name' (or 'operation_name') parameter is required."}

        clean_name = raw_name.strip()
        chronicle = get_chronicle_client(project_id, customer_id, region)

        if hasattr(type(chronicle), "get_operation"):
            return chronicle.get_operation(name=clean_name)

        if "/operations/" in clean_name:
            op_path = "operations/" + clean_name.split("/operations/", 1)[1]
        elif clean_name.startswith("operations/"):
            op_path = clean_name
        else:
            op_path = f"operations/{clean_name.lstrip('/')}"

        return chronicle_request(
            chronicle,
            method="GET",
            endpoint_path=op_path,
            api_version="v1alpha",
            timeout=timeout,
            error_message="Failed to get operation status",
        )
    except Exception as e:
        logger.exception("Error in get_operation")
        return {"error": str(e)}


@server.tool()
async def generate_rules(
    threat_detection_opportunity: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    threatDetectionOpportunity: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    threat_detection_opportunities: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    threatDetectionOpportunities: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    tdo: dict[str, Any] | list[dict[str, Any]] | str | None = None,
    background_context: str | None = None,
    backgroundContext: str | None = None,
    project_id: str | None = None,
    customer_id: str | None = None,
    region: str | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    """Generate draft YARA-L 2.0 detection rules for a given Threat Detection Opportunity (TDO).

    Creates draft detection rules and initial metadata (name, description, MITRE ATT&CK mapping)
    from a structured threat description to close detection coverage gaps.

    Args:
        threat_detection_opportunity: The TDO object, list of TDOs, or JSON string from generate_threat_detection_opportunity.
        threatDetectionOpportunity: Alias for threat_detection_opportunity.
        threat_detection_opportunities: Plural alias.
        threatDetectionOpportunities: Plural camelCase alias.
        tdo: Short alias for threat_detection_opportunity.
        background_context: Optional additional organizational or environment context.
        backgroundContext: CamelCase alias for background_context.
        project_id: Optional Google Cloud project ID.
        customer_id: Optional Chronicle customer ID.
        region: Optional Chronicle region.
        timeout: Request timeout in seconds. Defaults to 300s.

    Returns:
        Dict containing `generated_rules` (list of rules with `rule_text` and `feedback_id`) or error details.
    """
    try:
        tdo_input = (
            threat_detection_opportunity
            or threatDetectionOpportunity
            or threat_detection_opportunities
            or threatDetectionOpportunities
            or tdo
        )
        if not tdo_input:
            return {
                "error": "The 'threat_detection_opportunity' (or 'threat_detection_opportunities') parameter is required.",
                "generated_rules": [],
            }

        if isinstance(tdo_input, str):
            try:
                tdo_input = json.loads(tdo_input)
            except json.JSONDecodeError as err:
                return {
                    "error": f"Failed to parse 'threat_detection_opportunity' JSON string: {err}",
                    "generated_rules": [],
                }

        # Unwrap if raw wrapper dict was passed (e.g. {"threat_detection_opportunities": [...]})
        if isinstance(tdo_input, dict) and "threat_detection_opportunities" in tdo_input:
            tdo_input = tdo_input["threat_detection_opportunities"]

        # Normalize into list of TDO dictionaries
        tdo_list: list[dict[str, Any]] = []
        if isinstance(tdo_input, list):
            for item in tdo_input:
                if isinstance(item, dict):
                    tdo_list.append(dict(item))
                elif isinstance(item, str):
                    try:
                        parsed = json.loads(item)
                        if isinstance(parsed, dict):
                            tdo_list.append(parsed)
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse TDO JSON string item: %s", item)
        elif isinstance(tdo_input, dict):
            tdo_list.append(dict(tdo_input))
        else:
            return {
                "error": "'threat_detection_opportunity' must be a dictionary, list, or JSON string.",
                "generated_rules": [],
            }

        if not tdo_list:
            return {
                "error": "No valid threat detection opportunities found in input.",
                "generated_rules": [],
            }

        chronicle = get_chronicle_client(project_id, customer_id, region)
        bg_context = background_context or backgroundContext

        # Single TDO execution path
        if len(tdo_list) == 1:
            target_tdo = tdo_list[0]
            payload: dict[str, Any] = {"threat_detection_opportunity": target_tdo}
            if bg_context:
                payload["background_context"] = bg_context.strip()
            if hasattr(type(chronicle), "generate_rules"):
                try:
                    return chronicle.generate_rules(**payload)
                except TypeError:
                    return chronicle.generate_rules(threat_detection_opportunity=target_tdo)

            return chronicle_request(
                chronicle,
                method="POST",
                endpoint_path=":generateRules",
                api_version="v1alpha",
                json=payload,
                timeout=timeout,
                error_message="Failed to generate rules",
            )

        # Multi-TDO batching execution path
        aggregated_rules: list[Any] = []
        for target_tdo in tdo_list:
            payload = {"threat_detection_opportunity": target_tdo}
            if bg_context:
                payload["background_context"] = bg_context.strip()
            if hasattr(type(chronicle), "generate_rules"):
                try:
                    res = chronicle.generate_rules(**payload)
                except TypeError:
                    res = chronicle.generate_rules(threat_detection_opportunity=target_tdo)
            else:
                res = chronicle_request(
                    chronicle,
                    method="POST",
                    endpoint_path=":generateRules",
                    api_version="v1alpha",
                    json=payload,
                    timeout=timeout,
                    error_message="Failed to generate rules",
                )
            if isinstance(res, dict):
                rules = res.get("generated_rules") or res.get("generatedRules") or []
                if isinstance(rules, list):
                    aggregated_rules.extend(rules)

        return {"generated_rules": aggregated_rules}
    except Exception as e:
        logger.exception("Error generating rules")
        return {"error": str(e), "generated_rules": []}
