import os
import sys
import json
import argparse
import requests
from jinja2 import Environment, FileSystemLoader

# Configuration
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTEXT_FILE = os.path.join(SKILL_ROOT, "references", "project_context.json")
TEMPLATE_DIR = os.path.join(SKILL_ROOT, "templates")


def load_context():
    """Load persistent context for IDs and mappings."""
    if os.path.exists(CONTEXT_FILE):
        try:
            with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load context file: {e}")
    return {}


# Default fallback config
context = load_context()
WORKSPACE_SLUG = "agent-factory"
PROJECT_ID = "e71eb003-87d4-4b0c-a765-a044ac5affbe"
API_BASE = (
    f"https://api.plane.so/api/v1/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}"
)
DONE_STATE_ID = "ef4b2395-3edb-41e9-adcd-7ec77d534f0f"  # Verified via MCP for 'Done'


def validate_depth(data: dict):
    """Ensure the solution report has sufficient technical depth."""
    required_keys = [
        "summary",
        "changes",
        "verification_evidence",
        "evolution",
        "architectural_decisions",
    ]
    missing = [k for k in required_keys if k not in data or not data[k]]
    if missing:
        print(
            f"\n[X] ARCHITECTURAL BLOCKER:\n    -> Missing required solution fields: {', '.join(missing)}"
        )
        sys.exit(1)

    if len(data.get("summary", "")) < 20:
        print("\n[X] ARCHITECTURAL BLOCKER:\n    -> Solution 'summary' is too brief.")
        sys.exit(1)

    if not data.get("verification_evidence"):
        print("\n[X] ARCHITECTURAL BLOCKER:\n    -> Missing 'verification_evidence'.")
        sys.exit(1)

    long_evidence = [e for e in data["verification_evidence"] if len(e) > 10]
    if not long_evidence:
        print(
            "\n[X] ARCHITECTURAL BLOCKER:\n    -> 'verification_evidence' must contain at least one descriptive item."
        )
        sys.exit(1)


def render_solution(data: dict) -> str:
    """Render the solution report using Jinja2."""
    file_loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=file_loader)
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

    print(f"Error: Could not find issue {issue_identifier}. URL: {url}")
    sys.exit(1)


def get_existing_comments(issue_uuid: str, headers: dict) -> list:
    """Fetch existing comments for the issue."""
    url = f"{API_BASE}/work-items/{issue_uuid}/comments/"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("results", [])
    return []


def post_comment(issue_uuid: str, html: str, headers: dict):
    """Post a comment if a similar one doesn't exist."""
    existing = get_existing_comments(issue_uuid, headers)

    import re

    def clean(node):
        return re.sub("<[^<]+?>", "", node).strip().lower()

    clean_new = clean(html)
    for comment in existing:
        if clean(comment.get("comment_html", "")) == clean_new:
            print("INFO: Solution comment already exists. Skipping.")
            return

    url = f"{API_BASE}/work-items/{issue_uuid}/comments/"
    payload = {"comment_html": html}
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 201:
        print("SUCCESS: Solution comment posted to Plane.")
    else:
        print(f"Error posting comment: {resp.status_code} - {resp.text} - URL: {url}")


def close_issue(issue_uuid: str, headers: dict):
    url = f"{API_BASE}/work-items/{issue_uuid}/"
    payload = {"state": DONE_STATE_ID}
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print("SUCCESS: Issue closed (Done).")
    else:
        print(f"Error closing issue: {resp.status_code} - {resp.text}")


def main():
    parser = argparse.ArgumentParser(description="Post Solution to Plane")
    parser.add_argument("--issue", required=True, help="AGENT-XX or UUID")
    parser.add_argument("--json", help="Path to JSON")
    parser.add_argument("--close", action="store_true")
    parser.add_argument("--summary", help="Summary")
    parser.add_argument("--changes", help="Semicolon separated")
    parser.add_argument("--verification-evidence", help="Semicolon separated")
    parser.add_argument("--evolution", help="Semicolon separated")
    parser.add_argument("--architectural-decisions", help="Semicolon separated")
    parser.add_argument("--lessons-learned", help="Semicolon separated")

    args = parser.parse_args()

    api_key = os.environ.get("PLANE_API_TOKEN")
    if not api_key:
        print("Error: PLANE_API_TOKEN not set.")
        sys.exit(1)

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    data = {}
    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)

    def split_arg(a):
        return [x.strip() for x in a.split(";") if x.strip()] if a else None

    if args.summary:
        data["summary"] = args.summary
    if args.changes:
        data["changes"] = split_arg(args.changes)
    if args.verification_evidence:
        data["verification_evidence"] = split_arg(args.verification_evidence)
    if args.evolution:
        data["evolution"] = split_arg(args.evolution)
    if args.architectural_decisions:
        data["architectural_decisions"] = split_arg(args.architectural_decisions)
    if args.lessons_learned:
        data["lessons_learned"] = split_arg(args.lessons_learned)

    issue_identifier = args.issue
    if "-" in issue_identifier and len(issue_identifier) > 20:
        issue_uuid = issue_identifier
    else:
        issue_uuid = get_issue_uuid(issue_identifier, headers)

    validate_depth(data)
    html = render_solution(data)
    post_comment(issue_uuid, html, headers)

    if args.close:
        close_issue(issue_uuid, headers)


if __name__ == "__main__":
    main()
