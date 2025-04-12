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
import asyncio
import importlib
import json # Added json import
from pathlib import Path
import bindings
from mcp.server.fastmcp import FastMCP
from logger_utils import get_logger
from case_management import register_tools
from utils.utils import to_snake_case
from utils.consts import Endpoints # Added Endpoints import
# import argparse # Removed argparse

logger = get_logger(__name__)
mcp = FastMCP("SoarAS")

register_tools(mcp) # Register base case management tools

# Argument parsing removed - integrations will be fetched dynamically

async def main():
    """Main function."""
    logger.info("Starting SecOps SOAR MCP server")
    await bindings.bind() # Initialize HTTP client and bindings

    # --- Fetch Enabled Integrations Dynamically ---
    enabled_integrations_set = set()
    try:
        logger.info("Fetching enabled integrations from SOAR tenant...")
        # Assuming the response is JSON and contains a list under a key like 'integrations' or similar
        # And each item in the list is a dict with a 'name' field.
        # Adjust parsing based on actual API response structure if needed.
        response = await bindings.http_client.get(Endpoints.LIST_INSTALLED_INTEGRATIONS)

        # --- TODO: Adjust the parsing logic below based on the actual API response structure ---
        installed_integrations = response # Assuming the response *is* the list
        if isinstance(installed_integrations, list):
             # Assuming each item has a 'name' or 'identifier' field - check actual response
            integration_names = [integ.get('name') or integ.get('identifier') for integ in installed_integrations]
            valid_names = [name for name in integration_names if name and isinstance(name, str)]
            enabled_integrations_set = {to_snake_case(name) for name in valid_names}
            logger.info("Successfully fetched and processed enabled integrations: %s", enabled_integrations_set)
        else:
            logger.warning("API response for installed integrations was not a list as expected: %s", response)
        # --- END TODO ---

    except Exception as e:
        logger.error("Failed to fetch or parse enabled integrations from SOAR API: %s. No integrations will be loaded dynamically.", e, exc_info=True)
        enabled_integrations_set = set() # Fallback to empty set on error

    # --- Dynamic Tool Registration (Moved inside main) ---
    logger.info("Starting dynamic tool registration based on fetched integrations...")
    try:
        script_dir = Path(__file__).parent.resolve()
        marketplace_dir = script_dir / "marketplace"

        if marketplace_dir.is_dir():
            logger.debug("Scanning for tools in: %s", marketplace_dir)
            init_file = marketplace_dir / "__init__.py"
            if not init_file.exists():
                logger.warning("Marketplace directory '%s' is missing __init__.py.", marketplace_dir)

            for py_file in marketplace_dir.glob("*.py"):
                if py_file.name == "__init__.py" or not py_file.is_file():
                    continue

                module_stem = py_file.stem
                # Check if the module corresponds to an enabled integration
                if module_stem.lower() not in enabled_integrations_set:
                    logger.debug("Skipping module %s as it's not in the enabled set.", module_stem)
                    continue # Skip modules not in the dynamically fetched list

                module_import_path = f"marketplace.{module_stem}"
                try:
                    logger.debug("  Attempting to import module: %s", module_import_path)
                    module = importlib.import_module(module_import_path)

                    if hasattr(module, "register_tools") and callable(getattr(module, "register_tools")):
                        logger.info("    Found register_tools in %s. Registering...", module_stem)
                        register_function = getattr(module, "register_tools")
                        register_function(mcp)
                        logger.debug("    Successfully called register_tools for %s.", module_stem)
                    else:
                        logger.warning("    Module %s found, but has no callable 'register_tools' function.", module_stem)

                except ImportError as e:
                    logger.error("  * Failed to import module %s. Error: %s", module_import_path, e, exc_info=True)
                except Exception as e:
                    logger.error("  * Failed during registration call for module %s. Error: %s", module_import_path, e, exc_info=True)

            logger.info("Finished scanning marketplace directory.")
        else:
            logger.warning("Marketplace directory not found at %s. No tools dynamically registered.", marketplace_dir)

    except Exception as e:
        logger.error("An unexpected error occurred during dynamic tool registration: %s", e, exc_info=True)
    # --- End Dynamic Tool Registration ---

    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
