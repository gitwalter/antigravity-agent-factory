import os
import sys
import subprocess
import argparse
import json
from datetime import datetime

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


def list_issues(
    project_id: str = None,
    state_name: str = None,
    cycle_name: str = None,
    module_name: str = None,
    as_json: bool = False,
):
    logic = [
        "from plane.db.models import Issue, Project",
        "p = Project.objects.get(identifier='AGENT')",
        "filters = {'project': p}",
    ]
    if state_name:
        logic.append(f"filters['state__name'] = '{state_name}'")
    if cycle_name:
        logic.append(f"filters['issue_cycle__cycle__name'] = '{cycle_name}'")
    if module_name:
        logic.append(f"filters['issue_module__module__name'] = '{module_name}'")

    logic.append(
        "qs = Issue.objects.filter(**filters).values('sequence_id', 'name', 'priority', 'state__name').distinct()"
    )
    logic.append("print(list(qs))")
    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Project Issues: \n{output}")


def list_modules(as_json: bool = False):
    cmd = "from plane.db.models import Module, Project; p = Project.objects.get(identifier='AGENT'); print(list(Module.objects.filter(project=p).values('name', 'id')))"
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Modules: \n{output}")


def list_projects(as_json: bool = False):
    cmd = "from plane.db.models import Project; print(list(Project.objects.values('name', 'identifier')))"
    output = run_django_command(cmd)
    if as_json:
        print(output)
    else:
        print(f"Projects: \n{output}")


def get_issue_details(sequence_id: str, as_json: bool = False):
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
    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    # Extract JSON between START_JSON and END_JSON if multiple prints exist
    if "START_JSON" in output and "END_JSON" in output:
        json_part = output.split("START_JSON\n")[-1].split("\nEND_JSON")[0]
        if as_json:
            print(json_part)
        else:
            try:
                data = json.loads(json_part)
                print(
                    f"================ AGENT-{data.get('sequence_id')} ================"
                )
                print(f"Title: {data.get('name')}")
                print(f"Priority: {data.get('priority')}")
                print(f"State: {data.get('state')}")
                print(f"\nDescription:\n{data.get('desc', '')}")
                print("==============================================")
            except Exception as e:
                print(f"Failed to parse details: {e}")
                print(output)
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
    name: str,
    description: str = "",
    priority: str = "medium",
    state_name: str = "Todo",
    cycle_name: str = None,
    module_name: str = None,
    assignee_email: str = None,
    start_date: str = None,
    target_date: str = None,
    estimate: int = None,
    labels: list = None,
):
    logic = [
        "from plane.db.models import Issue, Project, State, Cycle, Module, ProjectMember, Label, EstimatePoint",
        "from django.utils import timezone",
        "p = Project.objects.get(identifier='AGENT')",
        f"s = State.objects.get(project=p, name='{state_name}')",
    ]
    safe_name = repr(name)
    safe_desc = repr("<div>" + description + "</div>")

    create_args = [
        "project=p",
        "workspace=p.workspace",
        f"name={safe_name}",
        f"description_html={safe_desc}",
        f"priority='{priority}'",
        "state=s",
    ]

    if start_date:
        logic.append(
            f"start = timezone.datetime.strptime('{start_date}', '%Y-%m-%d').date()"
        )
        create_args.append("start_date=start")
    if target_date:
        logic.append(
            f"target = timezone.datetime.strptime('{target_date}', '%Y-%m-%d').date()"
        )
        create_args.append("target_date=target")

    if estimate is not None:
        logic.append(
            f"ep = EstimatePoint.objects.filter(estimate__project=p, value={estimate}).first()"
        )
        create_args.append("estimate_point=ep")

    logic.append(f"issue = Issue.objects.create({', '.join(create_args)})")

    if assignee_email:
        logic.append(
            f"member = ProjectMember.objects.get(project=p, member__email='{assignee_email}')"
        )
        logic.append(
            "issue.issue_assignee.create(assignee=member.member, project=p, workspace=p.workspace)"
        )

    if labels:
        for label in labels:
            logic.append(f"l = Label.objects.get(project=p, name='{label}')")
            logic.append(
                "issue.label_issue.create(label=l, project=p, workspace=p.workspace)"
            )

    if cycle_name:
        logic.append(f"c = Cycle.objects.get(project=p, name='{cycle_name}')")
        logic.append(
            "from django.apps import apps; CI = apps.get_model('db', 'CycleIssue')"
        )
        logic.append(
            "CI.objects.create(issue=issue, cycle=c, project=p, workspace=p.workspace)"
        )

    if module_name:
        logic.append(f"m = Module.objects.get(project=p, name='{module_name}')")
        logic.append(
            "from django.apps import apps; MI = apps.get_model('db', 'ModuleIssue')"
        )
        logic.append(
            "MI.objects.create(issue=issue, module=m, project=p, workspace=p.workspace)"
        )

    logic.append("print(f'Created Issue: AGENT-{issue.sequence_id}')")

    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    print(output)


def update_issue(
    sequence_id: str,
    state_name: str = None,
    description: str = None,
    priority: str = None,
    name: str = None,
    append: bool = False,
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
        if append:
            # Append logic: wrap in div if not already, add timestamp and separator
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            separator = "<hr/>"

            if not (description.startswith("<") and description.endswith(">")):
                new_part = f"<div><b>Update ({timestamp}):</b><br/>{description}</div>"
            else:
                new_part = f"<div><b>Update ({timestamp}):</b></div>{description}"

            logic.append("current_desc = issue.description_html or ''")
            # Ensure we don't double up separators if it's the first append
            logic.append(
                f"if current_desc and not current_desc.endswith('{separator}'):"
            )
            logic.append(f"    current_desc += '{separator}'")
            logic.append(f"issue.description_html = current_desc + {repr(new_part)}")
        else:
            safe_desc = repr(description)
            if not (description.startswith("<") and description.endswith(">")):
                safe_desc = repr(f"<div>{description}</div>")
            logic.append(f"issue.description_html = {safe_desc}")
    if priority:
        logic.append(f"issue.priority = '{priority}'")
    if name:
        logic.append(f"issue.name = {repr(name)}")

    logic.append("issue.save()")
    logic.append(f"print(f'Updated Issue: AGENT-{seq_num}')")

    cmd = "\n".join(logic)
    output = run_django_command(cmd)
    print(output)


def create_comment(sequence_id: str, comment: str):
    if not comment.strip():
        print("Error: Comment cannot be empty.")
        return

    # Extract number from AGENT-5
    seq_num = sequence_id.split("-")[-1]

    logic = [
        "from plane.db.models import Issue, Project, IssueComment",
        "p = Project.objects.get(identifier='AGENT')",
        f"issue = Issue.objects.get(project=p, sequence_id={seq_num})",
    ]

    # Wrap in consistent HTML if not already
    if not (comment.strip().startswith("<") and comment.strip().endswith(">")):
        safe_comment = repr(f"<div>{comment.strip()}</div>")
    else:
        safe_comment = repr(comment.strip())

    # Use the project owner/workspace owner as the creator if possible
    logic.append("user = p.workspace.owner")
    logic.append(
        f"IssueComment.objects.create(issue=issue, project=p, workspace=p.workspace, "
        f"comment_html={safe_comment}, created_by=user, actor=user)"
    )
    logic.append(f"print(f'Added comment to Issue: AGENT-{seq_num}')")

    cmd = "\n".join(logic)
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
    list_parser.add_argument("--cycle", help="Filter by cycle/sprint name")
    list_parser.add_argument("--module", help="Filter by module name")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Details
    details_parser = subparsers.add_parser("details", aliases=["get"])
    details_parser.add_argument("id", help="Issue ID (e.g., AGENT-1 or simply 1)")
    details_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Cycles
    subparsers.add_parser("cycles")

    # States
    subparsers.add_parser("states")

    # Modules
    modules_parser = subparsers.add_parser("modules")
    modules_parser.add_argument("--json", action="store_true")

    # Create
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--description", default="")
    create_parser.add_argument("--priority", default="medium")
    create_parser.add_argument("--state", default="Todo")
    create_parser.add_argument("--cycle", help="Cycle/Sprint name")
    create_parser.add_argument("--module", help="Module name")
    create_parser.add_argument("--assignee", help="Assignee email")
    create_parser.add_argument("--start-date", help="YYYY-MM-DD")
    create_parser.add_argument("--target-date", help="YYYY-MM-DD")
    create_parser.add_argument("--estimate", type=int, help="Estimate value")
    create_parser.add_argument("--labels", nargs="+", help="Space-separated labels")

    # Metadata lists
    members_parser = subparsers.add_parser("members")
    members_parser.add_argument("--json", action="store_true")
    labels_parser = subparsers.add_parser("labels")
    labels_parser.add_argument("--json", action="store_true")

    # Update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "id", help="Issue identifier (e.g., AGENT-5 or simply 5)"
    )
    update_parser.add_argument("--state", help="New state for the issue")
    update_parser.add_argument(
        "--description", help="New HTML description or text for the issue"
    )
    update_parser.add_argument(
        "--append", action="store_true", help="Append to existing description"
    )
    update_parser.add_argument("--priority", help="New priority for the issue")
    update_parser.add_argument("--name", help="New name for the issue")

    # Comment
    comment_parser = subparsers.add_parser("comment")
    comment_parser.add_argument(
        "id", help="Issue identifier (e.g., AGENT-5 or simply 5)"
    )
    comment_parser.add_argument("--comment", required=True, help="Comment text or HTML")

    # Projects
    projects_parser = subparsers.add_parser("projects")
    projects_parser.add_argument("--json", action="store_true")

    # Run Django
    django_parser = subparsers.add_parser("run_django")
    django_parser.add_argument("logic", help="Django ORM logic to run")

    args = parser.parse_args()

    try:
        if args.command == "list":
            list_issues(args.project_id, args.state, args.cycle, args.module, args.json)
        elif args.command == "projects":
            list_projects(args.json)
        elif args.command == "modules":
            list_modules(args.json)
        elif args.command == "members":
            output = run_django_command(
                "from plane.db.models import ProjectMember, Project; p = Project.objects.get(identifier='AGENT'); print(list(ProjectMember.objects.filter(project=p).values('member__email', 'member__first_name', 'member__last_name')))"
            )
            if args.json:
                print(output)
            else:
                print(f"Project Members: \n{output}")
        elif args.command == "labels":
            output = run_django_command(
                "from plane.db.models import Label, Project; p = Project.objects.get(identifier='AGENT'); print(list(Label.objects.filter(project=p).values('name', 'id')))"
            )
            if args.json:
                print(output)
            else:
                print(f"Project Labels: \n{output}")
        elif args.command in ["details", "get"]:
            get_issue_details(args.id, getattr(args, "json", False))
        elif args.command == "cycles":
            list_cycles()
        elif args.command == "states":
            list_states()
        elif args.command == "create":
            create_issue(
                args.name,
                args.description,
                args.priority,
                args.state,
                args.cycle,
                args.module,
                args.assignee,
                args.start_date,
                args.target_date,
                args.estimate,
                args.labels,
            )
        elif args.command == "update":
            update_issue(
                args.id,
                args.state,
                args.description,
                args.priority,
                args.name,
                args.append,
            )
        elif args.command == "comment":
            create_comment(args.id, args.comment)
        elif args.command == "run_django":
            print(run_django_command(args.logic))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
