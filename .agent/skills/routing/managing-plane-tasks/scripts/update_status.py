#!/usr/bin/env python3
"""
Update Status — Utility to transition Plane issues between states.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/update_status.py \\
        --issue AGENT-126 --state "In Progress"
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

# State Mapping (UUIDs) from context or fallback
STATES = context.get(
    "STATES",
    {
        "BACKLOG": "294ddb00-19ce-4ffe-9eac-2fd4e998d7f8",
        "TODO": "8e155185-58ad-404b-8458-6a7c9edbf09b",
        "IN PROGRESS": "d89aabd2-46d4-4f46-8ce4-eb49e06cac03",
        "DONE": "ef4b2395-3edb-41e9-adcd-7ec77d534f0f",
        "CANCELLED": "0723fa1c-6935-4661-a873-f5295203e58c",
    },
)


def update_status(issue_seq_id, state_name):
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    # 1. Resolve State UUID
    state_id = STATES.get(state_name.upper())
    if not state_id:
        print(
            f"Error: Invalid state name '{state_name}'. Choose from: {', '.join(STATES.keys())}"
        )
        sys.exit(1)

    # 2. Resolve Issue Sequence ID to UUID
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

    # 3. Update Status
    patch_url = f"{API_BASE}/issues/{issue_uuid}/"
    payload = {"state": state_id}
    resp = requests.patch(patch_url, headers=headers, json=payload)
    if resp.status_code == 200:
        print(f"SUCCESS: Updated status of {issue_seq_id} to '{state_name}'")
    else:
        print(f"Error updating status: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Update the status of a Plane issue.")
    parser.add_argument(
        "--issue", required=True, help="Issue identifier (e.g., AGENT-126)"
    )
    parser.add_argument(
        "--state", required=True, help="State name (e.g., 'In Progress', 'Done')"
    )
    args = parser.parse_args()

    update_status(args.issue, args.state)


if __name__ == "__main__":
    main()
