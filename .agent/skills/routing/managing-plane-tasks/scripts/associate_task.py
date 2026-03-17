#!/usr/bin/env python3
"""
Associate Task — Utility to assign Plane issues to modules and cycles.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/associate_task.py \\
        --issue AGENT-126 --module MODULE_UUID --cycle CYCLE_UUID
"""

import argparse
import json
import os
import sys
import requests

# --- Configuration ---
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT_FILE = os.path.join(SKILL_ROOT, "references", "project_context.json")


def load_context():
    """Load persistent context for IDs and mappings."""
    if os.path.exists(CONTEXT_FILE):
        try:
            with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load context file: {e}")
    return {}


context = load_context()
WORKSPACE_SLUG = context.get("WORKSPACE_SLUG", "agent-factory")
PROJECT_ID = context.get("PROJECT_ID", "e71eb003-87d4-4b0c-a765-a044ac5affbe")
API_BASE = (
    f"https://api.plane.so/api/v1/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}"
)


def associate_issue(
    issue_seq_id,
    module_name_or_id=None,
    cycle_name_or_id=None,
    estimate=None,
    start_date=None,
    due_date=None,
    parent_seq_id=None,
):
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    # 1. Resolve Issue Sequence ID to UUID
    print(f"Resolving issue {issue_seq_id}...")
    search_url = f"{API_BASE}/issues/?search={issue_seq_id}"
    resp = requests.get(search_url, headers=headers)
    if resp.status_code != 200:
        print(f"Error searching issue: {resp.status_code}")
        sys.exit(1)

    issues = resp.json().get("results", [])
    issue_uuid = None
    for issue in issues:
        if f"AGENT-{issue['sequence_id']}" == issue_seq_id:
            issue_uuid = issue["id"]
            break

    if not issue_uuid:
        print(f"Error: Could not find UUID for issue {issue_seq_id}")
        sys.exit(1)

    print(f"Found Issue UUID: {issue_uuid}")

    update_payload = {}

    # 2. Resolve Module
    if module_name_or_id:
        module_id = None
        active_modules = context.get("ACTIVE_MODULES", {})
        for name, uid in active_modules.items():
            if name.lower() == module_name_or_id.lower():
                module_id = uid
                break

        if not module_id:
            if len(module_name_or_id) > 30:  # Heuristic for UUID
                module_id = module_name_or_id
            else:
                print(f"Error: Could not resolve module name '{module_name_or_id}'")

        if module_id:
            print(f"Adding to module {module_id}...")
            module_url = f"{API_BASE}/modules/{module_id}/module-issues/"
            payload = {"issues": [issue_uuid]}
            resp = requests.post(module_url, headers=headers, json=payload)
            if resp.status_code in (200, 201):
                print("Successfully associated with module.")
            else:
                print(f"Error associating with module: {resp.status_code}")
                print(resp.text[:500])

    # 3. Resolve Cycle
    if cycle_name_or_id:
        cycle_id = None
        active_cycle = context.get("ACTIVE_CYCLE", {})
        if active_cycle.get("name") == cycle_name_or_id:
            cycle_id = active_cycle.get("id")

        if not cycle_id:
            all_cycles = context.get("ALL_CYCLES", {})
            for name, uid in all_cycles.items():
                if name.lower() == cycle_name_or_id.lower():
                    cycle_id = uid
                    break

        if not cycle_id:
            if len(cycle_name_or_id) > 30:
                cycle_id = cycle_name_or_id
            else:
                print(f"Error: Could not resolve cycle name '{cycle_name_or_id}'")

        if cycle_id:
            print(f"Adding to cycle {cycle_id}...")
            cycle_url = f"{API_BASE}/cycles/{cycle_id}/cycle-issues/"
            payload = {"issues": [issue_uuid]}
            resp = requests.post(cycle_url, headers=headers, json=payload)
            if resp.status_code in (200, 201):
                print("Successfully associated with cycle.")
            else:
                print(f"Error associating with cycle: {resp.status_code}")
                print(resp.text[:500])

    # 4. Handle Estimation, Due Date, Parent
    if estimate:
        estimate_id = None
        estimate_map = context.get("ESTIMATES", {})
        # Try to resolve by name/string value (e.g., "8")
        estimate_id = estimate_map.get(str(estimate))

        if not estimate_id:
            if len(str(estimate)) > 30:  # Heuristic for UUID
                estimate_id = estimate
            else:
                print(f"Warning: Could not resolve estimate '{estimate}' from context.")
                # We'll still try to send it as is, maybe the API accepts integers
                estimate_id = estimate

        update_payload["estimate_point"] = estimate_id

    if start_date:
        update_payload["start_date"] = start_date

    if due_date:
        update_payload["target_date"] = due_date

    if parent_seq_id:
        print(f"Resolving parent issue {parent_seq_id}...")
        p_search_url = f"{API_BASE}/issues/?search={parent_seq_id}"
        p_resp = requests.get(p_search_url, headers=headers)
        if p_resp.status_code == 200:
            p_issues = p_resp.json().get("results", [])
            for p_issue in p_issues:
                if f"AGENT-{p_issue['sequence_id']}" == parent_seq_id:
                    update_payload["parent"] = p_issue["id"]
                    print(f"Found Parent UUID: {p_issue['id']}")
                    break
        if "parent" not in update_payload:
            print(f"Error: Could not find parent issue {parent_seq_id}")

    if update_payload:
        print(f"Updating issue {issue_uuid} with {update_payload}...")
        patch_url = f"{API_BASE}/issues/{issue_uuid}/"
        patch_resp = requests.patch(patch_url, headers=headers, json=update_payload)
        if patch_resp.status_code in (200, 204):
            print("Successfully updated issue metadata.")
        else:
            print(f"Error updating issue metadata: {patch_resp.status_code}")
            print(patch_resp.text[:500])


def main():
    parser = argparse.ArgumentParser(
        description="Associate a Plane issue with a module, cycle, estimate, due date, and/or parent."
    )
    parser.add_argument(
        "--issue", required=True, help="Issue identifier (e.g., AGENT-126)"
    )
    parser.add_argument("--module", help="Module UUID or Name")
    parser.add_argument("--cycle", help="Cycle UUID or Name")
    parser.add_argument("--estimate", help="Estimate (Point UUID or value)")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--parent", help="Parent Issue identifier (e.g., AGENT-100)")
    args = parser.parse_args()

    associate_issue(
        args.issue,
        args.module,
        args.cycle,
        args.estimate,
        args.start_date,
        args.due_date,
        args.parent,
    )


if __name__ == "__main__":
    main()
