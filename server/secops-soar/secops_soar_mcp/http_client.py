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
from typing import Any, Dict

import aiohttp
from logger_utils import get_logger

logger = get_logger(__name__)


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
            logger.debug("An error occurred: %s", e)
        return None

    async def close(self):
        await self._get_session().close()
