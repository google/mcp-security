# Copyright 2025 Google LLC
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
import vt

from mcp.server.fastmcp import FastMCP, Context

logging.basicConfig(level=logging.ERROR)

@dataclass
class AppContext:
  client: vt.Client


async def new_vt_client():
  return vt.Client(os.environ.get('VT_APIKEY'))


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
  """Manage application lifecycle with type-safe context"""
  # Initialize on startup
  client = await new_vt_client()
  try:
    yield AppContext(client=client)
  finally:
    # Cleanup on shutdown
    await client.close_async()


def vt_client(ctx: Context) -> vt.Client:
  return ctx.request_context.lifespan_context.client

# Create a named server and specify dependencies for deployment and development
server = FastMCP(
    "Google Threat Intelligence MCP server",
    dependencies=["vt-py"],
    lifespan=app_lifespan)

# Load tools.
from gti_mcp.tools import *

# Run the server
def main():
  server.run(transport='stdio')


if __name__ == '__main__':
  main()
