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
"""Local MCP gateway between the agent and the SecOps tools.

The agent reaches this gateway over stdio. The gateway:
  * holds the Google Cloud token and VT_APIKEY, which never reach the agent;
  * exposes only the read-only tools in ALLOWED_TOOLS;
  * fills in the Chronicle tenant arguments itself and hides them in results;
  * restores real values in tool arguments and redacts every result,
    including error text, then checks the result for leaks;
  * labels every result with a status, so a failed lookup is never
    mistaken for "no evidence".
"""

import argparse
import asyncio
import contextlib
import copy
import enum
import json
import logging
import os
import re
import shlex
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import httpx
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from .auth import GoogleAuthTransport
from .redaction import (
    SVC,
    TOKEN_RE,
    USER,
    PlaceholderError,
    Redactor,
    TokenMap,
    ips_in,
    is_internal_ip,
)

logger = logging.getLogger(__name__)

CHRONICLE = "chronicle"
GTI = "gti"

# Read-only tools only. Everything else the upstream servers offer, including
# every tool that writes or uploads, is hidden from the agent.
ALLOWED_TOOLS = {
    CHRONICLE: frozenset(
        {
            "get_security_alert",
            "list_security_alerts",
            "udm_search",
            "translate_udm_query",
            "summarize_entity",
            "get_ioc_match",
            "get_rule",
            "list_rule_detections",
        }
    ),
    GTI: frozenset(
        {
            "get_ip_address_report",
            "get_domain_report",
            "get_file_report",
            "get_url_report",
        }
    ),
}
assert not ALLOWED_TOOLS[CHRONICLE] & ALLOWED_TOOLS[GTI], "tool names must be unique"
REQUIRED_TOOLS = {
    CHRONICLE: frozenset({"get_security_alert", "udm_search"}),
    GTI: frozenset({"get_ip_address_report"}),
}
TENANT_ARGS = ("project_id", "customer_id", "region")
# Restored values in these arguments are escaped for UDM string literals.
UDM_QUERY_ARGS = frozenset({("udm_search", "query")})

DEFAULT_GTI_COMMAND = [
    "uv",
    "run",
    "--directory",
    str(Path(__file__).resolve().parents[3] / "server" / "gti"),
    "gti_mcp",
]


class Status(enum.StrEnum):
    OK = "OK"
    EMPTY = "EMPTY"
    NOT_FOUND = "NOT_FOUND"
    AUTH = "AUTH"
    QUOTA = "QUOTA"
    UPSTREAM_ERROR = "UPSTREAM_ERROR"
    REDACTION_ERROR = "REDACTION_ERROR"
    UNRESOLVED_PLACEHOLDER = "UNRESOLVED_PLACEHOLDER"
    DENIED = "DENIED"
    SKIPPED = "SKIPPED"


# Statuses that carry an answer. Every other status means the lookup did not happen.
ANSWER_STATUSES = frozenset({Status.OK, Status.EMPTY, Status.NOT_FOUND})

# Matched against error text. Bare status codes are not used, because a hash
# or a line number can contain "429" or "401". When in doubt the result is an
# error, never an answer: a false "not found" is the worst outcome.
_ERROR_PATTERNS = (
    (
        Status.QUOTA,
        re.compile(
            r"quota|resource_exhausted|rate.?limit|too many requests", re.IGNORECASE
        ),
    ),
    (
        Status.AUTH,
        re.compile(
            r"unauthenticated|unauthorized|permission_denied|permission denied|forbidden"
            r"|wrongcredentials|authenticationrequired",
            re.IGNORECASE,
        ),
    ),
    (Status.NOT_FOUND, re.compile(r"NotFoundError|\bNOT_FOUND\b|\b404 Not Found\b")),
)
_REGION_RE = re.compile(r"[a-z0-9-]{1,40}")


class MissingToolsError(RuntimeError):
    """An upstream server does not offer a tool the gateway requires."""

    def __init__(self, missing: list[str]) -> None:
        super().__init__("Required tools are missing: " + ", ".join(missing))
        self.missing = missing


class ToolSession(Protocol):
    async def list_tools(
        self, *, params: types.PaginatedRequestParams | None = None
    ) -> types.ListToolsResult: ...

    async def call_tool(
        self, name: str, arguments: dict[str, Any] | None = None
    ) -> types.CallToolResult: ...


@dataclass
class Upstream:
    name: str
    session: ToolSession
    tenant: dict[str, str] = field(default_factory=dict)
    concurrency: int = 4

    def __post_init__(self) -> None:
        self.limit = asyncio.Semaphore(self.concurrency)


def classify_error(text: str) -> Status:
    for status, pattern in _ERROR_PATTERNS:
        if pattern.search(text):
            return status
    return Status.UPSTREAM_ERROR


def _is_empty(payload: Any) -> bool:
    if payload in (None, "", [], {}):
        return True
    if isinstance(payload, dict):
        return all(value in (None, "", [], {}, 0, False) for value in payload.values())
    return False


def escape_udm_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


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


class Gateway:
    """Applies the allowlist, redaction and result checks to every call."""

    def __init__(
        self,
        upstreams: list[Upstream],
        redactor: Redactor,
        *,
        map_path: Path | None = None,
        max_result_chars: int = 24_000,
        max_gti_lookups: int = 25,
        call_timeout: float = 120.0,
    ) -> None:
        self._upstreams = upstreams
        self._redactor = redactor
        self._map_path = map_path
        self._max_result_chars = max_result_chars
        self._max_gti_lookups = max_gti_lookups
        self._call_timeout = call_timeout
        self._tools: dict[str, tuple[Upstream, types.Tool]] = {}
        self._cache: dict[str, types.CallToolResult] = {}
        self._in_flight: dict[str, asyncio.Task[types.CallToolResult]] = {}
        self._gti_lookups = 0
        self._gti_stopped = False
        self._saved_size = -1

    async def load_tools(self) -> None:
        """Discover upstream tools and keep the allowlisted ones.

        Raises MissingToolsError before any model call if a required tool is absent.
        """
        missing = []
        for upstream in self._upstreams:
            listed: list[types.Tool] = []
            cursor = None
            while True:
                params = types.PaginatedRequestParams(cursor=cursor) if cursor else None
                page = await upstream.session.list_tools(params=params)
                listed.extend(page.tools)
                cursor = page.nextCursor
                if not cursor:
                    break
            allowed = {
                tool.name: tool
                for tool in listed
                if tool.name in ALLOWED_TOOLS[upstream.name]
            }
            missing += [
                f"{upstream.name}:{name}"
                for name in sorted(REQUIRED_TOOLS[upstream.name] - allowed.keys())
            ]
            for tool in allowed.values():
                public = self._public_tool(upstream, tool)
                if self._redactor.find_leaks(public.model_dump()):
                    raise RuntimeError(
                        f"The definition of {tool.name} failed the leak check"
                    )
                self._tools[tool.name] = (upstream, public)
        if missing:
            raise MissingToolsError(missing)

    def _public_tool(self, upstream: Upstream, tool: types.Tool) -> types.Tool:
        schema = copy.deepcopy(tool.inputSchema)
        if upstream.tenant:
            properties = schema.get("properties", {})
            for name in TENANT_ARGS:
                properties.pop(name, None)
            if "required" in schema:
                schema["required"] = [
                    name for name in schema["required"] if name not in TENANT_ARGS
                ]
        # No outputSchema: results reach the agent only as redacted text.
        return types.Tool(
            name=tool.name,
            description=self._redactor.redact(tool.description or ""),
            inputSchema=self._redactor.redact(schema),
        )

    def list_tools(self) -> list[types.Tool]:
        return [tool for _, tool in self._tools.values()]

    async def call_tool(
        self, name: str, arguments: dict[str, Any] | None
    ) -> types.CallToolResult:
        try:
            return await self._call(name, arguments or {})
        except Exception:
            # The exception text may hold real values, so it goes to the local log only.
            logger.exception("Gateway failure in %s", name)
            return self._wrap(
                Status.UPSTREAM_ERROR, "The gateway failed while handling this call."
            )

    async def _call(self, name: str, arguments: dict[str, Any]) -> types.CallToolResult:
        entry = self._tools.get(name)
        if entry is None:
            return self._wrap(Status.DENIED, f"{name!r} is not an available tool.")
        upstream, _ = entry

        if upstream.name == GTI and any(
            match.group(1) in (USER, SVC)
            for text in _strings(arguments)
            for match in TOKEN_RE.finditer(text)
        ):
            return self._wrap(Status.SKIPPED, "Usernames are not sent to VirusTotal.")
        try:
            real_args = {
                key: self._redactor.restore(
                    value, escape_udm_string if (name, key) in UDM_QUERY_ARGS else None
                )
                for key, value in arguments.items()
            }
        except PlaceholderError as error:
            return self._wrap(Status.UNRESOLVED_PLACEHOLDER, str(error))

        cache_key = json.dumps([name, real_args], sort_keys=True, default=str)
        if cache_key in self._cache:
            return self._cache[cache_key]
        # Identical calls made at the same time share one upstream request.
        if cache_key not in self._in_flight:
            self._in_flight[cache_key] = asyncio.ensure_future(
                self._call_upstream(upstream, name, real_args, cache_key)
            )
        try:
            return await asyncio.shield(self._in_flight[cache_key])
        finally:
            if (
                self._in_flight.get(cache_key) is not None
                and self._in_flight[cache_key].done()
            ):
                self._in_flight.pop(cache_key, None)

    async def _call_upstream(
        self, upstream: Upstream, name: str, real_args: dict[str, Any], cache_key: str
    ) -> types.CallToolResult:
        if upstream.name == GTI:
            reason = self._gti_skip_reason(real_args)
            if reason:
                return self._wrap(Status.SKIPPED, reason)
            self._gti_lookups += 1

        async with upstream.limit:
            # Checked again: a quota error may have arrived while this call waited.
            if upstream.name == GTI and self._gti_stopped:
                return self._wrap(
                    Status.SKIPPED,
                    "GTI lookups are stopped for this run after a quota error.",
                )
            try:
                upstream_result = await asyncio.wait_for(
                    upstream.session.call_tool(name, {**real_args, **upstream.tenant}),
                    self._call_timeout,
                )
            except TimeoutError:
                status, payload = (
                    Status.UPSTREAM_ERROR,
                    {"error": f"No answer within {self._call_timeout:g} seconds."},
                )
            except Exception as error:  # noqa: BLE001 - any upstream failure becomes a status
                logger.warning("%s failed upstream: %s", name, error)
                status, payload = classify_error(str(error)), {"error": str(error)}
                # A failure of the call itself never means the record is missing.
                if status == Status.NOT_FOUND:
                    status = Status.UPSTREAM_ERROR
            else:
                status, payload = self._classify(upstream_result)

        if status == Status.QUOTA and upstream.name == GTI:
            self._gti_stopped = True
        result = self._finish(status, payload)
        if status in ANSWER_STATUSES:
            self._cache[cache_key] = result
        return result

    def _gti_skip_reason(self, real_args: dict[str, Any]) -> str | None:
        if self._gti_stopped:
            return "GTI lookups are stopped for this run after a quota error."
        if self._gti_lookups >= self._max_gti_lookups:
            return f"The limit of {self._max_gti_lookups} GTI lookups for this run was reached."
        for text in _strings(real_args):
            if any(is_internal_ip(ip) for ip in ips_in(text)):
                return "Internal addresses are not sent to VirusTotal."
        return None

    @staticmethod
    def _classify(result: types.CallToolResult) -> tuple[Status, Any]:
        texts = [
            item.text for item in result.content if isinstance(item, types.TextContent)
        ]
        if not texts and result.structuredContent is None and result.content:
            return Status.UPSTREAM_ERROR, {
                "error": "The tool returned only non-text content, which is not shown."
            }
        payload: Any = "\n".join(texts)
        if not texts and result.structuredContent is not None:
            payload = result.structuredContent
        if isinstance(payload, str):
            with contextlib.suppress(ValueError):
                payload = json.loads(payload)
        if result.isError:
            return classify_error(json.dumps(payload, default=str)), payload
        # GTI reports API errors as ordinary results with an "error" key.
        if isinstance(payload, dict) and payload.get("error") not in (None, "", [], {}):
            return classify_error(json.dumps(payload["error"], default=str)), payload
        if _is_empty(payload):
            return Status.EMPTY, payload
        return Status.OK, payload

    def _finish(self, status: Status, payload: Any) -> types.CallToolResult:
        """Redact an upstream payload, check it for leaks, save the map, and wrap it."""
        try:
            redacted = self._redactor.redact(payload)
            leaks = self._redactor.find_leaks(redacted)
        except Exception:
            logger.exception("Redaction failed")
            return self._wrap(
                Status.REDACTION_ERROR,
                "The result was withheld because redaction failed.",
            )
        if leaks:
            logger.error(
                "Withheld a result that failed the leak check: %s", sorted(set(leaks))
            )
            return self._wrap(
                Status.REDACTION_ERROR,
                "The result was withheld because it failed the leak check.",
            )
        try:
            self._save_map()
        except OSError:
            # Without the map on disk the report could never be revealed.
            logger.exception("Could not save the token map")
            return self._wrap(
                Status.REDACTION_ERROR,
                "The result was withheld because the token map could not be saved.",
            )
        return self._wrap(status, redacted)

    def _wrap(self, status: Status, body: Any) -> types.CallToolResult:
        """Wrap a body that is already safe to show the agent."""
        key = "result" if status in ANSWER_STATUSES else "error"
        text = json.dumps(
            {"status": status.value, key: body}, ensure_ascii=False, default=str
        )
        if len(text) > self._max_result_chars:
            text = (
                text[: self._max_result_chars]
                + f"\n[truncated: showing {self._max_result_chars} of {len(text)} characters]"
            )
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=text)],
            isError=status not in ANSWER_STATUSES,
        )

    def _save_map(self) -> None:
        if self._map_path is not None and len(self._redactor.map) != self._saved_size:
            self._redactor.map.save(self._map_path)
            self._saved_size = len(self._redactor.map)


def build_server(gateway: Gateway) -> Server:
    server = Server("secops-redacting-gateway")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return gateway.list_tools()

    # Upstream schemas may constrain values (for example an IP pattern) that
    # a placeholder would fail, so validation happens upstream on real values.
    @server.call_tool(validate_input=False)
    async def call_tool(name: str, arguments: dict[str, Any]) -> types.CallToolResult:
        return await gateway.call_tool(name, arguments)

    return server


# Configuration, upstream connections and the command line.


@dataclass(frozen=True)
class Problem:
    code: str
    fix: str


@dataclass(frozen=True)
class Config:
    project_id: str
    customer_id: str
    region: str
    vt_apikey: str
    gti_command: list[str]

    @classmethod
    def from_env(cls, env: dict[str, str]) -> "Config":
        command = env.get("GTI_MCP_COMMAND")
        try:
            gti_command = shlex.split(command) if command else DEFAULT_GTI_COMMAND
        except ValueError:
            gti_command = []
        return cls(
            project_id=env.get("CHRONICLE_PROJECT_ID", ""),
            customer_id=env.get("CHRONICLE_CUSTOMER_ID", ""),
            region=env.get("CHRONICLE_REGION", ""),
            vt_apikey=env.get("VT_APIKEY", ""),
            gti_command=gti_command,
        )

    @property
    def chronicle_url(self) -> str:
        return f"https://chronicle.{self.region}.rep.googleapis.com/mcp"

    @property
    def tenant_labels(self) -> dict[str, str]:
        """Tenant IDs and the labels that replace them in results."""
        return {self.project_id: "[project]", self.customer_id: "[customer]"}

    def problems(self, use_gti: bool) -> list[Problem]:
        found = [
            Problem("ENV_MISSING", f"Set {name}.")
            for name, value in (
                ("CHRONICLE_PROJECT_ID", self.project_id),
                ("CHRONICLE_CUSTOMER_ID", self.customer_id),
                ("CHRONICLE_REGION", self.region),
            )
            if not value
        ]
        # The region becomes part of the host name the token is sent to.
        if self.region and not _REGION_RE.fullmatch(self.region):
            found.append(
                Problem(
                    "REGION_INVALID",
                    "CHRONICLE_REGION may contain only a-z, 0-9 and '-'.",
                )
            )
        if use_gti and not self.vt_apikey:
            found.append(
                Problem("VT_APIKEY_MISSING", "Set VT_APIKEY, or run with --no-gti.")
            )
        if use_gti and not self.gti_command:
            found.append(
                Problem(
                    "GTI_COMMAND_INVALID", "GTI_MCP_COMMAND is empty or badly quoted."
                )
            )
        elif use_gti and shutil.which(self.gti_command[0]) is None:
            found.append(
                Problem(
                    "GTI_COMMAND_NOT_FOUND",
                    f"Install {self.gti_command[0]!r}, or set GTI_MCP_COMMAND.",
                )
            )
        return found


def map_problems(map_path: Path) -> list[Problem]:
    """Each run gets a new map; an existing one belongs to another run."""
    if not map_path.parent.is_dir():
        return [Problem("MAP_DIR_MISSING", f"Create {map_path.parent} first.")]
    if map_path.exists():
        return [
            Problem("MAP_EXISTS", f"{map_path} belongs to another run; use a new path.")
        ]
    return []


async def connect_chronicle(
    stack: contextlib.AsyncExitStack, config: Config, transport: GoogleAuthTransport
) -> Upstream:
    http_client = await stack.enter_async_context(
        httpx.AsyncClient(transport=transport, timeout=httpx.Timeout(30.0, read=300.0))
    )
    read, write, _ = await stack.enter_async_context(
        streamable_http_client(config.chronicle_url, http_client=http_client)
    )
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()
    tenant = {
        "project_id": config.project_id,
        "customer_id": config.customer_id,
        "region": config.region,
    }
    return Upstream(CHRONICLE, session, tenant=tenant, concurrency=4)


async def connect_gti(
    stack: contextlib.AsyncExitStack, config: Config, errlog: Any
) -> Upstream:
    # On Linux and macOS, stdio_client passes only PATH, HOME, USER, SHELL,
    # TERM and LOGNAME from this process, plus the variables given here.
    params = StdioServerParameters(
        command=config.gti_command[0],
        args=config.gti_command[1:],
        env={"VT_APIKEY": config.vt_apikey},
    )
    # GTI logs looked-up values to stderr, so stderr goes to the local log only.
    read, write = await stack.enter_async_context(stdio_client(params, errlog=errlog))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()
    return Upstream(GTI, session, concurrency=2)


def open_private(path: Path):
    """Open a log for appending, readable by the owner only, even if it already exists."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    os.fchmod(fd, 0o600)
    return os.fdopen(fd, "a", encoding="utf-8")


async def serve(
    config: Config, map_path: Path, log_path: Path, use_gti: bool, run_id: str
) -> None:
    log_file = open_private(log_path)
    logging.basicConfig(
        level=logging.INFO,
        stream=log_file,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    redactor = Redactor(TokenMap(run_id=run_id), secrets=config.tenant_labels)
    async with contextlib.AsyncExitStack() as stack:
        upstreams = [
            await connect_chronicle(
                stack, config, GoogleAuthTransport.from_adc(config.project_id)
            )
        ]
        if use_gti:
            upstreams.append(await connect_gti(stack, config, log_file))
        gateway = Gateway(upstreams, redactor, map_path=map_path)
        await gateway.load_tools()
        server = build_server(gateway)
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())


async def run_check(config: Config, use_gti: bool, log_path: Path) -> list[Problem]:
    """Check the setup without making any model call."""
    problems = config.problems(use_gti)
    if problems:
        return problems
    try:
        transport = GoogleAuthTransport.from_adc(config.project_id)
        await asyncio.to_thread(transport.refresh)
    except Exception:  # noqa: BLE001 - preflight reports any failure as a named problem
        return [Problem("ADC_FAILED", "Run `gcloud auth application-default login`.")]
    found: list[Problem] = []
    with open_private(log_path) as log_file:
        try:
            async with contextlib.AsyncExitStack() as stack:
                try:
                    upstreams = [await connect_chronicle(stack, config, transport)]
                except Exception:  # noqa: BLE001
                    found.append(
                        Problem(
                            "CHRONICLE_UNREACHABLE",
                            "Check CHRONICLE_REGION, that the Chronicle MCP service is enabled, "
                            "and that you have roles/mcp.toolUser.",
                        )
                    )
                    return found
                if use_gti:
                    try:
                        upstreams.append(await connect_gti(stack, config, log_file))
                    except Exception:  # noqa: BLE001
                        found.append(
                            Problem(
                                "GTI_START_FAILED",
                                f"See {log_path} for the GTI server's error output.",
                            )
                        )
                        return found
                try:
                    await Gateway(upstreams, Redactor(TokenMap())).load_tools()
                except MissingToolsError as error:
                    found.append(
                        Problem(
                            "TOOLS_MISSING",
                            f"{error}. Check the upstream server versions.",
                        )
                    )
        except Exception:  # noqa: BLE001 - connection errors can surface when the stack closes
            if not found:
                found.append(
                    Problem(
                        "CHRONICLE_UNREACHABLE",
                        "The connection failed while closing; see the log.",
                    )
                )
    return found


# Exit codes.
EXIT_OK, EXIT_PROBLEMS = 0, 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local redacting MCP gateway for Google SecOps."
    )
    parser.add_argument(
        "--map",
        type=Path,
        help="New token map file for this run (written with mode 0600).",
    )
    parser.add_argument(
        "--log",
        type=Path,
        help="Local log with real values (default: next to the map).",
    )
    parser.add_argument(
        "--run-id", default="", help="Run ID recorded in the token map."
    )
    parser.add_argument(
        "--no-gti", action="store_true", help="Do not start the GTI server."
    )
    parser.add_argument(
        "--check", action="store_true", help="Check the setup and exit."
    )
    args = parser.parse_args(argv)
    config = Config.from_env(dict(os.environ))
    use_gti = not args.no_gti

    # stdout carries the MCP protocol, so messages for people go to stderr.
    if args.check:
        log_path = args.log or Path.home() / ".secops-gateway-check.log"
        problems = asyncio.run(run_check(config, use_gti, log_path))
        if not problems:
            print(
                "OK: credentials, Chronicle tools"
                + (" and GTI" if use_gti else "")
                + " are ready.",
                file=sys.stderr,
            )
    else:
        if args.map is None:
            parser.error("--map is required unless --check is given")
        problems = config.problems(use_gti) + map_problems(args.map)
        if not problems:
            asyncio.run(
                serve(
                    config,
                    args.map,
                    args.log or args.map.with_name("gateway.log"),
                    use_gti,
                    args.run_id,
                )
            )
            return EXIT_OK
    for problem in problems:
        print(f"{problem.code}: {problem.fix}", file=sys.stderr)
    return EXIT_PROBLEMS if problems else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
