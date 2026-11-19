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
"""Google Cloud credentials for requests to the remote Chronicle MCP server."""

import asyncio
import json
import logging
from typing import Any

import google.auth
import google.auth.exceptions
import google.auth.transport.requests
import httpx

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


class GoogleAuthTransport(httpx.AsyncBaseTransport):
    """Adds a current ADC token and the quota project to every request.

    The token is refreshed when it has expired, and once more if the server
    answers 401, so a run that outlives one token keeps working.

    The MCP client ends the whole connection when a POST fails, so one 403,
    429 or 500 would break every later call. Here a failed POST, a failed
    token refresh or a network error becomes a JSON-RPC error reply to that
    one request instead.
    """

    def __init__(
        self,
        credentials: Any,
        quota_project: str,
        request: Any = None,
        inner: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._credentials = credentials
        self._quota_project = quota_project
        self._request = request or google.auth.transport.requests.Request()
        self._inner = inner or httpx.AsyncHTTPTransport()
        self._refresh_lock = asyncio.Lock()

    @classmethod
    def from_adc(cls, quota_project: str) -> "GoogleAuthTransport":
        credentials, _ = google.auth.default(scopes=SCOPES)
        return cls(credentials, quota_project)

    def refresh(self) -> None:
        self._credentials.refresh(self._request)

    async def _refresh(self, stale_token: str | None) -> None:
        # One refresh at a time; callers that waited reuse the new token.
        async with self._refresh_lock:
            if self._credentials.token == stale_token or not self._credentials.valid:
                await asyncio.to_thread(self.refresh)

    def _apply(self, request: httpx.Request) -> str:
        token = self._credentials.token
        request.headers["Authorization"] = f"Bearer {token}"
        request.headers["x-goog-user-project"] = self._quota_project
        return token

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        try:
            if not self._credentials.valid:
                await self._refresh(self._credentials.token)
            token = self._apply(request)
            response = await self._inner.handle_async_request(request)
            if response.status_code == 401:
                await response.aclose()
                await self._refresh(token)
                self._apply(request)
                response = await self._inner.handle_async_request(request)
        except Exception as error:  # noqa: BLE001 - becomes an error reply below
            # Only the exception type is shown; the message could hold a token.
            logger.warning(
                "Request to %s failed: %s", request.url.host, type(error).__name__
            )
            if isinstance(error, google.auth.exceptions.GoogleAuthError):
                message = (
                    f"UNAUTHENTICATED: Google credentials could not be refreshed ({type(error).__name__}). "
                    "Run `gcloud auth application-default login`."
                )
            else:
                message = f"UNAVAILABLE: {type(error).__name__} while contacting {request.url.host}."
            return _error_reply(request, message)
        # 202 and 404 have their own meaning in the MCP transport.
        if (
            request.method == "POST"
            and response.status_code >= 400
            and response.status_code != 404
        ):
            body = (await response.aread())[:500].decode("utf-8", errors="replace")
            await response.aclose()
            return _error_reply(
                request, f"HTTP {response.status_code} {response.reason_phrase}: {body}"
            )
        return response

    async def aclose(self) -> None:
        await self._inner.aclose()


def _error_reply(request: httpx.Request, message: str) -> httpx.Response:
    """Answer one JSON-RPC request with an error, or accept a notification."""
    try:
        sent = json.loads(request.content)
    except (ValueError, httpx.RequestNotRead):
        sent = None
    if isinstance(sent, dict) and "id" in sent and "method" in sent:
        return httpx.Response(
            200,
            json={
                "jsonrpc": "2.0",
                "id": sent["id"],
                "error": {"code": -32000, "message": message},
            },
            request=request,
        )
    return httpx.Response(202, request=request)
