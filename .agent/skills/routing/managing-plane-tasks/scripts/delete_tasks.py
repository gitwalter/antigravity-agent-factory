#!/usr/bin/env python3
"""
Deleting Plane issues in bulk.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/delete_tasks.py \\
        --issues AGENT-155 AGENT-156
"""

import os
import requests
import argparse
import json

# Retrieve API config from environment
PLANE_API_TOKEN = os.environ.get("PLANE_API_TOKEN")
WORKSPACE = "agent-factory"
PROJECT_ID = "e71eb003-87d4-4b0c-a765-a044ac5affbe"
HEADERS = {"x-api-key": PLANE_API_TOKEN, "Content-Type": "application/json"}


def get_issue_uuid(issue_id):
    """
    Resolves sequence ID (AGENT-123) to UUID.
    """
    url = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}/work-items/?search={issue_id}&limit=1"
    try:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            for item in results:
                if (
                    f"AGENT-{item['sequence_id']}" == issue_id
                    or str(item["sequence_id"]) == issue_id
                ):
                    return item["id"]
    except Exception as e:
        print(f"Error resolving {issue_id}: {e}")
    return None


def delete_issue(uuid):
    """
    Deletes a single issue by UUID.
    """
    url = f"https://api.plane.so/api/v1/workspaces/{WORKSPACE}/projects/{PROJECT_ID}/work-items/{uuid}/"
    try:
        resp = requests.delete(url, headers=HEADERS)
        return resp.status_code
    except Exception as e:
        print(f"Error deleting {uuid}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Delete Plane issues in bulk.")
    parser.add_argument(
        "--issues",
        nargs="+",
        required=True,
        help="List of Issue IDs (e.g. AGENT-155) or UUIDs",
    )
    args = parser.parse_args()

    if not PLANE_API_TOKEN:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        return

    for issue_id in args.issues:
        print(f"Processing {issue_id}...")

        # Heuristic: check if it's already a UUID
        if len(issue_id) > 30 and "-" in issue_id:
            uuid = issue_id
        else:
            uuid = get_issue_uuid(issue_id)

        if not uuid:
            print(f"  Error: Could not resolve UUID for {issue_id}")
            continue

        status = delete_issue(uuid)
        if status in [200, 204]:
            print(f"  SUCCESS: Deleted {issue_id}")
        else:
            print(f"  FAILED: Status {status}")


if __name__ == "__main__":
    main()
