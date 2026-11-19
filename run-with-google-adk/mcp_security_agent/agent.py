"""Google ADK v2 root agent wired to Google Cloud Security MCP servers."""

import os
from pathlib import Path
import shutil
import sys
from urllib.parse import urlparse
import dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams
from mcp import StdioServerParameters

dotenv.load_dotenv()
_MTLS = {
    "GOOGLE_API_USE_CLIENT_CERTIFICATE": "false",
    "GOOGLE_API_USE_MTLS_ENDPOINT": "never",
    "CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE": "false",
}
for _k, _v in _MTLS.items():
    os.environ.setdefault(_k, _v)

_SERVER_ROOT = Path(__file__).resolve().parents[2] / "server"
_BASE_ENV = (
    "PATH", "HOME", "USER", "VIRTUAL_ENV", "SSL_CERT_FILE", "SSL_CERT_DIR",
    "REQUESTS_CA_BUNDLE", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy",
    "https_proxy", "no_proxy", "GOOGLE_APPLICATION_CREDENTIALS", "CLOUDSDK_CONFIG",
    "GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_QUOTA_PROJECT",
)
_SERVERS = (
    ("secops", "secops_mcp/server.py", "LOAD_SECOPS_MCP", "SECOPS_MCP_URL", ("CHRONICLE_PROJECT_ID", "CHRONICLE_CUSTOMER_ID"),
     ("CHRONICLE_PROJECT_ID", "CHRONICLE_CUSTOMER_ID", "CHRONICLE_REGION", "SECOPS_SA_PATH", "SECOPS_IMPERSONATE_SERVICE_ACCOUNT")),
    ("scc", "scc_mcp.py", "LOAD_SCC_MCP", "SCC_MCP_URL", None, ()),
    ("gti", "gti_mcp/server.py", "LOAD_GTI_MCP", "GTI_MCP_URL", ("VT_APIKEY",), ("VT_APIKEY",)),
    ("secops-soar", "secops_soar_mcp/server.py", "LOAD_SECOPS_SOAR_MCP", "SECOPS_SOAR_MCP_URL", ("SOAR_URL", "SOAR_APP_KEY"), ("SOAR_URL", "SOAR_APP_KEY", "SOAR_VERIFY_SSL")),
)


def _validate_url(url: str) -> str:
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if host and not p.username and not p.password and not any(c.isspace() for c in url):
        if p.scheme == "https" or (p.scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}):
            return url
    raise ValueError(f"Unsafe MCP URL (expected https:// or loopback http://): {url!r}")


def build_agent() -> LlmAgent:
    timeout = float(os.getenv("STDIO_PARAM_TIMEOUT", "").strip() or "60.0")
    uv_bin = shutil.which("uv")
    tools: list[McpToolset] = []
    for subdir, script, load_var, url_var, req_keys, own_keys in _SERVERS:
        url, flag = os.getenv(url_var, "").strip(), os.getenv(load_var, "").strip().upper()
        auto = bool(url or (req_keys and all(os.getenv(k, "").strip() for k in req_keys)))
        if not ((flag in {"1", "Y", "YES", "TRUE"}) if flag else auto):
            continue
        if url:
            conn = StreamableHTTPConnectionParams(url=_validate_url(url))
        else:
            sdir = _SERVER_ROOT / subdir
            env = {**_MTLS, **{k: os.environ[k] for k in (*_BASE_ENV, *own_keys) if os.environ.get(k)}}
            if uv_bin:
                cmd, args = "uv", ["--directory", str(sdir), "run", script]
            else:
                cmd, args, env["PYTHONPATH"] = sys.executable, [str(sdir / script)], str(sdir)
            conn = StdioConnectionParams(server_params=StdioServerParameters(command=cmd, args=args, env=env), timeout=timeout)
        tools.append(McpToolset(connection_params=conn))
    return LlmAgent(
        name="mcp_security_agent",
        model=os.getenv("GOOGLE_MODEL", "").strip() or "gemini-3.1-pro-preview",
        description="Security operations agent with Google Cloud Security MCP tools.",
        instruction="You are a security operations analyst. Investigate alerts, query SIEM telemetry, enrich indicators with threat intelligence, review cloud posture findings, and manage SOAR cases using only verified tool data.",
        tools=tools,
    )


root_agent = build_agent()
