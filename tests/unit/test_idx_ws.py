import sys
import os
from pathlib import Path

# Ensure scripts/api is in the path
api_dir = (Path(__file__).parent.parent.parent / "scripts" / "api").resolve()
sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from mcp_api import app

client = TestClient(app)


def test_health_check():
    """Verify health endpoint works and returns expected version."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_websocket_thoughts():
    """Test connection to the thoughts websocket."""
    with client.websocket_connect("/ws/thoughts") as websocket:
        assert websocket is not None


def test_websocket_events():
    """Test connection to the events websocket."""
    with client.websocket_connect("/ws/events") as websocket:
        assert websocket is not None
