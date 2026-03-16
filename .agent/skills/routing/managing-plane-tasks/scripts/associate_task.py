#!/usr/bin/env python3
"""
Associate Task — Utility to assign Plane issues to modules and cycles.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/associate_task.py \\
        --issue AGENT-126 --module MODULE_UUID --cycle CYCLE_UUID
"""

import argparse
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


def associate_issue(issue_seq_id, module_id=None, cycle_id=None):
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
        # Check for exact sequence match
        if f"AGENT-{issue['sequence_id']}" == issue_seq_id:
            issue_uuid = issue["id"]
            break

    if not issue_uuid:
        print(f"Error: Could not find UUID for issue {issue_seq_id}")
        sys.exit(1)

    print(f"Found Issue UUID: {issue_uuid}")

    # 2. Associate with Module
    if module_id:
        print(f"Adding to module {module_id}...")
        # Note: The endpoint might be /modules/{module_id}/issues/ or /issues/{issue_uuid}/
        # Plane API often uses a bulk add endpoint or a patch on the issue.
        # However, the documented way in some versions is:
        module_url = f"{API_BASE}/modules/{module_id}/module-issues/"
        payload = {"issues": [issue_uuid]}
        resp = requests.post(module_url, headers=headers, json=payload)
        if resp.status_code in (200, 201):
            print("Successfully associated with module.")
        else:
            # Try alternate endpoint if 404
            alt_url = f"{API_BASE}/modules/{module_id}/issues/"
            resp = requests.post(alt_url, headers=headers, json=payload)
            if resp.status_code in (200, 201):
                print("Successfully associated with module (alt endpoint).")
            else:
                print(f"Error associating with module: {resp.status_code}")
                print(resp.text[:500])

    # 3. Associate with Cycle
    if cycle_id:
        print(f"Adding to cycle {cycle_id}...")
        cycle_url = f"{API_BASE}/cycles/{cycle_id}/cycle-issues/"
        payload = {"issues": [issue_uuid]}
        resp = requests.post(cycle_url, headers=headers, json=payload)
        if resp.status_code in (200, 201):
            print("Successfully associated with cycle.")
        else:
            # Try alternate endpoint if 404
            alt_url = f"{API_BASE}/cycles/{cycle_id}/issues/"
            resp = requests.post(alt_url, headers=headers, json=payload)
            if resp.status_code in (200, 201):
                print("Successfully associated with cycle (alt endpoint).")
            else:
                print(f"Error associating with cycle: {resp.status_code}")
                print(resp.text[:500])


def main():
    parser = argparse.ArgumentParser(
        description="Associate a Plane issue with a module and/or cycle."
    )
    parser.add_argument(
        "--issue", required=True, help="Issue identifier (e.g., AGENT-126)"
    )
    parser.add_argument("--module", help="Module UUID")
    parser.add_argument("--cycle", help="Cycle UUID")
    args = parser.parse_args()

    associate_issue(args.issue, args.module, args.cycle)


if __name__ == "__main__":
    main()
