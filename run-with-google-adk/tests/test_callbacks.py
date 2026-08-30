"""Unit tests for mcp_security_agent.callbacks."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.callbacks import bmc_trim_llm_request


def test_bmc_trim_llm_request_passthrough():
    mock_context = MagicMock()
    mock_request = MagicMock()
    mock_request.contents = ["alert summary"]
    
    result = bmc_trim_llm_request(mock_context, mock_request)
    assert result == mock_request
