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
import ssl

import dotenv
from logger_utils import get_logger
from secops_soar_mcp.http_client import HttpClient
from secops_soar_mcp.utils import consts

dotenv.load_dotenv()

logger = get_logger(__name__)


http_client: HttpClient = None
valid_scopes = set()

_CERTIFICATE_ERROR_MESSAGE = (
    "Failed to fetch valid scopes from SOAR due to an SSL certificate "
    "verification error. This is usually a local CA certificate "
    "configuration issue, not incorrect SOAR credentials. Install the "
    "certifi CA bundle, e.g. run Python's `Install Certificates.command` "
    "(macOS) or point SSL_CERT_FILE at the output of `python -m certifi`. "
    "See the 'Additionally, for the secops-soar MCP server...' note in "
    "README.md / docs/usage_guide.md for the exact setup steps. "
    "Shutting down..."
)


async def _get_valid_scopes():
    try:
        valid_scopes_list = await http_client.get(consts.Endpoints.GET_SCOPES)
    except ssl.SSLError as e:
        raise RuntimeError(_CERTIFICATE_ERROR_MESSAGE) from e
    if valid_scopes_list is None:
        raise RuntimeError(
            "Failed to fetch valid scopes from SOAR, please make sure you have configured the right SOAR credentials. Shutting down..."
        )
    return set(valid_scopes_list)


async def bind():
    """Binds global variables."""
    global http_client, valid_scopes
    http_client = HttpClient(
        os.getenv(consts.ENV_SOAR_URL), os.getenv(consts.ENV_SOAR_APP_KEY)
    )
    valid_scopes = await _get_valid_scopes()


async def cleanup():
    """Cleans up global variables."""
    if http_client is None:
        return
    await http_client.close()
