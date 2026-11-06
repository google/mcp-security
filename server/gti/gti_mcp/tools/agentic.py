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
import typing

import aiohttp
from mcp.server.fastmcp import Context
import vt

from .. import utils
from ..server import server, vt_client


logger = logging.getLogger(__name__)

__all__ = [
    "ask_gti_agent",
    "continue_chat",
    "copy_shared_session",
    "delete_session",
    "get_session_history",
    "list_sessions",
    "share_session",
]

_CONVERSATION_MESSAGE_TYPES = frozenset({
    "USER_MESSAGE",
    "AGENT_FINAL_RESPONSE",
})


def _build_message_form(message: str) -> aiohttp.FormData:
  """Builds a multipart/form-data payload required by /agentspace/sessions."""
  form = aiohttp.FormData(default_to_multipart=True)
  form.add_field("message", message)
  return form


async def _handle_error_response(
    client: vt.Client,
    response: vt.ClientResponse,
    operation: str,
) -> typing.Dict[str, typing.Any]:
  """Extracts a structured error dictionary from a non-2xx response."""
  api_error = await client.get_error_async(response)
  if api_error is not None:
    logger.warning(
        "GTI Agentic API error during %s: %s - %s",
        operation,
        api_error.code,
        api_error.message,
    )
    return {
        "error": f"VirusTotal API Error: {api_error.code} - {api_error.message}"
    }

  body_text = await response.text_async()
  logger.warning(
      "Unexpected HTTP %s during %s: %s", response.status, operation, body_text
  )
  return {"error": f"Unexpected HTTP {response.status} during {operation}."}


def _format_session_turn(
    payload: typing.Dict[str, typing.Any],
    fallback_session_id: typing.Optional[str] = None,
) -> typing.Dict[str, typing.Any]:
  """Extracts the synthesized agent answer, citations, and widgets for a turn."""
  data = payload.get("data", {}) if isinstance(payload, dict) else {}
  if not isinstance(data, dict):
    data = {}
  attributes = data.get("attributes", {})
  if not isinstance(attributes, dict):
    attributes = {}

  session_id = data.get("id") or fallback_session_id
  events = attributes.get("events", [])
  if not isinstance(events, list):
    events = []

  markdown_chunks: list[str] = []
  extra_widgets: list[typing.Dict[str, typing.Any]] = []
  citations: list[typing.Any] = []
  agent_id: typing.Optional[str] = None

  final_event = None
  for event in reversed(events):
    if isinstance(event, dict) and event.get("message_type") == "AGENT_FINAL_RESPONSE":
      final_event = event
      break

  if final_event is not None:
    final_body = final_event.get("agent_final_response", {})
    if isinstance(final_body, dict):
      agent_id = final_body.get("agent_id")
      for cite_key in ("gti_citations", "citations"):
        raw_cites = final_body.get(cite_key)
        if isinstance(raw_cites, list):
          citations.extend(raw_cites)

      widgets = final_body.get("widgets", [])
      if isinstance(widgets, list):
        for widget in widgets:
          if not isinstance(widget, dict):
            continue
          if widget.get("widget_type") == "MARKDOWN_TEXT":
            md_widget = widget.get("markdown_text_widget", {})
            if isinstance(md_widget, dict):
              text = md_widget.get("text", "")
              if isinstance(text, str) and text.strip():
                markdown_chunks.append(text.strip())
              for cite_key in ("gti_citations", "citations"):
                widget_cites = md_widget.get(cite_key)
                if isinstance(widget_cites, list):
                  citations.extend(widget_cites)
          else:
            extra_widgets.append(widget)

  result: typing.Dict[str, typing.Any] = {
      "session_id": session_id,
      "title": attributes.get("title"),
      "creation_date": attributes.get("creation_date"),
      "last_modification_date": attributes.get("last_modification_date"),
      "response": "\n\n".join(markdown_chunks),
  }
  if agent_id:
    result["agent_id"] = agent_id
  if citations:
    result["citations"] = citations
  if extra_widgets:
    result["widgets"] = extra_widgets

  return utils.sanitize_response(result)


@server.tool()
async def ask_gti_agent(
    message: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Start a new autonomous investigation session with the GTI Agentic analyst.

  Delegates multi-step threat intelligence and malware analysis questions to
  Google Threat Intelligence specialist agents and returns the synthesized
  markdown response, citations, structured widgets, and `session_id` for
  follow-up questions via `continue_chat`.

  Args:
    message (required): Initial investigation question, indicator(s), or prompt.

  Returns:
    Dictionary containing `session_id`, `title`, `response`, and optional
    `citations`, `widgets`, and `agent_id`.
  """
  try:
    async with vt_client(ctx) as client:
      response = await client.post_async(
          "/agentspace/sessions", data=_build_message_form(message)
      )
      if not 200 <= response.status < 300:
        return await _handle_error_response(client, response, "ask_gti_agent")
      header_session_id = response.headers.get("X-Session-Id")
      payload = await response.json_async()
    return _format_session_turn(payload, fallback_session_id=header_session_id)
  except (asyncio.TimeoutError, TimeoutError) as err:
    logger.warning("GTI Agentic session timed out in ask_gti_agent: %s", err)
    return {
        "error": (
            "The GTI Agentic investigation request timed out. Try narrowing"
            " the prompt or checking list_sessions for the created session."
        )
    }
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error in ask_gti_agent: %s - %s", err.code, err.message
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error("Unexpected error in ask_gti_agent: %s", err, exc_info=True)
    return {"error": f"Unexpected error in ask_gti_agent: {err}"}


@server.tool()
async def continue_chat(
    session_id: str, message: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Send a follow-up message to an existing GTI Agentic investigation session.

  Preserves conversation context and prior findings accumulated in `session_id`.

  Args:
    session_id (required): Session identifier returned by `ask_gti_agent`,
      `list_sessions`, or `copy_shared_session`.
    message (required): Follow-up question or instruction for the GTI agent.

  Returns:
    Dictionary containing `session_id`, `title`, `response`, and optional
    `citations`, `widgets`, and `agent_id`.
  """
  try:
    async with vt_client(ctx) as client:
      response = await client.post_async(
          f"/agentspace/sessions/{session_id}",
          data=_build_message_form(message),
      )
      if not 200 <= response.status < 300:
        return await _handle_error_response(client, response, "continue_chat")
      payload = await response.json_async()
    return _format_session_turn(payload, fallback_session_id=session_id)
  except (asyncio.TimeoutError, TimeoutError) as err:
    logger.warning(
        "GTI Agentic session %s timed out in continue_chat: %s", session_id, err
    )
    return {
        "error": (
            f"The GTI Agentic follow-up request on session '{session_id}'"
            " timed out. Check get_session_history for updated state."
        )
    }
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error in continue_chat for %s: %s - %s",
        session_id,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error in continue_chat for %s: %s",
        session_id,
        err,
        exc_info=True,
    )
    return {"error": f"Unexpected error in continue_chat: {err}"}


@server.tool()
async def list_sessions(
    ctx: Context,
    limit: int = 5,
    order: typing.Optional[str] = None,
    filter: typing.Optional[str] = None,  # pylint: disable=redefined-builtin
    cursor: typing.Optional[str] = None,
) -> typing.Dict[str, typing.Any]:
  """List GTI Agentic investigation sessions for the authenticated user.

  Args:
    limit: Maximum number of sessions to return per page (default 5).
    order: Optional sort order parameter.
    filter: Optional filter expression.
    cursor: Optional pagination cursor from a previous `list_sessions` call.

  Returns:
    Dictionary containing `sessions` summaries and optional pagination `cursor`.
  """
  raw_params = {
      "limit": limit,
      "order": order,
      "filter": filter,
      "cursor": cursor,
  }
  params = {k: v for k, v in raw_params.items() if v is not None and v != ""}

  try:
    async with vt_client(ctx) as client:
      response = await client.get_async("/agentspace/sessions", params=params)
      if not 200 <= response.status < 300:
        return await _handle_error_response(client, response, "list_sessions")
      payload = await response.json_async()
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error in list_sessions: %s - %s", err.code, err.message
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error("Unexpected error in list_sessions: %s", err, exc_info=True)
    return {"error": f"Unexpected error in list_sessions: {err}"}

  raw_items = payload.get("data", []) if isinstance(payload, dict) else []
  sessions = []
  if isinstance(raw_items, list):
    for item in raw_items:
      if not isinstance(item, dict):
        continue
      attrs = item.get("attributes", {})
      if not isinstance(attrs, dict):
        attrs = {}
      summary = {
          "id": item.get("id"),
          "type": item.get("type", "agentic_session"),
          "title": attrs.get("title"),
          "creation_date": attrs.get("creation_date"),
          "last_modification_date": attrs.get("last_modification_date"),
      }
      sessions.append(summary)

  result: typing.Dict[str, typing.Any] = {"sessions": sessions}
  meta = payload.get("meta", {}) if isinstance(payload, dict) else {}
  if isinstance(meta, dict):
    next_cursor = meta.get("cursor")
    if next_cursor:
      result["cursor"] = next_cursor
    if meta:
      result["meta"] = meta
  return utils.sanitize_response(result)


@server.tool()
async def get_session_history(
    session_id: str,
    ctx: Context,
    include_intermediate_events: bool = False,
) -> typing.Dict[str, typing.Any]:
  """Retrieve the conversation history for a GTI Agentic session.

  By default, only `USER_MESSAGE` and `AGENT_FINAL_RESPONSE` events are
  returned so multi-turn transcripts remain compact. Set
  `include_intermediate_events=True` to include `AGENT_THOUGHT`,
  `FUNCTION_CALL`, and `FUNCTION_RESPONSE` trace events.

  Args:
    session_id (required): Unique identifier of the GTI Agentic session.
    include_intermediate_events: Include internal thought and tool call events.
      Defaults to False.

  Returns:
    Dictionary containing `session_id`, `title`, timestamps, and `events`.
  """
  try:
    async with vt_client(ctx) as client:
      response = await client.get_async(f"/agentspace/sessions/{session_id}")
      if not 200 <= response.status < 300:
        return await _handle_error_response(
            client, response, "get_session_history"
        )
      payload = await response.json_async()
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error in get_session_history for %s: %s - %s",
        session_id,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error in get_session_history for %s: %s",
        session_id,
        err,
        exc_info=True,
    )
    return {"error": f"Unexpected error in get_session_history: {err}"}

  data = payload.get("data", {}) if isinstance(payload, dict) else {}
  if not isinstance(data, dict):
    data = {}
  attrs = data.get("attributes", {})
  if not isinstance(attrs, dict):
    attrs = {}

  events = attrs.get("events", [])
  if not isinstance(events, list):
    events = []
  if not include_intermediate_events:
    events = [
        event
        for event in events
        if isinstance(event, dict)
        and event.get("message_type") in _CONVERSATION_MESSAGE_TYPES
    ]

  result = {
      "session_id": data.get("id", session_id),
      "type": data.get("type", "agentic_session"),
      "title": attrs.get("title"),
      "creation_date": attrs.get("creation_date"),
      "last_modification_date": attrs.get("last_modification_date"),
      "events": events,
  }
  return utils.sanitize_response(result)


@server.tool()
async def delete_session(
    session_id: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Delete a GTI Agentic investigation session by ID.

  Args:
    session_id (required): Unique identifier of the session to delete.

  Returns:
    Confirmation dictionary `{"deleted": True, "session_id": ...}` or an error.
  """
  try:
    async with vt_client(ctx) as client:
      response = await client.delete_async(f"/agentspace/sessions/{session_id}")
      if not 200 <= response.status < 300:
        return await _handle_error_response(client, response, "delete_session")
      body_bytes = await response.read_async()
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error deleting session %s: %s - %s",
        session_id,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error deleting session %s: %s",
        session_id,
        err,
        exc_info=True,
    )
    return {"error": f"Unexpected error deleting session: {err}"}

  result: typing.Dict[str, typing.Any] = {
      "deleted": True,
      "session_id": session_id,
  }
  if body_bytes and body_bytes.strip():
    try:
      parsed = json.loads(body_bytes)
      if isinstance(parsed, dict) and isinstance(parsed.get("data"), dict):
        for key, value in parsed["data"].items():
          if value is not None:
            result.setdefault(key, value)
    except ValueError:
      pass
  return result


@server.tool()
async def share_session(
    session_id: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Generate a share token for a GTI Agentic session so another user can clone it.

  Args:
    session_id (required): Unique identifier of the session to share.

  Returns:
    Dictionary containing `session_id` and `share_token`.
  """
  try:
    async with vt_client(ctx) as client:
      response = await client.get_async(
          f"/agentspace/sessions/{session_id}/token"
      )
      if not 200 <= response.status < 300:
        return await _handle_error_response(client, response, "share_session")
      payload = await response.json_async()
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error sharing session %s: %s - %s",
        session_id,
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error sharing session %s: %s",
        session_id,
        err,
        exc_info=True,
    )
    return {"error": f"Unexpected error sharing session: {err}"}

  share_token: typing.Optional[str] = None
  if isinstance(payload, dict):
    data = payload.get("data")
    if isinstance(data, str):
      share_token = data
    elif isinstance(data, dict):
      share_token = (
          data.get("token")
          or data.get("share_token")
          or data.get("attributes", {}).get("token")
          or data.get("id")
      )
    if not share_token:
      share_token = payload.get("token") or payload.get("share_token")

  result: typing.Dict[str, typing.Any] = {
      "session_id": session_id,
      "share_token": share_token,
  }
  return utils.sanitize_response(result)


@server.tool()
async def copy_shared_session(
    share_token: str, ctx: Context
) -> typing.Dict[str, typing.Any]:
  """Clone a shared GTI Agentic session into the caller's workspace from a token.

  Args:
    share_token (required): Share token produced by `share_session` or a shared
      GTI Agentic session link.

  Returns:
    Cloned session summary with the new `session_id`, `title`, and latest
    `response`.
  """
  try:
    async with vt_client(ctx) as client:
      response = await client.post_async(
          "/agentspace/sessions/token", json_data={"token": share_token}
      )
      if not 200 <= response.status < 300:
        return await _handle_error_response(
            client, response, "copy_shared_session"
        )
      header_session_id = response.headers.get("X-Session-Id")
      payload = await response.json_async()
    return _format_session_turn(payload, fallback_session_id=header_session_id)
  except vt.error.APIError as err:
    logger.warning(
        "VirusTotal API error copying shared session: %s - %s",
        err.code,
        err.message,
    )
    return {"error": f"VirusTotal API Error: {err.code} - {err.message}"}
  except Exception as err:  # pylint: disable=broad-exception-caught
    logger.error(
        "Unexpected error copying shared session: %s", err, exc_info=True
    )
    return {"error": f"Unexpected error copying shared session: {err}"}
