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
from typing import Any, Dict

import aiohttp
from logger_utils import get_logger
from secops_soar_mcp.utils import consts

logger = get_logger(__name__)


class SoarSSLError(Exception):
    """Raised when an SSL certificate error occurs connecting to SOAR."""


class SoarConnectionError(Exception):
    """Raised when a connection to the SOAR server cannot be established."""


def _is_cert_verify_error(error: BaseException) -> bool:
    """Check if an error is caused by SSL certificate verification failure.

    Inspects the error message, its chain of causes (__cause__), and
    type to determine if the root cause is a certificate verification
    failure.
    """
    # Walk the cause chain to find CERTIFICATE_VERIFY_FAILED anywhere
    current = error
    while current is not None:
        error_str = str(current).lower()
        if (
            "certificate_verify_failed" in error_str
            or "certificate verify failed" in error_str
        ):
            return True
        if isinstance(current, ssl.SSLCertVerificationError):
            return True
        current = getattr(current, "__cause__", None)
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

    async def _get_headers(self):
        headers = {}
        if self.app_key:
            headers["AppKey"] = self.app_key
        return headers

    def _handle_ssl_error(self, error: Exception) -> None:
        """Check for SSL errors and raise descriptive exceptions.

        Args:
            error: The exception to inspect.

        Raises:
            SoarSSLError: If the error is an SSL certificate verification issue.
            SoarConnectionError: If the error is a non-SSL connection issue.
        """
        if isinstance(error, aiohttp.ClientConnectorSSLError):
            if _is_cert_verify_error(error):
                logger.error(
                    "SSL certificate verification failed: %s", error
                )
                raise SoarSSLError(
                    consts.SSL_CERTIFI_ERROR_MESSAGE
                ) from error
            else:
                logger.error("SSL/TLS error: %s", error)
                raise SoarSSLError(
                    consts.SSL_GENERIC_ERROR_MESSAGE.format(error=error)
                ) from error

        if isinstance(error, aiohttp.ClientConnectorError):
            logger.error("Connection error: %s", error)
            raise SoarConnectionError(
                consts.CONNECTION_ERROR_MESSAGE.format(url=self.base_url)
            ) from error

        # Also catch raw ssl.SSLError that may not be wrapped by aiohttp
        if isinstance(error, ssl.SSLError):
            if _is_cert_verify_error(error):
                logger.error(
                    "SSL certificate verification failed: %s", error
                )
                raise SoarSSLError(
                    consts.SSL_CERTIFI_ERROR_MESSAGE
                ) from error
            else:
                logger.error("SSL/TLS error: %s", error)
                raise SoarSSLError(
                    consts.SSL_GENERIC_ERROR_MESSAGE.format(error=error)
                ) from error

    async def get(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
    ):
        """Makes a GET request to the specified endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            params: Query parameters as a dictionary.

        Returns:
            The response as a JSON object, or None if an error occurred.

        Raises:
            SoarSSLError: If an SSL certificate verification error occurs.
            SoarConnectionError: If the SOAR server cannot be reached.
        """
        headers = await self._get_headers()
        try:
            async with self._get_session().get(
                self.base_url + endpoint, params=params, headers=headers
            ) as response:
                response.raise_for_status()  # Raise an exception for 4xx/5xx responses
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.debug("HTTP error occurred: %s", e)
        except Exception as e:
            self._handle_ssl_error(e)
            logger.debug("An error occurred: %s", e)
        return None

    async def post(
        self,
        endpoint: str,
        req: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ):
        """Makes a POST request to the specified endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            req: The request body as a dictionary.
            params: Query parameters as a dictionary.

        Returns:
            The response as a JSON object, or None if an error occurred.

        Raises:
            SoarSSLError: If an SSL certificate verification error occurs.
            SoarConnectionError: If the SOAR server cannot be reached.
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
        except aiohttp.ClientResponseError as e:
            logger.debug("HTTP error occurred: %s", e)
        except Exception as e:
            self._handle_ssl_error(e)
            logger.debug("An error occurred: %s", e)
        return None

    async def patch(
        self,
        endpoint: str,
        req: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ):
        """Makes a PATCH request to the specified endpoint.

        Args:
            endpoint: The API endpoint to send the request to.
            req: The request body as a dictionary.
            params: Query parameters as a dictionary.

        Returns:
            The response as a JSON object, or None if an error occurred.

        Raises:
            SoarSSLError: If an SSL certificate verification error occurs.
            SoarConnectionError: If the SOAR server cannot be reached.
        """
        headers = await self._get_headers()
        try:
            async with self._get_session().patch(
                self.base_url + endpoint, json=req, params=params, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logger.debug("HTTP error occurred: %s", e)
        except Exception as e:
            self._handle_ssl_error(e)
            logger.debug("An error occurred: %s", e)
        return None

    async def close(self):
        await self._get_session().close()
