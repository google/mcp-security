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
"""Main entry point for the SOAR MCP server."""

import asyncio
import importlib
from pathlib import Path
from secops_soar_mcp import bindings
from mcp.server.fastmcp import FastMCP
from logger_utils import get_logger, setup_logging
from secops_soar_mcp.case_management import (
    register_tools as register_tools_case_management,
)
from secops_soar_mcp.utils.utils import normalize_integration_name
import argparse

logger = get_logger(__name__)
mcp = FastMCP("SecOps SOAR")

register_tools_case_management(mcp)

parser = argparse.ArgumentParser(description="SecOps SOAR MCP Server")
parser.add_argument(
    "--integrations",
    help="Comma-separated list of integration names to enable (e.g., CSV,SiemplifyThreatFuse). If not provided, no integrations are enabled.",
)
parser.add_argument(
    "--verbose", action="store_true", help="Enable verbose (debug) logging"
)


def get_enabled_integrations_set(integrations_arg: str) -> set:
    """Get the set of enabled integrations from the command line arguments.

    Args:
        args: Parsed command line arguments."""
    enabled_integrations_set = set()
    if integrations_arg:
        integration_list = [
            normalize_integration_name(name)
            for name in integrations_arg.split(",")
            if name.strip()
        ]
        if integration_list:
            enabled_integrations_set = set(integration_list)
            logger.info(
                "Found --integrations flag. Enabling only: %s", enabled_integrations_set
            )
            return enabled_integrations_set
        else:
            logger.warning(
                "Received --integrations flag but the list was empty after parsing. No integrations are enabled."
            )
    else:
        logger.info("No --integrations flag provided. No integrations are enabled.")
    return set()


def register_tools(integrations_arg: str):
    """Register tools for the MCP server.

    Args:
        args: Parsed command line arguments."""
    enabled_integrations_set = get_enabled_integrations_set(integrations_arg)

    logger.info("Starting dynamic tool registration...")
    try:
        script_dir = Path(__file__).parent.resolve()

        marketplace_dir = script_dir / "marketplace"

        if marketplace_dir.is_dir():
            logger.debug("Scanning for tools in: %s", marketplace_dir)

            init_file = marketplace_dir / "__init__.py"
            if not init_file.exists():
                logger.warning(
                    "Marketplace directory '%s' is missing __init__.py. Tool registration might fail.",
                    marketplace_dir,
                )

            for py_file in marketplace_dir.glob("*.py"):
                if py_file.name == "__init__.py" or not py_file.is_file():
                    continue

                module_stem = (
                    py_file.stem
                )  # The filename without .py (e.g., "csv")
                if module_stem not in enabled_integrations_set:
                    continue
                module_import_path = f"marketplace.{module_stem}"  # The import path (e.g., "marketplace.csv")

                try:
                    logger.debug(
                        "  Attempting to import module: %s", module_import_path
                    )
                    module = importlib.import_module(module_import_path)

                    if hasattr(module, "register_tools") and callable(
                        getattr(module, "register_tools")
                    ):
                        logger.info(
                            "    Found register_tools in %s. Registering...",
                            module_stem,
                        )
                        register_function = getattr(module, "register_tools")
                        register_function(mcp)
                        logger.debug(
                            "    Successfully called register_tools for %s.",
                            module_stem,
                        )
                    else:
                        logger.warning(
                            "    Module %s found, but it has no callable 'register_tools' function.",
                            module_stem,
                        )

                except ImportError as e:
                    logger.error(
                        "  * Failed to import module %s. Error: %s",
                        module_import_path,
                        e,
                        exc_info=True,
                    )
                except Exception as e:
                    logger.error(
                        "  * Failed during registration call for module %s. Error: %s",
                        module_import_path,
                        e,
                        exc_info=True,
                    )

            logger.info("Finished scanning marketplace directory.")
        else:
            logger.warning(
                "Marketplace directory not found at %s. No tools dynamically registered.",
                marketplace_dir,
            )

    except Exception as e:
        logger.error(
            "An unexpected error occurred during tool registration setup: %s",
            e,
            exc_info=True,
        )


async def main():
    """Main function."""
    args = parser.parse_args()
    setup_logging(args.verbose)
    logger.info("Starting SecOps SOAR MCP server")
    try:
        await bindings.bind()
        register_tools(args.integrations)
        await mcp.run_stdio_async()
    except Exception as e:
        logger.error("Error: %s", e)
    finally:
        await bindings.cleanup()


def run_main():
    """Entry point function that properly awaits the async main function."""
    return asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
