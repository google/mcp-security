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
from typing import Optional, Set

import dotenv
from logger_utils import get_logger
from secops_soar_mcp.exceptions import (
    SoarAuthError,
    SoarConnectionError,
    SoarError,
    SoarSSLError,
)
from secops_soar_mcp.http_client import HttpClient
from secops_soar_mcp.utils import consts

dotenv.load_dotenv()

logger = get_logger(__name__)


http_client: Optional[HttpClient] = None
valid_scopes: Set[str] = set()


async def _get_valid_scopes() -> Set[str]:
    """Fetches valid scopes from SOAR endpoint during startup."""
    try:
        valid_scopes_list = await http_client.get(consts.Endpoints.GET_SCOPES)
        if valid_scopes_list is None:
            raise RuntimeError(
                "Failed to fetch valid scopes from SOAR, please make sure you have "
                "configured the right SOAR credentials. Shutting down..."
            )
        return set(valid_scopes_list)
    except SoarSSLError as e:
        raise RuntimeError(
            "Failed to fetch valid scopes from SOAR because TLS certificate "
            "verification failed. If you are using macOS (python.org installer), "
            "run the 'Install Certificates.command' for your Python version, for example: "
            "`/Applications/Python 3.12/Install Certificates.command`. "
            "You can also point Python at certifi's CA bundle with "
            "`SSL_CERT_FILE=$(python -m certifi)`."
        ) from e
    except SoarAuthError as e:
        raise RuntimeError(
            "Failed to fetch valid scopes from SOAR: authentication failed. "
            "Please make sure you have configured the right SOAR credentials "
            "(SOAR_URL, SOAR_APP_KEY). Shutting down..."
        ) from e
    except SoarConnectionError as e:
        raise RuntimeError(
            f"Failed to fetch valid scopes from SOAR: connection failed to {http_client.base_url}. "
            "Please check network connectivity or proxy settings. Shutting down..."
        ) from e
    except SoarError as e:
        raise RuntimeError(
            f"Failed to fetch valid scopes from SOAR: {e}. Shutting down..."
        ) from e


async def bind() -> None:
    """Binds global variables."""
    global http_client, valid_scopes
    http_client = HttpClient(
        os.getenv(consts.ENV_SOAR_URL), os.getenv(consts.ENV_SOAR_APP_KEY)
    )
    valid_scopes = await _get_valid_scopes()


async def cleanup() -> None:
    """Cleans up global variables."""
    if http_client is None:
        return
    await http_client.close()
