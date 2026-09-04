"""Unit tests for mcp_security_agent.server."""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.server.app import create_app


def test_healthz():
    client = TestClient(create_app())
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_name():
    client = TestClient(create_app())
    response = client.get("/app_name")
    assert response.status_code == 200
    assert response.json() == {"app_name": "Google Security Agent"}


def test_info():
    client = TestClient(create_app())
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.2.0"
    assert "tools" in data


def test_root():
    client = TestClient(create_app())
    response = client.get("/")
    assert response.status_code == 200


def test_get_session_default():
    client = TestClient(create_app())
    response = client.get("/get_session")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert len(data["session_id"]) > 10
    assert data["user_id"] == "default_user"


def test_get_session_with_username():
    client = TestClient(create_app())
    response = client.get("/get_session", params={"username": "alice"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "alice"


def test_chat_post():
    client = TestClient(create_app())
    response = client.post("/chat", json={"prompt": "Investigate alert 123", "session_id": "test-sess"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == "test-sess"


def test_chat_sse_stream():
    client = TestClient(create_app())
    response = client.get("/chat", params={"message": "check finding", "session_id": "test-sess"})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert "data:" in response.text
