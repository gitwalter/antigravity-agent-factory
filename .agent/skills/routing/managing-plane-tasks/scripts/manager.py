import os
import sys
import subprocess
import argparse
import json

# Correct environment path as per user rules
CONDA_EXEC = r"conda run -p D:\Anaconda\envs\cursor-factory"

import base64


def run_django_command(command: str):
    """Execute a command in the plane-api container using manage.py shell."""
    # Base64 encode the command to avoid shell character issues (<, >, quotes, etc.)
    encoded_cmd = base64.b64encode(command.encode()).decode()
    docker_cmd = f"docker exec plane-api python manage.py shell -c \"import base64; exec(base64.b64decode('{encoded_cmd}').decode())\""
    result = subprocess.run(docker_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Docker command failed: {result.stderr}")
    return result.stdout.strip()


def list_issues(project_id: str = None):
    cmd = (
        "from plane.db.models import Issue, Project; "
        "p = Project.objects.get(identifier='AGENT'); "
        "qs = Issue.objects.filter(project=p).values('sequence_id', 'name', 'priority', 'state__name'); "
        "print(list(qs))"
    )
    output = run_django_command(cmd)
    print(f"Project Issues: \n{output}")


def list_cycles():
    cmd = (
        "from plane.db.models import Cycle, Project; "
        "p = Project.objects.get(identifier='AGENT'); "
        "qs = Cycle.objects.filter(project=p).values('name', 'id', 'start_date', 'end_date', 'description'); "
        "print(list(qs))"
    )
    output = run_django_command(cmd)
    print(f"Project Cycles: \n{output}")


def create_issue(
    name: str, description: str = "", priority: str = "medium", state_name: str = "Todo"
):
    cmd = (
        f"from plane.db.models import Issue, Project, State; "
        f"p = Project.objects.get(identifier='AGENT'); "
        f"s = State.objects.get(project=p, name='{state_name}'); "
        f"issue = Issue.objects.create(project=p, workspace=p.workspace, name='{name}', "
        f"description_html='<p>{description}</p>', priority='{priority}', state=s); "
        f"print(f'Created Issue: AGENT-{{issue.sequence_id}}')"
    )
    output = run_django_command(cmd)
    print(output)


def update_issue(
    sequence_id: str,
    state_name: str = None,
    description: str = None,
    priority: str = None,
):
    # Extract number from AGENT-5
    seq_num = sequence_id.split("-")[-1]

    logic = [
        "from plane.db.models import Issue, Project, State",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
    ]
    if state_name:
        logic.append(
            f"s = State.objects.get(project=p, name='{state_name}'); issue.state = s"
        )
    if description:
        # Use repr to handle nested quotes safely
        safe_desc = "<div>" + description + "</div>"
        logic.append(f"issue.description_html = {repr(safe_desc)}")
    if priority:
        logic.append(f"issue.priority = '{priority}'")

    logic.append("issue.save()")
    logic.append(f"print('Updated Issue {sequence_id}')")

    cmd = "; ".join(logic)
    output = run_django_command(cmd)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Native Plane PMS Manager")
    subparsers = parser.add_subparsers(dest="command")

    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--project-id", help="Project ID filter")

    # Cycles
    subparsers.add_parser("cycles")

    # Create
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--description", default="")
    create_parser.add_argument("--priority", default="medium")
    create_parser.add_argument("--state", default="Todo")

    # Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "--id", required=True, help="Issue identifier (e.g., AGENT-5)"
    )
    update_parser.add_argument("--state", help="New state for the issue")
    update_parser.add_argument(
        "--description", help="New HTML description for the issue"
    )
    update_parser.add_argument("--priority", help="New priority for the issue")

    args = parser.parse_args()

    try:
        if args.command == "list":
            list_issues(args.project_id)
        elif args.command == "cycles":
            list_cycles()
        elif args.command == "create":
            create_issue(args.name, args.description, args.priority, args.state)
        elif args.command == "update":
            update_issue(args.id, args.state, args.description, args.priority)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
