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
"""Unit tests for SecOps SOAR HTTP client, exceptions, and startup error diagnostics."""

import os
import ssl
import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import aiohttp

# Ensure server/secops-soar is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_soar_dir = os.path.dirname(current_dir)
if server_soar_dir not in sys.path:
    sys.path.insert(0, server_soar_dir)

from secops_soar_mcp.exceptions import (
    SoarError,
    SoarConnectionError,
    SoarSSLError,
    SoarAuthError,
    SoarHttpError,
)
from secops_soar_mcp.http_client import HttpClient, is_ssl_cert_verification_error
from secops_soar_mcp import bindings


def test_is_ssl_cert_verification_error():
    """Test SSL verification detection walks exception chains."""
    # Direct SSLCertVerificationError
    direct_ssl = ssl.SSLCertVerificationError("certificate verify failed")
    assert is_ssl_cert_verification_error(direct_ssl) is True

    # Nested exception in cause
    wrapper = aiohttp.ClientConnectorError(
        connection_key=MagicMock(),
        os_error=ssl.SSLCertVerificationError("certificate verify failed: self signed certificate"),
    )
    assert is_ssl_cert_verification_error(wrapper) is True

    # Generic error
    generic = RuntimeError("Some generic error")
    assert is_ssl_cert_verification_error(generic) is False
    assert is_ssl_cert_verification_error(None) is False


@pytest.mark.asyncio
async def test_http_client_raises_soar_ssl_error():
    """Test HttpClient translates SSL verification failures into SoarSSLError."""
    client = HttpClient("https://soar.example.com", "test-key")
    
    mock_session = MagicMock()
    mock_session.get.side_effect = aiohttp.ClientConnectorCertificateError(
        connection_key=MagicMock(),
        certificate_error=ssl.SSLCertVerificationError("certificate verify failed"),
    )
    client._session = mock_session

    with pytest.raises(SoarSSLError) as exc_info:
        await client.get("/api/test")
    
    assert "TLS certificate verification failed" in str(exc_info.value)
    assert "Install Certificates.command" in str(exc_info.value)


@pytest.mark.asyncio
async def test_http_client_raises_soar_auth_error():
    """Test HttpClient translates 401/403 into SoarAuthError."""
    client = HttpClient("https://soar.example.com", "bad-key")
    
    mock_response = MagicMock()
    mock_response.status = 401
    mock_response.raise_for_status = MagicMock(side_effect=aiohttp.ClientResponseError(
        request_info=MagicMock(),
        history=(),
        status=401,
        message="Unauthorized",
    ))
    
    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_response
    mock_session = MagicMock()
    mock_session.get.return_value = mock_context
    client._session = mock_session

    with pytest.raises(SoarAuthError) as exc_info:
        await client.get("/api/test")
    
    assert "authentication failed" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_bindings_valid_scopes_ssl_error_message():
    """Test _get_valid_scopes raises actionable error message on SSL verification failure."""
    client = HttpClient("https://soar.example.com", "test-key")
    bindings.http_client = client

    with patch.object(client, "get", side_effect=SoarSSLError("TLS certificate verification failed")):
        with pytest.raises(RuntimeError) as exc_info:
            await bindings._get_valid_scopes()
        
        msg = str(exc_info.value)
        assert "TLS certificate verification failed" in msg
        assert "Install Certificates.command" in msg
        assert "certifi" in msg


@pytest.mark.asyncio
async def test_bindings_valid_scopes_auth_error_message():
    """Test _get_valid_scopes raises clear credentials message on authentication failure."""
    client = HttpClient("https://soar.example.com", "bad-key")
    bindings.http_client = client

    with patch.object(client, "get", side_effect=SoarAuthError("SOAR authentication failed (401)")):
        with pytest.raises(RuntimeError) as exc_info:
            await bindings._get_valid_scopes()
        
        msg = str(exc_info.value)
        assert "authentication failed" in msg
        assert "SOAR_URL" in msg or "SOAR_APP_KEY" in msg


def test_marketplace_import_path_resolution():
    """Test that dynamic marketplace tool registration uses the full package name."""
    from secops_soar_mcp.server import register_tools
    # Verify module resolution doesn't crash on marketplace submodules
    with patch("secops_soar_mcp.server.get_enabled_integrations_set", return_value={"googlechronicle"}), \
         patch("importlib.import_module") as mock_import:
        register_tools("googlechronicle")
        mock_import.assert_any_call("secops_soar_mcp.marketplace.googlechronicle")
