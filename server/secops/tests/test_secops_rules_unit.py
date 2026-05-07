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
"""Unit tests for security rule management tools."""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Ensure server/secops is in path to import secops_mcp
current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

# Mock secops if not installed (for unit testing without dependencies)
try:
    import secops
except ImportError:
    mock_secops = MagicMock()
    sys.modules["secops"] = mock_secops
    sys.modules["secops.chronicle"] = MagicMock()
    sys.modules["secops.exceptions"] = MagicMock()

# Mock mcp if not installed
try:
    import mcp
except ImportError:
    mock_mcp = MagicMock()
    sys.modules["mcp"] = mock_mcp
    sys.modules["mcp.server"] = MagicMock()
    sys.modules["mcp.server.fastmcp"] = MagicMock()

    def tool_decorator(*args, **kwargs):
        def wrapper(func):
            return func
        return wrapper

    mock_fastmcp_instance = MagicMock()
    mock_fastmcp_instance.tool.side_effect = tool_decorator
    sys.modules["mcp.server.fastmcp"].FastMCP.return_value = mock_fastmcp_instance

from secops_mcp.tools.security_rules import create_rule, update_rule


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_RULE_TEXT = """rule suspicious_powershell_download {
    meta:
        description = "Detects PowerShell downloading files"
        author = "Security Team"
        severity = "Medium"
    events:
        $process.metadata.event_type = "PROCESS_LAUNCH"
        $process.principal.process.command_line = /powershell.*downloadfile/i
        $process.principal.hostname != ""
    condition:
        $process
}"""

SAMPLE_RULE_ID = "ru_12345678-1234-1234-1234-123456789012"

VERSIONED_RULE_NAME = (
    "projects/my-project/locations/us/instances/my-customer"
    f"/rules/{SAMPLE_RULE_ID}@v_1234567890_123456789"
)


@pytest.fixture
def mock_chronicle_client():
    client = MagicMock()
    client.update_rule.return_value = {"name": VERSIONED_RULE_NAME}
    client.create_rule.return_value = {
        "name": f"projects/my-project/locations/us/instances/my-customer/rules/{SAMPLE_RULE_ID}"
    }
    return client


@pytest.fixture
def mock_get_client(mock_chronicle_client):
    with patch(
        "secops_mcp.tools.security_rules.get_chronicle_client",
        return_value=mock_chronicle_client,
    ):
        yield mock_chronicle_client


# ---------------------------------------------------------------------------
# update_rule tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_update_rule_success(mock_get_client):
    """update_rule returns a success message containing the rule ID and name."""
    result = await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    assert isinstance(result, str)
    assert SAMPLE_RULE_ID in result
    assert "suspicious_powershell_download" in result
    assert "successfully" in result.lower()


@pytest.mark.asyncio
async def test_update_rule_calls_chronicle_client(mock_get_client):
    """update_rule passes the correct rule_id and rule_text to the Chronicle client."""
    await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    mock_get_client.update_rule.assert_called_once_with(SAMPLE_RULE_ID, SAMPLE_RULE_TEXT)


@pytest.mark.asyncio
async def test_update_rule_passes_connection_params():
    """update_rule forwards project_id, customer_id, and region to get_chronicle_client."""
    mock_client = MagicMock()
    mock_client.update_rule.return_value = {"name": VERSIONED_RULE_NAME}

    with patch(
        "secops_mcp.tools.security_rules.get_chronicle_client",
        return_value=mock_client,
    ) as mock_get_client_fn:
        await update_rule(
            rule_id=SAMPLE_RULE_ID,
            rule_text=SAMPLE_RULE_TEXT,
            project_id="proj-123",
            customer_id="cust-456",
            region="europe",
        )

    mock_get_client_fn.assert_called_once_with("proj-123", "cust-456", "europe")


@pytest.mark.asyncio
async def test_update_rule_includes_version_info(mock_get_client):
    """update_rule surfaces the new version string when the API returns it."""
    result = await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    # The versioned ID (@v_...) should appear in the output.
    assert f"{SAMPLE_RULE_ID}@v_" in result


@pytest.mark.asyncio
async def test_update_rule_no_version_in_response(mock_get_client):
    """update_rule handles a response without a version suffix gracefully."""
    mock_get_client.update_rule.return_value = {
        "name": f"projects/my-project/locations/us/instances/my-customer/rules/{SAMPLE_RULE_ID}"
    }

    result = await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    assert isinstance(result, str)
    assert "successfully" in result.lower()
    # No version line emitted — the output should not contain "@v_".
    assert "@v_" not in result


@pytest.mark.asyncio
async def test_update_rule_extracts_rule_name(mock_get_client):
    """update_rule correctly parses the rule name from the rule text header."""
    rule_text = "rule detect_lateral_movement {\n    condition: true\n}"

    result = await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=rule_text,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    assert "detect_lateral_movement" in result


@pytest.mark.asyncio
async def test_update_rule_api_error(mock_get_client):
    """update_rule returns an error message when the Chronicle API raises an exception."""
    mock_get_client.update_rule.side_effect = Exception("API request failed: 404 Not Found")

    result = await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    assert isinstance(result, str)
    assert "Error" in result
    assert "API request failed" in result


@pytest.mark.asyncio
async def test_update_rule_empty_name_response(mock_get_client):
    """update_rule handles an empty name field in the API response without crashing."""
    mock_get_client.update_rule.return_value = {}

    result = await update_rule(
        rule_id=SAMPLE_RULE_ID,
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    assert isinstance(result, str)
    assert SAMPLE_RULE_ID in result


# ---------------------------------------------------------------------------
# create_rule smoke test (establishes baseline parity with update_rule)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_rule_success(mock_get_client):
    """create_rule returns a success message with the rule ID and name."""
    result = await create_rule(
        rule_text=SAMPLE_RULE_TEXT,
        project_id="my-project",
        customer_id="my-customer",
        region="us",
    )

    assert isinstance(result, str)
    assert SAMPLE_RULE_ID in result
    assert "suspicious_powershell_download" in result
    assert "successfully" in result.lower()
