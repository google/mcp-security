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

"""Unit tests for marketplace module imports (Fixes #293) and setup.py packaging sync (Fixes #294)."""

import importlib
import pathlib
from unittest.mock import MagicMock, patch

from secops_soar_mcp.server import register_tools


def test_marketplace_import_prefers_qualified_package_name():
    """Test that dynamic marketplace tool registration tries secops_soar_mcp.marketplace first."""
    mock_module = MagicMock()
    mock_module.register_tools = MagicMock()

    with (
        patch("secops_soar_mcp.server.get_enabled_integrations_set", return_value={"activedirectory"}),
        patch("importlib.import_module", return_value=mock_module) as mock_import,
    ):
        register_tools("activedirectory")
        mock_import.assert_called_once_with("secops_soar_mcp.marketplace.activedirectory")
        assert mock_module.register_tools.called


def test_marketplace_import_falls_back_to_unqualified_import():
    """Test that marketplace tool registration falls back to unqualified module name."""
    mock_module = MagicMock()
    mock_module.register_tools = MagicMock()

    def import_side_effect(name):
        if name == "secops_soar_mcp.marketplace.activedirectory":
            raise ImportError("No module named secops_soar_mcp")
        if name == "marketplace.activedirectory":
            return mock_module
        raise ImportError(f"Unknown module {name}")

    with (
        patch("secops_soar_mcp.server.get_enabled_integrations_set", return_value={"activedirectory"}),
        patch("importlib.import_module", side_effect=import_side_effect) as mock_import,
    ):
        register_tools("activedirectory")
        assert mock_import.call_count == 2
        mock_import.assert_any_call("secops_soar_mcp.marketplace.activedirectory")
        mock_import.assert_any_call("marketplace.activedirectory")
        assert mock_module.register_tools.called


def test_marketplace_import_preserves_inner_import_error():
    """Test that an internal ImportError inside the marketplace module is preserved and not masked."""
    orig_import = importlib.import_module

    def import_side_effect(name, *args, **kwargs):
        if name == "secops_soar_mcp.marketplace.activedirectory":
            raise ImportError("No module named 'missing_third_party_package'")
        if name == "marketplace.activedirectory":
            raise ImportError("No module named 'marketplace'")
        return orig_import(name, *args, **kwargs)

    with (
        patch("secops_soar_mcp.server.get_enabled_integrations_set", return_value={"activedirectory"}),
        patch("importlib.import_module", side_effect=import_side_effect),
        patch("secops_soar_mcp.server.logger.error") as mock_log_error,
    ):
        register_tools("activedirectory")
        assert mock_log_error.called
        # Verify the logged exception preserves the primary error
        err_msg = str(mock_log_error.call_args[0][2])
        assert "missing_third_party_package" in err_msg


def test_setup_py_declares_python_dotenv():
    """Verify setup.py install_requires includes python-dotenv matching pyproject.toml."""
    setup_file = pathlib.Path(__file__).resolve().parents[2] / "setup.py"
    pyproject_file = pathlib.Path(__file__).resolve().parents[2] / "pyproject.toml"
    assert setup_file.exists(), f"setup.py not found at {setup_file}"
    assert pyproject_file.exists(), f"pyproject.toml not found at {pyproject_file}"

    setup_content = setup_file.read_text()
    pyproject_content = pyproject_file.read_text()

    assert "python-dotenv>=1.0.0" in setup_content, "python-dotenv>=1.0.0 missing from setup.py"
    assert "python-dotenv>=1.0.0" in pyproject_content, "python-dotenv>=1.0.0 missing from pyproject.toml"
