
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


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
  """Manage application lifecycle with type-safe context"""
  # Initialize on startup
  client = vt.Client(os.environ.get('VT_APIKEY'))
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
