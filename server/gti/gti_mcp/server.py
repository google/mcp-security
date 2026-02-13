# Copyright 2025 Google LLC
# Modifications Copyright (c) 2025-2026 Deep Kanaparthi
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
# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

import logging
import os
from typing import Dict
import vt

from mcp.server.fastmcp import FastMCP, Context

logging.basicConfig(level=logging.ERROR)

# If True, creates a completely fresh transport for each request
# with no session tracking or state persistence between requests.
stateless = False
if os.getenv("STATELESS") == "1":
  stateless = True

# ---------------------------------------------------------------------------
# HTTP header access for multi-client credential passthrough
# ---------------------------------------------------------------------------
try:
  from fastmcp.server.dependencies import get_http_headers
except ImportError:
  get_http_headers = None


def _get_request_headers() -> Dict[str, str]:
  """Get HTTP headers for the current MCP session via FastMCP's built-in context."""
  if get_http_headers is None:
    return {}
  try:
    headers = get_http_headers()
    if headers:
      return headers
  except Exception:
    pass
  return {}


def _get_gti_config() -> Dict[str, str]:
  """Resolve VT config from HTTP headers with env var fallback."""
  headers = _get_request_headers()
  h = {k.lower(): v for k, v in headers.items()}
  return {
    "api_key": h.get("x-vt-apikey", os.getenv("VT_APIKEY", "")),
    "verify_ssl": os.getenv("VT_VERIFY_SSL", "true").lower() != "false",
  }


def _vt_client_factory(unused_ctx) -> vt.Client:
  cfg = _get_gti_config()
  api_key = cfg["api_key"]
  if not api_key:
    raise ValueError(
      "VT_APIKEY not configured. Set VT_APIKEY env var or send X-VT-ApiKey header."
    )
  return vt.Client(api_key, verify_ssl=cfg["verify_ssl"])

vt_client_factory = _vt_client_factory


@asynccontextmanager
async def vt_client(ctx: Context) -> AsyncIterator[vt.Client]:
  """Provides a vt.Client instance for the current request."""
  client = vt_client_factory(ctx)

  try:
    yield client
  finally:
    await client.close_async()

# Create a named server and specify dependencies for deployment and development
server = FastMCP(
    "Google Threat Intelligence MCP server",
    dependencies=["vt-py"],
    stateless_http=stateless)

# Load tools.
from gti_mcp.tools import *

# Run the server
def main():
  server.run(transport='stdio')


if __name__ == '__main__':
  import sys
  transport = sys.argv[1] if len(sys.argv) > 1 else os.getenv("MCP_TRANSPORT", "stdio")

  if transport == "streamable-http":
    import uvicorn
    app = server.streamable_http_app()
    uvicorn.run(
      app,
      host=os.getenv("FASTMCP_HOST", "0.0.0.0"),
      port=int(os.getenv("FASTMCP_PORT", "8003")),
    )
  else:
    main()
