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
"""Tests for the transport that adds Google Cloud credentials."""

import asyncio
import json

import google.auth.exceptions
import httpx
import pytest
from mcp import ClientSession, types
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.exceptions import McpError

from redacting_gateway.auth import GoogleAuthTransport

URL = "https://chronicle.us.rep.googleapis.com/mcp"
CALL = {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "x"}}


class FakeCredentials:
    def __init__(self, token: str | None, valid: bool, fail: bool = False) -> None:
        self.token = token
        self.valid = valid
        self.fail = fail
        self.refreshes = 0

    def refresh(self, request) -> None:
        self.refreshes += 1
        if self.fail:
            raise google.auth.exceptions.RefreshError("token endpoint said no")
        self.token = f"token-{self.refreshes}"
        self.valid = True


def client(credentials: FakeCredentials, handler) -> httpx.AsyncClient:
    transport = GoogleAuthTransport(
        credentials,
        quota_project="quota-project",
        request=object(),
        inner=httpx.MockTransport(handler),
    )
    return httpx.AsyncClient(transport=transport)


def accepting(tokens: set[str], seen: list):
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.headers))
        token = request.headers["Authorization"].removeprefix("Bearer ")
        return httpx.Response(200 if token in tokens else 401, json={})

    return handler


async def test_every_request_carries_the_token_and_quota_project() -> None:
    seen: list = []
    credentials = FakeCredentials("token-0", valid=True)
    async with client(credentials, accepting({"token-0"}, seen)) as http:
        response = await http.post(URL, json=CALL)
    assert response.status_code == 200
    assert seen[0]["authorization"] == "Bearer token-0"
    assert seen[0]["x-goog-user-project"] == "quota-project"
    assert credentials.refreshes == 0


async def test_an_expired_token_is_refreshed_before_sending() -> None:
    seen: list = []
    credentials = FakeCredentials("old", valid=False)
    async with client(credentials, accepting({"token-1"}, seen)) as http:
        response = await http.post(URL, json=CALL)
    assert response.status_code == 200
    assert [h["authorization"] for h in seen] == ["Bearer token-1"]


async def test_a_401_refreshes_once_and_retries() -> None:
    seen: list = []
    credentials = FakeCredentials("revoked", valid=True)
    async with client(credentials, accepting({"token-1"}, seen)) as http:
        response = await http.post(URL, json=CALL)
    assert response.status_code == 200
    assert [h["authorization"] for h in seen] == ["Bearer revoked", "Bearer token-1"]


async def test_concurrent_401s_share_one_refresh() -> None:
    seen: list = []
    credentials = FakeCredentials("revoked", valid=True)
    async with client(credentials, accepting({"token-1"}, seen)) as http:
        responses = await asyncio.gather(*(http.post(URL, json=CALL) for _ in range(5)))
    assert {r.status_code for r in responses} == {200}
    assert credentials.refreshes == 1


@pytest.mark.parametrize(
    ("status", "word"),
    [
        (401, "Unauthorized"),
        (403, "Forbidden"),
        (429, "Too Many Requests"),
        (500, "Internal Server Error"),
    ],
)
async def test_a_failed_post_becomes_an_error_reply_to_that_request(
    status, word
) -> None:
    credentials = FakeCredentials("token-0", valid=True)
    async with client(
        credentials, lambda request: httpx.Response(status, text="details")
    ) as http:
        response = await http.post(URL, json=CALL)
    body = response.json()
    assert response.status_code == 200
    assert body["id"] == 7
    assert body["error"]["message"].startswith(f"HTTP {status} {word}: details")


async def test_a_failed_notification_is_accepted_quietly() -> None:
    credentials = FakeCredentials("token-0", valid=True)
    async with client(credentials, lambda request: httpx.Response(500)) as http:
        response = await http.post(
            URL, json={"jsonrpc": "2.0", "method": "notifications/initialized"}
        )
    assert response.status_code == 202


async def test_a_refresh_failure_becomes_an_auth_error_reply() -> None:
    credentials = FakeCredentials("old", valid=False, fail=True)
    async with client(credentials, accepting(set(), [])) as http:
        response = await http.post(URL, json=CALL)
    message = response.json()["error"]["message"]
    assert message.startswith("UNAUTHENTICATED")
    assert "token endpoint said no" not in message


async def test_a_network_error_becomes_an_error_reply() -> None:
    def unreachable(request):
        raise httpx.ConnectError("no route", request=request)

    credentials = FakeCredentials("token-0", valid=True)
    async with client(credentials, unreachable) as http:
        response = await http.post(URL, json=CALL)
    assert response.json()["error"]["message"].startswith("UNAVAILABLE: ConnectError")


def fake_mcp_server(request: httpx.Request) -> httpx.Response:
    """Just enough of the MCP streamable HTTP protocol for one session."""
    if request.method != "POST":
        return httpx.Response(405)
    message = json.loads(request.content)
    if "id" not in message:
        return httpx.Response(202)
    if message["method"] == "initialize":
        result = {
            "protocolVersion": types.LATEST_PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "fake", "version": "1"},
        }
    elif message["method"] == "tools/list":
        result = {
            "tools": [
                {"name": name, "inputSchema": {"type": "object"}}
                for name in ("forbidden", "fine")
            ]
        }
    elif message["params"]["name"] == "forbidden":
        return httpx.Response(403, text="caller lacks permission")
    else:
        result = {"content": [{"type": "text", "text": "ok"}], "isError": False}
    return httpx.Response(
        200, json={"jsonrpc": "2.0", "id": message["id"], "result": result}
    )


async def test_an_http_error_fails_one_call_and_the_session_keeps_working() -> None:
    credentials = FakeCredentials("token-0", valid=True)
    async with (
        client(credentials, fake_mcp_server) as http,
        streamable_http_client(URL, http_client=http) as (read, write, _),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        with pytest.raises(McpError, match="HTTP 403 Forbidden"):
            await session.call_tool("forbidden", {})
        result = await session.call_tool("fine", {})
    assert result.content[0].text == "ok"
