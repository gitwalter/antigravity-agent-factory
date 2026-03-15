import pytest
from unittest.mock import MagicMock
import sys
import os

# Add the project root and API dir to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "scripts/api"))


def test_idx_api_health():
    """Verify that the IDX Orchestrator API starts correctly."""
    from mcp_api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_mcp_servers_endpoint():
    """Verify the MCP servers list endpoint."""
    from mcp_api import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/api/mcp/servers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ui_component_structure():
    """Verify that the UI page files exist in the correct locations."""
    base_path = os.path.join(PROJECT_ROOT, "ui/app/")
    required_files = [
        "page.tsx",
        "workflows/page.tsx",
        "agents/page.tsx",
        "skills/page.tsx",
    ]
    for file in required_files:
        assert os.path.exists(os.path.join(base_path, file))
