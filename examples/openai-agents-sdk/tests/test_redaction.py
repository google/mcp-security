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
"""Tests for the redaction core. All data is synthetic."""

import json
import random
import stat

import pytest

from redacting_gateway.redaction import (
    TOKEN_RE,
    MalformedPlaceholder,
    MapVersionError,
    Redactor,
    TokenMap,
    UnknownPlaceholder,
)

SID = "S-1-5-21-1111111111-2222222222-3333333333-1104"


def redactor() -> Redactor:
    return Redactor(TokenMap(run_id="test"))


def tokens_in(text: str) -> list[str]:
    return [m.group(0) for m in TOKEN_RE.finditer(text)]


@pytest.mark.parametrize(
    "forms",
    [
        [
            "198.51.100.7",
            "198[.]51[.]100[.]7",
            "198.51.100.7:443",
            "::ffff:198.51.100.7",
        ],
        [
            "2001:db8::1",
            "2001:0db8:0000:0000:0000:0000:0000:0001",
            "[2001:db8::1]:8443",
        ],
        ["10.1.2.3", "ip-10-1-2-3.example.internal", "10(.)1(.)2(.)3"],
    ],
)
def test_every_form_of_an_ip_gets_one_placeholder(forms) -> None:
    r = redactor()
    found = {token for form in forms for token in tokens_in(r.redact(form))}
    assert len(found) == 1
    assert r.find_leaks([r.redact(form) for form in forms]) == []


@pytest.mark.parametrize(
    ("address", "kind"),
    [
        ("10.1.2.3", "IP_INT"),
        ("172.16.5.4", "IP_INT"),
        ("192.168.1.5", "IP_INT"),
        ("100.64.0.9", "IP_INT"),
        ("127.0.0.1", "IP_INT"),
        ("fe80::1", "IP_INT"),
        ("fd00::7", "IP_INT"),
        ("203.0.113.9", "IP_EXT"),
        ("192.0.2.44", "IP_EXT"),
        ("2001:db8::9", "IP_EXT"),
    ],
)
def test_ips_are_typed_internal_or_external(address, kind) -> None:
    assert tokens_in(redactor().redact(f"conn to {address}")) == [f"[[{kind}_001]]"]


@pytest.mark.parametrize(
    "text",
    [
        "at 10:15:30",
        "mac 00:1a:2b:3c:4d:5e",
        "999.1.1.1",
        "version 1.2.3",
        "port 443",
        "std::vector",
    ],
)
def test_strings_that_are_not_ips_are_unchanged(text) -> None:
    assert redactor().redact(text) == text


def test_all_forms_of_a_user_collapse_to_one_placeholder() -> None:
    r = redactor()
    result = r.redact(
        {
            "note": "zqcanary logged in from ZQCANARY-LT then ZQCANARY_laptop",
            "principal": {
                "user": {
                    "userid": "CORP\\zqcanary",
                    "email_addresses": ["zqcanary@corp.example.com"],
                }
            },
        }
    )
    text = json.dumps(result)
    assert set(tokens_in(text)) == {"[[USER_001]]"}
    assert "[[USER_001]]-LT" in text
    assert "[[USER_001]]_laptop" in text
    assert "corp.example.com" in text
    assert "CORP" in text


def test_names_in_free_text_before_their_field_are_still_replaced() -> None:
    result = redactor().redact(
        {"a_first": "seen zqcanary", "z_last": {"user": {"userid": "zqcanary"}}}
    )
    assert result["a_first"] == "seen [[USER_001]]"


def test_display_names_and_sids_are_redacted() -> None:
    r = redactor()
    result = r.redact(
        {
            "target": {
                "user": {"user_display_name": "Quinn Zcanary", "windows_sid": SID}
            },
            "log": f"sid {SID}",
        }
    )
    text = json.dumps(result)
    assert "Quinn" not in text and SID not in text
    assert r.find_leaks(result) == []


@pytest.mark.parametrize(
    ("text", "name"),
    [
        ("C:\\Users\\zpcanary\\AppData\\x.ps1", "zpcanary"),
        ("/home/zpcanary/.ssh/id_rsa", "zpcanary"),
        ("/Users/zpcanary/Downloads", "zpcanary"),
        ("runas /user:CORP\\zrcanary cmd.exe", "zrcanary"),
        ('net use \\\\fs01\\share /user:"zrcanary" x', "zrcanary"),
        ("psexec \\\\host01 -u CORP\\zscanary cmd", "zscanary"),
        ("logon by CORP\\zdcanary failed", "zdcanary"),
        ("mail from zecanary@corp.example.com", "zecanary"),
    ],
)
def test_usernames_found_by_pattern(text, name) -> None:
    result = redactor().redact(text)
    assert name not in result
    assert "[[USER_001]]" in result


@pytest.mark.parametrize(
    "text",
    [
        "C:\\Windows\\System32\\cmd.exe",
        "HKLM\\SOFTWARE\\Microsoft\\Windows",
        "ran as NT AUTHORITY\\SYSTEM",
        "/root/.bashrc",
        "C:\\Users\\Public\\x.txt",
        "report to abuse@registrar.example.com",
    ],
)
def test_paths_and_built_in_accounts_stay_visible(text) -> None:
    assert redactor().redact(text) == text


def test_built_in_user_fields_stay_visible() -> None:
    result = redactor().redact(
        {
            "principal": {"user": {"userid": "Administrator"}},
            "t": {"user": {"userid": "root"}},
        }
    )
    assert result == {
        "principal": {"user": {"userid": "Administrator"}},
        "t": {"user": {"userid": "root"}},
    }


@pytest.mark.parametrize("name", ["svc_backup", "backup-svc", "SQLService", "WS01$"])
def test_service_accounts_get_svc_placeholders(name) -> None:
    assert redactor().redact({"user": {"userid": name}}) == {
        "user": {"userid": "[[SVC_001]]"}
    }


def test_a_username_never_corrupts_placeholders() -> None:
    r = redactor()
    result = r.redact(
        {"user": {"userid": "user"}, "note": "user from 203.0.113.5 and 10.0.0.8"}
    )
    assert result["note"] == "[[USER_001]] from [[IP_EXT_001]] and [[IP_INT_001]]"


def test_placeholder_lookalikes_from_upstream_cannot_be_restored() -> None:
    r = redactor()
    result = r.redact("attacker wrote [[USER_001]] here")
    assert tokens_in(result) == []
    assert len(r.map) == 0


def test_round_trip_restores_every_value() -> None:
    rng = random.Random(316)
    ips = [
        "10.0.0.1",
        "10.0.0.12",
        "192.168.7.7",
        "203.0.113.1",
        "203.0.113.12",
        "2001:db8::5",
    ]
    names = ["zqcanary", "zrcanary", "Quinn Zcanary", "svc_zbackup"]
    words = ["login", "from", "to", "via", "failed", "port", "443", "-", ":", "/"]
    r = redactor()
    r.redact({"users": [{"user": {"userid": name}} for name in names]})
    for _ in range(300):
        text = " ".join(
            rng.choice(ips + names + words) for _ in range(rng.randint(1, 12))
        )
        redacted = r.redact(text)
        assert r.find_leaks(redacted) == []
        assert r.restore(redacted) == text


def test_redaction_is_deterministic() -> None:
    data = {
        "a": "203.0.113.3 then 10.0.0.4",
        "user": {"userid": "zqcanary", "user_display_name": "Quinn Zcanary"},
    }
    assert redactor().redact(data) == redactor().redact(data)


def test_numbered_placeholders_never_collide() -> None:
    r = redactor()
    redacted = r.redact(" ".join(f"203.0.113.{n}" for n in range(1, 13)))
    assert "[[IP_EXT_001]]" in redacted and "[[IP_EXT_012]]" in redacted
    assert r.restore("[[IP_EXT_001]]") == "203.0.113.1"
    assert r.restore("[[IP_EXT_012]]") == "203.0.113.12"


def test_restore_escapes_values_when_asked() -> None:
    r = redactor()
    token = r.redact("logon by CORP\\zdcanary").split("\\")[-1]
    assert (
        r.restore(f'user = "CORP\\\\{token}"', escape=lambda v: v.upper())
        == 'user = "CORP\\\\ZDCANARY"'
    )


@pytest.mark.parametrize("text", ["[[IP_EXT_999]]", "[[USER_002]]"])
def test_unknown_placeholders_are_rejected(text) -> None:
    r = redactor()
    r.redact("203.0.113.1 and {'user': 'x'}")
    with pytest.raises(UnknownPlaceholder):
        r.restore(text)


@pytest.mark.parametrize(
    "text",
    ["ip_ext_001", "IP_12", "[[IP_EXT_1]]", "[[user_001]]", "USER-3", "svc_7 host"],
)
def test_malformed_placeholders_are_rejected(text) -> None:
    r = redactor()
    r.redact("203.0.113.1")
    with pytest.raises(MalformedPlaceholder):
        r.restore(text)


def test_find_leaks_reports_real_values_without_naming_them() -> None:
    r = redactor()
    r.redact({"user": {"userid": "zqcanary"}})
    leaks = r.find_leaks({"x": "zqcanary at 203.0.113.9"})
    assert sorted(leaks) == ["IP address", "known username"]
    assert all("zqcanary" not in leak for leak in leaks)


def test_map_round_trips_through_a_private_file(tmp_path) -> None:
    r = redactor()
    r.redact({"user": {"userid": "zqcanary"}, "ip": "203.0.113.9"})
    path = tmp_path / "map.json"
    r.map.save(path)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    loaded = Redactor(TokenMap.load(path))
    assert loaded.restore("[[USER_001]] [[IP_EXT_001]]") == "zqcanary 203.0.113.9"
    # Numbering continues after a reload instead of reusing a placeholder.
    assert loaded.redact("203.0.113.10") == "[[IP_EXT_002]]"
    assert not list(tmp_path.glob(".map.json.*"))


def test_map_rejects_an_unknown_version(tmp_path) -> None:
    path = tmp_path / "map.json"
    path.write_text(json.dumps({"version": 99, "entries": []}))
    with pytest.raises(MapVersionError):
        TokenMap.load(path)


def test_canaries_never_survive_redaction() -> None:
    canaries = [
        "zqcanary",
        "Quinn Zcanary",
        SID,
        "zpcanary",
        "zrcanary",
        "10.20.30.40",
        "203.0.113.77",
        "2001:db8::77",
    ]
    alert = {
        "principal": {
            "user": {
                "userid": "CORP\\zqcanary",
                "user_display_name": "Quinn Zcanary",
                "windows_sid": SID,
            }
        },
        "target": {"ip": ["203.0.113.77", "2001:db8::77"]},
        "events": [
            {
                "command_line": "runas /user:CORP\\zrcanary powershell -File C:\\Users\\zpcanary\\a.ps1"
            },
            {
                "summary": "zqcanary connected from 10.20.30.40 to 203[.]0[.]113[.]77:443"
            },
        ],
    }
    r = redactor()
    text = json.dumps(r.redact(alert), ensure_ascii=False).lower()
    assert [c for c in canaries if c.lower() in text] == []
    assert r.find_leaks(text) == []


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("from 010.001.002.003 now", "10.1.2.3"),
        ("host a.10.0.0.7 seen", "10.0.0.7"),
        ("addr x_2001:db8::3 seen", "2001:db8::3"),
        ("ip:2001:db8::6 seen", "2001:db8::6"),
        ("203-0-113-5.static.example.net", "203.0.113.5"),
    ],
)
def test_more_ip_forms_are_redacted(text, value) -> None:
    r = redactor()
    redacted = r.redact(text)
    assert value not in redacted and r.find_leaks(redacted) == []
    assert value in r.restore(redacted)


def test_unicode_email_local_parts_are_learned_whole() -> None:
    r = redactor()
    assert r.redact("mail from jörg@corp.example.com and later jörg") == (
        "mail from [[USER_001]]@corp.example.com and later [[USER_001]]"
    )


def test_nested_lists_in_user_fields_are_learned() -> None:
    result = redactor().redact(
        {"user": {"userid": ["zqcanary", ["zrcanary"]]}, "note": "zrcanary"}
    )
    assert result["note"] == "[[USER_002]]"


@pytest.mark.parametrize(
    "text",
    [
        "ran as NT AUTHORITY\\NETWORK SERVICE on the network",
        "IIS APPPOOL\\DefaultAppPool",
        "C:\\Temp\\payload.exe",
    ],
)
def test_built_in_two_word_accounts_and_paths_are_not_learned(text) -> None:
    r = redactor()
    assert r.redact(text) == text
    assert len(r.map) == 0


def test_profile_names_with_spaces_are_learned() -> None:
    redacted = redactor().redact(
        "C:\\Users\\Quinn Zqspace\\Desktop\\a.ps1 then Quinn Zqspace logged off"
    )
    assert "Zqspace" not in redacted


def test_unusual_case_folding_does_not_crash() -> None:
    r = redactor()
    r.redact({"user": {"userid": "zsam"}})
    assert r.redact("by zſam") == "by [[USER_001]]"


def test_stored_casing_does_not_depend_on_set_order() -> None:
    r = redactor()
    r.redact({"a": {"user": {"userid": "jdoez"}}, "b": {"user": {"userid": "JDoez"}}})
    assert r.restore("[[USER_001]]") == "JDoez"


def test_placeholders_in_dict_keys_are_restored_and_checked() -> None:
    r = redactor()
    r.redact("203.0.113.1")
    assert r.restore({"[[IP_EXT_001]]": 1}) == {"203.0.113.1": 1}
    with pytest.raises(MalformedPlaceholder):
        r.restore({"ip_ext_1": 1})


def test_tenant_values_are_replaced_by_labels() -> None:
    r = Redactor(
        TokenMap(), secrets={"zq-project-316": "[project]", "ab": "[too-short]"}
    )
    redacted = r.redact("projects/ZQ-PROJECT-316/instances/x and ab")
    assert redacted == "projects/[project]/instances/x and ab"
    assert r.find_leaks("projects/zq-project-316") == ["tenant value"]


def test_long_text_without_at_signs_stays_fast() -> None:
    import time

    start = time.perf_counter()
    redactor().redact("a" * 200_000)
    assert time.perf_counter() - start < 1.0


def test_many_rows_with_distinct_values_stay_fast() -> None:
    import time

    rows = [
        {
            "user": {"userid": f"zuser{n:04d}"},
            "ip": f"10.0.{n // 250}.{n % 250}",
            "msg": f"zuser{n:04d} ok",
        }
        for n in range(2000)
    ]
    start = time.perf_counter()
    redactor().redact(rows)
    assert time.perf_counter() - start < 3.0
