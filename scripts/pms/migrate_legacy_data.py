import sqlite3
import os
import sys
from datetime import datetime
from typing import Dict, Optional

# Add root to sys.path to import our lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from lib.pms.client import PlaneClient

DB_PATH = "projects/statistical_dashboards/data/dashboards.db"


def get_state_map(
    client: PlaneClient, workspace_slug: str, project_id: str
) -> Dict[str, str]:
    """Fetch states for a project and return a map of group -> state_id."""
    try:
        states = client.list_states(workspace_slug, project_id)
        state_map = {}
        for s in states:
            # group can be: backlog, unstarted, started, completed, cancelled
            group = s.get("group", "").lower()
            if group not in state_map:
                state_map[group] = s["id"]
        return state_map
    except Exception as e:
        print(f"Warning: Could not fetch states for project {project_id}: {e}")
        return {}


def migrate():
    # Load settings from .env
    from dotenv import load_dotenv

    env_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../apps/pms/.env")
    )
    load_dotenv(env_path)

    workspace_slug = os.getenv("PLANE_WORKSPACE_SLUG", "agent-factory")
    api_key = os.getenv("PLANE_API_TOKEN") or os.getenv("PLANE_API_KEY")
    api_url = os.getenv("PLANE_API_URL")

    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    client = PlaneClient(base_url=api_url, api_key=api_key)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f"Starting migration to workspace: {workspace_slug}")

    # 1. Get Legacy Projects
    cursor.execute("SELECT id, name, description FROM projects")
    projects = cursor.fetchall()

    for p_id, p_name, p_desc in projects:
        print(f"\nMigrating Project: {p_name}")
        # Clean identifier: no spaces, alphanumeric, max 5 chars
        identifier = "".join(filter(str.isalnum, p_name)).upper()[:5]

        try:
            # Check if project exists in Plane
            existing_projects = client.list_projects(workspace_slug)
            plane_proj = next(
                (p for p in existing_projects if p["name"] == p_name), None
            )

            if not plane_proj:
                plane_proj = client.create_project(
                    workspace_slug, p_name, identifier, p_desc or ""
                )
                print(f"Created Plane project: {p_name} ({identifier})")
            else:
                print(f"Plane project already exists: {p_name}")

            plane_project_id = plane_proj["id"]

            # Fetch states for mapping
            state_map = get_state_map(client, workspace_slug, plane_project_id)
            done_state = state_map.get("completed")
            todo_state = state_map.get("backlog") or state_map.get("unstarted")

            # 2. Migrate Tasks
            cursor.execute(
                "SELECT title, description, is_completed FROM project_tasks WHERE project_id = ?",
                (p_id,),
            )
            tasks = cursor.fetchall()

            for t_title, t_desc, is_completed in tasks:
                target_state = done_state if is_completed else todo_state
                print(f"  Ingesting Task: {t_title} (Done: {bool(is_completed)})")

                try:
                    client.create_issue(
                        workspace_slug=workspace_slug,
                        project_id=plane_project_id,
                        name=t_title,
                        description=t_desc or "",
                        state_id=target_state,
                    )
                except Exception as task_err:
                    print(f"    Error creating task {t_title}: {task_err}")

        except Exception as e:
            print(f"Error migrating project {p_name}: {e}")

    conn.close()
    print("\nMigration successfully completed!")


if __name__ == "__main__":
    migrate()
