#!/usr/bin/env python3
"""
Post Solution — Professional Solution Reporter for Plane

Renders a structured HTML solution comment from a JSON input file
and posts it to a specific Plane issue via the API.

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python \\
        .agent/skills/routing/managing-plane-tasks/scripts/post_solution.py \\
        --issue AGENT-48 \\
        --json solution_data.json \\
        --close
"""

import argparse
import json
import os
import sys
import requests

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Error: jinja2 not installed.")
    sys.exit(1)

# --- Configuration ---
WORKSPACE_SLUG = "agent-factory"
PROJECT_ID = "e71eb003-87d4-4b0c-a765-a044ac5affbe"
API_BASE = (
    f"https://api.plane.so/api/v1/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}"
)

# Paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
TEMPLATE_DIR = os.path.join(SKILL_ROOT, "templates")

DONE_STATE_ID = "ef4b2395-3edb-41e9-adcd-7ec77d534f0f"


def validate_depth(data: dict):
    """Enforce high-fidelity reporting standards to prevent 'alibi blablabla'."""
    errors = []

    # Validate architectural depth
    arch = data.get("architectural_decisions", [])
    if not arch:
        errors.append(
            "Missing 'architectural_decisions'. High-fidelity reporting demands deep technical insight."
        )
    elif len(arch) < 3 and not any(len(str(a).strip()) >= 50 for a in arch):
        errors.append(
            "Shallow 'architectural_decisions'. Must contain at least 3 points or highly detailed descriptions (>= 50 chars)."
        )

    # Validate evolution/mechanics depth
    evol = data.get("evolution", [])
    if not evol:
        errors.append("Missing 'evolution'. What factory assets were modified/created?")
    elif len(evol) < 3 and not any(len(str(e).strip()) >= 50 for e in evol):
        errors.append(
            "Shallow 'evolution'. Must contain at least 3 points or highly detailed descriptions (>= 50 chars)."
        )

    # Validate summary
    summary = str(data.get("summary", "")).strip()
    if len(summary) < 50:
        errors.append(
            f"Summary too short ({len(summary)} chars). Provide a meaningful context paragraph (>= 50 chars)."
        )

    if errors:
        print("\n❌ HIGH-FIDELITY REPORTING VIOLATION:")
        for err in errors:
            print(f"  - {err}")
        print(
            "\nThe Plane task closure has been blocked. Revise the solution JSON to meet architectural standards."
        )
        sys.exit(1)


def load_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_solution(data: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=["jinja2.ext.do"],
    )
    template = env.get_template("solution_comment.html.j2")
    return template.render(**data)


def get_issue_uuid(issue_identifier: str, headers: dict) -> str:
    """Resolve AGENT-XX identifier to a UUID."""
    if "-" not in issue_identifier:
        print(f"Error: Invalid issue identifier '{issue_identifier}'. Use AGENT-XX.")
        sys.exit(1)

    seq_str = issue_identifier.split("-")[1]
    try:
        seq = int(seq_str)
    except ValueError:
        print(f"Error: Sequence component must be an integer: {seq_str}")
        sys.exit(1)

    url = f"{API_BASE}/work-items/?sequence_id={seq}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        results = resp.json().get("results", [])
        for item in results:
            if item.get("sequence_id") == seq:
                return item["id"]

    print(f"Error: Could not find issue {issue_identifier} in project.")
    sys.exit(1)


def post_comment(issue_uuid: str, html: str, headers: dict):
    url = f"{API_BASE}/work-items/{issue_uuid}/comments/"
    payload = {"comment_html": html}
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code in (200, 201):
        print("SUCCESS: Posted solution comment.")
    else:
        print(f"Error: {resp.status_code}")
        sys.exit(1)


def close_issue(issue_uuid: str, headers: dict):
    url = f"{API_BASE}/work-items/{issue_uuid}/"
    payload = {"state": DONE_STATE_ID}
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print("SUCCESS: Issue closed (Done).")


def main():
    parser = argparse.ArgumentParser(
        description="Post a professional solution comment to Plane."
    )
    parser.add_argument(
        "--issue", required=True, help="Issue identifier (e.g., AGENT-48)"
    )
    parser.add_argument("--json", required=True, help="Path to JSON solution data")
    parser.add_argument(
        "--close", action="store_true", help="Automatically move issue to 'Done'"
    )
    args = parser.parse_args()

    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN not set.")
        sys.exit(1)

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    data = load_data(args.json)
    validate_depth(data)
    html = render_solution(data)

    issue_uuid = get_issue_uuid(args.issue, headers)
    post_comment(issue_uuid, html, headers)

    if args.close:
        close_issue(issue_uuid, headers)


if __name__ == "__main__":
    main()
