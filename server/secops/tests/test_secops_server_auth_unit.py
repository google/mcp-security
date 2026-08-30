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

"""Unit tests for SecOps MCP server client authentication and service account impersonation."""

import os
import sys
from unittest.mock import MagicMock, patch

# Ensure server/secops is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_secops_dir = os.path.dirname(current_dir)
if server_secops_dir not in sys.path:
    sys.path.append(server_secops_dir)

# Mock secops if not installed
if "secops" not in sys.modules:
    mock_secops = MagicMock()
    sys.modules["secops"] = mock_secops
    sys.modules["secops.chronicle"] = MagicMock()
    sys.modules["secops.exceptions"] = MagicMock()

# Mock mcp if not installed
if "mcp.server.fastmcp" not in sys.modules:
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

import secops_mcp.server as secops_server


@patch.dict(os.environ, {}, clear=True)
def test_get_chronicle_client_default_adc():
    """Test get_chronicle_client with default ADC when no environment variables are set."""
    with patch.object(secops_server, "SecOpsClient") as mock_secops_client:
        mock_instance = MagicMock()
        mock_secops_client.return_value = mock_instance

        client = secops_server.get_chronicle_client(
            project_id="test-proj", customer_id="test-cust", region="us"
        )
        assert client is not None

        mock_secops_client.assert_called_once_with()
        mock_instance.chronicle.assert_called_once_with(
            customer_id="test-cust", project_id="test-proj", region="us"
        )


@patch.dict(os.environ, {"SECOPS_SA_PATH": "/path/to/sa.json"}, clear=True)
def test_get_chronicle_client_secops_sa_path():
    """Test get_chronicle_client with SECOPS_SA_PATH set."""
    with patch.object(secops_server, "SecOpsClient") as mock_secops_client:
        mock_instance = MagicMock()
        mock_secops_client.return_value = mock_instance

        client = secops_server.get_chronicle_client(
            project_id="test-proj", customer_id="test-cust", region="us"
        )
        assert client is not None

        mock_secops_client.assert_called_once_with(
            service_account_path="/path/to/sa.json"
        )


@patch.dict(os.environ, {"GOOGLE_APPLICATION_CREDENTIALS": "/path/to/gac.json"}, clear=True)
def test_get_chronicle_client_google_application_credentials_fallback():
    """Test get_chronicle_client falls back to GOOGLE_APPLICATION_CREDENTIALS."""
    with patch.object(secops_server, "SecOpsClient") as mock_secops_client:
        mock_instance = MagicMock()
        mock_secops_client.return_value = mock_instance

        client = secops_server.get_chronicle_client(
            project_id="test-proj", customer_id="test-cust", region="us"
        )
        assert client is not None

        mock_secops_client.assert_called_once_with(
            service_account_path="/path/to/gac.json"
        )


@patch.dict(
    os.environ,
    {"SECOPS_IMPERSONATE_SERVICE_ACCOUNT": "secops-sa@project.iam.gserviceaccount.com"},
    clear=True,
)
def test_get_chronicle_client_secops_impersonate_sa():
    """Test get_chronicle_client with SECOPS_IMPERSONATE_SERVICE_ACCOUNT set."""
    with patch.object(secops_server, "SecOpsClient") as mock_secops_client:
        mock_instance = MagicMock()
        mock_secops_client.return_value = mock_instance

        client = secops_server.get_chronicle_client(
            project_id="test-proj", customer_id="test-cust", region="us"
        )
        assert client is not None

        mock_secops_client.assert_called_once_with(
            impersonate_service_account="secops-sa@project.iam.gserviceaccount.com"
        )


@patch.dict(
    os.environ,
    {"GOOGLE_IMPERSONATE_SERVICE_ACCOUNT": "secops-sa@project.iam.gserviceaccount.com"},
    clear=True,
)
def test_get_chronicle_client_google_impersonate_sa_fallback():
    """Test get_chronicle_client falls back to GOOGLE_IMPERSONATE_SERVICE_ACCOUNT."""
    with patch.object(secops_server, "SecOpsClient") as mock_secops_client:
        mock_instance = MagicMock()
        mock_secops_client.return_value = mock_instance

        client = secops_server.get_chronicle_client(
            project_id="test-proj", customer_id="test-cust", region="us"
        )
        assert client is not None

        mock_secops_client.assert_called_once_with(
            impersonate_service_account="secops-sa@project.iam.gserviceaccount.com"
        )


@patch.dict(
    os.environ,
    {
        "SECOPS_SA_PATH": "/path/to/worker-sa.json",
        "SECOPS_IMPERSONATE_SERVICE_ACCOUNT": "target-sa@project.iam.gserviceaccount.com",
    },
    clear=True,
)
def test_get_chronicle_client_chained_sa_and_impersonation():
    """Test get_chronicle_client with both service_account_path and impersonation (chained auth)."""
    with patch.object(secops_server, "SecOpsClient") as mock_secops_client:
        mock_instance = MagicMock()
        mock_secops_client.return_value = mock_instance

        client = secops_server.get_chronicle_client(
            project_id="test-proj", customer_id="test-cust", region="us"
        )
        assert client is not None

        mock_secops_client.assert_called_once_with(
            service_account_path="/path/to/worker-sa.json",
            impersonate_service_account="target-sa@project.iam.gserviceaccount.com",
        )
