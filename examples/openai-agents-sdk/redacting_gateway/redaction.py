# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Reversible redaction of usernames and IP addresses.

Every real value is replaced by a typed placeholder such as [[IP_EXT_001]] or
[[USER_001]]. The same value always gets the same placeholder, and the
TokenMap that links the two never leaves this machine.

What counts as a username:
  * values of user fields in structured results (userid, user_name,
    email_addresses, user_display_name, windows_sid, and similar keys);
  * names in profile paths (C:\\Users\\<name>, /home/<name>, /Users/<name>);
  * DOMAIN\\user, runas or net use /user:<name>, and psexec -u <name>;
  * the part of an email address before the @;
  * domain account SIDs (S-1-5-21-...).
Once a name is known, it is replaced everywhere, including inside hostnames
such as JDOE-LT. Built-in accounts such as SYSTEM stay visible.

What counts as an IP address: IPv4 (also with leading zeros, defanged as
10[.]0[.]0[.]1, and dash-encoded as ip-10-0-0-1 or 10-0-0-1.example.net), and
IPv6 (compressed, full, IPv4-mapped).

Known gaps, which the leak check in find_leaks() cannot close either:
  * a name seen only in free text, in a form none of the rules recognize,
    before any user field has revealed it (so fetch the alert first);
  * a name glued to other letters (xjdoe), and a first name used on its own
    after a display name was seen;
  * IPv4 written as one integer or in hex, PTR names (typed by the reversed
    address), and base64-encoded payloads.
"""

import ipaddress
import json
import os
import re
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

MAP_VERSION = 1

IP_INT = "IP_INT"
IP_EXT = "IP_EXT"
USER = "USER"
SVC = "SVC"
KINDS = (IP_INT, IP_EXT, USER, SVC)

# The exact placeholder format. Only this form is ever restored.
TOKEN_RE = re.compile(r"\[\[(IP_INT|IP_EXT|USER|SVC)_(\d{3,})\]\]")
# Anything that looks like an attempt at a placeholder, such as ip_ext_1,
# IP-12 or USER_7. Outgoing text that contains one is rejected.
LOOSE_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:IP_INT|IP_EXT|IP|USER|SVC)[_-]\d+(?![0-9])", re.IGNORECASE
)

_OCTET = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d|0\d{1,2})"
_DOT = r"(?:\.|\[\.\]|\(\.\)|\[dot\])"
IPV4_RE = re.compile(rf"(?<!\d)(?<!\d\.){_OCTET}(?:{_DOT}{_OCTET}){{3}}(?!\d|\.\d)")
_DASHED = rf"{_OCTET}(?:-{_OCTET}){{3}}"
# ip-10-0-0-1 anywhere, or 10-0-0-1 as the first label of a hostname.
DASHED_IPV4_RE = re.compile(
    rf"(?<=ip-){_DASHED}(?!\d)|(?<![\w-]){_DASHED}(?=\.[A-Za-z])", re.IGNORECASE
)
IPV6_CANDIDATE_RE = re.compile(
    r"(?:(?<![0-9A-Fa-f:.])|(?<=[G-Zg-z_]:))(?:[0-9A-Fa-f]{0,4}:){2,7}"
    r"(?:(?:\d{1,3}\.){3}\d{1,3}|[0-9A-Fa-f]{0,4})(?![\w:])"
)

_INTERNAL_NETWORKS = tuple(
    ipaddress.ip_network(net)
    for net in (
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "100.64.0.0/10",
        "127.0.0.0/8",
        "169.254.0.0/16",
        "::1/128",
        "fc00::/7",
        "fe80::/10",
    )
)

# Keys (lowercase, letters and digits only) whose string values are usernames.
_USER_KEYS = frozenset(
    {
        "user",
        "userid",
        "username",
        "accountname",
        "samaccountname",
        "userprincipalname",
        "userdisplayname",
        "email",
        "emailaddress",
        "emailaddresses",
        "windowssid",
        "usersid",
        "targetusername",
        "subjectusername",
        "srcuser",
        "dstuser",
        "firstname",
        "lastname",
        "givenname",
        "familyname",
        "fullname",
    }
)
# Keys that hold usernames only inside a user object, e.g. user.display_name.
_USER_OBJECT_KEYS = frozenset({"displayname", "sid", "name"})

# Accounts, folders and role mailboxes that do not identify a person stay visible.
_BUILT_IN_ACCOUNTS = frozenset(
    {
        "system",
        "local service",
        "localservice",
        "network service",
        "networkservice",
        "root",
        "administrator",
        "guest",
        "public",
        "default",
        "default user",
        "all users",
        "anonymous logon",
        "shared",
        "abuse",
        "admin",
        "billing",
        "contact",
        "help",
        "hostmaster",
        "info",
        "noreply",
        "no-reply",
        "postmaster",
        "sales",
        "security",
        "support",
        "webmaster",
    }
)
_NOT_A_NAME = frozenset({"", "-", "n/a", "na", "none", "null", "unknown"})

_PROFILE_RE = re.compile(
    # A profile name may contain spaces when a backslash follows it.
    r"(?:[A-Za-z]:)?\\{1,2}Users\\{1,2}"
    r"(?:([^\\/:*?\"<>|\r\n]{1,64}?)(?=\\)|([^\\/:*?\"<>|\s]+))"
    r"|/(?:home|Users)/([^/\s\"':]+)",
    re.IGNORECASE,
)
_DOMAIN_USER_RE = re.compile(
    r"(?<![\\/\w.$-])([A-Za-z][\w-]{0,14})\\{1,2}([\w.$-]{1,64})(?![\\/\w$-])"
)
# DOMAIN\name pairs that are really built-in accounts, registry keys or paths.
_NOT_A_DOMAIN = frozenset(
    {
        "authority",
        "apppool",
        "hklm",
        "hkcu",
        "hkcr",
        "hku",
        "temp",
        "tmp",
        "windows",
        "system32",
    }
)
_FILE_NAME_RE = re.compile(
    r"\.(?:exe|dll|sys|ps1|psm1|bat|cmd|vbs|js|txt|log|tmp|dat|ini)$", re.IGNORECASE
)
_SLASH_USER_RE = re.compile(r"/user:\"?(?:[\w.-]+\\{1,2})?([^\s\"\\/]+)", re.IGNORECASE)
_PSEXEC_USER_RE = re.compile(
    r"\bpsexec(?:64)?(?:\.exe)?\b[^\r\n]*?\s-u\s+\"?(?:[\w.-]+\\{1,2})?([^\s\"\\]+)",
    re.IGNORECASE,
)
# The lookbehind lets a match start only at the beginning of a local part, which
# keeps long runs of text without an @ linear instead of quadratic.
_EMAIL_RE = re.compile(r"(?<![\w.%+-])([\w.%+-]+)@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}")
_SID_RE = re.compile(r"\bS-1-5-21(?:-\d+){4}\b")
_SERVICE_RE = re.compile(r"^svc|[_.-]svc$|^sa[_.-]|service|\$$", re.IGNORECASE)


class PlaceholderError(ValueError):
    """Outgoing text holds a placeholder that cannot be restored."""


class UnknownPlaceholder(PlaceholderError):
    """A well-formed placeholder that is not in the map."""


class MalformedPlaceholder(PlaceholderError):
    """Text that looks like a placeholder but does not match the format."""


class MapVersionError(ValueError):
    """The map file was written in a format this code cannot read."""


def is_internal_ip(address: str) -> bool:
    """Return whether the address is private, loopback, link-local or CGNAT."""
    ip = ipaddress.ip_address(address)
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    return any(ip in net for net in _INTERNAL_NETWORKS if ip.version == net.version)


def _canonical_ip(text: str) -> str | None:
    """Return the canonical form of an IP address, or None if it is not one."""
    for dot in ("[.]", "(.)", "[dot]"):
        text = text.replace(dot, ".")
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", text):
        text = ".".join(str(int(part)) for part in text.split("."))
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return None
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    return str(ip)


def _ipv6_parts(candidate: str) -> tuple[str, str | None]:
    """Split an IPv6 candidate into a prefix to keep and its canonical address.

    A candidate can start with the colon of a label such as "ip:2001:db8::6".
    """
    canonical = _canonical_ip(candidate)
    if (
        canonical is None
        and candidate.startswith(":")
        and not candidate.startswith("::")
    ):
        return ":", _canonical_ip(candidate[1:])
    return "", canonical


def ips_in(text: str) -> list[str]:
    """Return the canonical form of every IP address in text."""
    found = [_ipv6_parts(m.group(0))[1] for m in IPV6_CANDIDATE_RE.finditer(text)]
    found += [_canonical_ip(m.group(0)) for m in IPV4_RE.finditer(text)]
    found += [
        _canonical_ip(m.group(0).replace("-", "."))
        for m in DASHED_IPV4_RE.finditer(text)
    ]
    return [ip for ip in found if ip]


def _base_name(value: str) -> str:
    """Strip a DOMAIN\\ prefix and an @domain suffix from an account name."""
    value = value.strip().rstrip(".")
    value = re.split(r"\\+", value)[-1]
    if "@" in value:
        value = value.split("@", 1)[0]
    return value.strip()


def _is_name(value: str) -> bool:
    folded = value.lower()
    return (
        len(value) >= 2
        and folded not in _NOT_A_NAME
        and folded not in _BUILT_IN_ACCOUNTS
        and _canonical_ip(value) is None
        and not TOKEN_RE.fullmatch(value)
    )


def _outside_tokens(text: str, replace: Callable[[str], str]) -> str:
    """Apply replace() to every part of text that is not a placeholder."""
    parts = []
    last = 0
    for match in TOKEN_RE.finditer(text):
        parts.append(replace(text[last : match.start()]))
        parts.append(match.group(0))
        last = match.end()
    parts.append(replace(text[last:]))
    return "".join(parts)


def _name_pattern(names: list[str]) -> re.Pattern[str] | None:
    if not names:
        return None
    alternatives = "|".join(
        re.escape(name) for name in sorted(names, key=len, reverse=True)
    )
    # A name matches only where it is not part of a longer word; "_", "-",
    # "." and "\" count as separators, so jdoe matches in JDOE-LT.
    return re.compile(rf"(?<![^\W_])(?:{alternatives})(?![^\W_])", re.IGNORECASE)


class TokenMap:
    """The placeholder-to-value pairs of one run."""

    def __init__(self, run_id: str = "") -> None:
        self.run_id = run_id
        self._token_by_key: dict[str, str] = {}
        self._value_by_token: dict[str, str] = {}
        self._kind_by_token: dict[str, str] = {}
        self._user_tokens: dict[str, str] = {}
        self._counts = dict.fromkeys(KINDS, 0)

    def __len__(self) -> int:
        return len(self._value_by_token)

    def token_for(self, kind: str, key: str, value: str) -> str:
        """Return the placeholder for key, creating one if needed."""
        token = self._token_by_key.get(key)
        if token is None:
            self._counts[kind] += 1
            token = f"[[{kind}_{self._counts[kind]:03d}]]"
            self._add(token, kind, key, value)
        return token

    def _add(self, token: str, kind: str, key: str, value: str) -> None:
        if key in self._token_by_key or token in self._value_by_token:
            raise ValueError(f"Duplicate map entry: {token}")
        self._token_by_key[key] = token
        self._value_by_token[token] = value
        self._kind_by_token[token] = kind
        if key.startswith("user:"):
            self._user_tokens[key.removeprefix("user:")] = token

    def value_for(self, token: str) -> str | None:
        return self._value_by_token.get(token)

    def user_tokens(self) -> dict[str, str]:
        """Return the known usernames (lowercase) and their placeholders. Do not modify."""
        return self._user_tokens

    def values(self) -> list[str]:
        return list(self._value_by_token.values())

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": MAP_VERSION,
            "run_id": self.run_id,
            "entries": [
                {
                    "token": token,
                    "kind": self._kind_by_token[token],
                    "key": key,
                    "value": self._value_by_token[token],
                }
                for key, token in self._token_by_key.items()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TokenMap":
        version = data.get("version")
        if version != MAP_VERSION:
            raise MapVersionError(f"Unsupported map version: {version!r}")
        token_map = cls(run_id=data.get("run_id", ""))
        entries = data.get("entries")
        if not isinstance(entries, list):
            raise ValueError("The map has no entries list")  # noqa: TRY004 - a malformed file
        for entry in entries:
            match = TOKEN_RE.fullmatch(entry["token"])
            if match is None or match.group(1) != entry["kind"]:
                raise ValueError(f"Bad map entry: {entry['token']!r}")
            token_map._add(entry["token"], entry["kind"], entry["key"], entry["value"])
            token_map._counts[entry["kind"]] = max(
                token_map._counts[entry["kind"]], int(match.group(2))
            )
        return token_map

    def save(self, path: Path) -> None:
        """Write the map atomically, readable by the owner only."""
        path = Path(path)
        fd, temp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.to_dict(), handle, ensure_ascii=False, indent=1)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        except BaseException:
            Path(temp_name).unlink(missing_ok=True)
            raise

    @classmethod
    def load(cls, path: Path) -> "TokenMap":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


class Redactor:
    """Replaces real values with placeholders and restores them."""

    def __init__(
        self, token_map: TokenMap, secrets: dict[str, str] | None = None
    ) -> None:
        """secrets maps fixed values, such as tenant IDs, to labels that replace them.

        Unlike placeholders, labels are never restored.
        """
        self.map = token_map
        # Very short values would match ordinary text, so they are ignored.
        self._secrets = {
            real.lower(): label
            for real, label in (secrets or {}).items()
            if len(real) >= 4
        }
        self._secret_pattern = (
            re.compile(
                "|".join(
                    re.escape(real)
                    for real in sorted(self._secrets, key=len, reverse=True)
                ),
                re.IGNORECASE,
            )
            if self._secrets
            else None
        )
        self._pattern: re.Pattern[str] | None = None
        self._pattern_size = -1

    # Redaction (upstream results on their way to the model).

    def redact(self, value: Any) -> Any:
        """Return a copy of a string or JSON-like value with real values replaced.

        All usernames in the whole value are learned first, so a name that
        appears in free text before its user field is still replaced.
        """
        names: set[str] = set()
        _collect_names(value, names, in_user_object=False)
        for name in sorted(names, key=lambda name: (name.lower(), name)):
            self._add_user(name)
        return self._redact_value(value)

    def _add_user(self, name: str) -> str:
        kind = SVC if _SERVICE_RE.search(name) else USER
        return self.map.token_for(kind, f"user:{name.lower()}", name)

    def _redact_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self._redact_text(value)
        if isinstance(value, dict):
            return {
                self._redact_text(str(k)): self._redact_value(v)
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [self._redact_value(item) for item in value]
        return value

    def _redact_text(self, text: str) -> str:
        # Text from upstream that already looks like a placeholder is broken
        # up, so it can never be restored into a real value.
        text = TOKEN_RE.sub(lambda m: "[ [" + m.group(0)[2:], text)
        if self._secret_pattern is not None:
            text = self._secret_pattern.sub(
                lambda m: self._secrets[m.group(0).lower()], text
            )
        text = _outside_tokens(text, self._replace_ips)
        return _outside_tokens(text, self._replace_names)

    def _ip_token(self, match: re.Match[str]) -> str:
        canonical = _canonical_ip(match.group(0))
        if canonical is None:
            return match.group(0)
        kind = IP_INT if is_internal_ip(canonical) else IP_EXT
        return self.map.token_for(kind, f"ip:{canonical}", canonical)

    def _ipv6_token(self, match: re.Match[str]) -> str:
        prefix, canonical = _ipv6_parts(match.group(0))
        if canonical is None:
            return match.group(0)
        kind = IP_INT if is_internal_ip(canonical) else IP_EXT
        return prefix + self.map.token_for(kind, f"ip:{canonical}", canonical)

    def _replace_ips(self, text: str) -> str:
        text = IPV6_CANDIDATE_RE.sub(self._ipv6_token, text)
        text = _outside_tokens(text, lambda part: IPV4_RE.sub(self._ip_token, part))

        def dashed(match: re.Match[str]) -> str:
            canonical = _canonical_ip(match.group(0).replace("-", "."))
            if canonical is None:
                return match.group(0)
            kind = IP_INT if is_internal_ip(canonical) else IP_EXT
            return self.map.token_for(kind, f"ip:{canonical}", canonical)

        return _outside_tokens(text, lambda part: DASHED_IPV4_RE.sub(dashed, part))

    def _names(self) -> re.Pattern[str] | None:
        users = self.map.user_tokens()
        if self._pattern_size != len(users):
            self._pattern = _name_pattern(list(users))
            self._pattern_size = len(users)
        return self._pattern

    def _replace_names(self, text: str) -> str:
        pattern = self._names()
        if pattern is None:
            return text
        tokens = self.map.user_tokens()

        def token(match: re.Match[str]) -> str:
            found = tokens.get(match.group(0).lower())
            if found is None:
                # re's case folding differs from str.lower() for a few letters (ſ, ı).
                found = next(
                    t
                    for name, t in tokens.items()
                    if re.fullmatch(re.escape(name), match.group(0), re.IGNORECASE)
                )
            return found

        return pattern.sub(token, text)

    # Restoring (model arguments on their way to an upstream tool).

    def restore(self, value: Any, escape: Callable[[str], str] | None = None) -> Any:
        """Return a copy of value with every placeholder replaced by its real value.

        Raises UnknownPlaceholder or MalformedPlaceholder rather than send a
        placeholder upstream, where it would silently match nothing.
        """
        if isinstance(value, str):
            return self._restore_text(value, escape)
        if isinstance(value, dict):
            return {
                self.restore(k, escape): self.restore(v, escape)
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [self.restore(item, escape) for item in value]
        return value

    def _restore_text(self, text: str, escape: Callable[[str], str] | None) -> str:
        loose = LOOSE_TOKEN_RE.search(TOKEN_RE.sub(" ", text))
        if loose:
            raise MalformedPlaceholder(
                f"{loose.group(0)!r} is not a valid placeholder; copy placeholders exactly, "
                "for example [[IP_EXT_001]]"
            )

        def real(match: re.Match[str]) -> str:
            value = self.map.value_for(match.group(0))
            if value is None:
                raise UnknownPlaceholder(f"{match.group(0)} is not a known placeholder")
            return escape(value) if escape else value

        return TOKEN_RE.sub(real, text)

    # The final check before anything is sent to the model.

    def find_leaks(self, value: Any) -> list[str]:
        """Describe real values still present in value, without naming them."""
        leaks: list[str] = []
        pattern = self._names()
        # Long names are also looked for inside other words, as the brief's
        # egress guard asks; short ones would match too much ordinary text.
        long_names = [name for name in self.map.user_tokens() if len(name) >= 6]
        for text in _strings(value):
            outside = TOKEN_RE.sub(" ", text)
            lowered = outside.lower()
            if ips_in(outside):
                leaks.append("IP address")
            if (pattern is not None and pattern.search(outside)) or any(
                name in lowered for name in long_names
            ):
                leaks.append("known username")
            if any(real in lowered for real in self._secrets):
                leaks.append("tenant value")
        return leaks


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _normal_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(key).lower())


def _collect_names(value: Any, names: set[str], in_user_object: bool) -> None:
    if isinstance(value, str):
        _collect_from_text(value, names)
    elif isinstance(value, list):
        for item in value:
            _collect_names(item, names, in_user_object)
    elif isinstance(value, dict):
        for key, item in value.items():
            normal = _normal_key(key)
            is_user_field = normal in _USER_KEYS or (
                in_user_object and normal in _USER_OBJECT_KEYS
            )
            if is_user_field:
                for text in _flat_strings(item):
                    if _is_name(_base_name(text)):
                        names.add(_base_name(text))
            # UDM nests user fields under principal.user, target.user and so on.
            _collect_names(item, names, in_user_object=normal.endswith("user"))


def _flat_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _flat_strings(item)


def _collect_from_text(text: str, names: set[str]) -> None:
    for match in _PROFILE_RE.finditer(text):
        candidate = (match.group(1) or match.group(2) or match.group(3) or "").strip()
        # A profile name with spaces may run into other words; learn its first word too.
        for name in {candidate, candidate.split()[0] if candidate else ""}:
            if _is_name(name):
                names.add(name)
    for match in _DOMAIN_USER_RE.finditer(text):
        domain, candidate = match.group(1), match.group(2).rstrip(".")
        if (
            domain.lower() not in _NOT_A_DOMAIN
            and not _FILE_NAME_RE.search(candidate)
            and _is_name(candidate)
        ):
            names.add(candidate)
    for pattern in (_SLASH_USER_RE, _PSEXEC_USER_RE, _EMAIL_RE):
        for match in pattern.finditer(text):
            candidate = match.group(1).rstrip(".")
            if _is_name(candidate):
                names.add(candidate)
    for match in _SID_RE.finditer(text):
        names.add(match.group(0))
