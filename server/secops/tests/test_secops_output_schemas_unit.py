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
"""Unit tests pinning wrapped outputSchema on Dict-returning SecOps tools."""

import pytest

mcp_memory = pytest.importorskip("mcp.shared.memory")
client_session = mcp_memory.create_connected_server_and_client_session

from secops_mcp.server import server  # noqa: E402


@pytest.mark.asyncio
async def test_dict_returning_tools_keep_wrapped_output_schema() -> None:
    """Tools returning `typing.Dict` keep the {"result": ...} outputSchema.

    FastMCP builds an unwrapped schema only for built-in `dict[...]` (and
    none at all for bare `dict`), so these 44 return annotations stay
    `typing.Dict` with `# noqa: UP006`. Rewriting them would change
    outputSchema and structuredContent for clients.
    """
    expected = {
        "compute_rule_exclusion_activity",
        "create_feed",
        "create_retrohunt",
        "create_rule_exclusion",
        "create_watchlist",
        "delete_feed",
        "delete_watchlist",
        "disable_feed",
        "enable_feed",
        "fetch_associated_investigations",
        "find_udm_field_values",
        "generate_feed_secret",
        "get_curated_rule",
        "get_curated_rule_by_name",
        "get_curated_rule_set",
        "get_detection_rule",
        "get_feed",
        "get_investigation",
        "get_retrohunt",
        "get_rule_detections",
        "get_rule_exclusion",
        "get_stats",
        "get_watchlist",
        "list_curated_rule_set_deployments",
        "list_curated_rule_sets",
        "list_curated_rules",
        "list_feeds",
        "list_investigations",
        "list_parsers",
        "list_rule_errors",
        "list_rule_exclusions",
        "list_security_rules",
        "list_watchlists",
        "patch_rule_exclusion",
        "search_curated_detections",
        "search_rule_alerts",
        "search_security_events",
        "search_security_rules",
        "search_udm",
        "trigger_investigation",
        "update_curated_rule_set_deployment",
        "update_feed",
        "update_rule_exclusion_deployment",
        "update_watchlist",
    }

    async with client_session(server._mcp_server) as client:
        tools_result = await client.list_tools()

    schemas = {tool.name: tool.outputSchema for tool in tools_result.tools}
    assert expected <= schemas.keys()
    for name in sorted(expected):
        schema = schemas[name]
        assert schema is not None, name
        assert schema["required"] == ["result"], name
        assert schema["properties"]["result"]["type"] == "object", name
