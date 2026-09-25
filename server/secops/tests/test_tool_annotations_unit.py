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
"""Unit tests for FastMCP tool annotations in secops-mcp."""

import pytest
from mcp.types import ToolAnnotations

import secops_mcp.server as secops_server

DESTRUCTIVE_TOOLS = [
    "delete_data_table_rows",
    "delete_feed",
    "delete_watchlist",
    "disable_feed",
    "generate_feed_secret",
    "deactivate_parser",
]

MUTATING_ADDITIVE_TOOLS = [
    "activate_parser",
    "add_rows_to_data_table",
    "create_data_table",
    "create_feed",
    "create_parser",
    "create_reference_list",
    "create_retrohunt",
    "create_rule",
    "create_rule_exclusion",
    "create_watchlist",
    "do_update_security_alert",
    "enable_feed",
    "ingest_raw_log",
    "ingest_udm_events",
    "patch_rule_exclusion",
    "trigger_investigation",
    "update_curated_rule_set_deployment",
    "update_feed",
    "update_reference_list",
    "update_rule_exclusion_deployment",
    "update_watchlist",
]

READ_ONLY_TOOLS = [
    "compute_rule_exclusion_activity",
    "export_udm_search_csv",
    "fetch_associated_investigations",
    "find_udm_field_values",
    "get_available_log_types",
    "get_curated_rule",
    "get_curated_rule_by_name",
    "get_curated_rule_set",
    "get_detection_rule",
    "get_feed",
    "get_investigation",
    "get_ioc_matches",
    "get_parser",
    "get_reference_list",
    "get_retrohunt",
    "get_rule_detections",
    "get_rule_exclusion",
    "get_security_alert_by_id",
    "get_security_alerts",
    "get_threat_intel",
    "get_watchlist",
    "list_curated_rule_set_deployments",
    "list_curated_rule_sets",
    "list_curated_rules",
    "list_data_table_rows",
    "list_feeds",
    "list_investigations",
    "list_parsers",
    "list_rule_errors",
    "list_rule_exclusions",
    "list_security_rules",
    "list_watchlists",
    "lookup_entity",
    "run_parser_against_sample_logs",
    "search_curated_detections",
    "search_rule_alerts",
    "search_security_events",
    "search_security_rules",
    "search_udm",
    "test_rule",
    "validate_rule",
]


def test_tool_catalog_coverage():
    """Verify our test suites cover all 68 tools registered on the server."""
    tools = secops_server.server._tool_manager.list_tools()
    all_registered_names = {t.name for t in tools}
    tested_names = set(DESTRUCTIVE_TOOLS) | set(MUTATING_ADDITIVE_TOOLS) | set(READ_ONLY_TOOLS)

    assert all_registered_names == tested_names, (
        f"Mismatch in tested tools vs registered tools. "
        f"Missing from tests: {all_registered_names - tested_names}. "
        f"Extra in tests: {tested_names - all_registered_names}"
    )


def test_all_tools_have_annotations():
    """Verify every registered tool defines explicit ToolAnnotations with readOnlyHint."""
    tools = secops_server.server._tool_manager.list_tools()
    assert len(tools) > 0, "No tools registered on server"

    missing_annotations = []
    missing_hints = []

    for tool in tools:
        if tool.annotations is None:
            missing_annotations.append(tool.name)
            continue

        assert isinstance(tool.annotations, ToolAnnotations)
        if tool.annotations.readOnlyHint is None:
            missing_hints.append(f"{tool.name}: readOnlyHint is None")

        if tool.annotations.readOnlyHint is False and tool.annotations.destructiveHint is None:
            missing_hints.append(f"{tool.name}: destructiveHint is None for mutating tool")

    assert not missing_annotations, (
        f"The following {len(missing_annotations)} tools are missing annotations: "
        f"{', '.join(sorted(missing_annotations))}"
    )
    assert not missing_hints, (
        f"The following tools have incomplete hint definitions: "
        f"{', '.join(sorted(missing_hints))}"
    )


@pytest.mark.parametrize("tool_name", DESTRUCTIVE_TOOLS)
def test_destructive_tool_annotations(tool_name: str):
    """Verify destructive tools declare readOnlyHint=False and destructiveHint=True."""
    tool = secops_server.server._tool_manager.get_tool(tool_name)
    assert tool is not None, f"Tool {tool_name} not found"
    assert tool.annotations is not None, f"Tool {tool_name} has no annotations"
    assert tool.annotations.readOnlyHint is False, f"Expected {tool_name} readOnlyHint=False"
    assert tool.annotations.destructiveHint is True, f"Expected {tool_name} destructiveHint=True"


@pytest.mark.parametrize("tool_name", MUTATING_ADDITIVE_TOOLS)
def test_mutating_additive_tool_annotations(tool_name: str):
    """Verify additive mutating tools declare readOnlyHint=False and destructiveHint=False."""
    tool = secops_server.server._tool_manager.get_tool(tool_name)
    assert tool is not None, f"Tool {tool_name} not found"
    assert tool.annotations is not None, f"Tool {tool_name} has no annotations"
    assert tool.annotations.readOnlyHint is False, f"Expected {tool_name} readOnlyHint=False"
    assert tool.annotations.destructiveHint is False, f"Expected {tool_name} destructiveHint=False"


@pytest.mark.parametrize("tool_name", READ_ONLY_TOOLS)
def test_read_only_tool_annotations(tool_name: str):
    """Verify query and search tools declare readOnlyHint=True."""
    tool = secops_server.server._tool_manager.get_tool(tool_name)
    assert tool is not None, f"Tool {tool_name} not found"
    assert tool.annotations is not None, f"Tool {tool_name} has no annotations"
    assert tool.annotations.readOnlyHint is True, f"Expected {tool_name} readOnlyHint=True"
