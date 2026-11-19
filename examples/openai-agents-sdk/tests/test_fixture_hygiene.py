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
"""Leak scan: this example must never commit real tenant data or credentials.

Test data may only use documentation IP ranges (RFC 5737, RFC 3849) and
private or loopback addresses, which identify no one.
"""

import ipaddress
import re
from pathlib import Path

import pytest

from redacting_gateway.redaction import ips_in

ROOT = Path(__file__).resolve().parents[1]
FILES = sorted(
    path
    for path in ROOT.rglob("*")
    if path.is_file()
    and path.suffix in {".py", ".json", ".md", ".toml", ".txt", ".yaml", ".yml"}
    and ".venv" not in path.parts
)
ALLOWED_NETWORKS = [
    ipaddress.ip_network(net)
    for net in (
        "192.0.2.0/24",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "2001:db8::/32",
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "100.64.0.0/10",
        "127.0.0.0/8",
        "169.254.0.0/16",
        "::/128",
        "::1/128",
        "fc00::/7",
        "fe80::/10",
    )
]
SECRET_PATTERNS = [
    re.compile(r"ya29\.[0-9A-Za-z_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"sk-[A-Za-z0-9_-]{32,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
]


@pytest.mark.parametrize("path", FILES, ids=lambda path: str(path.relative_to(ROOT)))
def test_file_has_no_real_ips_or_secrets(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    bad_ips = [
        ip
        for ip in ips_in(text)
        if not any(
            ipaddress.ip_address(ip) in net
            for net in ALLOWED_NETWORKS
            if net.version == ipaddress.ip_address(ip).version
        )
    ]
    assert bad_ips == []
    assert [
        pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text)
    ] == []
