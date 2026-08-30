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
from pathlib import Path
from typing import Dict, Any, Optional, AsyncGenerator
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel
from mcp_security_agent import __version__
from mcp_security_agent.config import AgentSettings

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@router.get("/")
def get_root():
    """Serves the main landing page of the web UI."""
    pkg_root = Path(__file__).resolve().parents[3]
    landing_file = pkg_root / "static" / "landing.html"
    index_file = pkg_root / "static" / "index.html"
    
    if landing_file.is_file():
        return FileResponse(str(landing_file))
    elif index_file.is_file():
        return FileResponse(str(index_file))
    return JSONResponse({"status": "ok", "message": "MCP Security Agent API is running."})


@router.get("/healthz")
def health_check() -> Dict[str, str]:
    """Health check endpoint for Cloud Run and Kubernetes probes."""
    return {"status": "ok"}


@router.get("/get_session")
def get_session() -> Dict[str, str]:
    """Generates a new session ID for chat sessions."""
    return {"session_id": str(uuid.uuid4())}


@router.get("/info")
def get_info() -> Dict[str, Any]:
    """Provides server runtime metadata and enabled MCP server status."""
    settings = AgentSettings()
    return {
        "version": __version__,
        "model": settings.google_model,
        "tools": {
            "secops": settings.load_secops_mcp,
            "scc": settings.load_scc_mcp,
            "gti": settings.load_gti_mcp,
            "soar": settings.load_secops_soar_mcp,
        },
    }


async def sse_event_generator(message: str, session_id: str) -> AsyncGenerator[str, None]:
    """Mock/stream response generator for SSE streaming."""
    # Yield initial ack
    ack_data = json.dumps({"text": f"Investigating: {message}", "last_msg": False, "session_id": session_id})
    yield f"data: {ack_data}\n\n"
    await asyncio.sleep(0.05)
    
    # Yield completion
    done_data = json.dumps({"text": "Stream finished.", "last_msg": True, "session_id": session_id})
    yield f"data: {done_data}\n\n"


@router.get("/chat")
async def chat_sse_stream(
    message: str = Query(..., description="User prompt or security alert query"),
    session_id: Optional[str] = Query(None, description="Session ID for conversation history"),
):
    """Server-Sent Events (SSE) streaming endpoint for web UI clients."""
    sess_id = session_id or str(uuid.uuid4())
    return StreamingResponse(
        sse_event_generator(message, sess_id),
        media_type="text/event-stream",
    )


@router.post("/chat", response_model=ChatResponse)
def chat_post(request: ChatRequest) -> ChatResponse:
    """REST JSON chat endpoint for API clients and automated workflows."""
    sess_id = request.session_id or str(uuid.uuid4())
    return ChatResponse(
        response=f"Received query: {request.prompt}",
        session_id=sess_id,
    )
