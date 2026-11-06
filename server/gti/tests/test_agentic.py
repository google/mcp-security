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
import asyncio
import json
import logging
from unittest import mock

import mcp
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
import pytest
import pytest_httpserver
import vt
from werkzeug.wrappers import Request, Response

from gti_mcp.server import server


SESSION_ID = "75033b8c-59aa-4751-81ae-db86a15b609b"
CLONED_SESSION_ID = "9120ab11-33cc-49ef-92aa-112233445566"


@pytest.fixture(autouse=True)
def fresh_vt_client_factory(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    monkeypatch: pytest.MonkeyPatch,
):
  """Returns a fresh vt.Client per request so close_async() stays isolated."""
  host = f"http://{make_httpserver_ipv4.host}:{make_httpserver_ipv4.port}"
  monkeypatch.setattr(
      "gti_mcp.server.vt_client_factory",
      lambda _ctx: vt.Client("dummy_api_key", host=host, timeout=30),
  )


async def _call_json_tool(name: str, arguments: dict) -> dict:
  async with client_session(server._mcp_server) as client:
    result = await client.call_tool(name, arguments=arguments)
  assert not result.isError, result.content[0].text
  assert len(result.content) == 1
  return json.loads(result.content[0].text)


def _sample_session_response(
    session_id: str = SESSION_ID,
    answer_markdown: str = "### APT29 Summary\nAPT29 targets diplomatic entities.",
) -> dict:
  return {
      "data": {
          "id": session_id,
          "type": "agentic_session",
          "attributes": {
              "title": "APT29 Threat Investigation",
              "creation_date": "2026-11-03T00:00:00Z",
              "last_modification_date": "2026-11-03T00:00:15Z",
              "events": [
                  {
                      "id": "evt-user-1",
                      "message_type": "USER_MESSAGE",
                      "user_message": {
                          "timestamp_seconds": 1793664000,
                          "widgets": [
                              {
                                  "widget_type": "MARKDOWN_TEXT",
                                  "markdown_text_widget": {
                                      "text": "Summarize APT29."
                                  },
                              }
                          ],
                      },
                  },
                  {
                      "id": "evt-thought-1",
                      "message_type": "AGENT_THOUGHT",
                      "agent_thought": {
                          "text": "Internal reasoning step that should stay out."
                      },
                  },
                  {
                      "id": "evt-fn-call-1",
                      "message_type": "FUNCTION_CALL",
                      "function_call": {"name": "search_threats"},
                  },
                  {
                      "id": "evt-fn-resp-1",
                      "message_type": "FUNCTION_RESPONSE",
                      "function_response": {"raw_blob": "x" * 2048},
                  },
                  {
                      "id": "evt-final-1",
                      "message_type": "AGENT_FINAL_RESPONSE",
                      "agent_final_response": {
                          "agent_id": "threat-intel-specialist",
                          "gti_citations": [
                              {
                                  "id": "report--apt29-001",
                                  "title": "APT29 Diplomatic Espionage",
                              }
                          ],
                          "widgets": [
                              {
                                  "widget_type": "MARKDOWN_TEXT",
                                  "markdown_text_widget": {
                                      "text": answer_markdown
                                  },
                              },
                              {
                                  "widget_type": "RULE",
                                  "rule_widget": {
                                      "rule_type": "yara",
                                      "content": "rule apt29_loader { condition: true }",
                                  },
                              },
                          ],
                      },
                  },
              ],
          },
      }
  }


@pytest.mark.asyncio(loop_scope="session")
async def test_agentic_tools_registered():
  """All 7 GTI Agentic session tools are exposed on the MCP server."""
  async with client_session(server._mcp_server) as client:
    tools_result = await client.list_tools()

  assert isinstance(tools_result, mcp.ListToolsResult)
  tool_names = {tool.name for tool in tools_result.tools}
  expected = {
      "ask_gti_agent",
      "continue_chat",
      "list_sessions",
      "get_session_history",
      "delete_session",
      "share_session",
      "copy_shared_session",
  }
  assert expected.issubset(tool_names)


@pytest.mark.asyncio(loop_scope="session")
async def test_ask_gti_agent_sends_multipart_and_compacts_turn(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
):
  """ask_gti_agent sends multipart/form-data and strips thought/tool trace noise."""
  captured = {}

  def _handle_create_session(request: Request) -> Response:
    captured["content_type"] = request.headers.get("Content-Type", "")
    captured["message"] = request.form.get("message")
    return Response(
        json.dumps(_sample_session_response()),
        status=200,
        headers={"X-Session-Id": SESSION_ID},
        content_type="application/json",
    )

  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/agentspace/sessions",
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_handler(_handle_create_session)

  data = await _call_json_tool(
      "ask_gti_agent", {"message": "Summarize APT29."}
  )

  assert captured["content_type"].startswith("multipart/form-data")
  assert captured["message"] == "Summarize APT29."
  assert data["session_id"] == SESSION_ID
  assert data["title"] == "APT29 Threat Investigation"
  assert data["agent_id"] == "threat-intel-specialist"
  assert "APT29 targets diplomatic entities." in data["response"]
  assert data["citations"] == [
      {"id": "report--apt29-001", "title": "APT29 Diplomatic Espionage"}
  ]
  assert len(data["widgets"]) == 1
  assert data["widgets"][0]["widget_type"] == "RULE"
  serialized = json.dumps(data)
  assert "Internal reasoning step" not in serialized
  assert "raw_blob" not in serialized


@pytest.mark.asyncio(loop_scope="session")
async def test_continue_chat_sends_multipart_to_session(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
):
  """continue_chat posts multipart/form-data to /agentspace/sessions/{id}."""
  captured = {}

  def _handle_continue(request: Request) -> Response:
    captured["content_type"] = request.headers.get("Content-Type", "")
    captured["message"] = request.form.get("message")
    return Response(
        json.dumps(
            _sample_session_response(
                answer_markdown="Primary initial access uses spearphishing."
            )
        ),
        status=200,
        content_type="application/json",
    )

  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/agentspace/sessions/{SESSION_ID}",
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_handler(_handle_continue)

  data = await _call_json_tool(
      "continue_chat",
      {
          "session_id": SESSION_ID,
          "message": "What initial access vectors do they use?",
      },
  )

  assert captured["content_type"].startswith("multipart/form-data")
  assert captured["message"] == "What initial access vectors do they use?"
  assert data["session_id"] == SESSION_ID
  assert data["response"] == "Primary initial access uses spearphishing."


@pytest.mark.asyncio(loop_scope="session")
async def test_list_sessions_drops_null_and_empty_params(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
):
  """list_sessions omits None/empty query params and returns session summaries."""
  captured = {}

  def _handle_list(request: Request) -> Response:
    captured["args"] = dict(request.args)
    return Response(
        json.dumps({
            "data": [
                {
                    "id": SESSION_ID,
                    "type": "agentic_session",
                    "attributes": {
                        "title": "APT29 Threat Investigation",
                        "creation_date": "2026-11-03T00:00:00Z",
                        "last_modification_date": "2026-11-03T00:00:15Z",
                        "events": [{"id": "evt-heavy"}],
                    },
                }
            ],
            "meta": {"cursor": "next-page-cursor-1"},
        }),
        status=200,
        content_type="application/json",
    )

  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/agentspace/sessions",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_handler(_handle_list)

  data = await _call_json_tool(
      "list_sessions",
      {"limit": 3, "order": None, "filter": "", "cursor": "page-0"},
  )

  assert captured["args"] == {"limit": "3", "cursor": "page-0"}
  assert len(data["sessions"]) == 1
  assert data["sessions"][0]["id"] == SESSION_ID
  assert data["sessions"][0]["title"] == "APT29 Threat Investigation"
  assert "events" not in data["sessions"][0]
  assert data["cursor"] == "next-page-cursor-1"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_session_history_filters_intermediate_events_by_default(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
):
  """get_session_history keeps USER_MESSAGE and AGENT_FINAL_RESPONSE by default."""
  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/agentspace/sessions/{SESSION_ID}",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(_sample_session_response())

  compact = await _call_json_tool(
      "get_session_history", {"session_id": SESSION_ID}
  )
  event_types = [e["message_type"] for e in compact["events"]]
  assert event_types == ["USER_MESSAGE", "AGENT_FINAL_RESPONSE"]

  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/agentspace/sessions/{SESSION_ID}",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(_sample_session_response())

  full = await _call_json_tool(
      "get_session_history",
      {"session_id": SESSION_ID, "include_intermediate_events": True},
  )
  full_types = [e["message_type"] for e in full["events"]]
  assert "AGENT_THOUGHT" in full_types
  assert "FUNCTION_CALL" in full_types


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("status_code", [200, 204])
async def test_delete_session_handles_200_and_204(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    status_code: int,
):
  """delete_session succeeds cleanly on both 200 JSON and 204 empty responses."""
  body = "" if status_code == 204 else json.dumps({"data": {}})
  content_type = "text/plain" if status_code == 204 else "application/json"
  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/agentspace/sessions/{SESSION_ID}",
      method="DELETE",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_data(body, status=status_code, content_type=content_type)

  data = await _call_json_tool("delete_session", {"session_id": SESSION_ID})
  assert data["deleted"] is True
  assert data["session_id"] == SESSION_ID


@pytest.mark.asyncio(loop_scope="session")
async def test_share_and_copy_shared_session_handles_201(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
):
  """share_session retrieves token and copy_shared_session handles 201 Created."""
  make_httpserver_ipv4.expect_oneshot_request(
      f"/api/v3/agentspace/sessions/{SESSION_ID}/token",
      method="GET",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json({"data": {"token": "share-tok-xyz"}})

  shared = await _call_json_tool("share_session", {"session_id": SESSION_ID})
  assert shared["session_id"] == SESSION_ID
  assert shared["share_token"] == "share-tok-xyz"

  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/agentspace/sessions/token",
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
      json={"token": "share-tok-xyz"},
  ).respond_with_json(
      _sample_session_response(session_id=CLONED_SESSION_ID),
      status=201,
  )

  cloned = await _call_json_tool(
      "copy_shared_session", {"share_token": "share-tok-xyz"}
  )
  assert cloned["session_id"] == CLONED_SESSION_ID
  assert cloned["title"] == "APT29 Threat Investigation"
  assert "APT29 targets diplomatic entities." in cloned["response"]


@pytest.mark.asyncio(loop_scope="session")
async def test_ask_gti_agent_error_and_timeout_handling(
    make_httpserver_ipv4: pytest_httpserver.HTTPServer,
    caplog: pytest.LogCaptureFixture,
):
  """4xx errors and timeouts return clean dicts and use lazy %s logger args."""
  make_httpserver_ipv4.expect_oneshot_request(
      "/api/v3/agentspace/sessions",
      method="POST",
      headers={"X-Apikey": "dummy_api_key"},
  ).respond_with_json(
      {
          "error": {
              "code": "ForbiddenError",
              "message": "Agentic quota exhausted",
          }
      },
      status=403,
  )

  with caplog.at_level(logging.WARNING, logger="gti_mcp.tools.agentic"):
    err_data = await _call_json_tool(
        "ask_gti_agent", {"message": "Test forbidden"}
    )

  assert "error" in err_data
  assert "ForbiddenError" in err_data["error"]
  assert "Agentic quota exhausted" in err_data["error"]
  assert caplog.records
  assert all(record.args for record in caplog.records)

  mock_client = mock.MagicMock()
  mock_client.post_async = mock.AsyncMock(side_effect=asyncio.TimeoutError())
  mock_cm = mock.MagicMock()
  mock_cm.__aenter__ = mock.AsyncMock(return_value=mock_client)
  mock_cm.__aexit__ = mock.AsyncMock(return_value=None)

  with mock.patch("gti_mcp.tools.agentic.vt_client", return_value=mock_cm):
    timeout_data = await _call_json_tool(
        "ask_gti_agent", {"message": "Long investigation"}
    )
  assert "error" in timeout_data
  assert "timed out" in timeout_data["error"].lower()
