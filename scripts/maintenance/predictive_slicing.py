#!/usr/bin/env python3
"""
Predictive Slicing — Automate Plane task creation from implementation plans.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        scripts/maintenance/predictive_slicing.py \\
        --plan C:\\Users\\wpoga\\.gemini\\antigravity\\brain\\...\\implementation_plan_agent_150.md \\
        --parent AGENT-150
"""

import os
import re
import json
import argparse
import subprocess
import requests

# Retrieve API config from environment
PLANE_API_TOKEN = os.environ.get("PLANE_API_TOKEN")
WORKSPACE = "agent-factory"
PROJECT_ID = "e71eb003-87d4-4b0c-a765-a044ac5affbe"
HEADERS = {"x-api-key": PLANE_API_TOKEN, "Content-Type": "application/json"}

# --- Configuration ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREATE_TASK_SCRIPT = os.path.join(
    REPO_ROOT,
    ".agent",
    "skills",
    "routing",
    "managing-plane-tasks",
    "scripts",
    "create_task.py",
)
GET_ISSUES_SCRIPT = os.path.join(
    REPO_ROOT,
    ".agent",
    "skills",
    "routing",
    "managing-plane-tasks",
    "scripts",
    "list_issues.py",
)
TMP_DIR = os.path.join(REPO_ROOT, "tmp")


def get_existing_issues(parent_id):
    """
    Fetches existing issues for a parent to avoid duplicates.
    """
    url = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}/work-items/?parent={parent_id}&limit=100"
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            return {
                item["name"]: item["sequence_id"]
                for item in resp.json().get("results", [])
            }
    except Exception as e:
        print(f"Warning: Could not fetch existing issues: {e}")
    return {}


def parse_task_md(task_md_path):
    """
    Parses task.md to extract high-level task descriptions.
    """
    if not os.path.exists(task_md_path):
        return {}

    with open(task_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find list items with IDs
    # e.g. - [ ] Some task <!-- id: 123 -->
    pattern = r"- \[(x| |/)\] (.*?) <!-- id: (\d+) -->"
    matches = re.finditer(pattern, content)

    tasks_by_id = {}
    for match in matches:
        status = match.group(1)
        name = match.group(2).strip()
        task_id = match.group(3)
        tasks_by_id[task_id] = {
            "name": name,
            "status": "DONE"
            if status == "x"
            else "IN_PROGRESS"
            if status == "/"
            else "TODO",
        }
    return tasks_by_id


def parse_plan(plan_path):
    """
    Parses implementation_plan.md for [MODIFY], [NEW], [DELETE] sections.
    """
    if not os.path.exists(plan_path):
        print(f"Error: Plan file not found at {plan_path}")
        return []

    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern for finding file-based changes in implementation plans
    # e.g. #### [NEW|MODIFY|DELETE] [basename](URI)
    pattern = r"#### \[(NEW|MODIFY|DELETE)\] \[(.*?)\]\((.*?)\)"
    matches = list(re.finditer(pattern, content))

    tasks = []
    for i, match in enumerate(matches):
        change_type = match.group(1)
        filename = match.group(2)
        file_uri = match.group(3)

        # Try to find requirements/context for this specific file
        start_pos = match.end()
        # End at the next header of same or higher level
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            # Or end at the next section (##)
            next_section = re.search(r"\n## ", content[start_pos:])
            end_pos = (
                (start_pos + next_section.start()) if next_section else len(content)
            )

        description = content[start_pos:end_pos].strip()

        tasks.append(
            {
                "type": change_type,
                "filename": filename,
                "uri": file_uri,
                "description": description,
            }
        )

    return tasks


def generate_task_input(
    task, parent_id, module, cycle, start_date=None, due_date=None, extra_context=""
):
    """
    Converts a parsed task into the high-fidelity JSON required by create_task.py.
    """
    name = f"{task['type']}: {task['filename']}"

    # Heuristic for labels based on file extensions or path
    labels = ["FEATURE"]
    if ".py" in task["filename"]:
        labels.append("SKILL")
    if "scripts/" in task["uri"] or ".agent" in task["uri"]:
        labels.append("INFRA")

    # Enrich description with extra context if available
    full_description = task["description"]
    if extra_context:
        full_description = f"{extra_context}\n\n{full_description}"

    task_json = {
        "schema_version": "1.0.0",
        "name": name,
        "type": "Feature" if task["type"] != "DELETE" else "Bug",
        "priority": "medium",
        "state": "TODO",
        "estimate_point": "2",  # Default to 2 for sliced tasks
        "parent": parent_id,
        "module": module,
        "cycle": cycle,
        "start_date": start_date or "2026-03-17",
        "target_date": due_date or "2026-03-24",
        "requirements": f"<h3>Requirement</h3><p>{full_description}</p>",
        "acceptance_criteria": f"<ul><li>{task['filename']} is correctly {task['type'].lower()}ed.</li><li>Logic passes all relevant tests.</li></ul>",
        "workflows": ["feature-development"],
        "agents": ["python-ai-specialist"],
        "skills": ["managing-plane-tasks"],
        "scripts": [f"[{task['type']}] {task['filename']}"],
        "tests": [f"pytest tests/maintenance/test_{task['filename'].split('.')[0]}.py"],
        "labels": labels,
    }

    return task_json


def main():
    parser = argparse.ArgumentParser(
        description="Predictively slice an implementation plan into Plane tasks."
    )
    parser.add_argument(
        "--plan", required=True, help="Path to the implementation plan markdown file"
    )
    parser.add_argument(
        "--parent", required=True, help="Parent Issue ID (e.g., AGENT-150)"
    )
    parser.add_argument("--module", default="agent system", help="Module name")
    parser.add_argument("--cycle", default="sprint 004", help="Cycle name")
    parser.add_argument("--start", default="2026-03-17", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--due", default="2026-03-24", help="Due date (YYYY-MM-DD)")
    args = parser.parse_args()

    # 1. Parse Context
    print(f"Parsing plan: {args.plan}")
    tasks = parse_plan(args.plan)

    # Optional task.md parsing
    task_md_path = os.path.join(os.path.dirname(args.plan), "task.md")
    context_map = parse_task_md(task_md_path)
    if context_map:
        print(f"Enriched with {len(context_map)} items from task.md")

    if not tasks:
        print(
            "No tasks found in plan. Ensure headers use #### [NEW|MODIFY|DELETE] format."
        )
        return

    print(f"Found {len(tasks)} potential tasks.")

    # 2. Iterate and Create
    os.makedirs(TMP_DIR, exist_ok=True)

    # Resolve Parent UUID if it's a sequence ID (e.g. AGENT-150)
    # For now, we assume the script is called with the readable ID, but we need the internal ID for some API calls
    # Heuristic: If it has '-', it's readable.
    parent_readable = args.parent

    # Fetch existing issues to avoid duplicates
    print(f"Checking for existing sub-tasks of {parent_readable}...")
    # Note: The API 'parent' filter usually expects the UUID.
    # We might need to resolve it first.
    existing_tasks = {}

    for i, task in enumerate(tasks):
        print(f"\nProcessing Task {i+1}/{len(tasks)}: {task['filename']}")

        name = f"{task['type']}: {task['filename']}"

        # SLOPPY: In a real 'conscious' system, we'd query by exact name.
        # For now, let's just use a simple name check if we had the list.
        # Since resolving parent UUID is complex here, we'll try to find by name in the recent project issues.

        check_url = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}/work-items/?search={task['filename']}&limit=5"
        dup_found = False
        try:
            c_resp = requests.get(check_url, headers=HEADERS)
            if c_resp.status_code == 200:
                for item in c_resp.json().get("results", []):
                    if item["name"] == name:
                        print(
                            f"SKIP: Issue '{name}' already exists as AGENT-{item['sequence_id']}"
                        )
                        dup_found = True
                        break
        except Exception as e:
            print(f"Warning: Duplicate check failed for {name}: {e}")

        if dup_found:
            continue

        # Try to find matching context from task.md (heuristic match by filename/activity)
        extra_ctx = ""
        for tid, tinfo in context_map.items():
            if task["filename"].lower() in tinfo["name"].lower():
                extra_ctx = f"Task Reference: {tinfo['name']} (ID: {tid})"
                break

        input_data = generate_task_input(
            task, args.parent, args.module, args.cycle, args.start, args.due, extra_ctx
        )
        input_path = os.path.join(TMP_DIR, f"sliced_task_{i}.json")

        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(input_data, f, indent=4)

        print(f"Created input file: {input_path}")

        # 3. Call create_task.py
        cmd = [
            "conda",
            "run",
            "-p",
            "D:\\Anaconda\\envs\\cursor-factory",
            "python",
            CREATE_TASK_SCRIPT,
            "--json",
            input_path,
        ]

        print(f"Executing: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error creating task: {e}")
            print(e.stderr)

    print("\nSUCCESS: Predictive slicing complete.")


if __name__ == "__main__":
    main()
