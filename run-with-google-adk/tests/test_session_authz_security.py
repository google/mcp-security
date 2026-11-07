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
"""Security tests for session authorization, identity binding, and IAP verification."""

import base64
import json
from pathlib import Path
import sys
import time
from typing import Any, List, Optional, Tuple
from unittest.mock import patch
import uuid

from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient
import jwt
from jwt.algorithms import ECAlgorithm
import pytest

src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.server.app import create_app
from mcp_security_agent.server.auth import SESSION_COOKIE_NAME, SessionAuthManager


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


class MockJwksRequest:
    """Mock HTTP transport returning a JWKS key set for ES256 IAP verification."""

    def __init__(self, jwks_json: str) -> None:
        self.jwks_json = jwks_json

    def __call__(self, url: str, method: str = "GET", body: Any = None, headers: Any = None, timeout: Any = None):
        class MockResponse:
            status = 200
            data = self.jwks_json.encode("utf-8")

        return MockResponse()


# Test Suite 1: Two-client IDOR PoC reproduction & GET /chat removal
def test_two_client_idor_poc_blocks_cross_user_and_unauthenticated_chat(monkeypatch):
    """Reproduces reporter amitu314's two-client IDOR PoC and verifies HTTP 403 and 405."""
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)
    monkeypatch.delenv("MCP_AGENT_REQUIRE_IAP", raising=False)
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

        # GET /chat was removed to prevent query-string token and prompt leaks -> 405
        get_chat_resp = client_a.get(
            "/chat",
            params={
                "session_id": ident_b["session_id"],
                "user_id": ident_b["user_id"],
                "message": "PoC: GET chat attempt",
            },
        )
        assert get_chat_resp.status_code == 405

        # Client A attempting SSE streaming into Client B's session via POST /chat -> 403
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

        # Client B can legitimately use its own session -> 200
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


# Test Suite 2: Session fixation blocked & strict identifier validation
def test_session_fixation_and_identifier_validation(monkeypatch):
    """Verifies unissued valid UUIDv4 is rejected with 403, and invalid identifiers with 400."""
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)
    monkeypatch.delenv("MCP_AGENT_REQUIRE_IAP", raising=False)
    app = create_app()
    client = TestClient(app)

    # 1. Attacker generates their own valid UUIDv4 and tries to inject it without an issued cookie
    unissued_uuid = str(uuid.uuid4())
    resp_fixation = client.post(
        "/chat",
        json={"session_id": unissued_uuid, "prompt": "inject session"},
    )
    assert resp_fixation.status_code == 403

    # 2. Non-UUID format for session_id -> 400
    for bad_sid in ["case-1042", "../admin", "12345", "not-a-uuid", str(uuid.uuid4()).upper()]:
        resp_bad_sid = client.post(
            "/chat",
            json={"session_id": bad_sid, "prompt": "test"},
        )
        assert resp_bad_sid.status_code == 400

    # 3. Invalid usernames on /get_session -> 400
    for bad_user in [".", "..", "user/evil", "user\\evil", "alice bob", "alice\ninjected", "a" * 129]:
        resp_bad_user = client.get("/get_session", params={"username": bad_user})
        assert resp_bad_user.status_code == 400


# Test Suite 3: UI operator switch & stale cookie recovery
def test_operator_switch_and_stale_cookie_recovery(monkeypatch):
    """Verifies switching operator name mints a fresh capability cookie, avoiding lockouts."""
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)
    monkeypatch.delenv("MCP_AGENT_REQUIRE_IAP", raising=False)
    monkeypatch.setenv("MCP_AGENT_SESSION_SECRET", "operator-switch-secret-key-0123456789")

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        app = create_app()
        client = TestClient(app)

        # 1. Operator starts as alice
        resp1 = client.get("/get_session", params={"username": "alice"})
        assert resp1.status_code == 200
        sess1 = resp1.json()
        assert sess1["user_id"] == "alice"
        sid1 = sess1["session_id"]

        # Alice chats successfully
        r_chat1 = client.post("/chat", json={"session_id": sid1, "prompt": "alice query"})
        assert r_chat1.status_code == 200

        # 2. Operator switches username in UI modal to bob -> succeeds with fresh cookie and session
        resp2 = client.get("/get_session", params={"username": "bob"})
        assert resp2.status_code == 200
        sess2 = resp2.json()
        assert sess2["user_id"] == "bob"
        sid2 = sess2["session_id"]
        assert sid2 != sid1

        # Bob chats successfully with new session
        r_chat2 = client.post("/chat", json={"session_id": sid2, "prompt": "bob query"})
        assert r_chat2.status_code == 200

        # But bob's client cannot access alice's old session (sid1) -> 403
        r_cross = client.post("/chat", json={"session_id": sid1, "prompt": "bob accessing alice session"})
        assert r_cross.status_code == 403

        # 3. Browser restart / distinct client requesting the same username succeeds (no squatting lockout)
        fresh_browser = TestClient(app)
        resp_alice_restart = fresh_browser.get("/get_session", params={"username": "alice"})
        assert resp_alice_restart.status_code == 200
        assert resp_alice_restart.json()["user_id"] == "alice"

        # 4. Server secret reload / rotated secret recovery: stale cookie on /get_session mints fresh valid cookie
        stale_client = TestClient(app)
        resp_stale = stale_client.get(
            "/get_session",
            headers={"Cookie": f"{SESSION_COOKIE_NAME}=stale.cookie.signature"},
        )
        assert resp_stale.status_code == 200
        assert SESSION_COOKIE_NAME in resp_stale.cookies
        stale_data = resp_stale.json()

        # Follow-up chat with the recovered cookie succeeds
        stale_client.cookies.set(SESSION_COOKIE_NAME, resp_stale.cookies[SESSION_COOKIE_NAME])
        r_recovered = stale_client.post(
            "/chat",
            json={"session_id": stale_data["session_id"], "prompt": "recovered"},
        )
        assert r_recovered.status_code == 200

        # 5. Tampered cookie on stateful /chat without prior session recovery fails closed with 403
        tampered_client = TestClient(app)
        r_tampered = tampered_client.post(
            "/chat",
            json={"session_id": str(uuid.uuid4()), "user_id": "alice", "prompt": "attack"},
            headers={"Cookie": f"{SESSION_COOKIE_NAME}=forged.signature"},
        )
        assert r_tampered.status_code == 403


# Test Suite 4: Stateless single-turn REST API and stateful follow-up
def test_stateless_single_turn_and_stateful_followup(monkeypatch):
    """Verifies unauthenticated curl/REST single-turn chat succeeds, while targeted spoofing fails."""
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)
    monkeypatch.delenv("MCP_AGENT_REQUIRE_IAP", raising=False)

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        app = create_app()

        # 1. Stateless single-turn POST /chat without cookies or explicit IDs -> 200, sets signed cookie
        client = TestClient(app)
        resp = client.post("/chat", json={"prompt": "Investigate CVE-2026-1042"})
        assert resp.status_code == 200
        data = resp.json()
        assert "response" in data
        assert "Authorized response" in data["response"]
        assert "session_id" in data
        sid = data["session_id"]
        assert SESSION_COOKIE_NAME in client.cookies

        # 2. Stateful follow-up turn in that minted session succeeds
        followup = client.post("/chat", json={"session_id": sid, "prompt": "Next step"})
        assert followup.status_code == 200
        assert followup.json()["session_id"] == sid

        # 3. But unauthenticated request targeting a specific victim user_id without cookie fails -> 403
        unauth_target = TestClient(app)
        r_target = unauth_target.post(
            "/chat",
            json={"user_id": "victim", "prompt": "spoofed user query"},
        )
        assert r_target.status_code == 403


# Test Suite 5: Browser CSRF & Same-Origin protection
def test_same_origin_csrf_protection(monkeypatch):
    """Verifies Sec-Fetch-Site and Origin header checks block cross-origin requests with 403."""
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)
    monkeypatch.delenv("MCP_AGENT_REQUIRE_IAP", raising=False)
    app = create_app()
    client = TestClient(app, base_url="http://localhost:8080")

    # 1. Sec-Fetch-Site checks
    # cross-site -> 403
    r_cross_site = client.get("/get_session", headers={"Sec-Fetch-Site": "cross-site"})
    assert r_cross_site.status_code == 403

    # same-site -> 403
    r_same_site = client.get("/get_session", headers={"Sec-Fetch-Site": "same-site"})
    assert r_same_site.status_code == 403

    # same-origin -> 200
    r_same_origin = client.get("/get_session", headers={"Sec-Fetch-Site": "same-origin"})
    assert r_same_origin.status_code == 200

    # none (browser navigation / direct) -> 200
    r_none = client.get("/get_session", headers={"Sec-Fetch-Site": "none"})
    assert r_none.status_code == 200

    # 2. Origin header checks
    # Mismatched origin -> 403
    r_evil_origin = client.get("/get_session", headers={"Origin": "https://evil.example.com"})
    assert r_evil_origin.status_code == 403

    # Origin null (sandboxed iframe) -> 403
    r_null_origin = client.get("/get_session", headers={"Origin": "null"})
    assert r_null_origin.status_code == 403

    # Matching origin -> 200
    r_good_origin = client.get("/get_session", headers={"Origin": "http://localhost:8080"})
    assert r_good_origin.status_code == 200


# Test Suite 6: Cookie security flags
def test_cookie_security_flags_httponly_samesite_and_conditional_secure(monkeypatch):
    """Verifies HttpOnly, SameSite=Lax, and conditional Secure cookie attributes."""
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)
    monkeypatch.delenv("MCP_AGENT_REQUIRE_IAP", raising=False)
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

    # Reverse-proxy X-Forwarded-Proto: https on external host -> includes Secure
    proxy_client = TestClient(app, base_url="http://secops-agent.corp.example.com")
    r_proxy = proxy_client.get(
        "/get_session",
        headers={"X-Forwarded-Proto": "https, http", "Host": "secops-agent.corp.example.com"},
    )
    assert r_proxy.status_code == 200
    set_cookie_proxy = r_proxy.headers.get("set-cookie", "")
    assert "Secure" in set_cookie_proxy


# Test Suite 7: Cryptographic IAP JWT verification
def test_iap_cryptographic_jwt_verification(monkeypatch):
    """Verifies cryptographic ES256 IAP token validation, rejection of unsigned headers, and multi-replica."""
    audience = "/projects/123456789/global/backendServices/987654321"
    monkeypatch.setenv("MCP_AGENT_IAP_AUDIENCE", audience)
    monkeypatch.setenv("MCP_AGENT_REQUIRE_IAP", "true")

    # Generate an EC P-256 keypair for testing
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    kid = "iap-test-key-2026"

    jwk_dict = json.loads(ECAlgorithm.to_jwk(public_key))
    jwk_dict["kid"] = kid
    jwk_dict["alg"] = "ES256"
    jwk_dict["use"] = "sig"
    mock_request = MockJwksRequest(json.dumps({"keys": [jwk_dict]}))

    def make_token(
        email: str = "alice@example.com",
        aud: str = audience,
        iss: str = "https://cloud.google.com/iap",
        expired: bool = False,
        alg: str = "ES256",
        key_id: Optional[str] = kid,
    ) -> str:
        now = int(time.time())
        exp = now - 60 if expired else now + 3600
        claims = {
            "iss": iss,
            "aud": aud,
            "exp": exp,
            "iat": now - 10,
            "sub": "100200300400",
            "email": email,
        }
        headers = {}
        if key_id:
            headers["kid"] = key_id
        if alg == "HS256":
            return jwt.encode(claims, "symmetric-secret-key-123456789012", algorithm="HS256", headers=headers)
        return jwt.encode(claims, private_key, algorithm=alg, headers=headers)

    runner = RecordingRunner()
    with patch("mcp_security_agent.server.routes.get_runner", return_value=runner):
        app = create_app()
        # Inject our mock transport for hermetic JWKS retrieval
        app.state.session_auth = SessionAuthManager(http_request=mock_request)
        client = TestClient(app)

        # 1. /healthz remains accessible without IAP headers for Cloud Run probes
        assert client.get("/healthz").status_code == 200

        # 2. Unsigned X-Goog-Authenticated-User-Email is completely ignored -> 401
        spoof_resp = client.get(
            "/get_session",
            headers={"X-Goog-Authenticated-User-Email": "accounts.google.com:victim@example.com"},
        )
        assert spoof_resp.status_code == 401

        # 3. Missing X-Goog-Iap-Jwt-Assertion header -> 401
        assert client.get("/get_session").status_code == 401
        assert client.get("/info").status_code == 401
        assert client.post("/chat", json={"prompt": "hi"}).status_code == 401

        # 4. Malformed JWT header or missing kid -> 401
        no_kid_token = make_token(key_id=None)
        assert client.get("/get_session", headers={"X-Goog-Iap-Jwt-Assertion": no_kid_token}).status_code == 401

        # 5. Unsupported algorithm (e.g. HS256) -> 401
        hs_token = make_token(alg="HS256")
        assert client.get("/get_session", headers={"X-Goog-Iap-Jwt-Assertion": hs_token}).status_code == 401

        # 6. Wrong audience -> 401
        wrong_aud_token = make_token(aud="/projects/999/global/backendServices/wrong")
        assert client.get("/get_session", headers={"X-Goog-Iap-Jwt-Assertion": wrong_aud_token}).status_code == 401

        # 7. Wrong issuer -> 401
        wrong_iss_token = make_token(iss="https://accounts.google.com")
        assert client.get("/get_session", headers={"X-Goog-Iap-Jwt-Assertion": wrong_iss_token}).status_code == 401

        # 8. Expired token -> 401
        expired_token = make_token(expired=True)
        assert client.get("/get_session", headers={"X-Goog-Iap-Jwt-Assertion": expired_token}).status_code == 401

        # 9. Valid ES256 IAP token for Alice -> 200
        alice_token = make_token(email="accounts.google.com:alice@example.com")
        alice_headers = {"X-Goog-Iap-Jwt-Assertion": alice_token}

        info_resp = client.get("/info", headers=alice_headers)
        assert info_resp.status_code == 200
        assert info_resp.json()["user"] == "alice@example.com"

        sess_resp = client.get("/get_session", headers=alice_headers)
        assert sess_resp.status_code == 200
        alice_sess = sess_resp.json()
        assert alice_sess["user_id"] == "alice@example.com"
        alice_sid = alice_sess["session_id"]

        # Alice chats successfully
        chat_resp = client.post(
            "/chat",
            json={"session_id": alice_sid, "prompt": "analyze alert"},
            headers=alice_headers,
        )
        assert chat_resp.status_code == 200
        assert runner.calls == [("alice@example.com", alice_sid)]

        # 10. Bob attempting to access Alice's session behind IAP -> 403
        bob_token = make_token(email="bob@example.com")
        bob_headers = {"X-Goog-Iap-Jwt-Assertion": bob_token}
        bob_idor = client.post(
            "/chat",
            json={"session_id": alice_sid, "user_id": "bob@example.com", "prompt": "hijack alice"},
            headers=bob_headers,
        )
        assert bob_idor.status_code == 403

        # 11. Multi-replica IAP with shared secret: Replica 2 validates cookie and token -> 200
        monkeypatch.setenv("MCP_AGENT_SESSION_SECRET", "iap-shared-replica-secret-1234567890")
        app_rep1 = create_app()
        app_rep1.state.session_auth = SessionAuthManager(http_request=mock_request)
        client_rep1 = TestClient(app_rep1)

        rep1_sess = client_rep1.get("/get_session", headers=alice_headers).json()
        cookie_val = client_rep1.cookies.get(SESSION_COOKIE_NAME)

        app_rep2 = create_app()
        app_rep2.state.session_auth = SessionAuthManager(http_request=mock_request)
        client_rep2 = TestClient(app_rep2)
        client_rep2.cookies.set(SESSION_COOKIE_NAME, cookie_val)

        rep2_chat = client_rep2.post(
            "/chat",
            json={"session_id": rep1_sess["session_id"], "prompt": "turn on replica 2"},
            headers=alice_headers,
        )
        assert rep2_chat.status_code == 200
        assert rep2_chat.json()["session_id"] == rep1_sess["session_id"]


def test_iap_require_iap_without_audience_fails_closed(monkeypatch):
    """Verifies fail-closed 500 error when MCP_AGENT_REQUIRE_IAP is True but audience is unconfigured."""
    monkeypatch.setenv("MCP_AGENT_REQUIRE_IAP", "true")
    monkeypatch.delenv("MCP_AGENT_IAP_AUDIENCE", raising=False)

    app = create_app()
    client = TestClient(app)

    # When require_iap is True and audience is None, requests to protected endpoints return 500
    resp = client.get("/get_session")
    assert resp.status_code == 500
    assert "MCP_AGENT_IAP_AUDIENCE must be configured" in resp.text
