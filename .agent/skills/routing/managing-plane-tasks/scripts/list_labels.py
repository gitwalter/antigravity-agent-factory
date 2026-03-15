#!/usr/bin/env python3
"""
List Labels — Utility to find labels in Plane.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/list_labels.py
"""

import os
import sys
import requests
import json

# --- Configuration ---
WORKSPACE_SLUG = "agent-factory"
PROJECT_ID = "e71eb003-87d4-4b0c-a765-a044ac5affbe"
API_BASE = (
    f"https://api.plane.so/api/v1/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}"
)


def get_labels():
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    url = f"{API_BASE}/labels/"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])

        if not results:
            print("No labels found.")
            return

        print(f"\nPlane Labels for PROJECT: {PROJECT_ID}")
        print("-" * 60)

        # Sort labels by name for better readability
        results.sort(key=lambda x: x.get("name", "").lower())

        for item in results:
            name = item.get("name", "Unnamed")
            uid = item.get("id")
            color = item.get("color", "N/A")

            print(f"[{name}]")
            print(f"   ID:    {uid}")
            print(f"   Color: {color}")
            print("-" * 60)
    else:
        print(f"Error fetching labels: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)


if __name__ == "__main__":
    get_labels()
