# Copyright 2025 Google LLC
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

"""Unit tests for SSL/certifi error handling in the SOAR MCP server.

These tests verify that SSL certificate errors are caught and reported with
actionable messages instead of the generic 'Failed to fetch valid scopes'
message.

Issue: https://github.com/google/mcp-security/issues/191

To run these tests:
    pytest -xvs server/secops-soar/tests/test_ssl_error_handling.py
"""

import ssl
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest
import pytest_asyncio

from secops_soar_mcp.http_client import (
    HttpClient,
    SoarConnectionError,
    SoarSSLError,
    _is_cert_verify_error,
)
from secops_soar_mcp.utils import consts


# Override the autouse setup_bindings fixture from conftest.py so these
# unit tests can run without real SOAR credentials / config.json.
@pytest_asyncio.fixture(autouse=True)
async def setup_bindings():
    """No-op override — SSL error tests do not need a live SOAR connection."""
    yield


# ---------------------------------------------------------------------------
# Tests for _is_cert_verify_error helper
# ---------------------------------------------------------------------------


class TestIsCertVerifyError:
    """Tests for the _is_cert_verify_error helper function."""

    def test_detects_certificate_verify_failed_string(self):
        error = Exception(
            "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed"
        )
        assert _is_cert_verify_error(error) is True

    def test_detects_lowercase_certificate_verify_failed(self):
        error = Exception("certificate verify failed (_ssl.c:1007)")
        assert _is_cert_verify_error(error) is True

    def test_detects_ssl_cert_verification_error_instance(self):
        """ssl.SSLCertVerificationError is a subclass of ssl.SSLError."""
        try:
            error = ssl.SSLCertVerificationError("test cert error")
        except TypeError:
            # SSLCertVerificationError may require more args on some platforms
            error = ssl.SSLError(1, "CERTIFICATE_VERIFY_FAILED")
        assert _is_cert_verify_error(error) is True

    def test_non_cert_error_returns_false(self):
        error = Exception("Connection refused")
        assert _is_cert_verify_error(error) is False

    def test_empty_error_returns_false(self):
        error = Exception("")
        assert _is_cert_verify_error(error) is False


# ---------------------------------------------------------------------------
# Tests for HttpClient SSL error handling
# ---------------------------------------------------------------------------


class TestHttpClientSSLErrorHandling:
    """Tests for HttpClient._handle_ssl_error method."""

    def setup_method(self):
        self.client = HttpClient(
            base_url="https://test-soar.example.com:443",
            app_key="test-key",
        )

    def test_handle_ssl_error_raises_soar_ssl_error_for_cert_verify(self):
        """ClientConnectorSSLError with CERTIFICATE_VERIFY_FAILED -> SoarSSLError."""
        # Create a realistic SSL cert verify error chain:
        # ssl.SSLCertVerificationError -> OSError -> ClientConnectorSSLError
        ssl_err = ssl.SSLError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed")
        os_error = OSError("CERTIFICATE_VERIFY_FAILED")
        os_error.__cause__ = ssl_err
        connection_key = MagicMock()
        error = aiohttp.ClientConnectorSSLError(connection_key, os_error)
        # Attach the os_error as cause so the chain walker finds it
        error.__cause__ = os_error

        with pytest.raises(SoarSSLError) as exc_info:
            self.client._handle_ssl_error(error)

        # Verify the error message contains actionable fix instructions
        error_msg = str(exc_info.value)
        assert "SSL certificate verification failed" in error_msg
        assert "certifi" in error_msg
        assert "Install" in error_msg or "pip install" in error_msg

    def test_handle_ssl_error_raises_soar_ssl_error_for_generic_ssl(self):
        """ClientConnectorSSLError without cert verify -> SoarSSLError with generic msg."""
        os_error = OSError("SSL handshake failed")
        connection_key = MagicMock()
        error = aiohttp.ClientConnectorSSLError(connection_key, os_error)

        with pytest.raises(SoarSSLError) as exc_info:
            self.client._handle_ssl_error(error)

        error_msg = str(exc_info.value)
        assert "SSL/TLS error" in error_msg

    def test_handle_ssl_error_raises_connection_error(self):
        """ClientConnectorError -> SoarConnectionError."""
        os_error = OSError("Connection refused")
        connection_key = MagicMock()
        error = aiohttp.ClientConnectorError(connection_key, os_error)

        with pytest.raises(SoarConnectionError) as exc_info:
            self.client._handle_ssl_error(error)

        error_msg = str(exc_info.value)
        assert "Failed to connect to SOAR" in error_msg
        assert "test-soar.example.com" in error_msg

    def test_handle_ssl_error_raises_for_raw_ssl_cert_error(self):
        """Raw ssl.SSLError with CERTIFICATE_VERIFY_FAILED -> SoarSSLError."""
        error = ssl.SSLError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed")

        with pytest.raises(SoarSSLError) as exc_info:
            self.client._handle_ssl_error(error)

        error_msg = str(exc_info.value)
        assert "SSL certificate verification failed" in error_msg
        assert "certifi" in error_msg

    def test_handle_ssl_error_does_nothing_for_non_ssl_errors(self):
        """Non-SSL exceptions should pass through without raising."""
        error = ValueError("something else went wrong")
        # Should not raise
        self.client._handle_ssl_error(error)

    def test_handle_ssl_error_does_nothing_for_timeout(self):
        """TimeoutError should pass through without raising."""
        import asyncio

        error = asyncio.TimeoutError()
        # Should not raise
        self.client._handle_ssl_error(error)


# ---------------------------------------------------------------------------
# Tests for HttpClient.get with mocked SSL errors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestHttpClientGetSSLError:
    """Tests that HttpClient.get properly propagates SSL errors."""

    async def test_get_raises_soar_ssl_error_on_cert_verify_failure(self):
        """GET request with SSL cert verify failure raises SoarSSLError."""
        client = HttpClient(
            base_url="https://test-soar.example.com:443",
            app_key="test-key",
        )

        ssl_err = ssl.SSLError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed")
        os_error = OSError("CERTIFICATE_VERIFY_FAILED")
        os_error.__cause__ = ssl_err
        connection_key = MagicMock()
        ssl_error = aiohttp.ClientConnectorSSLError(connection_key, os_error)
        ssl_error.__cause__ = os_error

        mock_session = AsyncMock()
        mock_session.get = MagicMock(side_effect=ssl_error)
        client._session = mock_session

        with pytest.raises(SoarSSLError) as exc_info:
            await client.get("/api/external/v1/settings/GetScopes")

        error_msg = str(exc_info.value)
        assert "SSL certificate verification failed" in error_msg
        assert "certifi" in error_msg

    async def test_get_raises_soar_connection_error_on_connection_failure(self):
        """GET request with connection refused raises SoarConnectionError."""
        client = HttpClient(
            base_url="https://test-soar.example.com:443",
            app_key="test-key",
        )

        os_error = OSError("Connection refused")
        connection_key = MagicMock()
        conn_error = aiohttp.ClientConnectorError(connection_key, os_error)

        mock_session = AsyncMock()
        mock_session.get = MagicMock(side_effect=conn_error)
        client._session = mock_session

        with pytest.raises(SoarConnectionError) as exc_info:
            await client.get("/api/external/v1/settings/GetScopes")

        error_msg = str(exc_info.value)
        assert "Failed to connect to SOAR" in error_msg

    async def test_get_returns_none_for_http_error(self):
        """GET request with HTTP 401 still returns None (existing behavior)."""
        client = HttpClient(
            base_url="https://test-soar.example.com:443",
            app_key="test-key",
        )

        http_error = aiohttp.ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=401,
            message="Unauthorized",
        )

        # Mock the session.get() as an async context manager that raises
        mock_cm = AsyncMock()
        mock_cm.__aenter__ = AsyncMock(side_effect=http_error)
        mock_cm.__aexit__ = AsyncMock(return_value=False)

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_cm)
        client._session = mock_session

        result = await client.get("/api/external/v1/settings/GetScopes")
        assert result is None


# ---------------------------------------------------------------------------
# Tests for HttpClient.post with mocked SSL errors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestHttpClientPostSSLError:
    """Tests that HttpClient.post properly propagates SSL errors."""

    async def test_post_raises_soar_ssl_error_on_cert_verify_failure(self):
        """POST request with SSL cert verify failure raises SoarSSLError."""
        client = HttpClient(
            base_url="https://test-soar.example.com:443",
            app_key="test-key",
        )

        ssl_err = ssl.SSLError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed")
        os_error = OSError("CERTIFICATE_VERIFY_FAILED")
        os_error.__cause__ = ssl_err
        connection_key = MagicMock()
        ssl_error = aiohttp.ClientConnectorSSLError(connection_key, os_error)
        ssl_error.__cause__ = os_error

        mock_session = AsyncMock()
        mock_session.post = MagicMock(side_effect=ssl_error)
        client._session = mock_session

        with pytest.raises(SoarSSLError):
            await client.post("/api/external/v1/cases/ExecuteManualAction")


# ---------------------------------------------------------------------------
# Tests for bindings.bind() with SSL errors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestBindingsSSLError:
    """Tests that bindings.bind() properly propagates SSL errors."""

    async def test_bind_raises_soar_ssl_error(self):
        """bindings.bind() should propagate SoarSSLError from HttpClient.

        We patch the aiohttp session's get() so the SSL error goes through
        HttpClient._handle_ssl_error and gets converted to SoarSSLError.
        """
        from secops_soar_mcp import bindings

        with patch.dict(
            "os.environ",
            {
                "SOAR_URL": "https://test-soar.example.com:443",
                "SOAR_APP_KEY": "test-key",
            },
        ):
            ssl_err = ssl.SSLError(
                1, "[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed"
            )
            os_error = OSError("CERTIFICATE_VERIFY_FAILED")
            os_error.__cause__ = ssl_err
            connection_key = MagicMock()
            ssl_error = aiohttp.ClientConnectorSSLError(connection_key, os_error)
            ssl_error.__cause__ = os_error

            # Patch at the session level so HttpClient.get()'s exception
            # handler (_handle_ssl_error) converts it to SoarSSLError.
            mock_session = MagicMock()
            mock_session.get = MagicMock(side_effect=ssl_error)

            with patch(
                "secops_soar_mcp.http_client.aiohttp.ClientSession",
                return_value=mock_session,
            ):
                with pytest.raises(SoarSSLError) as exc_info:
                    await bindings.bind()

                error_msg = str(exc_info.value)
                assert "SSL certificate verification failed" in error_msg
                assert "certifi" in error_msg

            # Cleanup
            if bindings.http_client:
                # Reset the session so cleanup doesn't fail
                bindings.http_client._session = AsyncMock()

    async def test_bind_raises_runtime_error_for_invalid_credentials(self):
        """bindings.bind() should raise RuntimeError for invalid credentials."""
        from secops_soar_mcp import bindings

        with patch.dict(
            "os.environ",
            {
                "SOAR_URL": "https://test-soar.example.com:443",
                "SOAR_APP_KEY": "bad-key",
            },
        ):
            # Mock the session to return an HTTP 401 (returns None from get())
            mock_response = AsyncMock()
            mock_response.raise_for_status.side_effect = aiohttp.ClientResponseError(
                request_info=MagicMock(), history=(), status=401, message="Unauthorized"
            )
            mock_cm = AsyncMock()
            mock_cm.__aenter__ = AsyncMock(side_effect=aiohttp.ClientResponseError(
                request_info=MagicMock(), history=(), status=401, message="Unauthorized"
            ))
            mock_cm.__aexit__ = AsyncMock(return_value=False)
            mock_session = MagicMock()
            mock_session.get = MagicMock(return_value=mock_cm)

            with patch(
                "secops_soar_mcp.http_client.aiohttp.ClientSession",
                return_value=mock_session,
            ):
                with pytest.raises(RuntimeError) as exc_info:
                    await bindings.bind()

                error_msg = str(exc_info.value)
                assert "Failed to fetch valid scopes from SOAR" in error_msg
                assert "SOAR_APP_KEY" in error_msg

            # Cleanup
            if bindings.http_client:
                bindings.http_client._session = AsyncMock()


# ---------------------------------------------------------------------------
# Tests for error message content quality
# ---------------------------------------------------------------------------


class TestErrorMessageContent:
    """Verify that error messages are actionable and helpful."""

    def test_ssl_certifi_message_contains_fix_instructions(self):
        """The SSL certifi error message should contain actionable fix steps."""
        msg = consts.SSL_CERTIFI_ERROR_MESSAGE
        assert "SSL certificate verification failed" in msg
        assert "certifi" in msg
        assert "pip install" in msg
        assert "google.github.io/mcp-security" in msg

    def test_connection_error_message_contains_checklist(self):
        """The connection error message should contain diagnostic steps."""
        msg = consts.CONNECTION_ERROR_MESSAGE.format(url="https://example.com")
        assert "Failed to connect to SOAR" in msg
        assert "SOAR_URL" in msg
        assert "example.com" in msg

    def test_credentials_error_message_contains_env_vars(self):
        """The credentials error message should mention required env vars."""
        msg = consts.CREDENTIALS_ERROR_MESSAGE
        assert "SOAR_URL" in msg
        assert "SOAR_APP_KEY" in msg
