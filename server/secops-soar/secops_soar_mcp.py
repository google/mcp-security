"""Main entry point for the SOAR MCP server."""

import asyncio

import bindings
from fastmcp import FastMCP
from logger_utils import get_logger
from tools import register_tools


logger = get_logger(__name__)
mcp = FastMCP("SoarAS")
bindings.bind()

register_tools(mcp)


async def main():
    """Main function."""
    logger.info("Starting SecOps SOAR MCP server")
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
