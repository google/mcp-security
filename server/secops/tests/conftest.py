"""Fixtures for Chronicle SecOps MCP integration tests.

This module contains pytest fixtures used by the integration tests 
for the secops-mcp tools.
"""

import json
import os
import pathlib
from typing import Dict, Generator, Any

import pytest
from secops import SecOpsClient


@pytest.fixture
def config_path() -> str:
    """Get the path to the config file.
    
    Returns:
        Path to the configuration file
    """
    return os.path.join(os.path.dirname(__file__), "config.json")


@pytest.fixture
def chronicle_config(config_path: str) -> Dict[str, str]:
    """Load Chronicle configuration from the config file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dictionary with Chronicle configuration
        
    Raises:
        FileNotFoundError: If the config file is missing
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Chronicle config file not found at {config_path}. "
            f"Please create this file with the following format:\n"
            f"{{\n"
            f'    "CHRONICLE_PROJECT_ID": "your-project-id",\n'
            f'    "CHRONICLE_CUSTOMER_ID": "your-customer-id",\n'
            f'    "CHRONICLE_REGION": "us"\n'
            f"}}"
        )
    
    with open(config_path, "r") as f:
        return json.load(f)


@pytest.fixture
def chronicle_client(chronicle_config: Dict[str, str]) -> Any:
    """Initialize Chronicle client using the configuration.
    
    Args:
        chronicle_config: Dictionary with Chronicle configuration
        
    Returns:
        Initialized Chronicle client
        
    Note:
        This fixture uses Google Application Default Credentials (ADC).
        Make sure you have authenticated with `gcloud auth application-default login`
        before running these tests.
    """
    client = SecOpsClient()
    chronicle = client.chronicle(
        customer_id=chronicle_config["CHRONICLE_CUSTOMER_ID"],
        project_id=chronicle_config["CHRONICLE_PROJECT_ID"],
        region=chronicle_config["CHRONICLE_REGION"]
    )
    return chronicle 