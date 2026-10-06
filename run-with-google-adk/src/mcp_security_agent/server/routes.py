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
"""REST and SSE endpoints for FastAPI server and Cloud Run deployments."""

import json
import uuid
import asyncio
import logging
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Dict, Any, Optional, AsyncGenerator
from fastapi import APIRouter, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import mcp_security_agent.agent as agent_mod
from mcp_security_agent import __version__
from mcp_security_agent.config import AgentSettings, discover_user_identity

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: Optional[str] = None
    message: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@router.get("/")
@router.get("/index.html")
@router.get("/landing.html")
@router.get("/chat.html")
@router.get("/login")
def get_root():
    """Serves the unified investigation console of the web UI."""
    pkg_root = Path(__file__).resolve().parents[3]
    index_file = pkg_root / "static" / "index.html"
    if index_file.is_file():
        return FileResponse(str(index_file))
    return JSONResponse({"status": "ok", "message": "MCP Security Agent API is running."})



@router.get("/healthz")
def health_check() -> Dict[str, str]:
    """Health check endpoint for Cloud Run and Kubernetes probes."""
    return {"status": "ok"}


@router.get("/favicon.ico")
def get_favicon():
    """Returns 204 No Content for browser favicon requests."""
    return Response(status_code=204)


@router.get("/app_name")
def get_app_name() -> Dict[str, str]:
    """Returns the application display name for the Web UI navbar."""
    return {"app_name": "Google Security Agent"}


@router.get("/get_session")
def get_session(username: Optional[str] = Query(None, description="Username for session")) -> Dict[str, str]:
    """Generates a session ID and returns user context for chat sessions."""
    detected_user = discover_user_identity()
    user = username if (username and username.strip() and username != "secops_user") else detected_user
    return {
        "session_id": str(uuid.uuid4()),
        "user_id": user,
    }


_settings: Optional[AgentSettings] = None
_settings_lock = threading.Lock()


def get_settings() -> AgentSettings:
    """Returns cached AgentSettings singleton to avoid redundant env parsing."""
    global _settings
    if _settings is None:
        with _settings_lock:
            if _settings is None:
                _settings = AgentSettings()
    return _settings


@router.get("/info")
def get_info() -> Dict[str, Any]:
    """Provides server runtime metadata, active user identity, and enabled MCP server status."""
    settings = get_settings()
    return {
        "version": __version__,
        "model": settings.google_model,
        "user": discover_user_identity(),
        "tools": {
            "secops": settings.load_secops_mcp,
            "scc": settings.load_scc_mcp,
            "gti": settings.load_gti_mcp,
            "soar": settings.load_secops_soar_mcp,
        },
    }


class BoundedSessionService(InMemorySessionService):
    """InMemorySessionService with FIFO session eviction to prevent unbounded memory growth."""

    def __init__(self, max_sessions: int = 1000):
        super().__init__()
        self.max_sessions = max_sessions
        self._session_order: OrderedDict = OrderedDict()
        self._lock = threading.RLock()

    def _create_session_impl(
        self,
        *,
        app_name: str,
        user_id: str,
        state: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> Any:
        with self._lock:
            while len(self._session_order) >= self.max_sessions:
                (old_app, old_user, old_sess), _ = self._session_order.popitem(last=False)
                if old_app in self.sessions and old_user in self.sessions[old_app]:
                    self.sessions[old_app][old_user].pop(old_sess, None)
                    if not self.sessions[old_app][old_user]:
                        self.sessions[old_app].pop(old_user, None)
                if old_app in self.sessions and not self.sessions[old_app]:
                    self.sessions.pop(old_app, None)
            sess = super()._create_session_impl(
                app_name=app_name,
                user_id=user_id,
                state=state,
                session_id=session_id,
            )
            self._session_order[(app_name, user_id, sess.id)] = True
            return sess

    def _get_session_impl(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        config: Optional[Any] = None,
    ) -> Optional[Any]:
        with self._lock:
            return super()._get_session_impl(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                config=config,
            )

    def _list_sessions_impl(
        self,
        *,
        app_name: str,
        user_id: Optional[str] = None,
    ) -> Any:
        with self._lock:
            return super()._list_sessions_impl(
                app_name=app_name,
                user_id=user_id,
            )

    async def append_event(self, session: Any, event: Any) -> Any:
        with self._lock:
            app_name = getattr(session, "app_name", None)
            user_id = getattr(session, "user_id", None)
            session_id = getattr(session, "id", None)
            if (
                not app_name
                or not user_id
                or not session_id
                or app_name not in self.sessions
                or user_id not in self.sessions[app_name]
                or session_id not in self.sessions[app_name][user_id]
            ):
                return event
            return await super().append_event(session=session, event=event)

    def _delete_session_impl(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
    ) -> None:
        with self._lock:
            self._session_order.pop((app_name, user_id, session_id), None)
            super()._delete_session_impl(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
            )
            if app_name in self.sessions and user_id in self.sessions[app_name]:
                if not self.sessions[app_name][user_id]:
                    self.sessions[app_name].pop(user_id, None)
            if app_name in self.sessions and not self.sessions[app_name]:
                self.sessions.pop(app_name, None)


_runner: Optional[Runner] = None
_runner_lock = threading.Lock()
_session_service: Optional[BoundedSessionService] = None


def get_session_service() -> BoundedSessionService:
    """Returns the singleton BoundedSessionService for active chat sessions."""
    global _session_service
    if _session_service is None:
        with _runner_lock:
            if _session_service is None:
                _session_service = BoundedSessionService(max_sessions=1000)
    return _session_service


def get_runner() -> Optional[Runner]:
    """Returns or initializes the thread-safe ADK Runner instance for the security agent."""
    global _runner
    if _runner is None:
        with _runner_lock:
            if _runner is None:
                settings = get_settings()
                agent = getattr(agent_mod, "_root_agent", None)
                if agent is None:
                    agent = agent_mod.create_security_agent(settings)
                    agent_mod._root_agent = agent
                if agent is None:
                    return None
                session_svc = get_session_service()
                _runner = Runner(
                    agent=agent,
                    app_name="mcp_security_agent",
                    session_service=session_svc,
                )
    return _runner


async def sse_event_generator(
    message: str,
    session_id: str,
    user_id: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    """Streams real ADK agent execution events over Server-Sent Events (SSE)."""
    uid = user_id or discover_user_identity()
    session_svc = get_session_service()
    runner = get_runner()

    if runner is None:
        err_msg = json.dumps({
            "text": "[Warning] Agent runner is unavailable in this environment.",
            "last_msg": False,
            "session_id": session_id,
        })
        yield f"data: {err_msg}\n\n"
        done_msg = json.dumps({"text": "Stream finished.", "last_msg": True, "session_id": session_id})
        yield f"data: {done_msg}\n\n"
        return

    session = await session_svc.get_session(
        app_name="mcp_security_agent",
        user_id=uid,
        session_id=session_id,
    )
    if not session:
        session = await session_svc.create_session(
            app_name="mcp_security_agent",
            user_id=uid,
            session_id=session_id,
        )

    content = types.Content(role="user", parts=[types.Part(text=message)])

    try:
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        data = json.dumps({
                            "text": part.text,
                            "last_msg": False,
                            "session_id": session_id,
                            "author": event.author or "SecurityOperationsAgent",
                            "event_type": "content",
                        })
                        yield f"data: {data}\n\n"
                    elif part.function_call:
                        call_info = json.dumps({
                            "text": f"[Tool] **Calling tool `{part.function_call.name}`**\n```json\n{json.dumps(part.function_call.args, indent=2)}\n```",
                            "last_msg": False,
                            "session_id": session_id,
                            "event_type": "tool_call",
                        })
                        yield f"data: {call_info}\n\n"
                    elif part.function_response:
                        resp_info = json.dumps({
                            "text": f"[Tool] **Received tool response from `{part.function_response.name}`**",
                            "last_msg": False,
                            "session_id": session_id,
                            "event_type": "tool_response",
                        })
                        yield f"data: {resp_info}\n\n"
    except asyncio.CancelledError:
        logger.info(f"SSE client disconnected for session {session_id}")
        raise
    except Exception as e:
        logger.error(f"Error during agent execution: {e}", exc_info=True)
        err_data = json.dumps({
            "text": f"[Error] **Error during investigation:** {str(e)}",
            "last_msg": False,
            "session_id": session_id,
            "event_type": "error",
        })
        yield f"data: {err_data}\n\n"

    done_data = json.dumps({
        "text": "Stream finished.",
        "last_msg": True,
        "session_id": session_id,
    })
    yield f"data: {done_data}\n\n"


@router.get("/chat")
async def chat_sse_stream(
    message: str = Query(..., description="User prompt or security alert query"),
    session_id: Optional[str] = Query(None, description="Session ID for conversation history"),
    user_id: Optional[str] = Query(None, description="Active user ID"),
):
    """Server-Sent Events (SSE) streaming endpoint for web UI clients."""
    sess_id = session_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_event_generator(message, sess_id, user_id),
        media_type="text/event-stream",
    )


@router.post("/chat", response_model=ChatResponse)
async def chat_post(request: ChatRequest, http_request: Request):
    """REST and SSE chat endpoint for API clients, automated workflows, and web UI."""
    sess_id = request.session_id or str(uuid.uuid4())
    query_text = request.message or request.prompt or ""
    uid = request.user_id or discover_user_identity()

    accept_header = http_request.headers.get("accept", "")
    if "text/event-stream" in accept_header:
        return StreamingResponse(
            sse_event_generator(query_text, sess_id, uid),
            media_type="text/event-stream",
        )

    # For non-streaming REST queries, collect text parts from runner
    accumulated = []
    async for chunk_str in sse_event_generator(query_text, sess_id, uid):
        if chunk_str.startswith("data: "):
            try:
                data = json.loads(chunk_str[6:].strip())
                if not data.get("last_msg") and data.get("text"):
                    accumulated.append(data["text"])
            except Exception:
                pass

    response_text = "\n\n".join(accumulated) if accumulated else f"No response generated for: {query_text}"
    return JSONResponse(
        content={
            "response": response_text,
            "session_id": sess_id,
        }
    )

