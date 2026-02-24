import os
import re
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from projects.statistical_dashboards.core.database import (
    DatabaseManager,
    Project,
    ProjectTask,
)


def parse_task_md(file_path):
    tasks = []
    current_phase = ""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        # Match phase headers
        phase_match = re.match(r"^\s*-\s*\[[x/ ]\]\s*(Phase \d+:.*)", line)
        if phase_match:
            current_phase = phase_match.group(1).strip()
            continue

        # Match task items
        task_match = re.match(r"^\s*-\s*\[([x/ ])\]\s*(.*)", line)
        if task_match:
            status_char = task_match.group(1)
            title = task_match.group(2).strip()
            if title and not title.startswith("Phase"):
                is_completed = 1 if status_char == "x" else 0
                tasks.append(
                    {
                        "title": title,
                        "description": f"Component of {current_phase}"
                        if current_phase
                        else "General Task",
                        "is_completed": is_completed,
                    }
                )
    return tasks


def sync_to_db():
    project_name = "Statistical Dashboard Masterplan"
    task_md_path = "C:/Users/wpoga/.gemini/antigravity/brain/2be546a4-efe7-4194-8b80-5fa52924d5da/task.md"

    if not os.path.exists(task_md_path):
        print(f"Error: task.md not found at {task_md_path}")
        return

    print(f"Parsing tasks from {task_md_path}...")
    tasks_to_sync = parse_task_md(task_md_path)
    print(f"Found {len(tasks_to_sync)} tasks.")

    db = DatabaseManager()
    session = db.get_session()

    try:
        # 1. Find or Create Project
        project = session.query(Project).filter_by(name=project_name).first()
        if not project:
            print(f"Creating project: {project_name}")
            project = Project(
                name=project_name,
                description="Consolidated masterplan project for the Statistical Dashboard implementation.",
                status="In Progress",
                priority="High",
                progress=0.0,
                target_date=datetime.now(),
            )
            session.add(project)
            session.commit()
            session.refresh(project)
        else:
            print(f"Found existing project: {project_name}")

        # 2. Sync Tasks
        existing_tasks = {t.title: t for t in project.tasks}

        for t_info in tasks_to_sync:
            title = t_info["title"]
            if title in existing_tasks:
                # Update existing task
                task = existing_tasks[title]
                if task.is_completed != t_info["is_completed"]:
                    print(
                        f"Updating task: {title} (Status -> {t_info['is_completed']})"
                    )
                    task.is_completed = t_info["is_completed"]
            else:
                # Create new task
                print(f"Creating task: {title}")
                new_task = ProjectTask(
                    project_id=project.id,
                    title=title,
                    description=t_info["description"],
                    is_completed=t_info["is_completed"],
                )
                session.add(new_task)

        session.commit()

        # 3. Update Project Progress
        total = len(project.tasks)
        completed = sum(1 for t in project.tasks if t.is_completed)
        if total > 0:
            project.progress = (completed / total) * 100
            print(f"Project progress updated to {project.progress:.1f}%")

        session.commit()
        print("Synchronization completed successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error during sync: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    sync_to_db()
