"""Main entry point for the SOAR MCP server."""

import asyncio
import importlib
from pathlib import Path
import bindings
from mcp.server.fastmcp import FastMCP
from logger_utils import get_logger
from case_management import register_tools
from utils.utils import to_snake_case
import argparse

logger = get_logger(__name__)
mcp = FastMCP("SoarAS")

register_tools(mcp)

parser = argparse.ArgumentParser(description="SecOps SOAR MCP Server")
parser.add_argument(
    "--integrations",
    help="Comma-separated list of integration names to enable (e.g., CSV,SiemplifyThreatFuse). If not provided, no integrations are enabled.",
)

args = parser.parse_args()

enabled_integrations_set = set()  # None means all enabled by default
if args.integrations:
    # Split the comma-separated string and remove whitespace
    integration_list = [
        to_snake_case(name) for name in args.integrations.split(",") if name.strip()
    ]
    if integration_list:
        enabled_integrations_set = set(integration_list)
        logger.info(
            "Found --integrations flag. Enabling only: %s", enabled_integrations_set
        )
    else:
        logger.warning(
            "Received --integrations flag but the list was empty after parsing. No integrations are enabled."
        )
else:
    logger.info("No --integrations flag provided. No integrations are enabled.")
# --- End Argument Parsing ---

# --- Dynamic Tool Registration ---
logger.info("Starting dynamic tool registration...")
try:
    # Get the directory where main.py is located
    script_dir = Path(__file__).parent.resolve()

    # Define the path to the marketplace directory (relative to main.py)
    # Assuming 'marketplace' is in the same directory as main.py
    marketplace_dir = script_dir / "marketplace"

    # # Add the script's directory to sys.path to help find the 'marketplace' package
    # # This is important if 'marketplace' isn't automatically discoverable
    # if str(script_dir) not in sys.path:
    #     sys.path.insert(0, str(script_dir))  # Prepend ensures it's checked first

    if marketplace_dir.is_dir():
        logger.debug("Scanning for tools in: %s", marketplace_dir)

        # Check for __init__.py (required for package imports)
        init_file = marketplace_dir / "__init__.py"
        if not init_file.exists():
            logger.warning(
                "Marketplace directory '%s' is missing __init__.py. Tool registration might fail.",
                marketplace_dir,
            )

        # Iterate through all .py files in the marketplace directory
        for py_file in marketplace_dir.glob("*.py"):
            # Skip __init__.py itself
            if py_file.name == "__init__.py" or not py_file.is_file():
                continue

            module_stem = py_file.stem  # The filename without .py (e.g., "csv")
            if module_stem.lower() not in enabled_integrations_set:
                continue
            module_import_path = f"marketplace.{module_stem}"  # The import path (e.g., "marketplace.csv")

            try:
                logger.debug("  Attempting to import module: %s", module_import_path)
                # Dynamically import the module
                module = importlib.import_module(module_import_path)

                # Check if the module has a 'register_tools' function
                if hasattr(module, "register_tools") and callable(
                    getattr(module, "register_tools")
                ):
                    logger.info(
                        "    Found register_tools in %s. Registering...", module_stem
                    )
                    # Get the function
                    register_function = getattr(module, "register_tools")
                    # Call the function, passing the mcp instance
                    register_function(mcp)
                    logger.debug(
                        "    Successfully called register_tools for %s.", module_stem
                    )
                else:
                    logger.warning(
                        "    Module %s found, but it has no callable 'register_tools' function.",
                        module_stem,
                    )

            except ImportError as e:
                # Handle errors during module import (e.g., syntax errors in the module)
                logger.error(
                    "  * Failed to import module %s. Error: %s",
                    module_import_path,
                    e,
                    exc_info=True,
                )
            except Exception as e:
                # Handle errors during the call to register_tools itself
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
# --- End Dynamic Tool Registration ---


async def main():
    """Main function."""
    logger.info("Starting SecOps SOAR MCP server")
    await bindings.bind()
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
