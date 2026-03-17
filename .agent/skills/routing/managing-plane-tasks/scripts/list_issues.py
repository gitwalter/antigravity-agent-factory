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
from typing import List, Optional, Dict

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


def resolve_id(name: str, category: str, context: Dict) -> Optional[str]:
    """Resolve a name to a UUID using project context."""
    if not name:
        return None

    # If it's already a UUID, return it
    if len(name) > 30 and "-" in name:
        return name

    # Search in context
    search_maps = {
        "cycle": ["ALL_CYCLES", "ACTIVE_CYCLE"],
        "module": ["ACTIVE_MODULES"],
        "state": ["STATES"],
        "label": ["LABELS"],
    }

    maps = search_maps.get(category, [])
    for map_key in maps:
        data = context.get(map_key, {})
        if isinstance(data, dict):
            # Special case for ACTIVE_CYCLE which is a dict with 'name' and 'id'
            if (
                map_key == "ACTIVE_CYCLE"
                and data.get("name", "").lower() == name.lower()
            ):
                return data.get("id")

            # Normal name -> id maps
            for k, v in data.items():
                if k.lower() == name.lower():
                    return v
    return None


def get_issues(
    cycle=None, module=None, labels=None, state=None, open_only=False, assignee=None
):
    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN environment variable not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    # Resolve names to UUIDs
    res_cycle = (
        resolve_id(cycle, "cycle", context)
        if cycle
        else (
            context.get("ACTIVE_CYCLE", {}).get("id")
            if not any([cycle, module, labels, state])
            else None
        )
    )
    res_module = resolve_id(module, "module", context) if module else None
    res_state = resolve_id(state, "state", context) if state else None

    # Handle 'open_only' status filtering
    # Backlog, Todo, In Progress are typical 'open' states.
    # We'll resolve these by group if possible or by name.
    open_state_ids = []
    if open_only:
        for s_name, s_id in context.get("STATES", {}).items():
            if s_name.lower() in [
                "backlog",
                "todo",
                "in progress",
                "in-progress",
                "ready",
            ]:
                open_state_ids.append(s_id)

    params = {}
    if res_cycle:
        params["cycle"] = res_cycle
    if res_module:
        params["module"] = res_module
    if res_state:
        params["state"] = res_state
    if labels:
        params["labels"] = labels  # Labels remains comma-sep UUIDs for now
    if assignee:
        params["assignees"] = assignee  # Support assignee UUID

    url = f"{API_BASE}/issues/"
    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])

        # Post-filter for 'open' if requested and state not explicitly provided
        if open_only and not res_state:
            results = [r for r in results if r.get("state") in open_state_ids]

        if not results:
            print("No issues found matching the filters.")
            return

        print(f"\nPlane Issues | Filtered ({len(results)} found)")
        print(f"{'Issue ID':<15} | {'Title':<50} | {'State':<15} | {'Points':<8}")
        print("-" * 96)

        estimate_map = context.get("ESTIMATES", {})
        # Create inverse map for display: UUID -> Name
        reverse_estimates = {v: k for k, v in estimate_map.items()}

        for item in results:
            name = item.get("name", "Unnamed")
            sid = item.get("sequence_id")
            state_id = item.get("state")
            est_id = item.get("estimate_point")
            full_sid = f"AGENT-{sid}"

            # Resolve state name
            state_name = item.get("state_detail", {}).get("name")
            if not state_name and state_id:
                for s_name, s_id in context.get("STATES", {}).items():
                    if s_id == state_id:
                        state_name = s_name
                        break
            state_name = state_name or "N/A"

            # Resolve point value
            points = reverse_estimates.get(est_id, "N/A")

            # Truncate title for display
            display_name = (name[:47] + "..") if len(name) > 50 else name
            print(
                f"{full_sid:<15} | {display_name:<50} | {state_name:<15} | {points:<8}"
            )
    else:
        print(f"Error fetching issues: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List and filter Plane issues.")
    parser.add_argument("--cycle", help="Filter by Cycle ID or Name")
    parser.add_argument("--module", help="Filter by Module ID or Name")
    parser.add_argument("--labels", help="Filter by Label IDs (comma-separated)")
    parser.add_argument("--state", help="Filter by State ID or Name")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Filter for 'open' issues (Backlog, Todo, In Progress)",
    )
    parser.add_argument("--assignee", help="Filter by Assignee UUID")

    args = parser.parse_args()
    get_issues(
        cycle=args.cycle,
        module=args.module,
        labels=args.labels,
        state=args.state,
        open_only=args.open,
        assignee=args.assignee,
    )
