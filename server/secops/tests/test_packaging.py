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

import importlib
from pathlib import Path
import tomllib
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CANONICAL_PYPROJECT = REPO_ROOT / "server" / "secops" / "pyproject.toml"
ALIAS_PYPROJECT = REPO_ROOT / "server" / "secops-alias" / "pyproject.toml"


def test_pyproject_files_exist():
    assert CANONICAL_PYPROJECT.is_file(), f"Missing {CANONICAL_PYPROJECT}"
    assert ALIAS_PYPROJECT.is_file(), f"Missing {ALIAS_PYPROJECT}"


def test_versions_in_sync():
    with open(CANONICAL_PYPROJECT, "rb") as f:
        canonical_data = tomllib.load(f)
    with open(ALIAS_PYPROJECT, "rb") as f:
        alias_data = tomllib.load(f)

    canonical_version = canonical_data["project"]["version"]
    alias_version = alias_data["project"]["version"]

    assert canonical_version == alias_version, (
        f"Version mismatch: google-secops-mcp is {canonical_version} "
        f"but secops-mcp alias is {alias_version}"
    )


def test_alias_depends_on_exact_canonical_version():
    with open(CANONICAL_PYPROJECT, "rb") as f:
        canonical_data = tomllib.load(f)
    with open(ALIAS_PYPROJECT, "rb") as f:
        alias_data = tomllib.load(f)

    canonical_version = canonical_data["project"]["version"]
    alias_deps = alias_data["project"]["dependencies"]

    expected_dep = f"google-secops-mcp=={canonical_version}"
    assert expected_dep in alias_deps, (
        f"Expected alias dependencies to contain '{expected_dep}', "
        f"found: {alias_deps}"
    )


def test_script_entry_points_valid():
    with open(CANONICAL_PYPROJECT, "rb") as f:
        canonical_data = tomllib.load(f)

    scripts = canonical_data["project"].get("scripts", {})
    entry_points = canonical_data["project"].get("entry-points", {}).get("mcp", {})

    # Ensure critical CLI aliases exist
    assert "secops_mcp" in scripts
    assert "secops-mcp" in scripts
    assert "google-secops-mcp" in scripts

    for name, target in {**scripts, **entry_points}.items():
        module_name, func_name = target.split(":")
        module = importlib.import_module(module_name)
        func = getattr(module, func_name, None)
        assert callable(func), f"Entry point {name} -> {target} is not callable"
