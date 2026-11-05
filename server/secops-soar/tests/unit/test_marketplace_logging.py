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

"""Marketplace tools must not write diagnostics to stdout.

On the MCP stdio transport stdout is the JSON-RPC channel. Marketplace
modules used to report missing instances and action failures with print(),
which corrupted the stream (issue #332). They now go through logger_utils.
"""

from __future__ import annotations

import logging
from pathlib import Path
from unittest import mock

import pytest

MARKETPLACE_DIR = (
    Path(__file__).resolve().parents[2]
    / "secops_soar_mcp"
    / "marketplace"
)


class _FakeMCP:
    """Captures tools registered by marketplace register_tools()."""

    def __init__(self) -> None:
        self.tools: dict[str, object] = {}

    def tool(self):
        def decorator(fn):
            self.tools[fn.__name__] = fn
            return fn

        return decorator


def test_marketplace_modules_have_no_print_calls() -> None:
    offenders = []
    for path in sorted(MARKETPLACE_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "print(" in text:
            offenders.append(path.name)
    assert offenders == [], (
        "marketplace modules must not call print(); "
        f"found in: {offenders[:10]}"
    )


def _ping_kwargs():
    from secops_soar_mcp.utils.models import TargetEntity

    # Non-empty target_entities bypasses scope validation (valid_scopes is
    # empty until the server binds a real client).
    return {
        "case_id": "1",
        "alert_group_identifiers": ["a"],
        "target_entities": [
            TargetEntity(Identifier="host1", EntityType="Hostname")
        ],
        "scope": "All entities",
    }


@pytest.mark.asyncio
async def test_missing_instance_logs_warning_not_stdout(caplog, capsys) -> None:
    from secops_soar_mcp.marketplace import activedirectory

    mcp = _FakeMCP()
    activedirectory.register_tools(mcp)
    tool = mcp.tools["active_directory_ping"]

    fake_client = mock.AsyncMock()
    fake_client.get.return_value = {"integration_instances": []}

    with (
        mock.patch.object(activedirectory.bindings, "http_client", fake_client),
        caplog.at_level(logging.WARNING, logger=activedirectory.__name__),
    ):
        result = await tool(**_ping_kwargs())

    assert result["Status"] == "Failed"
    assert "No active instance found" in result["Message"]
    assert capsys.readouterr().out == ""
    assert any(
        "No active integration instance found for ActiveDirectory"
        in record.getMessage()
        for record in caplog.records
    )


@pytest.mark.asyncio
async def test_fetch_instance_error_logs_not_stdout(caplog, capsys) -> None:
    from secops_soar_mcp.marketplace import activedirectory

    mcp = _FakeMCP()
    activedirectory.register_tools(mcp)
    tool = mcp.tools["active_directory_ping"]

    fake_client = mock.AsyncMock()
    fake_client.get.side_effect = RuntimeError("boom")

    with (
        mock.patch.object(activedirectory.bindings, "http_client", fake_client),
        caplog.at_level(logging.ERROR, logger=activedirectory.__name__),
    ):
        result = await tool(**_ping_kwargs())

    assert result["Status"] == "Failed"
    assert "Error fetching instance" in result["Message"]
    assert capsys.readouterr().out == ""
    assert any(
        "Error fetching instance for ActiveDirectory" in record.getMessage()
        for record in caplog.records
    )
