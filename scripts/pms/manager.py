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


def list_issues(project_id: str = None, state_name: str = None, as_json: bool = False):
    logic = [
        "from plane.db.models import Issue, Project",
        "p = Project.objects.get(identifier='AGENT')",
    ]
    if state_name:
        logic.append(
            f"qs = Issue.objects.filter(project=p, state__name='{state_name}').values('sequence_id', 'name', 'priority', 'state__name')"
        )
    else:
        logic.append(
            "qs = Issue.objects.filter(project=p).values('sequence_id', 'name', 'priority', 'state__name')"
        )

    logic.append("print(list(qs))")
    cmd = "; ".join(logic)
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Project Issues: \n{output}")


def list_projects(as_json: bool = False):
    cmd = "from plane.db.models import Project; print(list(Project.objects.values('name', 'identifier')))"
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Projects: \n{output}")


def get_issue_details(sequence_id: str):
    seq_num = sequence_id.split("-")[-1]
    logic = [
        "from plane.db.models import Issue, Project",
        "import json",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
        "data = {'id': str(issue.id), 'sequence_id': issue.sequence_id, 'name': issue.name, 'desc': issue.description_html, 'priority': issue.priority, 'state': issue.state.name}",
        "print('START_JSON')",
        "print(json.dumps(data))",
        "print('END_JSON')",
    ]
    cmd = "; ".join(logic)
    output = run_django_command(cmd)
    # Extract JSON between START_JSON and END_JSON if multiple prints exist
    if "START_JSON" in output and "END_JSON" in output:
        json_part = output.split("START_JSON\n")[-1].split("\nEND_JSON")[0]
        print(json_part)
    else:
        print(output)


def list_cycles():
    cmd = (
        "from plane.db.models import Cycle, Project; "
        "p = Project.objects.get(identifier='AGENT'); "
        "qs = Cycle.objects.filter(project=p).values('name', 'id', 'start_date', 'end_date', 'description'); "
        "print(list(qs))"
    )
    output = run_django_command(cmd)
    print(f"Project Cycles: \n{output}")


def list_states():
    cmd = (
        "from plane.db.models import State, Project; "
        "p = Project.objects.get(identifier='AGENT'); "
        "qs = State.objects.filter(project=p).values('name', 'group'); "
        "print(list(qs))"
    )
    output = run_django_command(cmd)
    print(f"Project States: \n{output}")


def create_issue(
    name: str, description: str = "", priority: str = "medium", state_name: str = "Todo"
):
    logic = [
        "from plane.db.models import Issue, Project, State",
        "p = Project.objects.get(identifier='AGENT')",
        f"s = State.objects.get(project=p, name='{state_name}')",
    ]
    safe_name = repr(name)
    safe_desc = repr("<div>" + description + "</div>")

    logic.append(
        f"issue = Issue.objects.create(project=p, workspace=p.workspace, name={safe_name}, "
        f"description_html={safe_desc}, priority='{priority}', state=s)"
    )
    logic.append("print(f'Created Issue: AGENT-{issue.sequence_id}')")

    cmd = "; ".join(logic)
    output = run_django_command(cmd)
    print(output)


def update_issue(
    sequence_id: str,
    state_name: str = None,
    description: str = None,
    priority: str = None,
    name: str = None,
):
    # Extract number from AGENT-5
    seq_num = sequence_id.split("-")[-1]

    logic = [
        "from plane.db.models import Issue, Project, State",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
    ]
    if state_name:
        logic.append(f"s = State.objects.get(project=p, name='{state_name}')")
        logic.append("issue.state = s")
    if description:
        safe_desc = repr(
            description
        )  # User expected to provide full HTML or plain text we wrap
        if not (description.startswith("<") and description.endswith(">")):
            safe_desc = repr(f"<div>{description}</div>")
        logic.append(f"issue.description_html = {safe_desc}")
    if priority:
        logic.append(f"issue.priority = '{priority}'")
    if name:
        logic.append(f"issue.name = {repr(name)}")

    logic.append("issue.save()")
    logic.append(f"print(f'Updated Issue: AGENT-{seq_num}')")

    cmd = "; ".join(logic)
    output = run_django_command(cmd)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Native Plane PMS Manager")
    subparsers = parser.add_subparsers(dest="command")

    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--project-id", help="Project ID filter")
    list_parser.add_argument(
        "--state", help="Filter by state name (e.g., Todo, Backlog)"
    )
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Details
    details_parser = subparsers.add_parser("details")
    details_parser.add_argument("--id", required=True, help="Issue ID (e.g., AGENT-1)")

    # Cycles
    subparsers.add_parser("cycles")

    # States
    subparsers.add_parser("states")

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
    update_parser.add_argument("--name", help="New name for the issue")

    # Projects
    projects_parser = subparsers.add_parser("projects")
    projects_parser.add_argument("--json", action="store_true")

    # Run Django
    django_parser = subparsers.add_parser("run_django")
    django_parser.add_argument("logic", help="Django ORM logic to run")

    args = parser.parse_args()

    try:
        if args.command == "list":
            list_issues(args.project_id, args.state, args.json)
        elif args.command == "projects":
            list_projects(args.json)
        elif args.command == "details":
            get_issue_details(args.id)
        elif args.command == "cycles":
            list_cycles()
        elif args.command == "states":
            list_states()
        elif args.command == "create":
            create_issue(args.name, args.description, args.priority, args.state)
        elif args.command == "update":
            update_issue(
                args.id, args.state, args.description, args.priority, args.name
            )
        elif args.command == "run_django":
            print(run_django_command(args.logic))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
