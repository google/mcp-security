"""Unit tests for mcp_security_agent package initialization."""

import sys
from pathlib import Path

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import mcp_security_agent


def test_package_version():
    assert hasattr(mcp_security_agent, "__version__")
    assert isinstance(mcp_security_agent.__version__, str)
    assert mcp_security_agent.__version__ == "0.2.0"
