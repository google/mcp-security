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
"""--integrations must be able to load every marketplace module.

Four modules have dots in their filenames (e.g. tenable.io.py), which a
dotted import name such as `marketplace.tenable.io` cannot reach.
"""

import logging
import re
import sys
from pathlib import Path

import pytest
from mcp.server.fastmcp import FastMCP

from secops_soar_mcp import server

MARKETPLACE_DIR = Path(server.__file__).resolve().parent / "marketplace"
TOOL_DEF = re.compile(r"@mcp\.tool\(\)\s*\n\s*async def (\w+)")


def _modules() -> list[Path]:
    return sorted(
        path for path in MARKETPLACE_DIR.glob("*.py") if path.name != "__init__.py"
    )


def _tool_names(paths: list[Path]) -> set[str]:
    names = set()
    for path in paths:
        names.update(TOOL_DEF.findall(path.read_text(encoding="utf-8")))
    return names


@pytest.mark.asyncio
async def test_dotted_integrations_register_their_tools(monkeypatch) -> None:
    monkeypatch.setattr(server, "mcp", FastMCP("dotted-integrations"))
    dotted = [path for path in _modules() if "." in path.stem]
    assert {path.stem for path in dotted} == {
        "any.run",
        "stealthwatchv6.10",
        "symantecemailsecurity.cloud",
        "tenable.io",
    }

    server.register_tools(",".join(path.stem for path in dotted))

    registered = {tool.name for tool in await server.mcp.list_tools()}
    assert _tool_names(dotted) <= registered
    assert "tenable_io_ping" in registered


@pytest.mark.asyncio
async def test_every_marketplace_module_loads(monkeypatch, caplog) -> None:
    monkeypatch.setattr(server, "mcp", FastMCP("all-integrations"))
    modules = _modules()

    # A module without register_tools only logs a warning, so check warnings too.
    with caplog.at_level(logging.WARNING, logger=server.logger.name):
        server.register_tools(",".join(path.stem for path in modules))

    problems = [record.getMessage() for record in caplog.records]
    assert problems == [], f"{len(problems)} load problems, e.g. {problems[:3]}"
    registered = {tool.name for tool in await server.mcp.list_tools()}
    missing = _tool_names(modules) - registered
    assert missing == set(), f"{len(missing)} tools not registered"


@pytest.mark.asyncio
async def test_dotted_integration_names_are_case_insensitive(monkeypatch) -> None:
    monkeypatch.setattr(server, "mcp", FastMCP("dotted-case"))

    server.register_tools("Tenable.io, Any.Run")

    registered = {tool.name for tool in await server.mcp.list_tools()}
    assert {"tenable_io_ping", "any_run_ping"} <= registered


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [ImportError, RuntimeError])
async def test_failed_module_is_logged_and_others_still_load(
    monkeypatch, caplog, error
) -> None:
    monkeypatch.setattr(server, "mcp", FastMCP("partial-failure"))
    real_loader = server._load_marketplace_module

    def flaky_loader(module_name, py_file):
        if module_name.endswith(".tenable_io"):
            raise error("simulated import failure")
        return real_loader(module_name, py_file)

    monkeypatch.setattr(server, "_load_marketplace_module", flaky_loader)

    with caplog.at_level(logging.ERROR, logger=server.logger.name):
        server.register_tools("tenable.io,csv")

    registered = {tool.name for tool in await server.mcp.list_tools()}
    assert "csv_ping" in registered
    assert not any(name.startswith("tenable_io_") for name in registered)
    expected = (
        "  * Failed to import module secops_soar_mcp.marketplace.tenable_io. "
        "Error: simulated import failure"
    )
    assert [record.getMessage() for record in caplog.records] == [expected]


@pytest.mark.parametrize("error", ["ImportError", "SyntaxError", "SystemExit"])
def test_load_failure_leaves_no_partial_module(tmp_path, error) -> None:
    broken = tmp_path / "broken.integration.py"
    broken.write_text(f'raise {error}("simulated import failure")\n')
    module_name = "secops_soar_mcp.marketplace.broken_integration"

    with pytest.raises(BaseException, match="simulated import failure") as raised:
        server._load_marketplace_module(module_name, broken)

    assert type(raised.value).__name__ == error
    assert module_name not in sys.modules
    assert not hasattr(sys.modules["secops_soar_mcp.marketplace"], "broken_integration")


def test_loaded_module_is_bound_on_its_package(monkeypatch) -> None:
    """Attribute access such as mock.patch("...marketplace.tenable_io.x") must work."""
    import secops_soar_mcp.marketplace as package

    module_name = "secops_soar_mcp.marketplace.tenable_io"
    monkeypatch.delitem(sys.modules, module_name, raising=False)
    monkeypatch.delattr(package, "tenable_io", raising=False)

    module = server._load_marketplace_module(
        module_name, MARKETPLACE_DIR / "tenable.io.py"
    )

    assert package.tenable_io is module
    assert sys.modules[module_name] is module


def test_already_imported_module_is_reused() -> None:
    from secops_soar_mcp.marketplace import csv

    loaded = server._load_marketplace_module(
        "secops_soar_mcp.marketplace.csv", MARKETPLACE_DIR / "csv.py"
    )

    assert loaded is csv


def test_sanitized_module_names_are_unique() -> None:
    """Replacing dots with underscores must not map two files to one name."""
    stems = [path.stem for path in _modules()]
    sanitized = [stem.replace(".", "_") for stem in stems]
    assert len(set(sanitized)) == len(stems)
