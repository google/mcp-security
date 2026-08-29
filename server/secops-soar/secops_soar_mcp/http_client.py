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
"""HTTP client for making requests to the SecOps SOAR API."""

import json
import ssl
from typing import Any, Dict, Optional

import aiohttp
from logger_utils import get_logger
from secops_soar_mcp.exceptions import (
    SoarAuthError,
    SoarConnectionError,
    SoarError,
    SoarHttpError,
    SoarSSLError,
)

logger = get_logger(__name__)


def is_ssl_cert_verification_error(exc: Optional[BaseException]) -> bool:
    """Checks whether an exception was caused by an SSL certificate verification failure."""
    if exc is None:
        return False
    current = exc
    visited = set()
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        if isinstance(current, (ssl.SSLCertVerificationError, aiohttp.ClientConnectorCertificateError)):
            return True
        msg = str(current).lower()
        if "certificate verify failed" in msg or "certifi" in msg:
            return True
        for related in (current.__cause__, current.__context__):
            if related is not None and is_ssl_cert_verification_error(related):
                return True
        if hasattr(current, "os_error") and current.os_error is not None:
            if is_ssl_cert_verification_error(current.os_error):
                return True
        current = current.__cause__ or current.__context__
    return False


class HttpClient:
    """HTTP client for making requests to the SecOps SOAR API."""

    def __init__(self, base_url: str, app_key: str):
        self.base_url = base_url
        self.app_key = app_key
        self._session = None

    def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _get_headers(self) -> Dict[str, str]:
        headers = {}
        if self.app_key:
            headers["AppKey"] = self.app_key
        return headers

    def _handle_error(self, exc: Exception) -> None:
        """Translates low-level aiohttp/network errors into structured SoarError subtypes."""
        if is_ssl_cert_verification_error(exc):
            logger.error("TLS certificate verification failed: %s", exc)
            raise SoarSSLError(
                "TLS certificate verification failed while connecting to SOAR. "
                "If you are using macOS (python.org installer), run: "
                "'/Applications/Python 3.X/Install Certificates.command' "
                "or set SSL_CERT_FILE with certifi's CA bundle (e.g. SSL_CERT_FILE=$(python -m certifi))."
            ) from exc

        if isinstance(exc, aiohttp.ClientResponseError):
            logger.debug("HTTP response error occurred (%s): %s", exc.status, exc)
            if exc.status in (401, 403):
                raise SoarAuthError(
                    f"SOAR authentication failed ({exc.status}): {exc.message}"
                ) from exc
            raise SoarHttpError(
                f"SOAR API returned HTTP {exc.status}: {exc.message}",
                status_code=exc.status,
            ) from exc

        if isinstance(exc, (aiohttp.ClientConnectorError, aiohttp.ServerTimeoutError)):
            logger.debug("Connection error occurred: %s", exc)
            raise SoarConnectionError(
                f"Failed to connect to SOAR endpoint ({self.base_url}): {exc}"
            ) from exc

        logger.debug("Unexpected error occurred: %s", exc)
        raise SoarError(f"SOAR request failed: {exc}") from exc

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Makes a GET request to the specified endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            params: Query parameters as a dictionary.

        Returns:
            The response as a JSON object, or None if an error occurred.
        """
        headers = await self._get_headers()
        try:
            async with self._get_session().get(
                self.base_url + endpoint, params=params, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            self._handle_error(e)

    async def post(
        self,
        endpoint: str,
        req: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Makes a POST request to the specified endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            req: The request body as a dictionary.
            params: Query parameters as a dictionary.

        Returns:
            The response as a JSON object, or None if an error occurred.
        """
        headers = await self._get_headers()
        try:
            async with self._get_session().post(
                self.base_url + endpoint, json=req, params=params, headers=headers
            ) as response:
                response.raise_for_status()
                data = await response.content.read()
                decoded_data = data.decode("utf-8")
                return json.loads(decoded_data)
        except Exception as e:
            self._handle_error(e)

    async def patch(
        self,
        endpoint: str,
        req: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Makes a PATCH request to the specified endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            req: The request body as a dictionary.
            params: Query parameters as a dictionary.

        Returns:
            The response as a JSON object, or None if an error occurred.
        """
        headers = await self._get_headers()
        try:
            async with self._get_session().patch(
                self.base_url + endpoint, json=req, params=params, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            self._handle_error(e)

    async def close(self) -> None:
        """Closes the underlying aiohttp session if open."""
        if self._session is not None:
            await self._session.close()
