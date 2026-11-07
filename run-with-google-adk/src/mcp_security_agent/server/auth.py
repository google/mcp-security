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
import uuid
from typing import Any, Dict, List, Optional, Tuple

from fastapi import HTTPException, Request, Response

from mcp_security_agent.config import AgentSettings, discover_user_identity

logger = logging.getLogger(__name__)

SESSION_COOKIE_NAME = "mcp_agent_session"
_COOKIE_VERSION = 1
_MAX_COOKIE_LENGTH = 4096
_MAX_COOKIE_SESSIONS = 32
_MAX_TRACKED_SESSIONS = 4096
_MAX_TRACKED_PRINCIPALS = 4096
_IAP_EMAIL_PREFIX = "accounts.google.com:"
_TRUTHY_VALUES = frozenset({"Y", "YES", "TRUE", "1"})
_START_NEW_VALUES = frozenset({"Y", "N", "YES", "NO", "TRUE", "FALSE", "1", "0", ""})

_USER_ID_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._@+-]{0,127}\Z")
_SESSION_ID_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")

_fallback_lock = threading.Lock()


def is_valid_user_id(value: Any) -> bool:
    """Validates user_id / username format and length bounds."""
    if not isinstance(value, str) or ".." in value:
        return False
    return bool(_USER_ID_RE.fullmatch(value))


def is_valid_session_id(value: Any) -> bool:
    """Validates session_id format and length bounds."""
    if not isinstance(value, str):
        return False
    return bool(_SESSION_ID_RE.fullmatch(value))


def is_https_request(request: Request) -> bool:
    """Determines whether the request arrived over HTTPS directly or via proxy."""
    if request.url.scheme.lower() == "https":
        return True
    forwarded_proto = request.headers.get("x-forwarded-proto", "")
    if forwarded_proto:
        first_hop = forwarded_proto.split(",")[0].strip().lower()
        if first_hop == "https":
            return True
    return False


def trust_auth_headers_enabled(settings: Optional[AgentSettings] = None) -> bool:
    """Checks whether trusted reverse-proxy identity headers are enabled."""
    raw = os.environ.get("MCP_AGENT_TRUST_AUTH_HEADERS")
    if raw is not None:
        return raw.strip().upper() in _TRUTHY_VALUES
    if settings is not None:
        return bool(settings.trust_auth_headers)
    return False


def extract_trusted_principal(request: Request) -> str:
    """Extracts and validates X-Goog-Authenticated-User-Email from a trusted proxy."""
    raw_header = request.headers.get("x-goog-authenticated-user-email")
    if raw_header is None or not raw_header.strip():
        raise HTTPException(
            status_code=401,
            detail="Authenticated user identity header is required.",
        )
    principal = raw_header.strip()
    if principal.lower().startswith(_IAP_EMAIL_PREFIX):
        principal = principal[len(_IAP_EMAIL_PREFIX):].strip()
    if not principal or not is_valid_user_id(principal):
        raise HTTPException(
            status_code=401,
            detail="Authenticated user identity header is invalid.",
        )
    return principal


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

    def __init__(self, max_sessions: int = _MAX_TRACKED_SESSIONS) -> None:
        self._ephemeral_secret: bytes = secrets.token_bytes(32)
        self._max_sessions = max_sessions
        self._session_owners: "OrderedDict[str, Tuple[str, str]]" = OrderedDict()
        self._principal_owners: "OrderedDict[str, str]" = OrderedDict()
        self._lock = threading.RLock()

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
        self._session_owners.pop(session_id, None)
        while len(self._session_owners) >= self._max_sessions:
            self._session_owners.popitem(last=False)
        self._session_owners[session_id] = (owner_key, user_id)

    def _record_principal_owner(self, user_id: str, cid: str) -> None:
        self._principal_owners.pop(user_id, None)
        while len(self._principal_owners) >= _MAX_TRACKED_PRINCIPALS:
            self._principal_owners.popitem(last=False)
        self._principal_owners[user_id] = cid

    def resolve_info_user(
        self,
        request: Request,
        settings: Optional[AgentSettings] = None,
    ) -> str:
        """Resolves the active user identity for /info metadata."""
        if trust_auth_headers_enabled(settings):
            return extract_trusted_principal(request)
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
        if trust_auth_headers_enabled(settings):
            principal = extract_trusted_principal(request)
            if start_new_session is not None and start_new_session.strip().upper() not in _START_NEW_VALUES:
                raise HTTPException(status_code=400, detail="Invalid start_new_session parameter.")
            if username is not None and username != "":
                if not is_valid_user_id(username):
                    raise HTTPException(status_code=400, detail="Invalid username format.")
                if username != principal:
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
                if cookie_data is None:
                    raise HTTPException(status_code=403, detail="Invalid session cookie.")
                if cookie_data["uid"] == principal:
                    cid = cookie_data["cid"]
                    sids = list(cookie_data["sids"])
            if cid is None:
                cid = secrets.token_urlsafe(24)

            session_id = str(uuid.uuid4())
            sids.append(session_id)
            sids = sids[-_MAX_COOKIE_SESSIONS:]
            with self._lock:
                self._record_session_owner(session_id, f"iap:{principal}", principal)

            token = self._sign_cookie_payload(cid, principal, sids, settings)
            self.set_cookie_on_response(response, request, token)
            return {"session_id": session_id, "user_id": principal}

        if start_new_session is not None and start_new_session.strip().upper() not in _START_NEW_VALUES:
            raise HTTPException(status_code=400, detail="Invalid start_new_session parameter.")

        requested_user: Optional[str] = None
        if username is not None and username != "":
            if not is_valid_user_id(username):
                raise HTTPException(status_code=400, detail="Invalid username format.")
            requested_user = username

        raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        if raw_cookie is not None:
            cookie_data = self.verify_cookie(raw_cookie, settings)
            if cookie_data is None:
                logger.warning("Rejected invalid or tampered session cookie on /get_session")
                raise HTTPException(status_code=403, detail="Invalid session cookie.")

            cid = cookie_data["cid"]
            bound_uid = cookie_data["uid"]
            if requested_user is not None and requested_user != bound_uid:
                logger.warning(
                    "Rejected /get_session principal switch from %s to %s",
                    bound_uid,
                    requested_user,
                )
                raise HTTPException(
                    status_code=403,
                    detail="Session cookie is already bound to a different user identity.",
                )

            session_id = str(uuid.uuid4())
            sids = list(cookie_data["sids"])
            sids.append(session_id)
            sids = sids[-_MAX_COOKIE_SESSIONS:]
            with self._lock:
                self._record_session_owner(session_id, f"cid:{cid}", bound_uid)

            token = self._sign_cookie_payload(cid, bound_uid, sids, settings)
            self.set_cookie_on_response(response, request, token)
            return {"session_id": session_id, "user_id": bound_uid}

        cid = secrets.token_urlsafe(24)
        session_id = str(uuid.uuid4())
        with self._lock:
            if requested_user is not None:
                existing_cid = self._principal_owners.get(requested_user)
                if existing_cid is not None:
                    logger.warning(
                        "Rejected unauthenticated claim for already-bound username %s",
                        requested_user,
                    )
                    raise HTTPException(
                        status_code=403,
                        detail="Requested username is already bound to another client.",
                    )
                uid = requested_user
                self._record_principal_owner(uid, cid)
            else:
                uid = _safe_default_user()
            self._record_session_owner(session_id, f"cid:{cid}", uid)

        token = self._sign_cookie_payload(cid, uid, [session_id], settings)
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
        req_uid = None if (user_id is None or user_id == "") else user_id
        req_sid = None if (session_id is None or session_id == "") else session_id

        if trust_auth_headers_enabled(settings):
            principal = extract_trusted_principal(request)
            if req_uid is not None and not is_valid_user_id(req_uid):
                raise HTTPException(status_code=400, detail="Invalid user_id format.")
            if req_sid is not None and not is_valid_session_id(req_sid):
                raise HTTPException(status_code=400, detail="Invalid session_id format.")
            if req_uid is not None and req_uid != principal:
                logger.warning(
                    "Rejected /chat user_id mismatch for authenticated principal %s",
                    principal,
                )
                raise HTTPException(
                    status_code=403,
                    detail="Caller user_id does not match authenticated principal.",
                )

            raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            cookie_data: Optional[Dict[str, Any]] = None
            if raw_cookie is not None:
                cookie_data = self.verify_cookie(raw_cookie, settings)
                if cookie_data is None:
                    raise HTTPException(status_code=403, detail="Invalid session cookie.")
                if cookie_data["uid"] != principal:
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
                with self._lock:
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

        raw_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        if not raw_cookie:
            raise HTTPException(
                status_code=403,
                detail="Missing session authorization cookie.",
            )
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
            with self._lock:
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
