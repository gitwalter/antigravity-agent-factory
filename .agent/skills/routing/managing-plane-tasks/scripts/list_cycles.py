#!/usr/bin/env python3
"""
List Cycles — Utility to find active and upcoming cycles in Plane.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/list_cycles.py
"""

import os
import sys
import requests
import json
from datetime import datetime

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


def get_cycles():
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    url = f"{API_BASE}/cycles/"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])

        if not results:
            print("No cycles found.")
            return

        print(f"\nPlane Cycles for PROJECT: {PROJECT_ID}")
        print("-" * 60)

        now = datetime.now()

        for item in results:
            name = item.get("name", "Unnamed")
            uid = item.get("id")
            start = item.get("start_date")
            end = item.get("end_date")

            # Determine state based on dates if state isn't explicitly provided in the list result
            status = "UPCOMING"
            if start and end:
                s_dt = datetime.strptime(start[:10], "%Y-%m-%d")
                e_dt = datetime.strptime(end[:10], "%Y-%m-%d")
                if s_dt <= now <= e_dt:
                    status = "ACTIVE"
                elif now > e_dt:
                    status = "PAST"

            print(f"[{status}] {name}")
            print(f"   ID:    {uid}")
            if start and end:
                print(f"   Dates: {start} to {end}")
            print("-" * 60)
    else:
        print(f"Error fetching cycles: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)


if __name__ == "__main__":
    get_cycles()
