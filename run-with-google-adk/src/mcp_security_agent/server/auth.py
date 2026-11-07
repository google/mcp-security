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
"""Session capability signing and principal authorization for the web server."""

import base64
from collections import OrderedDict
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import threading
import urllib.parse
import uuid
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException, Request, Response
import google.auth.transport.requests
import google.oauth2.id_token
import jwt

from mcp_security_agent.config import AgentSettings, discover_user_identity

logger = logging.getLogger(__name__)

SESSION_COOKIE_NAME = "mcp_agent_session"
_COOKIE_VERSION = 1
_MAX_COOKIE_LENGTH = 4096
_MAX_COOKIE_SESSIONS = 32
_MAX_TRACKED_SESSIONS = 4096
_IAP_EMAIL_PREFIX = "accounts.google.com:"
_IAP_CERTS_URL = "https://www.gstatic.com/iap/verify/public_key-jwk"
_IAP_EXPECTED_ISSUER = "https://cloud.google.com/iap"
_TRUTHY_VALUES = frozenset({"Y", "YES", "TRUE", "1"})
_START_NEW_VALUES = frozenset({"Y", "N", "YES", "NO", "TRUE", "FALSE", "1", "0", ""})

_USER_ID_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._@+-]{0,127}\Z")

_fallback_lock = threading.Lock()


def is_valid_user_id(value: Any) -> bool:
    """Validates user_id / username format and length bounds."""
    if not isinstance(value, str) or len(value) < 1 or len(value) > 128 or ".." in value:
        return False
    return bool(_USER_ID_RE.fullmatch(value))


def is_valid_session_id(value: Any) -> bool:
    """Validates that session_id is a strict canonical lowercase UUIDv4 string."""
    if not isinstance(value, str) or len(value) != 36:
        return False
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        return False
    return parsed.version == 4 and str(parsed) == value


def is_https_request(request: Request) -> bool:
    """Determines whether the request arrived over HTTPS directly or via proxy."""
    if request.url.scheme.lower() == "https":
        return True
    host = request.headers.get("host", "").split(":")[0].strip().lower()
    if host in ("localhost", "127.0.0.1", "testserver"):
        return False
    forwarded_proto = request.headers.get("x-forwarded-proto", "")
    if forwarded_proto:
        first_hop = forwarded_proto.split(",")[0].strip().lower()
        if first_hop == "https":
            return True
    return False


def is_iap_mode_enabled(settings: Optional[AgentSettings] = None) -> bool:
    """Checks whether Identity-Aware Proxy (IAP) enforcement is configured."""
    raw_aud = os.environ.get("MCP_AGENT_IAP_AUDIENCE")
    if raw_aud is not None and raw_aud.strip():
        return True
    raw_req = os.environ.get("MCP_AGENT_REQUIRE_IAP")
    if raw_req is not None and raw_req.strip().upper() in _TRUTHY_VALUES:
        return True
    if settings is not None:
        if settings.iap_audience and settings.iap_audience.strip():
            return True
        if settings.require_iap:
            return True
    return False


def get_iap_audience(settings: Optional[AgentSettings] = None) -> Optional[str]:
    """Retrieves the configured IAP audience string from environment or settings."""
    raw = os.environ.get("MCP_AGENT_IAP_AUDIENCE")
    if raw is not None and raw.strip():
        return raw.strip()
    if settings is not None and settings.iap_audience and settings.iap_audience.strip():
        return settings.iap_audience.strip()
    return None


def verify_same_origin(request: Request, settings: Optional[AgentSettings] = None) -> None:
    """Enforces browser same-origin semantics via Sec-Fetch-Site and Origin headers."""
    sec_fetch_site = request.headers.get("sec-fetch-site")
    if sec_fetch_site:
        clean_site = sec_fetch_site.strip().lower()
        if clean_site not in ("same-origin", "none"):
            logger.warning("Blocked cross-origin request with Sec-Fetch-Site: %s", clean_site)
            raise HTTPException(status_code=403, detail="Cross-origin request blocked.")

    origin = request.headers.get("origin")
    if origin is not None:
        clean_origin = origin.strip()
        if clean_origin.lower() == "null":
            logger.warning("Blocked cross-origin request with Origin: null")
            raise HTTPException(status_code=403, detail="Cross-origin request blocked.")
        try:
            parsed = urllib.parse.urlsplit(clean_origin)
        except Exception:
            logger.warning("Blocked request with unparseable Origin header: %s", clean_origin)
            raise HTTPException(status_code=403, detail="Cross-origin request blocked.")

        if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
            logger.warning("Blocked request with invalid Origin scheme/netloc: %s", clean_origin)
            raise HTTPException(status_code=403, detail="Cross-origin request blocked.")

        target_host = ""
        if is_iap_mode_enabled(settings):
            f_host = request.headers.get("x-forwarded-host")
            if f_host:
                target_host = f_host.split(",")[0].strip().lower()
        if not target_host:
            target_host = request.headers.get("host", "").strip().lower()

        if not target_host or parsed.netloc.lower() != target_host:
            logger.warning(
                "Blocked cross-origin request: origin %s does not match host %s",
                parsed.netloc,
                target_host,
            )
            raise HTTPException(status_code=403, detail="Cross-origin request blocked.")


def _safe_default_user() -> str:
    """Resolves local default identity with fallback if invalid characters appear."""
    detected = discover_user_identity()
    return detected if is_valid_user_id(detected) else "secops_user"


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(segment: str) -> Optional[bytes]:
    if not segment or not segment.isascii():
        return None
    padding = "=" * (-len(segment) % 4)
    try:
        return base64.urlsafe_b64decode((segment + padding).encode("ascii"))
    except Exception:
        return None


class SessionAuthManager:
    """Manages HMAC-SHA256 session cookies and server-side ownership bindings."""

    def __init__(
        self,
        max_sessions: int = _MAX_TRACKED_SESSIONS,
        http_request: Optional[Any] = None,
    ) -> None:
        self._ephemeral_secret: bytes = secrets.token_bytes(32)
        self._max_sessions = max_sessions
        self._session_owners: "OrderedDict[str, Tuple[str, str]]" = OrderedDict()
        self._lock = threading.RLock()
        self._http_request = http_request or google.auth.transport.requests.Request()

    def _get_secret_bytes(self, settings: Optional[AgentSettings] = None) -> bytes:
        env_secret = os.environ.get("MCP_AGENT_SESSION_SECRET")
        if env_secret is not None:
            stripped = env_secret.strip()
            if stripped:
                return stripped.encode("utf-8")
            return self._ephemeral_secret
        if settings is not None and settings.session_secret:
            stripped = settings.session_secret.strip()
            if stripped:
                return stripped.encode("utf-8")
        return self._ephemeral_secret

    def _sign_cookie_payload(
        self,
        cid: str,
        uid: str,
        sids: List[str],
        settings: Optional[AgentSettings] = None,
    ) -> str:
        payload = {
            "v": _COOKIE_VERSION,
            "cid": cid,
            "uid": uid,
            "sids": sids[-_MAX_COOKIE_SESSIONS:],
        }
        payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        payload_b64 = _b64url_encode(payload_bytes)
        secret = self._get_secret_bytes(settings)
        digest = hmac.new(secret, payload_b64.encode("ascii"), hashlib.sha256).digest()
        sig_b64 = _b64url_encode(digest)
        return f"{payload_b64}.{sig_b64}"

    def verify_cookie(
        self,
        token: str,
        settings: Optional[AgentSettings] = None,
    ) -> Optional[Dict[str, Any]]:
        """Verifies an HMAC-SHA256 signed session cookie in constant time."""
        if not isinstance(token, str) or not token or len(token) > _MAX_COOKIE_LENGTH:
            return None
        if not token.isascii():
            return None
        parts = token.split(".")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return None

        payload_b64, provided_sig_b64 = parts
        secret = self._get_secret_bytes(settings)
        expected_digest = hmac.new(secret, payload_b64.encode("ascii"), hashlib.sha256).digest()
        expected_sig_b64 = _b64url_encode(expected_digest)
        if not hmac.compare_digest(
            provided_sig_b64.encode("ascii"),
            expected_sig_b64.encode("ascii"),
        ):
            return None

        raw_payload = _b64url_decode(payload_b64)
        if raw_payload is None:
            return None

        try:
            data = json.loads(raw_payload.decode("utf-8"))
        except Exception:
            return None

        if not isinstance(data, dict) or data.get("v") != _COOKIE_VERSION:
            return None

        cid = data.get("cid")
        uid = data.get("uid")
        sids = data.get("sids")
        if not isinstance(cid, str) or not cid or len(cid) > 128:
            return None
        if not is_valid_user_id(uid):
            return None
        if not isinstance(sids, list) or len(sids) > _MAX_COOKIE_SESSIONS:
            return None
        if not all(is_valid_session_id(s) for s in sids):
            return None

        return {"cid": cid, "uid": uid, "sids": list(sids)}

    def set_cookie_on_response(
        self,
        response: Response,
        request: Request,
        token: str,
    ) -> None:
        """Sets the HttpOnly, SameSite=Lax (and conditional Secure) session cookie."""
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=token,
            httponly=True,
            samesite="lax",
            secure=is_https_request(request),
            path="/",
        )

    def _record_session_owner(self, session_id: str, owner_key: str, user_id: str) -> None:
        with self._lock:
            self._session_owners.pop(session_id, None)
            while len(self._session_owners) >= self._max_sessions:
                self._session_owners.popitem(last=False)
            self._session_owners[session_id] = (owner_key, user_id)

    def verify_iap_principal(
        self,
        request: Request,
        settings: Optional[AgentSettings] = None,
    ) -> str:
        """Validates Google Cloud IAP ES256 JWT assertion and extracts verified email."""
        audience = get_iap_audience(settings)
        if not audience:
            logger.error("MCP_AGENT_IAP_AUDIENCE must be configured when MCP_AGENT_REQUIRE_IAP is enabled.")
            raise HTTPException(
                status_code=500,
                detail="MCP_AGENT_IAP_AUDIENCE must be configured when MCP_AGENT_REQUIRE_IAP is enabled.",
            )

        raw_jwt = request.headers.get("x-goog-iap-jwt-assertion")
        if not raw_jwt or not raw_jwt.strip():
            logger.warning("Missing X-Goog-Iap-Jwt-Assertion header on IAP-protected route")
            raise HTTPException(
                status_code=401,
                detail="Missing X-Goog-Iap-Jwt-Assertion header.",
            )

        raw_jwt = raw_jwt.strip()
        try:
            header = jwt.get_unverified_header(raw_jwt)
        except Exception as e:
            logger.warning("Malformed IAP JWT header: %s", e)
            raise HTTPException(status_code=401, detail="Malformed IAP JWT header.")

        if header.get("alg") != "ES256" or not header.get("kid"):
            logger.warning("Rejected IAP JWT with unsupported alg or missing kid: %s", header.get("alg"))
            raise HTTPException(status_code=401, detail="Invalid IAP JWT header algorithm or key ID.")

        try:
            claims = google.oauth2.id_token.verify_token(
                raw_jwt,
                request=self._http_request,
                audience=audience,
                certs_url=_IAP_CERTS_URL,
                clock_skew_in_seconds=30,
            )
        except Exception as e:
            logger.warning("IAP token verification failed: %s", e)
            raise HTTPException(status_code=401, detail=f"IAP token verification failed: {e}")

        if claims.get("iss") != _IAP_EXPECTED_ISSUER:
            logger.warning("Rejected IAP JWT with unexpected issuer: %s", claims.get("iss"))
            raise HTTPException(status_code=401, detail="Invalid IAP token issuer.")

        email = claims.get("email")
        if not email or not isinstance(email, str):
            logger.warning("IAP JWT missing email claim")
            raise HTTPException(status_code=401, detail="IAP token missing email claim.")

        principal = email.strip()
        if principal.lower().startswith(_IAP_EMAIL_PREFIX):
            principal = principal[len(_IAP_EMAIL_PREFIX):].strip()

        if not principal or not is_valid_user_id(principal):
            logger.warning("IAP JWT email is not a valid user identifier: %s", principal)
            raise HTTPException(status_code=401, detail="IAP token contains invalid user identity.")

        return principal

    def resolve_info_user(
        self,
        request: Request,
        settings: Optional[AgentSettings] = None,
    ) -> str:
        """Resolves the active user identity for /info metadata."""
        if is_iap_mode_enabled(settings):
            if settings and settings.require_iap:
                return self.verify_iap_principal(request, settings)
            try:
                return self.verify_iap_principal(request, settings)
            except Exception:
                return "unauthenticated"
        raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        if raw_cookie:
            cookie_data = self.verify_cookie(raw_cookie, settings)
            if cookie_data is not None:
                return cookie_data["uid"]
        return _safe_default_user()

    def issue_session(
        self,
        request: Request,
        response: Response,
        username: Optional[str] = None,
        start_new_session: Optional[str] = "N",
        settings: Optional[AgentSettings] = None,
    ) -> Dict[str, str]:
        """Issues or refreshes a bound session capability for /get_session."""
        verify_same_origin(request, settings)

        if start_new_session is not None and start_new_session.strip().upper() not in _START_NEW_VALUES:
            raise HTTPException(status_code=400, detail="Invalid start_new_session parameter.")

        requested_user: Optional[str] = None
        if username is not None and username.strip() and username != "secops_user":
            if not is_valid_user_id(username):
                raise HTTPException(status_code=400, detail="Invalid username format.")
            requested_user = username

        if is_iap_mode_enabled(settings):
            principal = self.verify_iap_principal(request, settings)
            if requested_user is not None and requested_user != principal:
                logger.warning(
                    "Rejected /get_session username mismatch for authenticated principal %s",
                    principal,
                )
                raise HTTPException(
                    status_code=403,
                    detail="Requested username does not match authenticated principal.",
                )

            raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            cid: Optional[str] = None
            sids: List[str] = []
            if raw_cookie is not None:
                cookie_data = self.verify_cookie(raw_cookie, settings)
                if cookie_data is not None and cookie_data["uid"] == principal:
                    cid = cookie_data["cid"]
                    sids = list(cookie_data["sids"])
            if cid is None:
                cid = secrets.token_urlsafe(24)

            session_id = str(uuid.uuid4())
            sids.append(session_id)
            sids = sids[-_MAX_COOKIE_SESSIONS:]
            self._record_session_owner(session_id, f"iap:{principal}", principal)

            token = self._sign_cookie_payload(cid, principal, sids, settings)
            self.set_cookie_on_response(response, request, token)
            return {"session_id": session_id, "user_id": principal}

        # Default (non-IAP) mode
        raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        cookie_data = self.verify_cookie(raw_cookie, settings) if raw_cookie else None

        if cookie_data is None:
            cid = secrets.token_urlsafe(24)
            uid = requested_user or _safe_default_user()
            session_id = str(uuid.uuid4())
            sids = [session_id]
            self._record_session_owner(session_id, f"cid:{cid}", uid)
            token = self._sign_cookie_payload(cid, uid, sids, settings)
            self.set_cookie_on_response(response, request, token)
            return {"session_id": session_id, "user_id": uid}

        if requested_user is not None and requested_user != cookie_data["uid"]:
            cid = secrets.token_urlsafe(24)
            uid = requested_user
            session_id = str(uuid.uuid4())
            sids = [session_id]
            self._record_session_owner(session_id, f"cid:{cid}", uid)
            token = self._sign_cookie_payload(cid, uid, sids, settings)
            self.set_cookie_on_response(response, request, token)
            return {"session_id": session_id, "user_id": uid}

        cid = cookie_data["cid"]
        uid = cookie_data["uid"]
        session_id = str(uuid.uuid4())
        sids = list(cookie_data["sids"])
        sids.append(session_id)
        sids = sids[-_MAX_COOKIE_SESSIONS:]
        self._record_session_owner(session_id, f"cid:{cid}", uid)
        token = self._sign_cookie_payload(cid, uid, sids, settings)
        self.set_cookie_on_response(response, request, token)
        return {"session_id": session_id, "user_id": uid}

    def authorize_chat(
        self,
        request: Request,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        settings: Optional[AgentSettings] = None,
    ) -> Tuple[str, str, Optional[str]]:
        """Authorizes a /chat request and returns (user_id, session_id, new_cookie_or_none)."""
        verify_same_origin(request, settings)

        req_uid = None if (user_id is None or user_id == "") else user_id
        req_sid = None if (session_id is None or session_id == "") else session_id

        if is_iap_mode_enabled(settings):
            principal = self.verify_iap_principal(request, settings)
            if req_uid is not None:
                if not is_valid_user_id(req_uid):
                    raise HTTPException(status_code=400, detail="Invalid user_id format.")
                if req_uid != principal:
                    logger.warning(
                        "Rejected /chat user_id mismatch for authenticated principal %s",
                        principal,
                    )
                    raise HTTPException(
                        status_code=403,
                        detail="Caller user_id does not match authenticated principal.",
                    )
            if req_sid is not None and not is_valid_session_id(req_sid):
                raise HTTPException(status_code=400, detail="Invalid session_id format.")

            raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            cookie_data: Optional[Dict[str, Any]] = None
            if raw_cookie is not None:
                cookie_data = self.verify_cookie(raw_cookie, settings)
                if cookie_data is None or cookie_data["uid"] != principal:
                    raise HTTPException(
                        status_code=403,
                        detail="Session cookie does not match authenticated principal.",
                    )

            expected_owner = (f"iap:{principal}", principal)
            if req_sid is None:
                new_sid = str(uuid.uuid4())
                cid = cookie_data["cid"] if cookie_data else secrets.token_urlsafe(24)
                sids = list(cookie_data["sids"]) if cookie_data else []
                sids.append(new_sid)
                sids = sids[-_MAX_COOKIE_SESSIONS:]
                self._record_session_owner(new_sid, f"iap:{principal}", principal)
                new_token = self._sign_cookie_payload(cid, principal, sids, settings)
                return principal, new_sid, new_token

            with self._lock:
                owner = self._session_owners.get(req_sid)
                if owner is not None:
                    if owner != expected_owner:
                        logger.warning(
                            "Rejected cross-principal /chat access to session %s by %s",
                            req_sid,
                            principal,
                        )
                        raise HTTPException(
                            status_code=403,
                            detail="Session is not owned by the authenticated principal.",
                        )
                    return principal, req_sid, None

                if cookie_data is not None and req_sid in cookie_data["sids"]:
                    self._record_session_owner(req_sid, f"iap:{principal}", principal)
                    return principal, req_sid, None

            raise HTTPException(
                status_code=403,
                detail="Session is not authorized for the authenticated principal.",
            )

        # Default (non-IAP) mode
        raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        cookie_data: Optional[Dict[str, Any]] = None
        if raw_cookie is not None:
            cookie_data = self.verify_cookie(raw_cookie, settings)
            if cookie_data is None:
                logger.warning("Rejected invalid or tampered session cookie on /chat")
                raise HTTPException(
                    status_code=403,
                    detail="Invalid session authorization cookie.",
                )

        if req_uid is not None and not is_valid_user_id(req_uid):
            raise HTTPException(status_code=400, detail="Invalid user_id format.")
        if req_sid is not None and not is_valid_session_id(req_sid):
            raise HTTPException(status_code=400, detail="Invalid session_id format.")

        # Stateless single-turn API path:
        if cookie_data is None and req_sid is None and req_uid is None:
            cid = secrets.token_urlsafe(24)
            uid = _safe_default_user()
            new_sid = str(uuid.uuid4())
            self._record_session_owner(new_sid, f"cid:{cid}", uid)
            new_token = self._sign_cookie_payload(cid, uid, [new_sid], settings)
            return uid, new_sid, new_token

        # All stateful or user-targeted paths require a valid session cookie
        if cookie_data is None:
            raise HTTPException(
                status_code=403,
                detail="Missing session authorization cookie.",
            )

        cid = cookie_data["cid"]
        bound_uid = cookie_data["uid"]
        if req_uid is not None and req_uid != bound_uid:
            logger.warning(
                "Rejected cross-user /chat request from bound principal %s targeting %s",
                bound_uid,
                req_uid,
            )
            raise HTTPException(
                status_code=403,
                detail="Caller user_id does not match bound session identity.",
            )

        expected_owner = (f"cid:{cid}", bound_uid)
        if req_sid is None:
            new_sid = str(uuid.uuid4())
            sids = list(cookie_data["sids"])
            sids.append(new_sid)
            sids = sids[-_MAX_COOKIE_SESSIONS:]
            self._record_session_owner(new_sid, f"cid:{cid}", bound_uid)
            new_token = self._sign_cookie_payload(cid, bound_uid, sids, settings)
            return bound_uid, new_sid, new_token

        if req_sid not in cookie_data["sids"]:
            logger.warning(
                "Rejected /chat request for unowned session %s by principal %s",
                req_sid,
                bound_uid,
            )
            raise HTTPException(
                status_code=403,
                detail="Session is not bound to caller capability.",
            )

        with self._lock:
            owner = self._session_owners.get(req_sid)
            if owner is not None and owner != expected_owner:
                logger.warning(
                    "Rejected /chat session ownership conflict on %s for %s",
                    req_sid,
                    bound_uid,
                )
                raise HTTPException(
                    status_code=403,
                    detail="Session belongs to another client.",
                )
            if owner is None:
                self._record_session_owner(req_sid, f"cid:{cid}", bound_uid)

        return bound_uid, req_sid, None


def get_session_auth(request: Request) -> SessionAuthManager:
    """Retrieves or lazily initializes the app-scoped SessionAuthManager."""
    manager = getattr(request.app.state, "session_auth", None)
    if manager is None:
        with _fallback_lock:
            manager = getattr(request.app.state, "session_auth", None)
            if manager is None:
                manager = SessionAuthManager()
                request.app.state.session_auth = manager
    return manager
