# Copyright 2026 Google LLC
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

import json
import os
import pytest
import pytest_asyncio
import dotenv
from secops_soar_mcp import bindings
from typing import Dict

# Load .env file at session start
dotenv.load_dotenv()


@pytest.fixture
def config_path() -> str:
    """Get the path to the config file.

    Returns:
        Path to the configuration file
    """
    return os.path.join(os.path.dirname(__file__), "config.json")


@pytest.fixture
def soar_config(config_path: str) -> Dict[str, str]:
    """Load SOAR configuration from the config file or environment variables.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary with SOAR configuration

    Raises:
        FileNotFoundError: If the config file is missing and env vars are not set
    """
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)

    if os.getenv("SOAR_URL") and os.getenv("SOAR_APP_KEY"):
        return {
            "SOAR_URL": os.getenv("SOAR_URL"),
            "SOAR_APP_KEY": os.getenv("SOAR_APP_KEY"),
        }

    raise FileNotFoundError(
        f"SOAR configuration not found. Please set SOAR_URL and SOAR_APP_KEY environment variables "
        f"or create a config file at {config_path}."
    )


def update_env_vars(soar_config: Dict[str, str]):
    for key, value in soar_config.items():
        os.environ[key] = value


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def setup_bindings(soar_config: Dict[str, str]):
    """Ensures bindings are done once before tests in this module run."""
    update_env_vars(soar_config)
    await bindings.bind()
    yield
    await bindings.http_client.close()
