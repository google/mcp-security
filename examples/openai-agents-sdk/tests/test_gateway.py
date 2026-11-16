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
"""Gateway tests against in-memory fake Chronicle and GTI servers.

The agent side is a real MCP client session connected to the gateway, so
these tests see exactly what the agent (and so OpenAI) would see.
"""

import asyncio
import contextlib
import json
import stat

import pytest
from mcp import types
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.shared.memory import create_connected_server_and_client_session as connect

from redacting_gateway.gateway import (
    CHRONICLE,
    GTI,
    TENANT_ARGS,
    Config,
    Gateway,
    MissingToolsError,
    Upstream,
    build_server,
    classify_error,
    map_problems,
    open_private,
)
from redacting_gateway.redaction import Redactor, TokenMap

TENANT = {"project_id": "test-project", "customer_id": "test-customer", "region": "us"}
SID = "S-1-5-21-1111111111-2222222222-3333333333-1104"
CANARIES = [
    "zqcanary",
    "Quinn Zcanary",
    SID,
    "zrcanary",
    "zpcanary",
    "10.20.30.40",
    "203.0.113.77",
    "198.51.100.23",
    "2001:db8::77",
    "test-project",
    "test-customer",
    "203.0.113.99",
]

ALERT = {
    "id": "de_alert_1",
    "principal": {
        "hostname": "ZQCANARY-LT",
        "ip": ["10.20.30.40"],
        "user": {
            "userid": "CORP\\zqcanary",
            "user_display_name": "Quinn Zcanary",
            "windows_sid": SID,
        },
    },
    "target": {"ip": ["203.0.113.77", "2001:db8::77"]},
    "description": "powershell download cradle by zqcanary",
}


def fake_chronicle(calls: list, *, with_udm_search: bool = True) -> FastMCP:
    server = FastMCP("fake-chronicle")

    @server.tool()
    def get_security_alert(
        project_id: str, customer_id: str, region: str, alert_id: str
    ) -> dict:
        calls.append(
            (
                "get_security_alert",
                {
                    "project_id": project_id,
                    "customer_id": customer_id,
                    "region": region,
                    "alert_id": alert_id,
                },
            )
        )
        # Real Chronicle results echo the tenant in resource names.
        name = f"projects/{project_id}/locations/{region}/instances/{customer_id}/alerts/{alert_id}"
        return {**ALERT, "name": name}

    if with_udm_search:

        @server.tool()
        def udm_search(
            project_id: str, customer_id: str, region: str, query: str
        ) -> dict:
            """Search UDM events, for example principal.ip = "203.0.113.99"."""
            calls.append(("udm_search", {"query": query}))
            return {
                "events": [
                    {
                        "command_line": "runas /user:CORP\\zrcanary powershell -File C:\\Users\\zpcanary\\a.ps1"
                    },
                    {
                        "summary": "zqcanary connected from 10.20.30.40 to 198[.]51[.]100[.]23:443"
                    },
                ]
            }

    @server.tool()
    def list_security_alerts(project_id: str, customer_id: str, region: str) -> dict:
        calls.append(("list_security_alerts", {}))
        return {"alerts": []}

    @server.tool()
    def get_rule(project_id: str, customer_id: str, region: str, rule_id: str) -> dict:
        calls.append(("get_rule", {"rule_id": rule_id}))
        raise ToolError(
            "NOT_FOUND: rule does not exist; last edited by zqcanary from 203.0.113.77"
        )

    @server.tool()
    def summarize_entity(
        project_id: str, customer_id: str, region: str, value: str
    ) -> dict:
        calls.append(("summarize_entity", {"value": value}))
        raise ToolError("429 RESOURCE_EXHAUSTED: quota exceeded")

    @server.tool()
    def create_rule(
        project_id: str, customer_id: str, region: str, rule_text: str
    ) -> dict:
        calls.append(("create_rule", {}))
        return {"created": True}

    @server.tool()
    def list_rules(project_id: str, customer_id: str, region: str) -> dict:
        return {"rules": []}

    return server


def fake_gti(calls: list) -> FastMCP:
    server = FastMCP("fake-gti")

    @server.tool()
    def get_ip_address_report(ip_address: str) -> dict:
        calls.append(("get_ip_address_report", {"ip_address": ip_address}))
        if ip_address == "198.51.100.23":
            return {
                "error": "VirusTotal API Error: NotFoundError - Resource not found",
                "details": f"The requested ip_address '{ip_address}' could not be found.",
            }
        if ip_address == "2001:db8::77":
            return {
                "error": "VirusTotal API Error: QuotaExceededError - Quota exceeded"
            }
        return {
            "id": ip_address,
            "attributes": {
                "whois": "Registrant: zqcanary@corp.example.com",
                "reputation": -12,
            },
        }

    @server.tool()
    def get_file_report(hash: str) -> dict:
        calls.append(("get_file_report", {"hash": hash}))
        raise RuntimeError(f"internal failure for {hash} owned by zqcanary")

    @server.tool()
    def analyse_file(file_path: str) -> dict:
        calls.append(("analyse_file", {"file_path": file_path}))
        return {"uploaded": True}

    return server


class Agent:
    """The agent side of the gateway, recording everything it receives."""

    def __init__(self, session) -> None:
        self.session = session
        self.seen: list[str] = []

    async def tools(self) -> list:
        tools = (await self.session.list_tools()).tools
        self.seen.append(json.dumps([tool.model_dump() for tool in tools]))
        return tools

    async def call(self, name: str, **arguments) -> dict:
        result = await self.session.call_tool(name, arguments)
        text = result.content[0].text
        self.seen.append(text)
        body = (
            json.loads(text.split("\n[truncated:")[0])
            if "[truncated:" not in text
            else {"text": text}
        )
        body["is_error"] = result.isError
        return body


@contextlib.asynccontextmanager
async def running_gateway(tmp_path, **options):
    calls: list = []
    async with (
        connect(fake_chronicle(calls)) as chronicle_session,
        connect(fake_gti(calls)) as gti_session,
    ):
        gateway = Gateway(
            [
                Upstream(CHRONICLE, chronicle_session, tenant=TENANT),
                Upstream(GTI, gti_session),
            ],
            Redactor(
                TokenMap(run_id="test"),
                secrets={"test-project": "[project]", "test-customer": "[customer]"},
            ),
            map_path=tmp_path / "map.json",
            **options,
        )
        await gateway.load_tools()
        async with connect(build_server(gateway)) as agent_session:
            yield gateway, Agent(agent_session), calls


def assert_no_canaries(agent: Agent) -> None:
    seen = "\n".join(agent.seen).lower()
    assert [canary for canary in CANARIES if canary.lower() in seen] == []


async def test_agent_sees_only_allowlisted_read_tools(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, _):
        names = {tool.name for tool in await agent.tools()}
    assert names == {
        "get_security_alert",
        "udm_search",
        "list_security_alerts",
        "get_rule",
        "summarize_entity",
        "get_ip_address_report",
        "get_file_report",
    }


async def test_tenant_arguments_are_hidden_and_filled_in(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        tools = {tool.name: tool for tool in await agent.tools()}
        await agent.call("get_security_alert", alert_id="de_alert_1")
    schema = tools["get_security_alert"].inputSchema
    assert not set(TENANT_ARGS) & set(schema["properties"])
    assert not set(TENANT_ARGS) & set(schema.get("required", []))
    assert calls == [("get_security_alert", {**TENANT, "alert_id": "de_alert_1"})]


async def test_real_values_are_restored_only_on_the_way_upstream(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
        user = alert["result"]["principal"]["user"]["userid"].split("\\")[-1]
        external = alert["result"]["target"]["ip"][0]
        await agent.call(
            "udm_search", query=f'principal.user.userid = "CORP\\\\{user}"'
        )
        report = await agent.call("get_ip_address_report", ip_address=external)
    assert alert["status"] == "OK"
    assert (
        "udm_search",
        {"query": 'principal.user.userid = "CORP\\\\zqcanary"'},
    ) in calls
    assert ("get_ip_address_report", {"ip_address": "203.0.113.77"}) in calls
    assert report["status"] == "OK"
    assert "[[USER_" in report["result"]["attributes"]["whois"]
    assert_no_canaries(agent)


async def test_restored_values_are_escaped_for_udm_queries(tmp_path) -> None:
    async with running_gateway(tmp_path) as (gateway, agent, calls):
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
        user_token = alert["result"]["principal"]["user"]["userid"].split("\\")[-1]
        gateway._redactor.map._value_by_token[user_token] = 'CORP\\x" OR "1'
        await agent.call("udm_search", query=f'principal.user.userid = "{user_token}"')
    assert (
        "udm_search",
        {"query": 'principal.user.userid = "CORP\\\\x\\" OR \\"1"'},
    ) in calls


async def test_internal_addresses_are_never_sent_to_gti(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
        internal = alert["result"]["principal"]["ip"][0]
        result = await agent.call("get_ip_address_report", ip_address=internal)
        literal = await agent.call("get_ip_address_report", ip_address="10.9.9.9")
    assert internal.startswith("[[IP_INT_")
    assert result["status"] == literal["status"] == "SKIPPED"
    assert result["is_error"]
    assert not [call for call in calls if call[0] == "get_ip_address_report"]


@pytest.mark.parametrize("bad", ["[[IP_EXT_999]]", "ip_ext_1", "[[IP_EXT_1]]"])
async def test_bad_placeholders_are_rejected_before_any_upstream_call(
    tmp_path, bad
) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        result = await agent.call("udm_search", query=f'target.ip = "{bad}"')
    assert result["status"] == "UNRESOLVED_PLACEHOLDER"
    assert result["is_error"]
    assert calls == []


@pytest.mark.parametrize(
    ("tool", "arguments", "status"),
    [
        ("list_security_alerts", {}, "EMPTY"),
        ("get_rule", {"rule_id": "ru_1"}, "NOT_FOUND"),
        ("summarize_entity", {"value": "x"}, "QUOTA"),
        ("get_file_report", {"hash": "a" * 64}, "UPSTREAM_ERROR"),
    ],
)
async def test_results_are_classified_and_error_text_is_redacted(
    tmp_path, tool, arguments, status
) -> None:
    async with running_gateway(tmp_path) as (_, agent, _):
        await agent.call("get_security_alert", alert_id="de_alert_1")
        result = await agent.call(tool, **arguments)
    assert result["status"] == status
    assert result["is_error"] == (status not in ("OK", "EMPTY", "NOT_FOUND"))
    assert_no_canaries(agent)


async def test_gti_not_found_is_told_apart_from_quota(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
        events = await agent.call("udm_search", query="x")
        not_found_ip = (
            events["result"]["events"][1]["summary"].split(" to ")[1].split(":")[0]
        )
        not_found = await agent.call("get_ip_address_report", ip_address=not_found_ip)
        quota = await agent.call(
            "get_ip_address_report", ip_address=alert["result"]["target"]["ip"][1]
        )
        after_quota = await agent.call(
            "get_ip_address_report", ip_address=alert["result"]["target"]["ip"][0]
        )
    assert not_found["status"] == "NOT_FOUND"
    assert quota["status"] == "QUOTA"
    assert after_quota["status"] == "SKIPPED"
    assert [c[1]["ip_address"] for c in calls if c[0] == "get_ip_address_report"] == [
        "198.51.100.23",
        "2001:db8::77",
    ]
    assert_no_canaries(agent)


async def test_gti_lookups_stop_at_the_limit(tmp_path) -> None:
    async with running_gateway(tmp_path, max_gti_lookups=1) as (_, agent, calls):
        await agent.call("get_ip_address_report", ip_address="192.0.2.1")
        second = await agent.call("get_ip_address_report", ip_address="192.0.2.2")
    assert second["status"] == "SKIPPED"
    assert len([c for c in calls if c[0] == "get_ip_address_report"]) == 1


async def test_repeated_calls_are_answered_from_the_cache(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        first = await agent.call("get_security_alert", alert_id="de_alert_1")
        second = await agent.call("get_security_alert", alert_id="de_alert_1")
    assert first == second
    assert len(calls) == 1


async def test_tools_off_the_allowlist_are_denied(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        write = await agent.call("create_rule", rule_text="rule x {}")
        upload = await agent.call("analyse_file", file_path="/etc/passwd")
    assert write["status"] == upload["status"] == "DENIED"
    assert calls == []


async def test_egress_canary(tmp_path) -> None:
    """Every canary planted upstream, in fields and free text, stays local."""
    async with running_gateway(tmp_path) as (_, agent, _):
        await agent.tools()
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
        await agent.call("udm_search", query='metadata.event_type = "PROCESS_LAUNCH"')
        for ip in alert["result"]["target"]["ip"] + alert["result"]["principal"]["ip"]:
            await agent.call("get_ip_address_report", ip_address=ip)
        await agent.call("get_rule", rule_id="ru_1")
        await agent.call("get_file_report", hash="b" * 64)
    assert_no_canaries(agent)


async def test_a_redaction_bug_is_caught_by_the_leak_check(
    tmp_path, monkeypatch
) -> None:
    async with running_gateway(tmp_path) as (gateway, agent, _):
        await agent.call(
            "get_security_alert", alert_id="de_alert_1"
        )  # learn the usernames first
        monkeypatch.setattr(gateway._redactor, "redact", lambda value: value)
        result = await agent.call("udm_search", query="x")
    assert result["status"] == "REDACTION_ERROR"
    assert_no_canaries(agent)


async def test_a_redaction_crash_fails_closed(tmp_path, monkeypatch) -> None:
    async with running_gateway(tmp_path) as (gateway, agent, _):

        def broken(value):
            raise RuntimeError("zqcanary 203.0.113.77")

        monkeypatch.setattr(gateway._redactor, "redact", broken)
        result = await agent.call("get_security_alert", alert_id="de_alert_1")
    assert result["status"] == "REDACTION_ERROR"
    assert_no_canaries(agent)


async def test_long_results_are_truncated_with_a_marker(tmp_path) -> None:
    async with running_gateway(tmp_path, max_result_chars=120) as (_, agent, _):
        result = await agent.call("get_security_alert", alert_id="de_alert_1")
    assert "[truncated: showing 120 of" in result["text"]


async def test_the_map_file_is_private_and_restores_values(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, _):
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
    path = tmp_path / "map.json"
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    token = alert["result"]["target"]["ip"][0]
    assert Redactor(TokenMap.load(path)).restore(token) == "203.0.113.77"


async def test_missing_required_tools_stop_the_gateway() -> None:
    async with (
        connect(fake_chronicle([], with_udm_search=False)) as chronicle_session,
        connect(fake_gti([])) as gti_session,
    ):
        gateway = Gateway(
            [
                Upstream(CHRONICLE, chronicle_session, tenant=TENANT),
                Upstream(GTI, gti_session),
            ],
            Redactor(TokenMap()),
        )
        with pytest.raises(MissingToolsError) as raised:
            await gateway.load_tools()
    assert raised.value.missing == ["chronicle:udm_search"]


def test_preflight_names_each_missing_setting() -> None:
    config = Config.from_env({"GTI_MCP_COMMAND": "no-such-gti-command-316"})
    assert [p.code for p in config.problems(use_gti=True)] == [
        "ENV_MISSING",
        "ENV_MISSING",
        "ENV_MISSING",
        "VT_APIKEY_MISSING",
        "GTI_COMMAND_NOT_FOUND",
    ]
    assert [p.code for p in config.problems(use_gti=False)] == ["ENV_MISSING"] * 3


def test_preflight_passes_with_full_settings() -> None:
    config = Config.from_env(
        {
            "CHRONICLE_PROJECT_ID": "p",
            "CHRONICLE_CUSTOMER_ID": "c",
            "CHRONICLE_REGION": "eu",
            "VT_APIKEY": "k",
            "GTI_MCP_COMMAND": "python3 -m gti_mcp",
        }
    )
    assert config.problems(use_gti=True) == []
    assert config.chronicle_url == "https://chronicle.eu.rep.googleapis.com/mcp"
    assert config.gti_command == ["python3", "-m", "gti_mcp"]


class FailingSession:
    """An upstream whose transport fails, as when the endpoint URL is wrong."""

    def __init__(self, tools: list, error: Exception) -> None:
        self._tools = tools
        self._error = error

    async def list_tools(self, *, params=None):
        return types.ListToolsResult(tools=self._tools)

    async def call_tool(self, name, arguments=None):
        raise self._error


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (
            RuntimeError(
                "Client error '404 Not Found' for url 'https://chronicle.xx.rep.googleapis.com/mcp'"
            ),
            "UPSTREAM_ERROR",
        ),
        (RuntimeError("Client error '403 Forbidden' for user zqcanary"), "AUTH"),
        (RuntimeError("429 Too Many Requests"), "QUOTA"),
    ],
)
async def test_transport_failures_are_never_reported_as_no_evidence(
    error, status
) -> None:
    schema = {"type": "object", "properties": {"query": {"type": "string"}}}
    tools = [
        types.Tool(name=name, inputSchema=schema)
        for name in ("get_security_alert", "udm_search")
    ]
    redactor = Redactor(TokenMap())
    redactor.redact({"user": {"userid": "zqcanary"}})
    gateway = Gateway(
        [Upstream(CHRONICLE, FailingSession(tools, error), tenant=TENANT)], redactor
    )
    await gateway.load_tools()
    result = await gateway.call_tool("udm_search", {"query": "x"})
    body = json.loads(result.content[0].text)
    assert body["status"] == status
    assert result.isError
    assert "zqcanary" not in result.content[0].text


class StubSession:
    """An upstream that returns fixed results, or waits forever."""

    def __init__(
        self,
        names: list[str],
        result: types.CallToolResult | None = None,
        delay: float = 0,
    ) -> None:
        self._tools = [
            types.Tool(name=name, inputSchema={"type": "object"}) for name in names
        ]
        self.result = result
        self.delay = delay
        self.calls = 0

    async def list_tools(self, *, params=None):
        return types.ListToolsResult(tools=self._tools)

    async def call_tool(self, name, arguments=None):
        self.calls += 1
        await asyncio.sleep(self.delay)
        return self.result


def text_result(payload, is_error=False) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=json.dumps(payload))],
        isError=is_error,
    )


async def stub_gateway(result=None, delay=0.0, **options):
    session = StubSession(["get_security_alert", "udm_search"], result, delay)
    gateway = Gateway(
        [Upstream(CHRONICLE, session, tenant=TENANT)], Redactor(TokenMap()), **options
    )
    await gateway.load_tools()
    return gateway, session


async def body_of(gateway, name="udm_search", **arguments):
    result = await gateway.call_tool(name, arguments or {"query": "x"})
    return json.loads(result.content[0].text), result.isError


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("File 4291ab0c not found", "UPSTREAM_ERROR"),
        ("syntax error at line 401", "UPSTREAM_ERROR"),
        ("field principal.foo not found", "UPSTREAM_ERROR"),
        ("HTTP 403 Forbidden: caller lacks permission", "AUTH"),
        ("HTTP 429 Too Many Requests: slow down", "QUOTA"),
        ("NOT_FOUND: alert does not exist", "NOT_FOUND"),
    ],
)
def test_error_text_is_classified_without_false_matches(text, status) -> None:
    assert classify_error(text) == status


@pytest.mark.parametrize(
    ("result", "status"),
    [
        (
            types.CallToolResult(
                content=[
                    types.ImageContent(type="image", data="AA==", mimeType="image/png")
                ]
            ),
            "UPSTREAM_ERROR",
        ),
        (text_result({"error": {"code": 500}}), "UPSTREAM_ERROR"),
        (text_result({"error": ["boom"]}), "UPSTREAM_ERROR"),
        (text_result({"events": [], "total": 0}), "EMPTY"),
    ],
)
async def test_results_that_hold_no_answer_are_not_reported_as_answers(
    result, status
) -> None:
    gateway, _ = await stub_gateway(result)
    body, is_error = await body_of(gateway)
    assert body["status"] == status
    assert is_error == (status != "EMPTY")


async def test_a_hung_upstream_times_out_with_a_status() -> None:
    gateway, _ = await stub_gateway(text_result({"ok": 1}), delay=10, call_timeout=0.05)
    body, is_error = await body_of(gateway)
    assert body["status"] == "UPSTREAM_ERROR" and is_error


async def test_identical_concurrent_calls_share_one_upstream_request() -> None:
    gateway, session = await stub_gateway(text_result({"events": [1]}), delay=0.05)
    bodies = await asyncio.gather(*(body_of(gateway) for _ in range(5)))
    assert session.calls == 1
    assert {body["status"] for body, _ in bodies} == {"OK"}


async def test_queued_gti_calls_stop_after_a_quota_error() -> None:
    session = StubSession(
        ["get_ip_address_report"],
        text_result({"error": "QuotaExceededError"}),
        delay=0.02,
    )
    gateway = Gateway([Upstream(GTI, session, concurrency=1)], Redactor(TokenMap()))
    await gateway.load_tools()
    results = await asyncio.gather(
        *(
            gateway.call_tool("get_ip_address_report", {"ip_address": f"192.0.2.{n}"})
            for n in range(1, 6)
        )
    )
    statuses = [json.loads(r.content[0].text)["status"] for r in results]
    assert session.calls == 1
    assert statuses == ["QUOTA"] + ["SKIPPED"] * 4


async def test_usernames_are_never_sent_to_gti(tmp_path) -> None:
    async with running_gateway(tmp_path) as (_, agent, calls):
        alert = await agent.call("get_security_alert", alert_id="de_alert_1")
        user = alert["result"]["principal"]["user"]["userid"].split("\\")[-1]
        result = await agent.call("get_file_report", hash=user)
    assert result["status"] == "SKIPPED"
    assert not [c for c in calls if c[0] == "get_file_report"]


async def test_a_map_that_cannot_be_saved_withholds_the_result(tmp_path) -> None:
    gateway, _ = await stub_gateway(
        text_result({"ip": "203.0.113.5"}), map_path=tmp_path / "missing" / "map.json"
    )
    body, is_error = await body_of(gateway)
    assert body["status"] == "REDACTION_ERROR" and is_error
    assert "missing" not in body["error"]


@pytest.mark.parametrize("region", ["evil.com/x#", "us.evil.com", "x?y", "US"])
def test_a_region_that_would_change_the_host_is_refused(region) -> None:
    config = Config.from_env(
        {
            "CHRONICLE_PROJECT_ID": "p",
            "CHRONICLE_CUSTOMER_ID": "c",
            "CHRONICLE_REGION": region,
        }
    )
    assert "REGION_INVALID" in [p.code for p in config.problems(use_gti=False)]


@pytest.mark.parametrize("command", ['uv "run', "   "])
def test_a_bad_gti_command_is_reported(command) -> None:
    config = Config.from_env({"GTI_MCP_COMMAND": command})
    assert "GTI_COMMAND_INVALID" in [p.code for p in config.problems(use_gti=True)]


def test_each_run_needs_a_new_map_in_an_existing_directory(tmp_path) -> None:
    assert [p.code for p in map_problems(tmp_path / "nope" / "map.json")] == [
        "MAP_DIR_MISSING"
    ]
    (tmp_path / "map.json").write_text("{}")
    assert [p.code for p in map_problems(tmp_path / "map.json")] == ["MAP_EXISTS"]
    assert map_problems(tmp_path / "new.json") == []


def test_an_existing_log_is_made_private(tmp_path) -> None:
    log = tmp_path / "gateway.log"
    log.write_text("")
    log.chmod(0o644)
    with open_private(log):
        pass
    assert stat.S_IMODE(log.stat().st_mode) == 0o600
