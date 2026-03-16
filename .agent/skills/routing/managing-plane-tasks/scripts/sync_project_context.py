#!/usr/bin/env python3
"""
Sync Project Context — Synchronize local project_context.json with live Plane data.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/sync_project_context.py
"""

import json
import os
import sys
import requests
from datetime import datetime

# --- Configuration ---
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT_FILE = os.path.join(SKILL_ROOT, "references", "project_context.json")


def load_context():
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"Error: Context file not found at {CONTEXT_FILE}")
    sys.exit(1)


def save_context(data):
    data["LAST_SYNC"] = datetime.now().isoformat()
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"SUCCESS: Project context synchronized and saved to {CONTEXT_FILE}")


def main():
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    context = load_context()
    workspace = context["WORKSPACE_SLUG"]
    project = context["PROJECT_ID"]

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    base_url = f"https://api.plane.so/api/v1/workspaces/{workspace}/projects/{project}"

    # 1. Sync Labels
    print("Syncing Labels...")
    resp = requests.get(f"{base_url}/labels/", headers=headers)
    if resp.status_code == 200:
        results = resp.json().get("results", [])
        context["LABELS"] = {item["name"].upper(): item["id"] for item in results}
    else:
        print(f"Warning: Failed to sync labels ({resp.status_code})")

    # 2. Sync Cycles (Find Active)
    print("Syncing Cycles...")
    resp = requests.get(f"{base_url}/cycles/", headers=headers)
    if resp.status_code == 200:
        results = resp.json().get("results", [])
        now = datetime.now()
        active_found = False
        for item in results:
            start = item.get("start_date")
            end = item.get("end_date")
            if start and end:
                s_dt = datetime.strptime(start[:10], "%Y-%m-%d")
                e_dt = datetime.strptime(end[:10], "%Y-%m-%d")
                if s_dt <= now <= e_dt:
                    context["ACTIVE_CYCLE"] = {
                        "id": item["id"],
                        "name": item["name"],
                        "end_date": end,
                    }
                    active_found = True
                    break
        if not active_found:
            context["ACTIVE_CYCLE"] = {"id": None, "name": None, "end_date": None}
    else:
        print(f"Warning: Failed to sync cycles ({resp.status_code})")

    # 3. Sync Modules
    print("Syncing Modules...")
    resp = requests.get(f"{base_url}/modules/", headers=headers)
    if resp.status_code == 200:
        results = resp.json().get("results", [])
        context["ACTIVE_MODULES"] = {item["name"]: item["id"] for item in results}
    else:
        print(f"Warning: Failed to sync modules ({resp.status_code})")

    # 4. Sync States (Discovery)
    print("Syncing States...")
    resp = requests.get(f"{base_url}/states/", headers=headers)
    if resp.status_code == 200:
        results = resp.json().get("results", [])
        # Update existing states map if new names found, but keep canonical ones
        for item in results:
            name = item["name"].upper()
            context["STATES"][name] = item["id"]
    else:
        print(f"Warning: Failed to sync states ({resp.status_code})")

    save_context(context)


if __name__ == "__main__":
    main()
