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
"""Security tests for session authorization and principal binding (GHSA-vp7x-22c6-v566)."""

import base64
import json
import os
from pathlib import Path
import sys
from typing import List, Tuple
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.server.app import create_app
from mcp_security_agent.server.auth import SESSION_COOKIE_NAME


class RecordingRunner:
    """Mock ADK runner that records authorized invocations."""

    def __init__(self) -> None:
        self.calls: List[Tuple[str, str]] = []

    async def run_async(self, *args, **kwargs):
        from google.adk.events import Event
        from google.genai import types

        self.calls.append((kwargs.get("user_id", ""), kwargs.get("session_id", "")))
        yield Event(
            author="SecurityOperationsAgent",
            content=types.Content(
                role="model",
                parts=[types.Part(text="Authorized response")],
            ),
        )


def test_two_client_idor_poc_blocks_cross_user_and_unauthenticated_chat(monkeypatch):
    """Reproduces reporter amitu314's two-client IDOR PoC and verifies HTTP 403."""
    monkeypatch.delenv("MCP_AGENT_TRUST_AUTH_HEADERS", raising=False)
    monkeypatch.delenv("MCP_AGENT_SESSION_SECRET", raising=False)

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        app = create_app()
        client_a = TestClient(app)
        client_b = TestClient(app)
        client_c = TestClient(app)

        resp_a = client_a.get("/get_session", params={"username": "poc-user-a"})
        assert resp_a.status_code == 200
        ident_a = resp_a.json()
        assert ident_a["user_id"] == "poc-user-a"
        assert SESSION_COOKIE_NAME in client_a.cookies

        resp_b = client_b.get("/get_session", params={"username": "poc-user-b"})
        assert resp_b.status_code == 200
        ident_b = resp_b.json()
        assert ident_b["user_id"] == "poc-user-b"
        assert ident_a["session_id"] != ident_b["session_id"]
        assert SESSION_COOKIE_NAME in client_b.cookies

        # Unauthenticated third client (exact poc_idor.py requests.post without cookie) -> 403
        unauth_post = client_c.post(
            "/chat",
            json={
                "session_id": ident_b["session_id"],
                "user_id": ident_b["user_id"],
                "message": "PoC: benign read-only authorization test, please ignore.",
            },
        )
        assert unauth_post.status_code == 403

        # Client A attempting to post into Client B's session with Client B's user_id -> 403
        cross_user_post = client_a.post(
            "/chat",
            json={
                "session_id": ident_b["session_id"],
                "user_id": ident_b["user_id"],
                "message": "PoC: cross-user IDOR attempt",
            },
        )
        assert cross_user_post.status_code == 403

        # Client A attempting to post into Client B's session with Client A's own user_id -> 403
        cross_session_post = client_a.post(
            "/chat",
            json={
                "session_id": ident_b["session_id"],
                "user_id": ident_a["user_id"],
                "message": "PoC: cross-session IDOR attempt",
            },
        )
        assert cross_session_post.status_code == 403

        # Client A attempting SSE streaming into Client B's session via GET /chat and POST /chat -> 403
        cross_sse_get = client_a.get(
            "/chat",
            params={
                "session_id": ident_b["session_id"],
                "user_id": ident_b["user_id"],
                "message": "PoC: SSE IDOR attempt",
            },
        )
        assert cross_sse_get.status_code == 403

        cross_sse_post = client_a.post(
            "/chat",
            json={
                "session_id": ident_b["session_id"],
                "user_id": ident_b["user_id"],
                "message": "PoC: POST SSE IDOR attempt",
            },
            headers={"accept": "text/event-stream"},
        )
        assert cross_sse_post.status_code == 403

        # Verify runner was never invoked during any unauthorized attempt
        assert runner.calls == []

        # Client B can still legitimately use its own session -> 200
        ok_b = client_b.post(
            "/chat",
            json={
                "session_id": ident_b["session_id"],
                "user_id": ident_b["user_id"],
                "message": "Legitimate investigation query",
            },
        )
        assert ok_b.status_code == 200
        assert runner.calls == [("poc-user-b", ident_b["session_id"])]


def test_get_session_prevents_identity_switching_and_duplicate_username_hijack(monkeypatch):
    """Verifies /get_session blocks mid-session username switching and cross-client username hijack."""
    monkeypatch.delenv("MCP_AGENT_TRUST_AUTH_HEADERS", raising=False)

    app = create_app()
    client_a = TestClient(app)
    client_b = TestClient(app)

    first = client_a.get("/get_session", params={"username": "poc-user-a"})
    assert first.status_code == 200

    # Same client holding cookie for poc-user-a cannot switch to poc-user-b -> 403
    switch_resp = client_a.get("/get_session", params={"username": "poc-user-b"})
    assert switch_resp.status_code == 403

    # Distinct cookie-less client cannot claim already-bound poc-user-a -> 403
    hijack_resp = client_b.get("/get_session", params={"username": "poc-user-a"})
    assert hijack_resp.status_code == 403

    # Same client requesting start_new_session=Y for its own bound username succeeds -> 200
    renew_resp = client_a.get(
        "/get_session",
        params={"username": "poc-user-a", "start_new_session": "Y"},
    )
    assert renew_resp.status_code == 200
    assert renew_resp.json()["user_id"] == "poc-user-a"
    assert renew_resp.json()["session_id"] != first.json()["session_id"]


def test_missing_or_tampered_hmac_cookie_rejected_with_403(monkeypatch):
    """Verifies missing cookies, tampered signatures, and forged payloads fail closed with 403."""
    monkeypatch.delenv("MCP_AGENT_TRUST_AUTH_HEADERS", raising=False)
    monkeypatch.setenv("MCP_AGENT_SESSION_SECRET", "unit-test-hmac-secret-key-0123456789")

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        app = create_app()

        # 1. Missing cookie on POST /chat and GET /chat -> 403
        no_cookie_client = TestClient(app)
        assert no_cookie_client.post("/chat", json={"prompt": "test"}).status_code == 403
        assert no_cookie_client.get("/chat", params={"message": "test"}).status_code == 403

        # 2. Obtain valid session cookie, then tamper with signature
        valid_client = TestClient(app)
        sess = valid_client.get("/get_session", params={"username": "analyst-a"}).json()
        raw_token = valid_client.cookies.get(SESSION_COOKIE_NAME)
        assert raw_token is not None
        payload_b64, sig_b64 = raw_token.split(".")

        flipped_char = "A" if sig_b64[-1] != "A" else "B"
        tampered_sig_token = f"{payload_b64}.{sig_b64[:-1]}{flipped_char}"

        tampered_client = TestClient(app)
        tampered_client.cookies.set(SESSION_COOKIE_NAME, tampered_sig_token)
        assert (
            tampered_client.post(
                "/chat",
                json={
                    "session_id": sess["session_id"],
                    "user_id": "analyst-a",
                    "message": "test",
                },
            ).status_code
            == 403
        )
        assert tampered_client.get("/get_session").status_code == 403

        # 3. Tamper with payload JSON (change uid to analyst-b while keeping signature)
        forged_payload = json.dumps(
            {"v": 1, "cid": "forged-cid", "uid": "analyst-b", "sids": [sess["session_id"]]},
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        forged_b64 = base64.urlsafe_b64encode(forged_payload).decode("ascii").rstrip("=")
        forged_token = f"{forged_b64}.{sig_b64}"

        forged_client = TestClient(app)
        forged_client.cookies.set(SESSION_COOKIE_NAME, forged_token)
        assert (
            forged_client.post(
                "/chat",
                json={
                    "session_id": sess["session_id"],
                    "user_id": "analyst-b",
                    "message": "test",
                },
            ).status_code
            == 403
        )

        # 4. Malformed cookie values -> 403
        for malformed in ["not-a-valid-token", "a.b.c", ".sigonly", "payloadonly."]:
            bad_client = TestClient(app)
            bad_client.cookies.set(SESSION_COOKIE_NAME, malformed)
            assert bad_client.post("/chat", json={"prompt": "test"}).status_code == 403

        # 5. Arbitrary unissued session_id with valid cookie -> 403
        assert (
            valid_client.post(
                "/chat",
                json={
                    "session_id": "unissued-arbitrary-session",
                    "user_id": "analyst-a",
                    "message": "test",
                },
            ).status_code
            == 403
        )
        assert runner.calls == []


def test_cookie_security_flags_httponly_samesite_and_conditional_secure(monkeypatch):
    """Verifies HttpOnly, SameSite=Lax, and conditional Secure cookie attributes."""
    monkeypatch.delenv("MCP_AGENT_TRUST_AUTH_HEADERS", raising=False)
    app = create_app()

    # Plain HTTP request -> HttpOnly and SameSite=lax, no Secure attribute
    http_client = TestClient(app, base_url="http://testserver")
    r_http = http_client.get("/get_session")
    assert r_http.status_code == 200
    set_cookie_http = r_http.headers.get("set-cookie", "")
    assert "HttpOnly" in set_cookie_http
    assert "SameSite=lax" in set_cookie_http
    assert "; Secure" not in set_cookie_http

    # Direct HTTPS request -> includes Secure
    https_client = TestClient(app, base_url="https://testserver")
    r_https = https_client.get("/get_session")
    assert r_https.status_code == 200
    set_cookie_https = r_https.headers.get("set-cookie", "")
    assert "HttpOnly" in set_cookie_https
    assert "SameSite=lax" in set_cookie_https
    assert "Secure" in set_cookie_https

    # Reverse-proxy X-Forwarded-Proto: https -> includes Secure
    proxy_client = TestClient(app, base_url="http://testserver")
    r_proxy = proxy_client.get("/get_session", headers={"X-Forwarded-Proto": "https, http"})
    assert r_proxy.status_code == 200
    set_cookie_proxy = r_proxy.headers.get("set-cookie", "")
    assert "Secure" in set_cookie_proxy


def test_unauthenticated_header_spoofing_ignored_by_default(monkeypatch):
    """Ensures X-Goog-Authenticated-User-Email is ignored unless MCP_AGENT_TRUST_AUTH_HEADERS=true."""
    monkeypatch.setenv("MCP_AGENT_TRUST_AUTH_HEADERS", "false")

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner), \
         patch("mcp_security_agent.server.auth.discover_user_identity", return_value="local_operator"):
        app = create_app()
        spoofer = TestClient(app)

        # Forged IAP header on /get_session must not set user_id to victim@example.com
        r_sess = spoofer.get(
            "/get_session",
            headers={"X-Goog-Authenticated-User-Email": "accounts.google.com:victim@example.com"},
        )
        assert r_sess.status_code == 200
        assert r_sess.json()["user_id"] == "local_operator"

        # Forged IAP header on /chat without valid cookie must still fail closed -> 403
        raw_spoofer = TestClient(app)
        r_chat = raw_spoofer.post(
            "/chat",
            json={
                "session_id": r_sess.json()["session_id"],
                "user_id": "local_operator",
                "message": "forged header bypass attempt",
            },
            headers={"X-Goog-Authenticated-User-Email": "accounts.google.com:local_operator"},
        )
        assert r_chat.status_code == 403
        assert runner.calls == []


def test_trusted_auth_headers_iap_mode_enforced(monkeypatch):
    """Verifies IAP / Cloud Run principal binding when MCP_AGENT_TRUST_AUTH_HEADERS=true."""
    monkeypatch.setenv("MCP_AGENT_TRUST_AUTH_HEADERS", "true")

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        app = create_app()
        unauth_client = TestClient(app)

        # Missing X-Goog-Authenticated-User-Email fails closed with 401
        assert unauth_client.get("/get_session").status_code == 401
        assert unauth_client.post("/chat", json={"prompt": "hi"}).status_code == 401
        assert unauth_client.get("/chat", params={"message": "hi"}).status_code == 401
        assert unauth_client.get("/info").status_code == 401

        # Blank or malformed IAP headers fail closed with 401
        for bad_hdr in ["   ", "accounts.google.com:", "accounts.google.com:a@x.com, accounts.google.com:b@x.com"]:
            assert (
                unauth_client.get(
                    "/get_session",
                    headers={"X-Goog-Authenticated-User-Email": bad_hdr},
                ).status_code
                == 401
            )

        # /healthz remains reachable for Cloud Run liveness probes
        assert unauth_client.get("/healthz").status_code == 200

        # Valid IAP header strips accounts.google.com: prefix and binds principal
        alice_headers = {"X-Goog-Authenticated-User-Email": "accounts.google.com:alice@example.com"}
        bob_headers = {"X-Goog-Authenticated-User-Email": "accounts.google.com:bob@example.com"}

        alice_client = TestClient(app)
        bob_client = TestClient(app)

        info_resp = alice_client.get("/info", headers=alice_headers)
        assert info_resp.status_code == 200
        assert info_resp.json()["user"] == "alice@example.com"

        alice_sess = alice_client.get("/get_session", headers=alice_headers)
        assert alice_sess.status_code == 200
        alice_data = alice_sess.json()
        assert alice_data["user_id"] == "alice@example.com"

        # Mismatched username query param on /get_session -> 403
        mismatch_sess = alice_client.get(
            "/get_session",
            params={"username": "bob@example.com"},
            headers=alice_headers,
        )
        assert mismatch_sess.status_code == 403

        # Mismatched user_id body on /chat -> 403
        mismatch_chat = alice_client.post(
            "/chat",
            json={
                "session_id": alice_data["session_id"],
                "user_id": "bob@example.com",
                "message": "impersonate bob",
            },
            headers=alice_headers,
        )
        assert mismatch_chat.status_code == 403

        # Cross-user session IDOR behind IAP (Bob trying to use Alice's session_id) -> 403
        bob_idor = bob_client.post(
            "/chat",
            json={
                "session_id": alice_data["session_id"],
                "user_id": "bob@example.com",
                "message": "hijack alice session",
            },
            headers=bob_headers,
        )
        assert bob_idor.status_code == 403

        # Legitimate IAP request from Alice -> 200
        alice_ok = alice_client.post(
            "/chat",
            json={
                "session_id": alice_data["session_id"],
                "user_id": "alice@example.com",
                "message": "triage alert 42",
            },
            headers=alice_headers,
        )
        assert alice_ok.status_code == 200
        assert runner.calls == [("alice@example.com", alice_data["session_id"])]


def test_legitimate_browser_and_multi_replica_flow(monkeypatch):
    """Verifies end-to-end browser workflow including start_new_session=Y and multi-replica secret."""
    monkeypatch.delenv("MCP_AGENT_TRUST_AUTH_HEADERS", raising=False)
    monkeypatch.setenv("MCP_AGENT_SESSION_SECRET", "shared-replica-secret-key-9876543210")

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        replica_1 = create_app()
        replica_2 = create_app()

        browser = TestClient(replica_1)

        # Verify frontend uses same-origin fetch so cookies flow automatically
        js = browser.get("/static/app.js").text
        assert "window.location.origin" in js
        assert "fetch(`${API_BASE_URL}/get_session`" in js or "let url = `${API_BASE_URL}/get_session`" in js
        assert "fetch(`${API_BASE_URL}/chat`" in js

        # Step 1: Initial /get_session on replica 1
        s1_resp = browser.get("/get_session")
        assert s1_resp.status_code == 200
        s1 = s1_resp.json()
        cookie_val = browser.cookies.get(SESSION_COOKIE_NAME)
        assert cookie_val is not None

        # Step 2: Stream chat on replica 1
        chat1 = browser.post(
            "/chat",
            json={"session_id": s1["session_id"], "user_id": s1["user_id"], "message": "first turn"},
            headers={"accept": "text/event-stream"},
        )
        assert chat1.status_code == 200
        assert "Authorized response" in chat1.text

        # Step 3: Start new investigation session (start_new_session=Y)
        s2_resp = browser.get(
            "/get_session",
            params={"username": s1["user_id"], "start_new_session": "Y"},
        )
        assert s2_resp.status_code == 200
        s2 = s2_resp.json()
        assert s2["user_id"] == s1["user_id"]
        assert s2["session_id"] != s1["session_id"]
        updated_cookie = browser.cookies.get(SESSION_COOKIE_NAME)

        # Step 4: Route next /chat request to replica 2 using shared MCP_AGENT_SESSION_SECRET
        browser_on_replica_2 = TestClient(replica_2)
        browser_on_replica_2.cookies.set(SESSION_COOKIE_NAME, updated_cookie)
        chat2 = browser_on_replica_2.post(
            "/chat",
            json={"session_id": s2["session_id"], "user_id": s2["user_id"], "message": "second turn"},
        )
        assert chat2.status_code == 200
        assert chat2.json()["session_id"] == s2["session_id"]

        # Step 5: Omitting session_id with valid cookie auto-mints an owned session usable on follow-up
        auto_chat = browser.post("/chat", json={"prompt": "auto session turn 1"})
        assert auto_chat.status_code == 200
        auto_sid = auto_chat.json()["session_id"]
        followup = browser.post("/chat", json={"session_id": auto_sid, "prompt": "auto session turn 2"})
        assert followup.status_code == 200
        assert followup.json()["session_id"] == auto_sid


@pytest.mark.parametrize(
    "bad_identifier",
    [
        ".",
        "..",
        "../admin",
        "foo/../bar",
        "foo..bar",
        "user/evil",
        "user\\evil",
        "user?role=admin",
        "user#frag",
        "user%2f..",
        "//evil.host",
        "user{0}",
        "alice bob",
        "alice\ninjected",
        "   ",
        "a" * 129,
    ],
)
def test_identifier_format_and_length_bounds(monkeypatch, bad_identifier):
    """Verifies malformed username, user_id, and session_id inputs are rejected with HTTP 400."""
    monkeypatch.delenv("MCP_AGENT_TRUST_AUTH_HEADERS", raising=False)
    app = create_app()
    client = TestClient(app)

    # Malformed username on /get_session -> 400
    r_user = client.get("/get_session", params={"username": bad_identifier})
    assert r_user.status_code == 400

    # Valid session setup for /chat parameter validation checks
    valid_sess = client.get("/get_session").json()

    r_chat_uid = client.post(
        "/chat",
        json={
            "session_id": valid_sess["session_id"],
            "user_id": bad_identifier,
            "message": "test",
        },
    )
    assert r_chat_uid.status_code == 400

    r_chat_sid = client.post(
        "/chat",
        json={
            "session_id": bad_identifier,
            "user_id": valid_sess["user_id"],
            "message": "test",
        },
    )
    assert r_chat_sid.status_code == 400
