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

from collections import deque
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


def _is_certificate_verification_error(error: BaseException | None) -> bool:
    if error is None:
        return False
    pending = deque([error])
    seen: set[int] = set()
    while pending:
        current = pending.popleft()
        if id(current) in seen:
            continue
        seen.add(id(current))
        message = str(current).lower()
        if isinstance(current, ssl.SSLCertVerificationError):
            return True
        if (
            isinstance(current, ssl.SSLError)
            and "certificate verify failed" in message
        ):
            return True
        if "certificate verify failed" in message:
            return True
        for related in (current.__cause__, current.__context__):
            if isinstance(related, BaseException):
                pending.append(related)
        for arg in getattr(current, "args", ()):
            if isinstance(arg, BaseException):
                pending.append(arg)
    return False


def _valid_scopes_error_message(error: BaseException | None) -> str:
    if _is_certificate_verification_error(error):
        return (
            "Failed to fetch valid scopes from SOAR because TLS certificate "
            "verification failed. If you are using the Python.org macOS "
            "installer, run the Install Certificates.command for your Python "
            "version, for example: "
            "`/Applications/Python\\ 3.12/Install\\ Certificates.command`. "
            "You can also point Python at certifi's CA bundle with "
            "`SSL_CERT_FILE=$(python -m certifi)`."
        )
    return (
        "Failed to fetch valid scopes from SOAR, please make sure you have "
        "configured the right SOAR credentials. Shutting down..."
    )


async def _get_valid_scopes():
    valid_scopes_list = await http_client.get(consts.Endpoints.GET_SCOPES)
    if valid_scopes_list is None:
        raise RuntimeError(_valid_scopes_error_message(http_client.last_error))
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
    await http_client.close()
