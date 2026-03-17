#!/usr/bin/env python3
"""
Create Task — Jinja2 Template Renderer for Plane Work Items

Renders a structured HTML description from a JSON input file using the
work_item.html.j2 template, then creates a work item in Plane via the API.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/create_task.py \\
        --json task_input.json

The JSON input file schema matches task_definition_schema.json.
"""

import argparse
import json
import os
import sys
import requests

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print(
        "Error: jinja2 not installed. Run: conda install -p D:\\Anaconda\\envs\\cursor-factory jinja2"
    )
    sys.exit(1)

# --- Configuration ---
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT_FILE = os.path.join(SKILL_ROOT, "references", "project_context.json")
TEMPLATE_DIR = os.path.join(SKILL_ROOT, "templates")


def load_context():
    """Load persistent context for IDs and mappings."""
    if os.path.exists(CONTEXT_FILE):
        try:
            with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load context file: {e}")
    return {}


# Default fallback config
context = load_context()
WORKSPACE_SLUG = context.get("WORKSPACE_SLUG", "agent-factory")
PROJECT_ID = context.get("PROJECT_ID", "e71eb003-87d4-4b0c-a765-a044ac5affbe")
API_BASE = (
    f"https://api.plane.so/api/v1/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}"
)


def get_label_map(headers: dict) -> dict:
    """Fetch all labels for the project and map name (uppercase) to UUID."""
    url = f"{API_BASE}/labels/"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, dict) and "results" in data:
            results = data["results"]
        elif isinstance(data, list):
            results = data
        else:
            results = []
        return {item["name"].upper(): item["id"] for item in results}
    else:
        print(f"Warning: Failed to fetch labels ({resp.status_code})")
        return {}


def create_or_get_module(name: str, headers: dict) -> str:
    """Create a module (Epic) in Plane if it doesn't already exist."""
    url = f"{API_BASE}/modules/"
    print(f"Checking for module: {name}")
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        modules = resp.json().get("results", [])
        for m in modules:
            if m["name"].lower() == name.lower():
                return m["id"]

    # Create new module
    print(f"Creating new module (Epic): {name}")
    payload = {
        "name": name,
        "description": f"Automatically created epic for {name}",
        "status": "backlog",
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (200, 201):
        uid = resp.json().get("id")
        print(f"Successfully created module '{name}' (UUID: {uid})")
        return uid
    else:
        print(f"Warning: Failed to create module '{name}' ({resp.status_code})")
        return None


def load_input(path: str) -> dict:
    """Load and validate the JSON input file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required = [
        "name",
        "type",
        "schema_version",
        "requirements",
        "acceptance_criteria",
        "workflows",
        "agents",
        "skills",
        "tests",
        "module",
        "cycle",
        "priority",
    ]
    missing = [k for k in required if k not in data]
    if missing:
        print(f"Error: Missing required fields: {', '.join(missing)}")
        sys.exit(1)

    # Defaults for optional fields
    data.setdefault("rules", [])
    data.setdefault("patterns", [])
    data.setdefault("blueprints", [])
    data.setdefault("templates", [])
    data.setdefault("knowledge", [])
    data.setdefault("scripts", [])
    data.setdefault("memory_queries", [])
    data.setdefault("notes", "")
    data.setdefault("priority", "medium")
    data.setdefault("labels", [data["type"].upper()])

    return data


def render_template(data: dict) -> str:
    """Render the Jinja2 template with the given data."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    # Auto-populate schema_json if not provided, to meet high-fidelity requirements
    if "schema_json" not in data:
        # Create a copy without sensitive or internal render-only fields if any
        schema_data = {k: v for k, v in data.items() if k != "schema_json"}
        data["schema_json"] = json.dumps(schema_data, indent=2)

    template = env.get_template("work_item.html.j2")
    return template.render(**data)


def create_work_item(data: dict, description_html: str, update_id: str = None) -> dict:
    """Create or update the work item in Plane via the API."""
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    # Resolve label UUIDs from context or fallback to API
    label_map = context.get("LABELS", {})
    if not label_map:
        print("Context labels missing, fetching from API...")
        label_map = get_label_map(headers)

    # Resolve Cycle and Module UUIDs from Context
    cycle_id = None
    cycle_name_or_id = data.get("cycle")
    if cycle_name_or_id:
        active_cycle = context.get("ACTIVE_CYCLE", {})
        if (
            active_cycle.get("name") == cycle_name_or_id
            or active_cycle.get("id") == cycle_name_or_id
        ):
            cycle_id = active_cycle.get("id")
        else:
            cycle_id = cycle_name_or_id

    module_id = None
    module_name_or_id = data.get("module")
    if module_name_or_id:
        active_modules = context.get("ACTIVE_MODULES", {})
        for name, uid in active_modules.items():
            if name.lower() == module_name_or_id.lower():
                module_id = uid
                break
        if not module_id:
            if len(module_name_or_id) < 30:  # Name
                module_id = create_or_get_module(module_name_or_id, headers)
            else:  # UUID
                module_id = module_name_or_id

    payload = {
        "name": data["name"],
        "description_html": description_html,
        "priority": data.get("priority", "medium"),
        "state": context.get("STATES", {}).get(data.get("state", "TODO").upper()),
        "start_date": data.get("start_date"),
        "target_date": data.get("target_date"),
    }

    # Resolve estimate_point if provided as numeric name
    raw_estimate = data.get("estimate_point")
    if raw_estimate:
        estimate_id = None
        estimate_map = context.get("ESTIMATES", {})
        estimate_id = estimate_map.get(str(raw_estimate))

        if not estimate_id:
            if len(str(raw_estimate)) > 30:  # UUID
                estimate_id = raw_estimate
            else:
                print(
                    f"Warning: Could not resolve estimate '{raw_estimate}' from context."
                )
                estimate_id = raw_estimate

        payload["estimate_point"] = estimate_id

    # Associate with Cycle/Module
    if cycle_id:
        payload["cycle"] = cycle_id
    if module_id:
        payload["module"] = module_id

    # Resolve input labels to UUIDs
    label_ids = []
    for label_name in data.get("labels", []):
        uid = label_map.get(label_name.upper())
        if uid:
            label_ids.append(uid)
        else:
            print(f"Warning: Label '{label_name}' not found in project.")

    if label_ids:
        payload["labels"] = label_ids

    if update_id:
        url = f"{API_BASE}/work-items/{update_id}/"
        resp = requests.patch(url, headers=headers, json=payload)
        action = "Updated"
    else:
        url = f"{API_BASE}/work-items/"
        resp = requests.post(url, headers=headers, json=payload)
        action = "Created"

    if resp.status_code in (200, 201):
        result = resp.json()
        seq = result.get("sequence_id", "?")
        print(f"\nSUCCESS {action}: AGENT-{seq}")
        print(f"   Name: {data['name']}")
        print(f"   URL:  https://app.plane.so/{WORKSPACE_SLUG}/browse/AGENT-{seq}/")
        return result
    else:
        print(f"Error {action.lower()} work item: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)


def check_artifacts_exist(data: dict) -> list:
    """
    Check if referenced artifacts exist in the repo.
    Returns a list of missing artifacts that need prerequisite issues.
    """
    repo_root = os.path.abspath(os.path.join(SKILL_ROOT, "..", "..", "..", ".."))
    missing = []

    checks = {
        "workflows": ".agent/workflows",
        "skills": ".agent/skills",
        "rules": ".agent/rules",
    }

    for field, base_dir in checks.items():
        for asset in data.get(field, []):
            if asset.startswith("[NEW] "):
                missing.append({"type": field, "name": asset.replace("[NEW] ", "")})
                continue
            # Check if the artifact directory/file exists
            asset_path = os.path.join(repo_root, base_dir)
            if os.path.isdir(asset_path):
                # Check for the asset as a subdirectory or .md file
                found = False
                for entry in os.listdir(asset_path):
                    if entry == asset or entry == f"{asset}.md":
                        found = True
                        break
                    # Check subdirectories
                    sub = os.path.join(asset_path, entry)
                    if os.path.isdir(sub):
                        for sub_entry in os.listdir(sub):
                            if sub_entry == asset or sub_entry == f"{asset}.md":
                                found = True
                                break
                    if found:
                        break
                if not found:
                    missing.append({"type": field, "name": asset})

    return missing


def report_missing_artifacts(missing: list):
    """Report missing artifacts that should be created as prerequisite issues."""
    if not missing:
        return

    print("\nWARNING: Missing Artifacts Detected (Continuous Self-Improvement)")
    print("   The following artifacts don't exist yet and should be created:")
    print("   Consider creating prerequisite Plane issues for these:\n")
    for m in missing:
        print(f"   - [{m['type'].upper()}] {m['name']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Create a Plane work item from a JSON template input."
    )
    parser.add_argument("--json", required=True, help="Path to the JSON input file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render to tmp/dry_run.html instead of creating",
    )
    parser.add_argument(
        "--update",
        help="Update an existing issue by its UUID instead of creating a new one",
    )
    args = parser.parse_args()

    # Load input
    data = load_input(args.json)

    # Check for missing artifacts
    missing = check_artifacts_exist(data)
    report_missing_artifacts(missing)

    # Render template
    html = render_template(data)

    if args.dry_run:
        out_path = os.path.join(
            SKILL_ROOT, "..", "..", "..", "..", "tmp", "dry_run.html"
        )
        out_path = os.path.abspath(out_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\nSUCCESS Dry-run complete. HTML written to:\n   {out_path}\n")
        return

    # Create or update work item
    create_work_item(data, html, args.update)


if __name__ == "__main__":
    main()
