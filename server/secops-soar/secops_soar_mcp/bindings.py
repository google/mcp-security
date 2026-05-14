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
"""Bindings for the SOAR client."""

import os

import dotenv
from logger_utils import get_logger
from secops_soar_mcp.http_client import HttpClient, SoarSSLError, SoarConnectionError
from secops_soar_mcp.utils import consts

dotenv.load_dotenv()

logger = get_logger(__name__)


http_client: HttpClient = None
valid_scopes = set()


async def _get_valid_scopes():
    valid_scopes_list = await http_client.get(consts.Endpoints.GET_SCOPES)
    if valid_scopes_list is None:
        raise RuntimeError(consts.CREDENTIALS_ERROR_MESSAGE)
    return set(valid_scopes_list)


async def bind():
    """Binds global variables.

    Raises:
        SoarSSLError: If an SSL certificate verification error occurs
            when connecting to SOAR.
        SoarConnectionError: If the SOAR server cannot be reached.
        RuntimeError: If the SOAR credentials are invalid or scopes
            cannot be fetched.
    """
    global http_client, valid_scopes
    http_client = HttpClient(
        os.getenv(consts.ENV_SOAR_URL), os.getenv(consts.ENV_SOAR_APP_KEY)
    )
    valid_scopes = await _get_valid_scopes()


async def cleanup():
    """Cleans up global variables."""
    await http_client.close()
