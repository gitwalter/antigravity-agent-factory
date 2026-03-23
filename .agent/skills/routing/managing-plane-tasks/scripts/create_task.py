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
WORKSPACE_SLUG = "agent-factory"
PROJECT_ID = "e71eb003-87d4-4b0c-a765-a044ac5affbe"
API_BASE = (
    f"https://api.plane.so/api/v1/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}"
)


def render_template(data: dict) -> str:
    """Render the work item template using Jinja2."""
    file_loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=file_loader)
    template = env.get_template("work_item.html.j2")

    # Process complex fields into a format suitable for the template
    render_data = data.copy()
    if isinstance(render_data.get("requirements"), list):
        render_data["requirements_list"] = render_data["requirements"]

    # Provide defaults for list assets to avoid template iteration errors
    list_fields = [
        "workflows",
        "agents",
        "skills",
        "rules",
        "patterns",
        "blueprints",
        "templates",
        "tests",
        "knowledge",
        "scripts",
        "memory_queries",
    ]
    for field in list_fields:
        if field not in render_data or render_data[field] is None:
            render_data[field] = []

    # Handle schema_version/type if they exist in schema
    if "schema_version" in data:
        render_data["schema_json"] = json.dumps(data, indent=2)

    return template.render(**render_data)


def check_artifacts_exist(data: dict) -> list:
    """Validate that declared workflows, agents, and skills exist in the filesystem."""
    repo_root = os.path.abspath(os.path.join(SKILL_ROOT, "..", "..", ".."))
    missing = []

    # Check Workflows
    for wf in data.get("workflows", []):
        path = os.path.join(repo_root, ".agent", "workflows", f"{wf}.md")
        if not os.path.exists(path):
            missing.append({"type": "workflow", "name": wf, "path": path})

    # Check Agents (handling subdirectories)
    agent_dirs = [
        "chain",
        "routing",
        "parallel",
        "orchestrator-workers",
        "evaluator-optimizer",
    ]
    for agent in data.get("agents", []):
        found = False
        for d in agent_dirs:
            path = os.path.join(repo_root, ".agent", "agents", d, f"{agent}.md")
            if os.path.exists(path):
                found = True
                break
        if not found:
            missing.append(
                {"type": "agent", "name": agent, "path": "multiple searchable paths"}
            )

    # Check Skills
    for skill in data.get("skills", []):
        found = False
        skill_patterns = [
            "chain",
            "routing",
            "parallel",
            "orchestrator-workers",
            "evaluator-optimizer",
        ]
        for p in skill_patterns:
            path = os.path.join(repo_root, ".agent", "skills", p, skill, "SKILL.md")
            if os.path.exists(path):
                found = True
                break
        if not found:
            missing.append(
                {"type": "skill", "name": skill, "path": "multiple searchable paths"}
            )

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


def create_work_item(data: dict, html: str, update_id: str = None):
    """Create or update a Plane work item."""
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "name": data["name"],
        "description_html": html,
        "priority": data.get("priority", "none").lower(),
        "start_date": data.get("start_date"),
        "target_date": data.get("target_date"),
    }

    # Resolve Cycle (by name or UUID)
    cycle_id = None
    raw_cycle = data.get("cycle")
    if raw_cycle:
        if len(str(raw_cycle)) > 30:  # Likely a UUID
            cycle_id = raw_cycle
        else:
            cycle_id = context.get("CYCLES", {}).get(raw_cycle.upper())
            if not cycle_id and raw_cycle.lower() == "active":
                cycle_id = context.get("ACTIVE_CYCLE_ID")

    # Resolve Module (by name or UUID)
    module_id = None
    raw_module = data.get("module")
    if raw_module:
        if len(str(raw_module)) > 30:
            module_id = raw_module
        else:
            module_id = context.get("MODULES", {}).get(raw_module.upper())

    # Map Estimate Point (numeric name to UUID)
    raw_estimate = data.get("estimate_point")
    if raw_estimate:
        estimate_map = context.get("ESTIMATES", {})
        estimate_id = estimate_map.get(str(raw_estimate))
        if not estimate_id:
            estimate_id = raw_estimate if len(str(raw_estimate)) > 30 else None

        if estimate_id:
            payload["estimate_point"] = estimate_id

    # Resolve Labels
    label_map = context.get("LABELS", {})
    label_ids = []
    for lbl in data.get("labels", []):
        uid = label_map.get(lbl.upper())
        if uid:
            label_ids.append(uid)
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
        new_id = result.get("id")
        seq = result.get("sequence_id", "?")

        # Link extras
        if cycle_id:
            requests.post(
                f"{API_BASE}/cycles/{cycle_id}/work-items/",
                headers=headers,
                json={"work_items": [new_id]},
            )
        if module_id:
            requests.post(
                f"{API_BASE}/modules/{module_id}/work-items/",
                headers=headers,
                json={"work_items": [new_id]},
            )

        print(f"\nSUCCESS {action}: AGENT-{seq}")
        print(f"   Name: {data['name']}")
        print(f"   URL: https://app.plane.so/{WORKSPACE_SLUG}/browse/AGENT-{seq}/")
        return result
    else:
        print(f"Error {action.lower()} work item: {resp.status_code}")
        print(f"   Response: {resp.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Create/Update Plane Tasks")
    parser.add_argument("--json", help="Path to JSON data")
    parser.add_argument("--update", help="UUID to update")
    parser.add_argument("--issue-id", help="Alias for update")
    parser.add_argument("--name", help="Task name")
    parser.add_argument("--priority", help="Priority")
    parser.add_argument("--requirements", help="Semicolon-separated")
    parser.add_argument("--acceptance-criteria", help="Semicolon-separated")
    parser.add_argument("--workflows", help="Semicolon-separated")
    parser.add_argument("--agents", help="Semicolon-separated")
    parser.add_argument("--skills", help="Semicolon-separated")
    parser.add_argument("--tests", help="Semicolon-separated type:script:exp")
    parser.add_argument("--start-date", help="YYYY-MM-DD")
    parser.add_argument("--target-date", help="YYYY-MM-DD")
    parser.add_argument("--estimate-point", help="Numeric name or UUID")
    parser.add_argument("--module", help="Name or UUID")
    parser.add_argument("--cycle", help="Name, UUID or 'active'")
    parser.add_argument("--notes", help="Notes")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    data = {}
    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)

    def split_arg(v):
        return [x.strip() for x in v.split(";") if x.strip()] if v else None

    # Merge CLI
    if args.name:
        data["name"] = args.name
    if args.priority:
        data["priority"] = args.priority
    if args.requirements:
        data["requirements"] = split_arg(args.requirements)
    if args.acceptance_criteria:
        data["acceptance_criteria"] = split_arg(args.acceptance_criteria)
    if args.workflows:
        data["workflows"] = split_arg(args.workflows)
    if args.agents:
        data["agents"] = split_arg(args.agents)
    if args.skills:
        data["skills"] = split_arg(args.skills)
    if args.start_date:
        data["start_date"] = args.start_date
    if args.target_date:
        data["target_date"] = args.target_date
    if args.estimate_point:
        data["estimate_point"] = args.estimate_point
    if args.module:
        data["module"] = args.module
    if args.cycle:
        data["cycle"] = args.cycle
    if args.notes:
        data["notes"] = args.notes

    if args.tests:
        t_list = []
        for t_raw in split_arg(args.tests):
            p = t_raw.split(":", 2)
            if len(p) == 3:
                t_list.append({"type": p[0], "script": p[1], "expected": p[2]})
            else:
                t_list.append({"type": "UNIT", "script": "", "expected": p[0]})
        data["tests"] = t_list

    if not data.get("name"):
        print("Error: Missing task name.")
        sys.exit(1)

    missing = check_artifacts_exist(data)
    report_missing_artifacts(missing)

    html = render_template(data)

    if args.dry_run:
        print("\nDRY RUN HTML (Trimmed):\n")
        print(html[:500] + "...")
        return

    update_id = args.update or args.issue_id
    create_work_item(data, html, update_id)


if __name__ == "__main__":
    main()
