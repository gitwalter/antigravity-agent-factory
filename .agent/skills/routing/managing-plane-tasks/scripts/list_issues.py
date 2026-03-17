#!/usr/bin/env python3
"""
List Issues — Utility to find and filter issues in Plane.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/list_issues.py \\
        --cycle 913be610-6328-4ccf-ad98-b79923a005dc
"""

import os
import sys
import requests
import json
import argparse
from datetime import datetime

# --- Configuration ---
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT_FILE = os.path.join(SKILL_ROOT, "references", "project_context.json")


def load_context():
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


def get_issues(cycle=None, module=None, labels=None, state=None):
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    params = {}
    if cycle:
        params["cycle"] = cycle
    if module:
        params["module"] = module
    if labels:
        params["labels"] = labels
    if state:
        params["state"] = state

    url = f"{API_BASE}/issues/"
    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])

        if not results:
            print("No issues found matches the filters.")
            return

        print(f"\nFiltered Plane Issues for PROJECT: {PROJECT_ID}")
        print("-" * 80)

        for item in results:
            name = item.get("name", "Unnamed")
            sid = item.get("sequence_id")
            uid = item.get("id")
            state_name = item.get("state_detail", {}).get("name", "N/A")

            print(f"[{PROJECT_ID}-{sid}] {name}")
            print(f"   ID:    {uid}")
            print(f"   State: {state_name}")
            print("-" * 80)
    else:
        print(f"Error fetching issues: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List and filter Plane issues.")
    parser.add_argument("--cycle", help="Filter by Cycle ID")
    parser.add_argument("--module", help="Filter by Module ID")
    parser.add_argument("--labels", help="Filter by Label IDs (comma-separated)")
    parser.add_argument("--state", help="Filter by State ID")

    args = parser.parse_args()
    get_issues(
        cycle=args.cycle, module=args.module, labels=args.labels, state=args.state
    )
