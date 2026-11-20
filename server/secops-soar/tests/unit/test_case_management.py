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
"""Unit tests for SOAR case management tools and HTTP client paths."""

import json
import re
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Any, Self

import pytest

from secops_soar_mcp import bindings, case_management
from secops_soar_mcp.case_management import _validate_soar_id, register_tools
from secops_soar_mcp.http_client import HttpClient
from secops_soar_mcp.utils.consts import Endpoints


class _FakeMCP:
    def __init__(self) -> None:
        self.tools: dict[str, Callable[..., Awaitable[Any]]] = {}

    def tool(
        self,
    ) -> Callable[
        [Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]
    ]:
        def decorator(
            func: Callable[..., Awaitable[Any]],
        ) -> Callable[..., Awaitable[Any]]:
            self.tools[func.__name__] = func
            return func

        return decorator


class _FakeContent:
    def __init__(self, body: bytes) -> None:
        self._body = body

    async def read(self) -> bytes:
        return self._body


class _FakeResponse:
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self._data = {"ok": True} if data is None else data
        self.content = _FakeContent(json.dumps(self._data).encode("utf-8"))

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None

    def raise_for_status(self) -> None:
        return None

    async def json(self) -> dict[str, Any]:
        return self._data


class _RecordingSession:
    def __init__(self) -> None:
        self.requests: list[tuple[str, str, dict[str, Any]]] = []

    def get(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.requests.append(("GET", url, kwargs))
        return _FakeResponse()

    def post(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.requests.append(("POST", url, kwargs))
        return _FakeResponse()

    def patch(self, url: str, **kwargs: Any) -> _FakeResponse:
        self.requests.append(("PATCH", url, kwargs))
        return _FakeResponse()

    async def close(self) -> None:
        return None


@pytest.fixture
def case_tools(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[dict[str, Callable[..., Awaitable[Any]]], _RecordingSession]:
    client = HttpClient("https://soar.example.com", "test-app-key")
    session = _RecordingSession()
    client._session = session
    monkeypatch.setattr(bindings, "http_client", client)

    fake_mcp = _FakeMCP()
    register_tools(fake_mcp)  # type: ignore[arg-type]
    return fake_mcp.tools, session


INVALID_IDENTIFIERS: list[Any] = [
    "",
    "   ",
    "-",
    "-1",
    "--id",
    "_",
    "_id",
    "123/456",
    "../456",
    "..",
    "/123",
    "123/",
    "%2e%2e",
    "%252e%252e",
    "123%2f456",
    "123#section",
    "123?page=2",
    "//example.com/api",
    "123\\456",
    "{CASE_ID}",
    "123 456",
    "123\t456",
    "123\n456",
    "123\r456",
    "123\x00456",
    "123\x7f456",
    True,
    False,
    -1,
    None,
    12.34,
    ["523"],
    {"id": "523"},
]


@pytest.mark.parametrize(
    ("raw_id", "expected"),
    [
        ("0", "0"),
        (0, "0"),
        ("523", "523"),
        (523, "523"),
        (" 523 ", "523"),
        (
            "a1b2c3d4-e5f6-4321-abcd-ef1234567890",
            "a1b2c3d4-e5f6-4321-abcd-ef1234567890",
        ),
        ("alert_group_123-abc", "alert_group_123-abc"),
    ],
)
def test_validate_soar_id_accepts_valid_values(
    raw_id: str | int, expected: str
) -> None:
    assert _validate_soar_id(raw_id, "case_id") == expected


@pytest.mark.parametrize("bad_id", INVALID_IDENTIFIERS)
def test_validate_soar_id_rejects_invalid_values(bad_id: Any) -> None:
    with pytest.raises(ValueError):
        _validate_soar_id(bad_id, "case_id")


def _build_case_tool_call(
    tools: dict[str, Callable[..., Awaitable[Any]]],
    tool_name: str,
    case_id: Any,
) -> Awaitable[Any]:
    calls: dict[str, Callable[[], Awaitable[Any]]] = {
        "post_case_comment": lambda: tools["post_case_comment"](
            case_id=case_id, comment="Investigating"
        ),
        "list_alerts_by_case": lambda: tools["list_alerts_by_case"](
            case_id=case_id, next_page_token=None
        ),
        "list_alert_group_identifiers_by_case": lambda: tools[
            "list_alert_group_identifiers_by_case"
        ](case_id=case_id, next_page_token=None),
        "list_events_by_alert": lambda: tools["list_events_by_alert"](
            case_id=case_id, alert_id="751", next_page_token=None
        ),
        "change_case_priority": lambda: tools["change_case_priority"](
            case_id=case_id, case_priority="PriorityHigh"
        ),
        "update_case_description": lambda: tools["update_case_description"](
            case_id=case_id, description="Updated description"
        ),
        "close_case": lambda: tools["close_case"](
            case_id=case_id,
            root_cause="Routine maintenance",
            comment="Closing",
            reason="Inconclusive",
            tags=None,
        ),
        "assign_case": lambda: tools["assign_case"](
            case_id=case_id, user="analyst@example.com"
        ),
        "change_case_stage": lambda: tools["change_case_stage"](
            case_id=case_id, stage="Investigation"
        ),
        "add_case_tag": lambda: tools["add_case_tag"](
            case_id=case_id, tag="triage"
        ),
        "remove_case_tag": lambda: tools["remove_case_tag"](
            case_id=case_id, tag="triage"
        ),
        "get_entities_by_alert_group_identifiers": lambda: tools[
            "get_entities_by_alert_group_identifiers"
        ](
            case_id=case_id,
            alert_group_identifiers=["Email / Alert Group_1234"],
        ),
        "get_case_full_details": lambda: tools["get_case_full_details"](
            case_id=case_id
        ),
    }
    return calls[tool_name]()


CASE_ID_TOOLS: list[str] = [
    "post_case_comment",
    "list_alerts_by_case",
    "list_alert_group_identifiers_by_case",
    "list_events_by_alert",
    "change_case_priority",
    "update_case_description",
    "close_case",
    "assign_case",
    "change_case_stage",
    "add_case_tag",
    "remove_case_tag",
    "get_entities_by_alert_group_identifiers",
    "get_case_full_details",
]


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name", CASE_ID_TOOLS)
async def test_case_tools_validate_case_id(
    case_tools: tuple[dict[str, Callable[..., Awaitable[Any]]], _RecordingSession],
    tool_name: str,
) -> None:
    tools, session = case_tools
    with pytest.raises(ValueError):
        await _build_case_tool_call(tools, tool_name, "123/456")
    assert session.requests == []


@pytest.mark.asyncio
async def test_list_events_by_alert_validates_alert_id(
    case_tools: tuple[dict[str, Callable[..., Awaitable[Any]]], _RecordingSession],
) -> None:
    tools, session = case_tools
    with pytest.raises(ValueError):
        await tools["list_events_by_alert"](
            case_id="523", alert_id="123/456", next_page_token=None
        )
    assert session.requests == []


@pytest.mark.asyncio
async def test_case_tools_build_expected_requests(
    case_tools: tuple[dict[str, Callable[..., Awaitable[Any]]], _RecordingSession],
) -> None:
    tools, session = case_tools

    await tools["post_case_comment"](case_id="523", comment="ok")
    await tools["list_alerts_by_case"](case_id=" 523 ", next_page_token=None)
    await tools["list_alert_group_identifiers_by_case"](
        case_id="523", next_page_token=None
    )
    await tools["list_alert_group_identifiers_by_case"](
        case_id="523", next_page_token="page-2"
    )
    await tools["list_events_by_alert"](
        case_id="523",
        alert_id="a1b2c3d4-e5f6-4321-abcd-ef1234567890",
        next_page_token=None,
    )
    await tools["change_case_priority"](
        case_id="523", case_priority="PriorityHigh"
    )
    await tools["get_case_full_details"](case_id="alert_group_123-abc")

    assert session.requests[0][0:2] == (
        "POST",
        "https://soar.example.com/api/1p/external/v1/cases/523/comments",
    )
    assert session.requests[1][0:2] == (
        "GET",
        "https://soar.example.com/api/1p/external/v1.0/cases/523/caseAlerts",
    )
    assert session.requests[1][2]["params"] is None

    assert session.requests[2][0:2] == (
        "GET",
        "https://soar.example.com/api/1p/external/v1.0/cases/523/caseAlerts",
    )
    assert "?" not in session.requests[2][1]
    assert session.requests[2][2]["params"] == {
        "$select": "alertGroupIdentifier"
    }

    assert session.requests[3][0:2] == (
        "GET",
        "https://soar.example.com/api/1p/external/v1.0/cases/523/caseAlerts",
    )
    assert session.requests[3][2]["params"] == {
        "$select": "alertGroupIdentifier",
        "pageToken": "page-2",
    }

    assert session.requests[4][0:2] == (
        "GET",
        "https://soar.example.com/api/1p/external/v1.0/cases/523/alerts/a1b2c3d4-e5f6-4321-abcd-ef1234567890/involvedEvents",
    )
    assert session.requests[5][0:2] == (
        "PATCH",
        "https://soar.example.com/api/1p/external/v1/cases/523",
    )
    assert [req[0:2] for req in session.requests[6:9]] == [
        (
            "GET",
            "https://soar.example.com/api/1p/external/v1/cases/alert_group_123-abc",
        ),
        (
            "GET",
            "https://soar.example.com/api/1p/external/v1.0/cases/alert_group_123-abc/caseAlerts",
        ),
        (
            "GET",
            "https://soar.example.com/api/1p/external/v1/cases/alert_group_123-abc/comments",
        ),
    ]


@pytest.mark.asyncio
async def test_get_entities_preserves_alert_group_identifiers(
    case_tools: tuple[dict[str, Callable[..., Awaitable[Any]]], _RecordingSession],
) -> None:
    tools, session = case_tools
    groups = [
        "Email / Alert Group_1234",
        "Endpoint Detection / Host Alpha",
    ]
    await tools["get_entities_by_alert_group_identifiers"](
        case_id="523", alert_group_identifiers=groups
    )

    assert len(session.requests) == 1
    method, url, kwargs = session.requests[0]
    assert method == "POST"
    assert (
        url
        == "https://soar.example.com"
        + Endpoints.GET_ALERT_GROUP_IDENTIFIERS_ENTITIES
    )
    assert kwargs["json"] == {"caseId": "523", "alertGroupIdentifiers": groups}


@pytest.mark.asyncio
async def test_case_tools_quote_url_segments_without_encoding_json_bodies(
    case_tools: tuple[dict[str, Callable[..., Awaitable[Any]]], _RecordingSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools, session = case_tools
    monkeypatch.setattr(
        case_management,
        "_SOAR_ID_RE",
        re.compile(r"[A-Za-z0-9][A-Za-z0-9:_-]*", re.ASCII),
    )

    assert _validate_soar_id("case:523", "case_id") == "case:523"

    await tools["post_case_comment"](case_id="case:523", comment="ok")
    await tools["list_alerts_by_case"](
        case_id="case:523", next_page_token="page-2"
    )
    await tools["list_alert_group_identifiers_by_case"](
        case_id="case:523", next_page_token=None
    )
    await tools["list_events_by_alert"](
        case_id="case:523", alert_id="alert:751", next_page_token="page-2"
    )
    await tools["change_case_priority"](
        case_id="case:523", case_priority="PriorityHigh"
    )
    await tools["get_case_full_details"](case_id="case:523")

    await tools["update_case_description"](
        case_id="case:523", description="Updated"
    )
    await tools["close_case"](
        case_id="case:523",
        root_cause="Routine maintenance",
        comment="Closing",
        reason="Inconclusive",
        tags=None,
    )
    await tools["assign_case"](case_id="case:523", user="analyst@example.com")
    await tools["change_case_stage"](case_id="case:523", stage="Investigation")
    await tools["add_case_tag"](case_id="case:523", tag="triage")
    await tools["remove_case_tag"](case_id="case:523", tag="triage")
    await tools["get_entities_by_alert_group_identifiers"](
        case_id="case:523", alert_group_identifiers=["Group 1"]
    )

    assert [req[1] for req in session.requests[0:8]] == [
        "https://soar.example.com/api/1p/external/v1/cases/case%3A523/comments",
        "https://soar.example.com/api/1p/external/v1.0/cases/case%3A523/caseAlerts",
        "https://soar.example.com/api/1p/external/v1.0/cases/case%3A523/caseAlerts",
        "https://soar.example.com/api/1p/external/v1.0/cases/case%3A523/alerts/alert%3A751/involvedEvents",
        "https://soar.example.com/api/1p/external/v1/cases/case%3A523",
        "https://soar.example.com/api/1p/external/v1/cases/case%3A523",
        "https://soar.example.com/api/1p/external/v1.0/cases/case%3A523/caseAlerts",
        "https://soar.example.com/api/1p/external/v1/cases/case%3A523/comments",
    ]
    for _, _, kwargs in session.requests[8:14]:
        assert kwargs["json"]["CaseId"] == "case:523"
    assert session.requests[14][2]["json"]["caseId"] == "case:523"


INVALID_ENDPOINTS: list[Any] = [
    "",
    "api/1p/external/v1/cases",
    "//example.com/api",
    "https://example.com/api",
    "/api/1p/external/v1/cases/.",
    "/api/1p/external/v1/cases/..",
    "/api/1p/external/v1/cases/../523",
    "/api/1p/external/v1/cases/%2e%2e",
    "/api/1p/external/v1/cases/%252e%252e",
    "/api/1p/external/v1/cases/%25252e%25252e",
    "/api/1p/external/v1/cases/%252525252e",
    "/api/1p/external/v1/cases/123%2f456",
    "/api/1p/external/v1/cases/123%5c456",
    "/api/1p/external/v1/cases/123%3fpage=2",
    "/api/1p/external/v1/cases/123%23section",
    "/api/1p/external/v1/cases/123%2523section",
    "/api/1p/external/v1/cases/%2500",
    "/api/1p/external/v1/cases/%250d%250a",
    "/api/1p/external/v1/cases/123#section",
    "/api/1p/external/v1/cases/123\\456",
    "/api/1p/external/v1/cases/123\n456",
    "/api/1p/external/v1/cases/123 456",
    "/api/1p/external/v1/cases/123\x00",
    "/api/1p/external/v1/cases/123\x7f",
    None,
]


@pytest.mark.parametrize("bad_endpoint", INVALID_ENDPOINTS)
def test_validate_endpoint_rejects_invalid_paths(bad_endpoint: Any) -> None:
    with pytest.raises(ValueError):
        HttpClient._validate_endpoint(bad_endpoint)


@pytest.mark.parametrize(
    "good_endpoint",
    [
        "/api/1p/external/v1/cases/523/comments",
        "/api/1p/external/v1/cases/case%3A523/comments",
        "/api/1p/external/v1.0/cases/523/caseAlerts",
        Endpoints.LIST_INTEGRATION_INSTANCES.format(INTEGRATION_NAME="Siemplify"),
    ],
)
def test_validate_endpoint_accepts_valid_paths(good_endpoint: str) -> None:
    assert HttpClient._validate_endpoint(good_endpoint) == good_endpoint


@pytest.mark.asyncio
@pytest.mark.parametrize("method_name", ["get", "post", "patch"])
@pytest.mark.parametrize(
    "bad_endpoint",
    [
        "api/1p/external/v1/cases",
        "/api/1p/external/v1/cases/../523",
    ],
)
async def test_http_client_validates_endpoint_before_request(
    method_name: str, bad_endpoint: str
) -> None:
    client = HttpClient("https://soar.example.com", "test-app-key")
    session = _RecordingSession()
    client._session = session

    with pytest.raises(ValueError):
        await getattr(client, method_name)(bad_endpoint)
    assert session.requests == []
