import os
import sys
from dotenv import load_dotenv

# Add root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from lib.pms.client import PlaneClient


def test_connection():
    env_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../apps/pms/.env")
    )
    load_dotenv(env_path)

    workspace_slug = os.getenv("PLANE_WORKSPACE_SLUG", "agent-factory")
    api_key = os.getenv("PLANE_API_TOKEN") or os.getenv("PLANE_API_KEY")
    api_url = os.getenv("PLANE_API_URL", "http://localhost:8080/api")

    print(f"URL: {api_url}")
    print(f"Workspace: {workspace_slug}")
    print(f"API Key prefix: {api_key[:10]}...")

    client = PlaneClient(base_url=api_url, api_key=api_key)
    try:
        print("\nAttempting to list projects...")
        projects = client.list_projects(workspace_slug)
        print(f"Found {len(projects)} projects:")
        for p in projects:
            print(f"- {p['name']} (ID: {p['id']}, Identifier: {p['identifier']})")

        if not projects:
            print("No projects found in this workspace.")

    except Exception as e:
        print(f"Error Listing Projects: {e}")

        print("\nAttempting to list workspaces (global)...")
        try:
            workspaces = client.list_workspaces()
            print(f"Found {len(workspaces)} workspaces:")
            for w in workspaces:
                print(f"- {w['name']} (Slug: {w['slug']})")
        except Exception as e2:
            print(f"Error Listing Workspaces: {e2}")


if __name__ == "__main__":
    test_connection()
