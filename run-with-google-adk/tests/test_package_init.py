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


def test_package_exports():
    assert hasattr(mcp_security_agent, "create_security_agent")
    assert hasattr(mcp_security_agent, "root_agent")
    assert "create_security_agent" in dir(mcp_security_agent)
    assert "root_agent" in dir(mcp_security_agent)


def test_package_invalid_attr():
    import pytest
    with pytest.raises(AttributeError, match="has no attribute 'nonexistent'"):
        _ = mcp_security_agent.nonexistent
