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
"""Unit tests for FastMCP tool annotations in scc-mcp."""

import os
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"

import pytest
from mcp.types import ToolAnnotations

import scc_mcp

MUTATING_ADDITIVE_TOOLS = [
    "set_finding_mute",
]

READ_ONLY_TOOLS = [
    "search_findings",
    "get_finding_details",
    "search_findings_by_compliance",
    "top_vulnerability_findings",
    "get_finding_remediation",
]


def test_tool_catalog_coverage():
    """Verify our test suites cover all 6 tools registered on the server."""
    tools = scc_mcp.mcp._tool_manager.list_tools()
    all_registered_names = {t.name for t in tools}
    tested_names = set(MUTATING_ADDITIVE_TOOLS) | set(READ_ONLY_TOOLS)

    assert all_registered_names == tested_names, (
        f"Mismatch in tested tools vs registered tools. "
        f"Missing from tests: {all_registered_names - tested_names}. "
        f"Extra in tests: {tested_names - all_registered_names}"
    )


def test_all_tools_have_annotations():
    """Verify every registered tool defines explicit ToolAnnotations with readOnlyHint."""
    tools = scc_mcp.mcp._tool_manager.list_tools()
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


@pytest.mark.parametrize("tool_name", MUTATING_ADDITIVE_TOOLS)
def test_mutating_additive_tool_annotations(tool_name: str):
    """Verify additive mutating tools declare readOnlyHint=False and destructiveHint=False."""
    tool = scc_mcp.mcp._tool_manager.get_tool(tool_name)
    assert tool is not None, f"Tool {tool_name} not found"
    assert tool.annotations is not None, f"Tool {tool_name} has no annotations"
    assert tool.annotations.readOnlyHint is False, f"Expected {tool_name} readOnlyHint=False"
    assert tool.annotations.destructiveHint is False, f"Expected {tool_name} destructiveHint=False"


@pytest.mark.parametrize("tool_name", READ_ONLY_TOOLS)
def test_read_only_tool_annotations(tool_name: str):
    """Verify query and search tools declare readOnlyHint=True."""
    tool = scc_mcp.mcp._tool_manager.get_tool(tool_name)
    assert tool is not None, f"Tool {tool_name} not found"
    assert tool.annotations is not None, f"Tool {tool_name} has no annotations"
    assert tool.annotations.readOnlyHint is True, f"Expected {tool_name} readOnlyHint=True"
