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

import json
import os
import pytest
import pytest_asyncio
from secops_soar_mcp import bindings
from typing import Dict


@pytest.fixture
def config_path() -> str:
    """Get the path to the config file.

    Returns:
        Path to the configuration file
    """
    return os.path.join(os.path.dirname(__file__), "config.json")


@pytest.fixture
def soar_config(config_path: str) -> Dict[str, str]:
    """Load SOAR configuration from the config file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary with SOAR configuration

    Raises:
        FileNotFoundError: If the config file is missing
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"SOAR config file not found at {config_path}. "
            f"Please create this file with the following format:\n"
            f"{{\n"
            f'    "SOAR_URL": "your-soar-url",\n'
            f'    "SOAR_APP_KEY": "your-soar-app-key",\n'
            f"}}"
        )

    with open(config_path, "r") as f:
        return json.load(f)


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
