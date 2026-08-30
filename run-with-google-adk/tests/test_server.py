"""Unit tests for mcp_security_agent.server."""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src directory to path
src_dir = str(Path(__file__).resolve().parents[1] / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_security_agent.server.app import create_app


def test_healthz():
    client = TestClient(create_app())
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info():
    client = TestClient(create_app())
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.2.0"
    assert "tools" in data
