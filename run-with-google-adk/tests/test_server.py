"""Unit tests for mcp_security_agent.server."""

import sys
import unicodedata
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
    assert "user" in data
    assert bool(data["user"])


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
    assert "user_id" in data
    assert bool(data["user_id"])



def test_get_session_with_username():
    client = TestClient(create_app())
    response = client.get("/get_session", params={"username": "alice"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "alice"


class MockRunner:
    async def run_async(self, *args, **kwargs):
        from google.adk.events import Event
        from google.genai import types
        yield Event(
            author="SecurityOperationsAgent",
            content=types.Content(role="model", parts=[types.Part(text="Mocked analysis response")]),
        )


def test_chat_post():
    from unittest.mock import patch
    with patch("mcp_security_agent.server.routes.get_runner", return_value=MockRunner()):
        client = TestClient(create_app())
        response = client.post("/chat", json={"prompt": "Investigate alert 123", "session_id": "test-sess"})
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "Mocked analysis response" in data["response"]
        assert data["session_id"] == "test-sess"


def test_chat_sse_stream():
    from unittest.mock import patch
    with patch("mcp_security_agent.server.routes.get_runner", return_value=MockRunner()):
        client = TestClient(create_app())
        response = client.get("/chat", params={"message": "check finding", "session_id": "test-sess"})
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        assert "Mocked analysis response" in response.text
        assert "Stream finished." in response.text


def test_login_and_alias_routes():
    client = TestClient(create_app())
    for path in ["/login", "/index.html", "/landing.html", "/chat.html"]:
        response = client.get(path)
        assert response.status_code == 200


def test_chat_post_sse_streaming():
    from unittest.mock import patch
    with patch("mcp_security_agent.server.routes.get_runner", return_value=MockRunner()):
        client = TestClient(create_app())
        response = client.post("/chat", json={"message": "Investigate alert 123", "session_id": "test-sess"})
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        assert "Mocked analysis response" in response.text
        assert "Stream finished." in response.text



def test_no_cache_headers():
    client = TestClient(create_app())
    for path in ["/", "/login", "/landing.html", "/index.html"]:
        response = client.get(path)
        assert response.status_code == 200
        assert "no-store" in response.headers.get("cache-control", "")
        assert "no-cache" in response.headers.get("pragma", "")


def test_favicon():
    client = TestClient(create_app())
    response = client.get("/favicon.ico")
    assert response.status_code == 204


def test_static_assets():
    client = TestClient(create_app())
    for path in ["/static/app.css", "/static/app.js"]:
        response = client.get(path)
        assert response.status_code == 200
        assert "no-store" in response.headers.get("cache-control", "")


def test_index_html_no_emojis():
    client = TestClient(create_app())
    response = client.get("/index.html")
    assert response.status_code == 200
    html = response.text
    for char in html:
        code = ord(char)
        if (code > 0x2000 and unicodedata.category(char) in ("So", "Sk", "Sm", "Cn")) or code > 0x1F000 or (0x2600 <= code <= 0x27BF):
            assert char in ("`", "^", "~", "<", ">", "+", "=", "|", "•"), f"Unexpected emoji/symbol: {char!r} (U+{code:04X})"
    assert "<svg" in html



