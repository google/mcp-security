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
        response = client.post(
            "/chat",
            json={"message": "Investigate alert 123", "session_id": "test-sess"},
            headers={"accept": "text/event-stream"},
        )
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


def test_no_emojis_in_web_app_and_stream():
    client = TestClient(create_app())
    for path in ["/", "/index.html", "/static/app.js", "/static/app.css"]:
        resp = client.get(path)
        assert resp.status_code == 200
        for char in resp.text:
            code = ord(char)
            if (code > 0x2000 and unicodedata.category(char) in ("So", "Sk", "Sm", "Cn")) or code > 0x1F000 or (0x2600 <= code <= 0x27BF):
                assert char in ("`", "^", "~", "<", ">", "+", "=", "|", "•"), f"Unexpected emoji/symbol in {path}: {char!r} (U+{code:04X})"

    from unittest.mock import patch
    with patch("mcp_security_agent.server.routes.get_runner", return_value=None):
        resp = client.get("/chat", params={"message": "hello"})
        assert resp.status_code == 200
        assert "[Warning]" in resp.text
        for char in resp.text:
            code = ord(char)
            if (code > 0x2000 and unicodedata.category(char) in ("So", "Sk", "Sm", "Cn")) or code > 0x1F000 or (0x2600 <= code <= 0x27BF):
                assert char in ("`", "^", "~", "<", ">", "+", "=", "|", "•"), f"Unexpected emoji/symbol in stream: {char!r}"


def test_scroll_and_layout_constraints():
    client = TestClient(create_app())
    resp = client.get("/static/app.css")
    assert resp.status_code == 200
    css = resp.text

    # Ensure body is constrained to viewport height to avoid pushing input offscreen
    assert "max-height: 100vh" in css or "height: 100vh" in css
    # Ensure layout and workspace flex items allow shrinking
    assert "min-height: 0" in css
    # Ensure messages container scrolls vertically
    assert "overflow-y: auto" in css
    # Ensure custom scrollbar rules are defined for visibility
    assert "scrollbar-width: thin" in css
    assert "::-webkit-scrollbar" in css


def test_bounded_session_service_eviction():
    from mcp_security_agent.server.routes import BoundedSessionService

    service = BoundedSessionService(max_sessions=10)

    import asyncio
    async def run_test():
        # Test eviction within single user
        for i in range(12):
            await service.create_session(
                app_name="test_app",
                user_id="user",
                session_id=f"sess_{i}",
            )
        assert len(service._session_order) == 10
        user_sessions = service.sessions["test_app"]["user"]
        assert len(user_sessions) == 10
        assert "sess_0" not in user_sessions
        assert "sess_1" not in user_sessions
        assert "sess_10" in user_sessions
        assert "sess_11" in user_sessions

        # Test eviction across distinct users and empty user dict pruning
        multi_service = BoundedSessionService(max_sessions=5)
        for i in range(8):
            await multi_service.create_session(
                app_name="test_app",
                user_id=f"user_{i}",
                session_id=f"sess_{i}",
            )
        assert len(multi_service._session_order) == 5
        # Users 0, 1, 2 should be completely evicted and pruned from test_app dict
        assert "user_0" not in multi_service.sessions["test_app"]
        assert "user_1" not in multi_service.sessions["test_app"]
        assert "user_2" not in multi_service.sessions["test_app"]
        # Users 3..7 should remain
        for i in range(3, 8):
            assert f"user_{i}" in multi_service.sessions["test_app"]

        # Test explicit session deletion and empty dict cleanup
        await multi_service.delete_session(
            app_name="test_app",
            user_id="user_7",
            session_id="sess_7",
        )
        assert "user_7" not in multi_service.sessions["test_app"]

    asyncio.run(run_test())


def test_get_runner_agent_creation():
    from unittest.mock import patch, MagicMock
    import mcp_security_agent.server.routes as server_routes
    import mcp_security_agent.agent as agent_mod

    # Reset globals for test isolation
    original_runner = server_routes._runner
    original_root = getattr(agent_mod, "_root_agent", None)
    try:
        server_routes._runner = None
        agent_mod._root_agent = None

        mock_agent = MagicMock()
        with patch("mcp_security_agent.agent.create_security_agent", return_value=mock_agent) as mock_create, \
             patch("mcp_security_agent.server.routes.Runner") as mock_runner_cls:
            runner = server_routes.get_runner()
            assert runner is not None
            mock_create.assert_called_once()
            assert agent_mod._root_agent is mock_agent
    finally:
        server_routes._runner = original_runner
        agent_mod._root_agent = original_root


def test_dompurify_xss_protection():
    client = TestClient(create_app())
    html = client.get("/index.html").text
    js = client.get("/static/app.js").text

    # Verify DOMPurify is loaded in HTML before marked/app.js
    assert "dompurify" in html
    # Verify app.js defines renderMarkdown and uses DOMPurify.sanitize
    assert "DOMPurify.sanitize" in js
    assert "renderMarkdown" in js
    # Verify fail-closed behavior if DOMPurify is not available
    assert "failing closed to escaped text" in js


def test_frontend_streaming_abort_on_reset():
    client = TestClient(create_app())
    js = client.get("/static/app.js").text

    assert "cancelStreaming" in js
    # Verify newInvestigationBtn and saveUser call cancelStreaming when isStreaming is true
    assert "newInvestigationBtn.addEventListener" in js
    assert "if (isStreaming) {\n      cancelStreaming();\n    }\n    messagesContainer.innerHTML = '';" in js
    assert "if (isStreaming) {\n      cancelStreaming();\n    }\n    currentUserId = newName;" in js


def test_bounded_session_service_thread_safe_lookups():
    from mcp_security_agent.server.routes import BoundedSessionService
    from google.adk.events import Event
    from google.genai import types

    service = BoundedSessionService(max_sessions=5)

    import asyncio
    async def run_test():
        sess = await service.create_session(
            app_name="test_app",
            user_id="alice",
            session_id="sess_1",
        )
        assert sess is not None

        # Test get_session and list_sessions
        retrieved = await service.get_session(app_name="test_app", user_id="alice", session_id="sess_1")
        assert retrieved is not None
        assert retrieved.id == "sess_1"

        sessions_list = await service.list_sessions(app_name="test_app", user_id="alice")
        assert len(sessions_list.sessions) == 1

        # Test append_event on existing session
        test_event = Event(
            author="SecurityOperationsAgent",
            content=types.Content(role="model", parts=[types.Part(text="Test event")]),
        )
        appended = await service.append_event(sess, test_event)
        assert appended == test_event

        # Test append_event on non-existent / evicted session does not crash
        dummy_sess = type("DummySession", (), {"app_name": "test_app", "user_id": "bob", "id": "sess_gone"})()
        result_evicted = await service.append_event(dummy_sess, test_event)
        assert result_evicted == test_event

    asyncio.run(run_test())

