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
"""Exceptions for Chronicle SecOps SOAR MCP."""

from typing import Optional


class SoarError(Exception):
    """Base exception for all SecOps SOAR errors."""

    pass


class SoarConnectionError(SoarError):
    """Raised when connecting to the SOAR server fails (network/DNS/timeout)."""

    pass


class SoarSSLError(SoarConnectionError):
    """Raised when TLS/SSL certificate verification fails."""

    pass


class SoarAuthError(SoarError):
    """Raised when authentication with the SOAR server fails (e.g. 401 Unauthorized, 403 Forbidden)."""

    pass


class SoarHttpError(SoarError):
    """Raised for unexpected HTTP error responses from SOAR."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
