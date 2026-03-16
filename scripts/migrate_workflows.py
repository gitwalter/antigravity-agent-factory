import os
import sys
from pathlib import Path

# Add the project root to sys.path
root_dir = Path(r"d:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory")
sys.path.append(str(root_dir))

from scripts.api.workflow_service import parse_workflow, save_workflow


def migrate_workflows():
    workflows_dir = root_dir / ".agent" / "workflows"
    # Recursive glob to find nested workflows
    md_files = list(workflows_dir.rglob("*.md"))
    print(f"Found {len(md_files)} workflows to migrate.")

    success_count = 0
    fail_count = 0

    for md_file in md_files:
        try:
            # Preserve relative structure for save_workflow
            rel_path = md_file.relative_to(workflows_dir).with_suffix("")
            filename = str(rel_path).replace("\\", "/")

            print(f"Migrating: {filename}.md")

            # parse_workflow takes filename relative to .agent/workflows/
            workflow = parse_workflow(f"{filename}.md")

            # save_workflow handles the rest
            save_workflow(filename, workflow, raw_body=None)

            success_count += 1
        except Exception as e:
            print(f"Failed to migrate {md_file}: {str(e)}")
            # import traceback
            # traceback.print_exc()
            fail_count += 1

    print("\nMigration Complete!")
    print(f"Successfully migrated: {success_count}")
    print(f"Failed: {fail_count}")


if __name__ == "__main__":
    migrate_workflows()
